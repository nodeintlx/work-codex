# Law Agent

## Purpose

This repository now has the beginnings of a Codex-native law agent, not just TON-specific drafting helpers.

The first reusable interoperability surface is:

```bash
PYTHONPATH=src python3 -m work_codex.cli litigation-handoff --workspace .
PYTHONPATH=src python3 -m work_codex.cli litigation-handoff-write --workspace . --exchange-root ./agent-exchange
PYTHONPATH=src python3 -m work_codex.cli agent-exchange-ingest --workspace . --exchange-root ./agent-exchange
PYTHONPATH=src python3 -m work_codex.cli agent-proposal-status --workspace .
PYTHONPATH=src python3 -m work_codex.cli agent-review-queue --workspace .
```

That command exports a stable JSON payload containing:

- live matter posture
- settlement posture
- filing readiness
- ranked strategic actions
- deadline state
- missing core artifacts
- latest generated work product
- recent incident memos

## Why this matters

If a future Claude-side agent needs to cooperate with the Codex-side litigation runtime, it should consume this handoff payload rather than scrape markdown files or infer posture from chat.

This creates a cleaner separation:

- `shared/` and `nrg-bloom/litigation-ton/` remain the editable source of truth
- `src/work_codex/` remains the Codex-native runtime
- `litigation-handoff` becomes the agent-to-agent contract
- `agent-exchange/` or a synced Google Drive folder becomes the document bus

## Initial Protocol

Protocol identifier:

`law-agent-handoff/v1`

The payload is designed for:

- future Codex litigation agents
- future Claude litigation/workflow agents
- simple automations or dashboards

Formal exchange contract:

- [`docs/claude-codex-exchange-spec.md`](/home/dowsmasternode/repos/work-codex/docs/claude-codex-exchange-spec.md)

## Near-Term Upgrades

- add explicit event-log exports for litigation mutations
- add witness and evidence-preservation queues
- add a normalized incident model instead of memo discovery by filename
- expand the proposal layer from explicit reviewed patches into richer structured litigation state updates
