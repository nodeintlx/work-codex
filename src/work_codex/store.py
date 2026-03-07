from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
import json
from pathlib import Path
import sys
from tempfile import NamedTemporaryFile
from typing import Any

import yaml

from .workspace import Workspace

_VENDOR_DIR = Path(__file__).resolve().parents[2] / ".vendor"
if _VENDOR_DIR.exists() and str(_VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(_VENDOR_DIR))

from ruamel.yaml import YAML


TASK_PRIORITIES = {"P0", "P1", "P2", "P3"}
TASK_STATUSES = {"todo", "in_progress", "blocked", "done"}
TASK_COMPANIES = {"nrg_bloom", "coldstorm", "personal", "both"}
PIPELINE_STAGES = {
    "prospect",
    "outreach",
    "response",
    "meeting",
    "proposal",
    "negotiation",
    "closed_won",
    "closed_lost",
}
FUNDING_STATUSES = {
    "researching",
    "eligible",
    "applying",
    "submitted",
    "under_review",
    "approved",
    "rejected",
}


@dataclass(frozen=True)
class MutationResult:
    path: Path
    message: str


class StoreError(ValueError):
    pass


class SafeWorkspaceStore:
    def __init__(self, root: Path):
        self.root = root
        self.workspace = Workspace(root)
        self.yaml_rt = YAML()
        self.yaml_rt.preserve_quotes = True
        self.yaml_rt.width = 1000
        self.yaml_rt.indent(mapping=2, sequence=4, offset=2)

    def add_task(
        self,
        *,
        title: str,
        company: str,
        priority: str,
        due: str | None,
        notes: str,
        status: str = "todo",
        created: str | None = None,
    ) -> MutationResult:
        _ensure(company in TASK_COMPANIES, f"invalid task company: {company}")
        _ensure(priority in TASK_PRIORITIES, f"invalid task priority: {priority}")
        _ensure(status in TASK_STATUSES, f"invalid task status: {status}")
        if due is not None:
            _parse_date_string(due)
        created_value = created or date.today().isoformat()
        _parse_date_string(created_value)

        path = self.root / "shared/tasks.yaml"
        data = self._load_roundtrip_yaml(path)
        tasks = data.setdefault("tasks", [])
        _ensure(isinstance(tasks, list), "shared/tasks.yaml tasks must be a list")
        next_id = max((int(item.get("id", 0)) for item in tasks), default=0) + 1
        tasks.append(
            {
                "id": next_id,
                "title": title,
                "company": company,
                "priority": priority,
                "status": status,
                "due": due,
                "notes": notes,
                "created": created_value,
            }
        )
        data["last_updated"] = date.today().isoformat()
        self._write_yaml(path, data, action="task_add", details={"id": next_id, "title": title})
        self._validate_workspace()
        return MutationResult(path=path, message=f"added task #{next_id}: {title}")

    def update_task(
        self,
        *,
        task_id: int,
        title: str | None = None,
        company: str | None = None,
        priority: str | None = None,
        status: str | None = None,
        due: str | None = None,
        notes: str | None = None,
        append_note: str | None = None,
    ) -> MutationResult:
        path = self.root / "shared/tasks.yaml"
        data = self._load_roundtrip_yaml(path)
        tasks = data.get("tasks", [])
        task = _find_record_by_id(tasks, task_id)
        if company is not None:
            _ensure(company in TASK_COMPANIES, f"invalid task company: {company}")
            task["company"] = company
        if priority is not None:
            _ensure(priority in TASK_PRIORITIES, f"invalid task priority: {priority}")
            task["priority"] = priority
        if status is not None:
            _ensure(status in TASK_STATUSES, f"invalid task status: {status}")
            task["status"] = status
        if due is not None:
            _parse_date_string(due)
            task["due"] = due
        if title is not None:
            task["title"] = title
        if notes is not None:
            task["notes"] = notes
        if append_note:
            existing = str(task.get("notes", "")).strip()
            task["notes"] = f"{existing}\n{append_note}".strip() if existing else append_note

        data["last_updated"] = date.today().isoformat()
        self._write_yaml(path, data, action="task_update", details={"id": task_id})
        self._validate_workspace()
        return MutationResult(path=path, message=f"updated task #{task_id}")

    def upsert_pipeline(
        self,
        *,
        deal_id: int | None,
        name: str,
        company: str,
        fields: dict[str, Any],
    ) -> MutationResult:
        path = self.root / "shared/pipeline.yaml"
        data = self._load_roundtrip_yaml(path)
        deals = data.setdefault("deals", [])
        _ensure(isinstance(deals, list), "shared/pipeline.yaml deals must be a list")
        record = None
        if deal_id is not None:
            record = _find_record_by_id(deals, deal_id)
        else:
            record = _find_record_by_name(deals, name)

        created = False
        if record is None:
            next_id = max((int(item.get("id", 0)) for item in deals), default=0) + 1
            record = {"id": next_id, "name": name, "company": company}
            deals.append(record)
            created = True

        merged = {"name": name, "company": company, **fields}
        if "stage" in merged:
            _ensure(merged["stage"] in PIPELINE_STAGES, f"invalid pipeline stage: {merged['stage']}")
        if "next_action_date" in merged and merged["next_action_date"] not in (None, ""):
            _parse_date_string(str(merged["next_action_date"]))
        record.update(merged)
        data["last_updated"] = date.today().isoformat()
        action = "pipeline_add" if created else "pipeline_update"
        self._write_yaml(path, data, action=action, details={"name": name})
        self._validate_workspace()
        verb = "added" if created else "updated"
        return MutationResult(path=path, message=f"{verb} pipeline deal: {name}")

    def upsert_funding(
        self,
        *,
        program_id: int | None,
        name: str,
        company: str,
        fields: dict[str, Any],
    ) -> MutationResult:
        path = self.root / "shared/funding.yaml"
        data = self._load_roundtrip_yaml(path)
        programs = data.setdefault("programs", [])
        _ensure(isinstance(programs, list), "shared/funding.yaml programs must be a list")
        record = None
        if program_id is not None:
            record = _find_record_by_id(programs, program_id)
        else:
            record = _find_record_by_name(programs, name)

        created = False
        if record is None:
            next_id = max((int(item.get("id", 0)) for item in programs), default=0) + 1
            record = {"id": next_id, "name": name, "company": company}
            programs.append(record)
            created = True

        merged = {"name": name, "company": company, **fields}
        if "status" in merged:
            _ensure(merged["status"] in FUNDING_STATUSES, f"invalid funding status: {merged['status']}")
        for field_name in ("deadline", "next_action_date"):
            if field_name in merged and merged[field_name] not in (None, "", "none"):
                _parse_date_string(str(merged[field_name]))
        record.update(merged)
        data["last_updated"] = date.today().isoformat()
        action = "funding_add" if created else "funding_update"
        self._write_yaml(path, data, action=action, details={"name": name})
        self._validate_workspace()
        verb = "added" if created else "updated"
        return MutationResult(path=path, message=f"{verb} funding program: {name}")

    def append_memory(self, record: dict[str, Any]) -> MutationResult:
        _ensure(isinstance(record, dict), "memory record must be an object")
        _ensure("type" in record, "memory record must include 'type'")
        _ensure("name" in record, "memory record must include 'name'")
        path = self.root / "knowledge/memory.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(record, ensure_ascii=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
        self._write_audit(
            action="memory_append",
            path=path,
            details={"type": record.get("type"), "name": record.get("name")},
        )
        self.workspace.memory_record_count()
        return MutationResult(path=path, message=f"appended memory record: {record['name']}")

    def update_litigation_status(self, fields: dict[str, Any]) -> MutationResult:
        path = self.root / "nrg-bloom" / "litigation-ton" / "matter-status.yaml"
        data = self._load_roundtrip_yaml(path) if path.exists() else self._default_matter_status()
        for key, value in fields.items():
            _set_nested_value(data, key, value)
        data["last_updated"] = date.today().isoformat()
        self._write_yaml(path, data, action="litigation_status_update", details={"fields": sorted(fields.keys())})
        return MutationResult(path=path, message="updated litigation matter status")

    def update_settlement_tracker(self, fields: dict[str, Any]) -> MutationResult:
        path = self.root / "nrg-bloom" / "litigation-ton" / "settlement-tracker.yaml"
        data = self._load_roundtrip_yaml(path)
        for key, value in fields.items():
            _set_nested_value(data, key, value)
        data["last_updated"] = date.today().isoformat()
        self._write_yaml(path, data, action="settlement_tracker_update", details={"fields": sorted(fields.keys())})
        return MutationResult(path=path, message="updated settlement tracker")

    def append_settlement_round(self, round_record: dict[str, Any]) -> MutationResult:
        _ensure(isinstance(round_record, dict), "settlement round must be an object")
        _ensure("date" in round_record, "settlement round must include 'date'")
        _ensure("type" in round_record, "settlement round must include 'type'")
        _parse_date_string(str(round_record["date"]))
        path = self.root / "nrg-bloom" / "litigation-ton" / "settlement-tracker.yaml"
        data = self._load_roundtrip_yaml(path)
        rounds = data.setdefault("rounds", [])
        _ensure(isinstance(rounds, list), "settlement-tracker rounds must be a list")
        next_round = max((int(item.get("round", 0)) for item in rounds if isinstance(item, dict)), default=0) + 1
        record = {"round": next_round, **round_record}
        rounds.append(record)
        data["last_updated"] = date.today().isoformat()
        self._write_yaml(path, data, action="settlement_round_append", details={"round": next_round, "type": round_record["type"]})
        return MutationResult(path=path, message=f"appended settlement round {next_round}")

    def _validate_workspace(self) -> None:
        errors = self.workspace.validate()
        if errors:
            raise StoreError("; ".join(errors))

    def _write_yaml(self, path: Path, data: dict[str, Any], *, action: str, details: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._write_backup(path)
        with NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as handle:
            self.yaml_rt.dump(data, handle)
            temp_path = Path(handle.name)
        temp_path.replace(path)
        self._write_audit(action=action, path=path, details=details)

    def _load_roundtrip_yaml(self, path: Path):
        if not path.exists():
            raise StoreError(f"missing file: {path}")
        with path.open("r", encoding="utf-8") as handle:
            data = self.yaml_rt.load(handle)
        if not isinstance(data, dict):
            raise StoreError(f"file did not load as a mapping: {path}")
        return data

    def _write_backup(self, path: Path) -> None:
        if not path.exists():
            return
        backup_dir = self.root / ".work_codex" / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        backup_path = backup_dir / f"{timestamp}-{path.name}.bak"
        backup_path.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

    def _write_audit(self, *, action: str, path: Path, details: dict[str, Any]) -> None:
        audit_dir = self.root / ".work_codex"
        audit_dir.mkdir(parents=True, exist_ok=True)
        audit_path = audit_dir / "audit.jsonl"
        event = {
            "timestamp": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "action": action,
            "path": str(path.relative_to(self.root)),
            "details": details,
        }
        with audit_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=True) + "\n")

    def _default_matter_status(self):
        return {
            "matter": "NRG Bloom Inc. v. TON Infrastructure Ltd.",
            "status": "active",
            "phase": "negotiation",
            "representation": {
                "mode": "self_directed_with_ai",
                "canadian_counsel": "paused",
                "nigerian_counsel": "active",
            },
            "forum": {
                "current_track": "negotiation",
                "canadian_path": "under_evaluation",
                "nigerian_path": "active",
            },
            "filing": {
                "filing_readiness": "in_progress",
                "limitation_status": "not_expired",
                "protective_filing_needed": "to_be_determined",
            },
            "settlement": {
                "opening": "$727,000 USD (₦1.2B)",
                "floor": "$500,000 USD",
                "current_posture": "awaiting_counterparty_response",
            },
            "next_actions": [],
            "notes": "",
            "last_updated": date.today().isoformat(),
        }


def _load_yaml_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise StoreError(f"missing file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise StoreError(f"file did not load as a mapping: {path}")
    return data


def _find_record_by_id(items: list[dict[str, Any]], record_id: int) -> dict[str, Any]:
    for item in items:
        if int(item.get("id", -1)) == record_id:
            return item
    raise StoreError(f"record not found for id={record_id}")


def _find_record_by_name(items: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    for item in items:
        if str(item.get("name", "")) == name:
            return item
    return None


def _parse_date_string(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise StoreError(f"invalid date, expected YYYY-MM-DD: {value}") from exc
    return value


def _ensure(condition: bool, message: str) -> None:
    if not condition:
        raise StoreError(message)


def _set_nested_value(target: Any, dotted_key: str, value: Any) -> None:
    current = target
    parts = dotted_key.split(".")
    for part in parts[:-1]:
        if part not in current or not isinstance(current[part], dict):
            current[part] = {}
        current = current[part]
    current[parts[-1]] = value
