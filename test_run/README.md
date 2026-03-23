# OntoCast test checkpoint

This directory preserves the useful artifacts from the OntoCast debugging session.

## Current interpretation

These artifacts now serve mainly as a record of why we are narrowing scope.

For this repo, OntoCast is no longer being treated as something we must get fully working across its whole ontology-development feature set before proceeding. The current plan is to use it only in the smaller role we actually need: a constrained extractor for the predictive-maintenance CBR workflow, preferably against a fixed ontology.

Any future comparison between that fixed-ontology path and a more evolved-ontology path is deferred and explicitly experimental.

## Kept artifacts

- `working_dir/ontology_iiopm_1.0.1.ttl` — ontology output from the successful patched run using `gpt-5-nano`
- `working_dir/facts_5cc89b5bfaf6.ttl` — facts output from the same successful run

## `gpt-4o` re-test summary

A follow-up re-test was completed against the same patched local environment using `gpt-4o` and the same `example_paper.pdf` input.

Outcome:
- the run completed end-to-end
- ontology chunk processing salvaged output from `5/5` non-converged loops
- facts chunk processing salvaged output from `5/5` non-converged loops
- the exact earlier `systemic_critique_summary` list-vs-string mismatch from the `gpt-5-nano` run was **not** reproduced in that run
- however, the broader prompt/schema/convergence fragility clearly still affected `gpt-4o`

We intentionally did **not** keep the transient `gpt-4o` run directory and logs here. The durable record for that re-test lives in the local issue tracker instead.

Earlier local bug-report notes were also moved into GitHub issue comments before removing `test_run/BUG_REPORT.md`.

## Not kept

The following were intentionally removed before commit:

- `.env` / API key material
- scratch issue-body markdown files
- transient run logs
- copied input PDF duplicate

## Related local issues

- `MariaAC1501/Ontologies#1` — checkpoint for the successful patched run
- `MariaAC1501/Ontologies#2` — completed `gpt-4o` re-test
- `MariaAC1501/Ontologies#3` — design review on ontology provenance / RDF-star triple-terms
- `MariaAC1501/Ontologies#4` — checkpoint that upstream prompt/schema/convergence hardening is still needed after the `gpt-4o` re-test

## Important note

The successful run depended on **local patches to the installed OntoCast package** inside the conda environment. These artifacts document where we left off; they do not mean upstream OntoCast is fixed yet.
