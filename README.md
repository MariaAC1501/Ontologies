# Ontology Extraction for Predictive Maintenance CBR

This repo combines:
- **OntoCast** as a constrained extractor for papers relevant to predictive-maintenance CBR
- **headless Java CBR tooling** for querying the predictive-maintenance case base

## Two extraction modes

This repo supports two ways to extract knowledge from predictive-maintenance papers:

1. **Fixed OPMAD mode** — OntoCast extracts facts against the pre-defined OPMAD seed ontology, converts them to a 19-column CSV, and feeds them into the myCBR case-based reasoning system. This is the production path.

2. **Full evolution mode** — OntoCast bootstraps and evolves its own ontology from scratch, then extracts facts against it. Results are queried via SPARQL. This is useful for comparing what an unconstrained ontology discovers vs the fixed OPMAD vocabulary.

Both modes can be run on the same paper for side-by-side comparison. Fixed OPMAD mode is the operational path; full evolution mode is experimental and its generated ontology should be reviewed before use.

## Repository layout

- `external/CBR-Ontology-For-Predictive-Maintenance/` — upstream Java CBR project submodule
- `external/Diversity-Improvement-in-CBR/` — upstream Diversity-in-CBR Python project submodule
- `external/ontocast/` — upstream OntoCast Python project submodule
- `tools/cbr/HeadlessCBR.java` — relocatable CLI adapter for CBR
- `pipeline/` — integrated extraction pipeline (schema, seed ontology, bridge, config)
- `requirements.txt` — UV-installed Python requirements for the pipeline and diversity tooling
- `scripts/setup_submodules.sh` / `scripts/setup_submodules.ps1` — initialize submodules, apply local patches, install editable Python submodules, and build CBR
- `scripts/build_cbr.py` / `scripts/build_cbr.sh` — local jar build
- `scripts/run_cbr.sh` — local jar runner
- `scripts/diversify_cbr_results.py` / `pipeline/diversity_rerank.py` — Diversity-in-CBR post-processor for reranking CBR result CSVs
- `scripts/compare_diversity_all_papers.py` — reproducible baseline-vs-diversity batch comparison for all available OntoCast facts under `extraction_papers/`
- `tools/pi_codex_openai_proxy.mjs` — local OpenAI-compatible proxy backed by the Pi ChatGPT Plus/Pro (Codex) subscription OAuth credential

## Documentation map

| Document | Scope |
|---|---|
| `README.md` | Installation and end-to-end workflows maintained by this repository |
| `scripts/README.md` | Headless CBR commands and diversity-aware reranking |
| `scripts/LOCAL_PATCHES.md` | Locally maintained, reproducible patches for vendored submodules |
| `DIVERSITY_COMPARISON_RESULTS.md` | Current batch comparison of plain and diversity-aware CBR retrieval |
| `pipeline/SCHEMA_MAPPING.md` | OPMAD/CSV field mapping and the facts-to-CSV bridge |
| `pipeline/full_mode/README.md` | Full ontology-evolution mode, outputs, and caveats |
| `pipeline/INTEGRATION_RESULTS.md` | Integration-validation procedure and historical evidence |
| `paper/experiments/README.md` | Gold evaluation, LLM baselines, and RQ2 schema/ontology generation workflow |

Documentation under `external/` belongs to its upstream projects and is deliberately not maintained here.

## Clone

Clone with submodules so all vendored sources are available:

