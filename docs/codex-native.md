# Codex-Native Architecture

## Core principle

This repository is not a Claude workspace with some Python attached.

It is a Codex-native agent system whose canonical root is the `Work` workspace itself:
- `shared/` is the operational state layer
- `knowledge/` is the durable memory layer
- `nrg-bloom/`, `coldstorm/`, and `personal/` are domain workspaces
- `src/work_codex/` is the runtime and orchestration layer

## What Claude becomes

The `.claude/` directory is legacy compatibility and reference material.

It may still contain useful prompts, skills, and historical workflows, but it is not the system root and should not define the architecture going forward.

Codex should treat `.claude/` as:
- optional adapter material
- migration input
- historical context

Not as:
- canonical runtime logic
- canonical state model
- required execution environment

## What Codex owns

Codex owns:
- the runtime
- the state transitions
- the validation rules
- the litigation matter model
- the future scheduler, APIs, and services

## Portability target

The portability target is:
- clone repo on another computer
- run `scripts/bootstrap_mac.sh`
- pass `doctor`
- continue work from the same canonical state

That means machine-specific auth and secrets must remain outside the core runtime contract.

## Build direction

1. Move more workflows from prompt text into code.
2. Keep domain knowledge in the workspace.
3. Keep mutable operational state in structured files.
4. Keep adapters and machine-specific integrations isolated.
5. Make every critical agent behavior inspectable, testable, and portable.
