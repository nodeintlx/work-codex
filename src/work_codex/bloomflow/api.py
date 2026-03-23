"""BloomFlow v2 function API.

All public operations go through these functions.
"""

from __future__ import annotations

import sqlite3
from datetime import date
from typing import Any

from .db import (
    append_audit,
    insert_brief,
    insert_queue_item,
    next_brief_id,
    next_queue_id,
    select_brief,
    select_briefs,
    select_queue_item,
    select_queue_items,
    update_brief_fields,
    update_queue_fields,
)
from .models import Brief, QueueItem
from .states import (
    BriefStatus,
    QueueStatus,
    queue_status_for_brief,
    validate_brief_transition,
    validate_queue_transition,
)


def _row_to_brief(row: dict[str, Any]) -> Brief:
    return Brief(
        id=row["id"],
        title=row["title"],
        raw_idea=row["raw_idea"],
        status=row["status"],
        created_at=row.get("created_at", ""),
        updated_at=row.get("updated_at", ""),
        owner=row.get("owner", "makir"),
        source_type=row.get("source_type", ""),
        source_ref=row.get("source_ref", ""),
        source_notes=row.get("source_notes") or [],
        original_language=row.get("original_language", "en"),
        audience_primary=row.get("audience_primary", ""),
        audience_secondary=row.get("audience_secondary") or [],
        persona_problem=row.get("persona_problem", ""),
        content_pillar=row.get("content_pillar", ""),
        funnel_stage=row.get("funnel_stage", ""),
        campaign_theme=row.get("campaign_theme", ""),
        business_goal=row.get("business_goal", ""),
        primary_cta=row.get("primary_cta", ""),
        lead_magnet=row.get("lead_magnet", ""),
        main_thesis=row.get("main_thesis", ""),
        punch_idea=row.get("punch_idea", ""),
        contrarian_angle=row.get("contrarian_angle", ""),
        emotional_driver=row.get("emotional_driver", ""),
        proof_points=row.get("proof_points") or [],
        hooks=row.get("hooks") or [],
        supporting_points=row.get("supporting_points") or [],
        objections_to_answer=row.get("objections_to_answer") or [],
        closing_angle=row.get("closing_angle", ""),
        primary_format=row.get("primary_format", ""),
        primary_channel=row.get("primary_channel", ""),
        repurpose_formats=row.get("repurpose_formats") or [],
        series_role=row.get("series_role", ""),
        publish_window=row.get("publish_window", ""),
        creative_direction=row.get("creative_direction") or {},
        guardrails=row.get("guardrails") or {},
        drafts=row.get("drafts") or {},
        performance=row.get("performance") or {},
    )


def _row_to_queue_item(row: dict[str, Any]) -> QueueItem:
    return QueueItem(
        id=row["id"],
        title=row["title"],
        status=row["status"],
        brief_id=row.get("brief_id", ""),
        pillar=row.get("pillar", ""),
        audience=row.get("audience", ""),
        funnel_stage=row.get("funnel_stage", ""),
        primary_channel=row.get("primary_channel", ""),
        repurpose_channels=row.get("repurpose_channels") or [],
        cta=row.get("cta", ""),
        lead_magnet=row.get("lead_magnet", ""),
        scheduled_for=row.get("scheduled_for", ""),
        suggested_publish_date=row.get("suggested_publish_date", ""),
        published_at=row.get("published_at", ""),
        brief_path=row.get("brief_path", ""),
        note_path=row.get("note_path", ""),
        source=row.get("source", ""),
    )


# --- Brief operations ---


def create_brief(
    conn: sqlite3.Connection,
    *,
    title: str,
    raw_idea: str,
    status: str = "drafting_ready",
    today: date | None = None,
    **kwargs: Any,
) -> Brief:
    """Create a new brief and return it."""
    today = today or date.today()
    BriefStatus(status)  # validate

    brief_id = kwargs.pop("id", None) or next_brief_id(conn)
    row: dict[str, Any] = {
        "id": brief_id,
        "title": title,
        "raw_idea": raw_idea,
        "status": status,
        "created_at": today.isoformat(),
        "updated_at": today.isoformat(),
    }
    row.update(kwargs)
    insert_brief(conn, row)

    append_audit(
        conn,
        action="brief_created",
        entity_type="brief",
        entity_id=brief_id,
        details={"title": title, "status": status},
    )
    return _row_to_brief(select_brief(conn, brief_id))  # type: ignore[arg-type]


def get_brief(conn: sqlite3.Connection, brief_id: str) -> Brief | None:
    """Fetch a brief by ID."""
    row = select_brief(conn, brief_id)
    if row is None:
        return None
    return _row_to_brief(row)


def list_briefs(conn: sqlite3.Connection, *, status: str | None = None) -> list[Brief]:
    """List briefs, optionally filtered by status."""
    if status is not None:
        BriefStatus(status)  # validate
    return [_row_to_brief(r) for r in select_briefs(conn, status=status)]