```bash
git clone --recurse-submodules <repo-url>
cd Ontologies
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

> **Note on Windows:** If the submodule clone fails with a `Filename too long` error, your system is hitting the 260-character path limit. Tell Git to support long paths by running `git config --global core.longpaths true` in your terminal and then retry the clone.

## Prerequisites

- Git, with submodule support
- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/) on `PATH` for virtual-environment and dependency management
- A JDK that provides both `javac` and `jar` on `PATH` for the CBR build
- Bash for the `.sh` helpers on macOS/Linux (Git Bash is suitable on Windows); PowerShell equivalents are provided for setup and extraction

## UV environment setup (recommended)

The recommended local workflow keeps the three upstream projects checked out under `external/`, uses `uv` for every Python dependency installation, applies this repository's local compatibility patches, installs the Python submodule in editable mode, and builds the headless CBR jar locally.

### 1. Create and activate `.venv`

#### Bash

```bash
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install --python .venv/bin/python -r requirements.txt
```

#### Windows PowerShell

```powershell
uv venv --python 3.12 .venv
.\.venv\Scripts\Activate.ps1
uv pip install --python .\.venv\Scripts\python.exe -r requirements.txt
```

If PowerShell blocks activation scripts, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once and open a new terminal.

### 2. Initialize submodules, apply patches, and install/build the stack

Run this from the activated `.venv` so editable installs and generated entry points land in the local environment.

#### Bash

```bash
bash scripts/setup_submodules.sh
```

#### Windows PowerShell

```powershell
.\scripts\setup_submodules.ps1
```

The setup script runs `git submodule update --init --recursive`, applies local patches via `scripts/apply_local_patches.py`, installs `external/ontocast` in editable mode, registers `external/Diversity-Improvement-in-CBR` on the Python path, builds the local CBR jar, and installs the `ontologies-cbr` launcher in the active environment. Patch rationale and maintenance rules are in [`scripts/LOCAL_PATCHES.md`](scripts/LOCAL_PATCHES.md).

For a partial setup, pass `--help` to either setup wrapper. The available flags can skip submodule initialization, patching, a dependency, the CBR build, or UV dependency installation; use them only when the skipped component is already available.

### 3. Verify the stack

```bash
ontocast --help
python -c "import ontocast; import ontocast.cli.serve"
bash scripts/run_cbr.sh help
```

On Windows PowerShell, verify the launcher installed in `.venv\Scripts` instead:

```powershell
ontocast --help
ontologies-cbr help
```

## Local CBR workflow

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

> **Windows note:** There is no repo-local PowerShell version of `scripts/run_cbr.sh`. After `scripts/setup_submodules.ps1`, use the `ontologies-cbr` launcher installed in the active `.venv`; Git Bash can also run the Bash wrapper. Set `ONTOLOGIES_CBR_DATA_DIR` to use another CBR data directory.

## Extraction pipeline

The integrated pipeline extracts structured data from predictive-maintenance papers and feeds it into the CBR system.

### Prerequisites

Both extraction modes require:
- The `.venv` from [UV environment setup](#uv-environment-setup-recommended), activated in your shell
- A Pi/OpenAI Codex OAuth login backed by the ChatGPT Plus/Pro subscription. Direct OpenAI API keys (`OPENAI_API_KEY` or `LLM_API_KEY`) are intentionally rejected by the extraction wrappers.
- The local subscription proxy running in a separate terminal:

```bash
# Run Pi login first if the Codex OAuth credential is not present yet.
# In Pi, use /login and select ChatGPT Plus/Pro (Codex).
node tools/pi_codex_openai_proxy.mjs
```

`.env` is optional and is only used for non-secret proxy overrides such as `LLM_BASE_URL`, `PI_CODEX_PROXY_PORT`, or `PI_CODEX_MODEL`:

```bash
cp .env.example .env
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

This is the logical end-to-end flow. The extraction wrapper scripts run the **OntoCast extraction step only**; the RDF/Turtle → CSV conversion is a separate follow-up step performed by `pipeline/facts_to_csv.py`.

### Run extraction

#### macOS / Linux

```bash
source .venv/bin/activate
bash pipeline/run_extraction.sh your_paper.pdf
```

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
.\pipeline\run_extraction.ps1 your_paper.pdf
```

> **Note on Windows:**
> 1. The standard UV setup installs `docling`, `easyocr`, and `sentence-transformers` for PDF/document processing. If they were intentionally skipped, restore them with `uv pip install --python .\.venv\Scripts\python.exe docling easyocr sentence-transformers`.
> 2. If a PyTorch CUDA wheel fails to load DLLs (e.g., `shm.dll` throwing `WinError 127`), reinstall the CPU wheels with: `uv pip install --python .\.venv\Scripts\python.exe torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --upgrade --reinstall`
> 3. During its first extraction run, Hugging Face Hub will download models and attempt to cache them using symbolic links. By default, Windows standard users cannot create symlinks, causing a crash (`WinError 1314: El cliente no dispone de un privilegio requerido`). To bypass this one-time cache step, either run your PowerShell terminal as **Administrator** for the very first extraction, or permanently turn on "Developer Mode" in your Windows Settings.

The extraction scripts call OntoCast through the local subscription proxy configured by `LLM_BASE_URL` (default: `http://127.0.0.1:8977/v1`). Output goes to `pipeline/test_output/`. The fixed-mode runners process three chunks by default; pass a second positional `head-chunks` argument to override it. The Bash runner also accepts `ONTOCAST_HEAD_CHUNKS` when that argument is omitted.

The extraction scripts write OntoCast outputs such as `facts_*.ttl`, ontology files, and `run.log`. They do **not** automatically call `pipeline/facts_to_csv.py`, and they do **not** remove an existing `pipeline/test_output/extracted_cases.csv` or older fact/ontology outputs. Clear or archive that directory before a new isolated run; otherwise a later wildcard conversion can combine files from different papers. The Bash runner stages the input PDF as a symbolic link, whereas the PowerShell runner copies it.

> **First run required.** The regression tests and comparison scripts need extraction output to exist. Run at least one extraction before running tests.

