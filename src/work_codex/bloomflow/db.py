"""BloomFlow v2 SQLite database layer."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

_SCHEMA_VERSION = 1

_SCHEMA_SQL = """\
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS briefs (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    raw_idea        TEXT NOT NULL,
    status          TEXT NOT NULL,

    created_at      TEXT NOT NULL DEFAULT '',
    updated_at      TEXT NOT NULL DEFAULT '',
    owner           TEXT NOT NULL DEFAULT 'makir',
    source_type     TEXT NOT NULL DEFAULT '',
    source_ref      TEXT NOT NULL DEFAULT '',

    source_notes        TEXT NOT NULL DEFAULT '[]',
    original_language   TEXT NOT NULL DEFAULT 'en',

    audience_primary    TEXT NOT NULL DEFAULT '',
    audience_secondary  TEXT NOT NULL DEFAULT '[]',
    persona_problem     TEXT NOT NULL DEFAULT '',
    content_pillar      TEXT NOT NULL DEFAULT '',
    funnel_stage        TEXT NOT NULL DEFAULT '',
    campaign_theme      TEXT NOT NULL DEFAULT '',
    business_goal       TEXT NOT NULL DEFAULT '',
    primary_cta         TEXT NOT NULL DEFAULT '',
    lead_magnet         TEXT NOT NULL DEFAULT '',

    main_thesis         TEXT NOT NULL DEFAULT '',
    punch_idea          TEXT NOT NULL DEFAULT '',
    contrarian_angle    TEXT NOT NULL DEFAULT '',
    emotional_driver    TEXT NOT NULL DEFAULT '',
    proof_points        TEXT NOT NULL DEFAULT '[]',

    hooks               TEXT NOT NULL DEFAULT '[]',
    supporting_points   TEXT NOT NULL DEFAULT '[]',
    objections_to_answer TEXT NOT NULL DEFAULT '[]',
    closing_angle       TEXT NOT NULL DEFAULT '',

    primary_format      TEXT NOT NULL DEFAULT '',
    primary_channel     TEXT NOT NULL DEFAULT '',
    repurpose_formats   TEXT NOT NULL DEFAULT '[]',
    series_role         TEXT NOT NULL DEFAULT '',
    publish_window      TEXT NOT NULL DEFAULT '',

    creative_direction  TEXT NOT NULL DEFAULT '{}',
    guardrails          TEXT NOT NULL DEFAULT '{}',
    drafts              TEXT NOT NULL DEFAULT '{}',
    performance         TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS queue_items (
    id                  TEXT PRIMARY KEY,
    title               TEXT NOT NULL,
    status              TEXT NOT NULL,

    brief_id            TEXT NOT NULL DEFAULT '',
    pillar              TEXT NOT NULL DEFAULT '',
    audience            TEXT NOT NULL DEFAULT '',
    funnel_stage        TEXT NOT NULL DEFAULT '',
    primary_channel     TEXT NOT NULL DEFAULT '',
    repurpose_channels  TEXT NOT NULL DEFAULT '[]',
    cta                 TEXT NOT NULL DEFAULT '',
    lead_magnet         TEXT NOT NULL DEFAULT '',
    scheduled_for       TEXT NOT NULL DEFAULT '',
    suggested_publish_date TEXT NOT NULL DEFAULT '',
    published_at        TEXT NOT NULL DEFAULT '',
    brief_path          TEXT NOT NULL DEFAULT '',
    note_path           TEXT NOT NULL DEFAULT '',
    source              TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS audit_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp   TEXT NOT NULL,
    action      TEXT NOT NULL,
    entity_type TEXT NOT NULL DEFAULT '',
    entity_id   TEXT NOT NULL DEFAULT '',
    details     TEXT NOT NULL DEFAULT '{}'
);
"""

# JSON-encoded list/dict fields on briefs
_BRIEF_JSON_FIELDS = frozenset({
    "source_notes", "audience_secondary", "proof_points",
    "hooks", "supporting_points", "objections_to_answer",
    "repurpose_formats", "creative_direction", "guardrails",
    "drafts", "performance",
})

# JSON-encoded fields on queue_items
_QUEUE_JSON_FIELDS = frozenset({
    "repurpose_channels",
})


def open_db(path: Path) -> sqlite3.Connection:
    """Open (or create) the BloomFlow database at *path*."""
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Create tables if they don't exist and record schema version."""
    conn.executescript(_SCHEMA_SQL)
    row = conn.execute("SELECT version FROM schema_version").fetchone()
    if row is None:
        conn.execute("INSERT INTO schema_version (version) VALUES (?)", (_SCHEMA_VERSION,))
        conn.commit()


def db_path_for_workspace(root: Path) -> Path:
    """Return the canonical database path for a workspace root."""
    return root / ".work_codex" / "bloomflow.db"


# --- Brief CRUD ---

def insert_brief(conn: sqlite3.Connection, data: dict[str, Any]) -> None:
    """Insert a new brief row."""
    row = _encode_brief(data)
    cols = ", ".join(row.keys())
    placeholders = ", ".join("?" for _ in row)
    conn.execute(f"INSERT INTO briefs ({cols}) VALUES ({placeholders})", tuple(row.values()))
    conn.commit()


def select_brief(conn: sqlite3.Connection, brief_id: str) -> dict[str, Any] | None:
    """Return a brief row as a dict, or None."""
    row = conn.execute("SELECT * FROM briefs WHERE id = ?", (brief_id,)).fetchone()
    if row is None:
        return None
    return _decode_brief(dict(row))


def select_briefs(conn: sqlite3.Connection, *, status: str | None = None) -> list[dict[str, Any]]:
    """Return brief rows, optionally filtered by status."""
    if status is not None:
        rows = conn.execute("SELECT * FROM briefs WHERE status = ? ORDER BY created_at", (status,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM briefs ORDER BY created_at").fetchall()
    return [_decode_brief(dict(r)) for r in rows]


def update_brief_fields(conn: sqlite3.Connection, brief_id: str, fields: dict[str, Any]) -> None:
    """Update specific fields on a brief."""
    encoded = _encode_brief(fields)
    sets = ", ".join(f"{col} = ?" for col in encoded)
    values = list(encoded.values()) + [brief_id]
    conn.execute(f"UPDATE briefs SET {sets} WHERE id = ?", values)
    conn.commit()


# --- Queue CRUD ---

def insert_queue_item(conn: sqlite3.Connection, data: dict[str, Any]) -> None:
    """Insert a new queue item row."""
    row = _encode_queue(data)
    cols = ", ".join(row.keys())
    placeholders = ", ".join("?" for _ in row)
    conn.execute(f"INSERT INTO queue_items ({cols}) VALUES ({placeholders})", tuple(row.values()))
    conn.commit()


def select_queue_item(conn: sqlite3.Connection, item_id: str) -> dict[str, Any] | None:
    """Return a queue item row as a dict, or None."""
    row = conn.execute("SELECT * FROM queue_items WHERE id = ?", (item_id,)).fetchone()
    if row is None:
        return None
    return _decode_queue(dict(row))


def select_queue_items(conn: sqlite3.Connection, *, status: str | None = None) -> list[dict[str, Any]]:
    """Return queue item rows, optionally filtered by status."""
    if status is not None:
        rows = conn.execute(
            "SELECT * FROM queue_items WHERE status = ? ORDER BY COALESCE(NULLIF(scheduled_for,''), suggested_publish_date)",
            (status,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM queue_items ORDER BY COALESCE(NULLIF(scheduled_for,''), suggested_publish_date)",
        ).fetchall()
    return [_decode_queue(dict(r)) for r in rows]


def update_queue_fields(conn: sqlite3.Connection, item_id: str, fields: dict[str, Any]) -> None:
    """Update specific fields on a queue item."""
    encoded = _encode_queue(fields)
    sets = ", ".join(f"{col} = ?" for col in encoded)
    values = list(encoded.values()) + [item_id]
    conn.execute(f"UPDATE queue_items SET {sets} WHERE id = ?", values)
    conn.commit()


# --- Audit ---

def append_audit(conn: sqlite3.Connection, *, action: str, entity_type: str, entity_id: str, details: dict[str, Any]) -> None:
    """Append an audit log entry."""
    from datetime import UTC, datetime
    conn.execute(
        "INSERT INTO audit_log (timestamp, action, entity_type, entity_id, details) VALUES (?, ?, ?, ?, ?)",
        (
            datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
            action,
            entity_type,
            entity_id,
            json.dumps(details, ensure_ascii=True),
        ),
    )
    conn.commit()


# --- ID generation ---

def next_brief_id(conn: sqlite3.Connection) -> str:
    """Return the next available CB-NNN id."""
    row = conn.execute("SELECT id FROM briefs ORDER BY id DESC LIMIT 1").fetchone()
    if row is None:
        return "CB-001"
    import re
    match = re.match(r"CB-(\d+)", row["id"])
    num = int(match.group(1)) if match else 0
    return f"CB-{num + 1:03d}"


def next_queue_id(conn: sqlite3.Connection) -> str:
    """Return the next available CM-NNN id."""
    row = conn.execute("SELECT id FROM queue_items ORDER BY id DESC LIMIT 1").fetchone()
    if row is None:
        return "CM-001"
    import re
    match = re.match(r"CM-(\d+)", row["id"])
    num = int(match.group(1)) if match else 0
    return f"CM-{num + 1:03d}"


# --- Encoding helpers ---

def _encode_brief(data: dict[str, Any]) -> dict[str, Any]:
    """JSON-encode list/dict fields for storage."""
    out: dict[str, Any] = {}
    for key, value in data.items():
        if key in _BRIEF_JSON_FIELDS and not isinstance(value, str):
            out[key] = json.dumps(value, ensure_ascii=True)
        else:
            out[key] = value
    return out


def _decode_brief(row: dict[str, Any]) -> dict[str, Any]:
    """JSON-decode list/dict fields from storage."""
    for key in _BRIEF_JSON_FIELDS:
        if key in row and isinstance(row[key], str):
            try:
                row[key] = json.loads(row[key])
            except (json.JSONDecodeError, TypeError):
                pass
    return row


def _encode_queue(data: dict[str, Any]) -> dict[str, Any]:
    """JSON-encode list fields for storage."""
    out: dict[str, Any] = {}
    for key, value in data.items():
        if key in _QUEUE_JSON_FIELDS and not isinstance(value, str):
            out[key] = json.dumps(value, ensure_ascii=True)
        else:
            out[key] = value
    return out


def _decode_queue(row: dict[str, Any]) -> dict[str, Any]:
    """JSON-decode list fields from storage."""
    for key in _QUEUE_JSON_FIELDS:
        if key in row and isinstance(row[key], str):
            try:
                row[key] = json.loads(row[key])
            except (json.JSONDecodeError, TypeError):
                pass
    return row
