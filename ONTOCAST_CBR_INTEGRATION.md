# OntoCast → CBR Integration Guide

Complete pipeline for extracting predictive maintenance cases from academic papers using OntoCast and importing them into the OMSSA CBR system.

## Architecture

```
PDF Paper
    ↓
OntoCast (LLM extraction)
    ↓
RDF/Turtle (instance triples)
    ↓
ontocast_to_cbr.py (converter)
    ↓
CBR CSV (semicolon-separated)
    ↓
CSVtoOntologyExec.java (Eclipse)
    ↓
OPMADdatabase.owl (RDF/XML)
    ↓
myCBRSetting.java (reasoner)
    ↓
GUI2/GUI3 (CBR retrieval)
```

## Prerequisites

1. **Python 3.12+** with dependencies:
   ```bash
   pip install rdflib pandas
   ```

2. **OntoCast** configured with fixes (see ONTOCAST_SETUP.md)

3. **Java/Eclipse** with CBR project configured (see Code-Guide.md)

4. **OMSSA ontology** (`OPMAD.owl`) in `ontocast/ontologies/`

## Quick Start

### Method 1: Automated Pipeline

```bash
python scripts/run_ontocast_cbr_pipeline.py \
    --pdf example_paper.pdf \
    --output working/output \
    --start-id 439
```

This runs the complete workflow:
1. Starts OntoCast server
2. Processes PDF → RDF
3. Converts RDF → CSV
4. Copies to CBR data directory
5. Prints import instructions

### Method 2: Step-by-Step

#### Step 1: Configure OntoCast

Edit `ontocast/.env`:
```bash
# Key settings for CBR extraction
RENDER_MODE=facts
SKIP_ONTOLOGY_DEVELOPMENT=true
SKIP_FACTS_RENDERING=false
CURRENT_DOMAIN=http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD
```

#### Step 2: Start OntoCast Server

```bash
cd ontocast
ontocast --env-path .env --working-directory ./working --ontology-directory ./ontologies
```

#### Step 3: Process PDF

```bash
curl -X POST http://localhost:8999/process \
  -F "file=@example_paper.pdf" \
  -F "format=turtle" \
  --output working/extracted.ttl
```

#### Step 4: Convert to CBR CSV

```bash
python scripts/ontocast_to_cbr.py \
  --input ontocast/working/extracted.ttl \
  --output cbr_cases.csv \
  --start-id 439
```

#### Step 5: Import to CBR

1. Copy CSV to CBR data directory:
   ```bash
   cp cbr_cases.csv CBR-Ontology/CBRproject/data/
   ```

2. Update `AppConfiguration.java`:
   ```java
   data_path = "C:/.../CBR-Ontology/CBRproject/data/";
   csv = "cbr_cases.csv";
   ```

3. Prepare clean ontology:
   ```bash
   rm CBR-Ontology/CBRproject/data/OPMADdatabase.owl
   cp CBR-Ontology/CBRproject/data/OPMAD.owl \
      CBR-Ontology/CBRproject/data/OPMADdatabase.owl
   ```

4. Run in Eclipse:
   - `CSVtoOntologyExec.java`
   - `myCBRSetting.java` (takes minutes)
   - `GUI2.java` or `GUI3.java`

## Configuration

### OntoCast Settings for CBR

