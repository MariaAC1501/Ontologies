# Predictive Maintenance Screening Results

Date updated: 2026-06-11  
Source CSV: `extraction_papers/scopus_export_May 26-2026.csv`  
Criteria: `extraction_papers/predictive_maintenance_inclusion_exclusion_criteria.md`

## Scope update

The active corpus now keeps records with clear relevance to predictive maintenance / condition-based maintenance / PHM / RUL / fault diagnosis / asset degradation for in-scope physical equipment or components. Civil/geotechnical/infrastructure-only monitoring, generic non-maintenance AI/process/performance papers, and subagent-flagged controversial review-exclude papers have been excluded.

## Output files

| File | Description |
|---|---|
| `extraction_papers/scopus_export_May 26-2026_screened.csv` | All 3,990 records with current screening columns |
| `extraction_papers/scopus_export_May 26-2026_included.csv` | Included records only |
| `extraction_papers/scopus_export_May 26-2026_excluded.csv` | Excluded records only |
| `extraction_papers/failed_pdfs_screened.csv` | Failed-PDF list with current screening decision |
| `extraction_papers/failed_pdfs_included_for_retry.csv` | Failed-PDF records still worth retrying |
| `extraction_papers/failed_pdfs_excluded_outliers.csv` | Failed-PDF records excluded as outliers |
| `extraction_papers/generic_nonmaintenance_newly_excluded_applied.csv` | Generic non-maintenance exclusions applied |
| `extraction_papers/controversial_review_exclude_applied.csv` | Controversial scan exclusions applied |
| `extraction_papers/controversial_papers_candidates_remaining_included.csv` | Remaining borderline `review_keep` candidates |

## Current all-record screening counts

| Decision | Count |
|---|---:|
| included | 2768 |
| excluded | 1222 |

## Included records by reason category

| Reason category | Count |
|---|---:|
| physical_asset_maintenance | 2748 |
| uncertain_but_included | 20 |

## Included records by confidence

| Confidence | Count |
|---|---:|
| high | 2603 |
| medium | 161 |
| low | 4 |

## Current excluded records by reason category

| Reason category | Count |
|---|---:|
| generic_nonmaintenance_ai_control | 394 |
| environment_natural_system | 297 |
| other_nonmaintenance | 215 |
| software_it_cyber | 123 |
| clinical_human_outcome | 80 |
| business_social_finance | 61 |
| acronym_collision | 28 |
| biology_biotech_non_equipment | 24 |

## Current failed-PDF counts

| Decision | Count |
|---|---:|
| included | 946 |
| excluded | 441 |

## Current excluded failed-PDF records by reason category

| Reason category | Count |
|---|---:|
| generic_nonmaintenance_ai_control | 140 |
| environment_natural_system | 105 |
| other_nonmaintenance | 88 |
| software_it_cyber | 48 |
| clinical_human_outcome | 30 |
| business_social_finance | 14 |
| acronym_collision | 10 |
| biology_biotech_non_equipment | 6 |

## Controversial scan pass

| Item | Count |
|---|---:|
| Controversial review-exclude candidates applied | 112 |
| Remaining borderline review-keep candidates | 153 |

See `controversial_papers_scan_report.md` for details.

## PDF cleanup

| Cleanup manifest | PDFs removed |
|---|---:|
| `extraction_papers/removed_excluded_pdfs_manifest.csv` | 450 |
| `extraction_papers/removed_strict_irrelevant_pdfs_manifest.csv` | 59 |
| `extraction_papers/removed_civil_infra_pdfs_manifest.csv` | 133 |
| `extraction_papers/removed_generic_nonmaintenance_pdfs_manifest.csv` | 61 |
| `extraction_papers/removed_controversial_review_exclude_pdfs_manifest.csv` | 78 |

Current remaining paper PDFs: **1822**  
Current remaining PDFs for excluded records: **0**

## Notes

- `paper-3804` is excluded: highway-tunnel surrounding-rock deformation / construction geotechnical monitoring.
- The final generic non-maintenance audit removed 94 likely out-of-scope included records.
- The controversial scan removed another 112 review-exclude records.
- For retrying PDF retrieval, use `failed_pdfs_included_for_retry.csv` or the included CSV, not the original unfiltered Scopus export.
