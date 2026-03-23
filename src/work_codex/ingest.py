from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
import json
from pathlib import Path
import re
import shutil
from typing import Any

from .drafting import write_draft_bundle
from .exchange import init_agent_exchange, write_exchange_payload
from .filing import load_filing_package
from .handoff import build_litigation_handoff
from .litigation import load_litigation_matter
from .proposals import record_agent_proposal, supersede_matching_proposals
from .store import SafeWorkspaceStore, StoreError


TON_MATTER = "NRG Bloom Inc. v. TON Infrastructure Ltd."
SUPPORTED_ARTIFACT_TYPES = {
    "incident_memo",
    "case_development",
    "evidence_summary",
    "strategy_note",
    "strategy_memo",
    "strategic_plan",
    "strategic_response",
    "session_summary",
    "strategic_context",
    "witness_note",
    "counsel_draft",
    "decision_memo",
    "legal_analysis",
    "codex_response",
    "agent_identity",
}


@dataclass(frozen=True)
class IngestedArtifact:
    manifest: Path
    source_artifact: Path
    stored_artifact: Path
    artifact_type: str
    source_agent: str
    task_id_hint: str


def ingest_exchange(root: Path, exchange_root: Path, today: date) -> list[IngestedArtifact]:
    init_agent_exchange(exchange_root)
    manifests_dir = exchange_root / "manifests"
    processed_manifests_dir = manifests_dir / "processed"
    processed_manifests_dir.mkdir(parents=True, exist_ok=True)
    processed_incoming_dir = exchange_root / "incoming" / "processed"
    processed_incoming_dir.mkdir(parents=True, exist_ok=True)

    store = SafeWorkspaceStore(root)
    ingested: list[IngestedArtifact] = []
    manifest_paths = sorted(
        path for path in manifests_dir.glob("*.json") if path.name != "manifest-template.json"
    )
    for manifest_path in manifest_paths:
        payload = _load_manifest(manifest_path)
        matter = str(payload.get("matter", ""))
        artifact_type = str(payload.get("artifact_type", ""))
        source_agent = str(payload.get("source_agent", ""))
        artifact_path_value = str(payload.get("artifact_path", ""))

        if not artifact_path_value.startswith("incoming/"):
            continue

        if matter != TON_MATTER:
            raise StoreError(f"unsupported matter in manifest {manifest_path.name}: {matter}")
        if artifact_type not in SUPPORTED_ARTIFACT_TYPES:
            raise StoreError(f"unsupported artifact_type in manifest {manifest_path.name}: {artifact_type}")

        source_artifact = exchange_root / artifact_path_value
        if not source_artifact.exists():
            raise StoreError(f"manifest artifact missing: {artifact_path_value}")

        stored_artifact = _copy_into_workspace(root, source_artifact, artifact_type, source_agent)
        proposal_path = None
        supersedes = str(payload.get("supersedes", "")).strip()
        codex_state_patch = payload.get("codex_state_patch")
        if artifact_type == "codex_response" and not isinstance(codex_state_patch, dict):
            codex_state_patch = _extract_structured_patch(source_artifact)
        if isinstance(codex_state_patch, dict) and codex_state_patch:
            proposal_path = record_agent_proposal(
                root,
                source_agent=source_agent,
                artifact_type=artifact_type,
                artifact_path=str(stored_artifact.relative_to(root)),
                patch=codex_state_patch,
                supersedes=supersedes,
            )
        else:
            suggested_updates = payload.get("codex_state_updates_suggested")
            if not isinstance(suggested_updates, dict) or not suggested_updates:
                suggested_updates = payload.get("aegis_state_updates_suggested")
            if isinstance(suggested_updates, dict) and suggested_updates:
                proposal_path = record_agent_proposal(
                    root,
                    source_agent=source_agent,
                    artifact_type=artifact_type,
                    artifact_path=str(stored_artifact.relative_to(root)),
                    patch={},
                    suggested_updates=suggested_updates,
                    status="pending_review",
                    supersedes=supersedes,
                )
        if proposal_path is not None and supersedes:
            supersede_matching_proposals(
                root,
                source_agent=source_agent,
                artifact_type=artifact_type,
                supersedes=supersedes,
                replacement_proposal_path=proposal_path,
                today=today,
            )

        _record_ingestion(store, stored_artifact, artifact_type, source_agent, today, proposal_path)
        _mark_processed(source_artifact, processed_incoming_dir)
        _mark_processed(manifest_path, processed_manifests_dir)

        ingested.append(
            IngestedArtifact(
                manifest=manifest_path,
                source_artifact=source_artifact,
                stored_artifact=stored_artifact,
                artifact_type=artifact_type,
                source_agent=source_agent,
                task_id_hint=stored_artifact.name,
            )
        )

    if ingested:
        package = load_filing_package(root)
        matter = load_litigation_matter(root)
        write_draft_bundle(root, package, matter)
        payload = build_litigation_handoff(root, today)
        write_exchange_payload(exchange_root / "handoff", name="litigation-handoff.json", payload=payload)

    return ingested


def _load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise StoreError(f"manifest did not load as object: {path}")
    required = {"artifact_path", "artifact_type", "source_agent", "requested_action", "matter"}
    missing = sorted(field for field in required if field not in data)
    if missing:
        raise StoreError(f"manifest missing required fields {missing}: {path.name}")
    return data


def _copy_into_workspace(root: Path, source_artifact: Path, artifact_type: str, source_agent: str) -> Path:
    intake_dir = root / "nrg-bloom" / "litigation-ton" / "agent-intake" / artifact_type
    intake_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    safe_agent = source_agent.replace("/", "-").replace(" ", "-")
    destination = intake_dir / f"{stamp}-{safe_agent}-{source_artifact.name}"
    shutil.copy2(source_artifact, destination)
    return destination


def _record_ingestion(
    store: SafeWorkspaceStore,
    stored_artifact: Path,
    artifact_type: str,
    source_agent: str,
    today: date,
    proposal_path: Path | None,
) -> None:
    title = f"Review ingested {artifact_type.replace('_', ' ')} from {source_agent}"
    notes = f"Ingested artifact: {stored_artifact.relative_to(store.root)}"
    if proposal_path is not None:
        notes += f"\nPending proposal: {proposal_path.relative_to(store.root)}"
    store.add_task(
        title=title,
        company="nrg_bloom",
        priority="P1",
        due=today.isoformat(),
        notes=notes,
        status="todo",
        created=today.isoformat(),
    )
    store.append_memory(
        {
            "type": "agent_exchange_ingest",
            "name": stored_artifact.name,
            "date": today.isoformat(),
            "matter": TON_MATTER,
            "artifactType": artifact_type,
            "sourceAgent": source_agent,
            "storedPath": str(stored_artifact.relative_to(store.root)),
            "proposalPath": str(proposal_path.relative_to(store.root)) if proposal_path is not None else "",
        }
    )


def _mark_processed(path: Path, processed_dir: Path) -> None:
    processed_dir.mkdir(parents=True, exist_ok=True)
    destination = processed_dir / path.name
    if destination.exists():
        destination = processed_dir / f"{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}-{path.name}"
    path.replace(destination)


def _extract_structured_patch(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    matches = re.findall(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    for match in matches:
        try:
            data = json.loads(match)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            return data
    return {}
