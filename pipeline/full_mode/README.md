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

The run script looks for `ontocast` in this order:
1. `ONTOCAST_BIN` environment variable (if set)
2. `ontocast` on PATH (e.g., from an activated Conda environment)
3. Local venv at `pipeline/full_mode/.venv/bin/ontocast`

**Recommended**: use the Conda environment built by `scripts/create_conda_env.sh`.

- `OPENAI_API_KEY` is loaded from the repo-root `.env`
- Model: `gpt-4o` (configurable in `ontocast_full_config.env`)
- Default chunk limit: `--head-chunks 2` (to control API costs)

## Installed-package patches applied before the run

The runner applies the previously known local installed-package patches needed for OntoCast evaluation:

1. `ontology_prefix` fresh-ontology prompt fix
2. oxigraph deepcopy hardening in parallel worker paths / `RDFGraph.__deepcopy__`
3. SPARQL generation hardening for tuple-valued RDF-star triple-terms
4. critic / retry hardening
5. `skip_ontology_critique` support patch (kept available even though full mode does not enable it)

No new OntoCast source patch beyond that existing local patch set was required for this issue.

## Command run

```bash
bash pipeline/full_mode/run_full_extraction.sh example_paper.pdf 2
```

## Recorded result

The full-mode run completed and wrote both ontology and facts output:

- `pipeline/full_mode/test_output/ontology_brick_1.0.1.ttl`
- `pipeline/full_mode/test_output/facts_5cc89b5bfaf6.ttl`
- `pipeline/full_mode/test_output/run.log`

The run still showed salvage / fallback behavior, but it did **not** crash:

- ontology bootstrap did not yield a usable seed ontology
- parallel ontology map salvaged output from `2/2` non-converged unit loops
- normalization reported that no base ontology was available and continued with merged aggregated ontology output
- parallel facts map salvaged output from `2/2` non-converged unit loops

Key log lines are in `pipeline/full_mode/test_output/run.log`.

## Output validation notes

The output files exist and are non-empty.

Because OntoCast serializes RDF-star / Turtle-star provenance (for `rdf:reifies <<(...)>>` statements), stock `rdflib` Turtle parsing in this environment does not accept the emitted syntax. Validation with `pyoxigraph` succeeded:

- `ontology_brick_1.0.1.ttl`: 157 quads
- `facts_5cc89b5bfaf6.ttl`: 163 quads

So the deliverable files are present, but they remain RDF-star flavored outputs rather than plain Turtle consumable by vanilla `rdflib` parsing.

## Runtime issues observed

### 1. Missing `sentence-transformers`

The first full-mode attempt failed during clustering with:

```text
Entity clustering requires the sentence-transformers package.
```

Fix applied locally for the venv:

```bash
source pipeline/full_mode/.venv/bin/activate
pip install sentence-transformers
```

### 2. Missing `docling`

The run still logs:

```text
Could not import DocumentConverter: No module named 'docling'
```

This did **not** block the recorded run, but it remains a runtime warning.

## Regression check

The fixed-mode regression test still passed after this work:

```bash
bash pipeline/tests/test_regression.sh
```

## Assessment against issue criteria

- [x] Full OntoCast run completes without crashes on `example_paper.pdf`
- [x] Output includes both an evolved ontology TTL and facts TTL
- [x] Fixed-mode pipeline regression test still passes
- [x] Full-mode output is isolated under `pipeline/full_mode/test_output/`
- [x] Existing local patch set documented / referenced

## Remaining quality caveat

This is a **successful but still fragile** full-mode run. It completed only with the known local installed-package hardening and still relied on salvage / fallback behavior rather than a cleanly converged ontology-bootstrap path.
