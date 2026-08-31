# Full-text audit

This is a deterministic preflight of the 32 page-delimited Markdown conversions under `markdown/`. It is not extraction evidence and does not replace human eligibility or annotation.

Command:

```bash
python3 -m pipeline.fulltext audit \
  --input 'markdown/*/document.md' \
  --output /tmp/fulltext-audit.json
```

Result:

- 32 of 32 documents passed.
- 691 expected page markers were present in sequence.
- No missing, repeated, out-of-order, or unexpected page marker was detected.
- No duplicated-page pair or publisher-boilerplate dominance was detected.
- One intentionally sparse final page had fewer than 80 text characters. Its document remained below the low-text failure threshold.
- The source-map pass identified 9,949 page-linked blocks and 226 structured table blocks.

The publication preparation path runs the same checks after Docling conversion. A failed selective-OCR conversion is retried with full-page OCR before extraction starts.

Live no-LLM smoke tests on 2026-08-31 used OntoCast 0.3.0, Docling 2.124.0, Docling Core 2.92.0, Docling Parse 7.16.0, and EasyOCR 1.7.2:

- The complete 10-page CNC article passed with five retained tables and 112 page-linked blocks.
- The complete 25-page multi-function servomotor article passed with four retained tables and 195 page-linked blocks.

Neither conversion had a missing, sparse, duplicated, or truncated page. A separate image-only PDF fixture also passed through the forced full-page EasyOCR route and returned all four expected text lines.
