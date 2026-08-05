# Benchmark: gpt-5.4-mini vs gpt-5.6-luna

## Scope

- **Baseline:** the 10 matching artifacts from `run_500_more_20260721_105503`, whose Pi Codex proxy log identifies the actual model as `gpt-5.4-mini`.
- **Candidate:** `gpt-5.6-luna` through a dedicated localhost proxy on port 8978.
- **Documents:** 10 papers selected at evenly spaced positions (1, 56, 112, 167, 223, 278, 334, 389, 445, and 500) from the 500-paper baseline manifest. The list is in `selection.txt`.
- **Controlled extraction setup:** fixed OPMAD ontology, facts-only mode, `head_chunks=3`, 2 parallel workers, identical retry limits. Only the actual Pi model and local proxy port differ.

Output pairs were matched by their deterministic `facts_<document-hash>.ttl` name. All 20 fact artifacts parse after applying the pipeline's normal RDF-star cleanup and convert to the downstream case representation.

## Results

| Metric | gpt-5.4-mini | gpt-5.6-luna |
|---|---:|---:|
| Successful fact files | 10 / 10 | 10 / 10 |
| Total regular RDF triples | 1,734 | 1,992 |
| Blind quality score, total (max. 150) | 49 | **55** |
| Blind quality score, mean (max. 15) | 4.9 | **5.5** |
| Blind quality score, median | 5.0 | **5.5** |
| Per-paper blind wins | 4 | **6** |
| Candidate proxy requests | — | 41 |
| Candidate mean proxy latency | historical baseline: 18.36 s/request | 36.55 s/request |

The candidate needed one initial Turtle-parse retry; its retry succeeded and all ten final artifacts are valid.

## Blind quality evaluation

The evaluator received the first three PDF pages and two anonymous CBR-oriented RDF summaries per paper. It did **not** receive model identities. It scored factual fidelity, coverage of the CBR extraction fields, and usable structure (0–5 each; total 0–15), without rewarding raw triple count. The evaluator was `gpt-5.4-mini`; this is a limitation, but it makes the candidate's 6–4 win conservative rather than a self-evaluation by the candidate. Raw output and scores are retained in `blind_judge_raw_response.txt` and `blind_judge_scores.json`.

| Paper | 5.4 | 5.6 | Winner |
|---|---:|---:|---|
| paper-1358 | 6 | 4 | 5.4 |
| paper-1481 | 5 | 7 | 5.6 |
| paper-1602 | 5 | 6 | 5.6 |
| paper-1710 | 4 | 6 | 5.6 |
| paper-1814 | 4 | 5 | 5.6 |
| paper-1912 | 6 | 4 | 5.4 |
| paper-2027 | 5 | 8 | 5.6 |
| paper-2129 | 5 | 4 | 5.4 |
| paper-2252 | 4 | 8 | 5.6 |
| paper-2355 | 5 | 3 | 5.4 |

## Decision

**Use `gpt-5.6-luna` for subsequent OntoCast extractions.** It has the better evidence-grounded result on this 10-paper, controlled comparison: 6 of 10 blind wins, +6 total quality points, a higher median score, complete output coverage, and 14.9% more regular RDF triples.

The trade-off is speed: its mean proxy latency was about 2.0× the historical `gpt-5.4-mini` mean. Revisit this decision with a larger human-annotated sample if latency or quota becomes a limiting constraint.
