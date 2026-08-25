# Project Tasks

This file separates publication/research work from repository and extraction-engineering work.

The existing files under `extraction_papers/ontocast_runs/` are development experiments. They must not be mixed with the corpus or outputs used for the final paper.

## Task codes and status

- `P-*` identifies paper/research tasks; `T-*` identifies technical/repository tasks.
- Cite the complete bold code when discussing a task, for example `P-PROTOCOL-03` or `T-EXPORT-07`.
- `[x]` means the current repository provides and tests the stated capability; `[ ]` means it remains open.
- Codes are stable identifiers: completed or retired tasks should keep their codes rather than being renumbered.

The checked technical tasks reflect the engineering already present in the current tree, notably artifact cleanup, the generated authoritative OPMAD profile, the strict nullable review export, namespace/isolation hardening, and reproducible run-manifest validation. Remaining technical tasks depend on the final protocol, corpus, annotation model, upstream extraction behavior, or publication run.

## A. Paper and research tasks

### A1. Freeze the paper's contribution and scope

- [x] **P-SCOPE-01** — Use the combined contribution: an OPMAD-guided systematic mapping study plus human validation of the LLM-assisted extraction method.
- [x] **P-SCOPE-02** — Integrated and retired the working protocol and research questions in `paper/main.tex`.
- [x] **P-SCOPE-03** — Select a target venue later and check its requirements for systematic reviews, AI-assisted evidence synthesis, supplementary material, and article length. Until then, use the generic IEEE journal LaTeX working manuscript and a ten-page target.
- [x] **P-SCOPE-04** — Set the publication period to 2025--2026; set the final search-date cutoff to 2026-08-25 and avoid interpreting an incomplete 2026 as an annual trend.
- [x] **P-SCOPE-05** — State explicitly that the review covers English-language, open-access empirical journal and conference articles indexed in Scopus on OPMAD-representable diagnostic and prognostic functions, not all predictive-maintenance research.
- [x] **P-SCOPE-06** — Claim workflow reliability against expert annotation only; do not claim that ontology guidance improves extraction.
- [x] **P-SCOPE-07** — Retired: no ontology-benefit claim will be made, so a controlled flat-schema ablation is out of scope.

### A2. Write and register the review protocol

- [x] **P-PROTOCOL-01** — Recorded the Scopus API, 2025--2026 period, English-language journal/conference and OA criteria, and the search-date cutoff: **2026-08-25**. Exact pilot and final S1/S2 execution timestamps, queries, exports, and API-page recovery passes are archived.
- [x] **P-PROTOCOL-02** — Froze the two-stratum final S1a/S1b Scopus strategy (version 1.1) in `keywords_predictive_maintenance_scopus.txt` and `keywords_predictive_maintenance_scopus_diagnostic.txt`. The 2026-08-25 final runs, immutable query companions, and validated pre-screening union are archived in `.searches/scopus-final-2026-08-25/`; residual noise remains for documented screening.
- [x] **P-PROTOCOL-03** — Aligned eligibility in `predictive_maintenance_inclusion_exclusion_criteria.md` and `paper/main.tex` with implemented existing OPMAD diagnostic/prognostic functions on engineered maintainable items.
- [x] **P-PROTOCOL-04** — Defined exclusions in `predictive_maintenance_inclusion_exclusion_criteria.md` and `paper/main.tex` for reviews, non-engineered targets, generic AI/control, non-case maintenance management, and conceptual/unimplemented architectures.
- [x] **P-PROTOCOL-05** — Ran and documented the 2026-08-25 Scopus pilot. Its residual out-of-field noise establishes the need for documented screening; it does not invalidate the candidate query.
- [x] **P-PROTOCOL-06** — Have the search strategy peer-reviewed, preferably using PRESS-style checks or an information specialist. Discarded; will not be done.
- [ ] **P-PROTOCOL-07** — Define deduplication, title/abstract screening, full-text screening, conflict resolution, and exclusion-reason procedures.
- [ ] **P-PROTOCOL-08** — Decide whether screening is human-only, LLM-prioritized, or LLM-assisted. If an LLM can exclude records, validate screening sensitivity separately and audit a random sample of exclusions.
- [ ] **P-PROTOCOL-09** — Preregister or timestamp the protocol before final screening.
- [ ] **P-PROTOCOL-10** — Use PRISMA-S search reporting, a PRISMA 2020 study-selection flow diagram, and counts for every search, screening, retrieval, and inclusion transition.

