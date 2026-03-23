"""BloomFlow v2 data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Brief:
    """Canonical content brief — single source of truth for one content asset."""

    id: str
    title: str
    raw_idea: str
    status: str

    # metadata
    created_at: str = ""
    updated_at: str = ""
    owner: str = "makir"
    source_type: str = ""
    source_ref: str = ""

    # raw input
    source_notes: list[str] = field(default_factory=list)
    original_language: str = "en"

    # strategy
    audience_primary: str = ""
    audience_secondary: list[str] = field(default_factory=list)
    persona_problem: str = ""
    content_pillar: str = ""
    funnel_stage: str = ""
    campaign_theme: str = ""
    business_goal: str = ""
    primary_cta: str = ""
    lead_magnet: str = ""

    # thesis
    main_thesis: str = ""
    punch_idea: str = ""
    contrarian_angle: str = ""
    emotional_driver: str = ""
    proof_points: list[str] = field(default_factory=list)

    # messaging
    hooks: list[str] = field(default_factory=list)
    supporting_points: list[str] = field(default_factory=list)
    objections_to_answer: list[str] = field(default_factory=list)
    closing_angle: str = ""

    # format plan
    primary_format: str = ""
    primary_channel: str = ""
    repurpose_formats: list[str] = field(default_factory=list)
    series_role: str = ""
    publish_window: str = ""

    # structured blobs (stored as JSON)
    creative_direction: dict[str, Any] = field(default_factory=dict)
    guardrails: dict[str, Any] = field(default_factory=dict)
    drafts: dict[str, str] = field(default_factory=dict)
    performance: dict[str, Any] = field(default_factory=dict)


@dataclass
class QueueItem:
    """Content queue entry — tracks scheduling and status of a content idea."""

    id: str
    title: str
    status: str

    brief_id: str = ""
    pillar: str = ""
    audience: str = ""
    funnel_stage: str = ""
    primary_channel: str = ""
    repurpose_channels: list[str] = field(default_factory=list)
    cta: str = ""
    lead_magnet: str = ""
    scheduled_for: str = ""
    suggested_publish_date: str = ""
    published_at: str = ""
    brief_path: str = ""
    note_path: str = ""
    source: str = ""
