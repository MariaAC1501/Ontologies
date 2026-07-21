# Full OntoCast mode run

Issue: #13

## Goal

Run OntoCast in full ontology-evolution mode against `example_paper.pdf` with:

- `RENDER_MODE=ontology_and_facts`
- ontology critique enabled
- no seed ontology directory
- dedicated output under `pipeline/full_mode/test_output/`

## Files

- Config: `pipeline/full_mode/ontocast_full_config.env`
- Runner: `pipeline/full_mode/run_full_extraction.sh`
- Output dir: `pipeline/full_mode/test_output/` *(gitignored)*

## Environment

Activate the repo `.venv` and ensure the submodule stack has been set up:

```bash
source ../../.venv/bin/activate
bash ../../scripts/setup_submodules.sh
```

From Windows PowerShell at the repo root:

```powershell
.\.venv\Scripts\Activate.ps1
.\scripts\setup_submodules.ps1
```

The run script uses `ontocast` from PATH and the local Pi Codex subscription proxy at `LLM_BASE_URL` (default: `http://127.0.0.1:8977/v1`). Direct OpenAI API keys are rejected.

Start the proxy in another terminal before running extraction:

```bash
node tools/pi_codex_openai_proxy.mjs
```

- Model sent to the OpenAI-compatible proxy: `gpt-5-mini` (the proxy can route to `PI_CODEX_MODEL`)
- Default chunk limit: `--head-chunks 2` (to control subscription usage)

## OntoCast patches

All required patches are applied by `scripts/setup_submodules.*` via `scripts/apply_local_patches.py`. The maintained patch inventory and update procedure are in [`../../scripts/LOCAL_PATCHES.md`](../../scripts/LOCAL_PATCHES.md).

Full mode deliberately does **not** set `SKIP_ONTOLOGY_CRITIQUE` or an ontology directory. In contrast, fixed mode supplies the OPMAD seed and skips ontology critique. The complete effective settings are in `ontocast_full_config.env` and `../ontocast_config.env`.

## Run and outputs

```bash
bash pipeline/full_mode/run_full_extraction.sh example_paper.pdf
```

Pass an optional second argument to set the chunk limit:

```bash
bash pipeline/full_mode/run_full_extraction.sh example_paper.pdf 2
```

The default is two chunks. On Bash, `ONTOCAST_HEAD_CHUNKS` supplies the default when the argument is omitted. The runners clear previous top-level `*.ttl`, `*.json`, and `*.log` files in `pipeline/full_mode/test_output/`, stage the PDF under `test_output/input/`, and then require at least one of each output:

- `pipeline/full_mode/test_output/ontology_*.ttl`
- `pipeline/full_mode/test_output/facts_*.ttl`
- `pipeline/full_mode/test_output/run.log`

OntoCast serializes RDF-star/Turtle-star provenance (`rdf:reifies <<(...)>>`). Stock `rdflib` does not parse that syntax directly. `pipeline/full_mode/sparql_query.py`, `pipeline/facts_to_csv.py`, and the comparison tool remove those provenance statements before their ordinary-Turtle processing; use an RDF-star-capable parser when provenance itself must be retained.

## Historical validation record

Previous validation produced a non-empty ontology and facts graph, but the named artifacts from that run are generated output and are not part of this checkout. Earlier reports referred to `ontology_brick_1.0.1.ttl` and `facts_5cc89b5bfaf6.ttl`; treat their counts and logs as historical evidence, not as the result of the current working tree. Run the command above before using the SPARQL examples or comparison workflow.

The earlier run completed with salvage/fallback behavior: bootstrap did not yield a usable seed ontology, parallel ontology and facts loops salvaged non-converged units, and normalization continued without a base ontology. A successful exit therefore demonstrates pipeline execution, not clean ontology convergence.

## Runtime issues observed

### 1. Missing `sentence-transformers`

The first full-mode attempt failed during clustering with:

```text
Entity clustering requires the sentence-transformers package.
```

Fix: ensure `sentence-transformers` is installed in the activated `.venv` with UV (it is included by the standard setup):

```bash
uv pip install --python ../../.venv/bin/python sentence-transformers
```

### 2. Missing `docling`

The run still logs:

```text
Could not import DocumentConverter: No module named 'docling'
```

This did **not** block the recorded run, but it remains a runtime warning.

## Validation and caveats

Run the fixed-mode regression only after a fixed-mode facts fixture exists:

```bash
bash pipeline/tests/test_regression.sh
```

`pipeline/tests/test_sparql_query.py` runs only when its expected full-mode fixture files are present; otherwise its tests are skipped. Generated outputs are intentionally isolated under `pipeline/full_mode/test_output/` and should not be committed as source documentation.

Full mode remains experimental. It can finish by salvaging non-converged units, so evaluate the produced ontology and facts for completeness and consistency before drawing research conclusions.
