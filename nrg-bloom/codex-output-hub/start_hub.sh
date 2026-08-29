#!/bin/bash
set -euo pipefail

PORT=8771
ROOT="/home/dowsmasternode/repos/work-codex/nrg-bloom"
LOG="/tmp/nrg-bloom-codex-hub.log"

if ss -ltn "( sport = :$PORT )" 2>/dev/null | grep -q ":$PORT"; then
  exit 0
fi

nohup python3 -m http.server "$PORT" --directory "$ROOT" >"$LOG" 2>&1 &
