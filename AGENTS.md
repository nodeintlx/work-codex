# Work Codex Agent Guide

This repository is the Codex-native evolution of the original workspace.

## Intent

Treat this repository as a software system with an operational knowledge base, not as a loose folder of prompts.

## Current source of truth

- Operational state lives in `shared/*.yaml`
- Durable memory lives in `knowledge/memory.jsonl`
- Company and project material lives under `nrg-bloom/`, `coldstorm/`, and `personal/`
- Runtime code lives in `src/work_codex/`

## Working rules

- Prefer changing runtime code over adding more prompt-only process when a rule can be enforced in software.
- Keep workspace data human-readable.
- Do not break compatibility with the existing YAML structure unless you also ship a migration.
- Validate the workspace before relying on it:

```bash
PYTHONPATH=src python3 -m work_codex.cli validate --workspace .
```

## Near-term architecture

1. `shared/` remains the editable operating layer.
2. `src/work_codex/` becomes the agent runtime layer.
3. Future services should consume the runtime layer rather than reading workspace files ad hoc.

## Immediate next build targets

- schema validation hardening
- state mutation commands for tasks, deals, and funding
- event log and audit trail
- scheduler loop for recurring reviews and follow-ups
- API layer for remote and multi-agent operation
