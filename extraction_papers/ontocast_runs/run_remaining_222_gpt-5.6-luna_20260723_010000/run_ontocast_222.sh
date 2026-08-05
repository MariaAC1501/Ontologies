#!/usr/bin/env bash
set -uo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../../.." && pwd)"
RUN_DIR_REL="extraction_papers/ontocast_runs/$(basename "${SCRIPT_DIR}")"
CONFIG_FILE="${RUN_DIR_REL}/ontocast_222_config.env"
INPUT_DIR="${RUN_DIR_REL}/input"
OUTPUT_DIR="${RUN_DIR_REL}/output"
HEAD_CHUNKS="${ONTOCAST_HEAD_CHUNKS:-3}"
# Prefer the repo venv explicitly; do not accidentally use a global ontocast.
if [[ -x "${REPO_ROOT}/.venv/Scripts/ontocast.exe" ]]; then
  ONTOCAST_BIN="${REPO_ROOT}/.venv/Scripts/ontocast.exe"
elif [[ -x "${REPO_ROOT}/.venv/bin/ontocast" ]]; then
  ONTOCAST_BIN="${REPO_ROOT}/.venv/bin/ontocast"
else
  ONTOCAST_BIN="$(command -v ontocast 2>/dev/null || true)"
fi
cd "${REPO_ROOT}" || exit 1
export PYTHONUNBUFFERED=1 PYTHONUTF8=1 HF_HUB_DISABLE_SYMLINKS_WARNING=1
export ONTOCAST_QUOTA_RETRY_SECONDS="${ONTOCAST_QUOTA_RETRY_SECONDS:-900}"
# Put the venv scripts first for subprocesses.
export PATH="${REPO_ROOT}/.venv/Scripts:${REPO_ROOT}/.venv/bin:${PATH}"

# OntoCast expects an OpenAI Chat Completions endpoint. This localhost-only
# adapter translates those requests to Pi's OpenAI Codex OAuth subscription;
# it reads ~/.pi/agent/auth.json and never uses OPENAI_API_KEY.
PI_CODEX_PROXY_HOST="${PI_CODEX_PROXY_HOST:-127.0.0.1}"
PI_CODEX_PROXY_PORT="${PI_CODEX_PROXY_PORT:-8977}"
PI_CODEX_PROXY_URL="http://${PI_CODEX_PROXY_HOST}:${PI_CODEX_PROXY_PORT}/health"
PI_CODEX_PROXY_LOG="${RUN_DIR_REL}/pi_codex_proxy.log"
PI_CODEX_PROXY_PID="${RUN_DIR_REL}/pi_codex_proxy.pid"
PI_AI_COMPAT_PATH="${PI_AI_COMPAT_PATH:-C:/Users/maria/AppData/Local/nvm/v25.8.0/node_modules/@earendil-works/pi-coding-agent/node_modules/@earendil-works/pi-ai/dist/compat.js}"

proxy_healthy() {
  curl --silent --show-error --fail --connect-timeout 2 --max-time 5 "${PI_CODEX_PROXY_URL}" >/dev/null 2>&1
}

ensure_pi_codex_proxy() {
  if ! command -v curl >/dev/null 2>&1; then
    echo "curl is required to check the local Pi Codex proxy." >&2
    return 1
  fi
  if proxy_healthy; then
    return 0
  fi
  if ! command -v node >/dev/null 2>&1; then
    echo "Node.js is required for the local Pi Codex proxy." >&2
    return 1
  fi
  : > "${PI_CODEX_PROXY_LOG}"
  PI_AI_COMPAT_PATH="${PI_AI_COMPAT_PATH}"   PI_CODEX_PROXY_HOST="${PI_CODEX_PROXY_HOST}"   PI_CODEX_PROXY_PORT="${PI_CODEX_PROXY_PORT}"   nohup node "${REPO_ROOT}/tools/pi_codex_openai_proxy.mjs" >> "${PI_CODEX_PROXY_LOG}" 2>&1 &
  local proxy_pid=$!
  echo "${proxy_pid}" > "${PI_CODEX_PROXY_PID}"
  for _ in $(seq 1 30); do
    if proxy_healthy; then
      return 0
    fi
    sleep 1
  done
  echo "Pi Codex proxy did not become healthy; see ${PI_CODEX_PROXY_LOG}" >&2
  return 1
}

if ! ensure_pi_codex_proxy; then
  exit 1
fi
mkdir -p "${OUTPUT_DIR}"
pdf_count=$(find "${INPUT_DIR}" -maxdepth 1 -type f -iname '*.pdf' | wc -l | tr -d ' ')
echo "[$(date -Is)] Starting OntoCast fixed-mode extraction batch"
echo "  repo:    ${REPO_ROOT}"
echo "  config:  ${CONFIG_FILE}"
echo "  input:   ${INPUT_DIR} (${pdf_count} PDFs)"
echo "  output:  ${OUTPUT_DIR}"
echo "  chunks:  ${HEAD_CHUNKS}"
echo "  venv:    .venv"
echo "  binary:  ${ONTOCAST_BIN}"
echo "  auth:    Pi ChatGPT subscription via local Codex OAuth proxy"
echo "  quota retry delay: ${ONTOCAST_QUOTA_RETRY_SECONDS}s"
if [[ -z "${ONTOCAST_BIN}" || ! -x "${ONTOCAST_BIN}" ]]; then
  echo "OntoCast CLI not found. Activate/setup the repo venv first." >&2
  exit 1
fi
set +e
"${ONTOCAST_BIN}"   --env-file "${CONFIG_FILE}"   --input-path "${INPUT_DIR}"   --head-chunks "${HEAD_CHUNKS}"
status=$?
set -e
echo "[$(date -Is)] OntoCast batch finished with status ${status}"
exit "${status}"
