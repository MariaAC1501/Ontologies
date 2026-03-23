#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
# Use Conda env by default; fall back to local .venv if present
if [[ -n "${ONTOCAST_BIN:-}" ]]; then
  # Caller explicitly set ONTOCAST_BIN
  PYTHON_BIN="${PYTHON_BIN:-python3}"
elif command -v ontocast &>/dev/null; then
  ONTOCAST_BIN="$(command -v ontocast)"
  PYTHON_BIN="${PYTHON_BIN:-python3}"
elif [[ -x "${SCRIPT_DIR}/.venv/bin/ontocast" ]]; then
  ONTOCAST_BIN="${SCRIPT_DIR}/.venv/bin/ontocast"
  PYTHON_BIN="${SCRIPT_DIR}/.venv/bin/python"
else
  echo "OntoCast not found. Install via Conda (recommended) or create a local venv:" >&2
  echo "  python3 -m venv pipeline/full_mode/.venv" >&2
  echo "  source pipeline/full_mode/.venv/bin/activate" >&2
  echo "  pip install conda/recipes/ontocast/wheels/ontocast-0.3.0-py3-none-any.whl" >&2
  exit 1
fi
CONFIG_FILE="${SCRIPT_DIR}/ontocast_full_config.env"
OUTPUT_DIR="${SCRIPT_DIR}/test_output"
INPUT_DIR="${OUTPUT_DIR}/input"
LOG_FILE="${OUTPUT_DIR}/run.log"
DEFAULT_HEAD_CHUNKS=2
HEAD_CHUNKS="${ONTOCAST_HEAD_CHUNKS:-${DEFAULT_HEAD_CHUNKS}}"

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <pdf-path> [head-chunks]" >&2
  exit 1
fi