### A3. Build the publication corpus

- [x] **P-CORPUS-01** — Ran and archived the exact final S1a/S1b Scopus API JSON/CSV exports, query companions, commit markers, and pre-screening accounting in `.searches/scopus-final-2026-08-25/` without overwriting prior artifacts. Three complete S1a passes reconciled to its stable 1,219-record source total; S1b returned 1,642 unique records. Their 2,770-record pre-screening union is not yet eligibility screened.
- [ ] **P-CORPUS-02** — Assign stable corpus IDs and retain DOI, EID, title, year, source, authors, abstract, keywords, OA status, and source query.
- [x] **P-CORPUS-03** — Reconciled the three complete S1a API passes to the stable 1,219-record EID total, then deduplicated the final S1a/S1b pool by Scopus Paper ID and DOI. The one same-DOI wind-turbine alias and 90 cross-stratum EID duplicates are documented in `.searches/scopus-final-2026-08-25/pre-screening-accounting.json`; no unresolved normalized-title/year collision remained.
- [ ] **P-CORPUS-04** — Screen records against the registered criteria.
- [ ] **P-CORPUS-05** — Retrieve a full text for every included record.
- [ ] **P-CORPUS-06** — Verify each PDF against title, DOI, authors, and publication year.
- [ ] **P-CORPUS-07** — Record source URL, retrieval date, OA license when available, file hash, page count, text-extraction status, and OCR status.
- [ ] **P-CORPUS-08** — Resolve corrupt, partial, supplementary-only, or mismatched files before freezing the corpus.
- [ ] **P-CORPUS-09** — Ensure 100% full-text availability among the final included set or document and justify every exception.
- [x] **P-CORPUS-10** — Ran final S2a/S2b metadata-only all-access counterparts by deleting only the OA predicate from S1a/S1b. S2b was recovered through disjoint 2025/2026 partitions after the unpartitioned API request hit its 200-page rate ceiling; reconciled S2a/S2b totals were 4,156 and 5,168.
- [ ] **P-CORPUS-11** — Repeated the final pre-screening OA comparison: 2,770 matched OA candidates versus a 6,266-record all-access complement, with title/abstract and DOI-prefix skew reported in Annex B of `paper/main.tex`. Repeat after final screening and full-text verification before making field-level synthesis claims.

### A4. Define the OPMAD case-annotation guide

- [ ] **P-CODEBOOK-01** — Freeze the exact OPMAD version and list the competency questions used by the review.
- [ ] **P-CODEBOOK-02** — Define one OPMAD case as a linked article, maintainable item, function, model/configuration, and corresponding condition data.
- [ ] **P-CODEBOOK-03** — Specify how to split papers containing multiple assets, tasks, experiments, or model pipelines into cases.
- [ ] **P-CODEBOOK-04** — Define mappings for all existing OPMAD function subclasses.
- [ ] **P-CODEBOOK-05** — Define the intended use of `Maintainable_item`, `item_type`, `maintainable_item_record`, and `Data_variable`.
- [ ] **P-CODEBOOK-06** — Define how specific model names are recorded as open-text individuals.
- [ ] **P-CODEBOOK-07** — Restrict model types to the existing knowledge-based, data-driven, physics-based categories and their combinations.
- [ ] **P-CODEBOOK-08** — Define single-model and multi-model configuration consistently.
- [ ] **P-CODEBOOK-09** — Define online, off-line, both, unreported, and unclear decisions without adding unreported/unclear as OPMAD concepts.
- [ ] **P-CODEBOOK-10** — Define how performance indicators and values are linked to the correct module/case.
- [ ] **P-CODEBOOK-11** — Define evidence requirements: exact quotation, page, section, and source span for every analytical assertion.
- [ ] **P-CODEBOOK-12** — Define separate annotation statuses for present, genuinely not reported, unclear, not applicable, and extraction failure.
- [ ] **P-CODEBOOK-13** — Pilot the guide on heterogeneous papers and revise it before held-out annotation.

### A5. Create the human gold standard

