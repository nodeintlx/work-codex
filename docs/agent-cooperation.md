# Agent Cooperation

## Goal

Create a stable cooperation loop between the Codex-native law agent in this repo and future external agents, including Claude-based agents.

Detailed protocol:

- [`docs/claude-codex-exchange-spec.md`](/home/dowsmasternode/repos/work-codex/docs/claude-codex-exchange-spec.md)

## Rule

Google Drive is the exchange layer, not the source of truth.

The source of truth remains:

- `shared/`
- `knowledge/`
- `nrg-bloom/litigation-ton/`
- `src/work_codex/`

## Exchange Contract

Initialize a shared exchange directory:

```bash
PYTHONPATH=src python3 -m work_codex.cli agent-exchange-init --workspace . --root ./agent-exchange
```

Write the current litigation handoff into that exchange:

```bash
PYTHONPATH=src python3 -m work_codex.cli litigation-handoff-write --workspace . --exchange-root ./agent-exchange
```

Ingest incoming artifacts plus manifests from the exchange:

```bash
PYTHONPATH=src python3 -m work_codex.cli agent-exchange-ingest --workspace . --exchange-root ./agent-exchange
```

The exchange directory contains:

- `incoming/`
- `outgoing/`
- `handoff/`
- `evidence/`
- `counsel/`
- `manifests/`

## Google Drive Pattern

Recommended setup:

1. Create a shared Google Drive folder, for example `Work Codex Agent Exchange`.
2. Sync that folder to a local directory on this machine.
3. Point `agent-exchange-init` and `litigation-handoff-write` at that synced local directory.

Example:

```bash
PYTHONPATH=src python3 -m work_codex.cli agent-exchange-init --workspace . --root ~/GoogleDrive/Work-Codex-Agent-Exchange
PYTHONPATH=src python3 -m work_codex.cli litigation-handoff-write --workspace . --exchange-root ~/GoogleDrive/Work-Codex-Agent-Exchange
```

## Manifest Rule

Any external agent that drops a file into `incoming/` should also create a manifest in `manifests/`.

Example fields:

- `artifact_path`
- `artifact_type`
- `source_agent`
- `requested_action`
- `matter`

Use the template at:

- `manifests/manifest-template.json`

## Recommended Flow

1. Claude agent writes an incident memo into `incoming/`.
2. Claude agent writes a manifest describing the requested action.
3. Codex reads the incoming artifact and manifest.
4. Codex copies the artifact into the TON matter under `agent-intake/`, creates a review task, and records the ingestion in memory.
5. If the manifest includes a structured `codex_state_patch`, Codex records it as a pending proposal under `agent-intake/proposals/`.
6. Codex regenerates drafts and writes a fresh `handoff/litigation-handoff.json`.
7. Codex moves the processed artifact and manifest into `incoming/processed/` and `manifests/processed/`.

## Proposal Review Layer

List pending proposals:

```bash
PYTHONPATH=src python3 -m work_codex.cli agent-proposal-status --workspace .
```

Apply a proposal explicitly:

```bash
PYTHONPATH=src python3 -m work_codex.cli agent-proposal-apply --workspace . --path ./nrg-bloom/litigation-ton/agent-intake/proposals/<proposal>.json
```

Promote a `pending_review` proposal into a structured patch when the suggestions are safe and obvious:

```bash
PYTHONPATH=src python3 -m work_codex.cli agent-proposal-promote --workspace . --path ./nrg-bloom/litigation-ton/agent-intake/proposals/<proposal>.json
```

Review the full human decision queue:

```bash
PYTHONPATH=src python3 -m work_codex.cli agent-review-queue --workspace .
```

This is the key safety rule:

- agents may propose structured state changes
- Codex may apply supported structured patches
- free-text legal conclusions should not directly mutate live state
- the human operator decides what gets promoted from queue to live case state

## Why this is the right split

- Drive is good at file exchange.
- The repo is better for structured state and repeatable logic.
- The handoff JSON is the inter-agent contract.
- This avoids both agents racing to edit YAML directly.
