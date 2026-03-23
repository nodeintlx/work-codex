from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
import json
import re
import unicodedata
from tempfile import NamedTemporaryFile
from typing import Any

import yaml


@dataclass(frozen=True)
class ContentBrief:
    queue_id: str
    brief_id: str
    title: str
    idea: str
    audience: str
    audience_label: str
    pillar: str
    pillar_label: str
    funnel_stage: str
    stage_label: str
    primary_channel: str
    cta: str
    lead_magnet: str
    suggested_publish_date: str
    hooks: list[str]
    repurpose_channels: list[str]
    brief_path: Path


_AUDIENCE_RULES = (
    ("diaspora", "diaspora_founders"),
    ("nigeria", "diaspora_founders"),
    ("africa", "diaspora_founders"),
    ("founder", "founders"),
    ("partnership", "energy_infrastructure_partners"),
    ("investor", "investors"),
    ("capital", "investors"),
    ("bitcoin", "bitcoin_mining_buyers"),
    ("mining", "bitcoin_mining_buyers"),
    ("power", "energy_infrastructure_partners"),
    ("gas", "energy_infrastructure_partners"),
)

_PILLAR_RULES = (
    ("logistics", "nigeria_market_reality"),
    ("customs", "nigeria_market_reality"),
    ("community", "nigeria_market_reality"),
    ("nigeria", "nigeria_market_reality"),
    ("agreement", "founder_lessons"),
    ("partner", "founder_lessons"),
    ("capital", "founder_lessons"),
    ("leverage", "founder_lessons"),
    ("operator", "builder_credibility"),
    ("execution", "builder_credibility"),
    ("site", "builder_credibility"),
    ("build", "builder_credibility"),
    ("story", "field_storytelling"),
    ("travel", "field_storytelling"),
    ("pressure", "field_storytelling"),
    ("next", "future_facing_authority"),
    ("future", "future_facing_authority"),
    ("structure", "future_facing_authority"),
    ("oando", "future_facing_authority"),
)

_STAGE_RULES = (
    ("checklist", "consideration"),
    ("framework", "consideration"),
    ("how to", "consideration"),
    ("template", "consideration"),
    ("case study", "decision"),
    ("work with", "decision"),
    ("call", "decision"),
    ("proposal", "decision"),
)

_PRIMARY_CHANNEL_BY_STAGE = {
    "awareness": "linkedin",
    "consideration": "linkedin",
    "decision": "email",
}

_REPURPOSE_CHANNELS = {
    "linkedin": ["x", "email"],
    "x": ["linkedin", "email"],
    "email": ["linkedin", "x"],
    "video": ["linkedin", "x"],
}

_MARKETING_REQUIRED_FILES = (
    "nrg-bloom/marketing/brand-system.yaml",
    "nrg-bloom/marketing/content-queue.yaml",
    "nrg-bloom/marketing/content-brief-schema-2026-03-10.md",
    "nrg-bloom/marketing/library/exemplars.yaml",
)

_BRIEF_STATUSES = {
    "drafting_ready",
    "approved_for_drafting",
    "in_review",
    "approved",
    "scheduled",
    "published",
    "paused",
}

_QUEUE_STATUSES = {
    "backlog",
    "planned",
    "in_review",
    "approved",
    "scheduled",
    "published",
    "paused",
}

_ALLOWED_STATUS_TRANSITIONS = {
    "drafting_ready": {"in_review", "paused"},
    "approved_for_drafting": {"in_review", "paused"},
    "in_review": {"drafting_ready", "approved", "paused"},
    "approved": {"scheduled", "paused"},
    "scheduled": {"published", "approved", "paused"},
    "published": set(),
    "paused": {"drafting_ready", "in_review", "approved"},
}


