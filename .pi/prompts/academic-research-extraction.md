You are an expert researcher. Extract data from an accessible academic literature corpus that can answer the research questions.

Location of the existing corpus: $@

## Goal
Extract data from an existing markdown corpus to answer the research questions without rerunning search or retrieval unless the user explicitly asks.

Produce extraction data that is useful for synthesis without relying on loose keyword categorization. Combine:
- **controlled coding** for protocol-defined categories and other synthesis-critical fields
- **open extraction** for researcher observations, unexpected findings, and emergent themes

## Required inputs
Reuse an existing `{{topic-slug}}/` directory. If the user didn't provide this directory, alert them before continuing.

```bash
mkdir -p "{{topic-slug}}"/extractions
```

Required inputs:
- `protocol.md`
- `corpus_accessible.json` — accessible corpus; entries may include `screening_tier` (`core` or `supporting`)
- `markdown/` markdown papers

## Required outputs
- `extraction_codebook.json` — run-specific controlled vocabulary/codebook derived from `protocol.md`
- `extraction.json` — compilation of extraction forms for all available studies, preserving controlled-code summaries
- `extractions/` — individual extraction forms
- `sources.bib` — cited final sources

## Artifact templates

Use these minimal templates unless an existing artifact already has a stronger structure.

### `extraction_codebook.json`

Create a codebook before launching per-paper subagents. Do not edit `protocol.md` just to add coding helpers unless the user asks.

```json
{
  "codebook_version": "1.0",
  "source_protocol": "protocol.md",
  "controlled_fields": {
    "<field_path>": {
      "type": "single_select | multi_select | ordinal | boolean | scale",
      "allowed_values": ["exact protocol/codebook labels"],
      "coding_note": "When to apply this code and when not to apply it."
    }
  },
  "limitation_flags": {
    "allowed_values": ["review-specific limitation flags"],
    "coding_note": "Flags are for aggregation only; retain open limitation text separately."
  },
  "open_coding_policy": "Use emergent_codes for relevant findings that do not fit the controlled vocabulary."
}
```

### `extractions/{{corpus-id}}.json`

Use the variables already defined in the quality checklist and the extraction form. Include both the full extraction and a compact controlled-code summary for downstream synthesis.

```json
{
  "corpus_id": "...",
  "tier": "core | supporting | background | excluded-after-full-text",
  "year": 2026,
  "quality_checklist": {},
  "structured_code_summary": {
    "<field_path>": {
      "values": ["exact controlled labels"],
      "status": "coded | not_reported | not_applicable | none | uncertain",
      "rationale": "Why these codes apply.",
      "evidence": [
        {"quote": "Direct quote where possible.", "location": "section/page/figure/table if available"}
      ],
      "confidence": "high | medium | low"
    }
  },
  "structured_limitations": {
    "limitation_flags": ["exact limitation flag labels"],
    "limitation_assessments": [
      {
        "flag": "exact limitation flag label",
        "source": "author_stated | extractor_identified",
        "rationale": "Why this limitation matters for the review questions.",
        "evidence_quote": "Direct quote where possible, or explain if the limitation is extractor-identified from the completed extraction.",
        "confidence": "high | medium | low"
      }
    ],
    "emergent_limitations": [
      {
        "label": "short-kebab-case-label",
        "rationale": "Important limitation not covered by the controlled flags.",
        "evidence_quote": "Direct quote where possible.",
        "confidence": "high | medium | low"
      }
    ]
  },
  "emergent_codes": [
    {
      "field_path": "protocol field or synthesis topic",
      "label": "short-kebab-case-label",
      "description": "Unexpected but relevant finding.",
      "rationale": "Why it may matter for synthesis.",
      "evidence_quote": "Direct quote where possible.",
      "confidence": "high | medium | low"
    }
  ],
  "extraction": {
    "<protocol extraction fields>": "..."
  }
}
```

### `sources.bib`

Use standard BibTeX entries for cited final sources.

