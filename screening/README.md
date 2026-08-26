# Human screening templates

These versioned blank templates support the final human-only study selection and the retrospective LLM-screening benchmark. They do not reuse the historical development labels under `extraction_papers/`.

## Start a screening batch

1. Timestamp the protocol. Reviewer sheets belong in `batches/<batch-id>/`; that local directory is ignored because it contains sourced metadata.
2. From the repository root, use the immutable final union at `.searches/scopus-final-2026-08-25/pre-screening-union.json` to create two blinded sheets. Do not alter the union.

   ```bash
   uv run scripts/create_human_screening_batch.py \
     --union-path .searches/scopus-final-2026-08-25/pre-screening-union.json \
     --output-dir screening/batches/s1-final-v1 \
     --batch-id s1-final-v1 \
     --protocol-version v1
   ```

   The helper records the union SHA-256 and creates a batch manifest plus one CSV for `R1` and one for `R2`. It refuses to overwrite a batch. Use `--reviewer-id` twice to replace those IDs. The deduplication key is a temporary screening ID; retain it until permanent corpus IDs are assigned.
3. Each generated file has `screening_stage=title_abstract`. Reviewers work independently. A title/abstract record stops only when both reviewers exclude it; every unclear or discordant record advances.
4. For records that advance, create separate full-text reviewer files from the same template, set `screening_stage` to `full_text`, and record retrieval and bibliographic-match fields.
5. Merge completed reviewer files only after independent decisions are locked. Use `templates/adjudication_template.csv` to record the final decision and any discussion or third-reviewer resolution. Do not overwrite reviewer decisions. Place an ID-only adjudicated log in `decisions/` when it is ready to version and release where permitted.

Use `include`, `exclude`, or `unclear` for `decision`. At title/abstract stage, `include` and `unclear` both mean advance. At full-text stage, `include` is final inclusion. Leave `primary_exclusion_reason` blank unless the decision is `exclude`.

## Controlled values

| Field | Values |
|---|---|
| `primary_exclusion_reason` | `ineligible_bibliographic_record_or_publication`, `out_of_scope_target`, `no_implemented_eligible_diagnostic_or_prognostic_model`, `unavailable_or_mismatched_usable_oa_full_text`, `other_protocol_exclusion` |
| `exclusion_detail` | A short reason, for example `clinical_human`, `biological_process`, `software_it_cyber`, `business_social`, `natural_or_civil_infrastructure`, `generic_ai_control`, `review_editorial_book_chapter`, `no_eligible_opmad_function`, or `not_implemented_or_evaluated` |
| `confidence` | `high`, `medium`, `low` |
| `full_text_status` | `usable`, `unavailable`, `mismatched`, `partial_or_corrupt`, `not_assessed` |
| `bibliographic_match` | `yes`, `no`, `unclear`, `not_assessed` |
| `resolution` | `agreement`, `discussion`, `third_reviewer` |
| `benchmark_partition` | `development`, `held_out`, `not_assigned` |

Record one primary exclusion reason. If several apply, choose the reason that directly supports the final decision and place any additional context in `notes`.

## Benchmark safeguard

Do not show LLM labels, rankings, or rationales to either human reviewer or adjudicator. After final human decisions are frozen, assign the benchmark partition in the adjudication log. A benchmark system receives title/abstract text only in the core track; it receives no full text or external retrieval. The held-out labels must not be used to select prompts, models, or thresholds.
