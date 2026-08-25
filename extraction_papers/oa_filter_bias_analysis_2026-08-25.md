# OA-filter bias analysis — 2026-08-25 pilot

## Decision

**Do not accept these raw pilot exports as the paper's final corpus yet.** They are useful as a documented sensitivity pilot. The OA restriction itself is defensible for claims explicitly limited to *English-language, Scopus-indexed OA studies*: the companion title/abstract analysis finds a broadly comparable subset with moderate topic differences. It must not support field-wide claims, and the records still need a final search, deduplication, screening, and full-text verification.

## What was compared

The four complete Scopus exports were checked against their commit markers (all CSV hashes and byte counts match). S2 is a valid metadata sensitivity counterpart to S1: for each query, it removes exactly the leading `OPENACCESS(1) AND ` clause and changes nothing else.

| Search block | OA-filtered S1 rows | No-OA-filter S2 rows |
|---|---:|---:|
| Prognostic title anchor (a) | 622 | 2,226 |
| Diagnostic title anchor (b) | 559 | 1,629 |

All records have a Scopus Paper ID, so Paper ID was used for deduplication. “No OA filter” means all access statuses; “non-OA” below means the complement of the OA-filtered set in that all-status universe.

## Size and data-quality result

| Step | Records |
|---|---:|
| Raw S1 rows | 1,181 |
| Distinct S1 OA records | 1,154 |
| Raw S2 rows | 3,855 |
| Distinct S2 all-status records | 3,759 |
| Matched OA records in the S2 universe | 1,153 (30.7%) |
| Non-OA records in the S2 universe | 2,606 (69.3%) |

The OA filter therefore removes about **seven in ten** candidate records.

The raw exports cannot be used directly: S1a/S1b overlap by 27 records; S2a/S2b overlap by 85; S2a contains 7 repeated Paper IDs and S2b contains 4. One OA diagnostic record (`105035066397`) is absent from the S2b export obtained about five minutes later. It was excluded only from the matched comparison; it does not change the conclusion. This shows why a final run needs a deterministic deduplication manifest and a single documented search cutoff.

## Where the OA subset differs

### Year and retrieval-anchor composition

| Dimension | OA | Non-OA | OA availability in all-status set |
|---|---:|---:|---:|
| 2025 | 603 / 1,153 (52.3%) | 1,528 / 2,606 (58.6%) | 603 / 2,131 (28.3%) |
| 2026 | 550 / 1,153 (47.7%) | 1,078 / 2,606 (41.4%) | 550 / 1,628 (33.8%) |
| Prognostic-anchor only | 595 / 1,153 (51.6%) | 1,539 / 2,606 (59.1%) | 27.9% |
| Diagnostic-anchor only | 531 / 1,153 (46.1%) | 1,009 / 2,606 (38.7%) | 34.5% |

The OA set is more recent and is relatively more diagnostic. The 2026 comparison is additionally unstable because the search occurred on 25 August, before the year was complete.

### Title/abstract topic proxies

The following are transparent multi-label keyword checks over title and abstract, **not screening labels or final OPMAD annotations**. They show the same task imbalance as the search-anchor comparison.

| Proxy topic | OA | Non-OA | Difference (OA − non-OA) |
|---|---:|---:|---:|
| RUL / life-prognostic terms | 411 (35.6%) | 1,178 (45.2%) | **−9.6 percentage points** |
| Fault / anomaly diagnosis terms | 598 (51.9%) | 1,147 (44.0%) | **+7.9 percentage points** |
| Bearings / gears / rotors | 392 (34.0%) | 841 (32.3%) | +1.7 percentage points |
| Electrical / energy assets | 361 (31.3%) | 817 (31.4%) | −0.0 percentage points |

A title-only check gives the same direction for the two task results (RUL/life: −8.7 points; fault/anomaly: +6.9 points). Broad asset proxies are comparatively stable, but the task distribution that the paper intends to map is not.

### Source/platform skew

DOI prefixes are a conservative source/platform proxy because publication-title fields are blank in these exports. The skew is large:

| DOI prefix | All-status records | OA records | OA rate | Share of OA / non-OA sets |
|---|---:|---:|---:|---:|
| `10.1109` (IEEE) | 1,195 | 81 | 6.8% | 7.0% / 42.7% |
| `10.3390` (MDPI) | 351 | 351 | 100.0% | 30.4% / 0.0% |
| `10.1016` (Elsevier) | 770 | 210 | 27.3% | 18.2% / 21.5% |
| `10.1007` (Springer) | 432 | 50 | 11.6% | 4.3% / 14.7% |
| `10.1038` | 57 | 57 | 100.0% | 4.9% / 0.0% |

In particular, the OA corpus retains only 81 of 1,195 `10.1109` records while it retains every `10.3390` record. This is material source and likely document-format bias, not a random 31% sample of the retrieved literature.

## Screening and eligibility considerations

This is still a candidate set, not an included-study corpus. A conservative title audit found at least 10 clearly out-of-scope records under the stated eligibility criteria: one IT contact-centre incident-forecasting paper, six tree/crop/soil-health papers, and three road/asphalt-network papers. Seven are in the OA subset. This is a lower bound, not a precision estimate; implementation, engineered-item, review, and full-text eligibility have not been screened. It confirms the warning in `.searches/scopus-query-pilot-2026-08-25/README.md` that the full exports contain residual out-of-field noise.

The exports also leave `Publication title`, `Publication date`, `Document type`, and `Open access PDF` blank. Thus they cannot establish journal/document-type composition, a usable OA full text, or an OA licence. Citation counts are very immature and should not be interpreted as evidence quality.

## Required action before acceptance

1. Keep these four files as a pilot and OA-bias sensitivity artifact; do not merge S2 into the full-text corpus.
2. Freeze the search and apply the prespecified, auditable screening workflow to residual out-of-field records.
3. Re-run the final S1/S2 pair, deduplicate by Paper ID/DOI/normalised title, and retain a versioned deduplication manifest.
4. Screen the final OA candidates for the implemented diagnostic/prognostic model and engineered maintainable-item criteria; record exclusions.
5. Retrieve and verify a matching usable OA full text and licence for every included study.
6. Repeat this metadata comparison on the final query and limit all synthesis claims to the OA Scopus population. Do not generalise model or task prevalence to predictive-maintenance research as a whole.
