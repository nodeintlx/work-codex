# Agent Exchange

This directory is an exchange layer for multi-agent cooperation.

Rules:
- Treat workspace YAML and runtime state as the source of truth.
- Use `handoff/` for machine-readable exports from Codex.
- Use `incoming/` for files dropped by another agent.
- Use `manifests/` for machine-readable instructions describing each incoming artifact.
- Do not edit case-state YAML directly from an external agent without an ingestion step.