def create_content_brief(
    root: Path,
    *,
    title: str,
    idea: str,
    audience: str | None = None,
    channel: str | None = None,
    suggested_date: str | None = None,
    today: date | None = None,
) -> ContentBrief:
    today = today or date.today()
    strategy = _load_yaml(root / "nrg-bloom" / "marketing" / "brand-system.yaml")
    queue_path = root / "nrg-bloom" / "marketing" / "content-queue.yaml"
    queue_data = _load_yaml(queue_path)
    items = queue_data.setdefault("items", [])
    if not isinstance(items, list):
        raise ValueError("nrg-bloom/marketing/content-queue.yaml items must be a list")

    combined_text = f"{title}\n{idea}".lower()
    audience_key = audience or _pick_first_match(combined_text, _AUDIENCE_RULES, default="founders")
    pillar_key = _pick_first_match(combined_text, _PILLAR_RULES, default="builder_credibility")
    stage_key = _pick_first_match(combined_text, _STAGE_RULES, default="awareness")
    primary_channel = (channel or _PRIMARY_CHANNEL_BY_STAGE[stage_key]).lower()
    publish_date = suggested_date or _next_publish_date(queue_data, today).isoformat()

    audiences = strategy.get("audiences", {})
    pillars = strategy.get("content_pillars", {})
    funnel = strategy.get("funnel", {})
    audience_meta = audiences.get(audience_key, {})
    pillar_meta = pillars.get(pillar_key, {})
    stage_meta = funnel.get(stage_key, {})

    queue_id = _next_queue_id(items)
    brief_id = _next_brief_id(root)
    slug = _slugify(title)
    brief_path = root / "nrg-bloom" / "marketing" / "briefs" / f"{brief_id.lower()}-{slug}.yaml"
    note_path = root / "nrg-bloom" / "marketing" / "ideas" / f"{publish_date}-{slug}.md"
    hooks = _hooks_for(title=title, idea=idea, pillar_label=str(pillar_meta.get("label", pillar_key)))
    cta = str(stage_meta.get("default_cta", "Follow NRG Bloom for practical infrastructure lessons."))
    lead_magnet = str(stage_meta.get("lead_magnet", "Field note"))
    repurpose_channels = _REPURPOSE_CHANNELS.get(primary_channel, ["linkedin", "x"])
    proof_points = _proof_points_for(idea=idea, audience_label=str(audience_meta.get("label", audience_key)))
    supporting_points = _supporting_points_for(idea=idea, pillar_label=str(pillar_meta.get("label", pillar_key)))
    objections = _objections_for(stage_key)
    contrarian_angle = _contrarian_angle_for(stage_key, pillar_label=str(pillar_meta.get("label", pillar_key)))
    emotional_driver = _emotional_driver_for(pillar_key)
    business_goal = _business_goal_for(stage_key)
    campaign_theme = _campaign_theme_for(pillar_key)
    punch_idea = _punch_idea_for(idea)
    thesis = _main_thesis_for(idea, pillar_label=str(pillar_meta.get("label", pillar_key)))

    brief = ContentBrief(
        queue_id=queue_id,
        brief_id=brief_id,
        title=title,
        idea=idea,
        audience=audience_key,
        audience_label=str(audience_meta.get("label", audience_key)),
        pillar=pillar_key,
        pillar_label=str(pillar_meta.get("label", pillar_key)),
        funnel_stage=stage_key,
        stage_label=str(stage_meta.get("label", stage_key)),
        primary_channel=primary_channel,
        cta=cta,
        lead_magnet=lead_magnet,
        suggested_publish_date=publish_date,
        hooks=hooks,
        repurpose_channels=repurpose_channels,
        brief_path=brief_path,
    )

    items.append(
        {
            "id": queue_id,
            "brief_id": brief_id,
            "status": "backlog",
            "title": title,
            "pillar": pillar_key,
            "audience": audience_key,
            "funnel_stage": stage_key,
            "primary_channel": primary_channel,
            "repurpose_channels": repurpose_channels,
            "cta": cta,
            "lead_magnet": lead_magnet,
            "suggested_publish_date": publish_date,
            "brief_path": str(brief_path.relative_to(root)),
            "note_path": str(note_path.relative_to(root)),
            "source": "content-intake",
        }
    )
    queue_data["last_updated"] = today.isoformat()

    canonical_brief = {
        "id": brief_id,
        "created_at": today.isoformat(),
        "updated_at": today.isoformat(),
        "status": "drafting_ready",
        "owner": "makir",
        "source_type": "content_intake",
        "source_ref": queue_id,
        "title": title,
        "raw_idea": idea,
        "source_notes": [f"Generated from {queue_id} via content-intake."],
        "original_language": "en",
        "audience": {
            "primary": audience_key,
            "secondary": repurpose_channels[:1],
        },
        "persona_problem": _persona_problem_for(audience_meta),
        "content_pillar": pillar_key,
        "funnel_stage": stage_key,
        "campaign_theme": campaign_theme,
        "business_goal": business_goal,
        "primary_cta": cta,
        "lead_magnet": lead_magnet,
        "voice_profile": _voice_profile_for_strategy(strategy, pillar_key=pillar_key, stage_key=stage_key),
        "main_thesis": thesis,
        "punch_idea": punch_idea,
        "contrarian_angle": contrarian_angle,
        "emotional_driver": emotional_driver,
        "proof_points": proof_points,
        "hooks": hooks,
        "supporting_points": supporting_points,
        "objections_to_answer": objections,
        "closing_angle": punch_idea,
        "primary_format": _primary_format_for(primary_channel),
        "primary_channel": primary_channel,
        "repurpose_formats": _repurpose_formats_for(repurpose_channels),
        "series_role": "pillar_builder",
        "publish_window": publish_date,
        "creative_direction": {
            "visual_theme": _visual_theme_for(pillar_key),
            "thumbnail_concepts": _thumbnail_concepts_for(punch_idea),
            "image_prompt_directions": _image_prompt_directions_for(pillar_key),
            "onscreen_text": [punch_idea],
            "carousel_frames": _carousel_frames_for(thesis, supporting_points),
            "video_shot_ideas": _video_shot_ideas_for(pillar_key),
        },
        "guardrails": {
            "brand_voice_rules": strategy.get("brand", {}).get("voice", []),
            "legal_risk_level": "safe_public_generic",
            "legal_notes": [
                "Keep this Phase 1-safe while TON proceedings remain active.",
                "Do not include identifiable counterparty, site, contract, or evidence details.",
            ],
            "claims_to_avoid": [
                "Do not imply facts specific to the live dispute.",
            ],
            "required_review": "standard_editorial",
        },
        "drafts": {
            "linkedin": "",
            "x_thread": "",
            "email": "",
            "article_outline": "",
            "video_script": "",
            "faq": "",
        },
        "performance": {
            "published_assets": [],
            "performance_snapshot": {},
            "lessons_learned": [],
            "next_derivatives": [],
        },
    }

    _write_yaml(brief_path, canonical_brief)
    _write_text(note_path, _render_brief(brief, audience_meta, pillar_meta, stage_meta))
    _write_yaml(queue_path, queue_data)
    _append_audit(
        root,
        action="content_intake",
        path=queue_path,
        details={"id": queue_id, "brief_id": brief_id, "title": title, "brief_path": str(brief_path.relative_to(root))},
    )
    return brief


def calendar_lines(root: Path) -> list[str]:
    queue_path = root / "nrg-bloom" / "marketing" / "content-queue.yaml"
    queue_data = _load_yaml(queue_path)
    raw_items = queue_data.get("items", [])
    rendered: list[tuple[date | None, str]] = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        scheduled = _parse_optional_date(item.get("scheduled_for") or item.get("suggested_publish_date"))
        when = scheduled.isoformat() if scheduled else "unscheduled"
        rendered.append(
            (
                scheduled,
                f"  {when} [{item.get('status', '')}] {item.get('id', '')} {item.get('title', '')} "
                f"({item.get('primary_channel', '')}, {item.get('funnel_stage', '')}, {item.get('audience', '')})",
            )
        )
    rendered.sort(key=lambda item: (item[0] or date.max, item[1]))
    if not rendered:
        return ["NRG Bloom content calendar", "  none"]
    return ["NRG Bloom content calendar"] + [line for _, line in rendered]


def validate_content_system(root: Path) -> list[str]:
    errors: list[str] = []
    for relative_path in _MARKETING_REQUIRED_FILES:
        if not (root / relative_path).exists():
            errors.append(f"missing required marketing file: {relative_path}")

    queue_path = root / "nrg-bloom" / "marketing" / "content-queue.yaml"
    if queue_path.exists():
        queue = _load_yaml(queue_path)
        items = queue.get("items", [])
        if not isinstance(items, list):
            errors.append("nrg-bloom/marketing/content-queue.yaml items must be a list")
        else:
            for index, item in enumerate(items, start=1):
                if not isinstance(item, dict):
                    errors.append(f"queue item {index} is not a mapping")
                    continue
                for field_name in ("id", "title", "pillar", "audience", "funnel_stage", "primary_channel"):
                    if not item.get(field_name):
                        errors.append(f"queue item {index} missing {field_name}")
    return errors


def load_content_brief(path: Path) -> dict[str, Any]:
    return _load_yaml(path)


