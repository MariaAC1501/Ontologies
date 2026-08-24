# Strict review export

`pipeline/review_export.py` is the publication/review-oriented export path for
OntoCast facts. It is deliberately separate from `pipeline/facts_to_csv.py`.
The latter remains the legacy compatibility bridge for the 19-column CBR
loader and continues to supply schema-valid defaults.

## Usage

JSON Lines is the default and is recommended for batch review:

```bash
python pipeline/review_export.py \
  --facts 'pipeline/test_output/facts_*.ttl' \
  --output pipeline/test_output/review-records.jsonl
```

Use `--format json` (or an output name ending in `.json`) for one JSON array.
Every input TTL is read and parsed independently, and its records are appended
only after that graph's records have been constructed. The CLI exits `2` if
one or more inputs failed to decode or parse, but still writes an
`extraction_failure` record for each failed input so batch failures are
machine-visible.

## Record contract (`strict-review-export/1.0`)

The machine-readable JSON Schema is [`review_export.schema.json`](review_export.schema.json). Each JSON record carries:

- a stable content-derived `record_id` and `schema_version`;
- `source_document`, including the facts filename, path, SHA-256 document ID,
  parse status, and the number/handling boundary of RDF-star annotations;
- nullable `article_identity` and `case_identity` objects;
- `case_article_link`, whose `resolution` is `resolved`, `unresolved`, or
  `ambiguous` and which includes the RDF link evidence when resolved;
- the 19 review fields under `fields`; and
- non-normalized `supplementary_evidence`, currently design details and
  article keywords.

Every field has the same shape:

```json
{
  "status": "present",
  "value": 0,
  "raw_values": ["0"],
  "source_nodes": ["urn:example:failure-count"]
}
```

`value` is the normalized analytical value and is always `null` unless the
available RDF supports assignment. Lists remain JSON arrays and counts remain
JSON integers. `raw_values` and source IRIs retain the lexical evidence used in
normalization where practical.

### Status meanings

| Status | Meaning in this export |
|---|---|
| `present` | Linked RDF supplies a usable, non-conflicting value. Explicit numeric zero is present, not missing. |
| `not_reported` | A successfully parsed facts graph contains no RDF assertion for the field in this record context. This describes the extracted RDF, not a claim that the source paper omitted it. |
| `unclear` | Candidate evidence is ambiguous, conflicting, too broad, or not linked to this record; no candidate is selected. |
| `not_applicable` | The field cannot be evaluated for this record shape, for example article metadata on an orphan case. |
| `extraction_failure` | The document could not be parsed or an asserted value could not be normalized. |

## Strict normalization rules

The exporter does **not**:

- substitute publication year 2021;
- map a broad `Future_state_forecast` assertion to one-step forecasting;
- turn a missing variable/failure-mode count into zero;
- write `Not reported` strings into analytical values;
- treat every `Design_detail` as proof of preprocessing;
- derive model configuration (`Single model`/`Multi model`) from the count of
  models; or
- generate publication identifiers from RDF local names or filenames.

An explicit `Model_configuration`, explicit boolean preprocessing assertion,
or explicit typed count can be exported. Generic design details are retained
separately and may make preprocessing `unclear`, but are not converted to a
boolean. Model labels do not establish model approach.

## Document and case isolation

Graphs are never unioned. Within a graph, record scope is a bounded traversal
of domain relations and does not traverse author or provenance/chunk links.
A case is paired with an article only when the RDF directly connects them or
when the case and article explicitly refer to the same designated/about
resource. If no unique link exists, the exporter emits an unresolved or
ambiguous record rather than pairing by order or globally assigning entities.
One article may therefore occur on multiple case records when each link is
explicit. Unmatched articles are retained as unresolved article records.

## Current limitations and provenance boundary

- OPMAD does not itself provide all links needed to identify article-to-case,
  model-to-case, or field-to-case membership in arbitrary extraction output.
  Unlinked candidate entities are exposed as `unclear`, not guessed. Full
  multi-case extraction needs explicit case/provenance linkage upstream.
- Stock `rdflib` in this project does not parse OntoCast's RDF-star reification
  syntax. As in the compatibility bridge, annotations are removed before
  Turtle parsing. Unlike a silent drop, each record reports their count and
  handling, retains the original facts path and content digest, and leaves the
  source file untouched. Statement-level `prov:wasDerivedFrom` is not yet
  projected into fields; consumers needing chunk-level evidence must consult
  the original TTL.
- Lexical evidence is preserved, but this exporter is not an ontology reasoner
  and does not add inferred OPMAD concepts.
- `not_reported` means absent from the successfully parsed facts output. It
  cannot by itself distinguish an omission in the paper from an upstream
  extraction omission.

The strict JSON output is an analytical/review artifact, not accepted input for
the legacy Java CBR loader. Use `facts_to_csv.py` only when that interoperability
format and its documented defaults are required.
