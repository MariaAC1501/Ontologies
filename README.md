# Ontology Extraction for Predictive Maintenance CBR

This repo combines:
- **OntoCast** as a constrained extractor for papers relevant to predictive-maintenance CBR
- **headless Java CBR tooling** for querying the predictive-maintenance case base

## Current project direction

The target system in this repo is the existing predictive-maintenance CBR stack in `external/CBR-Ontology-For-Predictive-Maintenance/`, documented in `Code-Guide.md`.

We are **not** currently trying to make OntoCast's full ontology-development feature suite the centerpiece of this project. For this use case, the main goal is narrower:
- use OntoCast only for the extraction functionality we actually need
- keep extraction aligned to a **fixed ontology / fixed vocabulary** suitable for the CBR workflow
- avoid depending on ontology bootstrap, ontology critique loops, and open-ended ontology evolution as core requirements

A later comparison between extraction against a fixed ontology and extraction against an evolved ontology could still be interesting, but it is explicitly **deferred** until the constrained workflow is stable.

## Repository layout

- `external/CBR-Ontology-For-Predictive-Maintenance/` — upstream Java CBR project
- `tools/cbr/HeadlessCBR.java` — relocatable CLI adapter for CBR
- `pipeline/` — integrated extraction pipeline (schema, seed ontology, bridge, config)
- `scripts/build_cbr.sh` — local jar build
- `scripts/run_cbr.sh` — local jar runner
- `conda/recipes/ontologies-cbr/` — Conda recipe for the packaged CBR CLI
- `conda/recipes/ontocast/` — Conda recipe for OntoCast (with local patches)
- `conda/recipes/ontologies-pipeline/` — Conda recipe for the extraction pipeline
- `conda/recipes/ontologies-stack/` — meta-package that installs all three
- `scripts/build_conda_packages.sh` / `scripts/build_conda_packages.ps1` — build local Conda packages
- `scripts/create_conda_env.sh` / `scripts/create_conda_env.ps1` — create an env from the local package channel
- `.github/workflows/conda-matrix.yml` — CI matrix build/test workflow

## Clone

Clone with submodules so the vendored CBR source is available:

```bash
git clone --recurse-submodules <repo-url>
cd Ontologies
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

## Conda-first setup

This is the recommended setup for colleagues because it installs the Python and Java parts together.
The Conda workflow in this repo is now validated in CI on macOS, Linux, and Windows.

### 1. Install Conda

Miniforge works well.

#### macOS / Linux

```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
source "$HOME/miniforge3/etc/profile.d/conda.sh"
conda activate base
```

#### Windows PowerShell

Install Miniforge, then open a new PowerShell and run:

```powershell
conda activate base
```

If Miniforge is installed in a non-default location, set `CONDA_ROOT` before using the helper scripts.

### 2. Create the build environment

```bash
conda env create -f environment.yml
conda activate ontologies
```

On Windows PowerShell:

```powershell
conda env create -f environment.yml
conda activate ontologies
```

### 3. Build the local Conda packages

#### macOS / Linux

```bash
bash scripts/build_conda_packages.sh
```

#### Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_conda_packages.ps1
```

This builds:
- `ontologies-cbr`
- `ontocast`
- `ontologies-pipeline`
- `ontologies-stack`

and indexes your local Conda channel at:
- `~/miniforge3/conda-bld` on macOS/Linux
- `%USERPROFILE%\miniforge3\conda-bld` or your configured `CONDA_ROOT` on Windows

### 4. Create a runnable stack environment

#### macOS / Linux

```bash
bash scripts/create_conda_env.sh
```

Or choose your own prefix:

```bash
bash scripts/create_conda_env.sh /path/to/env
```

#### Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File scripts/create_conda_env.ps1
```

Or choose your own prefix:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/create_conda_env.ps1 C:\path\to\env
```

Default env location:
- macOS/Linux: `~/miniforge3/envs/ontologies`
- Windows: `miniforge3\envs\ontologies` under `CONDA_ROOT`

### 5. Verify the installed tools

After creating the environment, activate it and run:

```bash
conda activate ontologies
ontologies-cbr help
ontocast --help
```

On Windows PowerShell:

```powershell
conda activate ontologies
ontologies-cbr help
python -c "import ontocast; import ontocast.cli.serve"
```

If you created the environment at a custom prefix instead of the default name, use `conda run`:

```bash
conda run -p /path/to/env ontologies-cbr help
conda run -p /path/to/env ontocast --help
```

