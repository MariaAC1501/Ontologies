# Derived-artifact history

The raw S1a/S1b API JSON/CSV exports and commit markers in this directory are immutable and retained.

Two interim derived pre-screening unions were produced while validating the local reconciliation script on 2026-08-25:

1. the first omitted repeated S1a page rows from its displayed duplicate arithmetic; and
2. the second used only the first unstable S1a page pass.

They were not source exports, were never used for screening, and were removed after the corrected reconciliation recorded all three S1a passes. The canonical files are `pre-screening-accounting.json` and `pre-screening-union.json`; both use the version-2 schemas and reconcile 1,219 unique S1a IDs to the stable source total before cross-stratum deduplication.
