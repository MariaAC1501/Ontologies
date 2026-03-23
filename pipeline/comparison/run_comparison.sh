#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
cd "$REPO_ROOT"

PYTHON_BIN=${PYTHON_BIN:-python3}

FIXED_FACTS="pipeline/test_output/facts_5cc89b5bfaf6.ttl"
EVOLVED_FACTS="pipeline/full_mode/test_output/facts_5cc89b5bfaf6.ttl"
EVOLVED_ONTO="pipeline/full_mode/test_output/ontology_brick_1.0.1.ttl"
SEED_ONTO="pipeline/seed_ontology/opmad_seed.ttl"
OUTPUT="pipeline/comparison/COMPARISON_RESULTS.md"

for f in "$FIXED_FACTS" "$EVOLVED_FACTS" "$EVOLVED_ONTO" "$SEED_ONTO"; do
  if [[ ! -f "$f" ]]; then
    echo "Missing: $f" >&2
    echo "Run both extraction modes first." >&2
    exit 1
  fi
done

echo "Running side-by-side comparison..."
"$PYTHON_BIN" pipeline/comparison/compare.py \
  --fixed-facts "$FIXED_FACTS" \
  --evolved-facts "$EVOLVED_FACTS" \
  --evolved-ontology "$EVOLVED_ONTO" \
  --seed-ontology "$SEED_ONTO" \
  --output "$OUTPUT"

echo "Comparison report written to: $OUTPUT"
