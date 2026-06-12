---
name: academic-search
description: Search academic databases (Semantic Scholar, Scopus, arXiv, Google Scholar) and retrieve PDFs for academic papers.
---

**IMPORTANT**: Before saving any file, verify that the `--output-path` resolves to the user's expected location (the initial working directory where they started their session), not a subfolder or unexpected location.

## Overview

This skill searches academic databases and retrieves full text from papers using multiple open access sources.

## Search Process

### 1. Academic Database Search

Search across multiple academic databases. Run searches in parallel (2-3 at a time) for efficiency.

**Mandatory search-review loop:**
1. Run the search script and save the full JSON to `--output-path`.
2. **Read the saved JSON file** after each run. Do not rely only on stdout, because stdout is a capped preview.
3. Inspect both:
   - `total` = full hit count reported by the source (Google Scholar is still an estimate from the UI header)
   - `results` = the retrieved records actually available for screening in this run
4. If `total` is too large to screen comfortably (for example, well above ~30-60 unless the user explicitly wants a broader screen), refine the query and rerun before continuing.
5. When `total` is in a manageable range, review the **full saved `results` list**, not just the first few items printed to stdout.

Use the saved JSON as the source of truth for screening and query refinement.

After running multiple searches, you can merge and deduplicate the saved JSON files into one candidate corpus:

```bash
uv run ./scripts/merge_search_results.py \
  --input ./.searches \
  --output-path ./.searches/merged_corpus.json
```

The merged file keeps per-record provenance (`source`, `query`, `input_file`, `rank`) so you can screen from a single deduplicated corpus while preserving reproducibility.

**Semantic Scholar:**
```bash
uv run ./scripts/search_semantic_scholar.py \
  --query "transformer models NLP" \
  --limit 20 \
  --year-start 2020 \
  --year-end 2026 \
  --max-pages 3 \
  --output-path ./.searches/semantic_scholar_results.json
```

**Scopus:**
```bash
uv run ./scripts/search_scopus.py \
  --query "transformer models" \
  --limit 20 \
  --year-start 2020 \
  --year-end 2026 \
  --max-pages 3 \
  --output-path ./.searches/scopus_results.json
```

**arXiv:**
```bash
uv run ./scripts/search_arxiv.py \
  --query "transformer neural networks" \
  --limit 20 \
  --year-start 2020 \
  --year-end 2026 \
  --max-pages 3 \
  --output-path ./.searches/arxiv_results.json
```

**Google Scholar:**
```bash
uv run ./scripts/search_google_scholar.py \
  --query "transformer neural networks" \
  --limit 20 \
  --year-start 2020 \
  --year-end 2026 \
  --max-pages 3 \
  --output-path ./.searches/google_scholar_results.json
```

**Note**: Google Scholar uses web scraping and may be subject to rate limiting or blocking. It does not have an official API.

These are the only academic databases we have access to at the moment.

You always run Python scripts using `uv run`, you NEVER USE `uv run python`.

Available options:
- `--query`: Search query string (required)
- `--limit`: Maximum results per query (default: 20)
- `--year-start`: Filter from this year onwards
- `--year-end`: Filter up to this year
- `--max-pages`: Pages to fetch (for pagination, default: 3)
- `--output-path`: Path to save results (JSON, required)

**Note**: The scripts print JSON to stdout and save messages to stderr. Results include DOI, title, authors, abstract, year, and citation count.

**Count semantics:**
- Semantic Scholar: `total` is the API-reported full hit count.
- Scopus: `total` is the API-reported full hit count.
- arXiv: `total` is the OpenSearch-reported full hit count.
- Google Scholar: `total` is the result count estimate parsed from the Scholar results page.
- `results_retrieved` is how many records were actually collected into the saved JSON file for this run.

### 2. Full Text PDF Retrieval

Extract full text PDF for papers using either a DOI/arXiv ID or a direct publisher landing-page URL.

When you have a DOI, the script tries multiple sources in order:
1. **arXiv** - Direct download for arXiv papers
2. **OpenAlex** - OpenAlex catalog (285M+ works)
3. **Semantic Scholar Open Access** - Query for PDF URL
4. **Unpaywall** - Legal open access versions

If those fail, the script stops and returns a manual-download handoff instead of attempting interactive browser automation.

Use `--doi` when you have a DOI or arXiv ID:

