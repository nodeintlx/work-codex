from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
import re
from typing import Any

import yaml


@dataclass(frozen=True)
class MatterDeadline:
    label: str
    due: date
    source: str


@dataclass(frozen=True)
class MatterArtifact:
    label: str
    path: Path
    exists: bool


@dataclass(frozen=True)
class LitigationMatter:
    matter: str
    status: str
    phase: str
    mechanism: str
    representation_mode: str
    canadian_counsel: str
    nigerian_counsel: str
    current_track: str
    canadian_path: str
    filing_readiness: str
    limitation_status: str
    protective_filing_needed: str
    start_date: date | None
    negotiation_deadline: date | None
    mediation_deadline: date | None
    opening: str
    floor: str
    ton_zone: str
    latest_round: int | None
    latest_round_date: date | None
    latest_assessment: str
    latest_next_step: str
    live_next_actions: list[str]
    live_notes: str
    red_lines: list[str]
    leverage_points: list[dict[str, Any]]
    deadlines: list[MatterDeadline]
    artifacts: list[MatterArtifact]


def load_litigation_matter(root: Path) -> LitigationMatter:
    matter_root = root / "nrg-bloom" / "litigation-ton"
    tracker_path = matter_root / "settlement-tracker.yaml"
    context_path = matter_root / "CONTEXT.md"
    if not tracker_path.exists():
        raise ValueError(f"missing settlement tracker: {tracker_path}")
    if not context_path.exists():
        raise ValueError(f"missing context file: {context_path}")

    with tracker_path.open("r", encoding="utf-8") as handle:
        tracker = yaml.safe_load(handle)
    if not isinstance(tracker, dict):
        raise ValueError("settlement tracker did not load as a mapping")

    framework = tracker.get("framework", {})
    parameters = tracker.get("parameters", {})
    rounds = tracker.get("rounds", [])
    red_lines = tracker.get("red_lines", [])
    leverage_points = tracker.get("leverage_points", [])
    matter_status = _load_matter_status(matter_root / "matter-status.yaml")

    latest_round = rounds[-1] if rounds else {}
    artifacts = _build_artifacts(matter_root)
    deadlines = _build_deadlines(framework)

    return LitigationMatter(
        matter=str(matter_status.get("matter", tracker.get("matter", ""))),
        status=str(matter_status.get("status", tracker.get("status", ""))),
        phase=str(matter_status.get("phase", "")),
        mechanism=str(framework.get("mechanism", "")),
        representation_mode=str(_nested(matter_status, "representation.mode")),
        canadian_counsel=str(_nested(matter_status, "representation.canadian_counsel")),
        nigerian_counsel=str(_nested(matter_status, "representation.nigerian_counsel")),
        current_track=str(_nested(matter_status, "forum.current_track")),
        canadian_path=str(_nested(matter_status, "forum.canadian_path")),
        filing_readiness=str(_nested(matter_status, "filing.filing_readiness")),
        limitation_status=str(_nested(matter_status, "filing.limitation_status")),
        protective_filing_needed=str(_nested(matter_status, "filing.protective_filing_needed")),
        start_date=_parse_date(framework.get("start_date")),
        negotiation_deadline=_parse_date(framework.get("negotiation_deadline")),
        mediation_deadline=_parse_date(framework.get("mediation_deadline")),
        opening=str(_nested(matter_status, "settlement.opening") or parameters.get("nrg_bloom_opening", "")),
        floor=str(_nested(matter_status, "settlement.floor") or parameters.get("nrg_bloom_floor", "")),
        ton_zone=str(parameters.get("ton_estimated_zone", "")),
        latest_round=int(latest_round["round"]) if latest_round.get("round") is not None else None,
        latest_round_date=_parse_date(latest_round.get("date")),
        latest_assessment=str(latest_round.get("assessment", "")),
        latest_next_step=str(_first_live_next_action(matter_status) or latest_round.get("next_step", "")),
        live_next_actions=[str(item) for item in matter_status.get("next_actions", []) if isinstance(item, str)],
        live_notes=str(matter_status.get("notes", "")),
        red_lines=[str(item) for item in red_lines],
        leverage_points=[item for item in leverage_points if isinstance(item, dict)],
        deadlines=deadlines,
        artifacts=artifacts,
    )


