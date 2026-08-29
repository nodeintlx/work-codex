from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import html
import json
from pathlib import Path
from textwrap import dedent
from typing import Any

import yaml

from .factcheck import VerifiedFact, load_fact_registry
from .store import StoreError


@dataclass(frozen=True)
class CapitalBuild:
    output_dir: Path
    written_paths: list[Path]


@dataclass(frozen=True)
class WeeklyCapitalBatch:
    output_dir: Path
    written_paths: list[Path]


def generate_capital_stack(root: Path, plan_path: Path) -> CapitalBuild:
    plan = _load_plan(plan_path)
    facts = load_fact_registry(_resolve_path(plan_path.parent, str(plan["fact_registry"])))
    _validate_plan_facts(plan, facts)

    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    slug = str(plan.get("slug", plan_path.stem)).strip() or plan_path.stem
    output_dir = root / "nrg-bloom" / "capital-engine" / "generated" / f"{stamp}-{slug}"
    output_dir.mkdir(parents=True, exist_ok=True)

    written_paths: list[Path] = []
    docs: dict[Path, str] = {
        output_dir / "investor-thesis" / "investor-memo.md": _investor_memo(plan, facts),
        output_dir / "investor-thesis" / "one-page-brief.md": _one_page_brief(plan, facts),
        output_dir / "diligence-room" / "proof-of-execution.md": _proof_of_execution(plan, facts),
        output_dir / "diligence-room" / "market-and-timing.md": _market_and_timing(plan, facts),
        output_dir / "diligence-room" / "diligence-snapshot.md": _diligence_snapshot(plan, facts),
        output_dir / "audience-playbook.md": _audience_playbook(plan, facts),
        output_dir / "distribution-playbook.md": _distribution_playbook(plan),
        output_dir / "content-to-capital-map.md": _content_to_capital_map(plan, facts),
        output_dir / "investor-outreach-sequences.md": _investor_outreach_sequences(plan),
        output_dir / "weekly-operating-system.md": _weekly_operating_system(plan),
        output_dir / "site-source-notes.md": _site_source_notes(plan),
    }
    for path, content in docs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
        written_paths.append(path)

    audience_map_path = output_dir / "audience-map.yaml"
    audience_map_path.write_text(yaml.safe_dump(_audience_map_payload(plan), sort_keys=False), encoding="utf-8")
    written_paths.append(audience_map_path)

    backlog_path = output_dir / "content-backlog.yaml"
    backlog_path.write_text(yaml.safe_dump(_content_backlog_payload(plan), sort_keys=False), encoding="utf-8")
    written_paths.append(backlog_path)

    manifest = {
        "generated_at": datetime.now(UTC).isoformat(),
        "plan": {
            "slug": slug,
            "title": str(plan.get("title", slug)),
        },
        "outputs": {
            "investor_memo": str(output_dir / "investor-thesis" / "investor-memo.md"),
            "one_page_brief": str(output_dir / "investor-thesis" / "one-page-brief.md"),
            "proof_of_execution": str(output_dir / "diligence-room" / "proof-of-execution.md"),
            "market_and_timing": str(output_dir / "diligence-room" / "market-and-timing.md"),
            "diligence_snapshot": str(output_dir / "diligence-room" / "diligence-snapshot.md"),
            "audience_map": str(audience_map_path),
            "content_backlog": str(backlog_path),
        },
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written_paths.append(manifest_path)

    dashboard_path = output_dir / "capital-dashboard.html"
    dashboard_path.write_text(_capital_dashboard_html(plan, manifest), encoding="utf-8")
    written_paths.append(dashboard_path)

    latest_dir = root / "nrg-bloom" / "capital-engine" / "generated" / "latest"
    latest_dir.mkdir(parents=True, exist_ok=True)
    latest_path = latest_dir / "LATEST.txt"
    latest_path.write_text(str(output_dir) + "\n", encoding="utf-8")
    written_paths.append(latest_path)

    return CapitalBuild(output_dir=output_dir, written_paths=written_paths)


def generate_weekly_capital_batch(root: Path, plan_path: Path) -> WeeklyCapitalBatch:
    plan = _load_plan(plan_path)
    facts = load_fact_registry(_resolve_path(plan_path.parent, str(plan["fact_registry"])))
    _validate_plan_facts(plan, facts)

    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    slug = str(plan.get("slug", plan_path.stem)).strip() or plan_path.stem
    output_dir = root / "nrg-bloom" / "capital-engine" / "generated" / f"{stamp}-{slug}-weekly-batch"
    output_dir.mkdir(parents=True, exist_ok=True)

    written_paths: list[Path] = []
    batch_plan_path = output_dir / "weekly-batch.md"
    batch_plan_path.write_text(_weekly_batch_markdown(plan, facts).rstrip() + "\n", encoding="utf-8")
    written_paths.append(batch_plan_path)

    batch_queue_path = output_dir / "weekly-content-queue.yaml"
    batch_queue_path.write_text(yaml.safe_dump(_weekly_content_queue_payload(plan), sort_keys=False), encoding="utf-8")
    written_paths.append(batch_queue_path)

    touch_list_path = output_dir / "investor-touch-list.md"
    touch_list_path.write_text(_investor_touch_list(plan).rstrip() + "\n", encoding="utf-8")
    written_paths.append(touch_list_path)

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
    return WeeklyCapitalBatch(output_dir=output_dir, written_paths=written_paths)


def _load_plan(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise StoreError(f"capital plan did not load as a mapping: {path}")
    return data


def _resolve_path(base_dir: Path, raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else (base_dir / path).resolve()


def _validate_plan_facts(plan: dict[str, Any], facts: dict[str, VerifiedFact]) -> None:
    referenced: set[str] = set()
    evidence = plan.get("evidence", {})
    if isinstance(evidence, dict):
        for values in evidence.values():
            if isinstance(values, list):
                referenced.update(str(value) for value in values)
    for audience in plan.get("audiences", []):
        if isinstance(audience, dict):
            referenced.update(str(value) for value in audience.get("proof_fact_ids", []))
    for objection in plan.get("objections", []):
        if isinstance(objection, dict):
            referenced.update(str(value) for value in objection.get("fact_ids", []))
    for franchise in plan.get("franchises", []):
        if isinstance(franchise, dict):
            referenced.update(str(value) for value in franchise.get("fact_ids", []))
    missing = sorted(fact_id for fact_id in referenced if fact_id and fact_id not in facts)
    if missing:
        raise StoreError(f"capital plan references unknown fact ids: {', '.join(missing)}")


def _investor_memo(plan: dict[str, Any], facts: dict[str, VerifiedFact]) -> str:
    company = plan.get("company", {})
    capital = plan.get("capital", {})
    evidence = plan.get("evidence", {})
    lines = [
        f"# Investor Memo — {plan.get('title', 'NRG Bloom Investor Conversion')}",
        "",
        "## Company Snapshot",
        "",
        f"- Company: {company.get('name', 'NRG Bloom')}",
        f"- Headquarters: {company.get('headquarters', 'Montreal, Canada')}",
        f"- Operating geography: {company.get('operating_geography', 'Nigeria')}",
        f"- Operating model: {company.get('operating_model', '')}",
        f"- Current stage: {company.get('current_stage', '')}",
        "",
        "## Positioning",
        "",
        str(plan.get("positioning", "")).strip(),
        "",
        "## Core Investment Thesis",
        "",
        str(capital.get("core_thesis", "")).strip(),
        "",
        "## Verified Proof Today",
        "",
    ]
    lines.extend(_fact_bullet_lines(facts, evidence.get("company_proof", []), include_urls=False))
    lines.extend(
        [
            "",
            "## Why This Window Exists",
            "",
            str(capital.get("why_now", "")).strip(),
            "",
        ]
    )
    lines.extend(_fact_bullet_lines(facts, evidence.get("market_timing", []), include_urls=False))
    lines.extend(
        [
            "",
            "## Category Lineage",
            "",
            "NRG Bloom is not asking investors to believe stranded-gas compute is a speculative category. The category logic is already visible in North America; the question is which operator can adapt it to African field conditions.",
            "",
        ]
    )
    lines.extend(_fact_bullet_lines(facts, evidence.get("category_lineage", []), include_urls=False))
    lines.extend(
        [
            "",
            "## Why NRG Bloom Could Win",
            "",
            str(capital.get("winning_hypothesis", "")).strip(),
            "",
            "## What Capital Unlocks",
            "",
        ]
    )
    for item in capital.get("use_of_funds", []):
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## What This Means For Investors",
            "",
            str(capital.get("investor_fit", "")).strip(),
            "",
            "## Next Diligence Step",
            "",
            str(capital.get("next_step", "")).strip(),
            "",
            "## Evidence Appendix",
            "",
        ]
    )
    lines.extend(_fact_appendix_lines(facts, evidence.get("company_proof", []) + evidence.get("market_timing", []) + evidence.get("category_lineage", [])))
    return "\n".join(lines)


def _one_page_brief(plan: dict[str, Any], facts: dict[str, VerifiedFact]) -> str:
    company = plan.get("company", {})
    capital = plan.get("capital", {})
    evidence = plan.get("evidence", {})
    lines = [
        f"# One-Page Brief — {company.get('name', 'NRG Bloom')}",
        "",
        f"**What it is:** {company.get('operating_model', '')}",
        f"**Where it operates:** {company.get('operating_geography', '')}",
        f"**Why it matters:** {capital.get('core_thesis', '')}",
        "",
        "## Verified Signals",
        "",
    ]
    lines.extend(_fact_bullet_lines(facts, evidence.get("company_proof", [])[:3], include_urls=False))
    lines.extend(
        [
            "",
            "## Market Signals",
            "",
        ]
    )
    lines.extend(_fact_bullet_lines(facts, evidence.get("market_timing", [])[:3], include_urls=False))
    lines.extend(
        [
            "",
            "## Investment Framing",
            "",
            f"- Raise status: {capital.get('raise_status', '')}",
            f"- Investor fit: {capital.get('investor_fit', '')}",
            f"- Immediate ask: {capital.get('next_step', '')}",
        ]
    )
    return "\n".join(lines)


def _proof_of_execution(plan: dict[str, Any], facts: dict[str, VerifiedFact]) -> str:
    lines = [
        "# Proof of Execution",
        "",
        "This document separates verified operating proof from strategic interpretation.",
        "",
        "## Verified Company Facts",
        "",
    ]
    for fact_id in plan.get("evidence", {}).get("company_proof", []):
        lines.extend(_fact_detail_lines(facts[fact_id]))
    return "\n".join(lines)


def _market_and_timing(plan: dict[str, Any], facts: dict[str, VerifiedFact]) -> str:
    lines = [
        "# Market and Timing",
        "",
        "## Verified Market Signals",
        "",
    ]
    for fact_id in plan.get("evidence", {}).get("market_timing", []):
        lines.extend(_fact_detail_lines(facts[fact_id]))
    lines.extend(
        [
            "",
            "## Category Analogs",
            "",
        ]
    )
    for fact_id in plan.get("evidence", {}).get("category_lineage", []):
        lines.extend(_fact_detail_lines(facts[fact_id]))
    return "\n".join(lines)


def _diligence_snapshot(plan: dict[str, Any], facts: dict[str, VerifiedFact]) -> str:
    lines = [
        "# Diligence Snapshot",
        "",
        "## Investor Questions and Evidence Paths",
        "",
    ]
    for item in plan.get("objections", []):
        if not isinstance(item, dict):
            continue
        lines.extend(
            [
                f"## {item.get('question', '')}",
                str(item.get("answer", "")).strip(),
                "",
            ]
        )
        for fact_id in item.get("fact_ids", []):
            fact = facts[str(fact_id)]
            lines.append(f"- {fact.fact_id}: {fact.claim}")
        lines.append("")
    return "\n".join(lines)


def _audience_playbook(plan: dict[str, Any], facts: dict[str, VerifiedFact]) -> str:
    lines = [
        "# Audience Playbook",
        "",
        "The goal is not broad attention. The goal is repeated exposure among people who can validate, fund, or accelerate the company.",
        "",
    ]
    for audience in plan.get("audiences", []):
        if not isinstance(audience, dict):
            continue
        lines.extend(
            [
                f"## {audience.get('name', '')}",
                f"- Role in funnel: {audience.get('role_in_funnel', '')}",
                f"- Core thesis: {audience.get('thesis', '')}",
                f"- Conversion goal: {audience.get('conversion_goal', '')}",
                f"- Preferred channels: {', '.join(str(item) for item in audience.get('channels', []))}",
                f"- Call to action: {audience.get('cta', '')}",
                "- Supporting proof:",
            ]
        )
        for fact_id in audience.get("proof_fact_ids", []):
            fact = facts[str(fact_id)]
            lines.append(f"  - {fact.claim}")
        lines.append("")
    return "\n".join(lines)


def _distribution_playbook(plan: dict[str, Any]) -> str:
    lines = [
        "# Distribution Playbook",
        "",
        "## Weekly Cadence",
        "",
    ]
    for item in plan.get("weekly_sequence", []):
        if not isinstance(item, dict):
            continue
        lines.extend(
            [
                f"## {item.get('day', '')}",
                f"- Asset: {item.get('asset_type', '')}",
                f"- Audience: {item.get('audience', '')}",
                f"- Objective: {item.get('objective', '')}",
                f"- Theme: {item.get('theme', '')}",
                "",
            ]
        )
    return "\n".join(lines)


def _content_to_capital_map(plan: dict[str, Any], facts: dict[str, VerifiedFact]) -> str:
    lines = [
        "# Content to Capital Map",
        "",
        "Each content franchise should earn one of four outcomes: authority, validation, investor response, or diligence acceleration.",
        "",
    ]
    for item in plan.get("franchises", []):
        if not isinstance(item, dict):
            continue
        lines.extend(
            [
                f"## {item.get('name', '')}",
                f"- Investor problem solved: {item.get('investor_problem', '')}",
                f"- Recommended assets: {', '.join(str(value) for value in item.get('asset_types', []))}",
                f"- Conversion target: {item.get('conversion_target', '')}",
                "- Proof base:",
            ]
        )
        for fact_id in item.get("fact_ids", []):
            lines.append(f"  - {facts[str(fact_id)].claim}")
        lines.append("")
    return "\n".join(lines)


def _investor_outreach_sequences(plan: dict[str, Any]) -> str:
    company = plan.get("company", {})
    lines = [
        "# Investor Outreach Sequences",
        "",
        "## First Touch",
        "",
        dedent(
            f"""
            Subject: {company.get('name', 'NRG Bloom')} / remote compute infrastructure on stranded energy

            We are building {company.get('operating_model', '').rstrip('.')}.

            The reason we are reaching out now is simple: we already have operating proof in Nigeria, and the broader stranded-gas compute category now has stronger external validation across Nigeria, Alberta, the Bakken, and the Permian.

            If the intersection of energy infrastructure, remote operations, and frontier compute is relevant to your mandate, the next useful step would be a short diligence call around operating proof, market timing, and what capital would unlock.
            """
        ).strip(),
        "",
        "## Follow Up After Content Engagement",
        "",
        dedent(
            """
            Sharing the attached memo because it captures the exact thesis behind the post you engaged with:

            1. This is an operating story, not a concept story.
            2. The market timing is improving because gas-utilization and digital-infrastructure demand are both getting stronger.
            3. The diligence question is not whether the category exists. It is whether the operator can execute in-field.
            """
        ).strip(),
        "",
        "## Follow Up After First Call",
        "",
        "Send the one-page brief, proof-of-execution note, and the relevant diligence snapshot section tied to the investor's main objection.",
    ]
    return "\n".join(lines)


def _weekly_operating_system(plan: dict[str, Any]) -> str:
    lines = [
        "# Weekly Operating System",
        "",
        "## Monday",
        "- Publish one authority-led founder asset tied to a core investor objection.",
        "- Send 5 warm investor touches with that asset attached.",
        "",
        "## Tuesday",
        "- Publish one market-intelligence thread.",
        "- Reach out to 3 industry validators who can publicly reinforce the framing.",
        "",
        "## Wednesday",
        "- Publish one carousel or quote-card sequence tied to proof or category lineage.",
        "- Update the diligence stack with any new facts or milestones.",
        "",
        "## Thursday",
        "- Publish one short-form video or animated asset.",
        "- Follow up with investors who engaged earlier in the week.",
        "",
        "## Friday",
        "- Publish one contrarian or timing-oriented asset.",
        "- Review which assets created replies, calls, or diligence questions.",
        "- Move top-performing themes back into the backlog.",
    ]
    return "\n".join(lines)


def _site_source_notes(plan: dict[str, Any]) -> str:
    lines = [
        "# Public Site Source Notes",
        "",
        "This capital stack was grounded in public NRG Bloom site material that was reachable in this environment, plus verified external market sources in the fact registry.",
        "",
        "## Public NRG Bloom Pages Used",
        "",
    ]
    for item in plan.get("public_site_sources", []):
        if not isinstance(item, dict):
            continue
        lines.append(f"- {item.get('title', '')}: {item.get('url', '')}")
    lines.extend(
        [
            "",
            "## Important Note",
            "",
            "The `facts-and-numbers` route was referenced by the user as the deeper investor page, but it was not directly retrievable through the current web-crawler path. The investor stack here therefore uses the accessible public site pages and the local verified registries already in `work-codex`. The next upgrade should ingest that page or exported deck directly into the fact registry.",
        ]
    )
    return "\n".join(lines)


def _audience_map_payload(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_from": str(plan.get("title", "")),
        "audiences": [
            {
                "slug": str(item.get("slug", "")),
                "name": str(item.get("name", "")),
                "role_in_funnel": str(item.get("role_in_funnel", "")),
                "thesis": str(item.get("thesis", "")),
                "conversion_goal": str(item.get("conversion_goal", "")),
                "channels": [str(channel) for channel in item.get("channels", [])],
                "cta": str(item.get("cta", "")),
                "proof_fact_ids": [str(fact_id) for fact_id in item.get("proof_fact_ids", [])],
            }
            for item in plan.get("audiences", [])
            if isinstance(item, dict)
        ],
    }


def _content_backlog_payload(plan: dict[str, Any]) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for index, franchise in enumerate(plan.get("franchises", []), start=1):
        if not isinstance(franchise, dict):
            continue
        items.append(
            {
                "id": f"capital-{index:02d}",
                "theme": str(franchise.get("name", "")),
                "investor_problem": str(franchise.get("investor_problem", "")),
                "asset_types": [str(item) for item in franchise.get("asset_types", [])],
                "conversion_target": str(franchise.get("conversion_target", "")),
                "fact_ids": [str(item) for item in franchise.get("fact_ids", [])],
                "status": "ready",
            }
        )
    return {"items": items}


def _weekly_batch_markdown(plan: dict[str, Any], facts: dict[str, VerifiedFact]) -> str:
    lines = [
        f"# Weekly Capital Batch — {plan.get('title', '')}",
        "",
        "## This Week's Goal",
        "",
        str(plan.get("capital", {}).get("weekly_goal", "")).strip(),
        "",
    ]
    for item in plan.get("weekly_sequence", []):
        if not isinstance(item, dict):
            continue
        lines.extend(
            [
                f"## {item.get('day', '')}",
                f"- Asset: {item.get('asset_type', '')}",
                f"- Audience: {item.get('audience', '')}",
                f"- Objective: {item.get('objective', '')}",
                f"- Theme: {item.get('theme', '')}",
            ]
        )
        for franchise in plan.get("franchises", []):
            if isinstance(franchise, dict) and str(franchise.get("slug", "")) == str(item.get("franchise", "")):
                for fact_id in franchise.get("fact_ids", []):
                    lines.append(f"  - Proof: {facts[str(fact_id)].claim}")
        lines.append("")
    return "\n".join(lines)


def _weekly_content_queue_payload(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "week_of": datetime.now(UTC).date().isoformat(),
        "queue": [
            {
                "day": str(item.get("day", "")),
                "asset_type": str(item.get("asset_type", "")),
                "audience": str(item.get("audience", "")),
                "objective": str(item.get("objective", "")),
                "theme": str(item.get("theme", "")),
                "franchise": str(item.get("franchise", "")),
                "status": "planned",
            }
            for item in plan.get("weekly_sequence", [])
            if isinstance(item, dict)
        ],
    }


def _investor_touch_list(plan: dict[str, Any]) -> str:
    lines = [
        "# Investor Touch List",
        "",
        "Use this alongside the weekly batch so every content publish has a matching investor follow-up motion.",
        "",
    ]
    for audience in plan.get("audiences", []):
        if not isinstance(audience, dict):
            continue
        lines.extend(
            [
                f"## {audience.get('name', '')}",
                f"- Goal: {audience.get('conversion_goal', '')}",
                f"- Trigger asset: {audience.get('trigger_asset', 'founder post or market thread')}",
                f"- CTA: {audience.get('cta', '')}",
                "",
            ]
        )
    return "\n".join(lines)


def _fact_bullet_lines(facts: dict[str, VerifiedFact], fact_ids: list[Any], *, include_urls: bool) -> list[str]:
    lines: list[str] = []
    for raw_fact_id in fact_ids:
        fact = facts[str(raw_fact_id)]
        line = f"- {fact.claim}"
        if include_urls:
            urls = [source.url for source in fact.sources if source.url]
            if urls:
                line += f" ({urls[0]})"
        lines.append(line)
    return lines


def _fact_appendix_lines(facts: dict[str, VerifiedFact], fact_ids: list[Any]) -> list[str]:
    lines: list[str] = []
    seen: set[str] = set()
    for raw_fact_id in fact_ids:
        fact_id = str(raw_fact_id)
        if fact_id in seen:
            continue
        seen.add(fact_id)
        fact = facts[fact_id]
        lines.append(f"## {fact.fact_id}")
        lines.append(fact.claim)
        lines.append("")
        for source in fact.sources:
            source_line = f"- {source.source_type}: {source.path}"
            if source.url:
                source_line += f" ({source.url})"
            lines.append(source_line)
        lines.append("")
    return lines


def _fact_detail_lines(fact: VerifiedFact) -> list[str]:
    lines = [
        f"## {fact.fact_id}",
        fact.claim,
        "",
        f"Scope: {fact.scope}",
        "Sources:",
    ]
    for source in fact.sources:
        source_line = f"- [{source.source_type}] {source.path}"
        if source.title:
            source_line += f" — {source.title}"
        if source.url:
            source_line += f" ({source.url})"
        lines.append(source_line)
        lines.append(f"  Excerpt: {source.excerpt}")
    lines.append("")
    return lines


def _capital_dashboard_html(plan: dict[str, Any], manifest: dict[str, Any]) -> str:
    base_dir = Path(str(manifest.get("outputs", {}).get("investor_memo", "."))).resolve().parents[1]
    links = "\n".join(
        f'<a class="card" href="{html.escape(Path(path).resolve().relative_to(base_dir).as_posix())}"><div class="title">{html.escape(key.replace("_", " "))}</div><div class="meta">{html.escape(path)}</div></a>'
        for key, path in manifest.get("outputs", {}).items()
    )
    return dedent(
        f"""
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>{html.escape(str(plan.get('title', 'Capital Dashboard')))}</title>
          <style>
            * {{ box-sizing: border-box; }}
            body {{
              margin: 0;
              padding: 48px;
              font-family: Inter, Arial, sans-serif;
              background: #050814;
              color: #fff;
            }}
            h1 {{ margin: 0 0 12px; font-size: 42px; }}
            p {{ margin: 0 0 24px; color: rgba(255,255,255,0.68); font-size: 18px; }}
            .grid {{
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
              gap: 20px;
            }}
            .card {{
              display: block;
              background: #0f172a;
              border: 1px solid rgba(107,163,232,0.18);
              border-radius: 20px;
              padding: 24px;
              text-decoration: none;
              color: inherit;
            }}
            .title {{ font-size: 24px; font-weight: 800; text-transform: capitalize; }}
            .meta {{ margin-top: 12px; color: rgba(255,255,255,0.52); font-size: 14px; }}
          </style>
        </head>
        <body>
          <h1>{html.escape(str(plan.get("title", "Capital Dashboard")))}</h1>
          <p>Investor conversion documents generated from verified facts plus NRG Bloom strategic framing.</p>
          <div class="grid">{links}</div>
        </body>
        </html>
        """
    ).strip()
