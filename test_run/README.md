# OntoCast test checkpoint

This directory preserves the useful artifacts from the OntoCast debugging session.

## Kept artifacts

- `BUG_REPORT.md` — detailed notes on the bugs found and the local patches applied to the installed OntoCast package during testing
- `working_dir/ontology_iiopm_1.0.1.ttl` — ontology output from the successful patched run using `gpt-5-nano`
- `working_dir/facts_5cc89b5bfaf6.ttl` — facts output from the same successful run

## Not kept

The following were intentionally removed before commit:

- `.env` / API key material
- scratch issue-body markdown files
- transient run logs
- copied input PDF duplicate

## Related local issues

- `MariaAC1501/Ontologies#1` — checkpoint for the successful patched run
- `MariaAC1501/Ontologies#2` — planned re-test with `gpt-4o`
- `MariaAC1501/Ontologies#3` — design review on ontology provenance / RDF-star triple-terms

## Important note

The successful run depended on **local patches to the installed OntoCast package** inside the conda environment. These artifacts document where we left off; they do not mean upstream OntoCast is fixed yet.
