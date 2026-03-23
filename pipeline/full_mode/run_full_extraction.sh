#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
ONTOCAST_BIN="$(command -v ontocast 2>/dev/null || true)"
PYTHON_BIN="python3"

if [[ -z "${ONTOCAST_BIN}" ]]; then
  echo "OntoCast CLI not found. Activate the Conda environment first:" >&2
  echo "  conda activate ontologies" >&2
  exit 1
fi
CONFIG_FILE="${SCRIPT_DIR}/ontocast_full_config.env"
OUTPUT_DIR="${SCRIPT_DIR}/test_output"
INPUT_DIR="${OUTPUT_DIR}/input"
LOG_FILE="${OUTPUT_DIR}/run.log"
DEFAULT_HEAD_CHUNKS=2
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

if [[ ! -x "${ONTOCAST_BIN}" ]]; then
  echo "OntoCast CLI not found at: ${ONTOCAST_BIN}" >&2
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
rm -f "${OUTPUT_DIR}"/*.ttl "${OUTPUT_DIR}"/*.json "${OUTPUT_DIR}"/*.log "${INPUT_DIR}"/*
ln -sf "$(cd -- "$(dirname -- "${PDF_PATH}")" && pwd)/$(basename -- "${PDF_PATH}")" "${INPUT_DIR}/$(basename -- "${PDF_PATH}")"
: > "${LOG_FILE}"

echo "Running OntoCast full-mode extraction"
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

shopt -s nullglob
ontology_outputs=("${OUTPUT_DIR}"/ontology_*.ttl)
facts_outputs=("${OUTPUT_DIR}"/facts_*.ttl)
shopt -u nullglob

if (( ${#ontology_outputs[@]} == 0 )); then
  echo "No evolved ontology TTL found in ${OUTPUT_DIR}" >&2
  exit 1
fi
if (( ${#facts_outputs[@]} == 0 )); then
  echo "No facts TTL found in ${OUTPUT_DIR}" >&2
  exit 1
fi

echo ""
echo "Full-mode extraction completed"
printf '  ontology: %s\n' "${ontology_outputs[@]}"
printf '  facts:    %s\n' "${facts_outputs[@]}"
