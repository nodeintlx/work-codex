# Claude-Codex Exchange Spec

## Purpose

This document defines the repeatable communication contract between:

- `claude-work-agent`
- `codex-law-agent`

for the TON litigation matter.

This is a human-routed protocol for now. It is designed so the same contract can later be automated via API.

## Core Rule

The shared Google Drive exchange is the transport layer.

It is **not** the source of truth.

The source of truth remains the Codex workspace:

- `nrg-bloom/litigation-ton/matter-status.yaml`
- `nrg-bloom/litigation-ton/settlement-tracker.yaml`
- `nrg-bloom/litigation-ton/claims-map.yaml`
- `nrg-bloom/litigation-ton/chronology-map.yaml`
- `nrg-bloom/litigation-ton/evidence-map.yaml`

## Shared Folders

Under `Work Codex Agent Exchange`:

- `incoming/`
- `outgoing/`
- `handoff/`
- `evidence/`
- `counsel/`
- `manifests/`

## Directionality

Claude to Codex:

- write artifacts to `incoming/`
- write a matching manifest to `manifests/`

Codex to Claude:

- write requests or question briefs to `outgoing/`
- write a matching manifest to `manifests/`

Shared machine-readable state:

- `handoff/litigation-handoff.json`

## Required Manifest Fields

Every manifest must include:

- `protocol_version`
- `artifact_path`
- `artifact_type`
- `source_agent`
- `requested_action`
- `matter`
- `created_at_utc`

## Supported Incoming Artifact Types

These are currently supported by the Codex ingest pipeline:

- `incident_memo`
- `evidence_summary`
- `strategy_note`
- `strategy_memo`
- `strategic_context`
- `witness_note`
- `counsel_draft`
- `decision_memo`
- `legal_analysis`
- `codex_response`

If Claude uses a new artifact type, Codex must explicitly add support before ingestion succeeds.

## Supported Outgoing Artifact Types

Codex may send:

- `question_brief`
- future request types as the protocol expands

Important:

- Codex ignores manifests whose `artifact_path` does not start with `incoming/`
- this prevents Codex from trying to ingest its own outgoing requests

## Claude Guidance

Before producing new litigation analysis, Claude should read:

- `handoff/litigation-handoff.json`

Claude should assume the handoff is more current than old chat context unless there is a reason to question it.

Claude should not directly edit Codex YAML files.

## Codex Guidance

Codex should:

1. ingest incoming artifacts
2. copy them into `nrg-bloom/litigation-ton/agent-intake/<artifact_type>/`
3. create a review task
4. append a durable memory record
5. create a proposal when structured or suggested state updates exist
6. refresh `handoff/litigation-handoff.json`

## Proposal Types

There are two proposal modes.

### 1. `pending`

Use when the artifact contains a structured, machine-applyable patch.

Examples:

- manifest contains `codex_state_patch`
- `codex_response` includes a fenced `json` patch block

These can potentially be applied by Codex after review.

### 2. `pending_review`

Use when the artifact contains only free-text state suggestions.

These must be converted into a structured patch before any live-state mutation.

## Preferred Structured Patch Format

Claude should prefer this format whenever asking Codex to update live state:

```json
{
  "matter_status": {
    "forum.canadian_path": "confirmed_pressure_filing",
    "filing.filing_readiness": "ready_pending_lawyer"
  },
  "claim_updates": [
    {
      "id": "C2",
      "set": {
        "forum_track": "alberta_primary",
        "status": "ready_to_plead"
      }
    }
  ]
}
```

Notes:

- `matter_status` keys should use dotted runtime paths
- `claim_updates` should target existing claim IDs
- unsupported sections should go under `notes_for_human_review`, not into the patch

## Human-In-The-Loop Commands

Refresh handoff:

```bash
PYTHONPATH=src python3 -m work_codex.cli litigation-handoff-write --workspace . --exchange-root '/mnt/g/My Drive/Work Codex Agent Exchange'
```

Ingest Claude artifacts:

```bash
PYTHONPATH=src python3 -m work_codex.cli agent-exchange-ingest --workspace . --exchange-root '/mnt/g/My Drive/Work Codex Agent Exchange'
```

Review queue:

```bash
PYTHONPATH=src python3 -m work_codex.cli agent-review-queue --workspace .
```

List proposals:

```bash
PYTHONPATH=src python3 -m work_codex.cli agent-proposal-status --workspace .
```

Apply a reviewed proposal:

```bash
PYTHONPATH=src python3 -m work_codex.cli agent-proposal-apply --workspace . --path <proposal-json>
```

Promote a `pending_review` proposal when Aegis can conservatively infer a structured patch:

```bash
PYTHONPATH=src python3 -m work_codex.cli agent-proposal-promote --workspace . --path <proposal-json>
```

## Operating Loop

1. Codex publishes current handoff.
2. Claude reads handoff.
3. Human asks Claude for targeted work.
4. Claude writes artifact + manifest into `incoming/`.
5. Human tells Codex to ingest.
6. Codex updates the review queue.
7. Human reviews proposals.
8. Codex applies only explicitly approved structured patches.

## Why This Protocol Works

- Claude remains strong at legal analysis and strategic challenge.
- Codex remains strong at structured litigation operations.
- The human keeps visibility into token use and case-critical mutations.
- The same protocol can later be automated with minimal redesign.