- [ ] **P-GOLD-01** — Determine the validation sample size based on expected field prevalence and desired confidence intervals rather than convenience alone.
- [ ] **P-GOLD-02** — Reserve separate development and held-out sets.
- [ ] **P-GOLD-03** — Stratify the held-out set by task, asset type, model type/configuration, paper complexity, publication year, and PDF/OCR quality.
- [ ] **P-GOLD-04** — Ensure multi-case and multi-model articles are adequately represented.
- [ ] **P-GOLD-05** — Train annotators using the development set only.
- [ ] **P-GOLD-06** — Independently double-annotate the held-out set where feasible.
- [ ] **P-GOLD-07** — Measure inter-annotator agreement by field and relation.
- [ ] **P-GOLD-08** — Adjudicate disagreements without exposing held-out gold labels during system tuning.
- [ ] **P-GOLD-09** — Freeze and version the adjudicated gold dataset.

### A6. Prespecify method evaluation

- [ ] **P-EVAL-01** — Select field-level metrics: precision, recall, F1, exact match, and multi-label agreement as appropriate.
- [ ] **P-EVAL-02** — Evaluate relations and complete cases, not only extracted entity names.
- [ ] **P-EVAL-03** — Measure whether each claim is supported by its cited text span.
- [ ] **P-EVAL-04** — Count hallucinated, conflated, mislinked, and omitted facts separately.
- [ ] **P-EVAL-05** — Measure OPMAD expressibility/coverage without extending OPMAD.
- [ ] **P-EVAL-06** — Compare automated and human corpus distributions on the held-out sample and report absolute prevalence error.
- [ ] **P-EVAL-07** — Measure annotation, review, and adjudication time for human-only and assisted workflows.
- [ ] **P-EVAL-08** — Define confidence intervals and the statistical resampling procedure.
- [ ] **P-EVAL-09** — Set field-specific acceptance criteria before evaluating held-out data.
- [ ] **P-EVAL-10** — Decide in advance whether fields below threshold will be manually completed, qualified, or excluded from synthesis.
- [x] **P-EVAL-11** — Retired: title/abstract-versus-full-text comparison is outside the study scope.

### A7. Freeze and run the final extraction

- [ ] **P-FINALRUN-01** — Lock the corpus before the publication run.
- [ ] **P-FINALRUN-02** — Lock the OPMAD artifact/profile, model, prompts, parser, OCR version, sectioning, chunking, retries, normalization, and code revision.
- [ ] **P-FINALRUN-03** — Process complete texts; do not use experimental `head_chunks` limits.
- [ ] **P-FINALRUN-04** — Keep each paper's extraction isolated until case construction is complete.
- [ ] **P-FINALRUN-05** — Record failures and retries without silently changing models or prompts.
- [ ] **P-FINALRUN-06** — Do not tune the pipeline after inspecting held-out gold results; create a new validation cycle if changes are necessary.
- [ ] **P-FINALRUN-07** — Archive a machine-readable run manifest and checksums for all final outputs.
- [ ] **P-FINALRUN-08** — Have humans review all low-confidence cases, rare categories, outliers, and evidence supporting major claims.

### A8. Conduct the predictive-maintenance synthesis

- [ ] **P-SYNTH-01** — Report study and case counts separately.
- [ ] **P-SYNTH-02** — Summarize maintainable items, item types, and OPMAD functions.
- [ ] **P-SYNTH-03** — Analyze function × asset-type associations.
- [ ] **P-SYNTH-04** — Analyze function/asset/data × model and model-type associations.
- [ ] **P-SYNTH-05** — Compare single- and multi-model configurations across functions and assets.
- [ ] **P-SYNTH-06** — Summarize online/off-line synchronization where reliably available.
- [ ] **P-SYNTH-07** — Summarize performance-indicator usage without treating incomparable values as a common effectiveness scale.
- [ ] **P-SYNTH-08** — Identify sparse combinations only after checking extraction recall and corpus coverage.
- [ ] **P-SYNTH-09** — Quantify uncertainty introduced by extraction errors using the held-out validation results.
- [ ] **P-SYNTH-10** — Perform sensitivity analyses for OA restriction, OCR quality, and any manually corrected fields. The final metadata-only OA candidate comparison is reported in Annex B; repeat it after screening and full-text verification, then add the OCR/manual-correction analyses.
- [ ] **P-SYNTH-11** — Do not claim that frequently used models are necessarily superior models.

### A9. Write and release the paper package

