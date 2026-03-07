# Portability

## Current status

The core runtime is portable across machines because:
- code is in Git
- critical YAML and Markdown state is in Git
- vendored YAML dependency is in Git
- bootstrap does not depend on a virtual environment

## What is portable now

- workspace data
- litigation runtime
- CLI commands
- tests
- vendored `ruamel.yaml`

## What remains machine-specific

- GitHub auth
- Gmail and browser integrations
- any local MCP configuration
- any secrets or tokens

## macOS workflow

```bash
git clone git@github.com:nodeintlx/work-codex.git
cd work-codex
scripts/bootstrap_mac.sh
```

## Runtime check

```bash
PYTHONPATH=src python3 -m work_codex.cli doctor --workspace .
```
