# NRG Bloom Capital Engine

This layer turns verified NRG Bloom proof plus external market evidence into
investor-facing infrastructure.

It is meant to close the loop between:

- public authority content
- investor education
- diligence readiness
- capital formation

## Outputs

Each `capital-infra-build` run generates:

- `investor-thesis/investor-memo.md`
- `investor-thesis/one-page-brief.md`
- `diligence-room/proof-of-execution.md`
- `diligence-room/market-and-timing.md`
- `diligence-room/diligence-snapshot.md`
- `audience-map.yaml`
- `audience-playbook.md`
- `content-backlog.yaml`
- `distribution-playbook.md`
- `content-to-capital-map.md`
- `investor-outreach-sequences.md`
- `weekly-operating-system.md`
- `capital-dashboard.html`

The weekly operating layer can also be generated separately:

```bash
PYTHONPATH=src python3 -m work_codex.cli capital-weekly-batch-generate --workspace . --plan nrg-bloom/capital-engine/plans/2026-03-26-investor-conversion-foundation.yaml
```

## Principle

This engine keeps two layers separate:

- `verified facts`: what the records and public sources support
- `strategic interpretation`: why those facts matter for investors

That separation is necessary if the output is supposed to survive real
diligence rather than just produce attractive copy.
