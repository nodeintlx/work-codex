"""BloomFlow v2 migration — YAML to SQLite.

One-shot migrator that reads the existing v1 YAML files and inserts them
into the new SQLite database.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .db import (
    append_audit,
    init_db,
    insert_brief,
    insert_queue_item,
    open_db,
    select_brief,
    select_queue_item,
    db_path_for_workspace,
)


@dataclass
class MigrationResult:
    """Summary of what was migrated."""

    db_path: Path
    briefs_migrated: int = 0
    briefs_skipped: int = 0
    queue_items_migrated: int = 0
    queue_items_skipped: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def migrate_from_yaml(root: Path, *, db_path: Path | None = None) -> MigrationResult:
    """Migrate existing YAML data into a new (or existing) SQLite database.

    Skips records that already exist in the database (idempotent).
    """
    db = db_path or db_path_for_workspace(root)
    result = MigrationResult(db_path=db)

    conn = open_db(db)
    try:
        init_db(conn)
        _migrate_briefs(conn, root, result)
        _migrate_queue(conn, root, result)
        if result.briefs_migrated or result.queue_items_migrated:
            append_audit(
                conn,
                action="yaml_migration",
                entity_type="system",
                entity_id="migration",
                details={
                    "briefs_migrated": result.briefs_migrated,
                    "briefs_skipped": result.briefs_skipped,
                    "queue_items_migrated": result.queue_items_migrated,
                    "queue_items_skipped": result.queue_items_skipped,
                },
            )
    finally:
        conn.close()

    return result


def _migrate_briefs(conn: sqlite3.Connection, root: Path, result: MigrationResult) -> None:
    briefs_dir = root / "nrg-bloom" / "marketing" / "briefs"
    if not briefs_dir.exists():
        return
    for path in sorted(briefs_dir.glob("*.yaml")):
        try:
            data = _load_yaml(path)
            brief_id = str(data.get("id", ""))
            if not brief_id:
                result.errors.append(f"{path.name}: missing id")
                continue
            if select_brief(conn, brief_id) is not None:
                result.briefs_skipped += 1
                continue
            row = _yaml_brief_to_row(data)
            insert_brief(conn, row)
            result.briefs_migrated += 1
        except Exception as exc:
            result.errors.append(f"{path.name}: {exc}")


def _migrate_queue(conn: sqlite3.Connection, root: Path, result: MigrationResult) -> None:
    queue_path = root / "nrg-bloom" / "marketing" / "content-queue.yaml"
    if not queue_path.exists():
        return
    try:
        queue_data = _load_yaml(queue_path)
    except Exception as exc:
        result.errors.append(f"content-queue.yaml: {exc}")
        return

    items = queue_data.get("items", [])
    if not isinstance(items, list):
        result.errors.append("content-queue.yaml: items is not a list")
        return

    for item in items:
        if not isinstance(item, dict):
            continue
        item_id = str(item.get("id", ""))
        if not item_id:
            result.errors.append("queue item missing id")
            continue
        try:
            if select_queue_item(conn, item_id) is not None:
                result.queue_items_skipped += 1
                continue
            row = _yaml_queue_to_row(item)
            insert_queue_item(conn, row)
            result.queue_items_migrated += 1
        except Exception as exc:
            result.errors.append(f"queue item {item_id}: {exc}")


def _yaml_brief_to_row(data: dict[str, Any]) -> dict[str, Any]:
    """Convert a YAML brief dict to a database row dict."""
    audience = data.get("audience", {})
    if isinstance(audience, dict):
        audience_primary = str(audience.get("primary", ""))
        audience_secondary = audience.get("secondary", [])
    else:
        audience_primary = str(audience)
        audience_secondary = []

    return {
        "id": str(data.get("id", "")),
        "title": str(data.get("title", "")),
        "raw_idea": str(data.get("raw_idea", "")),
        "status": str(data.get("status", "drafting_ready")),
        "created_at": str(data.get("created_at", "")),
        "updated_at": str(data.get("updated_at", "")),
        "owner": str(data.get("owner", "makir")),
        "source_type": str(data.get("source_type", "")),
        "source_ref": str(data.get("source_ref", "")),
        "source_notes": data.get("source_notes") or [],
        "original_language": str(data.get("original_language", "en")),
        "audience_primary": audience_primary,
        "audience_secondary": audience_secondary if isinstance(audience_secondary, list) else [],
        "persona_problem": str(data.get("persona_problem", "")),
        "content_pillar": str(data.get("content_pillar", "")),
        "funnel_stage": str(data.get("funnel_stage", "")),
        "campaign_theme": str(data.get("campaign_theme", "")),
        "business_goal": str(data.get("business_goal", "")),
        "primary_cta": str(data.get("primary_cta", "")),
        "lead_magnet": str(data.get("lead_magnet", "")),
        "main_thesis": str(data.get("main_thesis", "")),
        "punch_idea": str(data.get("punch_idea", "")),
        "contrarian_angle": str(data.get("contrarian_angle", "")),
        "emotional_driver": str(data.get("emotional_driver", "")),
        "proof_points": data.get("proof_points") or [],
        "hooks": data.get("hooks") or [],
        "supporting_points": data.get("supporting_points") or [],
        "objections_to_answer": data.get("objections_to_answer") or [],
        "closing_angle": str(data.get("closing_angle", "")),
        "primary_format": str(data.get("primary_format", "")),
        "primary_channel": str(data.get("primary_channel", "")),
        "repurpose_formats": data.get("repurpose_formats") or [],
        "series_role": str(data.get("series_role", "")),
        "publish_window": str(data.get("publish_window", "")),
        "creative_direction": data.get("creative_direction") or {},
        "guardrails": data.get("guardrails") or {},
        "drafts": data.get("drafts") or {},
        "performance": data.get("performance") or {},
    }


def _yaml_queue_to_row(item: dict[str, Any]) -> dict[str, Any]:
    """Convert a YAML queue item dict to a database row dict."""
    return {
        "id": str(item.get("id", "")),
        "title": str(item.get("title", "")),
        "status": str(item.get("status", "backlog")),
        "brief_id": str(item.get("brief_id", "")),
        "pillar": str(item.get("pillar", "")),
        "audience": str(item.get("audience", "")),
        "funnel_stage": str(item.get("funnel_stage", "")),
        "primary_channel": str(item.get("primary_channel", "")),
        "repurpose_channels": item.get("repurpose_channels") or [],
        "cta": str(item.get("cta", "")),
        "lead_magnet": str(item.get("lead_magnet", "")),
        "scheduled_for": str(item.get("scheduled_for") or ""),
        "suggested_publish_date": str(item.get("suggested_publish_date") or ""),
        "published_at": str(item.get("published_at") or ""),
        "brief_path": str(item.get("brief_path") or ""),
        "note_path": str(item.get("note_path") or ""),
        "source": str(item.get("source") or ""),
    }


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not load as a mapping")
    return data
