#!/usr/bin/env bash
set -uo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../../../../.." && pwd)"
cd "$REPO_ROOT" || exit 1
export PATH="$REPO_ROOT/.venv/Scripts:$PATH" PYTHONUNBUFFERED=1 PYTHONUTF8=1 HF_HUB_DISABLE_SYMLINKS_WARNING=1
"$REPO_ROOT/.venv/Scripts/ontocast.exe" \
  --env-file "${SCRIPT_DIR}/ontocast_config.env" \
  --input-path "${SCRIPT_DIR}/input" \
  --head-chunks 3
