# Ontology Extraction for Predictive Maintenance CBR

This project extracts structured ontological knowledge from academic papers to populate a Case-Based Reasoning (CBR) database for predictive maintenance strategy selection.

---

### Workflow

1. **Input** 📄
   - Academic papers are provided in Markdown format
   - *Note: Paper retriever and PDF-to-Markdown converter components are already implemented and will be integrated in a future iteration*

2. **Ontology Extraction with OntoCast** 🔧
   - Processes Markdown documents using LLM-based extraction
   - Generates RDF/Turtle semantic triples (instances conforming to OMSSA schema)
   - **⚠️ Does NOT evolve OMSSA schema** (uses `--skip-ontology-critique`)

3. **RDF → CSV Conversion** 🔄
   - Converts OntoCast RDF output to CBR-compatible CSV format
   - Maps extracted instances to [expected CSV schema](#csv-schema-requirements)
   - Ensures column/row structure matches `CSVtoOntologyExec.java` requirements

4. **CBR Database Population** 🗄️
   - Run `CSVtoOntologyExec.java` to import CSV into OWL
   - Generates updated `OPMADdatabase.owl` with new cases
   - Uses [myCBR SDK](https://github.com/jjmj128/CBR-Ontology-For-Predictive-Maintenance) for case-based reasoning

---

## CSV Schema Requirements

The CBR system expects CSV files with **semicolon-separated** values in a specific format:

### Required Columns

| Col | Name | Maps to OMSSA Class | Example |
|-----|------|---------------------|---------|
| 0 | **Reference** | Case ID (numbered instance) | `1`, `2`, `3`... |
| 1 | **Publication Year** | `Publication year` | `2019`, `2020`... |
| 2 | **Task** | Subclass of `Predictive_maintenance_module_function` | `Health modelling`, `Remaining useful life estimation` |
| 3 | **Case study** | Subclass of `Maintainable item` | `Simulated jet-engines data`, `Lithium-ion battery` |
| 4 | **Case study type** | `item type` | `Rotary machines`, `Energy cells and batteries` |
| 5 | **Input for the model** | Subclass of `maintainable item record` | `Time series`, `Signals` |
| 7 | **Input type** | `Data_variable` (multiple values allowed) | `Temperature, Fluid Pressure, Voltage` |
| 10 | **Model Type** | `Model type` (multiple values allowed) | `Data-driven`, `Physics-based` |
| 11 | **Models** | Subclass of `Predictive maintenance model` (multiple) | `Logistic regression, LSTM` |
| 12 | **Online/Off-line** | `Module synchronization` | `Online`, `Off-line` |
| 17 | **Study title** | `Article title` + `Article` | Paper title string |
| 18 | **Publication identifier** | `Article identifier` | DOI or URL |

### CSV Format Example

```csv
Reference;Publication Year;Task;Case study;Case study type;Input for the model;...;Study title;Publication identifier
1;2019;Health modelling;Simulated jet-engines data;Rotary machines;Time series;...;Aircraft engine degradation...;doi.org/10.1016/j.ast.2018.09.044
2;2019;Remaining useful life estimation;Lithium-ion battery;Energy cells...;Time series;...;A new hybrid method...;doi.org/10.1016/j.apenergy.2017.09.106
```

### Reference Implementation

See [`CSVtoOntologyExec.java`](CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/src/User/CSVtoOntologyExec.java) for complete column-to-ontology mapping.

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

### ⚠️ Critical Architecture Note

The CBR system uses **CSV import via Java/Eclipse**, not direct OWL merging:

```
Markdown Papers
      ↓
OntoCast (RDF extraction)
      ↓
RDF → CSV Converter (to be implemented)
      ↓
CSV file (semicolon-separated, 19 columns)
      ↓
CSVtoOntologyExec.java (requires Eclipse + Java 8+)
      ↓
OPMADdatabase.owl (RDF/XML syntax - NOT Turtle!)
      ↓
myCBRSetting.java (generates .prj file)
      ↓
GUI2/GUI3 (CBR retrieval)
```

### 🚨 Critical Integration Problems Discovered

#### Problem 1: RDF/XML Required (NOT Turtle!)

| Format | Supported? | Note |
|--------|-----------|------|
| RDF/XML | ✅ **YES** | **Required format** for OWL files |
| Turtle (.ttl) | ❌ **NO** | OntoCast default - **must convert** |
| OWL/XML | ❌ **NO** | Not supported by CBR tool |

**OntoCast outputs Turtle** → **Must convert to RDF/XML** before CBR import.

#### Problem 2: Complex String Transformations

The CBR system requires specific text transformations:

| Character | In SPARQL | In CSV Output |
|-----------|-----------|---------------|
| Space | `-` | ` ` (space) |
| `-` | `--` | `-` |
| `/` | `---` | `/` |
| `_` | `_` | ` ` (space) |

**Example:**
- OntoCast output: `LSTM_(Long-Short_Term_Memory_Neural_Network)`
- SPARQL query: `LSTM_(Long--Short_Term_Memory_Neural_Network)`
- CSV display: `LSTM (Long-Short Term Memory Neural Network)`

#### Problem 3: Order-Dependent Columns

Some columns have **order dependencies** (must maintain 1:1 mapping):

| Column Pair | Relationship |
|-------------|--------------|
| **Model Type ↔ Models** | Each Model Type describes corresponding Model |
| **Performance indicator ↔ Performance** | Each indicator has one performance value |

If both columns have multiple values, they must have **same number of elements** in same order.

#### Problem 4: Input Type Formatting

The **Input type** column (col 7) has strict requirements:
- Values must start with **capital letters** (e.g., `Temperature`, not `temperature`)
- Separated by `, ` (comma + space)
- Supports misspelling up to 3 characters (Levenshtein distance)

**Correct:** `Temperature, Fluid Pressure, Spinning speed`
**Incorrect:** `temperature, fluid pressure` ❌

#### Problem 5: Missing Columns in CSV

The CSV must have **19 columns** (0-18). Some columns in the data file are **not imported** into the ontology:

| Column | Name | Imported? | Note |
|--------|------|-----------|------|
| 6 | Number of input variables | ❌ **NO** | Calculated field |
| 8 | Data Pre-processing | ❌ **NO** | Not in ontology |
| 9 | Model Approach | ❌ **NO** | Not in ontology |
| 13-16 | Performance metrics | ⚠️ **PARTIAL** | Only some fields |

The `OntologytoCSVExec` cannot fully reconstruct the original CSV because some columns are **not stored** in the ontology.

#### Problem 6: Java/Eclipse Dependency

The CBR tool **requires**:
- Eclipse IDE with Java 8+
- Multiple JAR dependencies (OWL API 5.1.9, HermiT reasoner, myCBR SDK, Jena)
- `AppConfiguration.java` must be edited to set file paths
- `external-libs/` folder with all dependencies

**Cannot run standalone** - must use Eclipse project structure.

#### Problem 7: Reference Index Management

- Current max ID: **438** (from existing cases)
- New cases must start from **439**
- IDs must be **sequential integers** (no gaps)
- Used for URI generation: `{ClassName}{ReferenceID}`

#### Problem 8: Clean Ontology Required

Before each import:
1. **Delete** existing `OPMADdatabase.owl` (with instances)
2. **Copy** clean `OPMAD.owl` (no instances) to new file
3. **Run** `CSVtoOntologyExec` to populate
4. **Run** `myCBRSetting` to update `.prj` file

**Cannot append** - must regenerate entire database.

### Integration Steps (Revised)

#### 1. Configure OntoCast

```bash
# .env file
SKIP_ONTOLOGY_DEVELOPMENT=true
SKIP_FACTS_RENDERING=false
```

Run OntoCast on markdown papers → produces `extracted.ttl`

#### 2. Convert RDF → CSV (Complex Transformation)

**Implementation needed**: `scripts/rdf_to_cbr_csv.py`

```python
#!/usr/bin/env python3
"""
Convert OntoCast RDF to CBR-compatible CSV.
Handles text transformations, column ordering, and format requirements.
"""

import rdflib
import pandas as pd
import re
from rdflib import Namespace

OMSSA = Namespace("http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD#")

def to_sparql_safe(text):
    """Convert to SPARQL-safe format"""
    if not text:
        return ""
    text = text.replace(" ", "-")      # space → -
    text = text.replace("-", "--")     # - → --
    text = text.replace("/", "---")    # / → ---
    return text

def to_display_format(text):
    """Convert underscores to spaces for display"""
    if not text:
        return ""
    return text.replace("_", " ")

def format_input_type(values):
    """Format Input type: capitalize each word, comma+space separated"""
    if not values:
        return ""
    formatted = []
    for val in values:
        # Capitalize each word
        val = val.title()
        formatted.append(val)
    return ", ".join(formatted)

def rdf_to_cbr_csv(rdf_file, csv_file, next_id=439):
    """
    Convert OntoCast RDF to CBR CSV format.
    
    Critical: Must maintain order-dependent column pairs!
    """
    g = rdflib.Graph()
    g.parse(rdf_file, format="turtle")
    
    cases = []
    
    # Query each case with all relationships
    query = """
    SELECT ?case ?ref ?year ?task ?study ?studyType ?inputModel ?inputType 
           ?modelType ?models ?onlineOffline ?title ?doi
    WHERE {
        ?case rdf:type def:Predictive_maintenance_case .
        OPTIONAL { ?case def:has_text_value ?ref }
        OPTIONAL { ?case def:has_publication_year ?year }
        OPTIONAL { ?case def:has_predictive_maintenance_function ?task }
        OPTIONAL { ?case def:has_part ?study }
        OPTIONAL { ?study rdf:type ?studyType }
        OPTIONAL { ?case def:has_part ?inputModel }
        OPTIONAL { ?inputModel rdf:type ?inputModelType }
        OPTIONAL { ?inputModel def:is_carrier_of ?inputType }
        OPTIONAL { ?case def:function_uses_model ?models }
        OPTIONAL { ?models rdf:type ?modelType }
        OPTIONAL { ?case def:has_synchronization ?onlineOffline }
        OPTIONAL { ?case def:has_title ?title }
        OPTIONAL { ?case def:has_identifier ?doi }
    }
    """
    
    results = g.query(query, initNs={"def": OMSSA, "rdf": rdflib.RDF})
    
    for row in results:
        case_data = {
            'Reference': next_id,
            'Publication Year': row.year or '',
            'Task': to_display_format(row.task),
            'Case study': to_display_format(row.study),
            'Case study type': to_display_format(row.studyType),
            'Input for the model': to_display_format(row.inputModel),
            'Input type': format_input_type(row.inputType),
            'Model Type': to_display_format(row.modelType),
            'Models': to_display_format(row.models),
            'Online/Off-line': to_display_format(row.onlineOffline),
            'Study title': row.title or '',
            'Publication identifier': row.doi or '',
            # Fill remaining required columns with empty values
            'Number of input variables': '',  # Not imported
            'Data Pre-processing': '',         # Not imported
            'Model Approach': '',              # Not imported
            'Number of failure modes': '',
            'Performance indicator': '',
            'Performance': '',
            'Complementary notes': '',
        }
        cases.append(case_data)
        next_id += 1
    
    # Create DataFrame with exact column order
    columns = [
        'Reference', 'Publication Year', 'Task', 'Case study', 'Case study type',
        'Input for the model', 'Number of input variables', 'Input type',
        'Data Pre-processing', 'Model Approach', 'Model Type', 'Models',
        'Online/Off-line', 'Number of failure modes', 'Performance indicator',
        'Performance', 'Complementary notes', 'Study title', 'Publication identifier'
    ]
    
    df = pd.DataFrame(cases, columns=columns)
    
    # CRITICAL: Save with semicolon separator!
    df.to_csv(csv_file, sep=';', index=False, encoding='utf-8')
    
    return len(cases)

if __name__ == "__main__":
    count = rdf_to_cbr_csv("extracted.ttl", "new_cases.csv", next_id=439)
    print(f"Converted {count} cases to CBR CSV")
```

#### 3. Import into CBR (Java/Eclipse Required)

**Preparation:**
```bash
# 1. Copy CSV to CBR data folder
cp new_cases.csv CBR-Ontology/CBRproject/data/

# 2. Edit AppConfiguration.java
data_path = "/path/to/CBR-Ontology/CBRproject/data/"
csv = "new_cases.csv"
ont_file_name = "OPMADdatabase_new.owl"
base_ont_file_name = "OPMAD.owl"  # Clean ontology
```

**Execution:**
```bash
# In Eclipse:
# 1. Delete old OPMADdatabase.owl (if exists)
# 2. Run CSVtoOntologyExec.java
# 3. Run myCBRSetting.java (takes minutes - runs HermiT reasoner)
# 4. Run GUI2.java or GUI3.java for queries
```

#### 4. Validation Checklist

Before using in CBR:

- [ ] CSV has **19 columns** (0-18)
- [ ] Separator is **semicolon** (`;`)
- [ ] Reference IDs start from **439** (sequential)
- [ ] Input type values are **capitalized** (e.g., `Temperature`)
- [ ] Order-dependent columns have **matching element counts**
- [ ] Text transformations applied (spaces→dashes in URIs)
- [ ] OWL file is **RDF/XML** format (not Turtle)
- [ ] HermiT reasoner runs without errors
- [ ] `.prj` file is regenerated by `myCBRSetting`

### Safe vs. Unsafe Operations

| Operation | Safe? | Notes |
|-----------|-------|-------|
| OntoCast extraction | ✅ **SAFE** | Use `--skip-ontology-critique` |
| RDF → CSV conversion | ⚠️ **COMPLEX** | Must handle text transformations |
| Direct Turtle import | ❌ **UNSAFE** | CBR requires RDF/XML |
| Append to existing OWL | ❌ **UNSAFE** | Must regenerate from clean |
| Skip CSV step | ❌ **UNSAFE** | CSV is primary input format |
| Manual OWL edit | ⚠️ **RISKY** | May break consistency |

---

## CBR Repository Setup

### Encoding Fixes

The CBR Java source files in `CBR-Ontology-For-Predictive-Maintenance/` use ISO-8859-1 encoding which causes compilation errors on modern systems. The following fixes were applied:

#### Files Converted to UTF-8
- `CBR-Ontology/CBRproject/src/OntologyTools/CSVtoOntology.java`
- `CBR-Ontology/CBRproject/src/OntologyTools/OntologytoCSV.java`
- `CBR-Ontology/CBRproject/src/User/CSVtoOntologyExec.java`
- `CBR-Ontology/CBRproject/src/User/GeneralMethods.java`

#### Configuration Updated
- `CBR-Ontology/CBRproject/src/User/AppConfiguration.java` - Updated `data_path` to local directory

#### Fix Script

```bash
# Convert ISO-8859-1 files to UTF-8
cd CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/src
for file in $(find . -name "*.java" -exec file {} \; | grep "ISO-8859" | cut -d: -f1); do
  iconv -f ISO-8859-1 -t UTF-8 "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
done

# Update data_path in AppConfiguration.java
# Edit: CBR-Ontology/CBRproject/src/User/AppConfiguration.java
# Change: data_path = "C:YOUR-DIRECTORY\\..."
# To: data_path = "C:\\Users\\...\\CBR-Ontology\\CBRproject\\data\\"
```

#### Git Setup

```bash
# Add .gitignore to exclude compiled files
cat > CBR-Ontology-For-Predictive-Maintenance/.gitignore << 'EOF'
# Compiled Java files
*.class

# Eclipse metadata
.metadata/

# Build directories
bin/

# IDE files
.classpath
.project
.settings/
EOF
```