### Convert facts to CSV

Use this script when you want to turn existing OntoCast facts into the 19-column CBR CSV format without rerunning extraction. This is also how the test scripts regenerate CSV output from facts fixtures when those generated files are available.

```bash
python pipeline/facts_to_csv.py \
  --facts pipeline/test_output/facts_*.ttl \
  --ontology pipeline/seed_ontology/opmad_seed.ttl \
  --output pipeline/test_output/extracted_cases.csv
```

The same command works in Windows PowerShell:

```powershell
python pipeline\facts_to_csv.py `
  --facts "pipeline\test_output\facts_*.ttl" `
  --ontology "pipeline\seed_ontology\opmad_seed.ttl" `
  --output "pipeline\test_output\extracted_cases.csv"
```

### Query CBR with extracted parameters

#### macOS / Linux

```bash
bash scripts/run_cbr.sh query-one \
  --task "One step future state forecast" \
  --input-for-model "Signals" \
  --input-type "Pressure, Tension" \
  --number-of-cases 3
```

#### Windows PowerShell

```powershell
ontologies-cbr query-one `
  --task "One step future state forecast" `
  --input-for-model "Signals" `
  --input-type "Pressure, Tension" `
  --number-of-cases 3
```

### Pipeline files

| File | Purpose |
|------|---------|
| `pipeline/extraction_schema.py` | Pydantic model mapping 19 CSV columns to OPMAD ontology IRIs |
| `pipeline/seed_ontology/opmad_seed.ttl` | Self-contained OPMAD seed ontology for fixed-ontology extraction |
| `pipeline/ontocast_config.env` | OntoCast configuration for constrained extraction mode |
| `pipeline/run_extraction.sh` | macOS/Linux wrapper script that runs OntoCast on a PDF |
| `pipeline/run_extraction.ps1` | Windows PowerShell wrapper script that runs OntoCast on a PDF |
| `pipeline/facts_to_csv.py` | Standalone bridge that converts existing RDF/Turtle facts to CBR-compatible CSV |
| `pipeline/SCHEMA_MAPPING.md` | Detailed documentation of the OPMAD field mapping |
| `pipeline/INTEGRATION_RESULTS.md` | End-to-end validation procedure and historical evidence |

### RQ2 LLM-generated schema/ontology flow

The paper experiment harness can generate an LLM-designed schema or ontology from `evidence.jsonl`, then use it as context for no-OntoCast JSON extraction:

```bash
python paper/experiments/generate_llm_schema_or_ontology.py \
  --evidence paper/experiments/llm_baselines/abstract/evidence.jsonl \
  --artifact schema_json \
  --dry-run \
  --model dry-run-model \
  --output-dir paper/experiments/llm_baselines/rq2_schema

python paper/experiments/run_llm_json_extraction.py \
  --evidence paper/experiments/llm_baselines/abstract/evidence.jsonl \
  --condition llm_schema \
  --schema-context paper/experiments/llm_baselines/rq2_schema/generated_schema.json \
  --dry-run \
  --model dry-run-model \
  --output paper/experiments/llm_baselines/abstract/llm_schema/predictions.jsonl
```

For the ontology arm, generate `--artifact ontology_ttl` and pass `--ontology .../generated_ontology.ttl` to `run_llm_json_extraction.py`. Omit `--dry-run` only for approved real API runs with `LLM_BASE_URL`, `LLM_API_KEY`, and `--model` configured. See `paper/experiments/README.md` for the full RQ2/RQ3/RQ4 experiment workflow.

## Full OntoCast mode (evolved ontology)

A second extraction mode runs OntoCast with full ontology evolution — no seed ontology and ontology critique enabled — and queries results via SPARQL instead of CBR. Its runners default to two chunks, clear prior TTL/JSON/log outputs before running, and verify that both `ontology_*.ttl` and `facts_*.ttl` were produced.

### Run full-mode extraction

#### macOS / Linux

```bash
source .venv/bin/activate
bash pipeline/full_mode/run_full_extraction.sh your_paper.pdf
```

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
uv pip install --python .\.venv\Scripts\python.exe docling easyocr sentence-transformers
.\pipeline\full_mode\run_full_extraction.ps1 your_paper.pdf
```

> **Note on Windows:** Review the previous Windows note on `docling`, `pytorch`, and `Hugging Face Hub` symlinks if your extraction run crashes. Required OntoCast patches are applied by `scripts/setup_submodules.*`.

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

- Extraction runs use the Pi Codex subscription proxy only; direct OpenAI API keys are not supported in this repository workflow.
- The **fixed OPMAD** mode feeds into the CBR system via CSV. The **full evolution** mode is queried via SPARQL.
- Starting the OntoCast server is a blocking command.
