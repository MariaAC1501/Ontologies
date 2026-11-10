#!/usr/bin/env python3
"""Apply OntoCast 0.8.2 runtime fixes and optional experimental patches.

Run from the repository root:
    python3 scripts/patch_ontocast.py
    python3 scripts/patch_ontocast.py --experimental cross-section-merging --check
    python3 scripts/patch_ontocast.py --experimental cross-section-merging

Use --source-dir PATH for another OntoCast checkout. This script needs Git,
not OntoCast's Python dependencies. Runtime fixes are always selected; repeat
--experimental to select additional patches. Every selected patch is checked
before any changes are applied. Already-applied patches are skipped, and
incompatible or partly patched code is refused without changing files.

Runtime fixes:
- Keep generated Turtle prefixes from ending in a dot.
- Preserve RDF 1.2 quoted triples when saving fact provenance.

Experimental patches are discovered in scripts/patches/experimental/*.patch.
Add a <name>.patch file there and select it with --experimental <name>.

Available experiment:
- cross-section-merging: add CHUNK_MERGE_ACROSS_SECTIONS (default false).
  Enable it for a run to merge content across section labels after filtering.
  Separately routed bibliography and skipped non-content units stay isolated.
  Set CHUNK_MIN_SIZE and CHUNK_MAX_SIZE per run, for example 48000 and 96000.

Timeouts need no OntoCast source patch: LLM_REQUEST_TIMEOUT_SECONDS in
scripts/ontocast-subscription.env configures both OntoCast and the proxy.

This does not change the ontology, prompt, or model, or run extraction.
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PATCH = r'''diff --git a/ontocast/onto/rdfgraph.py b/ontocast/onto/rdfgraph.py
index 1374e53..0786b15 100644
--- a/ontocast/onto/rdfgraph.py
+++ b/ontocast/onto/rdfgraph.py
@@ -1933,12 +1933,14 @@ class RDFGraph(Graph):
         # Offer digit-stripped stems as candidates: rdflib mints `schema1` when
         # `schema` is contested at parse time, and after namespace
         # canonicalization the stem is often free again. Only stems not claimed
-        # by a different namespace are eligible.
+        # by a different namespace are eligible. Stripping a numeric version
+        # must not leave a trailing dot, which is invalid in a Turtle prefix.
         for namespace, prefixes in uri_to_prefixes.items():
             for prefix in list(prefixes):
                 stem = prefix.rstrip("0123456789")
                 if (
                     stem
+                    and not stem.endswith(".")
                     and stem != prefix
                     and stem not in prefixes
                     and merged.get(stem, namespace) == namespace
diff --git a/ontocast/tool/triple_manager/in_memory.py b/ontocast/tool/triple_manager/in_memory.py
index 0aeca58..2dad702 100644
--- a/ontocast/tool/triple_manager/in_memory.py
+++ b/ontocast/tool/triple_manager/in_memory.py
@@ -65,7 +65,7 @@ def _clear_named_graph(store: ox.Store, graph_ctx: ox.NamedNode) -> None:
 _OX_POSITION_TYPES: dict[str, tuple[type, ...]] = {
     "subject": (ox.NamedNode, ox.BlankNode),
     "predicate": (ox.NamedNode,),
-    "object": (ox.NamedNode, ox.BlankNode, ox.Literal),
+    "object": (ox.NamedNode, ox.BlankNode, ox.Literal, ox.Triple),
 }
 
 
@@ -83,15 +83,15 @@ def _to_ox_term(
 
 @overload
 def _to_ox_term(
-    term: Node, position: Literal["object"], graph_ctx: ox.NamedNode
-) -> ox.NamedNode | ox.BlankNode | ox.Literal: ...
+    term: Node | tuple, position: Literal["object"], graph_ctx: ox.NamedNode
+) -> ox.NamedNode | ox.BlankNode | ox.Literal | ox.Triple: ...
 
 
 def _to_ox_term(
-    term: Node,
+    term: Node | tuple,
     position: Literal["subject", "predicate", "object"],
     graph_ctx: ox.NamedNode,
-) -> ox.NamedNode | ox.BlankNode | ox.Literal:
+) -> ox.NamedNode | ox.BlankNode | ox.Literal | ox.Triple:
     """Convert one rdflib term, naming the graph and position when it cannot be.
 
     Args:
