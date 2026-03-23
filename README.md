# Work Codex

Work Codex is the Codex-owned evolution of Makir's agent workspace.

The original repository already contains valuable operating data:
- task, goal, funding, and pipeline state in YAML
- durable memory in JSONL
- company and project context in Markdown
- Claude-oriented workflows and skills

This version starts turning that workspace into software.

The architectural goal is a pure Codex-native agent system. Claude-era assets can remain as migration/reference material, but they are not the system root.

## Direction

The immediate goal is not a full 24/7 autonomous system in one jump. The first goal is a stable runtime layer that can:
- validate the workspace state
- surface urgent work automatically
- provide a repeatable status and follow-up interface
- become the bridge between the data layer and future always-on agents

## Current Runtime

The first runtime lives in `src/work_codex/` and exposes a CLI:

```bash
python3 -m work_codex.cli validate --workspace .
python3 -m work_codex.cli status --workspace .
python3 -m work_codex.cli followup --workspace .
python3 -m work_codex.cli doctor --workspace .
python3 -m work_codex.cli litigation-status --workspace .
python3 -m work_codex.cli litigation-update --workspace . --set phase=filing_strategy
python3 -m work_codex.cli filing-status --workspace .
python3 -m work_codex.cli draft-alberta-skeleton --workspace .
python3 -m work_codex.cli draft-write-bundle --workspace .
python3 -m work_codex.cli litigation-next-actions --workspace .
python3 -m work_codex.cli litigation-handoff --workspace .
python3 -m work_codex.cli agent-exchange-init --workspace . --root ./agent-exchange
python3 -m work_codex.cli litigation-handoff-write --workspace . --exchange-root ./agent-exchange
python3 -m work_codex.cli agent-exchange-ingest --workspace . --exchange-root ./agent-exchange
python3 -m work_codex.cli agent-proposal-status --workspace .
python3 -m work_codex.cli agent-proposal-promote --workspace . --path ./nrg-bloom/litigation-ton/agent-intake/proposals/example.json
python3 -m work_codex.cli agent-proposal-apply --workspace . --path ./nrg-bloom/litigation-ton/agent-intake/proposals/example.json
python3 -m work_codex.cli agent-review-queue --workspace .
python3 -m work_codex.cli content-intake --workspace . --title "What people misunderstand about building in Nigeria" --idea "Founders underestimate how much trust, logistics, and visible movement matter when executing real infrastructure projects in Nigeria."
python3 -m work_codex.cli content-calendar --workspace .
python3 -m work_codex.cli content-validate --workspace . --brief ./nrg-bloom/marketing/templates/content-brief-example.yaml
python3 -m work_codex.cli content-draft --workspace . --brief ./nrg-bloom/marketing/templates/content-brief-example.yaml
python3 -m work_codex.cli content-creative --workspace . --brief ./nrg-bloom/marketing/templates/content-brief-example.yaml
python3 -m work_codex.cli content-editorial --workspace .
python3 -m work_codex.cli content-status --workspace . --brief ./nrg-bloom/marketing/templates/content-brief-example.yaml --set-status scheduled --scheduled-for 2026-03-18
python3 -m work_codex.cli content-backend --workspace .
python3 -m work_codex.cli content-backend --workspace . --write
python3 -m work_codex.cli content-app --workspace .
python3 -m work_codex.cli content-app --workspace . --write
python3 -m work_codex.cli signal-ingest --workspace . --domain ai_infra --headline "African data center expansion accelerates" --summary "A major hyperscaler announced new African data center capacity tied to AI demand growth." --nrg-angle "NRG Bloom can contrast hyperscaler capex with modular, local-first deployment reality." --source "Datacenter Dynamics" --published-at 2026-03-10 --pillar future_facing_authority --business-proximity 9 --content-opportunity 9 --recency-window 10 --topic-pillar-fit 9
python3 -m work_codex.cli signal-route --workspace . --id SIG-001 --create-brief
python3 -m work_codex.cli signal-log --workspace .
python3 -m work_codex.cli signal-backend --workspace .
```

What it does now:
- checks the required workspace files exist and load cleanly
- reports overdue, due-soon, and blocked tasks
- reports at-risk OKRs
- reports overdue next actions in pipeline and funding
- updates tasks, pipeline, funding, and memory through audited CLI commands
- loads and validates the TON litigation matter from the live case folder
- supports safe updates to litigation posture and settlement tracker state
- builds structured filing readiness, exhibit scaffolds, and draft litigation sections from the TON matter state
- writes versioned TON draft bundles and ranks the next highest-leverage litigation actions
- exports a stable litigation handoff payload for future Codex/Claude agent cooperation
- captures raw NRG Bloom content ideas into structured briefs with audience, pillar, CTA, and queue placement
- reports the current NRG Bloom content calendar
- validates the NRG Bloom content system and canonical content briefs
- generates multi-format draft packages from validated content briefs
- generates creative packages with thumbnail concepts, image directions, carousel frames, and video storyboard notes
- generates an editorial board view with next posts, ready backlog, funnel coverage, and gaps
- updates content workflow state for review, approval, scheduling, and publishing
- emits a frontend-ready backend summary payload for BloomFlow
- emits a frontend contract payload with dashboard cards, brief detail views, and app actions
- supports a local-first intelligence loop: signal ingest, router scoring, and auto-brief creation
- provides a Codex-native environment check via `doctor`

## Repository Layout

```text
src/work_codex/     Python runtime and CLI
tests/              Runtime tests
shared/             Operational state
knowledge/          Durable memory and research
nrg-bloom/          NRG Bloom workspace
coldstorm/          Coldstorm workspace
personal/           Personal workspace
```

## Development

Run locally from the repo root:

```bash
python3 -m unittest discover -s tests
```

Bootstrap a Mac clone:

```bash
scripts/bootstrap_mac.sh
```

Safe mutation commands:

```bash
PYTHONPATH=src python3 -m work_codex.cli task-add --workspace . --title "Follow up" --company nrg_bloom --priority P1 --due 2026-03-10 --notes "Call back"
PYTHONPATH=src python3 -m work_codex.cli task-update --workspace . --id 15 --status in_progress --append-note "Called and left voicemail"
PYTHONPATH=src python3 -m work_codex.cli pipeline-upsert --workspace . --name "Oando" --company nrg_bloom --set stage=proposal --set next_action_date=2026-03-10
PYTHONPATH=src python3 -m work_codex.cli funding-upsert --workspace . --name "CanExport SMEs" --company nrg_bloom --set status=applying
PYTHONPATH=src python3 -m work_codex.cli memory-append --workspace . --json '{"type":"entity","name":"Example","entityType":"note"}'
```

Mutations are written atomically, backed up under `.work_codex/backups/`, and logged to `.work_codex/audit.jsonl`.

## GitHub

This repo is ready to become a private GitHub repository. See `docs/github-setup.md`.

## Architecture

- Codex-native architecture: `docs/codex-native.md`
- Portability notes: `docs/portability.md`
- TON operating procedure: `docs/ton-daily-operating-procedure.md`
- Claude/Codex exchange spec: `docs/claude-codex-exchange-spec.md`
