from __future__ import annotations

import importlib.util
from pathlib import Path


def replace_text(path: Path, old: str, new: str) -> None:
    content = path.read_text()
    if old not in content:
        raise RuntimeError(f"Expected text not found in {path}")
    path.write_text(content.replace(old, new))


def main() -> None:
    spec = importlib.util.find_spec("ontocast")
    if spec is None or spec.origin is None:
        raise RuntimeError("Could not locate installed ontocast package")

    package_dir = Path(spec.origin).resolve().parent

    replace_text(
        package_dir / "config.py",
        """    enable_ontology_consolidation: bool = Field(\n        default=False,\n        description=\"Run optional ontology consolidation pass after normalization\",\n    )\n""",
        """    enable_ontology_consolidation: bool = Field(\n        default=False,\n        description=\"Run optional ontology consolidation pass after normalization\",\n    )\n    skip_ontology_critique: bool = Field(\n        default=False,\n        description=(\n            \"Experimental fast path: accept successful ontology render output \"\n            \"without running the ontology critic loop. This also affects \"\n            \"bootstrap ontology generation.\"\n        ),\n    )\n""",
    )

    replace_text(
        package_dir / "tool" / "atomic.py",
        """        web_search_for_facts_render: bool = False,\n        web_search_for_facts_critic: bool = False,\n        web_search_planner_enabled: bool = True,\n""",
        """        web_search_for_facts_render: bool = False,\n        web_search_for_facts_critic: bool = False,\n        skip_ontology_critique: bool = False,\n        web_search_planner_enabled: bool = True,\n""",
    )
    replace_text(
        package_dir / "tool" / "atomic.py",
        """            self.web_search_for_facts_render = web_search_config.facts_render_enabled\n            self.web_search_for_facts_critic = web_search_config.facts_critic_enabled\n            self.web_search_planner_enabled = web_search_config.planner_enabled\n""",
        """            self.web_search_for_facts_render = web_search_config.facts_render_enabled\n            self.web_search_for_facts_critic = web_search_config.facts_critic_enabled\n            self.skip_ontology_critique = skip_ontology_critique\n            self.web_search_planner_enabled = web_search_config.planner_enabled\n""",
    )
    replace_text(
        package_dir / "tool" / "atomic.py",
        """            self.web_search_for_facts_render = web_search_for_facts_render\n            self.web_search_for_facts_critic = web_search_for_facts_critic\n            self.web_search_planner_enabled = web_search_planner_enabled\n""",
        """            self.web_search_for_facts_render = web_search_for_facts_render\n            self.web_search_for_facts_critic = web_search_for_facts_critic\n            self.skip_ontology_critique = skip_ontology_critique\n            self.web_search_planner_enabled = web_search_planner_enabled\n""",
    )

    replace_text(
        package_dir / "toolbox.py",
        """        self.atomic_tools = AtomicToolBox(\n            llm_provider=self,\n            search_provider=self.search_provider,\n            web_search_config=tool_config.web_search,\n        )\n""",
        """        self.atomic_tools = AtomicToolBox(\n            llm_provider=self,\n            search_provider=self.search_provider,\n            web_search_config=tool_config.web_search,\n            skip_ontology_critique=config.server.skip_ontology_critique,\n        )\n""",
    )

    replace_text(
        package_dir / "stategraph" / "atomic.py",
        """        if unit_state.status != Status.SUCCESS:\n            render_request = unit_state.get_external_evidence_request(\n                WorkflowNode.TEXT_TO_ONTOLOGY\n            )\n            if render_request.initiate_search:\n                unit_state = await plan_external_evidence_for_node(\n                    unit_state, tools, WorkflowNode.TEXT_TO_ONTOLOGY\n                )\n                unit_state = await fetch_external_evidence_for_node(\n                    unit_state, tools, WorkflowNode.TEXT_TO_ONTOLOGY\n                )\n                unit_state = await render_ontology(unit_state, tools)\n                if unit_state.status == Status.SUCCESS:\n                    logger.info(\n                        \"Unit ontology render recovered with search at attempt %s/%s\",\n                        render_attempt,\n                        max_visits,\n                    )\n                else:\n                    logger.info(\n                        \"Unit ontology render failed at attempt %s/%s (with search)\",\n                        render_attempt,\n                        max_visits,\n                    )\n                    continue\n            else:\n                logger.info(\n                    \"Unit ontology render failed at attempt %s/%s (no search request)\",\n                    render_attempt,\n                    max_visits,\n                )\n                continue\n\n        for critic_attempt in range(1, max_visits + 1):\n""",
        """        if unit_state.status != Status.SUCCESS:\n            render_request = unit_state.get_external_evidence_request(\n                WorkflowNode.TEXT_TO_ONTOLOGY\n            )\n            if render_request.initiate_search:\n                unit_state = await plan_external_evidence_for_node(\n                    unit_state, tools, WorkflowNode.TEXT_TO_ONTOLOGY\n                )\n                unit_state = await fetch_external_evidence_for_node(\n                    unit_state, tools, WorkflowNode.TEXT_TO_ONTOLOGY\n                )\n                unit_state = await render_ontology(unit_state, tools)\n                if unit_state.status == Status.SUCCESS:\n                    logger.info(\n                        \"Unit ontology render recovered with search at attempt %s/%s\",\n                        render_attempt,\n                        max_visits,\n                    )\n                else:\n                    logger.info(\n                        \"Unit ontology render failed at attempt %s/%s (with search)\",\n                        render_attempt,\n                        max_visits,\n                    )\n                    continue\n            else:\n                logger.info(\n                    \"Unit ontology render failed at attempt %s/%s (no search request)\",\n                    render_attempt,\n                    max_visits,\n                )\n                continue\n\n        if tools.skip_ontology_critique:\n            logger.info(\n                \"Unit ontology loop accepted render output without ontology critique at attempt %s/%s\",\n                render_attempt,\n                max_visits,\n            )\n            return unit_state\n\n        for critic_attempt in range(1, max_visits + 1):\n""",
    )

    print(f"Patched ontocast package at {package_dir}")


if __name__ == "__main__":
    main()
