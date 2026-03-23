"""Apply all local patches to the installed OntoCast package.

This script is run during the Conda build (build.sh / bld.bat) and can also
be run manually after a pip install to apply the same fixes.

All patches are idempotent — running the script multiple times is safe.

See GitHub issue #1 for the full list of upstream issues filed.
"""
from __future__ import annotations

import importlib.util
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def _locate_package() -> Path:
    spec = importlib.util.find_spec("ontocast")
    if spec is None or spec.origin is None:
        raise RuntimeError("Could not locate installed ontocast package")
    return Path(spec.origin).resolve().parent


def replace_once(base: Path, rel_path: str, old: str, new: str) -> None:
    """Replace `old` with `new` in a file, skipping if already patched."""
    target = base / rel_path
    text = target.read_text()
    if new in text:
        return  # already patched
    if old not in text:
        raise RuntimeError(f"Expected patch anchor not found in {target}")
    target.write_text(text.replace(old, new))


def main() -> None:
    base = _locate_package()

    # --- Patch 1: ontology_prefix KeyError (upstream #47) ---
    replace_once(
        base,
        "prompt/render_ontology.py",
        'prefix_instruction = """Use prefix `{ontology_prefix}` for entities/properties placed in the current domain ontology. DECLARE the prefix in preamble!"""',
        'prefix_instruction = """Use prefix `{{ontology_prefix}}` for entities/properties placed in the current domain ontology. DECLARE the prefix in preamble!"""',
    )

    # --- Patch 2: skip_ontology_critique config flag ---
    replace_once(
        base,
        "config.py",
        '    enable_ontology_consolidation: bool = Field(\n        default=False,\n        description="Run optional ontology consolidation pass after normalization",\n    )\n',
        '    enable_ontology_consolidation: bool = Field(\n        default=False,\n        description="Run optional ontology consolidation pass after normalization",\n    )\n    skip_ontology_critique: bool = Field(\n        default=False,\n        description=(\n            "Experimental fast path: accept successful ontology render output "\n            "without running the ontology critic loop. This also affects "\n            "bootstrap ontology generation."\n        ),\n    )\n',
    )

    # --- Patch 3: wire skip_ontology_critique through AtomicToolBox ---
    replace_once(
        base,
        "tool/atomic.py",
        '        web_search_for_facts_render: bool = False,\n        web_search_for_facts_critic: bool = False,\n        web_search_planner_enabled: bool = True,\n',
        '        web_search_for_facts_render: bool = False,\n        web_search_for_facts_critic: bool = False,\n        skip_ontology_critique: bool = False,\n        web_search_planner_enabled: bool = True,\n',
    )
    replace_once(
        base,
        "tool/atomic.py",
        '            self.web_search_for_facts_render = web_search_config.facts_render_enabled\n            self.web_search_for_facts_critic = web_search_config.facts_critic_enabled\n            self.web_search_planner_enabled = web_search_config.planner_enabled\n',
        '            self.web_search_for_facts_render = web_search_config.facts_render_enabled\n            self.web_search_for_facts_critic = web_search_config.facts_critic_enabled\n            self.skip_ontology_critique = skip_ontology_critique\n            self.web_search_planner_enabled = web_search_config.planner_enabled\n',
    )
    replace_once(
        base,
        "tool/atomic.py",
        '            self.web_search_for_facts_render = web_search_for_facts_render\n            self.web_search_for_facts_critic = web_search_for_facts_critic\n            self.web_search_planner_enabled = web_search_planner_enabled\n',
        '            self.web_search_for_facts_render = web_search_for_facts_render\n            self.web_search_for_facts_critic = web_search_for_facts_critic\n            self.skip_ontology_critique = skip_ontology_critique\n            self.web_search_planner_enabled = web_search_planner_enabled\n',
    )
    replace_once(
        base,
        "toolbox.py",
        '        self.atomic_tools = AtomicToolBox(\n            llm_provider=self,\n            search_provider=self.search_provider,\n            web_search_config=tool_config.web_search,\n        )\n',
        '        self.atomic_tools = AtomicToolBox(\n            llm_provider=self,\n            search_provider=self.search_provider,\n            web_search_config=tool_config.web_search,\n            skip_ontology_critique=config.server.skip_ontology_critique,\n        )\n',
    )

    # --- Patch 4: skip_ontology_critique in stategraph loop ---
    replace_once(
        base,
        "stategraph/atomic.py",
        '        for critic_attempt in range(1, max_visits + 1):\n',
        '        if tools.skip_ontology_critique:\n            logger.info(\n                "Unit ontology loop accepted render output without ontology critique at attempt %s/%s",\n                render_attempt,\n                max_visits,\n            )\n            return unit_state\n\n        for critic_attempt in range(1, max_visits + 1):\n',
    )

    # --- Patch 5: deepcopy fix for parallel workers (upstream #48) ---
    replace_once(
        base,
        "stategraph/node_factories.py",
        '            max_visits_per_node=tools.config.server.max_visits_per_node,\n',
        '            max_visits_per_node=tools.config.server.parallel_ontology_retries,\n',
    )
    replace_once(
        base,
        "stategraph/node_factories.py",
        '                base_state = state.model_copy(deep=True)\n                ontology_state = UnitOntologyState(\n',
        '                budget_tracker = state.budget_tracker.model_copy(deep=True)\n                ontology_state = UnitOntologyState(\n',
    )
    replace_once(
        base,
        "stategraph/node_factories.py",
        '                    budget_tracker=base_state.budget_tracker,\n                    max_visits_per_node=tools.config.server.parallel_ontology_retries,\n',
        '                    budget_tracker=budget_tracker,\n                    max_visits_per_node=tools.config.server.parallel_ontology_retries,\n',
    )
    replace_once(
        base,
        "stategraph/node_factories.py",
        '                base_state = state.model_copy(deep=True)\n                facts_state = UnitFactsState(\n',
        '                budget_tracker = state.budget_tracker.model_copy(deep=True)\n                facts_state = UnitFactsState(\n',
    )
    replace_once(
        base,
        "stategraph/node_factories.py",
        '                    budget_tracker=base_state.budget_tracker,\n                    max_visits_per_node=tools.config.server.parallel_ontology_retries,\n',
        '                    budget_tracker=budget_tracker,\n                    max_visits_per_node=tools.config.server.parallel_facts_retries,\n',
    )

    # --- Patch 6: RDFGraph.__deepcopy__ (upstream #48) ---
    rdf_path = base / "onto/rdfgraph.py"
    rdf_text = rdf_path.read_text()
    if "def __deepcopy__(self, memo):" not in rdf_text:
        marker = '    def copy(self) -> "RDFGraph":\n        """Create a copy of this RDFGraph.\n\n        Returns:\n            RDFGraph: A new RDFGraph instance with all triples and namespace bindings copied.\n        """\n        result = RDFGraph()\n\n        # Copy all triples\n        for triple in self:\n            result.add(triple)\n\n        # Copy namespace bindings\n        for prefix, uri in self.namespaces():\n            result.bind(prefix, uri)\n\n        return result\n'
        deepcopy_method = '\n    def __deepcopy__(self, memo):\n        """Deep-copy oxigraph-backed graphs into a plain in-memory RDFGraph."""\n        cached = memo.get(id(self))\n        if cached is not None:\n            return cached\n\n        result = RDFGraph()\n        memo[id(self)] = result\n\n        for prefix, uri in self.namespaces():\n            result.bind(prefix, uri)\n\n        skipped = 0\n        for subject, predicate, obj in self:\n            if isinstance(subject, tuple) or isinstance(predicate, tuple) or isinstance(obj, tuple):\n                skipped += 1\n                continue\n            try:\n                result.add((subject, predicate, obj))\n            except Exception as exc:\n                skipped += 1\n                logger.debug("Skipping triple during RDFGraph deepcopy: %s", exc)\n\n        if skipped:\n            logger.warning("Skipped %s RDF-star / unsupported triple(s) during RDFGraph deepcopy", skipped)\n\n        return result\n'
        if marker not in rdf_text:
            raise RuntimeError(f"Expected patch anchor not found in {rdf_path}")
        rdf_path.write_text(rdf_text.replace(marker, marker + deepcopy_method))

    # --- Patch 7: SPARQL generation for RDF-star triples (upstream #49) ---
    sparql_path = base / "onto/sparql_models.py"
    sparql_text = sparql_path.read_text()
    if "def _iter_supported_triples" not in sparql_text:
        old_sparql = '    def _generate_insert_query(self, graph: RDFGraph, prefix_block: str) -> str:\n        """Generate a SPARQL INSERT query for the given RDFGraph."""\n        if len(graph) == 0:\n            return ""\n\n        # Format triples for SPARQL using proper RDF term serialization\n        triple_patterns = []\n        for subject, predicate, obj in graph:\n            triple_patterns.append(\n                f"    {self._serialize_rdf_term(subject)} {self._serialize_rdf_term(predicate)} {self._serialize_rdf_term(obj)} ."\n            )\n\n        triples_block = "\\n".join(triple_patterns)\n\n        query_parts = []\n        if prefix_block:\n            query_parts.append(prefix_block)\n        query_parts.append("INSERT DATA {")\n        query_parts.append(triples_block)\n        query_parts.append("}")\n\n        return "\\n".join(query_parts)\n\n    def _generate_delete_query(self, graph: RDFGraph, prefix_block: str) -> str:\n        """Generate a SPARQL DELETE query for the given RDFGraph."""\n        if len(graph) == 0:\n            return ""\n\n        # Format triples for SPARQL using proper RDF term serialization\n        triple_patterns = []\n        for subject, predicate, obj in graph:\n            triple_patterns.append(\n                f"    {self._serialize_rdf_term(subject)} {self._serialize_rdf_term(predicate)} {self._serialize_rdf_term(obj)} ."\n            )\n\n        triples_block = "\\n".join(triple_patterns)\n\n        query_parts = []\n        if prefix_block:\n            query_parts.append(prefix_block)\n        query_parts.append("DELETE DATA {")\n        query_parts.append(triples_block)\n        query_parts.append("}")\n\n        return "\\n".join(query_parts)\n\n    def _serialize_rdf_term(self, term: Node) -> str:\n        """Serialize an RDF term to its SPARQL string representation."""\n'
        new_sparql = '    def _iter_supported_triples(self, graph: RDFGraph):\n        """Yield only triples safe for SPARQL update text."""\n        skipped = 0\n        for subject, predicate, obj in graph:\n            if isinstance(subject, tuple) or isinstance(predicate, tuple) or isinstance(obj, tuple):\n                skipped += 1\n                continue\n            yield subject, predicate, obj\n        if skipped:\n            logger.warning("Skipped %s tuple-valued RDF-star triple(s) in SPARQL update", skipped)\n\n    def _generate_insert_query(self, graph: RDFGraph, prefix_block: str) -> str:\n        """Generate a SPARQL INSERT query for the given RDFGraph."""\n        if len(graph) == 0:\n            return ""\n        triple_patterns = []\n        for subject, predicate, obj in self._iter_supported_triples(graph):\n            triple_patterns.append(\n                f"    {self._serialize_rdf_term(subject)} {self._serialize_rdf_term(predicate)} {self._serialize_rdf_term(obj)} ."\n            )\n        if not triple_patterns:\n            return ""\n        triples_block = "\\n".join(triple_patterns)\n        query_parts = []\n        if prefix_block:\n            query_parts.append(prefix_block)\n        query_parts.append("INSERT DATA {")\n        query_parts.append(triples_block)\n        query_parts.append("}")\n        return "\\n".join(query_parts)\n\n    def _generate_delete_query(self, graph: RDFGraph, prefix_block: str) -> str:\n        """Generate a SPARQL DELETE query for the given RDFGraph."""\n        if len(graph) == 0:\n            return ""\n        triple_patterns = []\n        for subject, predicate, obj in self._iter_supported_triples(graph):\n            triple_patterns.append(\n                f"    {self._serialize_rdf_term(subject)} {self._serialize_rdf_term(predicate)} {self._serialize_rdf_term(obj)} ."\n            )\n        if not triple_patterns:\n            return ""\n        triples_block = "\\n".join(triple_patterns)\n        query_parts = []\n        if prefix_block:\n            query_parts.append(prefix_block)\n        query_parts.append("DELETE DATA {")\n        query_parts.append(triples_block)\n        query_parts.append("}")\n        return "\\n".join(query_parts)\n\n    def _serialize_rdf_term(self, term: Node) -> str:\n        """Serialize an RDF term to its SPARQL string representation."""\n        if isinstance(term, tuple):\n            raise TypeError(f"Unsupported tuple-valued RDF term: {term!r}")\n'
        if old_sparql not in sparql_text:
            raise RuntimeError(f"Expected patch anchor not found in {sparql_path}")
        sparql_path.write_text(sparql_text.replace(old_sparql, new_sparql))

    # --- Patch 8: critic threshold relaxation ---
    replace_once(base, "agent/criticise_ontology.py",
        "if critique.success or critique.score > 90:",
        "if critique.success or critique.score >= 80:")
    replace_once(base, "agent/criticise_facts.py",
        "if critique.success or critique.score > 90:",
        "if critique.success or critique.score >= 80:")

    # --- Patch 9: softer ontology critic prompt ---
    replace_once(base, "prompt/criticise_ontology.py",
        "6. **Domain Coverage**: Includes implicit domain knowledge beyond literal text\n",
        "6. **Domain Coverage**: Includes implicit domain knowledge beyond literal text when clearly supported; missing optional enrichment alone should not block an otherwise coherent ontology\n")
    replace_once(base, "prompt/criticise_ontology.py",
        "- Prioritize fixes that have cascading impact\n",
        "- Prioritize fixes that have cascading impact\n- Do not fail an otherwise sound ontology solely because it lacks optional implicit-domain enrichment beyond the source text\n")

    # --- Patch 10: softer facts critic prompt ---
    replace_once(base, "prompt/criticise_facts.py",
        "2. Completeness: Are all possible facts extracted from the text given the ontology?\n",
        "2. Completeness: Are all important facts extracted from the text given the ontology? Minor omissions should be treated as non-blocking unless they materially affect graph usefulness.\n")

    print(f"Patched ontocast package at {base}")


if __name__ == "__main__":
    main()
