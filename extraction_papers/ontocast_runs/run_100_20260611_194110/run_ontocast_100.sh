#!/usr/bin/env bash
set -uo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../../.." && pwd)"
RUN_DIR="extraction_papers/ontocast_runs/run_100_20260611_194110"
CONFIG_FILE="${RUN_DIR}/ontocast_100_config.env"
INPUT_DIR="${RUN_DIR}/input"
OUTPUT_DIR="${RUN_DIR}/output"
HEAD_CHUNKS="${ONTOCAST_HEAD_CHUNKS:-3}"
ONTOCAST_BIN="$(command -v ontocast 2>/dev/null || true)"
cd "${REPO_ROOT}" || exit 1
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
fi
export PYTHONUNBUFFERED=1 HF_HUB_DISABLE_SYMLINKS_WARNING=1
mkdir -p "${OUTPUT_DIR}"
pdf_count=$(find "${INPUT_DIR}" -maxdepth 1 -type f -iname '*.pdf' | wc -l)
echo "[$(date -Is)] Starting OntoCast fixed-mode extraction batch"
echo "  repo:    ${REPO_ROOT}"
echo "  config:  ${CONFIG_FILE}"
echo "  input:   ${INPUT_DIR} (${pdf_count} PDFs)"
echo "  output:  ${OUTPUT_DIR}"
echo "  chunks:  ${HEAD_CHUNKS}"
echo "  venv:    .venv"
echo "  llm:     Pi Codex subscription proxy (${SUBSCRIPTION_PROXY_BASE})"
if [[ -z "${ONTOCAST_BIN}" ]]; then
  echo "OntoCast CLI not found. Activate the repo venv and run the submodule setup first:" >&2
  echo "  source .venv/bin/activate" >&2
  echo "  bash scripts/setup_submodules.sh" >&2
  exit 1
fi
set +e
"${ONTOCAST_BIN}" \
  --env-file "${CONFIG_FILE}" \
  --input-path "${INPUT_DIR}" \
  --head-chunks "${HEAD_CHUNKS}"
status=$?
set -e
echo "[$(date -Is)] OntoCast batch finished with status ${status}"
exit "${status}"
