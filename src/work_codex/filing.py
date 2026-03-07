from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class FilingEvidence:
    evidence_id: str
    title: str
    source_type: str
    path: Path
    exists: bool
    strength: str
    issues: tuple[str, ...]


@dataclass(frozen=True)
class FilingEvent:
    event_id: str
    date: str
    phase: str
    title: str
    significance: str
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class FilingClaim:
    claim_id: str
    title: str
    forum_track: str
    status: str
    pleading_priority: str
    remedy_objective: str
    theory: str
    key_facts: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    chronology_event_ids: tuple[str, ...]
    damages_anchor: str
    pleading_notes: str


@dataclass(frozen=True)
class FilingReadiness:
    level: str
    critical_claims_ready: int
    critical_evidence_missing: int
    missing_references: tuple[str, ...]
    recommendations: tuple[str, ...]


@dataclass(frozen=True)
class FilingPackage:
    matter: str
    claims: tuple[FilingClaim, ...]
    chronology: tuple[FilingEvent, ...]
    evidence: tuple[FilingEvidence, ...]
    readiness: FilingReadiness


def load_filing_package(root: Path) -> FilingPackage:
    matter_root = root / "nrg-bloom" / "litigation-ton"
    claims_data = _load_yaml_mapping(matter_root / "claims-map.yaml")
    chronology_data = _load_yaml_mapping(matter_root / "chronology-map.yaml")
    evidence_data = _load_yaml_mapping(matter_root / "evidence-map.yaml")

    evidence = tuple(_parse_evidence(matter_root, item) for item in evidence_data.get("evidence", []))
    chronology = tuple(_parse_event(item) for item in chronology_data.get("events", []))
    claims = tuple(_parse_claim(item) for item in claims_data.get("claims", []))
    readiness = _build_readiness(claims, chronology, evidence)
    matter = str(claims_data.get("matter") or chronology_data.get("matter") or evidence_data.get("matter") or "")
    return FilingPackage(
        matter=matter,
        claims=claims,
        chronology=chronology,
        evidence=evidence,
        readiness=readiness,
    )


def filing_validation_errors(package: FilingPackage) -> list[str]:
    errors: list[str] = []
    if not package.matter:
        errors.append("filing package matter is blank")
    if not package.claims:
        errors.append("claims-map.yaml contains no claims")
    if not package.chronology:
        errors.append("chronology-map.yaml contains no events")
    if not package.evidence:
        errors.append("evidence-map.yaml contains no evidence items")

    evidence_ids = {item.evidence_id for item in package.evidence}
    chronology_ids = {item.event_id for item in package.chronology}
    for item in package.evidence:
        if not item.exists:
            errors.append(f"missing evidence file for {item.evidence_id}: {item.path}")
    for claim in package.claims:
        for evidence_id in claim.evidence_ids:
            if evidence_id not in evidence_ids:
                errors.append(f"{claim.claim_id} references missing evidence id: {evidence_id}")
        for event_id in claim.chronology_event_ids:
            if event_id not in chronology_ids:
                errors.append(f"{claim.claim_id} references missing chronology id: {event_id}")
    for event in package.chronology:
        for evidence_id in event.evidence_ids:
            if evidence_id not in evidence_ids:
                errors.append(f"{event.event_id} references missing evidence id: {evidence_id}")
    return errors


def filing_outline_lines(package: FilingPackage) -> list[str]:
    lines = [
        "filing outline",
        f"matter: {package.matter}",
        f"readiness: {package.readiness.level}",
        "claims",
    ]
    for claim in package.claims:
        lines.append(f"  [{claim.pleading_priority}] {claim.claim_id} {claim.title} ({claim.status}, {claim.forum_track})")
        lines.append(f"    theory: {claim.theory}")
    lines.append("chronology anchors")
    for event in package.chronology:
        lines.append(f"  {event.date} {event.event_id} {event.title}")
    lines.append("evidence anchors")
    for item in package.evidence:
        state = "ok" if item.exists else "missing"
        lines.append(f"  [{state}] {item.evidence_id} -> {item.path.name}")
    return lines


