# OPMAD conversion

Generate `OPMAD-ontocast.ttl` with `scripts/convert_opmad.py`. Run from the
repository root:

```sh
uv run scripts/convert_opmad.py
```

Use `--source-dir` or `--output-dir` to override the default paths.

## OntoCast input and usage

`OPMAD-ontocast.ttl` includes OPMAD and the bundled dependencies, with their definitions, axioms and annotations.
Only the 8 dependency subjects' `rdf:type owl:Ontology`
declarations are removed, so OPMAD remains the sole declared ontology for OntoCast compatibility.

The dependency ontology declarations are an explicitly approved RDF
loss in the OntoCast view. They remain in the original source files.

### Run extraction

Use `scripts/run_opmad.py` to select papers and keep the schema fixed:

```sh
.venv/bin/python scripts/run_opmad.py --papers OPMAD-S001 --output-dir out/pilot
```

See [the extraction guide](../../README.md#run-extraction) for proxy startup,
dry runs, subsets, full-corpus runs, and saved run metadata.

For direct OntoCast use, `--ontology-dir` is `ontologies/opmad-ontocast`.
The ontology IRI is
`http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD`.
