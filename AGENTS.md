# Work Codex Agent Guide

This repository is the Codex-native evolution of the original workspace.

## Intent

Treat this repository as a software system with an operational knowledge base, not as a loose folder of prompts.

## Current source of truth

- Operational state lives in `shared/*.yaml`
- Durable memory lives in `knowledge/memory.jsonl`
- Company and project material lives under `nrg-bloom/`, `coldstorm/`, and `personal/`
- Runtime code lives in `src/work_codex/`
- `.claude/` is legacy compatibility material, not the canonical runtime

## Working rules

- Prefer changing runtime code over adding more prompt-only process when a rule can be enforced in software.
- Keep workspace data human-readable.
- Do not break compatibility with the existing YAML structure unless you also ship a migration.
- Prefer the CLI mutation commands over direct manual edits when changing tracked workspace state.
- Validate the workspace before relying on it:

```bash
PYTHONPATH=src python3 -m work_codex.cli validate --workspace .
PYTHONPATH=src python3 -m work_codex.cli doctor --workspace .
```

Examples:

```bash
PYTHONPATH=src python3 -m work_codex.cli task-update --workspace . --id 42 --status in_progress --append-note "Updated by Codex"
PYTHONPATH=src python3 -m work_codex.cli memory-append --workspace . --json '{"type":"entity","name":"Example","entityType":"note"}'
```

## Near-term architecture

1. `shared/` remains the editable operating layer.
2. `src/work_codex/` becomes the agent runtime layer.
3. Future services should consume the runtime layer rather than reading workspace files ad hoc.
4. `.claude/` remains optional migration/reference material until explicitly retired.

## Command surface (as of 2026-08-29)

The CLI has grown well beyond the task/deal/funding examples above. Full
list via `--help`; grouped here so this file doesn't go stale as fast:

- **Workspace health**: `validate`, `status`, `followup`, `doctor`
- **State mutation**: `task-add`, `task-update`, `pipeline-upsert`,
  `funding-upsert`, `memory-append`
- **Growth engines**: `content-campaign-generate`, `content-factcheck-run`,
  `content-motion-build`, `capital-infra-build`,
  `capital-weekly-batch-generate`, `authority-os-build`,
  `authority-weekly-batch-generate`
- **Litigation**: `litigation-status`, `litigation-validate`,
  `litigation-update`, `litigation-next-actions`, `litigation-handoff-write`
- **Filing/drafting**: `filing-status`, `filing-validate`, `filing-outline`,
  `draft-claim-outline`, `draft-facts`, `draft-exhibits`,
  `draft-alberta-skeleton`, `draft-write-bundle`
- **Settlement**: `settlement-update`, `settlement-round-add`
- **Agent exchange** (external-agent handoff protocol, e.g. the "Sentinel"
  process): `agent-exchange-ingest`, `agent-review-queue`,
  `agent-proposal-status`, `agent-proposal-apply`
- **Scheduler**: `scheduler-status`, `scheduler-run`

An audit trail already exists at `.work_codex/audit.jsonl`, and automatic
backups land in `.work_codex/backups/*.bak` on mutation — both older items
in the target list below.

## Immediate next build targets

- schema validation hardening
- ~~state mutation commands for tasks, deals, and funding~~ — shipped (see
  command surface above)
- ~~event log and audit trail~~ — shipped (`.work_codex/audit.jsonl`)
- ~~scheduler loop for recurring reviews and follow-ups~~ — CLI commands
  exist (`scheduler-run`/`scheduler-status`); confirm whether an actual
  recurring trigger (cron/loop) is wired up, or just the on-demand command
  surface — not verified as part of the 2026-08-29 audit
- API layer for remote and multi-agent operation
- **New from 2026-08-29 audit**: a `goals.yaml` mutation command (goals are
  still hand-edited YAML, the last surviving manual-edit tracked file)
- **New from 2026-08-29 audit**: this workspace went ~6 months (2026-03-23
  to 2026-08-29) without a git commit or a CLI mutation while real state
  moved on substantially — consider a periodic `doctor`/`status` health
  check (e.g. via the scheduler) that flags "no commit/mutation in N days"
  so this doesn't recur silently