## Supported Conda packaging targets

Current OntoCast recipe support in this repo:
- `osx-arm64`
- `linux-64`
- `win-64`

Current CBR recipe support:
- `noarch` package with a Java runtime dependency

Notes:
- the OntoCast recipe vendors a few PyPI-only wheels for each supported platform
- Linux support in this repo currently targets `linux-64`
- Windows support in this repo currently targets `win-64`

## CI matrix builds

This repo includes a CI workflow at:
- `.github/workflows/conda-matrix.yml`

It builds and smoke-tests the Conda packaging flow on:
- macOS
- Linux
- Windows

Each CI job:
1. checks out the repo with submodules
2. installs Miniforge
3. installs build dependencies from `environment.yml`
4. builds `ontologies-cbr`, `ontocast`, `ontologies-pipeline`, and `ontologies-stack`
5. creates a fresh environment from the locally built channel
6. runs smoke tests for the installed tools

Current status:
- the Conda matrix build/test workflow is passing on macOS, Linux, and Windows

## Conda package details

| Package | Type | Contents |
|---------|------|----------|
| `ontologies-cbr` | `noarch` | Headless CBR jar, upstream jars, ontology/data assets, `ontologies-cbr` CLI wrapper |
| `ontocast` | per-platform | OntoCast Python package with vendored PyPI wheels and local patches |
| `ontologies-pipeline` | `noarch` | Extraction schema, seed ontology, facts→CSV bridge, config, run scripts |
| `ontologies-stack` | `noarch` | Meta-package installing all three above |

The `ontologies-cbr` CLI resolves its data directory in this order:
1. `--data-dir DIR`
2. `ONTOLOGIES_CBR_DATA_DIR`
3. repository-local default during development
4. `$CONDA_PREFIX/share/ontologies-cbr/data`

## Local non-Conda CBR workflow

If you only want to build and run the headless Java CBR tooling from the repo:

### Build

```bash
bash scripts/build_cbr.sh
```

### Run

```bash
bash scripts/run_cbr.sh help
```

Example query:

```bash
bash scripts/run_cbr.sh query-one \
  --task "Remaining useful life estimation" \
  --case-study-type "Rotary machines" \
  --input-for-model "Time series" \
  --input-type "Temperature, Fluid Pressure, Spinning speed" \
  --number-of-cases 1
```

## Extraction pipeline

The integrated pipeline extracts structured data from predictive-maintenance papers and feeds it into the CBR system.

### Pipeline flow

```
PDF paper
  → OntoCast (fixed-ontology, facts-only mode)
  → RDF/Turtle facts (OPMAD-typed)
  → facts_to_csv.py
  → 19-column semicolon-delimited CSV
  → HeadlessCBR query
```

### Run extraction (local, requires OpenAI API key)

```bash
export OPENAI_API_KEY=sk-...
bash pipeline/run_extraction.sh your_paper.pdf
```

### Convert facts to CSV

```bash
python pipeline/facts_to_csv.py \
  --facts pipeline/test_output/facts_*.ttl \
  --ontology pipeline/seed_ontology/opmad_seed.ttl \
  --output extracted_cases.csv
```

### Query CBR with extracted parameters

```bash
bash scripts/run_cbr.sh query-one \
  --task "One step future state forecast" \
  --input-for-model "Signals" \
  --input-type "Pressure, Tension" \
  --number-of-cases 3
```

### Pipeline files

| File | Purpose |
|------|---------|
| `pipeline/extraction_schema.py` | Pydantic model mapping 19 CSV columns to OPMAD ontology IRIs |
| `pipeline/seed_ontology/opmad_seed.ttl` | Self-contained OPMAD seed ontology for fixed-ontology extraction |
| `pipeline/ontocast_config.env` | OntoCast configuration for constrained extraction mode |
| `pipeline/run_extraction.sh` | Wrapper script to run OntoCast on a PDF |
| `pipeline/facts_to_csv.py` | Converts RDF/Turtle facts to CBR-compatible CSV |
| `pipeline/SCHEMA_MAPPING.md` | Detailed documentation of the OPMAD field mapping |
| `pipeline/INTEGRATION_RESULTS.md` | End-to-end test results |

## Notes

- `ontocast` requires an OpenAI API key for extraction runs.
- In this repo, OntoCast is used as a **fixed-ontology extractor** for the CBR system, not for full ontology evolution.
- Starting the OntoCast server is a blocking command.
