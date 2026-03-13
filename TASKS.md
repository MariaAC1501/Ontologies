# Ontologies
La Ontología está descrita en OWL

Usamos Ontology Model for Maintenance Strategy Selection and Assessment (OMSSA) definida en "INTEGRATING ONTOLOGIES AND CASE-BASED REASONING FOR THE DEVELOPMENT OF KNOWLEDGE-INTENSIVE INTELLIGENT SYSTEMS." 
Link: https://github.com/jjmj128/CBR-Ontology-For-Predictive-Maintenance

Ya existen 2 repositorios que extraen de un texto la Ontologia que necesito
https://github.com/monarch-initiative/ontogpt/
https://github.com/growgraph/ontocast

## Tasks
- [x] Determinar si hay lenguaje formal para describir Ontologías.
- [x] Buscar Ontología usada en el paper de Montero.
- [x] Descargar la Ontología del paper a OWL.
- [x] Investigar como cargar OWL a Python.
- [x] Determinar que formato necesita el repositorio para extraer la información (PDF o qué)
- [x] Donde se guardarían los resultados, en que base de datos
- [x] Investigar si hay forma de que la base de datos que se cree se fusione con la Ontología OMSSA o si hay que buscar como fusionarlas
- [x] Revisar documento nuevo
- [x] Si en el documento no está el enlace a Git debo pedirselo a Montero
- [x] Fix OntoCast bugs (custom model names, prefix handling, chunk sizes)
- [x] Fix OntoCast file upload for .md/.txt files (was failing on markdown)
- [x] Create RDF → CBR CSV converter script
- [x] Create OMSSA user instruction for OntoCast
- [x] Create pipeline integration script
- [x] Test converter with sample cases
- [x] Test end-to-end pipeline with real PDF
- [x] Create JSON-to-CBR converter (RDF-star workaround)
- [ ] Fix regex patterns in json_to_cbr.py
- [ ] Test CBR import with generated CSV
- [ ] Populate CBR database with extracted cases
- [ ] Create batch processing script for multiple papers