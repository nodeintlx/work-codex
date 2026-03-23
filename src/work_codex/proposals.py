from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
import json
from pathlib import Path
from typing import Any

import yaml

from .store import SafeWorkspaceStore, StoreError


@dataclass(frozen=True)
class AgentProposal:
    path: Path
    source_agent: str
    artifact_type: str
    artifact_path: str
    created_at_utc: str
    status: str
    patch: dict[str, Any]
    suggested_updates: dict[str, Any]
    supersedes: str
    superseded_by: str


def record_agent_proposal(
    root: Path,
    *,
    source_agent: str,
    artifact_type: str,
    artifact_path: str,
    patch: dict[str, Any],
    suggested_updates: dict[str, Any] | None = None,
    status: str = "pending",
    supersedes: str = "",
) -> Path:
    proposals_dir = root / "nrg-bloom" / "litigation-ton" / "agent-intake" / "proposals"
    proposals_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    safe_agent = source_agent.replace("/", "-").replace(" ", "-")
    path = proposals_dir / f"{stamp}-{safe_agent}-{artifact_type}.json"
    payload = {
        "protocol_version": "codex-state-patch/v1",
        "created_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "source_agent": source_agent,
        "artifact_type": artifact_type,
        "artifact_path": artifact_path,
        "status": status,
        "patch": patch,
        "suggested_updates": suggested_updates or {},
        "supersedes": supersedes,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def list_agent_proposals(root: Path) -> list[AgentProposal]:
    proposals_dir = root / "nrg-bloom" / "litigation-ton" / "agent-intake" / "proposals"
    if not proposals_dir.exists():
        return []
    proposals: list[AgentProposal] = []
    for path in sorted(proposals_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        proposals.append(
            AgentProposal(
                path=path,
                source_agent=str(data.get("source_agent", "")),
                artifact_type=str(data.get("artifact_type", "")),
                artifact_path=str(data.get("artifact_path", "")),
                created_at_utc=str(data.get("created_at_utc", "")),
                status=str(data.get("status", "pending")),
                patch=data.get("patch", {}) if isinstance(data.get("patch", {}), dict) else {},
                suggested_updates=(
                    data.get("suggested_updates", {}) if isinstance(data.get("suggested_updates", {}), dict) else {}
                ),
                supersedes=str(data.get("supersedes", "")),
                superseded_by=str(data.get("superseded_by", "")),
            )
        )
    return proposals


def apply_agent_proposal(root: Path, proposal_path: Path, today: date) -> list[str]:
    data = json.loads(proposal_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise StoreError(f"proposal did not load as object: {proposal_path}")
    if str(data.get("status", "pending")) != "pending":
        raise StoreError(f"proposal is not pending: {proposal_path.name}")
    patch = data.get("patch", {})
    if not isinstance(patch, dict):
        raise StoreError(f"proposal patch must be an object: {proposal_path.name}")

    store = SafeWorkspaceStore(root)
    applied: list[str] = []

    matter_status_patch = patch.get("matter_status", {})
    if matter_status_patch:
        if not isinstance(matter_status_patch, dict):
            raise StoreError("matter_status patch must be an object")
        normalized = _normalize_matter_status_patch(matter_status_patch)
        store.update_litigation_status(normalized)
        applied.extend(f"matter_status:{key}" for key in normalized.keys())

    claim_updates = patch.get("claim_updates", [])
    if claim_updates:
        if not isinstance(claim_updates, list):
            raise StoreError("claim_updates patch must be a list")
        for item in claim_updates:
            _apply_claim_update(root, item)
            applied.append(f"claim_update:{item.get('id', '')}")

    anti_stay_posture = patch.get("anti_stay_posture", [])
    if anti_stay_posture:
        if not isinstance(anti_stay_posture, list):
            raise StoreError("anti_stay_posture patch must be a list")
        store.update_litigation_status({"doctrine.anti_stay_posture": anti_stay_posture})
        applied.append("matter_status:doctrine.anti_stay_posture")

    strategy_principles = patch.get("strategy_principles_add", [])
    if strategy_principles:
        if not isinstance(strategy_principles, list):
            raise StoreError("strategy_principles_add patch must be a list")
        store.update_litigation_status({"doctrine.strategy_principles": strategy_principles})
        applied.append("matter_status:doctrine.strategy_principles")

    leverage_points = patch.get("leverage_points_add", [])
    if leverage_points:
        if not isinstance(leverage_points, list):
            raise StoreError("leverage_points_add patch must be a list")
        _append_leverage_points(root, leverage_points)
        applied.append("settlement_tracker:leverage_points_add")

    if not applied:
        raise StoreError(f"proposal contained no supported patch operations: {proposal_path.name}")

    data["status"] = "applied"
    data["applied_at_utc"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    proposal_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    store.append_memory(
        {
            "type": "agent_proposal_applied",
            "name": proposal_path.name,
            "date": today.isoformat(),
            "applied": applied,
        }
    )
    return applied


def supersede_matching_proposals(
    root: Path,
    *,
    source_agent: str,
    artifact_type: str,
    supersedes: str,
    replacement_proposal_path: Path,
    today: date,
) -> list[Path]:
    superseded_name = Path(supersedes).name
    if not superseded_name:
        return []

    changed: list[Path] = []
    for proposal in list_agent_proposals(root):
        if proposal.source_agent != source_agent or proposal.artifact_type != artifact_type:
            continue
        if proposal.path == replacement_proposal_path:
            continue
        if proposal.status == "applied":
            continue
        if not proposal.artifact_path.endswith(superseded_name):
            continue

        data = json.loads(proposal.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        data["status"] = "superseded"
        data["superseded_at_utc"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
        data["superseded_by"] = str(replacement_proposal_path.relative_to(root))
        proposal.path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        changed.append(proposal.path)

    if changed:
        store = SafeWorkspaceStore(root)
        store.append_memory(
            {
                "type": "agent_proposal_superseded",
                "name": replacement_proposal_path.name,
                "date": today.isoformat(),
                "supersedes": supersedes,
                "supersededProposalPaths": [str(path.relative_to(root)) for path in changed],
            }
        )
    return changed


def promote_agent_proposal(root: Path, proposal_path: Path, today: date) -> list[str]:
    data = json.loads(proposal_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise StoreError(f"proposal did not load as object: {proposal_path}")
    if str(data.get("status", "")) != "pending_review":
        raise StoreError(f"proposal is not pending_review: {proposal_path.name}")
    suggestions = data.get("suggested_updates", {})
    if not isinstance(suggestions, dict) or not suggestions:
        raise StoreError(f"proposal has no suggested_updates to promote: {proposal_path.name}")

    patch = _build_patch_from_suggestions(suggestions)
    if not patch:
        raise StoreError(f"proposal suggestions could not be promoted safely: {proposal_path.name}")

    data["patch"] = patch
    data["status"] = "pending"
    data["promoted_at_utc"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    proposal_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    store = SafeWorkspaceStore(root)
    store.append_memory(
        {
            "type": "agent_proposal_promoted",
            "name": proposal_path.name,
            "date": today.isoformat(),
            "promoted_keys": sorted(patch.keys()),
        }
    )
    return sorted(patch.keys())


def _apply_claim_update(root: Path, item: Any) -> None:
    if not isinstance(item, dict):
        raise StoreError("claim update entry must be an object")
    claim_id = str(item.get("id", ""))
    updates = item.get("set", {})
    if not claim_id:
        raise StoreError("claim update requires id")
    if not isinstance(updates, dict) or not updates:
        raise StoreError(f"claim update requires non-empty set for {claim_id}")

    path = root / "nrg-bloom" / "litigation-ton" / "claims-map.yaml"
    data = json.loads(json.dumps(_load_yaml(path)))
    claims = data.get("claims", [])
    if not isinstance(claims, list):
        raise StoreError("claims-map claims must be a list")
    for claim in claims:
        if isinstance(claim, dict) and str(claim.get("id", "")) == claim_id:
            for key, value in updates.items():
                claim[str(key)] = value
            _write_yaml(path, data)
            return
    raise StoreError(f"claim id not found in claims-map.yaml: {claim_id}")


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise StoreError(f"yaml did not load as mapping: {path}")
    return data


def _write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _normalize_matter_status_patch(patch: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    aliases = {
        "canadian_path": "forum.canadian_path",
        "canadian_path_scope": "forum.canadian_path_scope",
        "canadian_path_budget_cap": "forum.canadian_path_budget_cap",
        "filing_readiness": "filing.filing_readiness",
        "representation_mode": "representation.mode",
        "representation_note": "representation.note",
    }
    for key, value in patch.items():
        normalized[aliases.get(str(key), str(key))] = value
    return normalized


def _append_leverage_points(root: Path, items: list[Any]) -> None:
    path = root / "nrg-bloom" / "litigation-ton" / "settlement-tracker.yaml"
    data = _load_yaml(path)
    leverage_points = data.setdefault("leverage_points", [])
    if not isinstance(leverage_points, list):
        raise StoreError("settlement-tracker leverage_points must be a list")

    existing_names = {
        str(item.get("name", ""))
        for item in leverage_points
        if isinstance(item, dict)
    }
    changed = False
    for item in items:
        if not isinstance(item, dict):
            raise StoreError("each leverage point entry must be an object")
        name = str(item.get("name", ""))
        if not name:
            raise StoreError("leverage point entry requires name")
        if name in existing_names:
            continue
        leverage_points.append(item)
        existing_names.add(name)
        changed = True
    if changed:
        data["last_updated"] = date.today().isoformat()
        _write_yaml(path, data)


def _build_patch_from_suggestions(suggestions: dict[str, Any]) -> dict[str, Any]:
    patch: dict[str, Any] = {}

    filing_readiness = suggestions.get("filing_readiness")
    if isinstance(filing_readiness, str) and "ready_pending_lawyer" in filing_readiness:
        patch.setdefault("matter_status", {})["filing_readiness"] = "ready_pending_lawyer"

    matter_status = suggestions.get("matter_status")
    if isinstance(matter_status, dict):
        selected: dict[str, Any] = {}
        if isinstance(matter_status.get("phase"), str) and str(matter_status.get("phase")).strip():
            selected["phase"] = str(matter_status["phase"]).strip()
        if isinstance(matter_status.get("canadian_path"), str) and str(matter_status.get("canadian_path")).strip():
            selected["canadian_path"] = str(matter_status["canadian_path"]).strip()
        if (
            isinstance(matter_status.get("negotiation_status"), str)
            and str(matter_status.get("negotiation_status")).strip()
        ):
            selected["settlement.negotiation_status"] = str(matter_status["negotiation_status"]).strip()
        if (
            isinstance(matter_status.get("nigerian_proceedings"), str)
            and str(matter_status.get("nigerian_proceedings")).strip()
        ):
            selected["forum.nigerian_proceedings"] = str(matter_status["nigerian_proceedings"]).strip()

        canadian_note_parts: list[str] = []
        for key in ("canadian_path_note", "alberta_filing"):
            value = matter_status.get(key)
            if isinstance(value, str) and value.strip():
                canadian_note_parts.append(value.strip())
        if canadian_note_parts:
            selected["forum.canadian_path_note"] = " ".join(canadian_note_parts)
        if selected:
            patch.setdefault("matter_status", {}).update(selected)

    live_notes = suggestions.get("live_notes")
    if isinstance(live_notes, str) and live_notes.strip():
        patch.setdefault("matter_status", {})["notes"] = live_notes.strip()

    claims_map = suggestions.get("claims_map")
    claim_updates = _claim_updates_from_suggestions(claims_map)
    if claim_updates:
        patch["claim_updates"] = claim_updates

    strategy = suggestions.get("strategy")
    principles = _strategy_principles_from_suggestions(strategy)
    if principles:
        patch["strategy_principles_add"] = principles

    settlement_tracker = suggestions.get("settlement_tracker")
    leverage_points = _leverage_points_from_suggestions(settlement_tracker)
    if leverage_points:
        patch["leverage_points_add"] = leverage_points

    return patch


def _claim_updates_from_suggestions(claims_map: Any) -> list[dict[str, Any]]:
    updates: list[dict[str, Any]] = []
    if isinstance(claims_map, str):
        if "C3" in claims_map and "canada_cross_border" in claims_map:
            updates.append({"id": "C3", "set": {"forum_track": "canada_or_cross_border"}})
        return updates
    if not isinstance(claims_map, dict):
        return updates

    alias_map = {
        "C1_bad_faith_termination": "C1",
        "C2_axxela_circumvention": "C2",
        "C3_misrepresentation": "C3",
        "C4_unjust_enrichment": "C4",
        "C1": "C1",
        "C2": "C2",
        "C3": "C3",
        "C4": "C4",
    }
    for raw_key, value in claims_map.items():
        claim_id = alias_map.get(str(raw_key))
        if not claim_id or not isinstance(value, str):
            continue
        lower = value.lower()
        claim_set: dict[str, Any] = {}
        if "forum: alberta" in lower or "alberta court" in lower or "mnda claim" in lower:
            claim_set["forum_track"] = "alberta_primary"
        elif "forum: nigeria" in lower:
            claim_set["forum_track"] = "nigeria_primary"
        if "forum question resolved" in lower or "ready to plead" in lower or "primary alberta claim" in lower:
            claim_set["status"] = "ready_to_plead"
        if "mnda section 6" in lower:
            claim_set["forum_basis"] = "MNDA Section 6 exclusive Alberta court jurisdiction."
        if claim_set:
            updates.append({"id": claim_id, "set": claim_set})
    return updates


def _strategy_principles_from_suggestions(strategy: Any) -> list[str]:
    if isinstance(strategy, str):
        return [strategy]
    if isinstance(strategy, dict):
        ordered: list[str] = []
        for key in ("new_principle", "asymmetric_warfare"):
            value = strategy.get(key)
            if isinstance(value, str) and value.strip():
                ordered.append(value.strip())
        return ordered
    return []


def _leverage_points_from_suggestions(settlement_tracker: Any) -> list[dict[str, Any]]:
    if not isinstance(settlement_tracker, dict):
        return []
    new_point = settlement_tracker.get("new_leverage_point")
    if not isinstance(new_point, str) or not new_point.strip():
        return []
    return [
        {
            "name": "Alberta protective filing (MNDA exclusive jurisdiction)",
            "deployed": False,
            "impact": "Critical — leverage point from structured strategic context.",
            "concession_value": new_point.strip(),
        }
    ]
