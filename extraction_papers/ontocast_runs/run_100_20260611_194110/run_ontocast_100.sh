#!/usr/bin/env bash
set -uo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../../.." && pwd)"
RUN_DIR="extraction_papers/ontocast_runs/run_100_20260611_194110"
CONFIG_FILE="${RUN_DIR}/ontocast_100_config.env"
INPUT_DIR="${RUN_DIR}/input"
OUTPUT_DIR="${RUN_DIR}/output"
HEAD_CHUNKS="${ONTOCAST_HEAD_CHUNKS:-3}"
cd "${REPO_ROOT}" || exit 1
set -a
source "${REPO_ROOT}/.env"
set +a
if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "OPENAI_API_KEY is not set after loading ${REPO_ROOT}/.env" >&2
  exit 1
fi
export OPENAI_API_KEY PYTHONUNBUFFERED=1 HF_HUB_DISABLE_SYMLINKS_WARNING=1
mkdir -p "${OUTPUT_DIR}"
pdf_count=$(find "${INPUT_DIR}" -maxdepth 1 -type f -iname '*.pdf' | wc -l)
echo "[$(date -Is)] Starting OntoCast fixed-mode extraction batch"
echo "  repo:    ${REPO_ROOT}"
echo "  config:  ${CONFIG_FILE}"
echo "  input:   ${INPUT_DIR} (${pdf_count} PDFs)"
echo "  output:  ${OUTPUT_DIR}"
echo "  chunks:  ${HEAD_CHUNKS}"
echo "  conda:   ontologies"
set +e
conda run --no-capture-output -n ontologies ontocast \
  --env-file "${CONFIG_FILE}" \
  --input-path "${INPUT_DIR}" \
  --head-chunks "${HEAD_CHUNKS}"
status=$?
set -e
echo "[$(date -Is)] OntoCast batch finished with status ${status}"
exit "${status}"
