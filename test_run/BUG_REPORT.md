# OntoCast Bug Report — `KeyError: 'ontology_prefix'` in `render_ontology_fresh`

**Date**: 2026-03-22  
**OntoCast version**: 0.3.0  
**Discovered during**: End-to-end test with `example_paper.pdf`, Ollama/qwen2.5 backend, filesystem triple-store  
**Severity**: Critical (blocks all fresh-ontology extraction runs)

---

## Symptom

Running OntoCast with `--input-path` raises the following error for every document:

```
Error processing .../example_paper.pdf: 'ontology_prefix'
```

Full traceback (captured in `test_run/debug_run.log`):

```
File ".../ontocast/stategraph/node_factories.py", line 59, in bootstrap_ontology
File ".../ontocast/stategraph/atomic.py",        line 169, in ontology_loop
File ".../ontocast/agent/render_ontology.py",    line 112, in render_ontology_fresh
    general_ontology_instruction_str = general_ontology_instruction.format(
                                       prefix_instruction=prefix_instruction_fresh
                                       )
KeyError: 'ontology_prefix'
```

---

## Root Cause

**File**: `ontocast/prompt/render_ontology.py`

```python
# Line 40 — a regular string template with a deferred {ontology_prefix} placeholder
prefix_instruction = """Use prefix `{ontology_prefix}` for entities/properties ..."""

# Line 44 — defined as an **f-string**, so Python immediately evaluates {prefix_instruction}
# at module import time, substituting the full text of `prefix_instruction` into the string,
# including its own `{ontology_prefix}` brace-placeholder.
general_ontology_instruction = f"""
...
6. {prefix_instruction}      # <-- baked in at import; {ontology_prefix} now embedded literally
...
"""
```

After the f-string is evaluated `general_ontology_instruction` contains the literal text:

```
6. Use prefix `{ontology_prefix}` for entities/properties ...
```

There is **no** `{prefix_instruction}` placeholder left in the string — it was consumed by the
f-string. However `{ontology_prefix}` **is** present as a `.format()` placeholder.

### Why the update path works

`render_ontology_update` (line 214) coincidentally passes **both** keyword arguments:

```python
general_ontology_instruction_str = general_ontology_instruction.format(
    prefix_instruction=prefix_instruction.format(ontology_prefix=current.prefix),
    ontology_prefix=current.prefix,   # <-- supplies the embedded {ontology_prefix}
)
```

`ontology_prefix=current.prefix` satisfies the embedded `{ontology_prefix}` placeholder, so no
error is raised.  The `prefix_instruction=...` kwarg is silently ignored (there is no matching
`{prefix_instruction}` placeholder left after the f-string evaluation).

### Why the fresh path fails

`render_ontology_fresh` (line 112) only passes:

```python
general_ontology_instruction_str = general_ontology_instruction.format(
    prefix_instruction=prefix_instruction_fresh   # unused — no {prefix_instruction} left
)
# {ontology_prefix} is still present but not supplied → KeyError: 'ontology_prefix'
```

---

## Fix

**File to patch**: `ontocast/prompt/render_ontology.py`

Change item 6 in the `general_ontology_instruction` f-string from:

```python
6. {prefix_instruction}
```

to (double-brace escapes the placeholder so the f-string does NOT substitute it at import time):

```python
6. {{prefix_instruction}}
```

This preserves `{prefix_instruction}` as a deferred runtime placeholder. After the fix:

- `render_ontology_fresh` → `.format(prefix_instruction=prefix_instruction_fresh)` fills it ✓  
- `render_ontology_update` → `.format(prefix_instruction=..., ontology_prefix=...)` — the
  `prefix_instruction` kwarg is now used; `ontology_prefix` is no longer needed (harmless if left).

The `{DEFAULT_IRI}` placeholder on line 9 of the same f-string should remain as-is (single brace)
because that constant IS intended to be baked in at module load time.

---

## Patch Applied

The fix was applied to the **installed** package file:

```
/Users/antho/miniforge3/envs/ontologies-stack-test/lib/python3.12/site-packages/ontocast/prompt/render_ontology.py
```

> **Note**: This patch targets the installed file in the conda environment only.
> The vendored wheel at `conda/recipes/ontocast/wheels/ontocast-0.3.0-py3-none-any.whl` is unchanged.
> The upstream source must receive this fix before the next wheel/package release.

