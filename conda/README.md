# Conda Packaging Details

## Supported Conda packaging targets

Current OntoCast recipe support in this repo:
- `osx-arm64`
- `linux-64`
- `win-64`

Current CBR recipe support:
- `noarch` package with a Java runtime dependency

Notes:
- the OntoCast recipe vendors a few PyPI-only wheels for each supported platform
- Linux support in this repo currently targets `linux-64`
- Windows support in this repo currently targets `win-64`

## CI matrix builds

This repo includes a CI workflow at:
- `.github/workflows/conda-matrix.yml`

It builds and smoke-tests the Conda packaging flow on:
- macOS
- Linux
- Windows

Each CI job:
1. checks out the repo with submodules
2. installs Miniforge
3. installs build dependencies from `environment.yml`
4. builds `ontologies-cbr`, `ontocast`, `ontologies-pipeline`, and `ontologies-stack`
5. creates a fresh environment from the locally built channel
6. runs smoke tests for the installed tools

Current status:
- the Conda matrix build/test workflow is passing on macOS, Linux, and Windows

## Conda package details

| Package | Type | Contents |
|---------|------|----------|
| `ontologies-cbr` | `noarch` | Headless CBR jar, upstream jars, ontology/data assets, `ontologies-cbr` CLI wrapper |
| `ontocast` | per-platform | OntoCast Python package with vendored PyPI wheels and local patches |
| `ontologies-pipeline` | `noarch` | Extraction schema, seed ontology, facts→CSV bridge, config, run scripts |
| `ontologies-stack` | `noarch` | Meta-package installing all three above |

The `ontologies-cbr` CLI resolves its data directory in this order:
1. `--data-dir DIR`
2. `ONTOLOGIES_CBR_DATA_DIR`
3. repository-local default during development
4. `$CONDA_PREFIX/share/ontologies-cbr/data`
