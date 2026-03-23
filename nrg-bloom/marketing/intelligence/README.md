# BloomFlow Intelligence Layer

This folder contains the local-first intelligence layer for BloomFlow.

It is the bridge between the downloaded OpenClaw v2 concept and the current Codex-testable system.

## What It Does Today

- accepts manual or externally observed signals
- scores them with the BloomFlow router model
- decides `AUTO_FIRE`, `ADVISORY`, or `LOG_ONLY`
- optionally creates a canonical BloomFlow brief from the signal

## Files

- `router-settings.yaml` - signal thresholds and weights
- `signal-log.jsonl` - ingested signals and router decisions
- `signal-schema-2026-03-11.md` - canonical local signal shape

## Commands

```bash
PYTHONPATH=src python3 -m work_codex.cli signal-ingest --workspace . --domain ai_infra --headline "African data center expansion accelerates" --summary "A major hyperscaler announced new African data center capacity tied to AI demand growth." --nrg-angle "NRG Bloom can contrast hyperscaler capex with modular, local-first deployment reality." --source "Datacenter Dynamics" --published-at 2026-03-10 --pillar future_facing_authority --business-proximity 9 --content-opportunity 9 --recency-window 10 --topic-pillar-fit 9

PYTHONPATH=src python3 -m work_codex.cli signal-route --workspace . --id SIG-001 --create-brief

PYTHONPATH=src python3 -m work_codex.cli signal-log --workspace .

PYTHONPATH=src python3 -m work_codex.cli signal-backend --workspace .
```

## Why This Exists

Before BloomFlow gets an OpenClaw body, it needs a testable local intelligence loop.

This folder is that first version.
