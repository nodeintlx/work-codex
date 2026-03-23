#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source_root="${repo_root}/codex-assets"
codex_home="${CODEX_HOME:-/home/dowsmasternode/.codex}"

mkdir -p "${codex_home}/skills" "${codex_home}/memories"

cp -a "${source_root}/skills/." "${codex_home}/skills/"
cp -a "${source_root}/memories/." "${codex_home}/memories/"

echo "Installed Codex assets into ${codex_home}"
