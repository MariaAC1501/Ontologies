# OntoCast Run Logbook

Concisely log the rationale and the result for each run. No need for lengthy discussions or supplementary files, all the evidence is in the run logs.

| Run | Rationale | Result |
|--|--|--|
| pilot-s001-r1 | Test minimal prompt. | Extractions included cases from citations, not the paper itself. |
| pilot-s001-own-cases-600s | Update prompt to exclude citations from extractions, raise timeout to 600 seconds. Same paper as previous run. | Less extracted cases than the reference. |
| pilot-four-more | Gather more evidence of extraction behavior. 4 new papers. | Number of cases is larger than the reference. Duplicate cases. The definition of a case may still be ambiguous. PDF conversion issues. |
| pilot-five-terra | Same 5 previous papers. Same prompt. Tests `gpt-6.1-terra` since `gpt-6.1-sol` took ~75 minutes on the last run. | Terra is noticeably faster, no visible performance hit, will be benchmarked from now on. Both Terra and Sol produce considerably more facts than the human baseline. The definition of case needs to be improved before running larger pilots. |
