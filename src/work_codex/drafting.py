from __future__ import annotations

from .filing import FilingClaim, FilingEvidence, FilingEvent, FilingPackage
from .litigation import LitigationMatter


def claim_outline_lines(package: FilingPackage) -> list[str]:
    lines = [
        f"# Claim Outline: {package.matter}",
        "",
        f"Readiness: {package.readiness.level}",
        "",
    ]
    for index, claim in enumerate(package.claims, start=1):
        lines.extend(
            [
                f"## {index}. {claim.title}",
                f"- Claim ID: {claim.claim_id}",
                f"- Forum track: {claim.forum_track}",
                f"- Status: {claim.status}",
                f"- Priority: {claim.pleading_priority}",
                f"- Remedy objective: {claim.remedy_objective}",
                f"- Theory: {claim.theory}",
                "- Key facts:",
            ]
        )
        for fact in claim.key_facts:
            lines.append(f"  - {fact}")
        lines.append(f"- Damages anchor: {claim.damages_anchor}")
        lines.append(f"- Pleading notes: {claim.pleading_notes}")
        lines.append(f"- Chronology anchors: {', '.join(claim.chronology_event_ids) or 'none'}")
        lines.append(f"- Evidence anchors: {', '.join(claim.evidence_ids) or 'none'}")
        lines.append("")
    return lines


def facts_section_lines(package: FilingPackage) -> list[str]:
    lines = [
        f"# Draft Facts Section: {package.matter}",
        "",
        "## Core Facts",
        "",
    ]
    for event in package.chronology:
        lines.append(f"### {event.date} - {event.title}")
        lines.append(event.significance)
        if event.evidence_ids:
            lines.append(f"Evidence: {', '.join(event.evidence_ids)}")
        lines.append("")
    return lines


def exhibit_list_lines(package: FilingPackage) -> list[str]:
    lines = [
        f"# Exhibit List: {package.matter}",
        "",
        "| Exhibit | Evidence ID | Title | Path | Strength |",
        "|---|---|---|---|---|",
    ]
    for index, evidence in enumerate(package.evidence, start=1):
        exhibit_id = f"Exhibit {index}"
        lines.append(
            f"| {exhibit_id} | {evidence.evidence_id} | {evidence.title} | {evidence.path.name} | {evidence.strength} |"
        )
    lines.append("")
    return lines


def alberta_skeleton_lines(package: FilingPackage, matter: LitigationMatter) -> list[str]:
    canada_claims = [claim for claim in package.claims if claim.forum_track in {"canada_or_cross_border", "alberta_primary"}]
    canada_evidence_ids = _ordered_unique(
        evidence_id for claim in canada_claims for evidence_id in claim.evidence_ids
    )
    canada_events = _ordered_unique(
        event_id for claim in canada_claims for event_id in claim.chronology_event_ids
    )

    lines = [
        f"# Protective Alberta Filing Skeleton: {package.matter}",
        "",
        "## Draft Use",
        "Internal drafting skeleton only. Confirm forum, parties, causes of action, and limitation analysis before filing.",
        "",
        "## Proposed Caption",
        "Court of King's Bench of Alberta",
        "Judicial Centre: Calgary",
        "",
        "Plaintiff: NRG Bloom Inc.",
        "Defendant(s): TON Infrastructure Ltd., and any additional Alberta-linked defendants to be confirmed",
        "",
        "## Purpose of Protective Filing",
        f"- Current Canadian path: {matter.canadian_path}",
        f"- Protective filing needed: {matter.protective_filing_needed}",
        f"- Representation mode: {matter.representation_mode}",
        "- Objective: preserve Canadian leverage and protect the Axxela non-circumvention track while Nigerian proceedings continue.",
        "",
        "## Core Alberta-Oriented Claims",
    ]
    for claim in canada_claims:
        lines.append(f"- {claim.title} ({claim.claim_id})")
        lines.append(f"  Theory: {claim.theory}")
        lines.append(f"  Remedy objective: {claim.remedy_objective}")
    if not canada_claims:
        lines.append("- No Canada-specific claim is fully isolated yet; use C2 as the main protective anchor.")
    lines.extend(
        [
            "",
            "## Draft Factual Themes",
            "- NRG Bloom originated and developed the Axxela opportunity before TON entered the record.",
            "- TON was introduced to Axxela through NRG Bloom and later excluded NRG Bloom from the core communication stream.",
            "- The July 4 direct-arrangement statement to Axxela is a central pleaded fact.",
            "- The Canadian filing should be framed as protective and leverage-preserving, not as a substitute for the Nigerian dispute track.",
            "",
            "## Requested Relief",
            "- Damages to be particularized after final quantification review.",
            "- Equitable or protective relief as Canadian counsel strategy may support.",
            "- Costs and any further relief the Court deems just.",
            "",
            "## Chronology Anchors",
        ]
    )
    for event_id in canada_events:
        event = _find_event(package, event_id)
        if event:
            lines.append(f"- {event.date} {event.event_id} {event.title}")
    lines.extend(
        [
            "",
            "## Evidence Anchors",
        ]
    )
    for evidence_id in canada_evidence_ids:
        evidence = _find_evidence(package, evidence_id)
        if evidence:
            lines.append(f"- {evidence.evidence_id}: {evidence.title} ({evidence.path.name})")
    lines.extend(
        [
            "",
            "## Drafting Gaps To Resolve Before Filing",
            "- Confirm the exact Alberta causes of action and defendant list.",
            "- Confirm whether injunctive relief is strategically worth seeking.",
            "- Confirm limitation analysis and service mechanics.",
            "- Convert the high-level damages anchor into a quantified schedule.",
            "",
        ]
    )
    return lines


def _find_event(package: FilingPackage, event_id: str) -> FilingEvent | None:
    for event in package.chronology:
        if event.event_id == event_id:
            return event
    return None


def _find_evidence(package: FilingPackage, evidence_id: str) -> FilingEvidence | None:
    for evidence in package.evidence:
        if evidence.evidence_id == evidence_id:
            return evidence
    return None


def _ordered_unique(values):
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered
