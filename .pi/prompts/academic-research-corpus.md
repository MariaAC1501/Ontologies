You are an expert researcher. Build a deduplicated corpus of relevant academic literature for a systematic review topic.

Review protocol location: $@

## Goal
Produce a screened candidate corpus for full-text retrieval.

## Working directory
Reuse `{{topic-slug}}/` and create:

```bash
mkdir -p "{{topic-slug}}"/searches
```

## Required inputs
- `protocol.md` — existing review protocol to reuse. Do not create this, and alert the user if it doesn't exist yet.

## Required outputs
- `search-log.md` — exact queries, filters, totals, refinements, failed attempts, final search set
- `screening.md` — title/abstract screening decisions grouped into `core`, `supporting`, and `rejected`, with reasons
- `searches/merged_candidates.json` — merged + deduplicated search results
- `corpus.json` — screened retrieval corpus containing all kept papers, each labeled with `screening_tier: core` or `screening_tier: supporting`

## Artifact templates

Use these minimal templates unless an existing artifact already has a stronger structure.

### `search-log.md`

```markdown
# Search Log

Topic: ...
Review dir: `...`

## Protocol reuse
- 

## Search strategy notes
- 

## Query log
| ID | Database | Exact query | Filters | Total | Results retrieved | Assessment |
|---|---|---|---|---:|---:|---|

## Coverage audit
| Lineage / concept cluster | Representative papers expected | Found in candidates? | Found in kept corpus? | Recall risk |
|---|---|---|---|---|

## Final query set used
- 

## Merge and deduplication
- Input files:
- Raw results:
- Unique results:
- Duplicates removed:

## Stopping rationale
- 
```

### `screening.md`

```markdown
# Screening Log

Screened source: `searches/merged_candidates.json`
Candidates after merge/dedup: ...
Kept in retrieval corpus: ...
Excluded: ...

## Screening rule actually applied
- 

## Core papers
| Decision | Year | Title | Why core |
|---|---:|---|---|

## Supporting papers
| Decision | Year | Title | Why supporting |
|---|---:|---|---|

## Rejected papers
| Decision | Year | Title | Why rejected |
|---|---:|---|---|

## Screening confidence and corpus quality reflection
- 
```

### `corpus.json`

Use a top-level object with a `results` array. Each kept entry should minimally include:

```json
{
  "corpus_id": "paper-0001",
  "title": "...",
  "doi": "...",
  "authors": [{"name": "..."}],
  "year": 2024,
  "abstract": "...",
  "citationCount": 0,
  "openAccess_pdf_url": null,
  "paperId": "...",
  "provenance": [],
  "screening_tier": "core"
}
```

## Workflow

### 1. Reuse the review protocol
Read `protocol.md` first.
Assume the PICOC breakdown, research questions, databases, inclusion/exclusion criteria, quality checklist, and extraction fields have already been defined by the orchestrator.
Do not redefine the review scope, your task is only to build the corpus.

### 2. Refine keyword searches iteratively
Run the `academic-search` skill. Academic searches only, not regular internet search.
Search **2-3 targeted queries at a time**.
Before finalizing queries, identify the main concept clusters / literature lineages implied by `protocol.md` and make sure the search set covers them explicitly.
Use the research questions and PICOC concepts to iteratively improve search terms, including synonyms and narrower/broader variants.

For each query:
- save full JSON in `searches/`
- record database, exact query, filters, `total`, and `results_retrieved` in `search-log.md`
- note whether the query was too broad, too narrow, off-topic, or useful
- if `total` is clearly too large to screen comfortably (roughly above **30-70** per query), refine and rerun before screening

Be explicit in `search-log.md` about:
- which concept clusters / lineages you targeted
- which queries did not work well and why
- which refinements improved the search
- which final queries were actually used to build the corpus
- a concise coverage audit: major lineages, representative/canonical papers you expected, whether they were found, and any recall risks

Be **very thorough** with your query searches to produce a **very high-quality** corpus.

Reflect on how the inclusion/exclusion criteria are helping or hindering you when running the keyword searches. If necessary, propose changes to these criteria and await user approval before moving forward.

### 3. Merge and deduplicate
After the search set is good enough, merge saved search JSON files:

```bash
uv run ~/agent-tools/academic-research/skills/academic-search/scripts/merge_search_results.py \
  --input "{{topic-slug}}/searches" \
  --output-path "{{topic-slug}}/searches/merged_candidates.json"
```

### 4. Screen for relevance
Screen titles and abstracts/snippets from `merged_candidates.json` against the protocol and research questions.
Document decisions in `screening.md` using three tiers:
- `core` — central, review-defining evidence that directly answers one or more research questions
- `supporting` — relevant background, component, or contextual evidence worth retrieving but not central enough to define the review on its own
- `rejected` — out of scope or too weak, with a concise reason

Save all kept records (`core` + `supporting`) to `corpus.json` as the retrieval corpus.
Add `screening_tier` to each kept entry.
Each kept entry should preserve enough metadata for retrieval and synthesis: title, DOI, authors, year, abstract, citation count, OA PDF URL if present, provenance, and `screening_tier`.

## Stopping rule
Stop when the corpus is good enough for retrieval: the final query set is working well, the main concept clusters / lineages are covered, new searches are mostly redundant, and the kept set is relevant to the research questions.

Iterate and reflect on your work: are you confident that you are delivering a high-quality result?
