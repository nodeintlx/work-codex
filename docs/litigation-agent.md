# Litigation Agent Upgrade

## Problem

The existing legal-counsel skill is strategically rich but mostly prompt-driven. It knows the theory of the case, but the runtime had no structured case object tied to the live `nrg-bloom/litigation-ton/` folder.

## Upgrade

The litigation runtime now lives in `src/work_codex/litigation.py`.

It provides:
- structured loading of the TON matter from `settlement-tracker.yaml`
- extraction of current posture from `CONTEXT.md`
- deadline classification
- validation of core case artifacts
- a stable CLI surface for the agent to query before making recommendations

## Commands

```bash
PYTHONPATH=src python3 -m work_codex.cli litigation-validate --workspace .
PYTHONPATH=src python3 -m work_codex.cli litigation-status --workspace .
```

## Why this matters

This is the first step from a prompt-defined litigation agent to a case-grounded litigation system:
- strategy can now rely on explicit case state
- missing artifacts become detectable
- deadlines become machine-readable
- future drafting and filing helpers can target a defined matter object instead of reading ad hoc files

## Next upgrades

- add pleading tracker and filing tracker models
- parse chronology and evidence indexes into structured records
- add commands for updating settlement rounds and legal posture safely
- add drafting workflows tied to the current matter state
