#!/usr/bin/env python3
"""Apply local, idempotent patches to vendored git submodules.

The patches intentionally live outside the submodules so upstream checkouts can be
refreshed and then re-patched reproducibly.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PatchText:
    text: str
    newline: str


DEPENDENCIES = ("all", "ontocast", "cbr", "diversity")


class PatchError(RuntimeError):
    """Raised when a required patch anchor or submodule is missing."""


@dataclass(frozen=True)
class PatchResult:
    dependency: str
    path: Path
    label: str
    status: str


class LocalPatcher:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.results: list[PatchResult] = []
        self.notes: list[str] = []

    def rel(self, path: Path) -> Path:
        try:
            return path.resolve().relative_to(self.root)
        except ValueError:
            return path

    def require_submodule(self, dependency: str, rel_path: str) -> Path:
        path = self.root / rel_path
        if not path.exists():
            raise PatchError(
                f"[{dependency}] Missing submodule at {path}. "
                f"Run: git submodule update --init --recursive {rel_path}"
            )
        if not path.is_dir():
            raise PatchError(f"[{dependency}] Expected submodule directory at {path}")
        if not (path / ".git").exists():
            raise PatchError(
                f"[{dependency}] {path} exists but does not look like an initialized "
                f"git submodule (missing .git). Run: git submodule update --init --recursive {rel_path}"
            )
        self.notes.append(f"[{dependency}] validated submodule: {self.rel(path)}")
        return path

    def require_file(self, dependency: str, path: Path) -> None:
        if not path.exists():
            raise PatchError(f"[{dependency}] Missing file required by patch: {path}")
        if not path.is_file():
            raise PatchError(f"[{dependency}] Expected regular file for patch: {path}")

    def read_patch_text(self, path: Path) -> PatchText:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        crlf_count = text.count("\r\n")
        lf_count = text.count("\n") - crlf_count
        newline = "\r\n" if crlf_count > lf_count else "\n"
        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        return PatchText(normalized, newline)

    def write_patch_text(self, path: Path, text: str, newline: str) -> None:
        if newline != "\n":
            text = text.replace("\n", newline)
        path.write_bytes(text.encode("utf-8"))

    def replace_exact(
        self,
        dependency: str,
        path: Path,
        old: str,
        new: str,
        label: str,
    ) -> None:
        """Replace exact anchor occurrences, skipping if already patched."""
        self.require_file(dependency, path)
        patch_text = self.read_patch_text(path)
        text = patch_text.text
        rel_path = self.rel(path)

        if new in text:
            self.results.append(PatchResult(dependency, rel_path, label, "already"))
            return

        old_count = text.count(old)
        if old_count == 0:
            raise PatchError(
                f"[{dependency}] Expected patch anchor not found in {rel_path} "
                f"for '{label}'. Anchor preview:\n{preview(old)}"
            )

        # Every exact occurrence of an anchor is replaced once per run, while
        # the `new in text` guard above keeps the operation idempotent on later
        # runs.
        self.write_patch_text(path, text.replace(old, new), patch_text.newline)
        self.results.append(PatchResult(dependency, rel_path, label, "patched"))

    def replace_any_exact(
        self,
        dependency: str,
        path: Path,
        old_values: tuple[str, ...],
        new: str,
        label: str,
    ) -> None:
        """Replace the first matching exact anchor from several accepted states."""
        self.require_file(dependency, path)
        patch_text = self.read_patch_text(path)
        text = patch_text.text
        rel_path = self.rel(path)

        if new in text:
            self.results.append(PatchResult(dependency, rel_path, label, "already"))
            return

        for old in old_values:
            if old in text:
                self.write_patch_text(path, text.replace(old, new), patch_text.newline)
                self.results.append(PatchResult(dependency, rel_path, label, "patched"))
                return

        previews = "\n--- or ---\n".join(preview(old) for old in old_values)
        raise PatchError(
            f"[{dependency}] Expected one of several patch anchors not found in {rel_path} "
            f"for '{label}'. Anchor previews:\n{previews}"
        )

    def replace_optional_exact(
        self,
        dependency: str,
        path: Path,
        old: str,
        new: str,
        label: str,
    ) -> None:
        """Replace an exact anchor when present; skip clean upstream states."""
        self.require_file(dependency, path)
        patch_text = self.read_patch_text(path)
        text = patch_text.text
        rel_path = self.rel(path)

        if new in text:
            self.results.append(PatchResult(dependency, rel_path, label, "already"))
            return
        if old in text:
            self.write_patch_text(path, text.replace(old, new), patch_text.newline)
            self.results.append(PatchResult(dependency, rel_path, label, "patched"))
            return
        self.results.append(PatchResult(dependency, rel_path, label, "skipped"))

    def insert_after_exact(
        self,
        dependency: str,
        path: Path,
        marker: str,
        insertion: str,
        already_marker: str,
        label: str,
    ) -> None:
        """Insert text after an exact marker, skipping if already inserted."""
        self.require_file(dependency, path)
        patch_text = self.read_patch_text(path)
        text = patch_text.text
        rel_path = self.rel(path)

        if already_marker in text:
            self.results.append(PatchResult(dependency, rel_path, label, "already"))
            return

        marker_count = text.count(marker)
        if marker_count == 0:
            raise PatchError(
                f"[{dependency}] Expected insertion anchor not found in {rel_path} "
                f"for '{label}'. Anchor preview:\n{preview(marker)}"
            )
        if marker_count > 1:
            raise PatchError(
                f"[{dependency}] Insertion anchor for '{label}' is not unique in {rel_path} "
                f"({marker_count} matches). Refusing to patch."
            )

        self.write_patch_text(
            path, text.replace(marker, marker + insertion, 1), patch_text.newline
        )
        self.results.append(PatchResult(dependency, rel_path, label, "patched"))

    def changed_files(self) -> list[Path]:
        return sorted({result.path for result in self.results if result.status == "patched"})


def preview(anchor: str, max_chars: int = 500) -> str:
    text = anchor if len(anchor) <= max_chars else anchor[:max_chars] + "..."
    return "\n".join(f"    {line}" for line in text.splitlines())


def locate_repo_root() -> Path:
    starts = [Path(__file__).resolve(), Path.cwd().resolve()]
    seen: set[Path] = set()
    for start in starts:
        current = start if start.is_dir() else start.parent
        for candidate in (current, *current.parents):
            if candidate in seen:
                continue
            seen.add(candidate)
            if (candidate / ".git").exists() and (candidate / ".gitmodules").exists():
                return candidate
    raise PatchError(
        "Could not locate repository root from script path or current directory "
        "(expected .git and .gitmodules)."
    )


def apply_ontocast(patcher: LocalPatcher) -> None:
    submodule = patcher.require_submodule("ontocast", "external/ontocast")
    base = submodule / "ontocast"
    if not base.is_dir():
        raise PatchError(f"[ontocast] Missing package directory: {base}")

    def target(rel_path: str) -> Path:
        return base / rel_path

    # --- Patch 1: ontology_prefix KeyError (upstream #47) ---
    patcher.replace_exact(
        "ontocast",
        target("prompt/render_ontology.py"),
        'prefix_instruction = """Use prefix `{ontology_prefix}` for entities/properties placed in the current domain ontology. DECLARE the prefix in preamble!"""',
        'prefix_instruction = """Use prefix `{{ontology_prefix}}` for entities/properties placed in the current domain ontology. DECLARE the prefix in preamble!"""',
        "ontology_prefix escaped in render ontology prompt",
    )

    # --- Patch 1b: remove legacy direct OpenAI API-key support from this repo workflow ---
    patcher.replace_any_exact(
        "ontocast",
        target("config.py"),
        (
            '    api_key: str | None = Field(\n        default=None,\n        description="API key for LLM provider",\n        validation_alias=AliasChoices("LLM_API_KEY", "OPENAI_API_KEY"),\n    )',
            '    api_key: str | None = Field(default=None, description="API key for LLM provider")',
        ),
        '    api_key: str | None = Field(default=None, description="Direct OpenAI API keys are disabled; use the local subscription proxy via LLM_BASE_URL")',
        "OpenAI provider documents subscription proxy key policy",
    )

    patcher.replace_exact(
        "ontocast",
        target("config.py"),
        '    def validate_llm_config(self) -> None:\n        """Validate LLM configuration and raise errors for missing required settings."""\n        if (\n            self.tool_config.llm_config.provider == LLMProvider.OPENAI\n            and not self.tool_config.llm_config.api_key\n        ):\n            raise ValueError(\n                "LLM_API_KEY environment variable is required for OpenAI provider"\n            )\n',
        '    def validate_llm_config(self) -> None:\n        """Validate LLM configuration and raise errors for missing required settings."""\n        llm_config = self.tool_config.llm_config\n        if llm_config.provider == LLMProvider.OPENAI:\n            if llm_config.api_key:\n                raise ValueError(\n                    "Direct OpenAI API keys are disabled in this repository workflow. "\n                    "Use the local Pi Codex subscription proxy via LLM_BASE_URL instead."\n                )\n            if not llm_config.base_url:\n                raise ValueError(\n                    "LLM_BASE_URL must point to the local Pi Codex subscription proxy "\n                    "for OpenAI-compatible extraction runs."\n                )\n',
        "OpenAI provider requires subscription proxy and rejects direct keys",
    )

    patcher.replace_exact(
        "ontocast",
        target("tool/llm.py"),
        '                api_key=(\n                    SecretStr(self.config.api_key) if self.config.api_key else None\n                ),  # type: ignore\n',
        '                api_key=SecretStr(self.config.api_key or "subscription-proxy"),  # type: ignore\n',
        "OpenAI-compatible subscription proxy uses non-secret placeholder key",
    )

    # --- Patch 2: skip_ontology_critique config flag ---
    patcher.replace_exact(
        "ontocast",
        target("config.py"),
        '    enable_ontology_consolidation: bool = Field(\n        default=False,\n        description="Run optional ontology consolidation pass after normalization",\n    )\n',
        '    enable_ontology_consolidation: bool = Field(\n        default=False,\n        description="Run optional ontology consolidation pass after normalization",\n    )\n    skip_ontology_critique: bool = Field(\n        default=False,\n        description=(\n            "Experimental fast path: accept successful ontology render output "\n            "without running the ontology critic loop. This also affects "\n            "bootstrap ontology generation."\n        ),\n    )\n',
        "skip_ontology_critique config flag",
    )

    # --- Patch 3: wire skip_ontology_critique through AtomicToolBox ---
    patcher.replace_exact(
        "ontocast",
        target("tool/atomic.py"),
        '        web_search_for_facts_render: bool = False,\n        web_search_for_facts_critic: bool = False,\n        web_search_planner_enabled: bool = True,\n',
        '        web_search_for_facts_render: bool = False,\n        web_search_for_facts_critic: bool = False,\n        skip_ontology_critique: bool = False,\n        web_search_planner_enabled: bool = True,\n',
        "AtomicToolBox constructor skip_ontology_critique argument",
    )
    patcher.replace_exact(
        "ontocast",
        target("tool/atomic.py"),
        '            self.web_search_for_facts_render = web_search_config.facts_render_enabled\n            self.web_search_for_facts_critic = web_search_config.facts_critic_enabled\n            self.web_search_planner_enabled = web_search_config.planner_enabled\n',
        '            self.web_search_for_facts_render = web_search_config.facts_render_enabled\n            self.web_search_for_facts_critic = web_search_config.facts_critic_enabled\n            self.skip_ontology_critique = skip_ontology_critique\n            self.web_search_planner_enabled = web_search_config.planner_enabled\n',
        "AtomicToolBox config branch skip_ontology_critique assignment",
    )
    patcher.replace_exact(
        "ontocast",
        target("tool/atomic.py"),
        '            self.web_search_for_facts_render = web_search_for_facts_render\n            self.web_search_for_facts_critic = web_search_for_facts_critic\n            self.web_search_planner_enabled = web_search_planner_enabled\n',
        '            self.web_search_for_facts_render = web_search_for_facts_render\n            self.web_search_for_facts_critic = web_search_for_facts_critic\n            self.skip_ontology_critique = skip_ontology_critique\n            self.web_search_planner_enabled = web_search_planner_enabled\n',
        "AtomicToolBox explicit branch skip_ontology_critique assignment",
    )
    patcher.replace_exact(
        "ontocast",
        target("toolbox.py"),
        '        self.atomic_tools = AtomicToolBox(\n            llm_provider=self,\n            search_provider=self.search_provider,\n            web_search_config=tool_config.web_search,\n        )\n',
        '        self.atomic_tools = AtomicToolBox(\n            llm_provider=self,\n            search_provider=self.search_provider,\n            web_search_config=tool_config.web_search,\n            skip_ontology_critique=config.server.skip_ontology_critique,\n        )\n',
        "ToolBox passes skip_ontology_critique into AtomicToolBox",
    )

    # --- Patch 4: skip_ontology_critique in stategraph loop ---
    patcher.replace_exact(
        "ontocast",
        target("stategraph/atomic.py"),
        '        for critic_attempt in range(1, max_visits + 1):\n',
        '        if tools.skip_ontology_critique:\n            logger.info(\n                "Unit ontology loop accepted render output without ontology critique at attempt %s/%s",\n                render_attempt,\n                max_visits,\n            )\n            return unit_state\n\n        for critic_attempt in range(1, max_visits + 1):\n',
        "ontology loop can skip critique",
    )

    # --- Patch 5: deepcopy fix for parallel workers (upstream #48) ---
    patcher.replace_exact(
        "ontocast",
        target("stategraph/node_factories.py"),
        '            budget_tracker=state.budget_tracker,\n            max_visits_per_node=tools.config.server.max_visits_per_node,\n            current_domain=state.current_domain,\n            ontology_max_triples=tools.config.server.ontology_max_triples,\n        )\n        result = await ontology_loop(bootstrap_state, atomic_tools)',
        '            budget_tracker=state.budget_tracker,\n            max_visits_per_node=tools.config.server.parallel_ontology_retries,\n            current_domain=state.current_domain,\n            ontology_max_triples=tools.config.server.ontology_max_triples,\n        )\n        result = await ontology_loop(bootstrap_state, atomic_tools)',
        "bootstrap ontology retry budget",
    )
    patcher.replace_exact(
        "ontocast",
        target("stategraph/node_factories.py"),
        '                base_state = state.model_copy(deep=True)\n                ontology_state = UnitOntologyState(\n                    content_unit=state.content_units[unit_index],\n                    ontology_snapshot=state.current_ontology,\n                    ontology_user_instruction=state.ontology_user_instruction,\n                    budget_tracker=base_state.budget_tracker,\n                    max_visits_per_node=tools.config.server.max_visits_per_node,\n                    current_domain=state.current_domain,\n                    ontology_max_triples=tools.config.server.ontology_max_triples,\n                )\n                result = await ontology_loop(ontology_state, atomic_tools)',
        '                budget_tracker = state.budget_tracker.model_copy(deep=True)\n                ontology_state = UnitOntologyState(\n                    content_unit=state.content_units[unit_index],\n                    ontology_snapshot=state.current_ontology,\n                    ontology_user_instruction=state.ontology_user_instruction,\n                    budget_tracker=budget_tracker,\n                    max_visits_per_node=tools.config.server.parallel_ontology_retries,\n                    current_domain=state.current_domain,\n                    ontology_max_triples=tools.config.server.ontology_max_triples,\n                )\n                result = await ontology_loop(ontology_state, atomic_tools)',
        "parallel ontology workers deepcopy budget tracker",
    )
    patcher.replace_exact(
        "ontocast",
        target("stategraph/node_factories.py"),
        '                base_state = state.model_copy(deep=True)\n                facts_state = UnitFactsState(\n                    content_unit=state.content_units[unit_index],\n                    ontology_snapshot=state.current_ontology,\n                    facts_user_instruction=state.facts_user_instruction,\n                    budget_tracker=base_state.budget_tracker,\n                    max_visits_per_node=tools.config.server.max_visits_per_node,\n                )\n                result = await facts_loop(facts_state, atomic_tools)',
        '                budget_tracker = state.budget_tracker.model_copy(deep=True)\n                facts_state = UnitFactsState(\n                    content_unit=state.content_units[unit_index],\n                    ontology_snapshot=state.current_ontology,\n                    facts_user_instruction=state.facts_user_instruction,\n                    budget_tracker=budget_tracker,\n                    max_visits_per_node=tools.config.server.parallel_facts_retries,\n                )\n                result = await facts_loop(facts_state, atomic_tools)',
        "parallel facts workers deepcopy budget tracker",
    )

    # --- Patch 6: RDFGraph.__deepcopy__ (upstream #48) ---
    patcher.insert_after_exact(
        "ontocast",
        target("onto/rdfgraph.py"),
        '    def copy(self) -> "RDFGraph":\n        """Create a copy of this RDFGraph.\n\n        Returns:\n            RDFGraph: A new RDFGraph instance with all triples and namespace bindings copied.\n        """\n        result = RDFGraph()\n\n        # Copy all triples\n        for triple in self:\n            result.add(triple)\n\n        # Copy namespace bindings\n        for prefix, uri in self.namespaces():\n            result.bind(prefix, uri)\n\n        return result\n',
        '\n    def __deepcopy__(self, memo):\n        """Deep-copy oxigraph-backed graphs into a plain in-memory RDFGraph."""\n        cached = memo.get(id(self))\n        if cached is not None:\n            return cached\n\n        result = RDFGraph()\n        memo[id(self)] = result\n\n        for prefix, uri in self.namespaces():\n            result.bind(prefix, uri)\n\n        skipped = 0\n        for subject, predicate, obj in self:\n            if isinstance(subject, tuple) or isinstance(predicate, tuple) or isinstance(obj, tuple):\n                skipped += 1\n                continue\n            try:\n                result.add((subject, predicate, obj))\n            except Exception as exc:\n                skipped += 1\n                logger.debug("Skipping triple during RDFGraph deepcopy: %s", exc)\n\n        if skipped:\n            logger.warning("Skipped %s RDF-star / unsupported triple(s) during RDFGraph deepcopy", skipped)\n\n        return result\n',
        "def __deepcopy__(self, memo):",
        "RDFGraph.__deepcopy__",
    )

    # --- Patch 7: SPARQL generation for RDF-star triples (upstream #49) ---
    patcher.replace_exact(
        "ontocast",
        target("onto/sparql_models.py"),
        '    def _generate_insert_query(self, graph: RDFGraph, prefix_block: str) -> str:\n        """Generate a SPARQL INSERT query for the given RDFGraph."""\n        if len(graph) == 0:\n            return ""\n\n        # Format triples for SPARQL using proper RDF term serialization\n        triple_patterns = []\n        for subject, predicate, obj in graph:\n            triple_patterns.append(\n                f"    {self._serialize_rdf_term(subject)} {self._serialize_rdf_term(predicate)} {self._serialize_rdf_term(obj)} ."\n            )\n\n        triples_block = "\\n".join(triple_patterns)\n\n        query_parts = []\n        if prefix_block:\n            query_parts.append(prefix_block)\n        query_parts.append("INSERT DATA {")\n        query_parts.append(triples_block)\n        query_parts.append("}")\n\n        return "\\n".join(query_parts)\n\n    def _generate_delete_query(self, graph: RDFGraph, prefix_block: str) -> str:\n        """Generate a SPARQL DELETE query for the given RDFGraph."""\n        if len(graph) == 0:\n            return ""\n\n        # Format triples for SPARQL using proper RDF term serialization\n        triple_patterns = []\n        for subject, predicate, obj in graph:\n            triple_patterns.append(\n                f"    {self._serialize_rdf_term(subject)} {self._serialize_rdf_term(predicate)} {self._serialize_rdf_term(obj)} ."\n            )\n\n        triples_block = "\\n".join(triple_patterns)\n\n        query_parts = []\n        if prefix_block:\n            query_parts.append(prefix_block)\n        query_parts.append("DELETE DATA {")\n        query_parts.append(triples_block)\n        query_parts.append("}")\n\n        return "\\n".join(query_parts)\n\n    def _serialize_rdf_term(self, term: Node) -> str:\n        """Serialize an RDF term to its SPARQL string representation."""\n',
        '    def _iter_supported_triples(self, graph: RDFGraph):\n        """Yield only triples safe for SPARQL update text."""\n        skipped = 0\n        for subject, predicate, obj in graph:\n            if isinstance(subject, tuple) or isinstance(predicate, tuple) or isinstance(obj, tuple):\n                skipped += 1\n                continue\n            yield subject, predicate, obj\n        if skipped:\n            logger.warning("Skipped %s tuple-valued RDF-star triple(s) in SPARQL update", skipped)\n\n    def _generate_insert_query(self, graph: RDFGraph, prefix_block: str) -> str:\n        """Generate a SPARQL INSERT query for the given RDFGraph."""\n        if len(graph) == 0:\n            return ""\n        triple_patterns = []\n        for subject, predicate, obj in self._iter_supported_triples(graph):\n            triple_patterns.append(\n                f"    {self._serialize_rdf_term(subject)} {self._serialize_rdf_term(predicate)} {self._serialize_rdf_term(obj)} ."\n            )\n        if not triple_patterns:\n            return ""\n        triples_block = "\\n".join(triple_patterns)\n        query_parts = []\n        if prefix_block:\n            query_parts.append(prefix_block)\n        query_parts.append("INSERT DATA {")\n        query_parts.append(triples_block)\n        query_parts.append("}")\n        return "\\n".join(query_parts)\n\n    def _generate_delete_query(self, graph: RDFGraph, prefix_block: str) -> str:\n        """Generate a SPARQL DELETE query for the given RDFGraph."""\n        if len(graph) == 0:\n            return ""\n        triple_patterns = []\n        for subject, predicate, obj in self._iter_supported_triples(graph):\n            triple_patterns.append(\n                f"    {self._serialize_rdf_term(subject)} {self._serialize_rdf_term(predicate)} {self._serialize_rdf_term(obj)} ."\n            )\n        if not triple_patterns:\n            return ""\n        triples_block = "\\n".join(triple_patterns)\n        query_parts = []\n        if prefix_block:\n            query_parts.append(prefix_block)\n        query_parts.append("DELETE DATA {")\n        query_parts.append(triples_block)\n        query_parts.append("}")\n        return "\\n".join(query_parts)\n\n    def _serialize_rdf_term(self, term: Node) -> str:\n        """Serialize an RDF term to its SPARQL string representation."""\n        if isinstance(term, tuple):\n            raise TypeError(f"Unsupported tuple-valued RDF term: {term!r}")\n',
        "SPARQL skips tuple-valued RDF-star triples",
    )

    # --- Patch 8: critic threshold relaxation ---
    patcher.replace_exact(
        "ontocast",
        target("agent/criticise_ontology.py"),
        "if critique.success or critique.score > 90:",
        "if critique.success or critique.score >= 80:",
        "ontology critic threshold relaxation",
    )
    patcher.replace_exact(
        "ontocast",
        target("agent/criticise_facts.py"),
        "if critique.success or critique.score > 90:",
        "if critique.success or critique.score >= 80:",
        "facts critic threshold relaxation",
    )

    # --- Patch 9: softer ontology critic prompt ---
    patcher.replace_exact(
        "ontocast",
        target("prompt/criticise_ontology.py"),
        "6. **Domain Coverage**: Includes implicit domain knowledge beyond literal text\n",
        "6. **Domain Coverage**: Includes implicit domain knowledge beyond literal text when clearly supported; missing optional enrichment alone should not block an otherwise coherent ontology\n",
        "ontology critic prompt domain coverage softened",
    )
    patcher.replace_exact(
        "ontocast",
        target("prompt/criticise_ontology.py"),
        "- Prioritize fixes that have cascading impact\n",
        "- Prioritize fixes that have cascading impact\n- Do not fail an otherwise sound ontology solely because it lacks optional implicit-domain enrichment beyond the source text\n",
        "ontology critic prompt optional enrichment softened",
    )

    # --- Patch 10: softer facts critic prompt ---
    patcher.replace_exact(
        "ontocast",
        target("prompt/criticise_facts.py"),
        "2. Completeness: Are all possible facts extracted from the text given the ontology?\n",
        "2. Completeness: Are all important facts extracted from the text given the ontology? Minor omissions should be treated as non-blocking unless they materially affect graph usefulness.\n",
        "facts critic prompt completeness softened",
    )

    # --- Patch 11: retain a document when the provider quota is exhausted ---
    patcher.replace_exact(
        "ontocast",
        target("cli/serve.py"),
        "import asyncio\nimport logging\n",
        "import asyncio\nimport logging\nimport os\n",
        "serve imports os for quota retry configuration",
    )
    patcher.replace_optional_exact(
        "ontocast",
        target("cli/serve.py"),
        '"OpenAI quota exhausted while processing %s; "',
        '"Subscription usage limit reached while processing %s; "',
        "legacy OpenAI quota log migrated to subscription wording",
    )
    patcher.replace_exact(
        "ontocast",
        target("cli/serve.py"),
        '''        async def process_files():
            for file_path in files:
                try:
                    state = AgentState(
                        files={file_path.as_posix(): file_path.read_bytes()},
                        max_visits=config.server.max_visits_per_node,
                        max_chunks=head_chunks,
                        render_mode=config.server.render_mode,
                        dataset=config.tool_config.fuseki.dataset,
                    )
                    async for _ in workflow.astream(
                        state,
                        stream_mode="values",
                        config=RunnableConfig(recursion_limit=recursion_limit),
                    ):
                        pass

                except Exception as e:
                    logger.error(f"Error processing {file_path}: {str(e)}")

''',
        '''        async def process_files():
            try:
                quota_retry_seconds = max(
                    60, int(os.getenv("ONTOCAST_QUOTA_RETRY_SECONDS", "900"))
                )
            except ValueError:
                quota_retry_seconds = 900

            for file_path in files:
                quota_attempt = 0
                while True:
                    try:
                        state = AgentState(
                            files={file_path.as_posix(): file_path.read_bytes()},
                            max_visits=config.server.max_visits_per_node,
                            max_chunks=head_chunks,
                            render_mode=config.server.render_mode,
                            dataset=config.tool_config.fuseki.dataset,
                        )
                        async for _ in workflow.astream(
                            state,
                            stream_mode="values",
                            config=RunnableConfig(recursion_limit=recursion_limit),
                        ):
                            pass
                        break

                    except Exception as e:
                        message = str(e)
                        quota_error_markers = (
                            "insufficient_quota",
                            "gousagelimiterror",
                            "freeusagelimiterror",
                            "monthly usage limit",
                            "usage limit reached",
                        )
                        if any(marker in message.lower() for marker in quota_error_markers):
                            quota_attempt += 1
                            logger.error(
                                "Subscription usage limit reached while processing %s; "
                                "retry %s in %s seconds without advancing to the next file.",
                                file_path,
                                quota_attempt,
                                quota_retry_seconds,
                            )
                            await asyncio.sleep(quota_retry_seconds)
                            continue
                        logger.error(f"Error processing {file_path}: {message}")
                        break

''',
        "retry the same document indefinitely after subscription usage limits",
    )


def apply_diversity(patcher: LocalPatcher) -> None:
    submodule = patcher.require_submodule(
        "diversity", "external/Diversity-Improvement-in-CBR"
    )

    patcher.replace_exact(
        "diversity",
        submodule / "Methods.py",
        "import gensim.downloader as api\nfrom numpy import dot\nfrom numpy.linalg import norm\nimport Levenshtein\n#API for text semantic text similarity\nword2vec_model = api.load(\"glove-wiki-gigaword-50\")\n#Case Base comes from an Excel provided by the supervisor\npath = r'C:\\Users\\emman\\Documents\\TEC\\Diversity-Improvement-in-CBR\\Datasets\\CleanedDATA V12-05-2021.csv'\ndf = pd.read_csv(path, sep=';', encoding='windows-1252')\n",
        "try:\n    import gensim.downloader as api\nexcept ImportError:  # Optional; only needed by the unused semantic similarity helper.\n    api = None\nfrom numpy import dot\nfrom numpy.linalg import norm\nimport Levenshtein\nfrom pathlib import Path\n#API for text semantic text similarity\nword2vec_model = None\n#Case Base comes from an Excel provided by the supervisor\n_SUBMODULE_DIR = Path(__file__).resolve().parent\npath = _SUBMODULE_DIR / \"Datasets\" / \"CleanedDATA V12-05-2021.csv\"\ndf = pd.read_csv(path, sep=';', encoding='windows-1252')\n",
        "Methods dataset path relative and optional gensim",
    )

    patcher.replace_exact(
        "diversity",
        submodule / "Methods2.py",
        "import random\n#API for text semantic text similarity\n#word2vec_model = api.load(\"glove-wiki-gigaword-50\")\n\n#Case Base comes from an Excel provided by the supervisor\npath = r'C:\\Users\\emman\\Documents\\TEC\\Diversity-Improvement-in-CBR\\Datasets\\CleanedDATA V12-05-2021.csv'\npath_performance = r'C:\\Users\\emman\\Documents\\TEC\\Diversity-Improvement-in-CBR\\Datasets\\performance_normalized_averaged.csv'\n",
        "import random\nfrom pathlib import Path\n#API for text semantic text similarity\n#word2vec_model = api.load(\"glove-wiki-gigaword-50\")\n\n#Case Base comes from an Excel provided by the supervisor\n_SUBMODULE_DIR = Path(__file__).resolve().parent\npath = _SUBMODULE_DIR / \"Datasets\" / \"CleanedDATA V12-05-2021.csv\"\npath_performance = _SUBMODULE_DIR / \"Datasets\" / \"performance_normalized_averaged.csv\"\n",
        "Methods2 dataset paths relative to submodule",
    )

    patcher.replace_exact(
        "diversity",
        submodule / "Methods2.py",
        "        if DistFin>=6:\n            Sim=0.1\n        elif (DistFin<5 and DistFin>2):\n            Sim=0.5\n        elif DistFin<2:\n            Sim=0.8\n        elif DistFin==0:\n            Sim=1\n        return Sim\n",
        "        if DistFin==0:\n            Sim=1\n        elif DistFin>=6:\n            Sim=0.1\n        elif (DistFin<5 and DistFin>2):\n            Sim=0.5\n        elif DistFin<2:\n            Sim=0.8\n        return Sim\n",
        "SimTaxon exact match returns 1",
    )

    patcher.replace_exact(
        "diversity",
        submodule / "Validation.py",
        "        solutions_condensed,descriptions_condensed=apply_CNN(sol, des, CaseBase_Train, weights_description, weights_solution)\n",
        "        solutions_condensed,descriptions_condensed=apply_CNN(des, sol, CaseBase_Train, weights_description, weights_solution)\n",
        "Validation apply_CNN threshold order",
    )

    patcher.replace_exact(
        "diversity",
        submodule / "Validation.py",
        "            diversity=retrieval_for_ModCNN(solutions_condensed,descriptions_condensed,query)\n",
        "            diversity=retrieval_for_ModCNN(solutions_condensed,descriptions_condensed,query,weights_description,weights_solution)\n",
        "Validation retrieval_for_ModCNN passes weights",
    )

    patcher.replace_exact(
        "diversity",
        submodule / "Modified_Condensed_Nearest_Neighbors.py",
        "    for most_similar in similar_GC:\n        for generalized_solution in solutions_store:\n            if generalized_solution.parent_description == most_similar[0]:\n                list_solution.append(generalized_solution)\n                if len(list_solution) >= amount:\n                    return list_solution\n\n\ndef compute_diversity(candidates,weights):\n",
        "    for most_similar in similar_GC:\n        for generalized_solution in solutions_store:\n            if generalized_solution.parent_description == most_similar[0]:\n                list_solution.append(generalized_solution)\n                if len(list_solution) >= amount:\n                    return list_solution\n    return list_solution\n\n\ndef compute_diversity(candidates,weights):\n",
        "search_solutions_from_descriptions returns partial results",
    )

    patcher.replace_exact(
        "diversity",
        submodule / "Performance_Dataset_Generation.py",
        "import re\n\n#Nuevo\nimport pandas as pd\nfrom sklearn import preprocessing\n",
        "import re\nfrom pathlib import Path\n\n#Nuevo\nimport pandas as pd\nfrom sklearn import preprocessing\n",
        "Performance generator imports pathlib",
    )
    patcher.replace_exact(
        "diversity",
        submodule / "Performance_Dataset_Generation.py",
        "path = r\"C:\\Users\\emman\\Documents\\TEC\\Diversity-Improvement-in-CBR\\Datasets\\Performance_cleaned.xlsx\"\ndf = pd.read_excel(path)\n",
        "_SUBMODULE_DIR = Path(__file__).resolve().parent\n_DATASET_DIR = _SUBMODULE_DIR / \"Datasets\"\npath = _DATASET_DIR / \"Performance_cleaned.xlsx\"\ndf = pd.read_excel(path)\n",
        "Performance generator input path relative to submodule",
    )
    patcher.replace_exact(
        "diversity",
        submodule / "Performance_Dataset_Generation.py",
        "Performance.to_excel('Performance.xlsx', index=False)\n",
        "Performance.to_excel(_DATASET_DIR / 'Performance.xlsx', index=False)\n",
        "Performance generator writes cleaned workbook under Datasets",
    )
    patcher.replace_exact(
        "diversity",
        submodule / "Performance_Dataset_Generation.py",
        "Performance.to_excel('performance_normalized.xlsx', index=False)\n",
        "Performance.to_excel(_DATASET_DIR / 'performance_normalized.xlsx', index=False)\n",
        "Performance generator writes normalized workbook under Datasets",
    )
    patcher.replace_exact(
        "diversity",
        submodule / "Performance_Dataset_Generation.py",
        "Performance.to_csv('performance_normalized_averaged.csv', index=False)\n",
        "Performance.to_csv(_DATASET_DIR / 'performance_normalized_averaged.csv', index=False)\n",
        "Performance generator writes normalized csv under Datasets",
    )


def validate_cbr(patcher: LocalPatcher) -> None:
    patcher.require_submodule("cbr", "external/CBR-Ontology-For-Predictive-Maintenance")
    patcher.notes.append("[cbr] no local patches registered; existence validation only")


def selected_dependencies(value: str) -> tuple[str, ...]:
    if value == "all":
        return ("ontocast", "cbr", "diversity")
    return (value,)


def print_summary(patcher: LocalPatcher, dependencies: tuple[str, ...]) -> None:
    print(f"Local patch root: {patcher.root}")
    print(f"Dependencies requested: {', '.join(dependencies)}")

    if patcher.notes:
        print("\nValidation notes:")
        for note in patcher.notes:
            print(f"  - {note}")

    if patcher.results:
        print("\nPatch operations:")
        for result in patcher.results:
            print(
                f"  - [{result.dependency}] {result.status:7} "
                f"{result.path} :: {result.label}"
            )

    changed = patcher.changed_files()
    print("\nChanged files:")
    if changed:
        for path in changed:
            print(f"  - {path}")
    else:
        print("  - none (already patched or validation-only run)")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply idempotent local patches to vendored submodules."
    )
    parser.add_argument(
        "--dependency",
        choices=DEPENDENCIES,
        default="all",
        help="Dependency to patch/validate (default: all)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    try:
        root = locate_repo_root()
        patcher = LocalPatcher(root)
        dependencies = selected_dependencies(args.dependency)

        for dependency in dependencies:
            if dependency == "ontocast":
                apply_ontocast(patcher)
            elif dependency == "diversity":
                apply_diversity(patcher)
            elif dependency == "cbr":
                validate_cbr(patcher)
            else:  # Defensive guard; argparse choices should prevent this.
                raise PatchError(f"Unknown dependency: {dependency}")

        print_summary(patcher, dependencies)
        return 0
    except PatchError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
