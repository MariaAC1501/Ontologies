# Benchmarking LLM capabilities for ontology development and case extraction from predictive maintenance literature: A comparison of OPMAD and OntoCast

This repo contains an experimental comparison of the capabilities of humans (OPMAD authors) and large language models (LLMs) inferenced via OntoCast, for the task of ontology development and case extraction from predictive maintenance literature.

## Pipeline

0. Convert OPMAD and its bundled dependencies to Turtle with `scripts/convert_opmad.py` ([details and OntoCast usage](ontologies/opmad-ontocast/README.md)). Define comparison criteria.
1. Extract cases from papers using OntoCast in facts-only (no ontology evolution) mode. The exact extraction instruction used is:

> The very basic structure of a case starts with an instance of a  `Predictive maintenance case` (subclass of `Designative Information Content Entity`), designating an instance of a `Predictive maintenance system module` (subclass of `Information Processing Artifact`). The items to be maintained are instances of the diﬀerent subclasses in `Maintainable item` (equivalent to `Artifact`). Then, the models are instances of the type subclasses in the `Predictive maintenance model`. The models operate over a set of variables that are recovered from the operation of the item. These variables are instances of `Data variable` (subclass of `Descriptive Information Content Entity`). As the instances of variables are physical concepts (for example, the temperature), they can be reused in more than one case of the database. For each one of the diﬀerent measurable magnitudes that are mentioned in the database, there exists one single instance of `Data variable`. The functioning of the module and the models used for a certain case are explained in the corresponding `Predictive maintenance article`. Extract every case reported in this article, not in other papers articles within it, and all case-related facts expressible using the supplied ontology.

The definition of a case is taken from "Integrating Ontologies and Case-based Reasoning for the Development of Knowledge-intensive Intelligent Systems".
