# Ontologies
La Ontología está descrita en OWL

Usamos la Ontología definida en "INTEGRATING ONTOLOGIES AND CASE-BASED REASONING FOR THE
DEVELOPMENT OF KNOWLEDGE-INTENSIVE INTELLIGENT SYSTEMS."

Pasos de OWL a OWL:
1.Desde OWL extraer solo el “Shape” estructural, generar un modelo Pydantic solo para extracción
2.Usar LangExtract (Solo se puede usar desde Pydantic)
3.Convertir Pydantic → RDF Graph (rdflib)
4.RDF a OWL con owlready2



## Tasks
- [x] Determinar si hay lenguaje formal para describir Ontologías.
- [x] Buscar Ontología usada en el paper de Montero.
- [x] Convertir la Ontología del paper a OWL.
- [x] Investigar como cargar OWL a Python.
