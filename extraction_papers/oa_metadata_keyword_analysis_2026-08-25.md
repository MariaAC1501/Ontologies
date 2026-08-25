# Title/abstract keyword analysis — OA versus no OA filter

## What the available metadata supports

Yes: all four pilot exports contain a title and abstract for every record, so they support a **text-derived keyword and topic-marker analysis**. They do **not** contain author keywords, Scopus indexed keywords, controlled subject terms, full text, affiliations, or source titles. The results below are therefore title/abstract metadata signals, not author-keyword results and not final OPMAD annotations.

This companion analysis uses the matched, deduplicated comparison set from `oa_filter_bias_analysis_2026-08-25.md`:

- OA-filtered: **1,153** records
- no-OA-filter complement: **2,606** records
- total all-status candidate set: **3,759** records

Each marker is counted once per title-plus-abstract, case-insensitively. Markers are multi-label, so rows do not sum to the corpus total. The percentages are descriptive of the retrieved records, not estimates from a sample.

## Overall textual similarity

The two sets are **broadly similar in topic**, rather than sharply separated corpora. After removing generic scientific and query wording, a unigram/bigram document-frequency comparison found:

- cosine similarity: **0.977** (1.0 is identical);
- Jensen--Shannon divergence: **0.022** (0 is identical);
- overlap of 18 of the 20, and 83 of the 100, most prevalent terms; and
- a five-fold held-out, text-only OA-status classifier with AUC **0.65** and balanced accuracy **0.61** (0.50 is chance). Within the prognostic and diagnostic search-anchor strata, AUC was 0.63 and 0.64.

Thus, the terms below identify moderate, interpretable differences within a largely overlapping literature. They do **not** justify describing the OA set as wholesale topical skew. The sharpest difference remains source/platform coverage, especially the loss of IEEE-prefix records; that is a scope limitation rather than a reason to reject an explicitly OA-only review.

## Function keywords

| Text marker | OA | Non-OA | Difference | OA availability |
|---|---:|---:|---:|---:|
| `remaining useful life`, `remaining useful lifetime`, or `RUL` | 410 (35.6%) | 1,174 (45.0%) | **−9.5 pp** | 25.9% |
| life-prediction or prognos* terms | 320 (27.8%) | 936 (35.9%) | **−8.2 pp** | 25.5% |
| fault diagnos* | 352 (30.5%) | 668 (25.6%) | +4.9 pp | 34.5% |
| fault detect* | 255 (22.1%) | 462 (17.7%) | +4.4 pp | 35.6% |
| anomaly detect* | 135 (11.7%) | 253 (9.7%) | +2.0 pp | 34.8% |
| `predictive maintenance` or `condition-based maintenance` | 567 (49.2%) | 1,130 (43.4%) | +5.8 pp | 33.4% |

The main finding is robust: RUL/life-prognostic language is substantially less frequent in the OA subset. In the prognostic-anchor-only stratum, RUL appears in 65.9% of OA records versus 74.4% of non-OA records (−8.5 points), so this is not only caused by mixing the two search blocks.

The overall fault-diagnosis difference mainly reflects query composition: the OA set has a greater share of diagnostic-anchor records. Within the diagnostic-anchor-only stratum, `fault diagnos*` is nearly identical (61.6% OA; 61.2% non-OA). It should therefore be described as a corpus-composition difference, not an independent OA association.

## Asset keywords

| Text marker | OA | Non-OA | Difference | OA availability |
|---|---:|---:|---:|---:|
| bearing(s) | 301 (26.1%) | 685 (26.3%) | −0.2 pp | 30.5% |
| transformer(s) | 167 (14.5%) | 367 (14.1%) | +0.4 pp | 31.3% |
| engine(s) or turbofan(s) | 151 (13.1%) | 351 (13.5%) | −0.4 pp | 30.1% |
| battery / batteries | 123 (10.7%) | 362 (13.9%) | **−3.2 pp** | 25.4% |
| lithium-ion battery | 86 (7.5%) | 243 (9.3%) | −1.9 pp | 26.1% |
| wind turbine | 76 (6.6%) | 119 (4.6%) | +2.0 pp | 39.0% |
| motor(s) | 146 (12.7%) | 286 (11.0%) | +1.7 pp | 33.8% |
| gearbox(es) | 30 (2.6%) | 43 (1.7%) | +1.0 pp | 41.1% |

Bearings, transformers, and engines have similar representation in both sets. Batteries are less represented in OA; wind-turbine language is more represented. These are modest but relevant differences for a model-selection map.

## Method, benchmark, and evaluation keywords

| Text marker | OA | Non-OA | Difference | OA availability |
|---|---:|---:|---:|---:|
| CNN / convolutional neural network | 221 (19.2%) | 382 (14.7%) | +4.5 pp | 36.7% |
| LSTM / long short-term memory | 259 (22.5%) | 478 (18.3%) | +4.1 pp | 35.1% |
| deep learning | 292 (25.3%) | 594 (22.8%) | +2.5 pp | 33.0% |
| physics-informed, physics-guided, or physics-aware | 52 (4.5%) | 95 (3.6%) | +0.9 pp | 35.4% |
| transfer learning | 36 (3.1%) | 95 (3.6%) | −0.5 pp | 27.5% |
| domain adaptation or domain generalisation | 26 (2.3%) | 100 (3.8%) | −1.6 pp | 20.6% |
| digital twin | 35 (3.0%) | 95 (3.6%) | −0.6 pp | 26.9% |
| C-MAPSS | 93 (8.1%) | 209 (8.0%) | +0.0 pp | 30.8% |
| Case Western Reserve | 36 (3.1%) | 30 (1.2%) | +2.0 pp | 54.5% |
| F1 | 134 (11.6%) | 156 (6.0%) | +5.6 pp | 46.2% |
| RMSE | 150 (13.0%) | 263 (10.1%) | +2.9 pp | 36.3% |
| AUC | 54 (4.7%) | 48 (1.8%) | +2.8 pp | 52.9% |

The OA records use more CNN/LSTM and classification-metric language, while domain-adaptation language is less represented. The LSTM difference remains within the prognostic-anchor-only stratum (29.9% OA versus 22.3% non-OA). The higher F1 rate also remains within both main strata, so it may affect which evaluation evidence is easy to extract from an OA-only corpus. These are reporting/topic signals, **not evidence that one model or metric is better**.

## Interpretation and use

1. The keyword evidence supports calling the OA set a **broadly comparable but incomplete OA subset**, not a strongly topic-skewed replacement for the all-status set. It is relatively lighter on RUL, batteries, domain adaptation, and `10.1109` (IEEE-prefix) material, and relatively heavier on diagnostic, CNN/LSTM, and classification-metric language.
2. It is useful for final-corpus screening and validation strata: retain coverage of RUL, diagnosis, batteries, wind, CNN/LSTM, domain adaptation, and source/platform groups.
3. Do not use these metadata keyword counts as final findings. Recalculate them after final screening and full-text verification, then use validated OPMAD case annotations for the paper's substantive evidence map.
4. **Accept the OA restriction as the paper's defined population if claims remain OA-scoped.** Do not yet freeze these raw pilot exports as the final corpus: they still need a final search, deduplication, screening, and full-text/licence verification.
