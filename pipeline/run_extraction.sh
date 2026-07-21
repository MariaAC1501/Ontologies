#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
ONTOCAST_BIN="$(command -v ontocast 2>/dev/null || true)"
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

if [[ -n "${OPENAI_API_KEY:-}" || -n "${LLM_API_KEY:-}" ]]; then
  echo "Direct OpenAI API keys are disabled for this workflow." >&2
  echo "Use the local Pi Codex subscription proxy instead: node tools/pi_codex_openai_proxy.mjs" >&2
  exit 1
fi

SUBSCRIPTION_PROXY_BASE="${LLM_BASE_URL:-http://127.0.0.1:8977/v1}"
SUBSCRIPTION_PROXY_HEALTH="${SUBSCRIPTION_PROXY_BASE%/}"
SUBSCRIPTION_PROXY_HEALTH="${SUBSCRIPTION_PROXY_HEALTH%/v1}/health"
if command -v curl >/dev/null 2>&1; then
  if ! curl -fsS --max-time 5 "${SUBSCRIPTION_PROXY_HEALTH}" >/dev/null; then
    echo "Subscription proxy is not reachable at ${SUBSCRIPTION_PROXY_HEALTH}." >&2
    echo "Start it with: node tools/pi_codex_openai_proxy.mjs" >&2
    exit 1
  fi
else
  echo "Warning: curl not found; skipping subscription proxy health check for ${SUBSCRIPTION_PROXY_HEALTH}" >&2
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
echo "  llm:    Pi Codex subscription proxy (${SUBSCRIPTION_PROXY_BASE})"

(
  cd "${REPO_ROOT}"
  "${ONTOCAST_BIN}" \
    --env-file "${CONFIG_FILE}" \
    --input-path "${INPUT_DIR}" \
    --head-chunks "${HEAD_CHUNKS}"
) 2>&1 | tee -a "${LOG_FILE}"
