# Full OntoCast mode run

Issue: #13

## Goal

Run OntoCast in full ontology-evolution mode against `example_paper.pdf` with:

- `RENDER_MODE=ontology_and_facts`
- ontology critique disabled (`ONTOLOGY_CRITIC_PASSES=0`); facts critique enabled
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
node pipeline/tools/pi_codex_openai_proxy.mjs
```

- Default model: `gpt-5.6-luna` (override the actual Pi model with `PI_CODEX_MODEL`)
- Default document scope: every chunk in the converted article

## Stock OntoCast configuration

OntoCast is pinned to unmodified **0.8.2**. No OntoCast source patch is applied. The subscription proxy works with `LLM_BASE_URL` and the non-secret `LLM_API_KEY=subscription-proxy` placeholder; Pi's OAuth credential, not this placeholder, authenticates the subscription.

Both modes set `ONTOLOGY_CRITIC_PASSES=0` and `FACTS_CRITIC_PASSES=1`. Full mode has no seed ontology directory; fixed mode supplies the OPMAD profile. The complete settings are in `ontocast_full_config.env` and `../ontocast_config.env`. See [`../../scripts/LOCAL_PATCHES.md`](../../scripts/LOCAL_PATCHES.md).

## Run and outputs

**Known upstream blocker:** the 0.8.2 default in-memory store crashes while persisting RDF 1.2 provenance, before dumping outputs. The proxy connection is verified, but complete extraction needs an upstream fix or a validated alternative backend. See **T-RUN-10** in `TASKS.md`; no extra OntoCast patch is applied.

```bash
bash pipeline/full_mode/run_full_extraction.sh example_paper.pdf
```

Pass an optional positive second argument only for an explicitly limited development run:

```bash
bash pipeline/full_mode/run_full_extraction.sh example_paper.pdf 2
```

With no limit, the complete document is processed. On Bash, `ONTOCAST_HEAD_CHUNKS` can also set a development limit. The runners clear previous top-level `*.ttl`, `*.json`, `*.jsonl`, and `*.log` files in `pipeline/full_mode/test_output/`, stage the PDF under `test_output/input/`, and then require at least one of each output:

- `pipeline/full_mode/test_output/*.ontology.ttl`
- `pipeline/full_mode/test_output/*.facts.ttl`
- `pipeline/full_mode/test_output/run.log`

The runners invoke `ontocast --env-file ... process --output-dir ... --keep-provenance --exclude-sections ""`. They retain every section and bibliography text unless a development chunk limit is supplied. `--keep-provenance` retains RDF 1.2 statement-to-chunk links and a `*.units.jsonl` source-text sidecar. The former custom page/character/paragraph RDF fields are no longer emitted.

Stock `rdflib` does not parse RDF 1.2 triple terms directly. The SPARQL, legacy CSV, and comparison tools strip those statements; the strict review exporter preserves them.

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

This did **not** block the historical run, but publication preparation requires Docling and fails closed when it is unavailable. The standard repository requirements install Docling and EasyOCR.

## Publication full-text path

Use `pipeline/run_complete_extraction.*` for study runs. It verifies frozen bibliographic metadata and the PDF checksum, uses Docling's layout, table, and OCR pipeline, retries low-quality text with full-page OCR, and writes page-linked source maps before running full evolution. See [`../FULLTEXT.md`](../FULLTEXT.md).

## Validation and caveats

Run the fixed-mode regression only after a fixed-mode facts fixture exists:

```bash
bash pipeline/tests/test_regression.sh
```

`pipeline/tests/test_sparql_query.py` uses temporary fixtures and requires no generated extraction output. Generated outputs are intentionally isolated under `pipeline/full_mode/test_output/` and should not be committed as source documentation.

Full mode remains experimental. It can finish by salvaging non-converged units, so evaluate the produced ontology and facts for completeness and consistency before drawing research conclusions.
