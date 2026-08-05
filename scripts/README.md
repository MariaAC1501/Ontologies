# Headless CBR usage

This document covers repository-owned wrappers around the vendored CBR project; it does not modify or replace upstream documentation.

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
Instead, `scripts/build_cbr.py` compiles upstream sources with the same encoding setting; `scripts/build_cbr.sh` is the Bash wrapper. The relevant `javac` flag is:

```bash
javac -encoding ISO-8859-1
```

That makes the build reproducible without modifying vendor code.

## Setup and local patches

Before building, initialize the complete local stack from an activated `.venv`:

```bash
bash scripts/setup_submodules.sh
```

```powershell
.\scripts\setup_submodules.ps1
```

This initializes the three submodules, applies the repository-owned idempotent patches, uses `uv` to install OntoCast and Diversity dependencies, registers Diversity-in-CBR, builds the CBR jar, and installs `ontologies-cbr` in the active environment. The patch inventory and update procedure are maintained in [`LOCAL_PATCHES.md`](LOCAL_PATCHES.md).

## Build

From the activated repo `.venv`, the cross-platform builder is `scripts/build_cbr.py`:

```bash
python scripts/build_cbr.py
```

On Bash, the existing wrapper calls the same builder:

```bash
bash scripts/build_cbr.sh
```

## Commands

On Bash, all commands can go through:

```bash
bash scripts/run_cbr.sh ...
```

The setup command also installs an equivalent `ontologies-cbr` launcher in the active environment. It is the recommended command in Windows PowerShell:

```powershell
ontologies-cbr help
ontologies-cbr query-one --number-of-cases 3
```

Both launchers use the vendored CBR `data/` directory by default. Override it with `--data-dir DIR` or the `ONTOLOGIES_CBR_DATA_DIR` environment variable. The Bash wrapper rebuilds the jar before every invocation; `ontologies-cbr` uses the most recently built jar, so rerun `python scripts/build_cbr.py` after changing `HeadlessCBR.java`.

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

### 5. Diversity-aware reranking

The CBR engine retrieves by similarity only. To integrate the vendored
`external/Diversity-Improvement-in-CBR` submodule, this repo adds a Python
post-processor that reranks CBR CSV outputs with an MMR-style relevance/diversity
trade-off. It reads the Diversity submodule taxonomy from `Methods2.py` and uses
solution dissimilarity over model approach, model type, models, and preprocessing.

Recommended workflow: ask CBR for a larger candidate pool, then rerank to the
final number of cases:

```bash
bash scripts/run_cbr.sh query-batch input_file.csv raw_results_
python scripts/diversify_cbr_results.py \
  --results "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/raw_results_*.csv" \
  --output-dir "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/diverse_results" \
  --top-k 5 \
  --lambda-relevance 0.75
```

The reranked files preserve the original CBR columns and add `cbr_rank`,
`cbr_score`, `diversity_penalty`, `diversity_score`, `rerank_score`, and
`rerank_method`.

The bundled `PredictMaint_myCBR.prj` contains the 263 cases from
`CleanedDATA V12-05-2021.csv`, which is therefore the default enrichment CSV
for diversity scoring. Use a different `--casebase-csv` only when it matches
the project file loaded by myCBR; otherwise retrieved references can have
incomplete solution signatures and biased dissimilarities.

### 6. Batch comparison over extracted papers

To compare plain top-5 CBR retrieval against a pool-15 MMR rerank for every
canonical `facts_*.ttl` artifact under `extraction_papers/ontocast_runs/*/output/`, run:

```bash
python scripts/compare_diversity_all_papers.py --query-year 2026
```

`--query-year` freezes the year supplied to the legacy publication-recency
similarity. Without it, the current system year is used. The comparison also
accepts `--casebase-csv`; its default matches the bundled 263-case project.
Use `--drop-default-synchronization` when the extraction bridge produced
`Unknown synchronization` only as a missing-value default; the option assigns
that field weight zero instead of treating the default as query evidence.

The script rebuilds CBR, uses one deterministic extracted case per facts file,
and writes the queries, raw CBR results, reranked results, per-query metrics,
`summary.json`, and `REPORT.md` to a timestamped `.build/diversity_comparison_*`
directory. It reports corpus coverage explicitly: it does **not** invoke
OntoCast or send PDFs without a facts artifact to an external LLM. Use
`--max-facts N` for a smoke test, or `--output-dir DIR` to choose the artifact
directory.

### 7. Single query without GUI

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
Task;w1;Case study type;w2;Case study;w3;Online/Offline;w4;Input for the model;w5;Input type;w6;Query Year;Number of cases to retrieve;Amalgamation function
```

`Query Year` is optional for backward compatibility; when omitted, the current
system year is used.

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

Current CBR status:
- CBR upstream source patches required: **none**
- local compatibility layer added: `tools/cbr/HeadlessCBR.java`
- local build/run scripts added:
  - `scripts/build_cbr.py`
  - `scripts/build_cbr.sh`
  - `scripts/run_cbr.sh`
  - `scripts/install_submodule_stack.py`

OntoCast and Diversity-in-CBR do require repository-owned local patches. Their exact inventory, idempotence behavior, and update procedure are documented in [`LOCAL_PATCHES.md`](LOCAL_PATCHES.md). If a future CBR upstream patch is required, add it to `scripts/apply_local_patches.py` rather than maintaining a manual edit inside the submodule.
