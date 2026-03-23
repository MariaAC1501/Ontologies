#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
ONTOCAST_BIN="${ONTOCAST_BIN:-$(command -v ontocast 2>/dev/null || true)}"
CONFIG_FILE="${SCRIPT_DIR}/ontocast_config.env"
OUTPUT_DIR="${SCRIPT_DIR}/test_output"
INPUT_DIR="${OUTPUT_DIR}/input"
LOG_FILE="${OUTPUT_DIR}/run.log"
DEFAULT_HEAD_CHUNKS=3
HEAD_CHUNKS="${ONTOCAST_HEAD_CHUNKS:-${DEFAULT_HEAD_CHUNKS}}"

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <pdf-path> [head-chunks]" >&2
  exit 1
fi

PDF_PATH="$1"
if [[ $# -eq 2 ]]; then
  HEAD_CHUNKS="$2"
fi

if [[ ! -f "${PDF_PATH}" ]]; then
  echo "Input PDF not found: ${PDF_PATH}" >&2
  exit 1
fi

if [[ -z "${ONTOCAST_BIN}" || ! -x "${ONTOCAST_BIN}" ]]; then
  echo "OntoCast CLI not found. Install via Conda or set ONTOCAST_BIN." >&2
  exit 1
fi

if [[ ! -f "${REPO_ROOT}/.env" ]]; then
  echo "Repo root .env not found: ${REPO_ROOT}/.env" >&2
  exit 1
fi

set -a
source "${REPO_ROOT}/.env"
set +a

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "OPENAI_API_KEY is not set after loading ${REPO_ROOT}/.env" >&2
  exit 1
fi

mkdir -p "${OUTPUT_DIR}" "${INPUT_DIR}"
rm -f "${INPUT_DIR}"/*
ln -sf "$(cd -- "$(dirname -- "${PDF_PATH}")" && pwd)/$(basename -- "${PDF_PATH}")" "${INPUT_DIR}/$(basename -- "${PDF_PATH}")"
: > "${LOG_FILE}"

echo "Running OntoCast extraction"
echo "  config: ${CONFIG_FILE}"
echo "  input:  ${PDF_PATH}"
echo "  staged: ${INPUT_DIR}/$(basename -- "${PDF_PATH}")"
echo "  output: ${OUTPUT_DIR}"
echo "  log:    ${LOG_FILE}"
echo "  chunks: ${HEAD_CHUNKS}"

(
  cd "${REPO_ROOT}"
  export OPENAI_API_KEY
  "${ONTOCAST_BIN}" \
    --env-file "${CONFIG_FILE}" \
    --input-path "${INPUT_DIR}" \
    --head-chunks "${HEAD_CHUNKS}"
) 2>&1 | tee -a "${LOG_FILE}"
