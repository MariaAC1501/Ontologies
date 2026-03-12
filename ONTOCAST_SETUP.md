# OntoCast Setup Guide for Predictive Maintenance CBR

## Overview
This guide sets up OntoCast to extract structured knowledge from academic papers and prepare it for import into the CBR system.

## Prerequisites
- Python 3.12+ (Python 3.13 may work but is not officially supported)
- OpenAI API key (or Ollama for local LLMs)
- Java/Eclipse (for CBR import - see Code-Guide.md)

## Installation

### 1. Clone OntoCast (already done)
```bash
git clone https://github.com/growgraph/ontocast.git
cd ontocast
```

### 2. Install OntoCast
```bash
pip install -e .
# Or with document processing support:
pip install -e ".[doc-processing]"
```

### 3. Configure Environment

Edit `ontocast/.env`:

```bash
# For OpenAI (recommended for testing)
LLM_PROVIDER=openai
LLM_MODEL_NAME=gpt-4o-mini
LLM_API_KEY=sk-your-actual-api-key-here
LLM_TEMPERATURE=0.0

# For Ollama (local, free, but requires setup)
# LLM_PROVIDER=ollama
# LLM_MODEL_NAME=llama3.1
# LLM_BASE_URL=http://localhost:11434

# Domain for URI generation
CURRENT_DOMAIN=http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD

# Path Configuration
ONTOCAST_WORKING_DIRECTORY=./working
ONTOCAST_ONTOLOGY_DIRECTORY=./ontologies
ONTOCAST_CACHE_DIR=./cache

# Skip ontology evolution (instance extraction only)
SKIP_ONTOLOGY_DEVELOPMENT=true
RENDER_MODE=ontology

# Disable web search (not needed for academic papers)
WEB_SEARCH_ENABLED=false
```

### 4. Copy OMSSA Ontology
```bash
cp ../CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/OPMAD.owl ./ontologies/
```

### 5. Prepare Input Document
```bash
cp ../example_paper.md ./working/
```

## Running OntoCast

### Method 1: Server Mode (Recommended)

**Terminal 1 - Start Server:**
```bash
cd ontocast
ontocast --env-path .env --working-directory ./working --ontology-directory ./ontologies
```

**Terminal 2 - Process Document:**
```bash
# Process markdown file
curl -X POST http://localhost:8999/process \
  -F "file=@working/example_paper.md" \
  -F "format=turtle" \
  --output working/extracted.ttl

# Or process PDF
curl -X POST http://localhost:8999/process \
  -F "file=@paper.pdf" \
  --output working/extracted.ttl
```

### Method 2: Python API

```python
from ontocast.core import OntoCast

app = OntoCast()
result = app.process_document(
    file_path="working/example_paper.md",
    output_format="turtle"
)
print(f"Extracted {result['triple_count']} triples")
```

### Method 3: CLI Batch Processing

```bash
cd ontocast
python -m ontocast.cli.batch_process \
  --input-dir ./working/papers \
  --output-dir ./working/extracted \
  --format turtle
```

## Output Format

OntoCast generates **RDF/Turtle** (`.ttl`) files. Example output:

```turtle
@prefix def: <http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

def:Case439 rdf:type def:Predictive_maintenance_case ;
    def:has_text_value "439" ;
    def:has_publication_year "2023" ;
    def:has_predictive_maintenance_function def:Health_modelling ;
    def:has_part def:Slitting_Machine_439 ;
    def:has_synchronization def:Online_439 .
```

## Next Steps: Convert to CBR CSV

After extracting RDF, you need to convert it to CBR-compatible CSV:

```bash
# Run the converter (to be implemented)
python scripts/rdf_to_cbr_csv.py \
  --input working/extracted.ttl \
  --output working/cbr_input.csv \
  --start-id 439
```

Then import to CBR:
```bash
# Copy CSV to CBR data folder
cp working/cbr_input.csv ../CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/

# Run in Eclipse (see Code-Guide.md)
# 1. CSVtoOntologyExec.java
# 2. myCBRSetting.java
# 3. GUI2.java or GUI3.java
```

## Troubleshooting

### Issue: "LLM_API_KEY not set"
**Solution:** Set your OpenAI API key in `ontocast/.env`

### Issue: "Module not found"
**Solution:** Make sure you installed with `pip install -e .`

### Issue: "Ontology file not found"
**Solution:** Copy `OPMAD.owl` to `ontocast/ontologies/`

### Issue: Server won't start
**Solution:** Check if port 8999 is in use: `lsof -i :8999` (Unix) or `netstat -ano | findstr 8999` (Windows)

## Important Notes

1. **RDF Format**: OntoCast outputs Turtle format, but CBR requires RDF/XML
2. **Conversion Required**: You MUST convert RDF → CSV before CBR import
3. **Instance IDs**: New cases must start from ID 439 (current max is 438)
4. **No Direct OWL Import**: CBR only accepts CSV input via `CSVtoOntologyExec.java`

## Architecture Flow

```
example_paper.md
      ↓
OntoCast (LLM extraction)
      ↓
extracted.ttl (RDF/Turtle)
      ↓
rdf_to_cbr_csv.py (conversion)
      ↓
cbr_input.csv (semicolon-separated)
      ↓
CSVtoOntologyExec.java
      ↓
OPMADdatabase.owl (RDF/XML)
      ↓
myCBRSetting.java (generates .prj)
      ↓
GUI2/GUI3 (CBR retrieval)
```
