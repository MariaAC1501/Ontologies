Retrieve PDFs for a screened literature corpus, work with the user on inaccessible papers, and convert all accessible papers to Markdown.

Existing review folder containing the desired corpus: $@

## Goal
Starting from an existing review directory, produce a fully accessible markdown corpus for synthesis.

## Rquired inputs
Reuse an existing `{{topic-slug}}/` directory.
Required input file:
- `corpus.json` — kept retrieval corpus; preserve each paper's `screening_tier` (`core` or `supporting`)

## Required outputs
- `pdf-status.md` — retrieval status for every corpus entry
- `pdfs/` — normalized PDFs used by the pipeline
- `manual-pdf-drop/` — raw user-downloaded PDFs, with original filenames preserved
- `manual-pdf-drop/README.html` — brief instructions showing the folder path and which papers are still missing
- `markdown/` — markdown conversions for all accessible papers
- `corpus_accessible.json` — corpus restricted to papers with usable markdown

Create missing folders as needed:

```bash
mkdir -p "{{topic-slug}}"/{pdfs,manual-pdf-drop,markdown}
```

## Artifact templates

Use these minimal templates unless an existing artifact already has a stronger structure.

### `pdf-status.md`

```markdown
# PDF Retrieval Status

- Review dir: `...`
- Total corpus entries: ...
- `Core` papers in retrieval corpus: ...
- `Supporting` papers in retrieval corpus: ...
- Files present in `pdfs/`: ...
- Files present in `manual-pdf-drop/`: ...
- Markdown conversions completed: ...
- Accessible `core` papers / total `core` papers: ...
- Accessible `supporting` papers / total `supporting` papers: ...

## Retrieval summary
| corpus_id | Tier | Title | Retrieval status | PDF path | Notes |
|---|---|---|---|---|---|

## Manual drop matching summary
### Matched
- 
### Needs review
- [for each item: convert the raw PDF to markdown, confirm the title from the full text, then either normalize it into `pdfs/` or mark it missing if still unresolved]
### Unmatched
- 
### Still missing
- 

## User action needed
- 

## Conversion results
- 
```

### `corpus_accessible.json`

Use a top-level object with a `results` array. Preserve all useful corpus metadata and add at least:

```json
{
  "corpus_id": "paper-0001",
  "title": "...",
  "screening_tier": "core",
  "pdf_path": "pdfs/paper-0001_....pdf",
  "markdown_path": "markdown/paper-0001_....md"
}
```

## Workflow

### 1. Retrieve PDFs for the full corpus
For each entry in `corpus.json`:
- try DOI-based retrieval first when a DOI exists
- otherwise use publisher/landing-page URL or open-access PDF URL when available
- log the outcome in `pdf-status.md`

Use the `academic-search` skill for retrieval.
Use only OA/API retrieval inside `retrieve_paper_pdf.py`; if automatic retrieval fails, switch immediately to the manual user-download workflow below.
If helpful, you may use Playwright ad hoc to try alternative landing pages or repositories, but make at most two attempts per missing PDF and then prefer the canonical handoff with `manual-pdf-drop/`.
Use only the tools needed for PDF retrieval. Do not expand the corpus.

### 2. Work with the user on inaccessible papers
If a paper cannot be retrieved automatically:
- create or update `manual-pdf-drop/README.html` with the absolute folder path for `manual-pdf-drop/` and a linked list of still-missing papers / landing pages; prefer using `uv run ~/agent-tools/academic-research/skills/academic-search/scripts/generate_manual_pdf_drop_readme.py`
- if useful in an interactive run, open that HTML for the user after generating it
- tell the orchestrator to ask the user once to open those links in their normal browser (with institutional proxies / anti-bot handling if needed) and simply download any obtainable PDFs into `manual-pdf-drop/` **without renaming them**; prefer Safari, then Chrome, then Firefox on macOS, but keep the instructions cross-platform and browser-agnostic otherwise
- on the next pass, scan `manual-pdf-drop/`, match any newly added PDFs to corpus entries, and copy/rename them into `pdfs/` using the stable pipeline filenames; prefer using `uv run ~/agent-tools/academic-research/skills/academic-search/scripts/match_manual_pdf_drop.py`
- merge `manual-pdf-drop/match-report.json` back into `pdf-status.md`, clearly noting which papers were `matched`, `needs_review`, `unmatched`, and `still_missing`
- for each `needs_review` PDF, convert the raw file to markdown, inspect the full-text title, and try once more to resolve it to a corpus entry; if resolved, normalize it into `pdfs/`, otherwise mark it as missing because even the user-provided PDF could not be matched confidently
- after that one user pass, if all `core` papers are now accessible, continue directly to conversion and synthesis preparation
- if some `core` papers are still missing after that one user pass, still continue to conversion and finalize a `core`-incomplete accessible corpus; record the missing `core` papers clearly in `pdf-status.md`
- treat any papers still absent from `manual-pdf-drop/` after the user pass as inaccessible for this review run, and record that in `pdf-status.md`

Do not silently drop inaccessible items, and do not keep insisting on repeated manual retries once the drop folder has been checked.

### 3. Convert accessible PDFs to Markdown
For every PDF that is available on disk in `pdfs/`, invoke the `pdf-to-markdown` skill and save Markdown in `markdown/`.
Use a stable file naming scheme so each paper maps cleanly across `corpus_accessible.json`, `pdfs/`, and `markdown/`.

### 4. Finalize the accessible corpus
Create `corpus_accessible.json` containing only entries that now have usable markdown in `markdown/`.
Preserve `screening_tier` from `corpus.json` in every accessible entry.
For excluded entries, keep the reason in `pdf-status.md`.

Do not overwrite the original `corpus.json`; treat `corpus_accessible.json` as the synthesis-ready corpus.
