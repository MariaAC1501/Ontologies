# OntoCast Run Logbook

Concisely log the rationale and the result for each run. No need for lengthy discussions or supplementary files, all the evidence is in the run logs.
Technical failures (i.e. timeouts, connection losses) are deleted, retried and not logged here.

| Run | Rationale | Result |
|--|--|--|
| pilot-s001-r1 | Test minimal prompt. | Extractions included cases from citations, not the paper itself. |
| pilot-s001-own-cases-600s | Update prompt to exclude citations from extractions, raise timeout to 600 seconds. Same paper as previous run. | Less extracted cases than the reference. |
| pilot-four-more | Gather more evidence of extraction behavior. 4 new papers. | Number of cases is larger than the reference. Duplicate cases. The definition of a case may still be ambiguous. PDF conversion issues. |
| pilot-five-terra | Same 5 previous papers. Same prompt. Tests `gpt-6.1-terra` since `gpt-6.1-sol` took ~75 minutes on the last run. | Terra is noticeably faster, no visible performance hit, will be benchmarked from now on. Both Terra and Sol produce considerably more facts than the human baseline. The definition of case needs to be improved before running larger pilots. |
| pilot-five-terra-case-definition | Same 5 papers and `gpt-6.1-terra`. New prompt with explicit case definition. | All 5 papers completed in ~75 minutes. 55 case nodes vs. 17 in the human baseline (previous Terra prompt: 59). |
| pilot-s003-terra-case-definition-debug | Rerun S003 with the same case-definition prompt and `gpt-6.1-terra`, enabling DEBUG logs to inspect rejected entity merges. | 11 case nodes vs. 1 human case. OntoCast extracts chunk-by-chunk by default. Multiple nodes refer to the same case, and correspondingly have high embedding similarity, but the OntoCast merger also applies symbolic and lexical checks. These later checks were failed because nodes have equivalent but not identical identifiers, even when they relate to the same systems through valid ontological links. This could be caused by the same entities being referred to using different wording across chunks. OntoCast exposes chunk size controls, but merging only happens between neighboring chunks under the same section, as labelled by the bundled PDF processor. The checks can't all be disabled via OntoCast configuration. |
| pilot-s003-terra-cross-section-large-chunks | S003 with `gpt-6.1-terra` and the same case-definition prompt. Apply the experimental cross-section-merging patch and raise chunk bounds from 3,000–12,000 to 48,000–96,000 characters. Keep section filtering and DEBUG logging. | 1 content unit instead of 13. 1 case node vs. 1 human case. |
