# End-to-End Test Results

## Summary

Successfully tested the OntoCast → CBR integration pipeline.

## Test Execution

### Step 1: Start OntoCast Server
```bash
ontocast --env-file .env
# Running on port 9000
```

### Step 2: Process Document
```bash
curl -X POST http://localhost:9000/process \
  -H "Content-Type: application/json" \
  -d '{"text": "...paper text..."}' \
  --output extracted.json
```

**Result:** ✅ Success
- Chunks processed: 21 (for full paper)
- Facts extracted: 202KB of RDF triples
- Ontology: 177KB of schema

### Step 3: Convert to CBR CSV
```bash
python scripts/json_to_cbr.py \
  --input extracted.json \
  --output cbr_cases.csv \
  --start-id 439
```

**Result:** ✅ Success
- Extracted: Reference 439
- Publication year: 2021 (should be 2019 - needs regex fix)
- Case study: SlittingMachine
- Models: ARIMA
- Online/Off-line: Off-line

## Output Format

```csv
Reference;Publication year;Task;Case study;...
439;2021;;SlittingMachine;;Time series;;...;ARIMA;Off-line;...;doi.org/10.1109/ICCCNT45670.2019.8944506
```

## Key Findings

### What Works
1. ✅ OntoCast processes JSON text input correctly
2. ✅ Server runs with custom model (gpt-5-mini)
3. ✅ Extraction produces RDF facts
4. ✅ CBR CSV converter runs successfully
5. ✅ Semicolon-separated format correct

### What Needs Improvement
1. **Year extraction**: Regex picks up wrong year (2021 vs 2019)
2. **Case study formatting**: "SlittingMachine" should be "Slitting Machine"
3. **Task extraction**: Not finding "Health modelling"
4. **Sensor variables**: Regex patterns capturing bracket notation
5. **RDF parsing**: OntoCast outputs RDF-star which rdflib can't parse

### Critical Discovery

**JSON input works, file upload doesn't.**

Sending text as JSON payload:
```bash
-H "Content-Type: application/json" -d '{"text": "..."}'
```

Works correctly and produces chunks.

File upload with `-F "file=@..."`:
- Markdown/text: 0 chunks (parsing issue)
- PDF: Error (document converter not available)

## Recommended Workflow

1. Convert PDFs to text/markdown (external tool)
2. Send text via JSON API
3. Extract facts from JSON response
4. Transform to CBR CSV using custom script
5. Import to CBR system via Java/Eclipse

## Next Steps

1. Fix regex patterns in `json_to_cbr.py`
2. Test with multiple papers
3. Validate CSV imports correctly into CBR
4. Create batch processing script
