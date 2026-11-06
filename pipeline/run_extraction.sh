#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
ONTOCAST_BIN="$(command -v ontocast 2>/dev/null || true)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
CONFIG_FILE="${SCRIPT_DIR}/ontocast_config.env"
OUTPUT_DIR="${SCRIPT_DIR}/test_output"
INPUT_DIR="${OUTPUT_DIR}/input"
LOG_FILE="${OUTPUT_DIR}/run.log"
# Complete-document processing is the default. Set a positive second argument or
# ONTOCAST_HEAD_CHUNKS only for an explicitly labelled development run.
HEAD_CHUNKS="${ONTOCAST_HEAD_CHUNKS:-}"

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <pdf-path> [head-chunks]" >&2
  exit 1
fi

PDF_PATH="$1"
if [[ $# -eq 2 ]]; then
  HEAD_CHUNKS="$2"
fi
if [[ -n "${HEAD_CHUNKS}" && ! "${HEAD_CHUNKS}" =~ ^[1-9][0-9]*$ ]]; then
  echo "head-chunks must be a positive integer when supplied" >&2
  exit 2
fi

if [[ ! -f "${PDF_PATH}" ]]; then
  echo "Input PDF not found: ${PDF_PATH}" >&2
  exit 1
fi

if [[ -z "${ONTOCAST_BIN}" ]]; then
  echo "OntoCast CLI not found. Activate the repo venv and run the submodule setup first:" >&2
  echo "  source .venv/bin/activate" >&2
  echo "  bash scripts/setup_submodules.sh" >&2
  exit 1
fi

if [[ -f "${REPO_ROOT}/.env" ]]; then
  set -a
  source "${REPO_ROOT}/.env"
  set +a
fi

SUBSCRIPTION_PROXY_BASE="${LLM_BASE_URL:-http://127.0.0.1:8977/v1}"
"${PYTHON_BIN}" "${SCRIPT_DIR}/subscription_proxy.py" --base-url "${SUBSCRIPTION_PROXY_BASE}"
# Stock OntoCast requires a key value. This is not a real key; the proxy uses OAuth.
export LLM_PROVIDER=openai LLM_API_KEY=subscription-proxy
export LLM_BASE_URL="${SUBSCRIPTION_PROXY_BASE}" ONTOLOGY_CRITIC_PASSES=0

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
if [[ -n "${HEAD_CHUNKS}" ]]; then
  echo "  chunks: first ${HEAD_CHUNKS} (development limit)"
else
  echo "  chunks: complete document"
fi
echo "  llm:    Pi Codex subscription proxy (${SUBSCRIPTION_PROXY_BASE})"

ontocast_args=(
  --env-file "${CONFIG_FILE}"
  process --input-path "${INPUT_DIR}"
  --output-dir "${OUTPUT_DIR}"
  --keep-provenance --exclude-sections ""
)
if [[ -n "${HEAD_CHUNKS}" ]]; then
  ontocast_args+=(--head-chunks "${HEAD_CHUNKS}")
fi
(
  cd "${REPO_ROOT}"
  "${ONTOCAST_BIN}" "${ontocast_args[@]}"
) 2>&1 | tee -a "${LOG_FILE}"