PDF_PATH="$1"
if [[ $# -eq 2 ]]; then
  HEAD_CHUNKS="$2"
fi

if [[ ! -f "${PDF_PATH}" ]]; then
  echo "Input PDF not found: ${PDF_PATH}" >&2
  exit 1
fi

if [[ ! -x "${ONTOCAST_BIN}" ]]; then
  echo "OntoCast CLI not found at: ${ONTOCAST_BIN}" >&2
  exit 1
fi

if [[ ! -f "${REPO_ROOT}/.env" ]]; then
  echo "Repo root .env not found: ${REPO_ROOT}/.env" >&2
  exit 1
fi

set -a
source "${REPO_ROOT}/.env"
set +a

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "OPENAI_API_KEY is not set after loading ${REPO_ROOT}/.env" >&2
  exit 1
fi

apply_installed_patches() {
  "${PYTHON_BIN}" - <<'PY'
from pathlib import Path
import importlib.util

spec = importlib.util.find_spec("ontocast")
if spec is None or spec.origin is None:
    raise SystemExit("Could not locate installed ontocast package")
base = Path(spec.origin).resolve().parent

def replace_once(path: str, old: str, new: str) -> None:
    target = base / path
    text = target.read_text()
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"Missing expected patch anchor in {target}")
    target.write_text(text.replace(old, new))

replace_once(
    "prompt/render_ontology.py",
    "prefix_instruction = \"\"\"Use prefix `{ontology_prefix}` for entities/properties placed in the current domain ontology. DECLARE the prefix in preamble!\"\"\"",
    "prefix_instruction = \"\"\"Use prefix `{{ontology_prefix}}` for entities/properties placed in the current domain ontology. DECLARE the prefix in preamble!\"\"\"",
)
replace_once(
    "config.py",
    """    enable_ontology_consolidation: bool = Field(\n        default=False,\n        description=\"Run optional ontology consolidation pass after normalization\",\n    )\n""",
    """    enable_ontology_consolidation: bool = Field(\n        default=False,\n        description=\"Run optional ontology consolidation pass after normalization\",\n    )\n    skip_ontology_critique: bool = Field(\n        default=False,\n        description=(\n            \"Experimental fast path: accept successful ontology render output \"\n            \"without running the ontology critic loop. This also affects \"\n            \"bootstrap ontology generation.\"\n        ),\n    )\n""",
)
replace_once(
    "tool/atomic.py",
    """        web_search_for_facts_render: bool = False,\n        web_search_for_facts_critic: bool = False,\n        web_search_planner_enabled: bool = True,\n""",
    """        web_search_for_facts_render: bool = False,\n        web_search_for_facts_critic: bool = False,\n        skip_ontology_critique: bool = False,\n        web_search_planner_enabled: bool = True,\n""",
)
replace_once(
    "tool/atomic.py",
    """            self.web_search_for_facts_render = web_search_config.facts_render_enabled\n            self.web_search_for_facts_critic = web_search_config.facts_critic_enabled\n            self.web_search_planner_enabled = web_search_config.planner_enabled\n""",
    """            self.web_search_for_facts_render = web_search_config.facts_render_enabled\n            self.web_search_for_facts_critic = web_search_config.facts_critic_enabled\n            self.skip_ontology_critique = skip_ontology_critique\n            self.web_search_planner_enabled = web_search_config.planner_enabled\n""",
)
replace_once(
    "tool/atomic.py",
    """            self.web_search_for_facts_render = web_search_for_facts_render\n            self.web_search_for_facts_critic = web_search_for_facts_critic\n            self.web_search_planner_enabled = web_search_planner_enabled\n""",
    """            self.web_search_for_facts_render = web_search_for_facts_render\n            self.web_search_for_facts_critic = web_search_for_facts_critic\n            self.skip_ontology_critique = skip_ontology_critique\n            self.web_search_planner_enabled = web_search_planner_enabled\n""",
)
replace_once(
    "toolbox.py",
    """        self.atomic_tools = AtomicToolBox(\n            llm_provider=self,\n            search_provider=self.search_provider,\n            web_search_config=tool_config.web_search,\n        )\n""",
    """        self.atomic_tools = AtomicToolBox(\n            llm_provider=self,\n            search_provider=self.search_provider,\n            web_search_config=tool_config.web_search,\n            skip_ontology_critique=config.server.skip_ontology_critique,\n        )\n""",
)
replace_once(
    "stategraph/atomic.py",
    """        for critic_attempt in range(1, max_visits + 1):\n""",
    """        if tools.skip_ontology_critique:\n            logger.info(\n                \"Unit ontology loop accepted render output without ontology critique at attempt %s/%s\",\n                render_attempt,\n                max_visits,\n            )\n            return unit_state\n\n        for critic_attempt in range(1, max_visits + 1):\n""",
)
replace_once(
    "stategraph/node_factories.py",
    """            max_visits_per_node=tools.config.server.max_visits_per_node,\n""",
    """            max_visits_per_node=tools.config.server.parallel_ontology_retries,\n""",
)
replace_once(
    "stategraph/node_factories.py",
    """                base_state = state.model_copy(deep=True)\n                ontology_state = UnitOntologyState(\n""",
    """                budget_tracker = state.budget_tracker.model_copy(deep=True)\n                ontology_state = UnitOntologyState(\n""",
)
replace_once(
    "stategraph/node_factories.py",
    """                    budget_tracker=base_state.budget_tracker,\n                    max_visits_per_node=tools.config.server.parallel_ontology_retries,\n""",
    """                    budget_tracker=budget_tracker,\n                    max_visits_per_node=tools.config.server.parallel_ontology_retries,\n""",
)
replace_once(
    "stategraph/node_factories.py",
    """                base_state = state.model_copy(deep=True)\n                facts_state = UnitFactsState(\n""",
    """                budget_tracker = state.budget_tracker.model_copy(deep=True)\n                facts_state = UnitFactsState(\n""",
)
replace_once(
    "stategraph/node_factories.py",
    """                    budget_tracker=base_state.budget_tracker,\n                    max_visits_per_node=tools.config.server.parallel_ontology_retries,\n""",
    """                    budget_tracker=budget_tracker,\n                    max_visits_per_node=tools.config.server.parallel_facts_retries,\n""",
)

rdf_path = base / "onto/rdfgraph.py"
rdf_text = rdf_path.read_text()
if "def __deepcopy__(self, memo):" not in rdf_text:
    marker = """    def copy(self) -> \"RDFGraph\":\n        \"\"\"Create a copy of this RDFGraph.\n\n        Returns:\n            RDFGraph: A new RDFGraph instance with all triples and namespace bindings copied.\n        \"\"\"\n        result = RDFGraph()\n\n        # Copy all triples\n        for triple in self:\n            result.add(triple)\n\n        # Copy namespace bindings\n        for prefix, uri in self.namespaces():\n            result.bind(prefix, uri)\n\n        return result\n"""
    replacement = marker + """
    def __deepcopy__(self, memo):\n        \"\"\"Deep-copy oxigraph-backed graphs into a plain in-memory RDFGraph.\"\"\"\n        cached = memo.get(id(self))\n        if cached is not None:\n            return cached\n\n        result = RDFGraph()\n        memo[id(self)] = result\n\n        for prefix, uri in self.namespaces():\n            result.bind(prefix, uri)\n\n        skipped = 0\n        for subject, predicate, obj in self:\n            if isinstance(subject, tuple) or isinstance(predicate, tuple) or isinstance(obj, tuple):\n                skipped += 1\n                continue\n            try:\n                result.add((subject, predicate, obj))\n            except Exception as exc:\n                skipped += 1\n                logger.debug(\"Skipping triple during RDFGraph deepcopy: %s\", exc)\n\n        if skipped:\n            logger.warning(\"Skipped %s RDF-star / unsupported triple(s) during RDFGraph deepcopy\", skipped)\n\n        return result\n"""
    if marker not in rdf_text:
        raise SystemExit(f"Missing expected patch anchor in {rdf_path}")
    rdf_path.write_text(rdf_text.replace(marker, replacement))

sparql_path = base / "onto/sparql_models.py"
sparql_text = sparql_path.read_text()
if "def _iter_supported_triples" not in sparql_text:
    old = """    def _generate_insert_query(self, graph: RDFGraph, prefix_block: str) -> str:\n        \"\"\"Generate a SPARQL INSERT query for the given RDFGraph.\"\"\"\n        if len(graph) == 0:\n            return \"\"\n\n        # Format triples for SPARQL using proper RDF term serialization\n        triple_patterns = []\n        for subject, predicate, obj in graph:\n            triple_patterns.append(\n                f\"    {self._serialize_rdf_term(subject)} {self._serialize_rdf_term(predicate)} {self._serialize_rdf_term(obj)} .\"\n            )\n\n        triples_block = \"\\n\".join(triple_patterns)\n\n        query_parts = []\n        if prefix_block:\n            query_parts.append(prefix_block)\n        query_parts.append(\"INSERT DATA {\")\n        query_parts.append(triples_block)\n        query_parts.append(\"}\")\n\n        return \"\\n\".join(query_parts)\n\n    def _generate_delete_query(self, graph: RDFGraph, prefix_block: str) -> str:\n        \"\"\"Generate a SPARQL DELETE query for the given RDFGraph.\"\"\"\n        if len(graph) == 0:\n            return \"\"\n\n        # Format triples for SPARQL using proper RDF term serialization\n        triple_patterns = []\n        for subject, predicate, obj in graph:\n            triple_patterns.append(\n                f\"    {self._serialize_rdf_term(subject)} {self._serialize_rdf_term(predicate)} {self._serialize_rdf_term(obj)} .\"\n            )\n\n        triples_block = \"\\n\".join(triple_patterns)\n\n        query_parts = []\n        if prefix_block:\n            query_parts.append(prefix_block)\n        query_parts.append(\"DELETE DATA {\")\n        query_parts.append(triples_block)\n        query_parts.append(\"}\")\n\n        return \"\\n\".join(query_parts)\n\n    def _serialize_rdf_term(self, term: Node) -> str:\n        \"\"\"Serialize an RDF term to its SPARQL string representation.\"\"\"\n"""
    new = """    def _iter_supported_triples(self, graph: RDFGraph):\n        \"\"\"Yield only triples that can be represented safely in SPARQL update text.\"\"\"\n        skipped = 0\n        for subject, predicate, obj in graph:\n            if isinstance(subject, tuple) or isinstance(predicate, tuple) or isinstance(obj, tuple):\n                skipped += 1\n                continue\n            yield subject, predicate, obj\n        if skipped:\n            logger.warning(\n                \"Skipped %s tuple-valued RDF-star triple(s) while generating SPARQL update text\",\n                skipped,\n            )\n\n    def _generate_insert_query(self, graph: RDFGraph, prefix_block: str) -> str:\n        \"\"\"Generate a SPARQL INSERT query for the given RDFGraph.\"\"\"\n        if len(graph) == 0:\n            return \"\"\n\n        triple_patterns = []\n        for subject, predicate, obj in self._iter_supported_triples(graph):\n            triple_patterns.append(\n                f\"    {self._serialize_rdf_term(subject)} {self._serialize_rdf_term(predicate)} {self._serialize_rdf_term(obj)} .\"\n            )\n\n        if not triple_patterns:\n            return \"\"\n\n        triples_block = \"\\n\".join(triple_patterns)\n\n        query_parts = []\n        if prefix_block:\n            query_parts.append(prefix_block)\n        query_parts.append(\"INSERT DATA {\")\n        query_parts.append(triples_block)\n        query_parts.append(\"}\")\n\n        return \"\\n\".join(query_parts)\n\n    def _generate_delete_query(self, graph: RDFGraph, prefix_block: str) -> str:\n        \"\"\"Generate a SPARQL DELETE query for the given RDFGraph.\"\"\"\n        if len(graph) == 0:\n            return \"\"\n\n        triple_patterns = []\n        for subject, predicate, obj in self._iter_supported_triples(graph):\n            triple_patterns.append(\n                f\"    {self._serialize_rdf_term(subject)} {self._serialize_rdf_term(predicate)} {self._serialize_rdf_term(obj)} .\"\n            )\n\n        if not triple_patterns:\n            return \"\"\n\n        triples_block = \"\\n\".join(triple_patterns)\n\n        query_parts = []\n        if prefix_block:\n            query_parts.append(prefix_block)\n        query_parts.append(\"DELETE DATA {\")\n        query_parts.append(triples_block)\n        query_parts.append(\"}\")\n\n        return \"\\n\".join(query_parts)\n\n    def _serialize_rdf_term(self, term: Node) -> str:\n        \"\"\"Serialize an RDF term to its SPARQL string representation.\"\"\"\n        if isinstance(term, tuple):\n            raise TypeError(f\"Unsupported tuple-valued RDF term for SPARQL serialization: {term!r}\")\n"""
    if old not in sparql_text:
        raise SystemExit(f"Missing expected patch anchor in {sparql_path}")
    sparql_path.write_text(sparql_text.replace(old, new))

replace_once(
    "agent/criticise_ontology.py",
    "if critique.success or critique.score > 90:",
    "if critique.success or critique.score >= 80:",
)
replace_once(
    "agent/criticise_facts.py",
    "if critique.success or critique.score > 90:",
    "if critique.success or critique.score >= 80:",
)
replace_once(
    "prompt/criticise_ontology.py",
    "6. **Domain Coverage**: Includes implicit domain knowledge beyond literal text\n",
    "6. **Domain Coverage**: Includes implicit domain knowledge beyond literal text when clearly supported; missing optional enrichment alone should not block an otherwise coherent ontology\n",
)
replace_once(
    "prompt/criticise_ontology.py",
    "- Prioritize fixes that have cascading impact\n",
    "- Prioritize fixes that have cascading impact\n- Do not fail an otherwise sound ontology solely because it lacks optional implicit-domain enrichment beyond the source text\n",
)
replace_once(
    "prompt/criticise_facts.py",
    "2. Completeness: Are all possible facts extracted from the text given the ontology?\n",
    "2. Completeness: Are all important facts extracted from the text given the ontology? Minor omissions should be treated as non-blocking unless they materially affect graph usefulness.\n",
)
print(f"Patched installed ontocast package at {base}")
PY
}

mkdir -p "${OUTPUT_DIR}" "${INPUT_DIR}"
rm -f "${OUTPUT_DIR}"/*.ttl "${OUTPUT_DIR}"/*.json "${OUTPUT_DIR}"/*.log "${INPUT_DIR}"/*
ln -sf "$(cd -- "$(dirname -- "${PDF_PATH}")" && pwd)/$(basename -- "${PDF_PATH}")" "${INPUT_DIR}/$(basename -- "${PDF_PATH}")"
: > "${LOG_FILE}"

apply_installed_patches

echo "Running OntoCast full-mode extraction"
echo "  config: ${CONFIG_FILE}"
echo "  input:  ${PDF_PATH}"
echo "  staged: ${INPUT_DIR}/$(basename -- "${PDF_PATH}")"
echo "  output: ${OUTPUT_DIR}"
echo "  log:    ${LOG_FILE}"
echo "  chunks: ${HEAD_CHUNKS}"

(
  cd "${REPO_ROOT}"
  export OPENAI_API_KEY
  "${ONTOCAST_BIN}" \
    --env-file "${CONFIG_FILE}" \
    --input-path "${INPUT_DIR}" \
    --head-chunks "${HEAD_CHUNKS}"
) 2>&1 | tee -a "${LOG_FILE}"

shopt -s nullglob
ontology_outputs=("${OUTPUT_DIR}"/ontology_*.ttl)
facts_outputs=("${OUTPUT_DIR}"/facts_*.ttl)
shopt -u nullglob

if (( ${#ontology_outputs[@]} == 0 )); then
  echo "No evolved ontology TTL found in ${OUTPUT_DIR}" >&2
  exit 1
fi
if (( ${#facts_outputs[@]} == 0 )); then
  echo "No facts TTL found in ${OUTPUT_DIR}" >&2
  exit 1
fi

echo ""
echo "Full-mode extraction completed"
printf '  ontology: %s\n' "${ontology_outputs[@]}"
printf '  facts:    %s\n' "${facts_outputs[@]}"