def _build_readiness(
    claims: tuple[FilingClaim, ...],
    chronology: tuple[FilingEvent, ...],
    evidence: tuple[FilingEvidence, ...],
) -> FilingReadiness:
    missing_refs: list[str] = []
    evidence_ids = {item.evidence_id for item in evidence}
    chronology_ids = {item.event_id for item in chronology}
    critical_claims_ready = 0
    for claim in claims:
        if claim.pleading_priority == "critical" and claim.status == "ready_to_plead":
            critical_claims_ready += 1
        for evidence_id in claim.evidence_ids:
            if evidence_id not in evidence_ids:
                missing_refs.append(f"{claim.claim_id}:{evidence_id}")
        for event_id in claim.chronology_event_ids:
            if event_id not in chronology_ids:
                missing_refs.append(f"{claim.claim_id}:{event_id}")
    for event in chronology:
        for evidence_id in event.evidence_ids:
            if evidence_id not in evidence_ids:
                missing_refs.append(f"{event.event_id}:{evidence_id}")
    critical_evidence_missing = sum(1 for item in evidence if item.strength == "critical" and not item.exists)
    recommendations: list[str] = []
    if critical_evidence_missing:
        recommendations.append("Restore every missing critical evidence file before drafting a protective filing package.")
    if any(claim.status != "ready_to_plead" for claim in claims if claim.pleading_priority in {"critical", "high"}):
        recommendations.append("Resolve the high-priority claims still marked in_progress or needs_forum_review.")
    if not chronology:
        recommendations.append("Add a pleading chronology subset before draft generation.")
    if not recommendations:
        recommendations.append("Claims, chronology, and evidence map are in a usable state for draft generation.")
    if critical_evidence_missing or missing_refs:
        level = "blocked"
    elif critical_claims_ready < 2:
        level = "in_progress"
    else:
        level = "ready_for_draft"
    return FilingReadiness(
        level=level,
        critical_claims_ready=critical_claims_ready,
        critical_evidence_missing=critical_evidence_missing,
        missing_references=tuple(sorted(missing_refs)),
        recommendations=tuple(recommendations),
    )


def _parse_evidence(matter_root: Path, item: dict[str, Any]) -> FilingEvidence:
    relative_path = Path(str(item.get("path", "")))
    path = matter_root / relative_path
    issues = tuple(str(value) for value in item.get("issues", []) if isinstance(value, str))
    return FilingEvidence(
        evidence_id=str(item.get("id", "")),
        title=str(item.get("title", "")),
        source_type=str(item.get("source_type", "")),
        path=path,
        exists=path.exists(),
        strength=str(item.get("strength", "")),
        issues=issues,
    )


def _parse_event(item: dict[str, Any]) -> FilingEvent:
    return FilingEvent(
        event_id=str(item.get("id", "")),
        date=str(item.get("date", "")),
        phase=str(item.get("phase", "")),
        title=str(item.get("title", "")),
        significance=str(item.get("significance", "")),
        evidence_ids=tuple(str(value) for value in item.get("evidence_ids", []) if isinstance(value, str)),
    )


def _parse_claim(item: dict[str, Any]) -> FilingClaim:
    return FilingClaim(
        claim_id=str(item.get("id", "")),
        title=str(item.get("title", "")),
        forum_track=str(item.get("forum_track", "")),
        status=str(item.get("status", "")),
        pleading_priority=str(item.get("pleading_priority", "")),
        remedy_objective=str(item.get("remedy_objective", "")),
        theory=str(item.get("theory", "")),
        key_facts=tuple(str(value) for value in item.get("key_facts", []) if isinstance(value, str)),
        evidence_ids=tuple(str(value) for value in item.get("evidence_ids", []) if isinstance(value, str)),
        chronology_event_ids=tuple(str(value) for value in item.get("chronology_event_ids", []) if isinstance(value, str)),
        damages_anchor=str(item.get("damages_anchor", "")),
        pleading_notes=str(item.get("pleading_notes", "")),
    )


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"missing filing file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not load as a mapping")
    return data
