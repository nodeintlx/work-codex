from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
import json
from pathlib import Path
import shutil
import re
from typing import Any

from .actions import build_strategic_actions
from .drafting import write_draft_bundle
from .filing import load_filing_package
from .litigation import artifact_gaps, load_litigation_matter
from .store import SafeWorkspaceStore, StoreError


@dataclass(frozen=True)
class IngestedArtifact:
    kind: str
    proposal_id: str
    title: str
    source_path: Path
    queue_path: Path


@dataclass(frozen=True)
class AppliedProposal:
    proposal_id: str
    title: str
    archive_path: Path
    messages: list[str]


def write_litigation_handoff(root: Path, exchange_root: Path, *, today: date | None = None) -> list[Path]:
    payload = build_litigation_handoff(root, today=today)
    local_path = root / "agent-exchange" / "handoff" / "litigation-handoff.json"
    remote_path = exchange_root / "handoff" / "litigation-handoff.json"
    for path in (local_path, remote_path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return [local_path, remote_path]


def build_litigation_handoff(root: Path, *, today: date | None = None) -> dict[str, Any]:
    current_day = today or date.today()
    matter = load_litigation_matter(root)
    package = load_filing_package(root)
    latest_bundle_dir = _latest_bundle_dir(root)
    latest_bundle_files = []
    if latest_bundle_dir.exists():
        latest_bundle_files = sorted(path.name for path in latest_bundle_dir.glob("*.md"))

    actions = build_strategic_actions(root, current_day)
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "matter": {
            "name": matter.matter,
            "status": matter.status,
            "phase": matter.phase,
            "current_track": matter.current_track,
            "canadian_path": matter.canadian_path,
            "representation_mode": matter.representation_mode,
            "filing_readiness": matter.filing_readiness,
            "protective_filing_needed": matter.protective_filing_needed,
            "opening": matter.opening,
            "floor": matter.floor,
            "ton_zone": matter.ton_zone,
            "latest_assessment": matter.latest_assessment,
            "latest_next_step": matter.latest_next_step,
            "live_next_actions": matter.live_next_actions,
            "live_notes": matter.live_notes,
        },
        "filing": {
            "readiness": package.readiness.level,
            "critical_claims_ready": package.readiness.critical_claims_ready,
            "critical_evidence_missing": package.readiness.critical_evidence_missing,
            "recommendations": package.readiness.recommendations,
        },
        "claims": [
            {
                "claim_id": claim.claim_id,
                "title": claim.title,
                "status": claim.status,
                "forum_track": claim.forum_track,
                "priority": claim.pleading_priority,
            }
            for claim in package.claims
        ],
        "chronology": [
            {
                "event_id": event.event_id,
                "date": event.date,
                "title": event.title,
            }
            for event in package.chronology
        ],
        "next_actions": [
            {
                "title": action.title,
                "priority": action.priority,
                "rationale": action.rationale,
                "settlement_pressure": action.settlement_pressure,
            }
            for action in actions
        ],
        "artifact_gaps": [
            {
                "label": gap.label,
                "path": str(gap.path),
            }
            for gap in artifact_gaps(matter)
        ],
        "latest_bundle": {
            "path": str(latest_bundle_dir),
            "files": latest_bundle_files,
        },
        "agent_proposals": proposal_status_summary(root),
    }


def ingest_exchange_artifacts(root: Path, exchange_root: Path) -> list[IngestedArtifact]:
    incoming_dir = exchange_root / "incoming"
    if not incoming_dir.exists():
        return []

    ledger_path = root / "agent-exchange" / "ingest-log.json"
    ledger = _load_json_file(ledger_path, default={"sources": {}})
    sources = ledger.setdefault("sources", {})
    pending_dir = root / "agent-exchange" / "pending_review"
    pending_dir.mkdir(parents=True, exist_ok=True)

    ingested: list[IngestedArtifact] = []
    for source_path in sorted(path for path in incoming_dir.rglob("*") if path.is_file()):
        signature = _source_signature(incoming_dir, source_path)
        if signature in sources:
            continue
        records = _records_from_source(root, source_path)
        for record in records:
            queue_name = _unique_queue_name(pending_dir, record["proposal_id"])
            queue_path = pending_dir / f"{queue_name}.json"
            queue_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            ingested.append(
                IngestedArtifact(
                    kind=str(record.get("kind", "proposal")),
                    proposal_id=str(record.get("proposal_id", "")),
                    title=str(record.get("title", "")),
                    source_path=source_path,
                    queue_path=queue_path,
                )
            )
            sources[signature] = str(queue_path)

    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return ingested


def pending_review_entries(root: Path) -> list[dict[str, Any]]:
    pending_dir = root / "agent-exchange" / "pending_review"
    entries: list[dict[str, Any]] = []
    if not pending_dir.exists():
        return entries
    for path in sorted(pending_dir.glob("*.json")):
        payload = _load_json_file(path, default={})
        if isinstance(payload, dict):
            payload["_path"] = str(path)
            entries.append(payload)
    return entries


def proposal_status_summary(root: Path) -> dict[str, int]:
    counts = {"pending_review": 0, "applied": 0, "rejected": 0}
    base = root / "agent-exchange"
    for status in counts:
        status_dir = base / status
        if status_dir.exists():
            counts[status] = len(list(status_dir.glob("*.json")))
    return counts


def apply_agent_proposal(root: Path, proposal_path: Path) -> AppliedProposal:
    payload = _load_json_file(proposal_path, default=None)
    if not isinstance(payload, dict):
        raise StoreError(f"proposal file did not load as an object: {proposal_path}")

    actions = _proposal_actions(payload)
    if not actions:
        raise StoreError(f"proposal has no machine-applicable actions: {proposal_path}")
    if str(payload.get("status", "")).strip().lower() == "rejected":
        raise StoreError(f"proposal is rejected and cannot be applied: {proposal_path}")

    store = SafeWorkspaceStore(root)
    messages: list[str] = []
    needs_bundle_refresh = False

    for action in actions:
        command = str(action.get("command", "")).strip()
        if command == "litigation-update":
            result = store.update_litigation_status(_action_fields(action))
            messages.append(result.message)
            needs_bundle_refresh = True
            continue
        if command == "settlement-update":
            result = store.update_settlement_tracker(_action_fields(action))
            messages.append(result.message)
            needs_bundle_refresh = True
            continue
        if command == "settlement-round-add":
            record = action.get("record", action.get("json"))
            if not isinstance(record, dict):
                raise StoreError("settlement-round-add requires a JSON object under 'record' or 'json'")
            result = store.append_settlement_round(record)
            messages.append(result.message)
            needs_bundle_refresh = True
            continue
        if command == "task-add":
            fields = action.get("fields", {})
            if not isinstance(fields, dict):
                raise StoreError("task-add requires an object under 'fields'")
            result = store.add_task(
                title=str(fields["title"]),
                company=str(fields["company"]),
                priority=str(fields["priority"]),
                due=str(fields["due"]) if fields.get("due") not in (None, "") else None,
                notes=str(fields.get("notes", "")),
                status=str(fields.get("status", "todo")),
                created=str(fields["created"]) if fields.get("created") not in (None, "") else None,
            )
            messages.append(result.message)
            continue
        if command == "task-update":
            fields = action.get("fields", {})
            if not isinstance(fields, dict):
                raise StoreError("task-update requires an object under 'fields'")
            if "id" not in fields:
                raise StoreError("task-update requires 'id' in fields")
            result = store.update_task(
                task_id=int(fields["id"]),
                title=_optional_text(fields.get("title")),
                company=_optional_text(fields.get("company")),
                priority=_optional_text(fields.get("priority")),
                status=_optional_text(fields.get("status")),
                due=_optional_text(fields.get("due")),
                notes=_optional_text(fields.get("notes")),
                append_note=_optional_text(fields.get("append_note")),
            )
            messages.append(result.message)
            continue
        if command == "memory-append":
            record = action.get("record", action.get("json"))
            if not isinstance(record, dict):
                raise StoreError("memory-append requires a JSON object under 'record' or 'json'")
            result = store.append_memory(record)
            messages.append(result.message)
            continue
        if command == "draft-write-bundle":
            package = load_filing_package(root)
            matter = load_litigation_matter(root)
            written_paths = write_draft_bundle(root, package, matter)
            messages.append(f"wrote draft bundle ({len(written_paths)} files)")
            needs_bundle_refresh = False
            continue
        raise StoreError(f"unsupported proposal command: {command}")

    if needs_bundle_refresh:
        package = load_filing_package(root)
        matter = load_litigation_matter(root)
        written_paths = write_draft_bundle(root, package, matter)
        messages.append(f"wrote draft bundle ({len(written_paths)} files)")

    applied_dir = root / "agent-exchange" / "applied"
    applied_dir.mkdir(parents=True, exist_ok=True)
    archive_path = applied_dir / f"{_slugify(str(payload.get('proposal_id') or proposal_path.stem))}.json"
    if archive_path.exists():
        archive_path = applied_dir / f"{_slugify(str(payload.get('proposal_id') or proposal_path.stem))}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}.json"

    archived_payload = dict(payload)
    archived_payload["status"] = "applied"
    archived_payload["applied_at"] = datetime.now(UTC).isoformat()
    archived_payload["apply_results"] = messages
    archive_path.write_text(json.dumps(archived_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    pending_dir = root / "agent-exchange" / "pending_review"
    if proposal_path.parent == pending_dir and proposal_path.exists():
        proposal_path.unlink()

    return AppliedProposal(
        proposal_id=str(archived_payload.get("proposal_id", proposal_path.stem)),
        title=str(archived_payload.get("title", proposal_path.stem)),
        archive_path=archive_path,
        messages=messages,
    )


def _latest_bundle_dir(root: Path) -> Path:
    return root / "nrg-bloom" / "litigation-ton" / "generated" / "latest"


def _source_signature(incoming_dir: Path, source_path: Path) -> str:
    relative = source_path.relative_to(incoming_dir).as_posix()
    stat = source_path.stat()
    return f"{relative}:{stat.st_size}:{stat.st_mtime_ns}"


def _records_from_source(root: Path, source_path: Path) -> list[dict[str, Any]]:
    if source_path.suffix.lower() == ".json":
        raw = _load_json_file(source_path, default=None)
        if isinstance(raw, dict) and isinstance(raw.get("proposals"), list):
            return [
                _normalize_proposal_record(item, source_path=source_path)
                for item in raw["proposals"]
                if isinstance(item, dict)
            ]
        if isinstance(raw, dict) and _looks_like_proposal(raw):
            return [_normalize_proposal_record(raw, source_path=source_path)]
    return [_manual_review_record(root, source_path)]


def _manual_review_record(root: Path, source_path: Path) -> dict[str, Any]:
    evidence_dir = root / "agent-exchange" / "evidence" / "incoming"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    copied_name = f"{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}-{source_path.name}"
    copied_path = evidence_dir / copied_name
    shutil.copy2(source_path, copied_path)
    proposal_id = _slugify(source_path.stem) or "manual-review"
    return {
        "proposal_id": proposal_id,
        "title": f"Manual review required: {source_path.name}",
        "status": "pending_review",
        "kind": "manual_review",
        "source_artifact": str(source_path),
        "copied_artifact": str(copied_path),
        "actions": [],
    }


def _normalize_proposal_record(payload: dict[str, Any], *, source_path: Path) -> dict[str, Any]:
    proposal_id = str(payload.get("proposal_id") or payload.get("id") or source_path.stem).strip() or source_path.stem
    title = str(payload.get("title") or payload.get("summary") or proposal_id)
    status = str(payload.get("status") or "pending_review")
    actions = _proposal_actions(payload)
    kind = "proposal" if actions else "manual_review"
    return {
        "proposal_id": _slugify(proposal_id),
        "title": title,
        "status": status,
        "kind": kind,
        "source_artifact": str(source_path),
        "summary": str(payload.get("summary", "")).strip(),
        "rationale": str(payload.get("rationale", "")).strip(),
        "actions": actions,
    }


def _proposal_actions(payload: dict[str, Any]) -> list[dict[str, Any]]:
    actions = payload.get("actions")
    if isinstance(actions, list):
        return [item for item in actions if isinstance(item, dict)]
    if _looks_like_proposal(payload):
        action = dict(payload)
        if "command" in action:
            return [action]
    return []


def _looks_like_proposal(payload: dict[str, Any]) -> bool:
    return "command" in payload or "actions" in payload


def _action_fields(action: dict[str, Any]) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    raw_fields = action.get("fields")
    if isinstance(raw_fields, dict):
        fields.update(raw_fields)
    raw_set = action.get("set")
    if isinstance(raw_set, dict):
        fields.update(raw_set)
    raw_set_json = action.get("set_json")
    if isinstance(raw_set_json, dict):
        fields.update(raw_set_json)
    return fields


def _optional_text(value: Any) -> str | None:
    if value in (None, ""):
        return None
    return str(value)


def _unique_queue_name(directory: Path, proposal_id: str) -> str:
    base = _slugify(proposal_id) or "proposal"
    candidate = base
    index = 2
    while (directory / f"{candidate}.json").exists():
        candidate = f"{base}-{index}"
        index += 1
    return candidate


def _slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip().lower()).strip("-")
    return normalized or "proposal"


def _load_json_file(path: Path, *, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
