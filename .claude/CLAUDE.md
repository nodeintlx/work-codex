# Agent Configuration

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
