# Work Codex

Work Codex is the Codex-owned evolution of Makir's agent workspace.

The original repository already contains valuable operating data:
- task, goal, funding, and pipeline state in YAML
- durable memory in JSONL
- company and project context in Markdown
- Claude-oriented workflows and skills

This version starts turning that workspace into software.

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
python3 -m work_codex.cli litigation-status --workspace .
python3 -m work_codex.cli litigation-update --workspace . --set phase=filing_strategy
```

What it does now:
- checks the required workspace files exist and load cleanly
- reports overdue, due-soon, and blocked tasks
- reports at-risk OKRs
- reports overdue next actions in pipeline and funding
- updates tasks, pipeline, funding, and memory through audited CLI commands
- loads and validates the TON litigation matter from the live case folder
- supports safe updates to litigation posture and settlement tracker state

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