def validate_content_brief(brief: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not brief.get("id"):
        errors.append("missing id")
    if not brief.get("status"):
        errors.append("missing status")
    elif str(brief.get("status")) not in _BRIEF_STATUSES:
        errors.append(f"invalid status: {brief.get('status')}")
    if not brief.get("title"):
        errors.append("missing title")
    if not brief.get("raw_idea"):
        errors.append("missing raw_idea")
    audience = brief.get("audience", {})
    if not isinstance(audience, dict) or not audience.get("primary"):
        errors.append("missing audience.primary")
    if not brief.get("content_pillar"):
        errors.append("missing content_pillar")
    if not brief.get("funnel_stage"):
        errors.append("missing funnel_stage")
    if not brief.get("main_thesis"):
        errors.append("missing main_thesis")
    if not brief.get("punch_idea"):
        errors.append("missing punch_idea")
    hooks = brief.get("hooks", [])
    if not isinstance(hooks, list) or len(hooks) < 3:
        errors.append("hooks must contain at least 3 items")
    if not brief.get("primary_format"):
        errors.append("missing primary_format")
    if not brief.get("primary_channel"):
        errors.append("missing primary_channel")
    if not brief.get("primary_cta"):
        errors.append("missing primary_cta")
    guardrails = brief.get("guardrails", {})
    if not isinstance(guardrails, dict) or not guardrails.get("legal_risk_level"):
        errors.append("missing guardrails.legal_risk_level")
    return errors


def update_content_status(
    root: Path,
    *,
    brief_path: Path,
    status: str,
    scheduled_for: str | None = None,
    published_at: str | None = None,
) -> tuple[Path, str]:
    if status not in _BRIEF_STATUSES:
        raise ValueError(f"invalid content status: {status}")
    brief = load_content_brief(brief_path)
    current_status = str(brief.get("status", ""))
    allowed = _ALLOWED_STATUS_TRANSITIONS.get(current_status, set())
    if current_status and status != current_status and status not in allowed:
        raise ValueError(f"invalid status transition: {current_status} -> {status}")
    brief["status"] = status
    brief["updated_at"] = date.today().isoformat()
    if scheduled_for is not None:
        _parse_optional_date(scheduled_for)
        brief["publish_window"] = scheduled_for
    if published_at is not None:
        _parse_optional_date(published_at)
        performance = dict(brief.get("performance", {}))
        published_assets = list(performance.get("published_assets", []))
        published_assets.append(
            {
                "date": published_at,
                "channel": brief.get("primary_channel", ""),
                "format": brief.get("primary_format", ""),
            }
        )
        performance["published_assets"] = published_assets
        brief["performance"] = performance
    _write_yaml(brief_path, brief)

    queue_path = root / "nrg-bloom" / "marketing" / "content-queue.yaml"
    queue = _load_yaml(queue_path)
    for item in queue.get("items", []):
        if not isinstance(item, dict):
            continue
        if str(item.get("brief_path", "")) == str(brief_path.relative_to(root)):
            item["status"] = _queue_status_for_brief(status)
            if scheduled_for is not None:
                item["scheduled_for"] = scheduled_for
                item.pop("suggested_publish_date", None)
            if published_at is not None:
                item["published_at"] = published_at
            break
    queue["last_updated"] = date.today().isoformat()
    _write_yaml(queue_path, queue)
    _append_audit(
        root,
        action="content_status_update",
        path=brief_path,
        details={"brief_id": brief.get("id"), "status": status},
    )
    return brief_path, status


def content_backend_payload(root: Path, today: date | None = None) -> dict[str, Any]:
    today = today or date.today()
    queue = _load_yaml(root / "nrg-bloom" / "marketing" / "content-queue.yaml")
    items = [item for item in queue.get("items", []) if isinstance(item, dict)]
    briefs = []
    for item in items:
        brief_path_value = item.get("brief_path")
        brief_data = None
        if isinstance(brief_path_value, str):
            brief_path = root / brief_path_value
            if brief_path.exists() and brief_path.suffix == ".yaml":
                brief_data = load_content_brief(brief_path)
        brief_status = brief_data.get("status", "") if isinstance(brief_data, dict) else ""
        effective_status = _effective_queue_status(item.get("status", ""), brief_status)
        briefs.append(
            {
                "queue_id": item.get("id", ""),
                "brief_id": item.get("brief_id", ""),
                "title": item.get("title", ""),
                "status": effective_status,
                "queue_status": item.get("status", ""),
                "scheduled_for": item.get("scheduled_for") or item.get("suggested_publish_date"),
                "primary_channel": item.get("primary_channel", ""),
                "funnel_stage": item.get("funnel_stage", ""),
                "audience": item.get("audience", ""),
                "pillar": item.get("pillar", ""),
                "brief_path": item.get("brief_path", ""),
                "note_path": item.get("note_path", ""),
                "brief_status": brief_status,
                "has_drafts": bool(brief_data and any(str(value).strip() for value in brief_data.get("drafts", {}).values())),
                "has_creative": bool(brief_data and brief_data.get("creative_direction")),
            }
        )

    editorial = editorial_lines(root, today)
    payload = {
        "agent_name": "BloomFlow",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "workspace": str(root),
        "summary": {
            "total_items": len(briefs),
            "backlog_items": sum(1 for item in briefs if item["status"] == "backlog"),
            "scheduled_items": sum(1 for item in briefs if item["status"] in {"planned", "scheduled"}),
            "published_items": sum(1 for item in briefs if item["status"] == "published"),
        },
        "items": briefs,
        "editorial_lines": editorial,
    }
    return payload


def write_content_backend_payload(root: Path, today: date | None = None) -> Path:
    payload = content_backend_payload(root, today)
    path = root / "nrg-bloom" / "marketing" / "generated" / "backend-summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
        temp_path = Path(handle.name)
    temp_path.replace(path)
    return path


def content_app_payload(root: Path, today: date | None = None) -> dict[str, Any]:
    today = today or date.today()
    backend = content_backend_payload(root, today)
    items = backend["items"]
    dashboard_cards = []
    for item in items:
        dashboard_cards.append(
            {
                "id": item["queue_id"],
                "title": item["title"],
                "status": item["status"],
                "brief_status": item["brief_status"],
                "scheduled_for": item["scheduled_for"],
                "primary_channel": item["primary_channel"],
                "funnel_stage": item["funnel_stage"],
                "audience": item["audience"],
                "pillar": item["pillar"],
                "has_drafts": item["has_drafts"],
                "has_creative": item["has_creative"],
            }
        )

    brief_detail = {}
    for item in items:
        if not item["brief_path"] or not item["brief_path"].endswith(".yaml"):
            continue
        brief_path = root / item["brief_path"]
        if not brief_path.exists():
            continue
        brief = load_content_brief(brief_path)
        brief_detail[item["brief_id"] or item["queue_id"]] = {
            "id": brief.get("id", ""),
            "queue_id": item["queue_id"],
            "title": brief.get("title", ""),
            "status": item["status"],
            "queue_status": item["queue_status"],
            "brief_status": item["brief_status"],
            "audience": brief.get("audience", {}),
            "strategy": {
                "pillar": brief.get("content_pillar", ""),
                "funnel_stage": brief.get("funnel_stage", ""),
                "campaign_theme": brief.get("campaign_theme", ""),
                "business_goal": brief.get("business_goal", ""),
                "primary_cta": brief.get("primary_cta", ""),
            },
            "thesis": {
                "main_thesis": brief.get("main_thesis", ""),
                "punch_idea": brief.get("punch_idea", ""),
                "contrarian_angle": brief.get("contrarian_angle", ""),
                "emotional_driver": brief.get("emotional_driver", ""),
            },
            "assets": {
                "drafts": {key: bool(str(value).strip()) for key, value in brief.get("drafts", {}).items()},
                "creative": {
                    "visual_theme": brief.get("creative_direction", {}).get("visual_theme", ""),
                    "thumbnail_count": len(brief.get("creative_direction", {}).get("thumbnail_concepts", [])),
                    "carousel_frame_count": len(brief.get("creative_direction", {}).get("carousel_frames", [])),
                },
            },
            "paths": {
                "brief_path": item["brief_path"],
                "note_path": item["note_path"],
            },
        }

    actions = {
        "content_intake": {
            "command": "PYTHONPATH=src python3 -m work_codex.cli content-intake --workspace . --title '<title>' --idea '<idea>'",
            "label": "Capture Idea",
        },
        "content_validate": {
            "command": "PYTHONPATH=src python3 -m work_codex.cli content-validate --workspace . --brief '<brief_path>'",
            "label": "Validate Brief",
        },
        "content_draft": {
            "command": "PYTHONPATH=src python3 -m work_codex.cli content-draft --workspace . --brief '<brief_path>'",
            "label": "Generate Drafts",
        },
        "content_creative": {
            "command": "PYTHONPATH=src python3 -m work_codex.cli content-creative --workspace . --brief '<brief_path>'",
            "label": "Generate Creative",
        },
        "content_status": {
            "command": "PYTHONPATH=src python3 -m work_codex.cli content-status --workspace . --brief '<brief_path>' --set-status <status>",
            "label": "Update Status",
        },
        "content_editorial": {
            "command": "PYTHONPATH=src python3 -m work_codex.cli content-editorial --workspace .",
            "label": "Review Editorial Board",
        },
    }

    return {
        "agent": {
            "name": "BloomFlow",
            "workspace": str(root),
            "generated_at": backend["generated_at"],
        },
        "views": {
            "dashboard": {
                "summary": backend["summary"],
                "cards": dashboard_cards,
                "editorial_lines": backend["editorial_lines"],
            },
            "brief_detail": brief_detail,
        },
        "actions": actions,
    }


def write_content_app_payload(root: Path, today: date | None = None) -> Path:
    payload = content_app_payload(root, today)
    path = root / "nrg-bloom" / "marketing" / "generated" / "app-contract.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
        temp_path = Path(handle.name)
    temp_path.replace(path)
    return path


def generate_content_package(root: Path, brief_path: Path) -> Path:
    system_errors = validate_content_system(root)
    if system_errors:
        raise ValueError("; ".join(system_errors))

    brief = load_content_brief(brief_path)
    brief_errors = validate_content_brief(brief)
    if brief_errors:
        raise ValueError("; ".join(brief_errors))

    package_path = root / "nrg-bloom" / "marketing" / "generated" / f"{brief['id'].lower()}-drafts.md"
    drafts = _draft_outputs(root, brief)
    _write_text(package_path, _render_content_package(brief, drafts))

    stored_brief = dict(brief)
    stored_drafts = dict(stored_brief.get("drafts", {}))
    stored_drafts.update(drafts)
    stored_brief["drafts"] = stored_drafts
    stored_brief["updated_at"] = date.today().isoformat()
    _write_yaml(brief_path, stored_brief)
    _append_audit(
        root,
        action="content_draft_generate",
        path=package_path,
        details={"brief_id": brief["id"], "brief_path": str(brief_path.relative_to(root))},
    )
    return package_path


def generate_creative_package(root: Path, brief_path: Path) -> Path:
    system_errors = validate_content_system(root)
    if system_errors:
        raise ValueError("; ".join(system_errors))

    brief = load_content_brief(brief_path)
    brief_errors = validate_content_brief(brief)
    if brief_errors:
        raise ValueError("; ".join(brief_errors))

    package_path = root / "nrg-bloom" / "marketing" / "generated" / f"{brief['id'].lower()}-creative.md"
    _write_text(package_path, _render_creative_package(brief))
    _append_audit(
        root,
        action="content_creative_generate",
        path=package_path,
        details={"brief_id": brief["id"], "brief_path": str(brief_path.relative_to(root))},
    )
    return package_path


def ingest_published_post(
    root: Path,
    *,
    brief_path: Path,
    channel: str,
    body: str,
    posted_at: str,
    url: str | None = None,
) -> Path:
    brief = load_content_brief(brief_path)
    _parse_optional_date(posted_at)
    performance = dict(brief.get("performance", {}))
    published_posts = list(performance.get("published_posts", []))
    published_posts.append(
        {
            "channel": channel,
            "body": body.strip(),
            "posted_at": posted_at,
            "url": (url or "").strip(),
        }
    )
    performance["published_posts"] = published_posts
    brief["performance"] = performance
    brief["updated_at"] = date.today().isoformat()
    _write_yaml(brief_path, brief)
    _append_audit(
        root,
        action="content_post_ingest",
        path=brief_path,
        details={"brief_id": brief.get("id"), "channel": channel, "posted_at": posted_at},
    )
    return brief_path


def log_post_performance(
    root: Path,
    *,
    brief_path: Path,
    channel: str,
    captured_at: str,
    impressions: int | None = None,
    likes: int | None = None,
    comments: int | None = None,
    reposts: int | None = None,
    saves: int | None = None,
    profile_visits: int | None = None,
    dms: int | None = None,
    leads: int | None = None,
) -> Path:
    brief = load_content_brief(brief_path)
    _parse_optional_date(captured_at)
    performance = dict(brief.get("performance", {}))
    snapshots = list(performance.get("performance_snapshots", []))
    snapshot = {
        "channel": channel,
        "captured_at": captured_at,
        "impressions": impressions or 0,
        "likes": likes or 0,
        "comments": comments or 0,
        "reposts": reposts or 0,
        "saves": saves or 0,
        "profile_visits": profile_visits or 0,
        "dms": dms or 0,
        "leads": leads or 0,
    }
    snapshot["engagement_total"] = snapshot["likes"] + snapshot["comments"] + snapshot["reposts"] + snapshot["saves"]
    snapshots.append(snapshot)
    performance["performance_snapshots"] = snapshots
    performance["performance_snapshot"] = snapshot
    brief["performance"] = performance
    brief["updated_at"] = date.today().isoformat()
    _write_yaml(brief_path, brief)
    _append_audit(
        root,
        action="content_performance_log",
        path=brief_path,
        details={"brief_id": brief.get("id"), "channel": channel, "captured_at": captured_at},
    )
    return brief_path


def content_review_lines(root: Path, brief_path: Path) -> list[str]:
    brief = load_content_brief(brief_path)
    drafts = brief.get("drafts", {})
    performance = brief.get("performance", {})
    published_posts = performance.get("published_posts", [])
    snapshots = performance.get("performance_snapshots", [])
    lines = [f"BloomFlow review: {brief.get('id', '')}", f"title: {brief.get('title', '')}"]
    lines.append(f"status: {brief.get('status', '')}")
    if not published_posts:
        lines.append("published posts: none")
    else:
        latest_post = published_posts[-1]
        draft_key = _draft_key_for_channel(str(latest_post.get("channel", "")))
        draft_text = str(drafts.get(draft_key, "")).strip()
        final_text = str(latest_post.get("body", "")).strip()
        lines.append(f"latest channel: {latest_post.get('channel', '')}")
        lines.append(f"posted at: {latest_post.get('posted_at', '')}")
        lines.append("draft vs final")
        lines.append(f"  draft length: {len(draft_text)}")
        lines.append(f"  final length: {len(final_text)}")
        lines.append(f"  changed: {'yes' if _clean_sentence(draft_text) != _clean_sentence(final_text) else 'no'}")
        if final_text:
            lines.append(f"  final opening: {_first_line(final_text)}")
    if not snapshots:
        lines.append("performance: none")
    else:
        latest_snapshot = snapshots[-1]
        lines.append("latest performance")
        lines.append(f"  impressions: {latest_snapshot.get('impressions', 0)}")
        lines.append(f"  engagement_total: {latest_snapshot.get('engagement_total', 0)}")
        lines.append(f"  dms: {latest_snapshot.get('dms', 0)}")
        lines.append(f"  leads: {latest_snapshot.get('leads', 0)}")
    return lines


def content_validation_lines(root: Path, brief_path: Path | None = None) -> list[str]:
    lines = ["NRG Bloom content health"]
    system_errors = validate_content_system(root)
    if system_errors:
        lines.append("system: failed")
        for error in system_errors:
            lines.append(f"- {error}")
    else:
        lines.append("system: ok")
    if brief_path is not None:
        brief = load_content_brief(brief_path)
        brief_errors = validate_content_brief(brief)
        if brief_errors:
            lines.append(f"brief {brief_path.name}: failed")
            for error in brief_errors:
                lines.append(f"- {error}")
        else:
            lines.append(f"brief {brief_path.name}: ok")
    return lines


def editorial_lines(root: Path, today: date | None = None) -> list[str]:
    today = today or date.today()
    queue = _load_yaml(root / "nrg-bloom" / "marketing" / "content-queue.yaml")
    items = [item for item in queue.get("items", []) if isinstance(item, dict)]
    scheduled = []
    backlog = []
    stage_counts: dict[str, int] = {}
    pillar_counts: dict[str, int] = {}
    audience_counts: dict[str, int] = {}

    for item in items:
        stage = str(item.get("funnel_stage", ""))
        pillar = str(item.get("pillar", ""))
        audience = str(item.get("audience", ""))
        stage_counts[stage] = stage_counts.get(stage, 0) + 1
        pillar_counts[pillar] = pillar_counts.get(pillar, 0) + 1
        audience_counts[audience] = audience_counts.get(audience, 0) + 1
        scheduled_for = _parse_optional_date(item.get("scheduled_for") or item.get("suggested_publish_date"))
        if scheduled_for is not None:
            scheduled.append((scheduled_for, item))
        else:
            backlog.append(item)

    scheduled.sort(key=lambda pair: pair[0])
    lines = ["BloomFlow editorial board"]

    lines.append("next posts")
    upcoming = [pair for pair in scheduled if pair[0] >= today][:3]
    if not upcoming:
        lines.append("  none")
    else:
        for scheduled_for, item in upcoming:
            lines.append(
                f"  {scheduled_for.isoformat()} {item.get('id', '')} {item.get('title', '')} "
                f"({item.get('primary_channel', '')}, {item.get('funnel_stage', '')})"
            )

    lines.append("ready backlog")
    ready_backlog = [item for item in items if item.get("status") == "backlog" and item.get("brief_id")]
    if not ready_backlog:
        lines.append("  none")
    else:
        for item in ready_backlog[:5]:
            lines.append(
                f"  {item.get('id', '')} {item.get('title', '')} "
                f"({item.get('audience', '')}, {item.get('pillar', '')}, brief {item.get('brief_id', '')})"
            )

    lines.append("funnel coverage")
    for stage in ("awareness", "consideration", "decision"):
        lines.append(f"  {stage}: {stage_counts.get(stage, 0)}")

    gaps: list[str] = []
    if stage_counts.get("consideration", 0) < 2:
        gaps.append("Need more consideration-stage content.")
    if stage_counts.get("decision", 0) < 1:
        gaps.append("Need at least one decision-stage asset.")
    if pillar_counts.get("founder_lessons", 0) < 2:
        gaps.append("Need more founder_lessons coverage.")
    if audience_counts.get("investors", 0) < 2:
        gaps.append("Need more investor-facing content.")

    lines.append("editorial gaps")
    if not gaps:
        lines.append("  none")
    else:
        for gap in gaps:
            lines.append(f"  {gap}")

    recommendation = _editorial_recommendation(items, today)
    if recommendation is not None:
        lines.append("recommended next brief")
        lines.append(
            f"  {recommendation.get('id', '')} {recommendation.get('title', '')} "
            f"({recommendation.get('primary_channel', '')}, {recommendation.get('funnel_stage', '')})"
        )
    return lines


def _render_brief(
    brief: ContentBrief,
    audience_meta: dict[str, Any],
    pillar_meta: dict[str, Any],
    stage_meta: dict[str, Any],
) -> str:
    pain_points = audience_meta.get("pain_points", [])
    outcomes = pillar_meta.get("outcomes", [])
    assets = stage_meta.get("recommended_assets", [])
    pain_line = "\n".join(f"- {item}" for item in pain_points) or "- Clarify the commercial problem"
    outcomes_line = "\n".join(f"- {item}" for item in outcomes) or "- Build authority"
    assets_line = "\n".join(f"- {item}" for item in assets) or "- LinkedIn post"
    hooks_line = "\n".join(f"- {item}" for item in brief.hooks)
    repurpose_line = "\n".join(f"- {item}" for item in brief.repurpose_channels)
    return (
        f"# {brief.title}\n\n"
        f"- Queue ID: {brief.queue_id}\n"
        f"- Suggested publish date: {brief.suggested_publish_date}\n"
        f"- Audience: {brief.audience_label}\n"
        f"- Pillar: {brief.pillar_label}\n"
        f"- Funnel stage: {brief.stage_label}\n"
        f"- Primary channel: {brief.primary_channel}\n"
        f"- CTA: {brief.cta}\n"
        f"- Lead magnet: {brief.lead_magnet}\n\n"
        f"## Raw Idea\n{brief.idea}\n\n"
        f"## Audience Pain Points\n{pain_line}\n\n"
        f"## Strategic Outcome\n{outcomes_line}\n\n"
        f"## Hooks\n{hooks_line}\n\n"
        f"## Recommended Assets\n{assets_line}\n\n"
        f"## Repurpose Next\n{repurpose_line}\n\n"
        f"## Guardrails\n"
        f"- Keep this Phase 1-safe while TON proceedings remain active.\n"
        f"- Do not include identifiable counterparty, site, contract, or evidence details.\n"
        f"- Escalate for lawyer review if the story becomes specific enough to identify the dispute.\n"
    )


def _draft_outputs(root: Path, brief: dict[str, Any]) -> dict[str, str]:
    title = str(brief.get("title", ""))
    raw_idea = str(brief.get("raw_idea", ""))
    thesis = str(brief.get("main_thesis", ""))
    punch = str(brief.get("punch_idea", ""))
    cta = str(brief.get("primary_cta", ""))
    hooks = [str(item) for item in brief.get("hooks", [])]
    points = [str(item) for item in brief.get("supporting_points", [])]
    objections = [str(item) for item in brief.get("objections_to_answer", [])]
    closing = str(brief.get("closing_angle", ""))
    visual = str(brief.get("creative_direction", {}).get("visual_theme", ""))
    pillar_text = str(brief.get("content_pillar", "")).replace("_", " ")
    voice = _voice_profile_from_brief(brief)
    signature_patterns = [str(item) for item in voice.get("signature_patterns", []) if str(item).strip()]
    exemplar = _pick_exemplar(
        root,
        pillar_key=str(brief.get("content_pillar", "")),
        stage_key=str(brief.get("funnel_stage", "")),
        format_key=str(brief.get("primary_channel", "")),
    )
    observation, angle = _split_raw_idea(raw_idea or thesis)
    hook = _fresh_hook_for(title, observation, signature_patterns=signature_patterns, exemplar=exemplar)
    second_hook = _fresh_second_hook_for(pillar_text or "execution", signature_patterns=signature_patterns, exemplar=exemplar)
    punch_line = angle or _resolved_punch_idea(raw_idea or thesis, punch)
    points = _unique_lines(
        [],
        fallback=[
            angle or points[0] if points else observation,
            _pillar_takeaway_for(pillar_text),
            _practical_move_line_for(stage_key=str(brief.get("funnel_stage", ""))),
        ],
    )
    close_line = closing if closing and "..." not in closing else punch_line

    linkedin = "\n".join(
        [
            hook,
            "",
            _bridge_line_for(exemplar, default="Most commentary stops at the headline. The better question is what this changes for operators on the ground."),
            "",
            observation,
            "",
            "What this changes in practice:",
            *(f"- {point}" for point in points[:3]),
            "",
            f"The real takeaway: {punch_line}",
            "",
            _close_line_for(exemplar, default=cta, cta=cta),
        ]
    ).strip()

    x_thread_lines = [
        f"1. {hook}",
        f"2. {observation}",
        f"3. {angle or thesis}",
    ]
    x_thread_lines.extend(f"{index}. {point}" for index, point in enumerate(_thread_points(points, punch_line), start=4))
    x_thread_lines.append(f"{len(x_thread_lines) + 1}. The real takeaway: {punch_line}")
    x_thread_lines.append(f"{len(x_thread_lines) + 1}. {cta}")
    x_thread = "\n".join(x_thread_lines)

    email_subject = _email_subject_for(title, punch_line)
    email = "\n".join(
        [
            f"Subject: {email_subject}",
            "",
            second_hook,
            "",
            observation,
            "",
            "Why this matters:",
            *(f"- {point}" for point in points[:3]),
            "",
            f"Bottom line: {punch_line}",
            cta,
        ]
    ).strip()

    article_outline = "\n".join(
        [
            f"# {title}",
            "",
            "## Opening Tension",
            hook,
            "",
            "## What Changed",
            observation,
            "",
            "## Why Builders Should Care",
            *(f"- {point}" for point in points[:3]),
            "",
            "## Questions To Answer",
            *(f"- {item}" for item in objections[:3]),
            "",
            "## Closing Angle",
            _close_line_for(exemplar, default=close_line, cta=cta),
        ]
    ).strip()

    video_script = "\n".join(
        [
            "Hook:",
            hook,
            "",
            "Bridge:",
            "This is not just a headline story. It changes how serious builders should read the market.",
            "",
            "Main point:",
            observation,
            "",
            "Beat 1:",
            points[0],
            "",
            "Beat 2:",
            points[1] if len(points) > 1 else angle or thesis,
            "",
            "Close:",
            f"{punch_line}",
            cta,
            "",
            f"Visual note: {visual}" if visual else "Visual note: keep the visuals practical and builder-first.",
        ]
    ).strip()

    faq = "\n".join(
        [
            f"Q: What is actually changing behind '{title}'?",
            f"A: {observation}",
            "",
            "Q: Why should builders care?",
            f"A: {angle or punch_line}",
            "",
            "Q: What is the practical takeaway?",
            f"A: {punch_line}",
        ]
    ).strip()

    return {
        "linkedin": linkedin,
        "x_thread": x_thread,
        "email": email,
        "article_outline": article_outline,
        "video_script": video_script,
        "faq": faq,
    }


def _render_content_package(brief: dict[str, Any], drafts: dict[str, str]) -> str:
    sections = [
        f"# Content Draft Package: {brief['id']}",
        "",
        f"Title: {brief.get('title', '')}",
        f"Primary channel: {brief.get('primary_channel', '')}",
        f"Primary format: {brief.get('primary_format', '')}",
        f"Audience: {brief.get('audience', {}).get('primary', '')}",
        f"Risk level: {brief.get('guardrails', {}).get('legal_risk_level', '')}",
        "",
    ]
    for name in ("linkedin", "x_thread", "email", "article_outline", "video_script", "faq"):
        label = name.replace("_", " ").title()
        sections.extend([f"## {label}", drafts[name], ""])
    return "\n".join(sections).strip() + "\n"


def _render_creative_package(brief: dict[str, Any]) -> str:
    creative = brief.get("creative_direction", {})
    thumbnail_concepts = creative.get("thumbnail_concepts", [])
    image_prompt_directions = creative.get("image_prompt_directions", [])
    onscreen_text = creative.get("onscreen_text", [])
    carousel_frames = creative.get("carousel_frames", [])
    video_shot_ideas = creative.get("video_shot_ideas", [])
    hooks = brief.get("hooks", [])
    sections = [
        f"# Creative Package: {brief.get('id', '')}",
        "",
        f"Title: {brief.get('title', '')}",
        f"Visual theme: {creative.get('visual_theme', '')}",
        f"Primary channel: {brief.get('primary_channel', '')}",
        "",
        "## Thumbnail Concepts",
        *[f"- {item}" for item in thumbnail_concepts],
        "",
        "## Image Prompt Directions",
        *[f"- {item}" for item in image_prompt_directions],
        "",
        "## On-screen Text",
        *[f"- {item}" for item in onscreen_text],
        "",
        "## Carousel Frames",
        *[f"- {item}" for item in carousel_frames],
        "",
        "## Short Video Storyboard",
        f"- Hook frame: {hooks[0] if hooks else brief.get('punch_idea', '')}",
        *[f"- Shot idea: {item}" for item in video_shot_ideas],
        f"- Close frame: {brief.get('primary_cta', '')}",
        "",
    ]
    return "\n".join(sections).strip() + "\n"


def _editorial_recommendation(items: list[dict[str, Any]], today: date) -> dict[str, Any] | None:
    backlog = [item for item in items if item.get("status") == "backlog" and item.get("brief_id")]
    if backlog:
        backlog.sort(key=lambda item: _parse_optional_date(item.get("suggested_publish_date")) or today)
        return backlog[0]
    scheduled = []
    for item in items:
        when = _parse_optional_date(item.get("scheduled_for") or item.get("suggested_publish_date"))
        if when is not None and when >= today:
            scheduled.append((when, item))
    scheduled.sort(key=lambda pair: pair[0])
    return scheduled[0][1] if scheduled else None


def _queue_status_for_brief(status: str) -> str:
    mapping = {
        "drafting_ready": "backlog",
        "approved_for_drafting": "backlog",
        "in_review": "in_review",
        "approved": "approved",
        "scheduled": "scheduled",
        "published": "published",
        "paused": "paused",
    }
    return mapping.get(status, "backlog")


def _effective_queue_status(queue_status: str, brief_status: str) -> str:
    if brief_status:
        return _queue_status_for_brief(brief_status)
    return queue_status


def _hooks_for(*, title: str, idea: str, pillar_label: str) -> list[str]:
    short_idea = _clean_sentence(idea)
    return [
        f"The headline is {title.lower()}. The real story is what it changes on the ground.",
        f"Most people notice the headline. Operators notice the constraint behind it.",
        f"If you're building across borders, {pillar_label.lower()} shows up earlier than your spreadsheet says it will.",
    ]


def _proof_points_for(*, idea: str, audience_label: str) -> list[str]:
    return [
        idea.strip(),
        f"This matters to {audience_label.lower()} because execution quality changes trust and outcomes.",
    ]


def _supporting_points_for(*, idea: str, pillar_label: str) -> list[str]:
    observation, angle = _split_raw_idea(idea)
    return [
        observation,
        angle or f"{pillar_label} is rarely abstract. It shows up in execution quality, timing, and leverage.",
        "The useful move is to change behavior, not just repeat the insight.",
    ]


def _objections_for(stage_key: str) -> list[str]:
    if stage_key == "decision":
        return ["Why act now instead of waiting?", "What makes NRG Bloom credible here?"]
    if stage_key == "consideration":
        return ["Is this practical or just interesting?", "What would implementation look like?"]
    return ["Is this really a major issue?", "Does this apply outside one edge case?"]


def _contrarian_angle_for(stage_key: str, *, pillar_label: str) -> str:
    if stage_key == "decision":
        return f"The real blocker is rarely awareness. It is whether {pillar_label.lower()} turns into action."
    if stage_key == "consideration":
        return f"Most people stop at insight. The edge comes from operationalizing {pillar_label.lower()}."
    return f"What sounds obvious becomes valuable when explained through real {pillar_label.lower()} experience."


def _emotional_driver_for(pillar_key: str) -> str:
    mapping = {
        "builder_credibility": "earned confidence",
        "nigeria_market_reality": "hard-won realism",
        "founder_lessons": "disciplined caution",
        "field_storytelling": "field tension",
        "future_facing_authority": "measured ambition",
    }
    return mapping.get(pillar_key, "practical authority")


def _business_goal_for(stage_key: str) -> str:
    mapping = {
        "awareness": "Build founder authority and grow relevant reach.",
        "consideration": "Create qualified conversations and deepen trust.",
        "decision": "Drive inbound interest and direct project conversations.",
    }
    return mapping.get(stage_key, "Build useful audience trust.")


def _campaign_theme_for(pillar_key: str) -> str:
    mapping = {
        "builder_credibility": "operator credibility",
        "nigeria_market_reality": "building in West Africa",
        "founder_lessons": "founder discipline",
        "field_storytelling": "field execution reality",
        "future_facing_authority": "what we build next",
    }
    return mapping.get(pillar_key, "NRG Bloom field notes")


def _punch_idea_for(idea: str) -> str:
    observation, angle = _split_raw_idea(idea)
    if angle:
        return angle
    return observation


def _main_thesis_for(idea: str, *, pillar_label: str) -> str:
    trimmed = _clean_sentence(idea)
    return f"{trimmed}. That is the practical edge behind {pillar_label.lower()}."


def _clean_sentence(value: str) -> str:
    return " ".join(str(value).strip().rstrip(".").split())


def _split_raw_idea(value: str) -> tuple[str, str]:
    cleaned = _clean_sentence(value)
    marker = "NRG Bloom angle:"
    if marker in cleaned:
        observation, angle = cleaned.split(marker, 1)
        return observation.strip(), angle.strip()
    return cleaned, ""


def _pick_hook(hooks: list[str], *, fallback: str) -> str:
    for hook in hooks:
        cleaned = _clean_sentence(hook)
        if cleaned:
            return cleaned
    return fallback


def _fresh_hook_for(title: str, observation: str, *, signature_patterns: list[str], exemplar: dict[str, Any] | None) -> str:
    topic = title.lower()
    exemplar_open = _clean_sentence((exemplar or {}).get("opening_pattern", ""))
    if signature_patterns:
        lead = signature_patterns[0].rstrip(".")
        if "headline" in lead.lower():
            return f"{lead}. {title} is where that difference starts."
    if exemplar_open.startswith("Open with a misconception"):
        return f"What most people miss about {topic} is where the real lesson starts."
    if exemplar_open.startswith("Start with quiet authority"):
        return f"I've learned that {topic} is usually misunderstood by people who only see the polished version."
    if "nigeria" in topic:
        return f"{title} is not just a policy story. It changes what becomes workable on the ground."
    if observation:
        return f"{title} is not just a headline. It changes how operators should read the market."
    return f"The headline is {topic}. The real story is what it changes for operators."


def _fresh_second_hook_for(pillar_text: str, *, signature_patterns: list[str], exemplar: dict[str, Any] | None) -> str:
    exemplar_open = _clean_sentence((exemplar or {}).get("opening_pattern", ""))
    if len(signature_patterns) > 1:
        return signature_patterns[1].rstrip(".") + f" for {pillar_text}."
    if exemplar_open.startswith("Lead with what was learned in the field"):
        return f"This is less about commentary and more about what the field teaches you about {pillar_text}."
    return f"Most people stop at the headline. Serious builders ask what it means for {pillar_text}."


def _resolved_punch_idea(raw_idea: str, stored_punch: str) -> str:
    cleaned = _clean_sentence(stored_punch)
    if cleaned and "..." not in cleaned:
        return cleaned
    return _punch_idea_for(raw_idea)


def _unique_lines(values: list[str], *, fallback: list[str]) -> list[str]:
    lines: list[str] = []
    seen: set[str] = set()
    for value in values + fallback:
        cleaned = _clean_sentence(value)
        if not cleaned:
            continue
        key = cleaned.casefold()
        if key in seen:
            continue
        seen.add(key)
        lines.append(cleaned)
    return lines


def _email_subject_for(title: str, punch_line: str) -> str:
    if len(punch_line) <= 72:
        return punch_line
    return title


def _bridge_line_for(exemplar: dict[str, Any] | None, *, default: str) -> str:
    moves = (exemplar or {}).get("moves", [])
    if isinstance(moves, list):
        for move in moves:
            cleaned = _clean_sentence(move)
            if "ground truth" in cleaned.lower():
                return "The useful move is to replace surface interpretation with ground truth."
            if "unseen work" in cleaned.lower():
                return "Most people respond to the polished story. The work that matters happens earlier and under more pressure."
    return default


def _close_line_for(exemplar: dict[str, Any] | None, *, default: str, cta: str) -> str:
    closing = _clean_sentence((exemplar or {}).get("closing_pattern", ""))
    if "future lessons" in closing.lower():
        return "I’ll keep sharing the lessons that come from building under real pressure."
    if "future projects" in closing.lower() or "partnerships" in closing.lower():
        return "The point is not to sound insightful. It is to become the kind of operator stronger projects and partnerships actually need."
    if "practical takeaway" in closing.lower():
        return default
    return cta


def _thread_points(points: list[str], punch_line: str) -> list[str]:
    filtered = [point for point in points if _clean_sentence(point).casefold() != _clean_sentence(punch_line).casefold()]
    return filtered[:2]


def _draft_key_for_channel(channel: str) -> str:
    mapping = {
        "linkedin": "linkedin",
        "x": "x_thread",
        "email": "email",
    }
    return mapping.get(channel, channel)


def _first_line(text: str) -> str:
    for line in str(text).splitlines():
        cleaned = line.strip()
        if cleaned:
            return cleaned
    return ""


def _pillar_takeaway_for(pillar_text: str) -> str:
    label = pillar_text or "execution"
    return f"{label.capitalize()} is a market-reading problem before it becomes a communication problem."


def _practical_move_line_for(stage_key: str) -> str:
    if stage_key == "decision":
        return "The practical edge is showing the buyer what changes if they move now."
    if stage_key == "consideration":
        return "The practical edge is turning the insight into a framework someone can actually use."
    return "The practical edge comes from changing how you move, not just how you narrate the situation."


def _voice_profile_for_strategy(strategy: dict[str, Any], *, pillar_key: str, stage_key: str) -> dict[str, Any]:
    voice_system = strategy.get("brand", {}).get("voice_system", {})
    format_rules = voice_system.get("format_rules", {})
    return {
        "brand_voice": strategy.get("brand", {}).get("voice", []),
        "posture": voice_system.get("posture", []),
        "do": voice_system.get("do", []),
        "avoid": voice_system.get("avoid", []),
        "signature_patterns": voice_system.get("signature_patterns", []),
        "pillar_emphasis": pillar_key,
        "stage_emphasis": stage_key,
        "format_rules": format_rules,
    }


def _voice_profile_from_brief(brief: dict[str, Any]) -> dict[str, Any]:
    profile = brief.get("voice_profile", {})
    if isinstance(profile, dict) and profile:
        return profile
    return {
        "brand_voice": brief.get("guardrails", {}).get("brand_voice_rules", []),
        "posture": ["Write like an operator who has paid for the lesson."],
        "do": ["Lead with what changed and why it matters."],
        "avoid": ["generic thought leadership"],
        "signature_patterns": [
            "Most people see the headline. Operators see the constraint.",
            "The real question is what this changes on the ground.",
        ],
        "format_rules": {},
    }


def _pick_exemplar(root: Path, *, pillar_key: str, stage_key: str, format_key: str) -> dict[str, Any] | None:
    data = _load_yaml(root / "nrg-bloom" / "marketing" / "library" / "exemplars.yaml")
    exemplars = data.get("library", {}).get("exemplars", [])
    if not isinstance(exemplars, list):
        return None
    best: tuple[int, dict[str, Any]] | None = None
    for exemplar in exemplars:
        if not isinstance(exemplar, dict):
            continue
        score = 0
        if exemplar.get("format") == format_key:
            score += 3
        if pillar_key in exemplar.get("pillars", []):
            score += 2
        if stage_key in exemplar.get("stages", []):
            score += 1
        if best is None or score > best[0]:
            best = (score, exemplar)
    if best and best[0] > 0:
        return best[1]
    return None


def _persona_problem_for(audience_meta: dict[str, Any]) -> str:
    pain_points = audience_meta.get("pain_points", [])
    if isinstance(pain_points, list) and pain_points:
        return str(pain_points[0])
    return "The audience needs practical, non-generic guidance."


def _primary_format_for(primary_channel: str) -> str:
    mapping = {
        "linkedin": "linkedin_post",
        "x": "x_thread",
        "email": "email_note",
    }
    return mapping.get(primary_channel, "content_asset")


def _repurpose_formats_for(repurpose_channels: list[str]) -> list[str]:
    mapping = {
        "linkedin": "linkedin_post",
        "x": "x_thread",
        "email": "email_note",
    }
    formats = [mapping.get(channel, channel) for channel in repurpose_channels]
    if "short_video_script" not in formats:
        formats.append("short_video_script")
    return formats


def _visual_theme_for(pillar_key: str) -> str:
    mapping = {
        "builder_credibility": "operator realism",
        "nigeria_market_reality": "field realism",
        "founder_lessons": "sharp editorial",
        "field_storytelling": "documentary tension",
        "future_facing_authority": "forward-looking infrastructure",
    }
    return mapping.get(pillar_key, "builder-first realism")


def _thumbnail_concepts_for(punch_idea: str) -> list[str]:
    return [
        f"Bold text pull-quote: {punch_idea[:60]}",
        "Founder portrait plus one operational contrast visual",
    ]


def _image_prompt_directions_for(pillar_key: str) -> list[str]:
    return [
        f"{pillar_key.replace('_', ' ')} visual, practical infrastructure setting, no site-identifiable details",
        "Editorial documentary style, commercially serious, no hype aesthetics",
    ]


def _carousel_frames_for(thesis: str, supporting_points: list[str]) -> list[str]:
    frames = ["The core problem", thesis]
    frames.extend(supporting_points[:2])
    frames.append("What to do differently")
    return frames


def _video_shot_ideas_for(pillar_key: str) -> list[str]:
    return [
        "Direct-to-camera founder lesson",
        f"B-roll that reinforces {pillar_key.replace('_', ' ')} without exposing protected details",
    ]


def _pick_first_match(text: str, rules: tuple[tuple[str, str], ...], *, default: str) -> str:
    for keyword, value in rules:
        if keyword in text:
            return value
    return default


def _next_brief_id(root: Path) -> str:
    briefs_dir = root / "nrg-bloom" / "marketing" / "briefs"
    highest = 0
    if briefs_dir.exists():
        for path in briefs_dir.glob("cb-*.yaml"):
            match = re.match(r"cb-(\d+)", path.stem)
            if match:
                highest = max(highest, int(match.group(1)))
    return f"CB-{highest + 1:03d}"


def _next_queue_id(items: list[Any]) -> str:
    highest = 0
    for item in items:
        if not isinstance(item, dict):
            continue
        match = re.fullmatch(r"CM-(\d+)", str(item.get("id", "")))
        if match:
            highest = max(highest, int(match.group(1)))
    return f"CM-{highest + 1:03d}"


def _next_publish_date(queue_data: dict[str, Any], today: date) -> date:
    cadence = queue_data.get("cadence", {})
    publish_days = cadence.get("publish_days", ["Tuesday", "Thursday"])
    day_numbers = [_weekday_number(value) for value in publish_days]
    existing_dates = set()
    for item in queue_data.get("items", []):
        if not isinstance(item, dict):
            continue
        scheduled = item.get("scheduled_for") or item.get("suggested_publish_date")
        parsed = _parse_optional_date(scheduled)
        if parsed is not None:
            existing_dates.add(parsed)
    for offset in range(1, 31):
        candidate = today + timedelta(days=offset)
        if candidate.weekday() in day_numbers and candidate not in existing_dates:
            return candidate
    return today + timedelta(days=7)


def _weekday_number(name: str) -> int:
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    return weekdays.get(str(name).lower(), 1)


def _parse_optional_date(value: Any) -> date | None:
    if value in (None, "", "none"):
        return None
    if isinstance(value, date):
        return value
    return datetime.strptime(str(value), "%Y-%m-%d").date()


def _slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return slug or "idea"


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not load as a mapping")
    return data


def _write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=False)
        temp_path = Path(handle.name)
    temp_path.replace(path)


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as handle:
        handle.write(content)
        temp_path = Path(handle.name)
    temp_path.replace(path)


def _append_audit(root: Path, *, action: str, path: Path, details: dict[str, Any]) -> None:
    audit_dir = root / ".work_codex"
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit_path = audit_dir / "audit.jsonl"
    event = {
        "timestamp": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "action": action,
        "path": str(path.relative_to(root)),
        "details": details,
    }
    with audit_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=True) + "\n")
