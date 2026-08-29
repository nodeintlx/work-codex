# Agent Configuration

## Legacy status

This `.claude/` directory is **legacy compatibility material**, not the canonical
runtime — see `../AGENTS.md`. Canonical state lives in `../shared/*.yaml`
(mutated via the `src/work_codex` CLI, not hand-edited) and litigation state
lives in `../nrg-bloom/litigation-ton/matter-status.yaml`. Skills/rules here
are kept for reference and for prompt-only workflows, but don't assume they
reflect current business state — check `git log -1` and run
`PYTHONPATH=src python3 -m work_codex.cli status --workspace ..` first.

## Context Loading
This directory contains agent definitions, skills, commands, rules, and hooks for Makir's AI Chief of Staff system.

## Dynamic Context
@../shared/goals.yaml
@../shared/tasks.yaml
@../shared/schedules.yaml

## Agent Guidelines
- Agents operate with scoped tool access — respect each agent's allowed-tools
- Skills are auto-discovered by description matching
- Commands are manually triggered via /slash-command
- Rules are always loaded with the same priority as CLAUDE.md

## Logs
- Audit logs are written to .claude/logs/audit.jsonl
- Review logs periodically for anomalies
