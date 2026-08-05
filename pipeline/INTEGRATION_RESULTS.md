# Integration validation: OntoCast facts → CSV → CBR

## Purpose

This document describes the repository-owned integration check from extracted OntoCast facts to a 19-column CBR CSV and a headless CBR retrieval. It is a validation procedure, not evidence that every generated extraction is semantically correct.

## Prerequisites

- Complete the local setup in the root [`README.md`](../README.md).
- Activate the same Python environment used for setup.
- Ensure a fixed-mode facts file exists under `pipeline/test_output/`.
- Ensure the CBR submodule and its Java dependencies are initialized.

The generated files in `pipeline/test_output/` are working artifacts, not a versioned test fixture. A clean checkout must run fixed-mode extraction before the integration scripts can use them.

## Unit test suite

Run the deterministic Python unit tests from the repository root:

```bash
python -m unittest discover -s pipeline/tests -p "test_*.py"
```

These tests use committed minimal fixtures and temporary files; they do not require OntoCast-generated outputs or the Java CBR stack.

## Current validation procedure

1. Run fixed-mode extraction for a PDF:

   ```bash
   bash pipeline/run_extraction.sh your_paper.pdf
   ```

2. Select the facts file from that run and pass it explicitly to the end-to-end script. `test_e2e.sh` intentionally has no facts-file default; generated facts are integration artifacts, not versioned unit-test fixtures:

   ```bash
   FACTS_PATH=pipeline/test_output/facts_<run-id>.ttl \
     PYTHON_BIN=python \
     bash pipeline/tests/test_e2e.sh
   ```

   The script converts the facts with `pipeline/facts_to_csv.py`, verifies the 19-column semicolon-delimited header against the legacy CBR case base, derives a query that only uses compatible CBR vocabulary, runs `query-one`, and writes its CSV/log artifacts under `pipeline/test_output/`.

3. Run the broader integration regression check once one or more fixed-mode facts files exist:

   ```bash
   PYTHON_BIN=python bash pipeline/tests/test_regression.sh
   ```

   This test consumes every artifact matching `FACTS_GLOB` (default: `pipeline/test_output/facts_*.ttl`). Clear or archive older outputs, or set `FACTS_GLOB` to a concrete `facts_*.ttl` path/glob, when you need a single-paper result.

## Latest local check

On 2026-07-10, the UV-managed `.venv` passed the dependency import check and both integration scripts against the available `pipeline/test_output/facts_a0c666fbbd74.ttl` artifact:

- `test_e2e.sh` generated one CSV row and returned three CBR results.
- `test_regression.sh` parsed the seed ontology, validated the 19-column schema, converted the facts artifact, and returned three CBR results.
- The extracted query retained `Fault identification` and `Input type = Not reported`; it dropped unavailable case-study type, case-study, and input-mode values before querying the legacy case base.

This is a local interoperability check against generated data, not a semantic-quality assessment of the extraction.

## Vocabulary adaptation

The extracted labels can be broader or different from the legacy CBR case-base vocabulary. The integration scripts keep a compatible task when possible, drop unavailable case-study/case-study-type fields, and currently map `Data Collection` to `Signals`. Inspect `e2e_query_meta.json` or the temporary regression metadata to see the actual values, applied mapping, and dropped fields for a run.

A successful retrieval therefore proves technical interoperability; it does not prove an exact semantic match between the extracted paper and the returned legacy cases.

## Unit/integration boundary

The shell scripts in `pipeline/tests/` are integration checks. They consume generated fixed-mode artifacts from `pipeline/test_output/` and must not default to historical run identifiers such as `facts_5cc89b5bfaf6.ttl`.

Python unit tests do not depend on `pipeline/test_output/` generated artifacts. Converter/query/reranker unit coverage uses committed minimal fixtures under `pipeline/tests/fixtures/` or in-test temporary files.

## Historical result

A prior run against an IoT slitting-machine paper converted one facts file into one CSV row and retrieved three one-step forecasting cases after vocabulary adaptation. It reported a matching 19-column header and CBR similarities of `0.707` for the top three returned cases. Those files and their exact query metadata were generated artifacts, so this is retained as historical evidence only; rerun the procedure above to obtain current results.