---

## Bug 2 — `TypeError: cannot pickle 'pyoxigraph.Store' object` in `render_facts`

**File**: `ontocast/stategraph/node_factories.py`  
**Functions**: `make_render_facts_node → render_facts → process_unit` (line 245 in installed package)  
**Also affects**: `make_render_ontology_node → render_ontology_updates → process_unit` (same pattern)

### Symptom

After ontology normalization, the pipeline aborts with:

```
TypeError: cannot pickle 'pyoxigraph.Store' object
```

Full traceback chain:

```
node_factories.py, render_facts → process_unit
  pydantic/main.py, model_copy → __deepcopy__
  copy.py, deepcopy
  TypeError: cannot pickle 'pyoxigraph.Store' object
```

### Root Cause

`normalize_ontology_units` calls `tools.aggregator.aggregate_graphs(units)`, which internally
calls `GraphRewriter.merge()` in `tool/agg/rewriter.py`.  `merge()` creates the merged graph as:

```python
merged = RDFGraph(store="oxigraph")   # oxigraph-backed store
```

This oxigraph-backed `RDFGraph` flows into `state.current_ontology.graph`.

Later, in both `make_render_ontology_node` and `make_render_facts_node`, each parallel
`process_unit` worker does:

```python
base_state = state.model_copy(deep=True)   # <-- full deep-copy of AgentState
budget_tracker = base_state.budget_tracker  # only this field is ever used
```

Python's `deepcopy` (called by Pydantic's `model_copy(deep=True)`) tries to pickle and restore
every field of `AgentState`, including `current_ontology.graph` which is backed by
`pyoxigraph.Store` — an extension type that **cannot be pickled** → `TypeError`.

### Fix

Replace `state.model_copy(deep=True)` with a targeted deep-copy of only the field that is
actually needed — `budget_tracker`:

```python
# BEFORE (in both make_render_ontology_node and make_render_facts_node):
base_state = state.model_copy(deep=True)
# ... then only base_state.budget_tracker is used

# AFTER:
budget_tracker = state.budget_tracker.model_copy(deep=True)
```

`BudgetTracker` only contains plain `int` fields; deep-copying it is safe and cheap.

### Patches Applied

**Patch A** — `node_factories.py`: both occurrences of `state.model_copy(deep=True)` replaced
with `state.budget_tracker.model_copy(deep=True)` (only the `budget_tracker` field is used from
the copy).

**Patch B** — `ontocast/onto/rdfgraph.py`: added `__deepcopy__` to `RDFGraph` that creates a
plain (non-oxigraph) copy while skipping RDF 1.2 triple-term triples (tuples), which arise from
the aggregator rewriter's provenance annotations and cannot be added to a plain rdflib Graph.
This makes all `copy.deepcopy()` traversals through any `RDFGraph` safe.

---

## Bug 4 — `ParseException: Expected end of text, found 'INSERT'` when applying SPARQL updates

**Discovered during**: re-run with `gpt-5-nano` (smarter model produces richer updates)  
**File**: `ontocast/onto/rdfgraph.py` → `update()`  
**Severity**: Critical — aborts the pipeline after the ontology normalization step

### Symptom

```
pyparsing.exceptions.ParseException:
  Expected end of text, found 'INSERT'  (at char 1492), (line:34, col:1)
```

Full traceback:
```
node_factories.py, normalize_ontology_updates
  normalize_ontology.py, normalize_ontology_units
    state.py, render_updated_graph
      rdfgraph.py, update
        rdflib graph.py / sparql parser
        ParseException: Expected end of text, found 'INSERT'
```

### Root Cause

`GraphUpdate.generate_sparql_queries()` passes `GenericSparqlQuery.query` strings
as-is to `rdfgraph.update()`. A smarter model (gpt-5-nano) sometimes emits multiple
`INSERT DATA { … }` blocks in a single `query` string **without semicolons** separating
them, e.g.:

```sparql
PREFIX ex: <…>
INSERT DATA { ex:A ex:p ex:B . }
INSERT DATA { ex:C ex:p ex:D . }
```

rdflib's SPARQL 1.1 Update parser accepts multiple update operations **only when
separated by `;`**.  Without the semicolon it raises `ParseException`.