@@ -107,7 +107,16 @@ def _to_ox_term(
         TypeError: The term does not convert to something valid in ``position``.
     """
     try:
-        converted = to_ox(term)
+        if position == "object" and isinstance(term, tuple) and len(term) == 3:
+            # oxrdflib exposes RDF 1.2 triple terms as tuples, but to_ox()
+            # treats tuples as whole quads rather than quoted object terms.
+            converted = ox.Triple(
+                _to_ox_term(term[0], "subject", graph_ctx),
+                _to_ox_term(term[1], "predicate", graph_ctx),
+                _to_ox_term(term[2], "object", graph_ctx),
+            )
+        else:
+            converted = to_ox(term)
     except ValueError as exc:
         raise TypeError(
             f"cannot serialize {position} {term!r} "
@@ -116,7 +125,7 @@ def _to_ox_term(
     # Two checks, not one: the first narrows the union for the type checker,
     # the second enforces what this particular position accepts.
     if not isinstance(
-        converted, (ox.NamedNode, ox.BlankNode, ox.Literal)
+        converted, (ox.NamedNode, ox.BlankNode, ox.Literal, ox.Triple)
     ) or not isinstance(converted, _OX_POSITION_TYPES[position]):
         raise TypeError(
             f"{position} {term!r} (rdflib type {type(term).__name__}) of graph "
'''


EXPERIMENTAL_PATCH_DIR = ROOT / "scripts/patches/experimental"
EXPERIMENTAL_PATCHES = {
    path.stem: path
    for path in sorted(EXPERIMENTAL_PATCH_DIR.glob("*.patch"))
    if path.is_file()
}


def git_apply(
    source: Path, *options: str, patch: str = PATCH
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(source), "apply", *options, "-"],
        input=patch,
        text=True,
        capture_output=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--source-dir", type=Path, default=ROOT / "external/ontocast",
        help="OntoCast checkout (default: external/ontocast).",
    )
    parser.add_argument(
        "--check", action="store_true",
        help="Check compatibility or report already applied; change no files.",
    )
    parser.add_argument(
        "--experimental", action="append", choices=tuple(EXPERIMENTAL_PATCHES),
        default=[], help="Select an experimental patch; repeat for multiple patches.",
    )
    args = parser.parse_args()
    source = args.source_dir.expanduser().resolve()
    if not source.is_dir():
        parser.error(f"OntoCast checkout not found: {source}")

    selected = [("runtime fixes", PATCH)]
    selected.extend(
        (f"experimental {name}", EXPERIMENTAL_PATCHES[name].read_text(encoding="utf-8"))
        for name in dict.fromkeys(args.experimental)
    )
    pending = []
    for name, patch in selected:
        if git_apply(source, "--reverse", "--check", patch=patch).returncode == 0:
            print(f"Already applied ({name}): {source}")
            continue
        check = git_apply(source, "--check", patch=patch)
        if check.returncode:
            parser.exit(
                1,
                f"Patch ({name}) does not match this checkout, or is only partly "
                "applied. No files were changed.\n" + check.stderr,
            )
        pending.append((name, patch))

    if args.check:
        for name, _ in pending:
            print(f"Can be applied ({name}): {source} (no files changed)")
        return 0
    if not pending:
        return 0

    # Apply all pending patches together so Git checks the whole batch before
    # writing any files, including when several experimental patches are selected.
    result = git_apply(source, patch="\n".join(patch for _, patch in pending))
    if result.returncode:
        parser.exit(1, "Git could not apply the patches:\n" + result.stderr)
    for name, _ in pending:
        print(f"Applied ({name}): {source}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except OSError as exc:
        print(f"Could not run patch script: {exc}", file=sys.stderr)
        sys.exit(1)
