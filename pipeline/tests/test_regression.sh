#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
cd "$ROOT_DIR"

PYTHON_BIN=${PYTHON_BIN:-python3}
SEED_ONTOLOGY=${SEED_ONTOLOGY:-pipeline/seed_ontology/opmad_seed.ttl}
REFERENCE_CSV=${REFERENCE_CSV:-external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/CleanedDATA V21-07-2021.csv}
NUMBER_OF_CASES=${NUMBER_OF_CASES:-3}

shopt -s nullglob
FACTS_FIXTURES=(pipeline/test_output/facts_*.ttl)
shopt -u nullglob

TMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/ontologies-regression.XXXXXX")
CSV_OUTPUT="$TMP_DIR/extracted_cases.csv"
QUERY_META="$TMP_DIR/query_meta.json"
CBR_RAW_OUTPUT="$TMP_DIR/cbr_query_output.txt"
CBR_CSV_OUTPUT="$TMP_DIR/cbr_query_results.csv"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

fail() {
  echo "[FAIL] $1" >&2
  exit 1
}

pass() {
  echo "[PASS] $1"
}

step() {
  echo
  echo "==> $1"
}

[[ -f "$SEED_ONTOLOGY" ]] || fail "Missing seed ontology: $SEED_ONTOLOGY"
[[ -f "$REFERENCE_CSV" ]] || fail "Missing reference CSV: $REFERENCE_CSV"
(( ${#FACTS_FIXTURES[@]} > 0 )) || fail "No frozen facts fixtures found at pipeline/test_output/facts_*.ttl"

step "1/6 Validate seed ontology parses with rdflib"
"$PYTHON_BIN" - <<'PY' "$SEED_ONTOLOGY"
from pathlib import Path
import sys
from rdflib import Graph

path = Path(sys.argv[1])
graph = Graph()
graph.parse(path, format="turtle")
if len(graph) == 0:
    raise SystemExit(f"Parsed ontology is empty: {path}")
print(f"Parsed {path} with {len(graph)} triples")
PY
pass "Seed ontology parses"

step "2/6 Validate extraction schema against first row of reference CSV"
"$PYTHON_BIN" - <<'PY' "$REFERENCE_CSV"
import csv
import sys
from pipeline.extraction_schema import PredictiveMaintenanceCase

reference_csv = sys.argv[1]
expected_headers = list(PredictiveMaintenanceCase.CSV_HEADERS.values())
with open(reference_csv, "r", encoding="latin-1", newline="") as handle:
    reader = csv.DictReader(handle, delimiter=";")
    headers = reader.fieldnames or []
    first_row = next(reader, None)

if headers != expected_headers:
    raise SystemExit(
        "Reference CSV headers do not match extraction schema\n"
        f"Expected: {expected_headers}\n"
        f"Actual:   {headers}"
    )
if first_row is None:
    raise SystemExit("Reference CSV has no data rows")
case = PredictiveMaintenanceCase.from_csv_row(first_row)
print(f"Validated reference row for study: {case.study_title}")
PY
pass "Extraction schema matches reference CSV"

step "3/6 Run facts_to_csv.py on frozen facts fixtures"
"$PYTHON_BIN" pipeline/facts_to_csv.py \
  --ontology "$SEED_ONTOLOGY" \
  --output "$CSV_OUTPUT" \
  --facts "${FACTS_FIXTURES[@]}"
[[ -f "$CSV_OUTPUT" ]] || fail "facts_to_csv.py did not produce output: $CSV_OUTPUT"
pass "facts_to_csv.py generated CSV from ${#FACTS_FIXTURES[@]} fixture(s)"

step "4/6 Validate output CSV structure and schema compliance"
"$PYTHON_BIN" - <<'PY' "$CSV_OUTPUT" "$REFERENCE_CSV" "$QUERY_META"
import csv
import json
import sys
from pipeline.extraction_schema import PredictiveMaintenanceCase

csv_output, reference_csv, query_meta = sys.argv[1:4]
expected_headers = list(PredictiveMaintenanceCase.CSV_HEADERS.values())
with open(csv_output, "r", encoding="utf-8", newline="") as handle:
    reader = csv.DictReader(handle, delimiter=";")
    headers = reader.fieldnames or []
    rows = list(reader)

if headers != expected_headers:
    raise SystemExit(
        "Extracted CSV headers do not match schema\n"
        f"Expected: {expected_headers}\n"
        f"Actual:   {headers}"
    )
if len(headers) != 19:
    raise SystemExit(f"Expected 19 headers, found {len(headers)}")
if not rows:
    raise SystemExit("Extracted CSV has no data rows")

validated = [PredictiveMaintenanceCase.from_csv_row(row) for row in rows]
first = validated[0]

with open(reference_csv, "r", encoding="latin-1", newline="") as handle:
    reference_rows = list(csv.DictReader(handle, delimiter=";"))

allowed_tasks = {r["Task"].strip() for r in reference_rows if r.get("Task", "").strip()}
allowed_case_types = {r["Case study type"].strip() for r in reference_rows if r.get("Case study type", "").strip()}
allowed_case_studies = {r["Case study"].strip() for r in reference_rows if r.get("Case study", "").strip()}
allowed_input_modes = {r["Input for the model"].strip() for r in reference_rows if r.get("Input for the model", "").strip()}

actual = {
    "task": first.task,
    "case_study_type": first.case_study_type,
    "case_study": first.case_study,
    "input_for_model": first.input_for_model,
    "input_type": ", ".join(first.input_types),
    "row_count": len(validated),
}
query = dict(actual)
notes = []

if query["task"] not in allowed_tasks:
    if "future state forecast" in query["task"].lower():
        query["task"] = "One step future state forecast"
        notes.append("Mapped task to closest CBR vocabulary: One step future state forecast")
    else:
        query["task"] = ""
        notes.append("Dropped task from query because it is not present in the CBR vocabulary")

if query["case_study_type"] not in allowed_case_types:
    query["case_study_type"] = ""
    notes.append("Dropped case-study-type from query because it is not present in the existing case base")

if query["case_study"] not in allowed_case_studies:
    query["case_study"] = ""
    notes.append("Dropped case-study from query because it is not present in the existing case base")

if query["input_for_model"] not in allowed_input_modes:
    input_mapping = {"Data Collection": "Signals"}
    mapped = input_mapping.get(query["input_for_model"], "")
    if mapped:
        query["input_for_model"] = mapped
        notes.append(f"Mapped input-for-model to closest CBR vocabulary: {mapped}")
    else:
        query["input_for_model"] = ""
        notes.append("Dropped input-for-model from query because it is not present in the existing case base")

payload = {
    "actual": actual,
    "query": query,
    "notes": notes,
}
with open(query_meta, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2)
print(json.dumps(payload, indent=2))
PY
pass "Extracted CSV has 19-column header and schema-valid row(s)"

step "5/6 Run CBR query-one with extracted parameters"
TASK=$("$PYTHON_BIN" - <<'PY' "$QUERY_META"
import json, sys
meta = json.load(open(sys.argv[1], encoding='utf-8'))
print(meta['query']['task'])
PY
)
CASE_STUDY_TYPE=$("$PYTHON_BIN" - <<'PY' "$QUERY_META"
import json, sys
meta = json.load(open(sys.argv[1], encoding='utf-8'))
print(meta['query']['case_study_type'])
PY
)
CASE_STUDY=$("$PYTHON_BIN" - <<'PY' "$QUERY_META"
import json, sys
meta = json.load(open(sys.argv[1], encoding='utf-8'))
print(meta['query']['case_study'])
PY
)
INPUT_FOR_MODEL=$("$PYTHON_BIN" - <<'PY' "$QUERY_META"
import json, sys
meta = json.load(open(sys.argv[1], encoding='utf-8'))
print(meta['query']['input_for_model'])
PY
)
INPUT_TYPE=$("$PYTHON_BIN" - <<'PY' "$QUERY_META"
import json, sys
meta = json.load(open(sys.argv[1], encoding='utf-8'))
print(meta['query']['input_type'])
PY
)

QUERY_CMD=(bash scripts/run_cbr.sh query-one --number-of-cases "$NUMBER_OF_CASES")
[[ -n "$TASK" ]] && QUERY_CMD+=(--task "$TASK")
[[ -n "$CASE_STUDY_TYPE" ]] && QUERY_CMD+=(--case-study-type "$CASE_STUDY_TYPE")
[[ -n "$CASE_STUDY" ]] && QUERY_CMD+=(--case-study "$CASE_STUDY")
[[ -n "$INPUT_FOR_MODEL" ]] && QUERY_CMD+=(--input-for-model "$INPUT_FOR_MODEL")
[[ -n "$INPUT_TYPE" ]] && QUERY_CMD+=(--input-type "$INPUT_TYPE")

printf 'Running: '
printf '%q ' "${QUERY_CMD[@]}"
printf '\n'
"${QUERY_CMD[@]}" >"$CBR_RAW_OUTPUT" 2>&1 || {
  cat "$CBR_RAW_OUTPUT" >&2
  fail "CBR query failed"
}
pass "CBR query completed"

step "6/6 Verify CBR returns results"
awk 'BEGIN{capture=0} /^Reference;Sim;/{capture=1} capture{print}' "$CBR_RAW_OUTPUT" > "$CBR_CSV_OUTPUT"
[[ -s "$CBR_CSV_OUTPUT" ]] || {
  cat "$CBR_RAW_OUTPUT" >&2
  fail "Unable to capture structured CBR output"
}

RESULT_LINES=$(wc -l < "$CBR_CSV_OUTPUT" | tr -d ' ')
(( RESULT_LINES >= 2 )) || {
  cat "$CBR_CSV_OUTPUT" >&2
  fail "CBR query returned no result rows"
}
pass "CBR returned $((RESULT_LINES - 1)) result row(s)"

echo
echo "Regression test passed"
echo "- Facts fixtures: ${#FACTS_FIXTURES[@]}"
echo "- Temporary output dir: $TMP_DIR"
