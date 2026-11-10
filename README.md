# Benchmarking LLM capabilities for ontology development and case extraction from predictive maintenance literature: An OntoCast study informed by the OPMAD ontology

**Abstract:** This work presents an experimental comparison of the capabilities of humans (OPMAD authors) and large language models (LLMs) for the tasks of ontology development and case extraction from predictive maintenance literature.
LLMs were inferenced via the OntoCast Python library using a tailored extraction prompt constrained by a human-made ontology (OPMAD), and tasked to extract predictive maintenance cases and their associated facts from a corpus of 102 papers that had been previously extracted by the same human authors of the OPMAD ontology.
The LLM- and human-extracted facts were compared using quality metrics.
Then, the same 102-paper corpus was used to evolve a predictive maintenance case ontology from zero using OntoCast, whose quality was compared against OPMAD.

## Pipeline

0. Convert OPMAD and its bundled dependencies to Turtle with `scripts/convert_opmad.py` ([details and OntoCast usage](ontologies/opmad-ontocast/README.md)). Define comparison criteria.
1. Extract cases from papers using OntoCast in facts-only (no ontology evolution) mode. The exact extraction instruction used is:

> The very basic structure of a case starts with an instance of a  `Predictive maintenance case` (subclass of `Designative Information Content Entity`), designating an instance of a `Predictive maintenance system module` (subclass of `Information Processing Artifact`). The items to be maintained are instances of the diﬀerent subclasses in `Maintainable item` (equivalent to `Artifact`). Then, the models are instances of the type subclasses in the `Predictive maintenance model`. The models operate over a set of variables that are recovered from the operation of the item. These variables are instances of `Data variable` (subclass of `Descriptive Information Content Entity`). As the instances of variables are physical concepts (for example, the temperature), they can be reused in more than one case of the database. For each one of the diﬀerent measurable magnitudes that are mentioned in the database, there exists one single instance of `Data variable`. The functioning of the module and the models used for a certain case are explained in the corresponding `Predictive maintenance article`. Extract every case reported in this article, not in other papers articles within it, and all case-related facts expressible using the supplied ontology.

The definition of a case is taken from "Integrating Ontologies and Case-based Reasoning for the Development of Knowledge-intensive Intelligent Systems".