- [ ] **P-PACKAGE-01** — Write the introduction around the predictive-maintenance model-selection problem, not around LLM novelty alone.
- [ ] **P-PACKAGE-02** — Describe OPMAD as an existing validated ontology and clearly distinguish instantiation from extension.
- [ ] **P-PACKAGE-03** — Report all AI involvement, model versions, prompts, human oversight, and failure handling.
- [ ] **P-PACKAGE-04** — Include the search protocol, PRISMA-S search report, PRISMA 2020 flow diagram, annotation guide, and validation procedure.
- [ ] **P-PACKAGE-05** — Separate development experiments from final study results.
- [ ] **P-PACKAGE-06** — Report limitations from OA restriction, Scopus-only coverage, OPMAD scope, PDF parsing, and LLM error.
- [ ] **P-PACKAGE-07** — Release search strings, screening decisions where permitted, corpus metadata, code, prompts, derived cases, evidence locations, and evaluation outputs.
- [ ] **P-PACKAGE-08** — Do not redistribute article PDFs unless their individual licenses permit it.
- [ ] **P-PACKAGE-09** — Prepare supplementary material for detailed mappings, prompts, field metrics, and additional analyses.
- [x] **P-PACKAGE-10** — Maintain `paper/main.tex` as the generic IEEE journal LaTeX working manuscript with a ten-page target until a venue is selected.

## B. Technical and repository tasks

Checked items below were completed in the initial unblocked engineering pass. Tasks that depend on the final review protocol, corpus, annotation design, or a publication extraction run remain open.

### B1. Establish an artifact-retention policy

- [x] **T-ARTIFACT-01** — Inventory tracked and untracked artifacts under `extraction_papers/ontocast_runs/`, `pipeline/test_output/`, and `pipeline/full_mode/test_output/`.
- [x] **T-ARTIFACT-02** — Classify each artifact as source, deterministic test fixture, experiment summary, raw generated output, log, cache, or temporary input.
- [x] **T-ARTIFACT-03** — Preserve only experiment manifests/reports that are needed to document development decisions.
- [x] **T-ARTIFACT-04** — Archive or remove raw experimental TTL outputs, copied/hard-linked PDFs, logs, PID files, and superseded retry directories after confirming they are not needed.
- [x] **T-ARTIFACT-05** — Remove local `__pycache__`, `.pyc`, stale test outputs, and OS metadata from working directories.
- [x] **T-ARTIFACT-06** — Add ignore rules for future corpus PDFs, local search artifacts, run inputs, raw outputs, logs, caches, and temporary review files.
- [x] **T-ARTIFACT-07** — Allowlist intentionally versioned manifests, small fixtures, and summary reports rather than tracking whole run directories.
- [x] **T-ARTIFACT-08** — Mark retained historical reports prominently as development evidence, not publication results.
- [ ] **T-ARTIFACT-09** — Remove documentation references to historical fact hashes when they are not stable fixtures.

### B2. Create a reproducible final-corpus layout

- [ ] **T-CORPUS-01** — Define separate locations for immutable search exports, screening tables, PDF manifests, local PDFs, parsed texts, annotations, development runs, held-out evaluation, and final runs.
- [ ] **T-CORPUS-02** — Keep local PDFs outside Git while retaining checksums and retrieval metadata in versioned manifests.
- [ ] **T-CORPUS-03** — Add schema validation for corpus and screening manifests.
- [ ] **T-CORPUS-04** — Write deterministic scripts for ID assignment, deduplication, manifest updates, and title/DOI audits.
- [ ] **T-CORPUS-05** — Make every transformation append-only or versioned so the original database export remains unchanged.
- [ ] **T-CORPUS-06** — Generate PRISMA counts directly from the authoritative screening manifest.

### B3. Replace the hand-maintained ontology seed with a verified profile

- [x] **T-OPMAD-01** — Identify and pin the authoritative `OPMAD.owl` artifact and required imports by checksum.
- [x] **T-OPMAD-02** — Decide whether OntoCast can consume the authoritative ontology directly.
- [x] **T-OPMAD-03** — If a smaller profile is required, generate it deterministically from the authoritative graph instead of maintaining an independent ontology manually.
- [x] **T-OPMAD-04** — Verify that every selected class, property, label, and axiom exists in the authoritative source.
- [x] **T-OPMAD-05** — Fail the build if the profile introduces a new OPMAD domain IRI or changes an existing axiom.
- [ ] **T-OPMAD-06** — Document omitted OPMAD terms and why they are outside the review competency questions.
- [x] **T-OPMAD-07** — Fix namespace handling so extracted facts consistently use authoritative OPMAD IRIs rather than generated `/seed#` or `None:` namespaces.
- [x] **T-OPMAD-08** — Add regression tests for ontology/profile equivalence and namespace stability.

