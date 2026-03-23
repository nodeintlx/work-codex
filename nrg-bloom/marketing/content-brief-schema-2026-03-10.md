# NRG Bloom Content Brief Schema

Created: 2026-03-10
Purpose: define the canonical object that drives idea intake, drafting, creative generation, editorial review, and the future frontend.

## Why This Object Matters

Everything downstream should read from the same brief:

- drafting agents
- thumbnail and image concept agents
- repurposing agents
- editorial scheduling
- approval workflow
- analytics feedback

If the brief is weak, the whole system becomes generic. If the brief is strong, one idea can become a campaign.

## Design Rules

The brief must:

1. preserve the founder's original thought
2. force strategic clarity before drafting
3. support multiple output formats from one source
4. capture business intent, not just copy intent
5. carry legal and brand guardrails with it

## Canonical Sections

### 1. Metadata

Identifies the brief and lets the system track it over time.

Fields:
- `id`
- `created_at`
- `updated_at`
- `status`
- `owner`
- `source_type`
- `source_ref`

### 2. Raw Input

Stores the original thought before the system refines it.

Fields:
- `title`
- `raw_idea`
- `source_notes`
- `original_language`

### 3. Strategy

This is the core of the object.

Fields:
- `audience.primary`
- `audience.secondary`
- `persona_problem`
- `content_pillar`
- `funnel_stage`
- `campaign_theme`
- `business_goal`
- `primary_cta`
- `lead_magnet`

### 4. Thesis

This is what makes the content sharp instead of generic.

Fields:
- `main_thesis`
- `punch_idea`
- `contrarian_angle`
- `emotional_driver`
- `proof_points`

Definitions:
- `main_thesis`: the main argument
- `punch_idea`: the sharpest one-line takeaway
- `contrarian_angle`: what makes the content worth noticing
- `emotional_driver`: the feeling to trigger, such as urgency, ambition, caution, confidence, or relief
- `proof_points`: the evidence or experience that makes the claim credible

### 5. Messaging

This section shapes how the asset opens and lands.

Fields:
- `hooks`
- `supporting_points`
- `objections_to_answer`
- `closing_angle`

### 6. Format Plan

One idea should support many outputs.

Fields:
- `primary_format`
- `primary_channel`
- `repurpose_formats`
- `series_role`
- `publish_window`

### 7. Creative Direction

This is the bridge into thumbnails, visuals, carousels, and generated images.

Fields:
- `visual_theme`
- `thumbnail_concepts`
- `image_prompt_directions`
- `onscreen_text`
- `carousel_frames`
- `video_shot_ideas`

### 8. Guardrails

This section prevents bad outputs.

Fields:
- `brand_voice_rules`
- `legal_risk_level`
- `legal_notes`
- `claims_to_avoid`
- `required_review`

### 9. Production Outputs

This is where generated assets attach later.

Fields:
- `drafts.linkedin`
- `drafts.x_thread`
- `drafts.email`
- `drafts.article_outline`
- `drafts.video_script`
- `drafts.faq`

### 10. Performance

This is future-facing but should exist now so the schema does not need rework later.

Fields:
- `published_assets`
- `performance_snapshot`
- `lessons_learned`
- `next_derivatives`

## Required Fields For MVP

The first build only needs these to be mandatory:

- `id`
- `status`
- `title`
- `raw_idea`
- `audience.primary`
- `content_pillar`
- `funnel_stage`
- `main_thesis`
- `punch_idea`
- `hooks`
- `primary_format`
- `primary_channel`
- `primary_cta`
- `legal_risk_level`

## Good Brief Test

A brief is good if:

- a writer can draft from it without asking what the point is
- a designer can create a thumbnail direction from it
- an editor can schedule it confidently
- a reviewer can see the risk level quickly
- the same brief can produce three or more assets without drifting
