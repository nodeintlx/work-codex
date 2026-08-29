from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import yaml

from .store import StoreError


@dataclass(frozen=True)
class FactSource:
    path: str
    excerpt: str
    source_type: str
    authority: str
    title: str | None = None
    url: str | None = None
    published_on: str | None = None
    checked_on: str | None = None


@dataclass(frozen=True)
class VerifiedFact:
    fact_id: str
    claim: str
    status: str
    scope: str
    sources: list[FactSource]


@dataclass(frozen=True)
class BriefVerification:
    slug: str
    title: str
    fact_ids: list[str]
    facts: list[VerifiedFact]


@dataclass(frozen=True)
class FactcheckResult:
    registry_path: Path
    fact_count: int
    briefs: list[BriefVerification]
    verification_standard: str = (
        "3 corroborating sources minimum per fact; public and hybrid claims require at least 2 authoritative external sources"
    )


def load_fact_registry(path: Path) -> dict[str, VerifiedFact]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise StoreError(f"fact registry did not load as a mapping: {path}")
    raw_facts = data.get("facts", [])
    if not isinstance(raw_facts, list):
        raise StoreError(f"fact registry facts must be a list: {path}")

    facts: dict[str, VerifiedFact] = {}
    for item in raw_facts:
        if not isinstance(item, dict):
            raise StoreError(f"fact registry entry must be an object: {path}")
        fact_id = str(item.get("id", "")).strip()
        claim = str(item.get("claim", "")).strip()
        status = str(item.get("status", "verified")).strip()
        scope = str(item.get("scope", "internal")).strip()
        sources_raw = item.get("sources", [])
        if not fact_id or not claim:
            raise StoreError(f"fact registry entries require id and claim: {path}")
        if not isinstance(sources_raw, list):
            raise StoreError(f"fact sources must be a list for {fact_id}")
        sources = []
        for source in sources_raw:
            if not isinstance(source, dict):
                raise StoreError(f"fact source must be an object for {fact_id}")
            source_path = str(source.get("path", "")).strip()
            excerpt = str(source.get("excerpt", "")).strip()
            source_type = str(source.get("type", source.get("source_type", ""))).strip() or "internal_doc"
            authority = str(source.get("authority", "")).strip() or _default_authority_for_source_type(source_type)
            if not source_path or not excerpt:
                raise StoreError(f"fact sources require path and excerpt for {fact_id}")
            sources.append(
                FactSource(
                    path=source_path,
                    excerpt=excerpt,
                    source_type=source_type,
                    authority=authority,
                    title=_optional_string(source.get("title")),
                    url=_optional_string(source.get("url")),
                    published_on=_optional_string(source.get("published_on")),
                    checked_on=_optional_string(source.get("checked_on")),
                )
            )
        if len(sources) < 3:
            raise StoreError(f"fact {fact_id} must have at least 3 corroborating sources")
        _validate_source_mix(fact_id=fact_id, scope=scope, sources=sources)
        facts[fact_id] = VerifiedFact(
            fact_id=fact_id,
            claim=claim,
            status=status,
            scope=scope,
            sources=sources,
        )
    return facts


def factcheck_campaign(root: Path, campaign_path: Path) -> FactcheckResult:
    with campaign_path.open("r", encoding="utf-8") as handle:
        campaign = yaml.safe_load(handle)
    if not isinstance(campaign, dict):
        raise StoreError(f"campaign did not load as a mapping: {campaign_path}")

    registry_raw = str(campaign.get("fact_registry", "")).strip()
    if not registry_raw:
        raise StoreError(f"campaign does not declare fact_registry: {campaign_path}")
    registry_path = _resolve_path(campaign_path.parent, registry_raw)
    facts = load_fact_registry(registry_path)

    raw_briefs = campaign.get("briefs", [])
    if not isinstance(raw_briefs, list):
        raise StoreError(f"campaign briefs must be a list: {campaign_path}")

    briefs: list[BriefVerification] = []
    for brief in raw_briefs:
        if not isinstance(brief, dict):
            raise StoreError(f"campaign brief must be an object: {campaign_path}")
        fact_ids = [str(item) for item in brief.get("fact_ids", [])]
        if not fact_ids:
            raise StoreError(f"brief {brief.get('slug', '')} has no fact_ids")
        resolved = []
        for fact_id in fact_ids:
            if fact_id not in facts:
                raise StoreError(f"brief {brief.get('slug', '')} references unknown fact_id: {fact_id}")
            resolved.append(facts[fact_id])
        briefs.append(
            BriefVerification(
                slug=str(brief.get("slug", "")),
                title=str(brief.get("title", "")),
                fact_ids=fact_ids,
                facts=resolved,
            )
        )
    return FactcheckResult(registry_path=registry_path, fact_count=len(facts), briefs=briefs)


