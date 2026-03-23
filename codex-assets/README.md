# Codex Assets

This folder vendors the custom Codex skills and memory needed to recreate the local agent setup on another machine.

## What is here

- `skills/`: custom Codex skills that should be copied into `$CODEX_HOME/skills`
- `memories/`: persisted case memory that should be copied into `$CODEX_HOME/memories`
- `scripts/install_codex_assets.sh`: install helper for restoring these assets into a local Codex home

## Restore

Run:

```bash
bash codex-assets/scripts/install_codex_assets.sh
```

That installs the vendored skills and memories into:

- `/home/dowsmasternode/.codex/skills`
- `/home/dowsmasternode/.codex/memories`

Adjust the script if the target machine uses a different Codex home.
