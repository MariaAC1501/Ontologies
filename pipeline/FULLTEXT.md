# Publication full-text processing

`pipeline.fulltext` prepares complete article text before a publication extraction run. It uses Docling and the OCR engines installed by OntoCast's `doc-processing` extra. It does not call an LLM.

## Final-run gate

Final preparation requires a JSON manifest matching [`fulltext_corpus.schema.json`](fulltext_corpus.schema.json). The selected record must have:

- `bibliographic_status: "verified"`;
- a stable corpus ID, title, DOI, year, and partition;
- a matching PDF SHA-256 checksum; and
- a manifest-level `partition_frozen: true` value.

The prepared `bibliographic-identity.json` remains the authority for corpus ID, title, DOI, and year. LLM output is not used to establish these fields.

## Conversion and OCR

The first pass uses Docling's standard PDF pipeline with:

- layout analysis and reading-order reconstruction;
- accurate table-structure extraction;
- OCR enabled through EasyOCR by default; and
- numbered page markers in the generated Markdown.

The quality gate checks page coverage, sparse pages, duplicated pages, truncation, and publisher-boilerplate dominance. A failed first pass is converted again with full-page OCR. The lower-ranked conversion is retained. A final quality failure is recorded and stops the publication extraction. It is an operational failure, not a corpus-selection rule.

Use `--ocr-engine rapidocr` or `--ocr-engine auto` when the frozen configuration selects another Docling engine.

## Prepared outputs

Each prepared document directory contains:

| File | Purpose |
|---|---|
| `document.md` | Complete page-delimited text with verified source metadata and structured tables. |
| `document.json` | OntoCast input containing the complete text. |
| `bibliographic-identity.json` | Manifest-controlled corpus ID, title, DOI, year, PDF hash, and licence metadata. |
| `source-map.json` | Exact character spans and hashes for page-linked sections, paragraphs, lists, images, and tables. It does not duplicate block text. |
| `quality.json` | Page, truncation, duplication, sparse-text, and boilerplate checks. |
| `processing.json` | Parser/OCR versions, settings, attempts, selected route, and output checksums/locations. |

OntoCast 0.8.2 runs without source patches. The runner passes `--keep-provenance`, retaining RDF 1.2 assertion-to-chunk links and the upstream `*.units.jsonl` source-text sidecar. Exact page/character/paragraph RDF fields from the former patch are no longer emitted. The prepared `source-map.json` still records exact text locations, but upstream does not automatically link those locations to each assertion.

`document.md` and `document.json` contain article text and belong in ignored local run directories. Do not release them unless the article licence permits redistribution. The source map retains locations and integrity hashes without repeating the text.

## Commands

Audit existing page-delimited Markdown without OCR or LLM calls:

```bash
python3 -m pipeline.fulltext audit \
  --input 'markdown/*/document.md' \
  --output /tmp/fulltext-audit.json
```

Prepare one verified document without extraction:

```bash
python3 -m pipeline.fulltext prepare \
  --manifest corpus/manifest.json \
  --corpus-id paper-0001 \
  --output-dir runs/paper-0001/fulltext
```

Prepare and run a fixed or evolved complete-document extraction. **Currently blocked after extraction by the upstream 0.8.2 in-memory provenance serialization bug** (see **T-RUN-10** in `TASKS.md`); `--prepare-only` remains usable:

```bash
bash pipeline/run_complete_extraction.sh \
  fixed corpus/manifest.json paper-0001 runs/paper-0001

bash pipeline/run_complete_extraction.sh \
  evolved corpus/manifest.json paper-0001 runs/paper-0001-evolved
```

Use the final optional `--prepare-only` argument to stop before any LLM request. PowerShell users can run `pipeline/run_complete_extraction.ps1` with the same four positional values and `-PrepareOnly`.

The publication runner uses `ontocast --env-file ... process --output-dir ... --keep-provenance --exclude-sections ""` and never sends `--head-chunks`. Default section exclusions are disabled, and bibliography text is retained. Both conditions set `ONTOLOGY_CRITIC_PASSES=0` and `FACTS_CRITIC_PASSES=1`. Stock OntoCast connects to the Pi Codex subscription proxy with the non-secret `LLM_API_KEY=subscription-proxy` placeholder, not a direct OpenAI API key.

The single-PDF development wrappers use the same settings. Supplying a positive second argument explicitly creates a limited development run. Output names are `*.facts.ttl` and `*.ontology.ttl`, with upstream validation and run-metadata sidecars.

## Tests

```bash
python3 -m unittest pipeline.tests.test_fulltext
```

The tests cover manifest gates, OCR rerouting, source-span round trips, quality failures, table preservation, complete-run command construction, and complete page coverage for two tracked long and multi-case challenge articles.
