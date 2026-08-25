# Final Scopus pre-screening run — 2026-08-25

**Status:** frozen identification-stage retrieval under strategy version 1.1. This is **not** a title/abstract-screened, full-text-screened, or included-study corpus.

## Scope and frozen strategy

- Source: Scopus Developer API via `search_scopus.py`.
- Search-date cutoff: 2026-08-25.
- Limits in both queries: English, open access, journal article or conference paper, and publication year 2025--2026.
- S1a is the maintenance/prognostic title-anchor stratum; S1b is the diagnostic/condition title-anchor stratum.
- Both queries require an engineered-asset context. CBM, PHM, and RUL acronyms occur only in functional context. The strategy avoids broad medical, cloud, and civil exclusions that could suppress eligible equipment studies.

Immutable query companions:

| Query | File | SHA-256 |
|---|---|---|
| S1a | `S1a-maintenance-prognostic-oa.scopus.txt` | `9e699fcba307496cab5aeaab9b42c939e9ba67c488cfc0f6b00f0c61fbedfda5` |
| S1b | `S1b-diagnostic-condition-oa.scopus.txt` | `17a889199f8be82fdbbe12af71bec20ec5fdd82c5452a4f69760c118e2229816` |

## Complete source retrieval

| Stratum | UTC execution | Source total | Pages per pass | Recovery result |
|---|---|---:|---:|---|
| S1a | 16:35:25--16:47:32 | 1,219 | 49 | Three complete passes reconciled to 1,219 unique Scopus Paper IDs |
| S1b | 16:37:12--16:39:16 | 1,642 | 66 | One complete pass; 1,642 unique Scopus Paper IDs |

The legacy API adapter reported S1a complete but returned duplicate page rows: three repeats in pass 1, three in pass 2, and one in pass 3. All three passes had the same 1,219 source total. Their unique Scopus-Paper-ID union was exactly 1,219, so it was used as the reconciled S1a result. The repeat files are technical recovery passes, not additional search sources or additional PRISMA records.

Each JSON/CSV pair has a matching `.ACADEMIC_SEARCH_COMMIT.json` marker that verifies its bytes and SHA-256 hash. The reconciliation receipt validates those markers and verifies that every API executed query matches its archived query companion. The raw JSON/CSV archive remains local rather than being committed to Git; its hashes, byte counts, and marker receipts are retained in `pre-screening-accounting.json`.

## Final pre-screening accounting

| Transition | Records |
|---|---:|
| Reconciled S1a source records | 1,219 |
| S1b source records | 1,642 |
| Records before cross-stratum deduplication | 2,861 |
| Shared S1a/S1b Scopus Paper IDs | −90 |
| Additional same-DOI record with a distinct Scopus Paper ID | −1 |
| **Unique pre-screening candidates** | **2,770** |

The DOI duplicate is one 2025 wind-turbine article (`10.3390/ijtpp10030014`) indexed under Paper IDs `105017000119` and `105018056402`; its normalized title also matches. There were no unresolved normalized-title/year collisions. The union contains 1,535 records dated 2025 and 1,235 dated 2026. All 2,770 records have a Scopus Paper ID, DOI, title, year, and abstract.

`pre-screening-union.json` contains canonical database records and S1a/S1b membership. `pre-screening-accounting.json` contains all 91 cross-query/DOI duplicate events, the complete-pass receipts, and input hashes.

## Coverage and reproduction checks

A comparison with the 1,154 unique records in the earlier S1a/S1b pilot found only two direct-ID absences:

1. `105018056402`, which is represented by its same-DOI Scopus alias `105017000119`; and
2. `105021669246`, the intentionally excluded contact-centre IT incident-forecasting study.

Thus, the final strategy retained the earlier in-scope pilot coverage while deliberately excluding the documented IT outlier.

The union was built with `scripts/build_scopus_pre_screening_union.py` (SHA-256 `d0a8173e78ffc0653ba8d5ecce9ec57bc00102936b4240ce0bb898261419162f`). It verifies complete source runs, query echoes, commit markers, S1a recovery-pass totals, and DOI/EID/title accounting before it writes the derived JSON files.

No eligibility decision, full-text retrieval, bibliographic verification, licence verification, or screening conflict resolution has occurred. Residual clinical, civil/structural, IT, and generic-method noise remains for the prespecified screening workflow. The earlier no-OA S2 pilot is not part of this final candidate union and must not be reported as a final sensitivity result.
