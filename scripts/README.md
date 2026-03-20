# Headless CBR usage

This project vendors the Java CBR code as a git submodule at:

- `external/CBR-Ontology-For-Predictive-Maintenance`

## What I found

The upstream CBR repo does **not** have a native CLI entrypoint for retrieval.

It exposes these runnable classes:
- `User.CSVtoOntologyExec` — imports CSV into OWL
- `User.myCBRSetting` — rebuilds the myCBR `.prj` file and similarity functions
- `User.GUI2` — interactive Swing GUI for single-query retrieval
- `User.GUI3` — Swing GUI for batch retrieval from an input CSV

So the retrieval logic is already available headlessly in code, but upstream only wires it to Swing.

Specifically:
- `CBR.Recommender.solveOuery(...)` performs retrieval
- `CBR.Recommender.Export(...)` writes retrieval results to CSV
- `User.GUI3` is only a GUI wrapper around those two methods

## Headless approach used here

Instead of patching the upstream repo directly, this repository adds a small local adapter:

- `tools/cbr/HeadlessCBR.java`

This adapter:
- bootstraps `User.AppConfiguration` with the local data directory
- calls upstream classes directly
- provides headless commands for:
  - ontology rebuild from CSV
  - myCBR project preparation
  - batch query execution
  - single-query execution

## Upstream quirks handled reproducibly

### 1. Hard-coded Windows path in `User/AppConfiguration.java`
Upstream defaults to a Windows-specific path.

We do **not** patch the file in-place.
Instead, `HeadlessCBR.java` sets the `AppConfiguration` fields at runtime before invoking upstream code.

### 2. Source encoding
Several upstream `.java` files are encoded as `ISO-8859-1`.

We do **not** rewrite the upstream sources.
Instead, `scripts/build_cbr.sh` compiles upstream sources with:

```bash
javac -encoding ISO-8859-1
```

That makes the build reproducible without modifying vendor code.

## Build

```bash
bash scripts/build_cbr.sh
```

## Commands

All commands go through:

```bash
bash scripts/run_cbr.sh ...
```

### 1. Rebuild OWL from CSV

Uses upstream `User.CSVtoOntologyExec`.

```bash
bash scripts/run_cbr.sh csv-to-ontology \
  --csv "CleanedDATA V12-05-2021.csv" \
  --base-ont "OPMAD.owl" \
  --ont "OPMADdatabase.owl"
```

### 2. Rebuild myCBR project

Uses upstream `User.myCBRSetting`.

```bash
bash scripts/run_cbr.sh prepare-project \
  --csv "CleanedDATA V12-05-2021.csv" \
  --ont "OPMADdatabase.owl" \
  --project "PredictMaint_myCBR.prj"
```

### 3. Full rebuild

Runs both steps above in order.

```bash
bash scripts/run_cbr.sh rebuild \
  --csv "CleanedDATA V12-05-2021.csv" \
  --base-ont "OPMAD.owl" \
  --ont "OPMADdatabase.owl" \
  --project "PredictMaint_myCBR.prj"
```

### 4. Batch retrieval without GUI

This is the headless replacement for `User.GUI3`.

```bash
bash scripts/run_cbr.sh query-batch input_file.csv retrieval_results
```

That reads:
- `external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/input_file.csv`

and writes:
- `.../data/retrieval_results1.csv`
- `.../data/retrieval_results2.csv`
- etc.

You can also pass an absolute path for the input file.

### 5. Single query without GUI

This is a small CLI replacement for ad hoc `GUI2` usage.
It prints semicolon-separated results to stdout.

```bash
bash scripts/run_cbr.sh query-one \
  --task "Remaining useful life estimation" \
  --case-study-type "Rotary machines" \
  --input-for-model "Time series" \
  --input-type "Temperature, Fluid Pressure, Spinning speed" \
  --number-of-cases 3
```

Optional fields:
- `--task`
- `--case-study-type`
- `--case-study`
- `--online-offline`
- `--input-for-model`
- `--input-type`
- `--number-of-cases`
- `--amalgamation` (`euclidean` or `weighted sum`)
- `--w1` ... `--w6`

## Input CSV format for batch retrieval

The header must match upstream `GUI3` expectations:

```csv
Task;w1;Case study type;w2;Case study;w3;Online/Offline;w4;Input for the model;w5;Input type;w6;Number of cases to retrieve;Amalgamation function
```

A sample file already exists at:

- `external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/input_file.csv`

## Practical headless workflow

For a new case base:

```bash
# 1. Put your converted case CSV into the CBR data dir
# 2. Rebuild ontology and .prj
bash scripts/run_cbr.sh rebuild --csv "new_cases.csv"

# 3. Run batch retrievals
bash scripts/run_cbr.sh query-batch input_file.csv retrieval_results
```

## Patch policy

Current status:
- upstream source patches required: **none**
- local compatibility layer added: `tools/cbr/HeadlessCBR.java`
- local build/run scripts added:
  - `scripts/build_cbr.sh`
  - `scripts/run_cbr.sh`

If we later decide to patch the upstream submodule itself, those patches should be stored as patch files in this repository and applied from a script rather than edited manually.
