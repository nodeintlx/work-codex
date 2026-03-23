from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from .actions import build_strategic_actions
from .filing import load_filing_package
from .litigation import artifact_gaps, litigation_deadlines, load_litigation_matter
from .proposals import list_agent_proposals


def build_litigation_handoff(root: Path, today: date) -> dict[str, Any]:
    matter = load_litigation_matter(root)
    package = load_filing_package(root)
    actions = build_strategic_actions(root, today)
    overdue_deadlines, upcoming_deadlines = litigation_deadlines(matter, today)
    gaps = artifact_gaps(matter)
    proposals = list_agent_proposals(root)

    return {
        "protocol_version": "law-agent-handoff/v1",
        "exported_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "agent": {
            "id": "codex-law-agent",
            "domain": "litigation_operations",
            "workspace_root": str(root),
        },
        "matter": {
            "name": matter.matter,
            "status": matter.status,
            "phase": matter.phase,
            "representation_mode": matter.representation_mode,
            "current_track": matter.current_track,
            "canadian_path": matter.canadian_path,
            "filing_readiness": matter.filing_readiness,
            "limitation_status": matter.limitation_status,
            "protective_filing_needed": matter.protective_filing_needed,
            "settlement": {
                "opening": matter.opening,
                "floor": matter.floor,
                "estimated_ton_zone": matter.ton_zone,
            },
            "latest_round": {
                "number": matter.latest_round,
                "date": matter.latest_round_date.isoformat() if matter.latest_round_date else None,
                "assessment": matter.latest_assessment,
                "next_step": matter.latest_next_step,
            },
            "live_next_actions": matter.live_next_actions,
            "live_notes": matter.live_notes,
            "doctrine": _matter_doctrine(root),
            "red_lines": matter.red_lines,
            "leverage_points": matter.leverage_points,
        },
        "filing": {
            "readiness_level": package.readiness.level,
            "critical_claims_ready": package.readiness.critical_claims_ready,
            "critical_evidence_missing": package.readiness.critical_evidence_missing,
            "recommendations": list(package.readiness.recommendations),
            "claims": [
                {
                    "id": claim.claim_id,
                    "title": claim.title,
                    "forum_track": claim.forum_track,
                    "status": claim.status,
                    "priority": claim.pleading_priority,
                    "remedy_objective": claim.remedy_objective,
                }
                for claim in package.claims
            ],
            "chronology": [
                {
                    "id": event.event_id,
                    "date": _date_value(event.date),
                    "title": event.title,
                    "phase": event.phase,
                }
                for event in package.chronology
            ],
        },
        "strategy": {
            "top_action": _action_payload(actions[0]) if actions else None,
            "ranked_actions": [_action_payload(action) for action in actions],
        },
        "deadlines": {
            "overdue": [_deadline_payload(item) for item in overdue_deadlines],
            "upcoming": [_deadline_payload(item) for item in upcoming_deadlines],
        },
        "artifacts": {
            "missing_core_artifacts": [
                {
                    "label": item.label,
                    "path": _relative_path(root, item.path),
                }
                for item in gaps
            ],
            "latest_generated_bundle": _latest_generated_bundle(root),
            "latest_incident_memos": _latest_incident_memos(root),
        },
        "agent_proposals": {
            "pending_count": sum(1 for item in proposals if item.status == "pending"),
            "items": [
                {
                    "path": _relative_path(root, item.path),
                    "source_agent": item.source_agent,
                    "artifact_type": item.artifact_type,
                    "artifact_path": item.artifact_path,
                    "status": item.status,
                    "created_at_utc": item.created_at_utc,
                }
                for item in proposals
            ],
        },
        "interoperability": {
            "source_of_truth": [
                "nrg-bloom/litigation-ton/matter-status.yaml",
                "nrg-bloom/litigation-ton/settlement-tracker.yaml",
                "nrg-bloom/litigation-ton/claims-map.yaml",
                "nrg-bloom/litigation-ton/chronology-map.yaml",
                "nrg-bloom/litigation-ton/evidence-map.yaml",
            ],
            "intended_consumers": [
                "future_codex_agents",
                "future_claude_agents",
                "external_automation",
            ],
            "notes": "Consume this payload instead of scraping ad hoc markdown or chat transcripts.",
        },
    }


def _action_payload(action: Any) -> dict[str, str]:
    return {
        "priority": action.priority,
        "title": action.title,
        "rationale": action.rationale,
        "settlement_pressure": action.settlement_pressure,
    }


def _deadline_payload(item: Any) -> dict[str, str]:
    return {
        "label": item.label,
        "due": item.due.isoformat(),
        "source": item.source,
    }


def _latest_generated_bundle(root: Path) -> dict[str, Any] | None:
    latest_dir = root / "nrg-bloom" / "litigation-ton" / "generated" / "latest"
    if not latest_dir.exists():
        return None
    files = sorted(path.name for path in latest_dir.iterdir() if path.is_file())
    return {
        "path": _relative_path(root, latest_dir),
        "files": files,
    }


def _latest_incident_memos(root: Path) -> list[str]:
    matter_root = root / "nrg-bloom" / "litigation-ton"
    memos = sorted(matter_root.glob("incident-memo-*.md"))
    return [_relative_path(root, path) for path in memos[-5:]]


def _relative_path(root: Path, path: Path) -> str:
    return str(path.relative_to(root))


def _date_value(value: Any) -> str:
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _matter_doctrine(root: Path) -> dict[str, Any]:
    import yaml

    path = root / "nrg-bloom" / "litigation-ton" / "matter-status.yaml"
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        return {}
    doctrine = data.get("doctrine", {})
    return doctrine if isinstance(doctrine, dict) else {}