### B4. Separate review extraction from the legacy CBR bridge

- [x] **T-EXPORT-01** — Preserve `pipeline/facts_to_csv.py` as a compatibility bridge only, or introduce an explicit legacy mode.
- [x] **T-EXPORT-02** — Create a publication-grade per-case export that does not force missing values merely to satisfy the legacy 19-column CBR schema.
- [x] **T-EXPORT-03** — Remove the `2021` publication-year fallback from the review path.
- [x] **T-EXPORT-04** — Remove the default `One step future state forecast` task from the review path.
- [x] **T-EXPORT-05** — Stop representing an unreported number of failure modes as `0`.
- [x] **T-EXPORT-06** — Stop forcing `Not reported` strings into ontology-backed analytical fields.
- [x] **T-EXPORT-07** — Do not infer preprocessing from the existence of any generic `Design_detail` without case-specific evidence.
- [x] **T-EXPORT-08** — Do not infer single/multi-model configuration from a corpus-wide model count; determine it within each case.
- [x] **T-EXPORT-09** — Extract synchronization, performance indicators, and performance values when explicitly linked in the facts.
- [x] **T-EXPORT-10** — Process each article graph independently before concatenating case records; never choose one article's first asset or model for another article.
- [x] **T-EXPORT-11** — Preserve null/status distinctions and RDF lexical/source-node evidence in the review export.
- [x] **T-EXPORT-12** — Keep the optional CBR export downstream of the validated review representation.

### B5. Model explicit OPMAD case boundaries

- [ ] **T-CASE-01** — Update extraction so one article can yield zero, one, or multiple predictive-maintenance cases.
- [ ] **T-CASE-02** — Use stable case and entity identifiers derived from corpus ID plus local case identity.
- [ ] **T-CASE-03** — Represent specific models and maintainable items as individuals, not newly generated OPMAD classes.
- [ ] **T-CASE-04** — Link each case/module to the correct function, asset, condition data, models, configuration, synchronization, and performance evidence.
- [ ] **T-CASE-05** — Prevent entities with different names or roles from being collapsed into one RDF resource.
- [x] **T-CASE-06** — Retain raw labels alongside normalized labels.
- [x] **T-CASE-07** — Add explicit validation for model-to-function and data-to-model/case relations.
- [x] **T-CASE-08** — Detect and flag contradictory values within a case rather than choosing the first value silently.

### B6. Make full-text processing publication-grade

- [ ] **T-FULLTEXT-01** — Replace experimental head-chunk defaults with a complete-document mode for final runs.
- [ ] **T-FULLTEXT-02** — Preserve section, page, paragraph/chunk, and character-span provenance through parsing and extraction.
- [ ] **T-FULLTEXT-03** — Add PDF text-quality checks and route low-quality files through OCR.
- [ ] **T-FULLTEXT-04** — Record parser/OCR software versions and settings per document.
- [ ] **T-FULLTEXT-05** — Detect truncated text, missing pages, duplicated pages, and publisher boilerplate dominance.
- [ ] **T-FULLTEXT-06** — Keep title, DOI, year, and corpus ID from the verified manifest rather than relying on LLM extraction for authoritative bibliographic identity.
- [ ] **T-FULLTEXT-07** — Handle tables and multi-column layouts explicitly where they contain model inputs or results.
- [ ] **T-FULLTEXT-08** — Test complete-document behavior on long and multi-case papers before the final run.

### B7. Preserve usable evidence and provenance

- [ ] **T-PROV-01** — Stop discarding RDF-star provenance in the publication path.
- [ ] **T-PROV-02** — Adopt an RDF-star-capable parser or convert statement provenance deterministically to a supported representation.
- [ ] **T-PROV-03** — Alternatively, retain evidence in a sidecar table keyed by stable assertion IDs.
- [ ] **T-PROV-04** — Require every analytical assertion to point to its source document and textual span.
- [ ] **T-PROV-05** — Distinguish source text, LLM assertion, normalized assertion, validation result, and human correction.
- [ ] **T-PROV-06** — Record prompt version, actual provider model, request/retry history, extraction timestamp, and software commit for every paper.
- [ ] **T-PROV-07** — Ensure sanitization of invalid IRIs and control characters does not alter source evidence silently.

