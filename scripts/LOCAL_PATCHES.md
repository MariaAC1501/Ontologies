# Local submodule patches

This repository keeps compatibility-change definitions in `scripts/apply_local_patches.py`. The patcher applies them to submodule working trees but does not commit them to the upstream projects. Run it through the normal setup command:

```bash
bash scripts/setup_submodules.sh
```

```powershell
.\scripts\setup_submodules.ps1
```

To inspect or apply one dependency only:

```bash
python scripts/apply_local_patches.py --dependency ontocast
python scripts/apply_local_patches.py --dependency diversity
python scripts/apply_local_patches.py --dependency cbr
```

The patcher validates the requested submodule, replaces only exact upstream anchors, and is idempotent: a previously applied replacement is reported as `already`. An anchor failure means that the submodule revision has drifted; update the patch definition and validate it before changing the pinned revision.

## OntoCast

The following patches are applied to the local `external/ontocast` checkout:

| Area | Purpose |
|---|---|
| Ontology-render prompt | Escapes `ontology_prefix` so fresh ontology bootstrapping does not raise a formatting `KeyError`. |
| Configuration | Disables direct OpenAI API-key configuration, permits the OpenAI-compatible local subscription proxy via `LLM_BASE_URL`, and adds `skip_ontology_critique`. |
| Tool and state graph wiring | Propagates `skip_ontology_critique`; gives parallel ontology/facts workers their configured retry budgets and safely copied budget trackers. |
| RDF graph copying | Adds `RDFGraph.__deepcopy__`, omitting unsupported RDF-star triple terms while preserving ordinary triples and namespace bindings. |
| SPARQL updates | Omits tuple-valued RDF-star terms from generated SPARQL update text instead of serializing invalid updates. |
| Critics | Accepts scores of 80 or higher and makes optional implicit enrichment/minor fact omissions non-blocking. |
| Quota handling | Retries the same document after subscription usage-limit errors instead of skipping it. The wait is controlled by `ONTOCAST_QUOTA_RETRY_SECONDS` (default: 900 seconds). |

The fixed OPMAD configuration enables `SKIP_ONTOLOGY_CRITIQUE=true`; the full-evolution configuration intentionally leaves it unset. Both configurations use the local Pi Codex subscription proxy and do not carry OpenAI API keys. See `pipeline/ontocast_config.env` and `pipeline/full_mode/ontocast_full_config.env`.

## Diversity-in-CBR

The local patcher makes the vendored research code usable from an arbitrary checkout:

| Area | Purpose |
|---|---|
| `Methods.py` | Uses the submodule-relative dataset path, and treats `gensim` as optional because the semantic helper is not used by this repository's reranker. |
| `Methods2.py` | Uses submodule-relative dataset paths and fixes the exact-match branch of `SimTaxon`. |
| `Validation.py` | Corrects the argument order passed to `apply_CNN` and passes similarity weights to `retrieval_for_ModCNN`. |
| `Modified_Condensed_Nearest_Neighbors.py` | Returns partial matches instead of implicitly returning `None`. |
| `Performance_Dataset_Generation.py` | Reads and writes performance datasets under the submodule's `Datasets/` directory. |

`pipeline/diversity_rerank.py` does not import these modules. It reads the model taxonomy from `Methods2.py` using the Python AST, avoiding the upstream module's import-time dataset loading.

## CBR ontology project

No source patch is applied to `external/CBR-Ontology-For-Predictive-Maintenance`. The local `HeadlessCBR.java` adapter and build scripts configure the upstream project at runtime and compile its ISO-8859-1 sources without modifying them.

## Updating a submodule revision

1. Update and test the submodule revision in a disposable working tree.
2. Run the patcher for that dependency.
3. If an exact anchor no longer matches, update `scripts/apply_local_patches.py` with a reviewed replacement; do not hand-edit the submodule as the permanent fix.
4. Run the relevant local build/tests and review the submodule diff.
5. Commit the submodule pointer and the patcher/documentation change together.
