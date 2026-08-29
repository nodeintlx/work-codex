from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
from textwrap import dedent
from typing import Any

import yaml

from .factcheck import VerifiedFact, load_fact_registry
from .store import StoreError


@dataclass(frozen=True)
class AuthorityBuild:
    output_dir: Path
    written_paths: list[Path]


@dataclass(frozen=True)
class WeeklyAuthorityBatch:
    output_dir: Path
    written_paths: list[Path]


def generate_authority_system(root: Path, plan_path: Path) -> AuthorityBuild:
    plan = _load_plan(plan_path)
    facts = load_fact_registry(_resolve_path(plan_path.parent, str(plan["fact_registry"])))
    _validate_plan_facts(plan, facts)

    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    slug = str(plan.get("slug", plan_path.stem)).strip() or plan_path.stem
    output_dir = root / "nrg-bloom" / "authority-engine" / "generated" / f"{stamp}-{slug}"
    output_dir.mkdir(parents=True, exist_ok=True)

    written_paths: list[Path] = []
    docs: dict[Path, str] = {
        output_dir / "authority-operating-system.md": _authority_operating_system(plan),
        output_dir / "source-watchlist.md": _source_watchlist_markdown(plan),
        output_dir / "investor-objection-bank.md": _objection_bank_markdown(plan, facts),
        output_dir / "evergreen-franchise-map.md": _franchise_map_markdown(plan, facts),
        output_dir / "distribution-rules.md": _distribution_rules_markdown(plan),
        output_dir / "sanitized-founder-insight-rules.md": _founder_insight_rules(plan),
        output_dir / "external-intelligence-intake.md": _external_intelligence_intake(plan),
    }
    for path, content in docs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
        written_paths.append(path)

    watchlist_path = output_dir / "source-watchlist.yaml"
    watchlist_path.write_text(yaml.safe_dump(_source_watchlist_payload(plan), sort_keys=False), encoding="utf-8")
    written_paths.append(watchlist_path)

    objections_path = output_dir / "investor-objection-bank.yaml"
    objections_path.write_text(yaml.safe_dump(_objection_bank_payload(plan), sort_keys=False), encoding="utf-8")
    written_paths.append(objections_path)

    franchise_path = output_dir / "evergreen-franchise-map.yaml"
    franchise_path.write_text(yaml.safe_dump(_franchise_map_payload(plan), sort_keys=False), encoding="utf-8")
    written_paths.append(franchise_path)

    queue_path = output_dir / "external-intel-queue.yaml"
    queue_path.write_text(yaml.safe_dump(_external_intel_queue_payload(plan), sort_keys=False), encoding="utf-8")
    written_paths.append(queue_path)

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(UTC).isoformat(),
                "plan": {"slug": slug, "title": str(plan.get("title", slug))},
                "outputs": {
                    "authority_operating_system": str(output_dir / "authority-operating-system.md"),
                    "source_watchlist": str(watchlist_path),
                    "investor_objection_bank": str(objections_path),
                    "evergreen_franchise_map": str(franchise_path),
                    "external_intel_queue": str(queue_path),
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    written_paths.append(manifest_path)

    latest_dir = root / "nrg-bloom" / "authority-engine" / "generated" / "latest"
    latest_dir.mkdir(parents=True, exist_ok=True)
    latest_path = latest_dir / "LATEST.txt"
    latest_path.write_text(str(output_dir) + "\n", encoding="utf-8")
    written_paths.append(latest_path)

    return AuthorityBuild(output_dir=output_dir, written_paths=written_paths)


def generate_weekly_authority_batch(root: Path, plan_path: Path) -> WeeklyAuthorityBatch:
    plan = _load_plan(plan_path)
    facts = load_fact_registry(_resolve_path(plan_path.parent, str(plan["fact_registry"])))
    _validate_plan_facts(plan, facts)

    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    slug = str(plan.get("slug", plan_path.stem)).strip() or plan_path.stem
    output_dir = root / "nrg-bloom" / "authority-engine" / "generated" / f"{stamp}-{slug}-weekly-batch"
    output_dir.mkdir(parents=True, exist_ok=True)

    written_paths: list[Path] = []
    weekly_batch_path = output_dir / "weekly-authority-batch.md"
    weekly_batch_path.write_text(_weekly_authority_batch_markdown(plan, facts).rstrip() + "\n", encoding="utf-8")
    written_paths.append(weekly_batch_path)

    weekly_queue_path = output_dir / "weekly-authority-queue.yaml"
    weekly_queue_path.write_text(yaml.safe_dump(_weekly_authority_queue_payload(plan), sort_keys=False), encoding="utf-8")
    written_paths.append(weekly_queue_path)

    source_priority_path = output_dir / "source-priority-list.md"
    source_priority_path.write_text(_source_priority_list(plan).rstrip() + "\n", encoding="utf-8")
    written_paths.append(source_priority_path)

    prompt_pack_path = output_dir / "editorial-prompt-pack.md"
    prompt_pack_path.write_text(_editorial_prompt_pack(plan, facts).rstrip() + "\n", encoding="utf-8")
    written_paths.append(prompt_pack_path)

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(UTC).isoformat(),
                "plan": {"slug": slug, "title": str(plan.get("title", slug))},
                "files": [str(path) for path in written_paths],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    written_paths.append(manifest_path)

    return WeeklyAuthorityBatch(output_dir=output_dir, written_paths=written_paths)


def _load_plan(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise StoreError(f"authority plan did not load as a mapping: {path}")
    return data


def _resolve_path(base_dir: Path, raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else (base_dir / path).resolve()


def _validate_plan_facts(plan: dict[str, Any], facts: dict[str, VerifiedFact]) -> None:
    referenced: set[str] = set()
    for objection in plan.get("objections", []):
        if isinstance(objection, dict):
            referenced.update(str(item) for item in objection.get("fact_ids", []))
    for franchise in plan.get("franchises", []):
        if isinstance(franchise, dict):
            referenced.update(str(item) for item in franchise.get("fact_ids", []))
    missing = sorted(fact_id for fact_id in referenced if fact_id and fact_id not in facts)
    if missing:
        raise StoreError(f"authority plan references unknown fact ids: {', '.join(missing)}")


def _authority_operating_system(plan: dict[str, Any]) -> str:
    lines = [
        f"# Authority Operating System — {plan.get('title', '')}",
        "",
        "This operating system is designed for periods when NRG Bloom should stay visible without depending on fresh operating disclosures.",
        "",
        "## Core Principle",
        "",
        str(plan.get("core_principle", "")).strip(),
        "",
        "## Inputs",
        "",
    ]
    for item in plan.get("inputs", []):
        lines.append(f"- {item}")
    lines.extend(["", "## Constraints", ""])
    for item in plan.get("constraints", []):
        lines.append(f"- {item}")
    lines.extend(["", "## Weekly Lanes", ""])
    for lane in plan.get("weekly_lanes", []):
        if not isinstance(lane, dict):
            continue
        lines.extend(
            [
                f"## {lane.get('day', '')}",
                f"- Lane: {lane.get('lane', '')}",
                f"- Objective: {lane.get('objective', '')}",
                f"- Output: {lane.get('output', '')}",
                f"- Primary objection: {lane.get('objection', '')}",
                "",
            ]
        )
    return "\n".join(lines)


def _source_watchlist_markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# Source Watchlist",
        "",
        "These are the sources that should keep feeding the authority system even when internal operating updates are limited.",
        "",
    ]
    for item in plan.get("source_watchlist", []):
        if not isinstance(item, dict):
            continue
        lines.extend(
            [
                f"## {item.get('name', '')}",
                f"- Tier: {item.get('tier', '')}",
                f"- Type: {item.get('type', '')}",
                f"- Why it matters: {item.get('why_it_matters', '')}",
                f"- Tracking focus: {', '.join(str(x) for x in item.get('tracking_focus', []))}",
                f"- URL: {item.get('url', '')}",
                "",
            ]
        )
    return "\n".join(lines)


def _objection_bank_markdown(plan: dict[str, Any], facts: dict[str, VerifiedFact]) -> str:
    lines = [
        "# Investor Objection Bank",
        "",
        "These are the recurring objections the content system should answer repeatedly.",
        "",
    ]
    for item in plan.get("objections", []):
        if not isinstance(item, dict):
            continue
        lines.extend(
            [
                f"## {item.get('question', '')}",
                f"- Short answer: {item.get('answer', '')}",
                f"- Best formats: {', '.join(str(x) for x in item.get('formats', []))}",
                "- Supporting proof:",
            ]
        )
        for fact_id in item.get("fact_ids", []):
            lines.append(f"  - {facts[str(fact_id)].claim}")
        lines.append("")
    return "\n".join(lines)


def _franchise_map_markdown(plan: dict[str, Any], facts: dict[str, VerifiedFact]) -> str:
    lines = [
        "# Evergreen Franchise Map",
        "",
        "These are the repeatable content franchises that should keep NRG Bloom visible.",
        "",
    ]
    for item in plan.get("franchises", []):
        if not isinstance(item, dict):
            continue
        lines.extend(
            [
                f"## {item.get('name', '')}",
                f"- Purpose: {item.get('purpose', '')}",
                f"- Best audiences: {', '.join(str(x) for x in item.get('audiences', []))}",
                f"- Tone: {item.get('tone', '')}",
                f"- Recommended formats: {', '.join(str(x) for x in item.get('formats', []))}",
                "- Proof base:",
            ]
        )
        for fact_id in item.get("fact_ids", []):
            lines.append(f"  - {facts[str(fact_id)].claim}")
        if item.get("notes"):
            lines.append(f"- Notes: {item.get('notes', '')}")
        lines.append("")
    return "\n".join(lines)


def _distribution_rules_markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# Distribution Rules",
        "",
        "Use these rules when deciding what should actually ship.",
        "",
    ]
    for item in plan.get("distribution_rules", []):
        lines.append(f"- {item}")
    return "\n".join(lines)


def _founder_insight_rules(plan: dict[str, Any]) -> str:
    lines = [
        "# Sanitized Founder Insight Rules",
        "",
        "Founder insight still matters, but it should be abstracted away from live-sensitive facts.",
        "",
    ]
    for item in plan.get("founder_insight_rules", []):
        lines.append(f"- {item}")
    return "\n".join(lines)


def _external_intelligence_intake(plan: dict[str, Any]) -> str:
    return dedent(
        f"""
        # External Intelligence Intake

        Use this intake when NRG Bloom needs to stay visible without relying on fresh operating disclosures.

        ## What To Capture
        {chr(10).join(f"- {item}" for item in plan.get("intake_fields", []))}

        ## Fast Triage Rule
        - If the source strengthens a current objection answer, it should move into next week's queue.
        - If it is interesting but not directly useful, archive it under the watchlist instead of forcing content from it.
        - If it would require live-sensitive disclosure to make sense, hold it.
        """
    ).strip()


def _source_watchlist_payload(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_from": str(plan.get("title", "")),
        "sources": [
            {
                "name": str(item.get("name", "")),
                "tier": str(item.get("tier", "")),
                "type": str(item.get("type", "")),
                "url": str(item.get("url", "")),
                "why_it_matters": str(item.get("why_it_matters", "")),
                "tracking_focus": [str(x) for x in item.get("tracking_focus", [])],
            }
            for item in plan.get("source_watchlist", [])
            if isinstance(item, dict)
        ],
    }


def _objection_bank_payload(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_from": str(plan.get("title", "")),
        "objections": [
            {
                "question": str(item.get("question", "")),
                "answer": str(item.get("answer", "")),
                "formats": [str(x) for x in item.get("formats", [])],
                "fact_ids": [str(x) for x in item.get("fact_ids", [])],
            }
            for item in plan.get("objections", [])
            if isinstance(item, dict)
        ],
    }


def _franchise_map_payload(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_from": str(plan.get("title", "")),
        "franchises": [
            {
                "slug": str(item.get("slug", "")),
                "name": str(item.get("name", "")),
                "purpose": str(item.get("purpose", "")),
                "audiences": [str(x) for x in item.get("audiences", [])],
                "tone": str(item.get("tone", "")),
                "formats": [str(x) for x in item.get("formats", [])],
                "fact_ids": [str(x) for x in item.get("fact_ids", [])],
            }
            for item in plan.get("franchises", [])
            if isinstance(item, dict)
        ],
    }


def _external_intel_queue_payload(plan: dict[str, Any]) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for index, franchise in enumerate(plan.get("franchises", []), start=1):
        if not isinstance(franchise, dict):
            continue
        items.append(
            {
                "id": f"authority-{index:02d}",
                "franchise": str(franchise.get("slug", "")),
                "theme": str(franchise.get("name", "")),
                "purpose": str(franchise.get("purpose", "")),
                "audiences": [str(x) for x in franchise.get("audiences", [])],
                "formats": [str(x) for x in franchise.get("formats", [])],
                "fact_ids": [str(x) for x in franchise.get("fact_ids", [])],
                "status": "ready",
            }
        )
    return {"week_of": datetime.now(UTC).date().isoformat(), "queue": items}


def _weekly_authority_batch_markdown(plan: dict[str, Any], facts: dict[str, VerifiedFact]) -> str:
    lines = [
        f"# Weekly Authority Batch — {plan.get('title', '')}",
        "",
        "This weekly batch is designed to keep NRG Bloom visible through market intelligence, category framing, and sanitized founder conviction.",
        "",
    ]
    for lane in plan.get("weekly_lanes", []):
        if not isinstance(lane, dict):
            continue
        lines.extend(
            [
                f"## {lane.get('day', '')}",
                f"- Lane: {lane.get('lane', '')}",
                f"- Objective: {lane.get('objective', '')}",
                f"- Output: {lane.get('output', '')}",
                f"- Objection focus: {lane.get('objection', '')}",
            ]
        )
        for objection in plan.get("objections", []):
            if isinstance(objection, dict) and str(objection.get("slug", "")) == str(lane.get("objection_slug", "")):
                for fact_id in objection.get("fact_ids", []):
                    lines.append(f"  - Proof: {facts[str(fact_id)].claim}")
        lines.append("")
    return "\n".join(lines)


def _weekly_authority_queue_payload(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "week_of": datetime.now(UTC).date().isoformat(),
        "queue": [
            {
                "day": str(item.get("day", "")),
                "lane": str(item.get("lane", "")),
                "output": str(item.get("output", "")),
                "objective": str(item.get("objective", "")),
                "objection": str(item.get("objection", "")),
                "objection_slug": str(item.get("objection_slug", "")),
                "status": "planned",
            }
            for item in plan.get("weekly_lanes", [])
            if isinstance(item, dict)
        ],
    }


def _source_priority_list(plan: dict[str, Any]) -> str:
    lines = [
        "# Source Priority List",
        "",
        "These are the first sources to check each week before generating new authority content.",
        "",
    ]
    for item in plan.get("source_watchlist", [])[:6]:
        if not isinstance(item, dict):
            continue
        lines.append(f"- {item.get('name', '')}: {item.get('url', '')}")
    return "\n".join(lines)


def _editorial_prompt_pack(plan: dict[str, Any], facts: dict[str, VerifiedFact]) -> str:
    lines = [
        "# Editorial Prompt Pack",
        "",
        "Use these prompts to generate weekly authority content without drifting off the verified fact base.",
        "",
    ]
    for franchise in plan.get("franchises", []):
        if not isinstance(franchise, dict):
            continue
        lines.extend(
            [
                f"## {franchise.get('name', '')}",
                f"Prompt: Create a {', '.join(str(x) for x in franchise.get('formats', []))} for audiences {', '.join(str(x) for x in franchise.get('audiences', []))}. Keep the tone {franchise.get('tone', '')}. Anchor the piece in the following claims:",
            ]
        )
        for fact_id in franchise.get("fact_ids", []):
            lines.append(f"- {facts[str(fact_id)].claim}")
        lines.append("")
    return "\n".join(lines)
