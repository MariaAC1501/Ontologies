# Ontology Extraction for Predictive Maintenance CBR

This project extracts structured ontological knowledge from academic papers to populate a Case-Based Reasoning (CBR) database for predictive maintenance strategy selection.

---

### Workflow

1. **Input** 📄
   - Academic papers are provided in Markdown format
   - *Note: Paper retriever and PDF-to-Markdown converter components are already implemented and will be integrated in a future iteration*

2. **Ontology Extraction with OntoCast** 🔧
   - Processes Markdown documents using LLM-based extraction
   - Generates RDF/Turtle semantic triples
   - Co-evolves ontology with extracted facts
   - Supports version control and incremental updates

3. **CBR Database Population** 🗄️
   - Extracted triples populate the OMSSA ontology cases
   - Integrates with [CBR-Ontology-For-Predictive-Maintenance](https://github.com/jjmj128/CBR-Ontology-For-Predictive-Maintenance)
   - Enables case-based reasoning for maintenance strategy selection

---

## Why OntoCast?

After evaluating [OntoGPT](https://github.com/monarch-initiative/ontogpt/) and [OntoCast](https://github.com/growgraph/ontocast), we selected **OntoCast** for the following reasons:

| Criterion | OntoCast Advantage |
|-----------|-------------------|
| **RDF/OWL Native** | Built specifically for RDF/Turtle output - directly compatible with OMSSA OWL ontologies |
| **Triple Store Integration** | Native support for Fuseki and Neo4j - matches our semantic web stack |
| **SPARQL-based Updates** | GraphUpdate system uses SPARQL operations - efficient for incremental case updates |
| **Ontology Co-evolution** | Extracts AND refines ontologies simultaneously - perfect for extending OMSSA with new cases |
| **Token Efficiency** | GraphUpdate system reduces LLM token usage by 80-95% |
| **Versioning** | Automatic semantic versioning - critical for tracking ontology evolution |
| **Instance Population** | Better suited for populating CBR cases into existing ontologies |

---

## Base Ontology

We use the **Ontology Model for Maintenance Strategy Selection and Assessment (OMSSA)** defined in [CBR-Ontology-For-Predictive-Maintenance](https://github.com/jjmj128/CBR-Ontology-For-Predictive-Maintenance)

The OMSSA ontology provides:
- Structured representation of maintenance strategies
- Failure modes and effects
- Equipment configurations
- Case structure for CBR retrieval

---

## OntoCast + OMSSA/CBR Integration Guide

### Potential Overlap Risks

There are **architectural incompatibilities** that must be addressed:

| Risk | Description | Severity |
|------|-------------|----------|
| **Ontology Evolution** | OntoCast co-evolves ontology; OMSSA/CBR requires stable schema | 🔴 **HIGH** |
| **Instance URI Conflicts** | Different naming conventions may cause ID collisions | 🟡 **MEDIUM** |
| **Storage Mismatch** | OntoCast uses triple store; CBR uses OWL files | 🟡 **MEDIUM** |
| **Schema Modifications** | Auto-generated classes/properties may break CBR | 🔴 **HIGH** |

### Integration Steps

#### 1. Configure OntoCast in Read-Only Mode

Create `.env` file:

```bash
# LLM Configuration
LLM_PROVIDER=openai
LLM_API_KEY=your-api-key-here
LLM_MODEL_NAME=gpt-5.4
LLM_TEMPERATURE=0.1

# Paths
ONTOCAST_WORKING_DIRECTORY=./data/working
ONTOCAST_ONTOLOGY_DIRECTORY=./data/ontologies

# CRITICAL: Skip ontology evolution to preserve OMSSA schema
SKIP_ONTOLOGY_DEVELOPMENT=true
ONTOLOGY_MAX_TRIPLES=10000

# Export to files instead of triple store (avoids storage mismatch)
# Leave FUSEKI_URI and NEO4J_URI unset to use filesystem mode
```

#### 2. Import OMSSA as Reference Ontology

Place OMSSA files in `ONTOCAST_ONTOLOGY_DIRECTORY`, preferrably with a simlink:

```
data/ontologies/
├── OPMAD.owl              # Schema (248 classes/properties)
├── OPMADdatabase.owl      # Existing cases (~4,378 instances)
├── CCOmerged.owl
└── [other imports]
```

#### 3. Run OntoCast with Safe Flags

```bash
# Process papers WITHOUT modifying OMSSA schema
ontocast \
    --env-path .env \
    --working-directory ./data/working \
    --ontology-directory ./data/ontologies \
    --skip-ontology-critique \
    --head-chunks 10
```

**Key flags:**
- `--skip-ontology-critique`: Prevents OntoCast from modifying OMSSA classes/properties
- `--head-chunks N`: Limits processing for testing

#### 4. Post-Processing: Instance URI Standardization

OntoCast may generate URIs like:
- ❌ `http://ontocast.org/maintenance/lstm_network`

OMSSA expects:
- ✅ `http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD#LSTM_(Long-Short_Term_Memory_Neural_Network)184`

**Conversion script example**:

```python
# scripts/standardize_uris.py
import rdflib
from rdflib import Namespace

OMSSA = Namespace("http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD#")

# Map OntoCast instances to OMSSA naming convention
# - Use OMSSA class names
# - Append sequential numbers (starting from max existing + 1)
# - Maintain rdf:type references to OMSSA classes only
```

#### 5. Merge Extracted Instances into OPMADdatabase.owl

```python
# scripts/merge_cases.py
import rdflib

# Load existing OMSSA database
g = rdflib.Graph()
g.parse("data/ontologies/OPMADdatabase.owl", format="xml")

# Load OntoCast extracted instances
extracted = rdflib.Graph()
extracted.parse("data/working/extracted_cases.ttl", format="turtle")

# Merge (append only, no schema changes)
g += extracted

# Save merged database
g.serialize("data/ontologies/OPMADdatabase_extended.owl", format="xml")
```

### Safe vs. Unsafe Operations

| Operation | Safe? | Reason |
|-----------|-------|--------|
| Extract instances (NamedIndividuals) | ✅ **SAFE** | Adds cases to database |
| Use existing OMSSA classes for typing | ✅ **SAFE** | Respects schema |
| Create new classes | ❌ **UNSAFE** | Breaks CBR schema |
| Create new properties | ❌ **UNSAFE** | Breaks CBR reasoning |
| Modify existing class definitions | ❌ **UNSAFE** | Corrupts ontology |
| Auto-evolve ontology | ❌ **UNSAFE** | Use `--skip-ontology-critique` |
