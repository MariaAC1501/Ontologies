#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
cd "$ROOT_DIR"

PYTHON_BIN=${PYTHON_BIN:-$ROOT_DIR/.tmp-ontocast-test/bin/python3}
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN=${PYTHON_BIN_FALLBACK:-python3}
fi

FACTS_PATH=${FACTS_PATH:-pipeline/test_output/facts_5cc89b5bfaf6.ttl}
ONTOLOGY_PATH=${ONTOLOGY_PATH:-pipeline/seed_ontology/opmad_seed.ttl}
CSV_OUTPUT=${CSV_OUTPUT:-pipeline/test_output/extracted_cases.csv}
QUERY_META=${QUERY_META:-pipeline/test_output/e2e_query_meta.json}
CBR_RAW_OUTPUT=${CBR_RAW_OUTPUT:-pipeline/test_output/cbr_query_output.txt}
CBR_CSV_OUTPUT=${CBR_CSV_OUTPUT:-pipeline/test_output/cbr_query_results.csv}
REFERENCE_CSV=${REFERENCE_CSV:-external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/CleanedDATA V21-07-2021.csv}
NUMBER_OF_CASES=${NUMBER_OF_CASES:-3}

mkdir -p "$(dirname "$CSV_OUTPUT")"
mkdir -p "$(dirname "$CBR_RAW_OUTPUT")"

if [[ ! -f "$FACTS_PATH" ]]; then
  echo "Missing facts file: $FACTS_PATH" >&2
  exit 1
fi

if [[ ! -f "$REFERENCE_CSV" ]]; then
  echo "Missing reference CSV: $REFERENCE_CSV" >&2
  exit 1
fi

echo "[1/4] Rebuilding extracted CSV from existing OntoCast facts"
"$PYTHON_BIN" pipeline/facts_to_csv.py \
  --facts "$FACTS_PATH" \
  --ontology "$ONTOLOGY_PATH" \
  --output "$CSV_OUTPUT"

echo "[2/4] Validating CSV structure and deriving CBR query parameters"
"$PYTHON_BIN" - <<'PY' "$CSV_OUTPUT" "$REFERENCE_CSV" "$QUERY_META" "$NUMBER_OF_CASES"
import csv
import json
import sys
from pathlib import Path

csv_output = Path(sys.argv[1])
reference_csv = Path(sys.argv[2])
query_meta = Path(sys.argv[3])
number_of_cases = int(sys.argv[4])

with csv_output.open("r", encoding="utf-8", newline="") as handle:
    extracted_rows = list(csv.DictReader(handle, delimiter=";"))
if not extracted_rows:
    raise SystemExit("Extracted CSV has no case rows")

with reference_csv.open("r", encoding="latin-1", newline="") as handle:
    reference_reader = csv.DictReader(handle, delimiter=";")
    reference_headers = reference_reader.fieldnames or []
    reference_rows = list(reference_reader)

extracted_headers = list(extracted_rows[0].keys())
if extracted_headers != reference_headers:
    raise SystemExit(
        "CSV header mismatch\n"
        f"Extracted: {extracted_headers}\n"
        f"Reference: {reference_headers}"
    )

row = extracted_rows[0]

allowed_tasks = {r["Task"].strip() for r in reference_rows if r.get("Task", "").strip()}
allowed_case_types = {r["Case study type"].strip() for r in reference_rows if r.get("Case study type", "").strip()}
allowed_case_studies = {r["Case study"].strip() for r in reference_rows if r.get("Case study", "").strip()}
allowed_input_modes = {r["Input for the model"].strip() for r in reference_rows if r.get("Input for the model", "").strip()}

actual = {
    "task": row["Task"].strip(),
    "case_study_type": row["Case study type"].strip(),
    "case_study": row["Case study"].strip(),
    "input_for_model": row["Input for the model"].strip(),
    "input_type": row["Input type"].strip(),
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
    notes.append(
        f"Dropped case-study-type '{query['case_study_type']}' from the query because it is not present in the existing case base"
    )
    query["case_study_type"] = ""

if query["case_study"] not in allowed_case_studies:
    notes.append(
        f"Dropped case-study '{query['case_study']}' from the query because it is not present in the existing case base"
    )
    query["case_study"] = ""

if query["input_for_model"] not in allowed_input_modes:
    input_mapping = {
        "Data Collection": "Signals",
    }
    mapped = input_mapping.get(query["input_for_model"], "")
    if mapped:
        query["input_for_model"] = mapped
        notes.append(f"Mapped input-for-model to closest CBR vocabulary: {mapped}")
    else:
        notes.append(
            f"Dropped input-for-model '{query['input_for_model']}' from the query because it is not present in the existing case base"
        )
        query["input_for_model"] = ""

query["number_of_cases"] = str(number_of_cases)

payload = {
    "csv_output": str(csv_output),
    "reference_csv": str(reference_csv),
    "row_count": len(extracted_rows),
    "actual": actual,
    "query": query,
    "notes": notes,
}
query_meta.write_text(json.dumps(payload, indent=2), encoding="utf-8")
print(json.dumps(payload, indent=2))
PY

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
if [[ -n "$TASK" ]]; then
  QUERY_CMD+=(--task "$TASK")
fi
if [[ -n "$CASE_STUDY_TYPE" ]]; then
  QUERY_CMD+=(--case-study-type "$CASE_STUDY_TYPE")
fi
if [[ -n "$CASE_STUDY" ]]; then
  QUERY_CMD+=(--case-study "$CASE_STUDY")
fi
if [[ -n "$INPUT_FOR_MODEL" ]]; then
  QUERY_CMD+=(--input-for-model "$INPUT_FOR_MODEL")
fi
if [[ -n "$INPUT_TYPE" ]]; then
  QUERY_CMD+=(--input-type "$INPUT_TYPE")
fi

echo "[3/4] Running headless CBR query"
printf 'Command: '
printf '%q ' "${QUERY_CMD[@]}"
printf '\n'
"${QUERY_CMD[@]}" >"$CBR_RAW_OUTPUT" 2>&1

awk 'BEGIN{capture=0} /^Reference;Sim;/{capture=1} capture{print}' "$CBR_RAW_OUTPUT" > "$CBR_CSV_OUTPUT"

if [[ ! -s "$CBR_CSV_OUTPUT" ]]; then
  echo "Failed to capture structured CBR output: $CBR_CSV_OUTPUT" >&2
  echo "Raw output saved at: $CBR_RAW_OUTPUT" >&2
  exit 1
fi

RESULT_LINES=$(wc -l < "$CBR_CSV_OUTPUT" | tr -d ' ')
if (( RESULT_LINES < 2 )); then
  echo "CBR query returned no case rows" >&2
  cat "$CBR_CSV_OUTPUT" >&2
  exit 1
fi

echo "[4/4] Success"
echo "- Extracted CSV: $CSV_OUTPUT"
echo "- Query metadata: $QUERY_META"
echo "- Raw CBR output: $CBR_RAW_OUTPUT"
echo "- Parsed CBR results: $CBR_CSV_OUTPUT"
echo "- Result rows: $((RESULT_LINES - 1))"
