# Benchmarking LLM capabilities for ontology development and case extraction from predictive maintenance literature: A comparison of OPMAD and OntoCast

This repo contains an experimental comparison of the capabilities of humans (OPMAD authors) and large language models (LLMs) inferenced via OntoCast, for the task of ontology development and case extraction from predictive maintenance literature.

## Pipeline

0. Convert OPMAD and its bundled dependencies to Turtle with `scripts/convert_opmad.py` ([details and OntoCast usage](ontologies/opmad-ontocast/README.md)). Define comparison criteria.
1. Extract cases from papers using OntoCast in facts-only (no ontology evolution) mode. The exact extraction instruction used is:

> Extract every predictive maintenance case reported in this paper and all case-related facts expressible using the supplied ontology.