```bash
uv run ./scripts/retrieve_paper_pdf.py \
  --doi "10.1016/j.example.2023.001" \
  --output-path ./.papers/paper_10_1016_j_example_2023_001.pdf
```

Use `--url` when DOI-based OA APIs miss the paper, the DOI has not propagated yet, or you already have the publisher page URL. The URL is preserved in the result as a landing-page handoff for manual download if OA retrieval fails:

```bash
uv run ./scripts/retrieve_paper_pdf.py \
  --url "https://www.mdpi.com/2306-5338/13/4/108" \
  --output-path ./.papers/mdpi_hydrology13040108.pdf
```

For anti-bot-protected or institution-gated sites such as IEEE Xplore, ACM Digital Library, ScienceDirect, SpringerLink, and ResearchGate, keep the default OA-first flow, but switch quickly to the **manual browser-download workflow** instead of any persistent interactive browser automation:

1. Try the normal `retrieve_paper_pdf.py` flow first.
2. If open-access APIs do not retrieve the PDF, ask the user to download it in their normal browser.
3. Prefer Safari, then Chrome, then Firefox on macOS, but keep instructions cross-platform and browser-agnostic otherwise.
4. The user may use institutional proxies, normal site sign-in, and anti-bot/CAPTCHA completion in that browser.
5. Have the user save any obtainable PDFs into the review's `manual-pdf-drop/` folder **without renaming them**.
6. Any papers still absent from `manual-pdf-drop/` after that pass should be treated as inaccessible for the current review run.

To help with this handoff, generate `manual-pdf-drop/README.html`, ideally with:

```bash
uv run ./scripts/generate_manual_pdf_drop_readme.py \
  --output-path ./manual-pdf-drop/README.html \
  --drop-folder ./manual-pdf-drop
```

You can optionally pass `--open` in an interactive run to open the handoff page for the user.

When the user has dropped raw PDFs into `manual-pdf-drop/`, normalize them into `papers/` with:

```bash
uv run ./scripts/match_manual_pdf_drop.py \
  --corpus ./corpus.json \
  --manual-dir ./manual-pdf-drop \
  --papers-dir ./papers \
  --report-path ./manual-pdf-drop/match-report.json
```

The matcher uses DOI first, then PDF metadata / first-page title text / filename heuristics, and reports `matched`, `needs_review`, `unmatched`, and `still_missing`.

For `needs_review` items, convert the raw PDF to markdown, inspect the full-text title, and try once more to resolve it to a corpus entry. If that still does not resolve the match confidently, treat the paper as missing for the current review run.

Available options:
- `--doi`: DOI or arXiv ID to extract
- `--url`: Direct publisher landing-page URL to preserve for manual-download handoff
- `--output-path`: Path to save the PDF file or directory (required)

Exactly one of `--doi` or `--url` is required.

**Parsing the response:**

The script outputs JSON:

| Status | Meaning | Action |
|--------|---------|--------|
| `"pdf_ready"` | PDF downloaded | **Invoke the `pdf-to-markdown` skill** to convert |
| `source == "existing_file"` | PDF already on disk | **Invoke the `pdf-to-markdown` skill** to convert |
| `"requires_manual_upload"` | No PDF from OA/API sources | **Invoke the `pdf-to-markdown` skill** after user provides PDF |
| `"error"` | Download failed | Skip or try alternative source |

`retrieve_paper_pdf.py` only downloads the PDF — it does not convert it. **Always invoke the `pdf-to-markdown` skill** as the next step, passing the `pdf_path` from the response as input.

**Fallback workflow**
1. Try `--doi` first when you have a DOI.
2. If DOI-based retrieval returns `requires_manual_upload` or `error`, and you know the publisher page URL, retry with `--url` so the manual-download handoff includes the right landing page.
3. Ask the user to download the PDF manually in their normal browser and place it in `manual-pdf-drop/` without renaming it.
4. Generate or update `manual-pdf-drop/README.html` so the folder path and missing-paper links are easy to follow.
5. Treat any papers still missing from `manual-pdf-drop/` after the user's pass as inaccessible for the current review run.
6. **Invoke the `pdf-to-markdown` skill** to convert any successfully retrieved or manually provided PDF.

**Progress indicators:** The script outputs progress to stderr for OA/API retrieval attempts and download validation.

PDF conversion can take up to 10 minutes for large documents. Watch stderr for progress updates.

## Persistence

Use the `--output-path` option to specify the path where the results should be saved.