def update_brief(conn: sqlite3.Connection, brief_id: str, today: date | None = None, **fields: Any) -> Brief:
    """Update fields on an existing brief (does not change status — use transition_brief)."""
    today = today or date.today()
    existing = select_brief(conn, brief_id)
    if existing is None:
        raise ValueError(f"brief not found: {brief_id}")
    fields.pop("status", None)  # status changes must go through transition_brief
    fields["updated_at"] = today.isoformat()
    update_brief_fields(conn, brief_id, fields)
    return _row_to_brief(select_brief(conn, brief_id))  # type: ignore[arg-type]


def transition_brief(
    conn: sqlite3.Connection,
    brief_id: str,
    new_status: str,
    *,
    today: date | None = None,
    scheduled_for: str | None = None,
    published_at: str | None = None,
) -> Brief:
    """Transition a brief to a new status, enforcing the state machine."""
    today = today or date.today()
    target = BriefStatus(new_status)
    existing = select_brief(conn, brief_id)
    if existing is None:
        raise ValueError(f"brief not found: {brief_id}")
    current = BriefStatus(existing["status"])
    validate_brief_transition(current, target)

    updates: dict[str, Any] = {
        "status": target.value,
        "updated_at": today.isoformat(),
    }
    if scheduled_for is not None:
        updates["publish_window"] = scheduled_for
    if published_at is not None:
        perf = existing.get("performance") or {}
        assets = list(perf.get("published_assets") or [])
        assets.append({
            "date": published_at,
            "channel": existing.get("primary_channel", ""),
            "format": existing.get("primary_format", ""),
        })
        perf["published_assets"] = assets
        updates["performance"] = perf

    update_brief_fields(conn, brief_id, updates)

    # Sync linked queue item
    source_ref = existing.get("source_ref", "")
    if source_ref:
        queue_row = select_queue_item(conn, source_ref)
        if queue_row is not None:
            queue_updates: dict[str, Any] = {"status": queue_status_for_brief(target).value}
            if scheduled_for is not None:
                queue_updates["scheduled_for"] = scheduled_for
            if published_at is not None:
                queue_updates["published_at"] = published_at
            update_queue_fields(conn, source_ref, queue_updates)

    append_audit(
        conn,
        action="brief_transitioned",
        entity_type="brief",
        entity_id=brief_id,
        details={"from": current.value, "to": target.value},
    )
    return _row_to_brief(select_brief(conn, brief_id))  # type: ignore[arg-type]


# --- Queue operations ---


def add_queue_item(
    conn: sqlite3.Connection,
    *,
    title: str,
    status: str = "backlog",
    **kwargs: Any,
) -> QueueItem:
    """Add a new queue item and return it."""
    QueueStatus(status)  # validate

    item_id = kwargs.pop("id", None) or next_queue_id(conn)
    row: dict[str, Any] = {
        "id": item_id,
        "title": title,
        "status": status,
    }
    row.update(kwargs)
    insert_queue_item(conn, row)

    append_audit(
        conn,
        action="queue_item_added",
        entity_type="queue_item",
        entity_id=item_id,
        details={"title": title, "status": status},
    )
    return _row_to_queue_item(select_queue_item(conn, item_id))  # type: ignore[arg-type]


def get_queue_item(conn: sqlite3.Connection, item_id: str) -> QueueItem | None:
    """Fetch a queue item by ID."""
    row = select_queue_item(conn, item_id)
    if row is None:
        return None
    return _row_to_queue_item(row)


def list_queue(conn: sqlite3.Connection, *, status: str | None = None) -> list[QueueItem]:
    """List queue items, optionally filtered by status."""
    if status is not None:
        QueueStatus(status)  # validate
    return [_row_to_queue_item(r) for r in select_queue_items(conn, status=status)]


def transition_queue_item(
    conn: sqlite3.Connection,
    item_id: str,
    new_status: str,
    *,
    scheduled_for: str | None = None,
    published_at: str | None = None,
) -> QueueItem:
    """Transition a queue item to a new status, enforcing the state machine."""
    target = QueueStatus(new_status)
    existing = select_queue_item(conn, item_id)
    if existing is None:
        raise ValueError(f"queue item not found: {item_id}")
    current = QueueStatus(existing["status"])
    validate_queue_transition(current, target)

    updates: dict[str, Any] = {"status": target.value}
    if scheduled_for is not None:
        updates["scheduled_for"] = scheduled_for
    if published_at is not None:
        updates["published_at"] = published_at

    update_queue_fields(conn, item_id, updates)

    append_audit(
        conn,
        action="queue_item_transitioned",
        entity_type="queue_item",
        entity_id=item_id,
        details={"from": current.value, "to": target.value},
    )
    return _row_to_queue_item(select_queue_item(conn, item_id))  # type: ignore[arg-type]