| Variable | Value | Description |
|----------|-------|-------------|
| `RENDER_MODE` | `ontology_and_facts` | Extract both (required for instance population) |
| `SKIP_ONTOLOGY_DEVELOPMENT` | `true` | Use OMSSA as-is (don't evolve schema) |
| `SKIP_FACTS_RENDERING` | `false` | Enable fact extraction (instance population) |
| `CURRENT_DOMAIN` | `http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD` | OMSSA namespace |

**Note**: `SKIP_ONTOLOGY_DEVELOPMENT=true` prevents OntoCast from modifying the OMSSA schema, but we still need `RENDER_MODE=ontology_and_facts` to extract instances that conform to the existing schema.

### Converter Options

```bash
python scripts/ontocast_to_cbr.py \
  --input extracted.ttl \      # Input RDF from OntoCast
  --output cbr_cases.csv \     # Output CSV file
  --start-id 439 \             # Starting case ID
  --append                     # Append to existing CSV
```

## Data Mapping

### OntoCast RDF → CBR CSV

| CBR Column | OMSSA Property | Example |
|------------|----------------|---------|
| Reference | auto-generated | `439` |
| Publication year | `has_publication_year` | `2019` |
| Task | `has_predictive_maintenance_function` | `Health modelling` |
| Case study | `has_part` (Maintainable_item) | `Slitting Machine` |
| Case study type | `rdf:type` of item | `Rotary machines` |
| Input for the model | `has_part` (record) | `Time series` |
| Input type | `is_carrier_of` | `Temperature, Vibration` |
| Model Type | `rdf:type` of model | `Data-driven` |
| Models | `function_uses_model` | `ARIMA` |
| Online/Off-line | `has_synchronization` | `Off-line` |
| Study title | `has_title` | Paper title |
| Publication identifier | `has_identifier` | DOI |

### SPARQL-safe Text Transformations

The CBR system uses special character encoding:

| Display | SPARQL | Example |
|---------|--------|---------|
| Space | `-` | `Health modelling` → `Health-modelling` |
| `-` | `--` | `Off-line` → `Off--line` |
| `/` | `---` | `Input/Output` → `Input---Output` |

## Troubleshooting

### Issue: No cases extracted

**Cause**: OntoCast produced ontology schema instead of instances

**Solution**:
- Check `RENDER_MODE=facts` in `.env`
- Verify OMSSA ontology loaded: `ls ontocast/ontologies/OPMAD.owl`
- Review OntoCast logs for errors

### Issue: Empty CSV columns

**Cause**: OntoCast used different property names than expected

**Solution**:
- Inspect RDF: `cat working/extracted.ttl | grep -i "case"`
- Update property mappings in `ontocast_to_cbr.py`
- Check OMSSA ontology defines expected properties

### Issue: CBR import fails

**Cause**: CSV format mismatch

**Solution**:
- Verify semicolon separator: `head -1 cbr_cases.csv | grep ";"`
- Check column count: 19 columns expected
- Ensure UTF-8 encoding: `file -i cbr_cases.csv`

### Issue: Duplicate IDs

**Cause**: start-id conflicts with existing cases

**Solution**:
- Check current max ID: `tail -5 DataBasefromOntology.csv`
- Use `--start-id` with next available number

## Testing

### Test Converter

```bash
# Use provided test cases
python scripts/ontocast_to_cbr.py \
  --input ontocast/working/test_cases.ttl \
  --output test_output.csv \
  --start-id 439

# Verify output
cat test_output.csv
```

### Validate RDF

```bash
# Check triples
python -c "
import rdflib
g = rdflib.Graph()
g.parse('ontocast/working/extracted.ttl', format='turtle')
print(f'Triples: {len(g)}')
print('Subjects:', set(s for s in g.subjects()))
"
```

## Files

| File | Purpose |
|------|---------|
| `ontocast/.env` | OntoCast configuration |
| `ontocast/prompts/omssa_user_instruction.txt` | Custom extraction prompt |
| `scripts/ontocast_to_cbr.py` | RDF → CSV converter |
| `scripts/run_ontocast_cbr_pipeline.py` | Full pipeline automation |
| `ontocast/working/test_cases.ttl` | Sample cases for testing |

## Next Steps

1. **Test with real papers**: Process 3-5 papers to validate extraction quality
2. **Tune prompts**: Refine `omssa_user_instruction.txt` based on results
3. **Build case database**: Scale to 100+ cases for effective CBR retrieval
4. **Evaluate accuracy**: Compare extracted vs. manual entry

## References

- [OntoCast Repository](https://github.com/growgraph/ontocast)
- [CBR Ontology](https://github.com/jjmj128/CBR-Ontology-For-Predictive-Maintenance)
- [OMSSA Paper](https://doi.org/10.1016/j.knosys.2021.107068)
