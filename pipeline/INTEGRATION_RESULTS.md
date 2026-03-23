# Integration results: PDF → OntoCast facts → CSV → CBR query

Issue: #10

## Scope

This integration check validates the pipeline using the existing OntoCast extraction output for `example_paper.pdf`.

Per issue guidance, this test **did not rerun OntoCast**. It reused the previously generated facts file:

- `pipeline/test_output/facts_5cc89b5bfaf6.ttl`

The automated test script is:

- `pipeline/tests/test_e2e.sh`

## Commands run

### 1. Regenerate CSV from existing facts

```bash
python pipeline/facts_to_csv.py \
  --facts pipeline/test_output/facts_5cc89b5bfaf6.ttl \
  --ontology pipeline/seed_ontology/opmad_seed.ttl \
  --output pipeline/test_output/extracted_cases.csv
```

### 2. Run the end-to-end test

```bash
pipeline/tests/test_e2e.sh
```

The test script then executed this headless CBR query:

```bash
bash scripts/run_cbr.sh query-one \
  --number-of-cases 3 \
  --task 'One step future state forecast' \
  --input-for-model 'Signals' \
  --input-type 'Pressure, Tension, Time Stamp, Width'
```

## Extracted case summary

Source CSV:

- `pipeline/test_output/extracted_cases.csv`

The regenerated CSV contained 1 extracted case row with these key values:

- **Study title:** Machine Learning for Predictive Maintenance of Industrial Machines using IoT Sensor Data
- **Task:** One step future state forecast
- **Case study:** Slitting Machine
- **Case study type:** Maintainable item
- **Input for the model:** Data Collection
- **Input type:** Pressure, Tension, Time Stamp, Width
- **Models:** ARIMA Model
- **Model type:** Data Analysis
- **Number of input variables:** 4

## CSV validation

The test script compared the generated CSV header against:

- `external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/CleanedDATA V21-07-2021.csv`

Result:

- Header structure matched the existing 19-column CBR CSV exactly
- Row count was `1`
- The generated row remained parseable as the expected semicolon-delimited format

## Query parameter adaptation

The extracted values do not fully match the vocabulary present in the existing CBR case base, so the test script applied the closest safe query it could derive from the extracted row:

- Kept **Task** as `One step future state forecast`
- Dropped **Case study type** `Maintainable item` because that value is not present in the existing case base
- Dropped **Case study** `Slitting Machine` because that value is not present in the existing case base
- Mapped **Input for the model** from `Data Collection` to the closest CBR value: `Signals`
- Kept **Input type** as `Pressure, Tension, Time Stamp, Width`

This derivation is recorded in:

- `pipeline/test_output/e2e_query_meta.json`

## CBR results

Saved outputs:

- Raw output: `pipeline/test_output/cbr_query_output.txt`
- Parsed results: `pipeline/test_output/cbr_query_results.csv`

Top 3 returned cases:

| Reference | Sim | Task | Case study type | Case study | Input for the model | Models |
|---|---:|---|---|---|---|---|
| 131 | 0.707 | One step future state forecast | Rotary machines | Cutter tool | Signals | Gaussian Process Regression (GPR) |
| 132 | 0.707 | One step future state forecast | Rotary machines | Cutter tool | Signals | v-support vector regression |
| 135 | 0.707 | One step future state forecast | Rotary machines | Cutter tool | Signals | Elman Neural Network Model |

Shared characteristics of the returned cases:

- Same task family: **One step future state forecast**
- Same query input mode after mapping: **Signals**
- Similar measured-variable flavor: tool-condition / physical sensor variables
- All three results come from the same 2017 cutter-tool forecasting study

## Assessment

### What worked

- Existing OntoCast facts were converted to CSV without crashes
- Facts→CSV produced a valid semicolon-delimited CSV with 1 case row
- The CSV column structure matched the established CBR dataset schema
- Headless CBR query returned 3 results successfully
- Outputs were saved under `pipeline/test_output/`

### Quality notes

- The extracted row is coherent and useful as a retrieval seed:
  - task extraction is strong
  - model extraction is strong (`ARIMA Model`)
  - input variables are plausible for the paper
- Retrieval quality is **reasonable but not exact** because the extracted ontology labels do not fully align with the legacy CBR vocabulary:
  - `Maintainable item` is too generic for the CBR case-base categories
  - `Data Collection` had to be mapped to `Signals`
  - `Slitting Machine` is not a named case already present in the case base
- Even with those vocabulary gaps, the CBR system still retrieved relevant one-step forecasting cases, which is sufficient to demonstrate end-to-end interoperability

## Acceptance criteria status

- [x] OntoCast extraction completes without crashes *(validated via existing facts output reused for this integration test)*
- [x] Facts→CSV produces a valid CSV with at least 1 case row
- [x] CBR query returns results when given extracted case parameters
- [x] Results documented in `pipeline/INTEGRATION_RESULTS.md`
- [ ] All patches documented in #1 *(no new OntoCast patch was required for this issue; if desired, note that explicitly in issue #1)*
