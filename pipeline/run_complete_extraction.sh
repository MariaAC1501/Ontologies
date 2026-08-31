#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [[ $# -lt 4 || $# -gt 5 ]]; then
  echo "Usage: $0 <fixed|evolved> <corpus-manifest.json> <corpus-id> <run-dir> [--prepare-only]" >&2
  exit 2
fi

condition="$1"
manifest="$2"
corpus_id="$3"
run_dir="$4"
extra=()
if [[ $# -eq 5 ]]; then
  if [[ "$5" != "--prepare-only" ]]; then
    echo "Unknown argument: $5" >&2
    exit 2
  fi
  extra+=("--prepare-only")
fi

cd "${REPO_ROOT}"
exec "${PYTHON_BIN}" -m pipeline.fulltext_run \
  --condition "${condition}" \
  --manifest "${manifest}" \
  --corpus-id "${corpus_id}" \
  --run-dir "${run_dir}" \
  "${extra[@]}"
