# NRG Bloom Authority Engine

The authority engine is the external-intelligence-first layer for periods when NRG Bloom
should keep publishing without relying on fresh operating disclosures.

It converts:

- trusted source watchlists
- recurring investor objections
- evergreen content franchises
- verified external and internal facts

into:

- a repeatable authority operating system
- a source watchlist
- an objection bank
- an evergreen franchise map
- an external-intelligence queue
- a weekly authority batch

## Commands

```bash
PYTHONPATH=src python3 -m work_codex.cli authority-os-build --workspace . --plan nrg-bloom/authority-engine/plans/2026-03-26-external-intel-authority.yaml
PYTHONPATH=src python3 -m work_codex.cli authority-weekly-batch-generate --workspace . --plan nrg-bloom/authority-engine/plans/2026-03-26-external-intel-authority.yaml
```