def write_factcheck_report(output_dir: Path, result: FactcheckResult) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written_paths: list[Path] = []

    report_lines = [
        "# Factcheck Report",
        "",
        f"Registry: {result.registry_path}",
        f"Verified facts available: {result.fact_count}",
        f"Verification standard: {result.verification_standard}",
        "",
    ]

    for brief in result.briefs:
        brief_dir = output_dir / brief.slug
        brief_dir.mkdir(parents=True, exist_ok=True)
        verification_lines = [
            f"# Verification Pack — {brief.title}",
            "",
            f"Brief slug: {brief.slug}",
            f"Verification status: {len(brief.facts)} facts / each with 3+ corroborating sources",
            f"Verification standard: {result.verification_standard}",
            "",
        ]
        report_lines.extend([f"## {brief.title}", ""])
        for fact in brief.facts:
            report_lines.extend(
                [
                    f"- {fact.fact_id}: {fact.claim}",
                ]
            )
            verification_lines.extend(
                [
                    f"## {fact.fact_id}",
                    fact.claim,
                    "",
                    f"Status: {fact.status}",
                    f"Scope: {fact.scope}",
                    "Sources:",
                ]
            )
            for source in fact.sources:
                report_lines.append(f"  - [{source.source_type}] {source.authority}: {source.path}")
                verification_lines.append(f"- [{source.source_type}] {source.authority}: {source.path}")
                if source.title:
                    verification_lines.append(f"  Title: {source.title}")
                if source.url:
                    verification_lines.append(f"  URL: {source.url}")
                verification_lines.append(f"  Excerpt: {source.excerpt}")
                if source.published_on:
                    verification_lines.append(f"  Published: {source.published_on}")
                if source.checked_on:
                    verification_lines.append(f"  Checked: {source.checked_on}")
            verification_lines.append("")
        report_lines.append("")
        verification_path = brief_dir / "verification.md"
        verification_path.write_text("\n".join(verification_lines).rstrip() + "\n", encoding="utf-8")
        written_paths.append(verification_path)

        verification_json = {
            "slug": brief.slug,
            "title": brief.title,
            "fact_ids": brief.fact_ids,
            "verified": True,
            "verification_standard": result.verification_standard,
            "facts": [
                {
                    "id": fact.fact_id,
                    "claim": fact.claim,
                    "status": fact.status,
                    "scope": fact.scope,
                    "sources": [
                        {
                            "path": source.path,
                            "excerpt": source.excerpt,
                            "source_type": source.source_type,
                            "authority": source.authority,
                            "title": source.title,
                            "url": source.url,
                            "published_on": source.published_on,
                            "checked_on": source.checked_on,
                        }
                        for source in fact.sources
                    ],
                }
                for fact in brief.facts
            ],
        }
        verification_json_path = brief_dir / "verification.json"
        verification_json_path.write_text(json.dumps(verification_json, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        written_paths.append(verification_json_path)

    report_path = output_dir / "factcheck-report.md"
    report_path.write_text("\n".join(report_lines).rstrip() + "\n", encoding="utf-8")
    written_paths.append(report_path)
    return written_paths


def _resolve_path(base_dir: Path, raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else (base_dir / path).resolve()


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _default_authority_for_source_type(source_type: str) -> str:
    mapping = {
        "internal_doc": "internal",
        "internal_record": "internal",
        "official_report": "institutional",
        "official_dataset": "institutional",
        "regulator": "institutional",
        "multilateral": "institutional",
        "trusted_media": "media",
        "industry_report": "industry",
        "company_release": "company",
        "company_profile": "company",
        "industry_voice": "voice",
        "market_voice": "voice",
        "social_post": "voice",
    }
    return mapping.get(source_type, "unknown")


def _validate_source_mix(*, fact_id: str, scope: str, sources: list[FactSource]) -> None:
    authoritative_types = {"official_report", "official_dataset", "regulator", "multilateral", "industry_report", "trusted_media"}
    voice_types = {"industry_voice", "market_voice", "social_post"}
    internal_types = {"internal_doc", "internal_record"}
    authoritative_count = sum(1 for source in sources if source.source_type in authoritative_types)
    voice_count = sum(1 for source in sources if source.source_type in voice_types)
    internal_count = sum(1 for source in sources if source.source_type in internal_types)

    if scope in {"public", "external", "hybrid"} and authoritative_count < 2:
        raise StoreError(f"fact {fact_id} with scope {scope} must include at least 2 authoritative external sources")
    if voice_count and authoritative_count == 0:
        raise StoreError(f"fact {fact_id} cannot rely on voice-only sources")
    if scope == "internal" and internal_count == 0:
        raise StoreError(f"fact {fact_id} with scope internal must include at least 1 internal source")