Verified: rdflib accepts the same input when semicolons are present:
```sparql
INSERT DATA { … } ;
INSERT DATA { … }
```

### Fix

In `RDFGraph.update()`, before passing the query string to rdflib, insert missing
semicolons between adjacent top-level SPARQL update operations.

The normalizer uses a regex to find transitions between the end of a closing `}`
and the start of a new update keyword (`INSERT`, `DELETE`, `LOAD`, `CLEAR`, `CREATE`,
`DROP`, `COPY`, `MOVE`, `ADD`, `WITH`) at a line boundary, inserting `;` if absent.

### Root Cause (revised after deeper investigation)

The `ParseException` is NOT caused by missing semicolons. On closer inspection the
generated query contains lines like:

```sparql
_:blank <rdf:reifies> (rdflib.term.URIRef('…'), rdflib.term.URIRef('…'), rdflib.term.Literal('…')) .
```

`_generate_insert_query` in `sparql_models.py` iterates the oxigraph-backed delta
graph, hits a triple whose object is a Python **tuple** (an RDF 1.2 triple-term
from oxrdflib), and falls through to the `else: return str(term)` branch in
`_serialize_rdf_term`, producing the Python tuple repr verbatim — which is
syntactically invalid SPARQL.  rdflib's parser chokes on the malformed triple and
issues `ParseException`.

The `_normalize_sparql_update()` helper (inserted while investigating) is harmless
but ineffective against this class of error; it is retained.

### Actual Fix

**File patched**: `ontocast/onto/sparql_models.py` — `_generate_insert_query()` and
`_generate_delete_query()`

Skip any triple where `subject` or `object` is a Python tuple (RDF 1.2 triple-term
yielded by the oxrdflib store iterator).  These are provenance-reification triples
injected by the aggregator rewriter and have no place in an ontology SPARQL update.
This is the same guard already applied in `RDFGraph.__deepcopy__`.

Also added as a belt-and-suspenders: `_serialize_rdf_term()` now raises `TypeError`
for unknown term types instead of silently producing a Python repr.

---

## Bug 3 (Warning) — `Failed to compute hash for ontology …: Object … must be an rdflib term`

**File**: `ontocast/onto/ontology.py` (hash computation)  
**Severity**: Warning only — does not abort the pipeline

### Symptom

```
WARNING: Failed to compute hash for ontology slitting:
  Object (rdflib.term.URIRef(...), rdflib.term.URIRef(...), rdflib.term.URIRef(...))
  must be an rdflib term
```

### Root Cause (observed)

The hash computation iterates over triples in the ontology graph and attempts to hash each term.
When `aggregated_delta` is an oxigraph-backed `RDFGraph`, the triples it yields may be
`pyoxigraph` term types rather than `rdflib` terms — the iteration protocol for
`oxrdflib`-backed graphs wraps terms for most operations, but the hash computation seems to
receive unwrapped tuples containing raw `rdflib.term.URIRef` objects that do not match the
expected type (the error message is internally inconsistent — the objects shown ARE rdflib terms
but the hashing code rejected them; likely the hash code tests `isinstance(term, pyoxigraph.*)`
when the graph is oxigraph-backed).

**Not patched** — this is a warning; the pipeline continues. Documenting for upstream.

---

## Additional Issues Found During Setup

### 1. `docling` not included in the conda package

`docling` (PDF converter) is listed as a required capability but is **not** declared as a
dependency in the conda recipe and is not vendored in `conda/recipes/ontocast/wheels/`.

Without it, OntoCast logs a warning at startup and then raises:

```
ImportError: Could not import DocumentConverter: <file>
```

when a PDF is submitted.

**Resolution for this test run**: `docling` was installed manually into the conda env:

```bash
conda run -n ontologies-stack-test pip install docling
```

This is a runtime dependency that should either be added to the recipe's `requirements/run`
section or vendored as a wheel for offline installs.

### 2. `--input-path` requires a directory, not a file

The CLI help text says `--input-path PATH` without clarifying that a **directory** must be
provided. Passing `example_paper.pdf` directly prints:

```
The path example_paper.pdf is not a valid directory.
```

and silently succeeds (processes zero files).

**Resolution for this test run**: the PDF was copied into `test_run/input/` and the directory
was passed as `--input-path`.
