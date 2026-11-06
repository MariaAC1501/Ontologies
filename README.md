# Benchmarking LLM capabilities for ontology development and case extraction from predictive maintenance literature: A comparison of OPMAD and OntoCast

This repo contains an experimental comparison of the capabilities of humans (OPMAD authors) and large language models (LLMs) inferenced via OntoCast, for the task of ontology development and case extraction from predictive maintenance literature.

## Pipeline

0. Convert OPMAD and its bundled dependencies to Turtle with `scripts/convert_opmad.py` ([details and OntoCast usage](ontologies/opmad-ontocast/README.md)). Define comparison criteria.
1. Extract cases from papers using OntoCast in facts-only (no ontology evolution) mode. The exact extraction instruction used is:

> Extract every predictive maintenance case reported in this paper and all case-related facts expressible using the supplied ontology.

## Run extraction

`scripts/run_opmad.py` requires an explicit selection. `--papers` accepts exact
source IDs from `papers/opmad_sources.csv`, DOIs, or PDF filenames, separated by
spaces. Repeated selections run only once. Unknown selections or missing PDFs
stop the script before extraction starts.

Start the subscription proxy in one terminal:

```sh
node --env-file=scripts/ontocast-subscription.env scripts/subscription-proxy.mjs
```

In another terminal, preview one paper without making model calls or writing files:

```sh
.venv/bin/python scripts/run_opmad.py --papers OPMAD-S001 --output-dir out/pilot --dry-run
```

Run that paper, then inspect its results before choosing a larger selection:

```sh
.venv/bin/python scripts/run_opmad.py --papers OPMAD-S001 --output-dir out/pilot

# A specific subset.
.venv/bin/python scripts/run_opmad.py --papers OPMAD-S001 OPMAD-S003 --output-dir out/subset

# All downloaded papers in the source index, only when ready.
.venv/bin/python scripts/run_opmad.py --all --output-dir out/full
```

The runner uses the instruction above, facts-only mode, and the fixed OPMAD
ontology. It keeps provenance, disables web search, and runs one paper at a time
with one model call in flight. It reports sources without local PDFs when using
`--all`. For sources without a DOI, name their PDFs `<source_id>.pdf`.

Use `--env-file PATH` for other LLM settings. Shell settings override the file;
the runner always pins facts-only mode, OPMAD context, web search off, and serial
execution. When changing the subscription model, restart the proxy with the
same model selected.

Each run needs a new output directory. The script stops at the first failed
paper or missing facts file and keeps any outputs already written. It does not
compare the results automatically.

### Saved outputs

- `selection.json`: the full extraction instruction, effective LLM provider and
  model, configured generation settings, ontology SHA-256, selected papers, and
  commands. This records the planned run, not a claim that every paper finished.
  API keys and endpoint URLs are not included in this record.
- `<source_id>/*.facts.ttl`: extracted facts with provenance links.
- `<source_id>/*.units.jsonl`: source text chunks for checking the facts.
- `<source_id>/*.run.json`: OntoCast's per-paper settings, model, and token usage.
- `<source_id>/*.facts.validation.json`: validation findings, when available.