## Workflow

### 1. Reuse the protocol
Read `protocol.md` and keep the existing research questions, criteria, quality checklist, and extraction fields unless the user explicitly asks to revise them. Assess whether the extraction fields will be sufficient to answer the research questions, and propose any necessary protocol modifications to the user before continuing.

### 2. Build the extraction codebook
Before extracting individual papers, create `extraction_codebook.json` from the protocol.

Coding rules:
- Treat any protocol field with explicit allowed options as a controlled field. Use the exact option labels from the protocol/codebook; do not invent synonyms.
- Treat protocol fields without explicit allowed options as open text unless they are clearly synthesis-critical and can be coded conservatively.
- When a protocol field allows `other`, code the controlled value as `other` and put the new label and explanation in `emergent_codes`; do not silently expand the enum.
- Distinguish `not_reported`, `not_applicable`, `none`, and `uncertain`.
- Do not assign a code from keyword presence alone. Assign a code only when the surrounding meaning supports it.
- Do not infer capabilities or limitations from silence alone. Absence-based limitation flags require either an explicit author statement or a completed extraction showing the relevant evidence fields are absent/not reported.
- Every selected controlled code that affects synthesis should have a rationale, a direct quote or location where possible, and a confidence rating.
- Preserve open observations even when they do not match the controlled vocabulary.

If the protocol does not define limitation flags, derive a small review-specific `limitation_flags` enum from the review questions, inclusion/exclusion criteria, quality checklist, and evidence fields. Keep these flags narrow and synthesis-oriented. For example, a nanosatellite/EPS MBSE review might use flags such as:
- `prototype_or_future_work`
- `single_case_or_limited_scope`
- `no_quantitative_evaluation`
- `no_baseline_or_comparator`
- `no_independent_validation`
- `no_physical_test_or_flight_evidence`
- `no_eps_specific_evidence`
- `assumptions_or_data_quality_limits`
- `tool_dependency_or_vendor_lockin`
- `interoperability_limitations`
- `learning_curve_or_training_burden`
- `model_not_available`
- `incomplete_lifecycle_coverage`

These flags are not a replacement for open limitation text. Store unexpected limitations in `emergent_limitations`.

### 3. Read and assess studies
Use `corpus_accessible.json` as the source list.
Read the markdown files in `markdown/` and:
- complete one extraction form per paper in `extractions/`
- include the protocol-based full extraction, the `structured_code_summary`, `structured_limitations`, and `emergent_codes`
- create an index of all extractions in `extraction.json`
- add cited final sources to `sources.bib`

For each study, extract in two passes:
1. **Open researcher pass:** capture relevant claims, methods, context, evidence, quotations, stated limitations, and extractor observations without forcing categories.
2. **Controlled coding pass:** map only well-supported findings to the codebook enums, with rationale, evidence, and confidence.

To avoid context pollution, run the individual extractions using subagents:

```bash
pi -p \
  --model openai-codex/gpt-5.5 \
  --thinking xhigh \
  --no-session \
  "Your prompt here"
```

Subagent guidelines:
- Silo subagents. They should only see the paper they need to extract information from in Markdown format, `protocol.md`, and `extraction_codebook.json`.
- Enforce exact controlled-code labels via your prompt.
- Require quotes/locations for synthesis-critical codes and claim-evidence records.
- Require emergent codes for important findings not covered by the codebook.
- Generate `extraction.json` and `sources.bib` yourself once all subagents have completed.

### 4. Validate and normalize
Before finishing:
- Parse every JSON file to ensure it is valid.
- Check that controlled-code values match `extraction_codebook.json` exactly, except values explicitly placed in `emergent_codes`.
- Check that every selected limitation flag has a rationale and evidence or a clear extractor-identified absence-based explanation.
- Check that no field has been coded only because a keyword appeared.
- Normalize inconsistent labels and rerun or repair weak extractions when needed.

Iterate and reflect on your work: are you confident that you are delivering a high-quality result?