def litigation_deadlines(matter: LitigationMatter, today: date) -> tuple[list[MatterDeadline], list[MatterDeadline]]:
    overdue: list[MatterDeadline] = []
    upcoming: list[MatterDeadline] = []
    for deadline in matter.deadlines:
        if deadline.due < today:
            overdue.append(deadline)
        elif deadline.due <= date.fromordinal(today.toordinal() + 7):
            upcoming.append(deadline)
    return overdue, upcoming


def context_snapshot(root: Path) -> dict[str, str]:
    context_path = root / "nrg-bloom" / "litigation-ton" / "CONTEXT.md"
    text = context_path.read_text(encoding="utf-8")
    return {
        "phase": _extract_section_value(text, "Phase"),
        "key_deadline": _extract_section_value(text, "Key deadline"),
        "if_negotiation_fails": _extract_section_value(text, "If negotiation fails"),
        "last_update": _extract_section_value(text, "Last update"),
    }


def artifact_gaps(matter: LitigationMatter) -> list[MatterArtifact]:
    return [artifact for artifact in matter.artifacts if not artifact.exists]


def _build_deadlines(framework: dict[str, Any]) -> list[MatterDeadline]:
    deadlines: list[MatterDeadline] = []
    for key, label in (
        ("start_date", "Negotiation Start"),
        ("negotiation_deadline", "Negotiation Deadline"),
        ("mediation_deadline", "Mediation Deadline"),
    ):
        parsed = _parse_date(framework.get(key))
        if parsed:
            deadlines.append(MatterDeadline(label=label, due=parsed, source="settlement-tracker.yaml"))
    return deadlines


def _build_artifacts(matter_root: Path) -> list[MatterArtifact]:
    required = [
        ("Matter Status", matter_root / "matter-status.yaml"),
        ("Context", matter_root / "CONTEXT.md"),
        ("Settlement Tracker", matter_root / "settlement-tracker.yaml"),
        ("Claims Map", matter_root / "claims-map.yaml"),
        ("Chronology Map", matter_root / "chronology-map.yaml"),
        ("Evidence Map", matter_root / "evidence-map.yaml"),
        ("Unified Chronology", matter_root / "unified-chronology.md"),
        ("Evidence Index", matter_root / "source-linked-evidence-index.md"),
        ("Verified Call Transcripts", matter_root / "verified-call-transcripts.md"),
        ("Axxela Analysis", matter_root / "axxela-analysis.md"),
        ("Risk Assessment", matter_root / "risk-assessment.md"),
        ("TON Response Analysis", matter_root / "ton-response-analysis.md"),
        ("Master Evidence Summary", matter_root / "master-evidence-summary-2026-02-25.md"),
        ("Expenditure Ledger", matter_root / "nrg-bloom-expenditure-ledger-2026-03-01.md"),
        ("Demand Letter", matter_root / "dayo-demand-letter-to-ton.pdf"),
        ("TON Response", matter_root / "ton-response-to-demand-letter.pdf"),
        ("Signed Site Agreement", matter_root / "ogboinbiri-site-development-agreement-signed.pdf"),
        ("MNDA", matter_root / "nrg-bloom-mutual-nda-non-compete.pdf"),
        ("Original JV Agreement", matter_root / "tyler-macpherson" / "00000022-Joint_Venture_Agreement_NRG_BLOOM_TON_Feb_19_2025_Updated.pdf"),
    ]
    return [MatterArtifact(label=label, path=path, exists=path.exists()) for label, path in required]


def _parse_date(value: Any) -> date | None:
    if value in (None, "", "none"):
        return None
    return datetime.strptime(str(value), "%Y-%m-%d").date()


def _extract_section_value(text: str, label: str) -> str:
    pattern = re.compile(rf"- \*\*{re.escape(label)}:\*\* (.+)")
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def _load_matter_status(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data if isinstance(data, dict) else {}


def _nested(data: dict[str, Any], dotted_key: str) -> Any:
    current: Any = data
    for part in dotted_key.split("."):
        if not isinstance(current, dict):
            return ""
        current = current.get(part, "")
    return current


def _first_live_next_action(data: dict[str, Any]) -> str:
    actions = data.get("next_actions", [])
    if not isinstance(actions, list) or not actions:
        return ""
    for action in actions:
        if isinstance(action, str) and action.strip():
            return action
    return ""
