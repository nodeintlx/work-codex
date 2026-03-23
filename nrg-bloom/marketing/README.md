# NRG Bloom Marketing OS

This folder is the working content system for NRG Bloom.

It is designed for one specific job: take rough founder ideas and turn them into a usable publishing queue tied to audience, funnel stage, and CTA.

## What Lives Here

- `brand-system.yaml` - audiences, pillars, funnel rules, and publishing guardrails
- `content-queue.yaml` - the active content backlog and scheduled queue
- `content-brief-schema-2026-03-10.md` - canonical brief design for agents and future frontend
- `ideas/` - one markdown brief per captured idea
- `templates/` - reusable drafting structure
- `operating-system-2026-03-10.md` - the higher-level workflow

## Current Operating Rule

As of March 10, 2026, the safest public lane is still the Phase 1 founder-authority strategy because the TON matter is active.

Before publishing, apply the guardrails from:

- `../litigation-ton/phase-1-content-strategy-2026-03-08.md`
- `../litigation-ton/content-inventory.yaml`

If a post can identify the counterparty, the site, the dispute, or protected evidence, it is not publish-ready.

## Commands

Capture a raw idea:

```bash
PYTHONPATH=src python3 -m work_codex.cli content-intake --workspace . --title "What people misunderstand about building projects in Nigeria" --idea "Founders underestimate how much trust, logistics, and visible movement matter when executing real infrastructure projects in Nigeria."
```

Review the queue:

```bash
PYTHONPATH=src python3 -m work_codex.cli content-calendar --workspace .
```

Validate the system and a brief:

```bash
PYTHONPATH=src python3 -m work_codex.cli content-validate --workspace . --brief ./nrg-bloom/marketing/templates/content-brief-example.yaml
```

Generate a multi-format draft package from a validated brief:

```bash
PYTHONPATH=src python3 -m work_codex.cli content-draft --workspace . --brief ./nrg-bloom/marketing/templates/content-brief-example.yaml
```

Generate the creative package from the same brief:

```bash
PYTHONPATH=src python3 -m work_codex.cli content-creative --workspace . --brief ./nrg-bloom/marketing/templates/content-brief-example.yaml
```

Review what BloomFlow thinks should happen next:

```bash
PYTHONPATH=src python3 -m work_codex.cli content-editorial --workspace .
```

Move a brief through the workflow:

```bash
PYTHONPATH=src python3 -m work_codex.cli content-status --workspace . --brief ./nrg-bloom/marketing/templates/content-brief-example.yaml --set-status scheduled --scheduled-for 2026-03-18
```

Emit the frontend-ready backend payload:

```bash
PYTHONPATH=src python3 -m work_codex.cli content-backend --workspace .
PYTHONPATH=src python3 -m work_codex.cli content-backend --workspace . --write
```

Emit the frontend contract payload:

```bash
PYTHONPATH=src python3 -m work_codex.cli content-app --workspace .
PYTHONPATH=src python3 -m work_codex.cli content-app --workspace . --write
```

Run the local-first intelligence layer:

```bash
PYTHONPATH=src python3 -m work_codex.cli signal-ingest --workspace . --domain ai_infra --headline "African data center expansion accelerates" --summary "A major hyperscaler announced new African data center capacity tied to AI demand growth." --nrg-angle "NRG Bloom can contrast hyperscaler capex with modular, local-first deployment reality." --source "Datacenter Dynamics" --published-at 2026-03-10 --pillar future_facing_authority --business-proximity 9 --content-opportunity 9 --recency-window 10 --topic-pillar-fit 9
PYTHONPATH=src python3 -m work_codex.cli signal-route --workspace . --id SIG-001 --create-brief
PYTHONPATH=src python3 -m work_codex.cli signal-log --workspace .
```
