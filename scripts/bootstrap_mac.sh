#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Work Codex macOS bootstrap"
echo "repo: $ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required"
  exit 1
fi

echo "python: $(python3 --version)"

cd "$ROOT"

echo "running doctor"
PYTHONPATH=src python3 -m work_codex.cli doctor --workspace .

echo "running tests"
PYTHONPATH=src python3 -m unittest discover -s tests

cat <<'EOF'

Bootstrap complete.

Recommended next steps on the Mac:
1. Configure git and GitHub auth.
2. Add machine-specific secrets outside git.
3. If you need Gmail/MCP integrations, create local config for this machine.
4. Use the Codex runtime as the primary interface, not the legacy .claude layer.
EOF
