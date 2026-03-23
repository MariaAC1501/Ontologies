#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
cd "$REPO_ROOT"

PYTHON_BIN=${PYTHON_BIN:-python3}

FIXED_FACTS_GLOB="pipeline/test_output/facts_*.ttl"
EVOLVED_FACTS_GLOB="pipeline/full_mode/test_output/facts_*.ttl"
EVOLVED_ONTO_GLOB="pipeline/full_mode/test_output/ontology_*.ttl"
SEED_ONTO="pipeline/seed_ontology/opmad_seed.ttl"
OUTPUT="pipeline/comparison/COMPARISON_RESULTS.md"

shopt -s nullglob
fixed_files=($FIXED_FACTS_GLOB)
evolved_fact_files=($EVOLVED_FACTS_GLOB)
evolved_onto_files=($EVOLVED_ONTO_GLOB)
shopt -u nullglob

if (( ${#fixed_files[@]} == 0 )); then
  echo "No fixed-mode facts found matching: $FIXED_FACTS_GLOB" >&2
  echo "Run the fixed-mode extraction first: bash pipeline/run_extraction.sh <pdf>" >&2
  exit 1
fi
if (( ${#evolved_fact_files[@]} == 0 )); then
  echo "No full-mode facts found matching: $EVOLVED_FACTS_GLOB" >&2
  echo "Run full-mode extraction first: bash pipeline/full_mode/run_full_extraction.sh <pdf>" >&2
  exit 1
fi
if [[ ! -f "$SEED_ONTO" ]]; then
  echo "Seed ontology not found: $SEED_ONTO" >&2
  exit 1
fi

echo "Running side-by-side comparison..."
"$PYTHON_BIN" pipeline/comparison/compare.py \
  --fixed-facts $FIXED_FACTS_GLOB \
  --evolved-facts $EVOLVED_FACTS_GLOB \
  --evolved-ontology $EVOLVED_ONTO_GLOB \
  --seed-ontology "$SEED_ONTO" \
  --output "$OUTPUT"

echo "Comparison report written to: $OUTPUT"
