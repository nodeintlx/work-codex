# BloomFlow System Brief

Created: 2026-03-10
Purpose: provide a concise but complete description of the current BloomFlow app so another agent can evaluate it.

## What BloomFlow Is

BloomFlow is the NRG Bloom content operating system inside `work-codex`.

It is not yet a polished frontend application. It is currently a backend-first content pipeline with:

- canonical content briefs
- draft generation
- creative generation
- editorial planning
- workflow state management
- frontend-ready JSON payloads

## Core Idea

One founder idea should become one structured brief.

That brief should then power:

- copy generation
- creative direction
- scheduling
- review and approval
- future analytics
- future frontend views

The system is designed to avoid generic AI output by forcing strategy before drafting.

## Main Objects

### 1. Content Queue

File:
- `nrg-bloom/marketing/content-queue.yaml`

Purpose:
- track all planned and backlog content items
- store scheduling state
- map queue items to briefs

### 2. Canonical Brief

Files:
- `nrg-bloom/marketing/briefs/*.yaml`

Purpose:
- single source of truth for a content asset
- holds strategy, thesis, hooks, creative direction, guardrails, drafts, and performance placeholders

### 3. Generated Assets

Files:
- `nrg-bloom/marketing/generated/*`

Purpose:
- draft packages
- creative packages
- backend summary JSON
- app contract JSON

## Current Commands

### Intake

`content-intake`

Purpose:
- capture a raw idea
- classify audience, pillar, funnel stage
- create canonical brief
- add queue item
- create a human-readable note

### Validation

`content-validate`

Purpose:
- ensure the marketing system files exist
- ensure a brief has all required fields
- catch broken settings before generation

### Drafting

`content-draft`

Purpose:
- generate LinkedIn, X thread, email, article outline, video script, and FAQ from a validated brief

### Creative

`content-creative`

Purpose:
- generate thumbnail concepts
- image prompt directions
- on-screen text
- carousel frames
- short video storyboard notes

### Editorial

`content-editorial`

Purpose:
- show next posts
- identify ready backlog items
- report funnel coverage and gaps
- recommend the next brief to move forward

### Workflow State

`content-status`

Purpose:
- move briefs through:
  - `drafting_ready`
  - `in_review`
  - `approved`
  - `scheduled`
  - `published`
  - `paused`

### Frontend Payloads

`content-backend`

Purpose:
- produce a normalized backend summary of queue items and editorial state

`content-app`

Purpose:
- produce a frontend-oriented payload with:
  - dashboard summary
  - dashboard cards
  - brief detail views
  - UI action definitions

## Current Strengths

- clear content object model
- deterministic CLI workflow
- strong test coverage for the current pipeline
- backend payloads already shaped for future UI
- strategy and safety embedded in the brief object

## Current Weaknesses

- no actual web UI yet
- no external image generation integration yet
- no analytics ingestion yet
- legacy queue items still point at older markdown sources instead of canonical briefs
- heuristic intake logic is useful but still simple

## How It Works End To End

1. Capture idea with `content-intake`
2. Validate brief with `content-validate`
3. Generate copy with `content-draft`
4. Generate creative direction with `content-creative`
5. Review board with `content-editorial`
6. Advance state with `content-status`
7. Export app-facing payloads with `content-backend` and `content-app`

## Files Another Agent Should Inspect First

- `src/work_codex/content.py`
- `src/work_codex/cli.py`
- `nrg-bloom/marketing/content-brief-schema-2026-03-10.md`
- `nrg-bloom/marketing/content-queue.yaml`
- `nrg-bloom/marketing/briefs/`
- `nrg-bloom/marketing/generated/backend-summary.json`
- `nrg-bloom/marketing/generated/app-contract.json`
- `tests/test_cli.py`

## Best Future Improvements

### Short Term

- migrate all queue items to canonical briefs
- add scheduling helpers that auto-promote approved briefs
- add richer brief scoring and approval criteria

### Medium Term

- build the frontend on top of `app-contract.json`
- add asset-level status tracking
- add performance ingestion and feedback loops
- add user-editable brand settings

### Long Term

- connect image generation
- connect publishing APIs
- add experiment tracking for hooks and CTAs
- add analytics-based content recommendations
