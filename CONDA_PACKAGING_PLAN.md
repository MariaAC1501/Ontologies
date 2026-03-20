# Conda packaging plan for CBR

This repository is moving toward a Conda-first setup where:

- `ontocast` is installed into the Conda environment as a Python dependency
- the Java CBR tooling is packaged as a Conda package
- colleagues can create one environment and get Python + Java + the CBR CLI in one step

## Packaging target

The CBR Conda package installs:

- `share/ontologies-cbr/ontologies-cbr-headless.jar`
- `share/ontologies-cbr/lib/*.jar` from upstream `external-libs`
- `share/ontologies-cbr/data/*` ontology and sample data assets
- `bin/ontologies-cbr` thin CLI wrapper

## CLI contract

Primary command:

```bash
ontologies-cbr help
ontologies-cbr rebuild --csv "CleanedDATA V12-05-2021.csv"
ontologies-cbr query-batch input_file.csv retrieval_results
```

The CLI resolves its data directory in this order:

1. `--data-dir DIR`
2. `ONTOLOGIES_CBR_DATA_DIR`
3. repository-local default during development
4. `$CONDA_PREFIX/share/ontologies-cbr/data`

## Files added for Conda route

- `environment.yml` — top-level environment definition
- `conda/recipes/ontologies-cbr/meta.yaml` — Conda package recipe
- `conda/recipes/ontologies-cbr/build.sh` — package build/install script
- `conda/recipes/ontocast/` — Conda recipe for OntoCast
- `conda/recipes/ontologies-stack/` — meta-package that installs both
- `scripts/build_conda_packages.sh` — build all local packages and index the local channel
- `scripts/create_conda_env.sh` — create an environment from the local package channel

## Local development flow

Build the jar locally:

```bash
bash scripts/build_cbr.sh
```

Run the local CLI wrapper:

```bash
bash scripts/run_cbr.sh help
```

## Conda package build flow

From an activated Conda environment with `conda-build` installed:

```bash
conda build conda/recipes/ontologies-cbr
```

Then install the built package into your environment, for example from the local build output.

## Current status

Verified locally on macOS arm64:

- `ontologies-cbr` package builds and passes a real headless query smoke test
- `ontocast` package builds and passes import/CLI smoke tests
- `ontologies-stack` meta-package builds
- a fresh Conda environment can be created from the local build channel and run both:
  - `ontologies-cbr help`
  - `ontocast --help`

## Recommended next steps

1. Publish the local packages to an internal Conda channel or artifact store.
2. Add CI to build and test the packages automatically.
3. Add Linux recipes/variants for OntoCast if the team needs cross-platform support.
4. Decide whether to package OntoCast optional `doc-processing` extras in a separate package variant.
5. Document the full OntoCast → RDF → CSV → CBR workflow once OntoCast execution is finalized.
