# Local submodule patches

`scripts/setup_submodules.sh` (or `.ps1`) validates the submodules, applies the repository-owned Diversity-in-CBR patches, and installs/builds the stack. Patch definitions live in `scripts/apply_local_patches.py` and are idempotent. An exact-anchor failure means the upstream revision has drifted; review the patch before updating the pin.

```bash
python scripts/apply_local_patches.py --dependency ontocast  # validation only
python scripts/apply_local_patches.py --dependency diversity
python scripts/apply_local_patches.py --dependency cbr       # validation only
```

## OntoCast: no source patches

`external/ontocast` is pinned to stock **0.8.2** (`4e7a00c6120b84780db226f834848470fed1fc5c`). All former OntoCast patches have been removed, including the critic thresholds/bypass, quota-wait loop, RDF workarounds, and custom full-text location fields.

The existing `pipeline/tools/pi_codex_openai_proxy.mjs` works through upstream configuration:

```dotenv
LLM_PROVIDER=openai
LLM_BASE_URL=http://127.0.0.1:8977/v1
LLM_API_KEY=subscription-proxy
ONTOLOGY_CRITIC_PASSES=0
FACTS_CRITIC_PASSES=1
```

`subscription-proxy` is a public, non-secret placeholder required by the OpenAI SDK, **not an API key**. The proxy authenticates with Pi's ChatGPT Plus/Pro (Codex) OAuth credential. The repository runners verify the local proxy, reject real keys, and pin this placeholder and endpoint in the child environment. No OAuth token is copied into OntoCast settings.

Both modes use `ontocast --env-file ... process --output-dir ... --keep-provenance --exclude-sections ""`. They retain bibliography text too. Ontology critique is off; facts critique remains on. Output names are `*.facts.ttl` and `*.ontology.ttl`; `*.units.jsonl` retains the source chunks. Upstream provenance does not contain the removed page/character/paragraph RDF fields. Prepared `source-map.json` sidecars remain available separately.

Setup installs `[server,openai,doc-processing,semantic-chunking]`. Native SDK retries replace the removed indefinite subscription-quota wait; a failed document may need an explicit rerun.

### Known upstream extraction blocker

The subscription connection passes a live smoke test, but complete local extraction is blocked in 0.8.2. `InMemoryTripleStoreManager.serialize()` rejects the RDF 1.2 triple terms produced by OntoCast's own provenance rewriter: `TypeError: ... converts to Quad, which is not valid in object position`. This happens before CLI output dumps, including when `--keep-provenance` is supplied.

`pipeline/tests/test_subscription_proxy.py` contains an expected-failure reproducer (**T-RUN-10**). No source patch, runtime monkeypatch, or provenance-stripping workaround is applied. An upstream fix is needed for the default backend; Fuseki is an alternative native backend to investigate, not a validated workaround here.

### Validation

- Live stock OntoCast `LLMTool` → local proxy → Pi Codex subscription: passed, without a real API key.
- 112 pipeline tests, four annotation tests, and 62 focused upstream tests passed. The provenance-store reproducer is one expected failure.
- The pre-existing screening test module could not run because `screening/` is absent. PowerShell runners were updated but not executed on this macOS checkout.
- Both config files pass `ontocast config check`; the OntoCast submodule remains clean. Diversity patch definitions are unchanged.

## Diversity-in-CBR

These patches are unchanged:

| Area | Purpose |
|---|---|
| `Methods.py` | Uses the submodule-relative dataset path and makes unused `gensim` optional. |
| `Methods2.py` | Uses submodule-relative dataset paths and fixes exact matches in `SimTaxon`. |
| `Validation.py` | Corrects `apply_CNN` argument order and passes retrieval weights. |
| `Modified_Condensed_Nearest_Neighbors.py` | Returns partial matches instead of `None`. |
| `Performance_Dataset_Generation.py` | Reads and writes under the submodule's `Datasets/` directory. |

`pipeline/diversity_rerank.py` reads the taxonomy using the Python AST rather than importing these modules.

## CBR ontology project

No source patch is applied to `external/CBR-Ontology-For-Predictive-Maintenance`. `pipeline/tools/cbr/HeadlessCBR.java` adapts it at runtime; build scripts compile its ISO-8859-1 sources without changing them.

## Updating a submodule revision

1. Test the revision in a disposable working tree.
2. Run the patcher/validator for that dependency. OntoCast must remain unmodified.
3. For Diversity anchor drift, update the patch definitions rather than hand-editing the submodule.
4. Run the relevant tests and review the submodule diff.
5. Commit the submodule pointer together with related setup, runner, and documentation changes.
