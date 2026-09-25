# Held-out gold annotation (manual baseline)

This is the first stage of the human-in-the-loop interface. It collects **independent, blank-form manual annotations** for the held-out benchmark and timed unassisted baseline. It does not import, display, or evaluate any LLM outputs. The provisional list in `paper/challenge_set_candidates.md` is **not** a frozen corpus or gold standard. Do not begin final held-out annotation until eligibility, the representation-neutral codebook, bibliographic identity, and partition are frozen by humans.

## Inputs and launch

1. Create a `pipeline/fulltext_corpus.schema.json`-compatible manifest with `partition_frozen: true`; verify each record, select `partition: "held_out"`, and record accurate PDF SHA-256 values. Keep it at `corpus/manifest.json` (local, not in Git until approved). See `pipeline/FULLTEXT.md` for the parser and sidecars. This interface rejects an unfrozen manifest, unverified records, mismatched PDFs, missing prepared pages, failed quality gates, or a mismatched text/identity source map.
2. Prepare **all held-out articles** with the complete-document, page-delimited preparation command, without an LLM call:

   ```bash
   python3 -m pipeline.fulltext prepare --manifest corpus/manifest.json --corpus-id paper-0001 --output-dir runs/held-out-fulltext/paper-0001
   # Repeat for each held-out corpus ID in the frozen manifest.
   ```

3. Start one local server **per reviewer** (use a separate port for the other reviewer):

   ```bash
   python3 -m annotation.server --manifest corpus/manifest.json \
     --prepared-dir runs/held-out-fulltext --output-dir annotation/work \
     --reviewer R1 --port 8765
   # Open http://127.0.0.1:8765/
   ```

The server binds only to `127.0.0.1`, has no multi-user login, and should not be placed behind a network proxy. Use separate local OS accounts or otherwise prevent reviewers from accessing each other's output directories; per-reviewer API filtering alone is **not** a filesystem security boundary. Only assigned reviewers should run their instance. No model-output directory is accepted as an input. Back up the local output directory securely; `annotation/work/` is Git-ignored. Do not distribute article text or PDFs without checking their licences.

## Using the form

- Start the timer when you start reading/annotating. Pause it for breaks. It records UTC start/end intervals and active elapsed seconds, not idle-detection or hidden browser time. Pause before closing the browser or server; a running interval continues across restarts until paused. Submit closes an active interval and locks the record. Drafts autosave; save status shows validation failures, and switching articles waits for a successful save. A revision conflict requires reloading rather than overwriting another tab.
- Add zero, one, or several cases per article. If zero, explain why. The case ID is stable in this reviewer's record. Each case links the case boundary, item, function, data inputs, models, and configuration by nesting them together; split distinct function–item–data–model-set combinations into separate cases. Independently evaluated alternatives should not be grouped as one coordinated model set. Apply the **frozen codebook** for ambiguous splits and normalization.
- For each assertion choose `present`, `not_reported`, `unclear`, `not_applicable`, or `extraction_failure`. Present values need raw source wording and at least one exact evidence quote. Normalized labels are optional except for a present model configuration, which must be `single` or `coordinated`. Record each distinct data input/model as a separate entry. Use case and article notes for unresolved decisions; optional performance and synchronization fields are not yet part of this core form.
- Search across text pages or browse PDF pages. Select a quotation within the numbered **text** page and click **Use selection** in the relevant evidence row. Or type/paste a unique quotation and click **Find exact quote**. Text spans are validated against the prepared text and stored as page-relative character offsets plus its SHA-256. If OCR/Markdown does not represent the quote faithfully, use the PDF view, select `PDF (manual verification)`, and enter the exact quote, PDF page, and optionally the section/table; PDF quotes cannot be automatically checked against the source text and require human verification.

Keep an assignment log outside this tool: a reviewer who has annotated an article here must not later receive that article in an assisted session. Do not expose either reviewer's work to the other before independent submission.

The saved file is `annotation/work/<reviewer>/<corpus-id>.json` (`held-out-gold/v1`). It includes identity and source-text hash, case/entry IDs, statuses, raw and normalized values, exact quotations with page/section and text offsets where available, revision/state, and timer intervals. It does **not** merge the two reviewers' records. Submitted records are locked in the interface; preserve both independently submitted files before any adjudication or model evaluation.

This stage does **not** implement adjudication, inter-annotator agreement, prefill correction, atomic edit logging, assisted-session assignment/counterbalancing, or a frozen gold release. Those require separate workflows after the codebook and assignments are fixed. The elapsed time here is the manual baseline only.

Run the local tests with `python3 -m unittest discover -s annotation/tests -v`.
