# BloomFlow Signal Schema

Created: 2026-03-11
Purpose: define the local-first intelligence object that the future OpenClaw watchers and router will use.

## Signal Object

Required fields:

- `id`
- `created_at`
- `domain`
- `headline`
- `summary`
- `nrg_angle`
- `source`
- `published_at`
- `pillar`
- `scores.business_proximity`
- `scores.content_opportunity`
- `scores.recency_window`
- `scores.topic_pillar_fit`

Optional fields:

- `router_decision.score`
- `router_decision.action`
- `router_decision.reason`
- `router_decision.routed_at`
- `router_decision.brief_path`

## Domains

- `btc`
- `energy`
- `africa`
- `ai_infra`
- `manual`

## Router Actions

- `AUTO_FIRE`
- `ADVISORY`
- `LOG_ONLY`

## Scoring Model

Each axis is scored from `0` to `10`.

Weights:

- business proximity: `35`
- content opportunity: `30`
- recency window: `20`
- topic pillar fit: `15`

Output:

- score `>= 75` -> `AUTO_FIRE`
- score `50-74` -> `ADVISORY`
- score `< 50` -> `LOG_ONLY`

## Local-First Rule

In the current Codex version, signals are manually ingested through CLI.

In the future OpenClaw version, watchers will emit this same object automatically.