### B8. Add normalization without creating a new ontology

- [ ] **T-NORM-01** — Build versioned lexical mappings for spelling variants, abbreviations, and synonymous model names.
- [ ] **T-NORM-02** — Retain raw extracted values so normalization decisions remain auditable.
- [ ] **T-NORM-03** — Restrict controlled OPMAD fields to their existing values and flag unmappable values.
- [ ] **T-NORM-04** — Treat detailed modern model names as labeled instances rather than new formal subclasses.
- [ ] **T-NORM-05** — Review high-frequency and high-impact normalization mappings manually.
- [ ] **T-NORM-06** — Measure normalization accuracy separately from extraction accuracy.

### B9. Add annotation and evaluation tooling

- [ ] **T-EVAL-01** — Define a machine-readable annotation format for cases, relations, evidence spans, and status values.
- [ ] **T-EVAL-02** — Provide annotator instructions and validation that catches incomplete or inconsistent annotations.
- [ ] **T-EVAL-03** — Support blind independent annotation and later adjudication.
- [ ] **T-EVAL-04** — Implement entity-, relation-, field-, and complete-case matching between gold and extracted outputs.
- [ ] **T-EVAL-05** — Report micro and macro metrics so common tasks do not hide failures on rare categories.
- [ ] **T-EVAL-06** — Add bootstrap confidence intervals and aggregate prevalence-error calculations.
- [ ] **T-EVAL-07** — Produce per-field error tables and adjudication queues.
- [ ] **T-EVAL-08** — Add timing capture for manual and assisted review effort.
- [ ] **T-EVAL-09** — Keep development and held-out evaluation outputs in separate directories with access discipline during tuning.

### B10. Strengthen tests

- [ ] **T-TEST-01** — Add fixtures for one-paper/one-case, one-paper/multiple-cases, and one-case/multiple-models.
- [x] **T-TEST-02** — Add fixtures for missing versus explicit-zero numeric values.
- [x] **T-TEST-03** — Add fixtures for unreported, unclear, not-applicable, and failed-extraction states.
- [ ] **T-TEST-04** — Add fixtures for repeated model names across distinct cases and repeated entities across papers.
- [x] **T-TEST-05** — Add tests for namespace consistency with authoritative OPMAD IRIs.
- [ ] **T-TEST-06** — Add tests for provenance retention and evidence-span round trips.
- [ ] **T-TEST-07** — Add tests for malformed Turtle, RDF-star conversion, invalid IRIs, encoding problems, and OCR text.
- [x] **T-TEST-08** — Add an end-to-end test that converts several article graphs into multiple isolated review cases without cross-document contamination.
- [x] **T-TEST-09** — Keep tiny deterministic fixtures under version control; do not make tests depend on historical generated runs.

### B11. Freeze runtime and run metadata

- [ ] **T-RUN-01** — Add a dependency lockfile or another documented mechanism for reproducible Python and parser versions.
- [ ] **T-RUN-02** — Pin submodule revisions and record local patches used in the final run.
- [ ] **T-RUN-03** — Record the actual model used by the proxy rather than trusting only the requested model name.
- [ ] **T-RUN-04** — Persist token/request counts, latency, failures, and retry reasons where the provider exposes them.
- [ ] **T-RUN-05** — Make runs resumable and idempotent without mixing configurations.
- [x] **T-RUN-06** — Fail when a resume attempt changes ontology, prompt, model, parser, or normalization version.
- [ ] **T-RUN-07** — Generate a final run manifest containing corpus hash, configuration hashes, software revisions, timestamps, and output checksums.

### B12. Update documentation

- [x] **T-DOC-01** — Update `README.md` to distinguish development extraction, publication review extraction, legacy CBR export, and full ontology-evolution experiments.
- [x] **T-DOC-02** — Update `pipeline/SCHEMA_MAPPING.md` after the review representation and legacy boundary are finalized.
- [x] **T-DOC-03** — Replace interoperability-only claims with precise statements about what each test validates.
- [x] **T-DOC-04** — Document the authoritative OPMAD source and generated-profile procedure.
- [ ] **T-DOC-05** — Document corpus setup, full-text processing, annotation, evaluation, final extraction, and synthesis commands.
- [ ] **T-DOC-06** — Add a reproducibility checklist linking every paper table/figure to its generating script and input manifest.
