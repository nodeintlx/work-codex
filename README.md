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
```

What it does now:
- checks the required workspace files exist and load cleanly
- reports overdue, due-soon, and blocked tasks
- reports at-risk OKRs
- reports overdue next actions in pipeline and funding

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

## GitHub

This repo is ready to become a private GitHub repository. See `docs/github-setup.md`.
