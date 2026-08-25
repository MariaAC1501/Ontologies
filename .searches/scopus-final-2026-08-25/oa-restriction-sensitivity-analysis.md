# Final OA-restriction sensitivity analysis — 2026-08-25

**Status:** metadata-only, pre-screening sensitivity analysis. It compares the final OA S1 candidate set with the complement of the matched all-access S2 universe. It is not a screened or included-study analysis.

## Retrieval and reconciliation

S2a was formed by deleting only the leading `OPENACCESS(1) AND ` predicate from S1a. S2b was formed the same way from S1b, then retrieved as disjoint 2025 and 2026 partitions because the unpartitioned API run hit a 200-page rate ceiling. The partition totals sum to the unpartitioned source total. Repeated API passes were reconciled by Scopus Paper ID only when their unique-ID union equalled the stable source total.

| Stratum | Source total | Recovery passes | Unique reconciled IDs |
|---|---:|---:|---:|
| S1a | 1,219 | 3 | 1,219 |
| S1b | 1,642 | 1 | 1,642 |
| S2a | 4,156 | 4 | 4,156 |
| S2b | 5,168 | 8 | 5,168 |

## Matched comparison universe

| Transition | Records |
|---|---:|
| Raw OA S1 source records | 2,861 |
| Distinct OA S1 records | 2,770 |
| Raw all-access S2 source records | 9,324 |
| Distinct all-access S2 records | 9,036 |
| Matched OA records in all-access universe | 2,770 (30.7%) |
| All-access complement (called non-OA here) | 6,266 (69.3%) |
| Unmatched OA records excluded from comparison | 0 |

`non-OA` means the complement of the matched OA set in the all-access candidate universe; it is not a separately verified licence classification.

## Year and retrieval-anchor composition

| Dimension | OA | Non-OA | OA availability |
|---|---:|---:|---:|
| 2025 | 1,535 (55.4%) | 3,762 (60.0%) | 29.0% |
| 2026 | 1,235 (44.6%) | 2,504 (40.0%) | 33.0% |
| Maintenance/prognostic-anchor only | 1,128 (40.7%) | 2,741 (43.7%) | 29.2% |
| Diagnostic/condition-anchor only | 1,552 (56.0%) | 3,329 (53.1%) | 31.8% |

The 2026 component remains incomplete because the source was searched before the end of the year.

## Textual similarity

Title-plus-abstract unigram/bigram document-frequency profiles had cosine similarity **0.988** and Jensen--Shannon divergence **0.275**. Their top-term overlap was 17 of 20 and 89 of 100.

A five-fold held-out text-only OA-status classifier had AUC **0.66** and balanced accuracy **0.61** (0.50 is chance).

## Title/abstract topic markers

Markers are transparent multi-label text checks, not screening labels, OPMAD annotations, or evidence of model superiority.

| Marker | OA | Non-OA | Difference (pp) | OA availability |
|---|---:|---:|---:|---:|
| RUL / remaining-useful-life terms | 687 (24.8%) | 1,814 (28.9%) | -4.1 | 27.5% |
| Life-prediction or prognostic terms | 560 (20.2%) | 1,447 (23.1%) | -2.9 | 27.9% |
| Fault-diagnosis terms | 705 (25.5%) | 1,542 (24.6%) | +0.8 | 31.4% |
| Fault-detection terms | 521 (18.8%) | 1,085 (17.3%) | +1.5 | 32.4% |
| Anomaly-detection terms | 371 (13.4%) | 713 (11.4%) | +2.0 | 34.2% |
| Predictive-maintenance or CBM terms | 1,006 (36.3%) | 2,087 (33.3%) | +3.0 | 32.5% |
| Bearing terms | 527 (19.0%) | 1,115 (17.8%) | +1.2 | 32.1% |
| Transformer terms | 310 (11.2%) | 773 (12.3%) | -1.1 | 28.6% |
| Engine or turbofan terms | 224 (8.1%) | 502 (8.0%) | +0.1 | 30.9% |
| Battery terms | 221 (8.0%) | 587 (9.4%) | -1.4 | 27.4% |
| Lithium-ion battery terms | 152 (5.5%) | 382 (6.1%) | -0.6 | 28.5% |
| Wind-turbine terms | 149 (5.4%) | 285 (4.5%) | +0.8 | 34.3% |
| Motor terms | 234 (8.4%) | 478 (7.6%) | +0.8 | 32.9% |
| Gearbox terms | 50 (1.8%) | 92 (1.5%) | +0.3 | 35.2% |
| CNN or convolutional-neural-network terms | 470 (17.0%) | 818 (13.1%) | +3.9 | 36.5% |
| LSTM or long-short-term-memory terms | 476 (17.2%) | 915 (14.6%) | +2.6 | 34.2% |
| Deep-learning terms | 583 (21.0%) | 1,225 (19.5%) | +1.5 | 32.2% |
| Physics-informed/guided/aware terms | 103 (3.7%) | 194 (3.1%) | +0.6 | 34.7% |
| Transfer-learning terms | 89 (3.2%) | 213 (3.4%) | -0.2 | 29.5% |
| Domain-adaptation/generalisation terms | 59 (2.1%) | 188 (3.0%) | -0.9 | 23.9% |
| Digital-twin terms | 107 (3.9%) | 259 (4.1%) | -0.3 | 29.2% |
| C-MAPSS terms | 140 (5.1%) | 303 (4.8%) | +0.2 | 31.6% |
| Case-Western terms | 56 (2.0%) | 65 (1.0%) | +1.0 | 46.3% |
| F1 terms | 310 (11.2%) | 435 (6.9%) | +4.2 | 41.6% |
| RMSE terms | 243 (8.8%) | 441 (7.0%) | +1.7 | 35.5% |
| AUC terms | 109 (3.9%) | 143 (2.3%) | +1.7 | 43.3% |

## DOI-prefix source/platform proxy

| Prefix | All access | OA | OA rate | OA / non-OA share |
|---|---:|---:|---:|---:|
| 10.1109 | 3,014 | 198 | 6.6% | 7.1% / 44.9% |
| 10.3390 | 787 | 787 | 100.0% | 28.4% / 0.0% |
| 10.1016 | 1,658 | 498 | 30.0% | 18.0% / 18.5% |
| 10.1007 | 1,010 | 122 | 12.1% | 4.4% / 14.2% |
| 10.1038 | 124 | 124 | 100.0% | 4.5% / 0.0% |

## Interpretation

The comparison characterizes the final retrieved candidate population, not included studies. It supports OA-scoped claims only. Any substantive mapping result must still be based on screened, full-text-verified studies and validated extraction fields.
