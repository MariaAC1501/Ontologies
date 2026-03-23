# Ontology Extraction for Predictive Maintenance CBR

This repo combines:
- **OntoCast** as a constrained extractor for papers relevant to predictive-maintenance CBR
- **headless Java CBR tooling** for querying the predictive-maintenance case base

## Two extraction modes

This repo supports two ways to extract knowledge from predictive-maintenance papers:

1. **Fixed OPMAD mode** — OntoCast extracts facts against the pre-defined OPMAD seed ontology, converts them to a 19-column CSV, and feeds them into the myCBR case-based reasoning system. This is the production path.

2. **Full evolution mode** — OntoCast bootstraps and evolves its own ontology from scratch, then extracts facts against it. Results are queried via SPARQL. This is useful for comparing what an unconstrained ontology discovers vs the fixed OPMAD vocabulary.

Both modes are fully functional and can be run on the same paper for side-by-side comparison.

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

> **Note on Windows:** If the submodule clone fails with a `Filename too long` error, your system is hitting the 260-character path limit. Tell Git to support long paths by running `git config --global core.longpaths true` in your terminal and then retry the clone.

## Conda-first setup

This is the recommended setup because it installs the Python and Java parts together.
The Conda workflow in this repo is validated in CI on macOS, Linux, and Windows.

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

Install Miniforge, then open a new PowerShell and configure it to allow Conda's initialization script:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
conda init powershell
```

Close the PowerShell window and open a new one. Your prompt should now begin with `(base)`, meaning Conda is active and ready to manage environments.

If Miniforge is installed in a non-default location, set `CONDA_ROOT` before using the helper scripts.

### 2. Update the base environment for building

The build dependencies (like `conda-build`) must be installed in your `base` Conda environment. This environment is only for building the Conda packages — it is separate from the runtime environment created in step 4.

```bash
conda env update -n base -f environment.yml
```

On Windows PowerShell:

```powershell
conda env update -n base -f environment.yml
```

### 3. Build the local Conda packages

#### macOS / Linux

```bash
bash scripts/build_conda_packages.sh
```

#### Windows PowerShell

```powershell
.\scripts\build_conda_packages.ps1
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
.\scripts\create_conda_env.ps1
```

Or choose your own prefix:

```powershell
.\scripts\create_conda_env.ps1 C:\path\to\env
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

### Prerequisites

Both extraction modes require:
- The runtime Conda environment created in step 4 of [Conda-first setup](#conda-first-setup), activated with `conda activate ontologies`
- An OpenAI API key in `.env` at the repo root:

```bash
cp .env.example .env
# Edit .env and set your actual API key
```

### Pipeline flow

```
PDF paper
  → OntoCast (fixed-ontology, facts-only mode)
  → RDF/Turtle facts (OPMAD-typed)
  → facts_to_csv.py
  → 19-column semicolon-delimited CSV
  → HeadlessCBR query
```

### Run extraction

#### macOS / Linux

```bash
conda activate ontologies
bash pipeline/run_extraction.sh your_paper.pdf
```

#### Windows PowerShell

```powershell
conda activate ontologies
pip install docling
.\pipeline\run_extraction.ps1 your_paper.pdf
```

> **Note on Windows:** 
> 1. `docling` is currently missing some dependencies on the Windows Conda-forge channel, so it must be installed manually via `pip` before running the extraction pipeline.
> 2. The `pytorch` CUDA builds on the Windows `conda-forge` channel are frequently broken and may fail to load DLLs (e.g., `shm.dll` throwing `WinError 127`). If this happens, cleanly reinstall the working CPU version using: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --upgrade --force-reinstall`
> 3. During its first extraction run, Hugging Face Hub will download models and attempt to cache them using symbolic links. By default, Windows standard users cannot create symlinks, causing a crash (`WinError 1314: El cliente no dispone de un privilegio requerido`). To bypass this one-time cache step, either run your PowerShell terminal as **Administrator** for the very first extraction, or permanently turn on "Developer Mode" in your Windows Settings.

The API key is read automatically from `.env` at the repo root. Output goes to `pipeline/test_output/`.

> **First run required.** The regression tests and comparison scripts need extraction output to exist. Run at least one extraction before running tests.

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

## Full OntoCast mode (evolved ontology)

A second extraction mode runs OntoCast with full ontology evolution — no seed ontology, no skipped critique — and queries results via SPARQL instead of CBR.

### Run full-mode extraction

#### macOS / Linux

```bash
conda activate ontologies
bash pipeline/full_mode/run_full_extraction.sh your_paper.pdf
```

#### Windows PowerShell

```powershell
conda activate ontologies
pip install docling
.\pipeline\full_mode\run_full_extraction.ps1 your_paper.pdf
```

> **Note on Windows:** Review the previous Windows note on `docling`, `pytorch`, and `Hugging Face Hub` symlinks if your extraction run crashes. All required OntoCast patches are applied at Conda build time (see issue #1 for the full list).

### Query the evolved ontology with SPARQL

```bash
# Summary statistics
python pipeline/full_mode/sparql_query.py \
  --ontology pipeline/full_mode/test_output/ontology_*.ttl \
  --facts pipeline/full_mode/test_output/facts_*.ttl \
  --preset summary

# List all discovered classes
python pipeline/full_mode/sparql_query.py \
  --ontology pipeline/full_mode/test_output/ontology_*.ttl \
  --facts pipeline/full_mode/test_output/facts_*.ttl \
  --preset classes

# Custom SPARQL query
python pipeline/full_mode/sparql_query.py \
  --ontology pipeline/full_mode/test_output/ontology_*.ttl \
  --facts pipeline/full_mode/test_output/facts_*.ttl \
  --query "SELECT ?s ?type WHERE { ?s a ?type } LIMIT 10"
```

### Compare both extraction modes

#### macOS / Linux

```bash
bash pipeline/comparison/run_comparison.sh
```

#### Windows PowerShell

```powershell
.\pipeline\comparison\run_comparison.ps1
```

Both write the report to `pipeline/comparison/COMPARISON_RESULTS.md`.

## Notes

- `ontocast` requires an OpenAI API key for extraction runs.
- The **fixed OPMAD** mode feeds into the CBR system via CSV. The **full evolution** mode is queried via SPARQL.
- Starting the OntoCast server is a blocking command.
