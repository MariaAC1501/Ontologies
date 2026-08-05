# Gold extraction evaluation harness

Herramientas reproducibles (solo stdlib de Python) para RQ1/RQ3: muestrear un corpus dorado desde `extraction_manifest.csv` y evaluar predicciones estructuradas contra anotación experta.

## 1. Preparar muestra dorada

```bash
python paper/experiments/prepare_gold_sample.py \
  --manifest paper/supplement/protocol/extraction_manifest.csv \
  --n 25 \
  --seed 20260730 \
  --output-dir paper/experiments/gold_sample \
  --require-pdf-exists
```

Por defecto estratifica usando aliases disponibles para `task`, `model` y `linkage` (por ejemplo `extracted_task`, `actual_model`, `linkage_method`). Para fijarlos manualmente:

```bash
python paper/experiments/prepare_gold_sample.py --n 25 --seed 1 \
  --output-dir paper/experiments/gold_sample \
  --strata-cols extracted_task,actual_model,linkage_method
```

Salidas:

- `sample_manifest.csv`: filas muestreadas del manifest original.
- `gold_template.jsonl`: una línea por fila, con `gold` vacío para completar por expertos.

## Formato JSONL

Gold anotado:

```json
{"record_id":"paper-0001","gold":{"task":["fault detection"],"model":["cnn"],"linkage":"title match"}}
```

Predicciones:

```json
{"record_id":"paper-0001","prediction":{"task":"Fault Detection","model":["CNN","LSTM"],"linkage":"title-match"}}
```

Los valores de campo pueden ser escalares o listas. La comparación normaliza minúsculas, espacios y puntuación, y compara sets por campo.

## 2. Evaluar predicciones

```bash
python paper/experiments/evaluate_extraction.py \
  --gold paper/experiments/gold_sample/gold_annotated.jsonl \
  --predictions paper/experiments/predictions.jsonl \
  --output-dir paper/experiments/eval \
  --fields task,model,linkage
```

Salidas:

- `metrics.json`: métricas micro agregadas (`tp`, `fp`, `fn`, `precision`, `recall`, `f1`, `exact_match`, `hallucination_rate`).
- `field_metrics.csv`: las mismas métricas por campo.

## 3. Predicciones desde facts TTL existentes

Genera `predictions.jsonl` determinista, sin llamadas a APIs, usando la columna `facts_file` del manifest:

```bash
python paper/experiments/predictions_from_facts.py \
  --manifest paper/experiments/gold_sample/sample_manifest.csv \
  --output paper/experiments/predictions.jsonl \
  --ontology pipeline/seed_ontology/opmad_seed.ttl
```

Para un manifest que no use `corpus_id`/`record_id` como identificador:

```bash
python paper/experiments/predictions_from_facts.py \
  --manifest paper/supplement/protocol/extraction_manifest.csv \
  --output paper/experiments/predictions_from_extraction_manifest.jsonl \
  --record-id-column corpus_id
```

Use `--strict` si cualquier error de carga/conversión debe abortar; sin `--strict`, los errores quedan en `metadata.errors` por registro.

## 4. Planificar matriz experimental

Crea `matrix.csv` y `README_protocol.md` para las condiciones `opmad_fixed`, `generic_json`, `llm_schema`, `llm_ontology`; scopes `abstract`, `sections`, `fulltext`; y modelos indicados. El script solo planifica comandos/salidas y no llama LLMs:

```bash
python paper/experiments/build_experiment_matrix.py \
  --sample-manifest paper/experiments/gold_sample/sample_manifest.csv \
  --models gpt-5-mini,gpt-5.1-mini \
  --output-dir paper/experiments/matrix
```

## 5. Baselines LLM no-OntoCast (RQ1/RQ2/RQ3/RQ4)

Construir paquetes de evidencia desde la muestra dorada y el CSV Scopus incluido:

```bash
python paper/experiments/build_evidence_packages.py \
  --sample-manifest paper/experiments/gold_sample/sample_manifest.csv \
  --scopus-csv "extraction_papers/scopus_export_May 26-2026_included.csv" \
  --scope abstract \
  --output paper/experiments/llm_baselines/abstract/evidence.jsonl
```

Para el scope con metadatos de PDF/facts:

```bash
python paper/experiments/build_evidence_packages.py \
  --sample-manifest paper/experiments/gold_sample/sample_manifest.csv \
  --scopus-csv "extraction_papers/scopus_export_May 26-2026_included.csv" \
  --scope metadata \
  --output paper/experiments/llm_baselines/metadata/evidence.jsonl
```

Para RQ3 con texto completo local (sin APIs), preconvertir PDFs a `.txt`, `.md` o `.json` y nombrarlos como `corpus_id.ext` o con el stem del PDF (`pdf_file`). `fulltext` incluye los primeros `--max-fulltext-chars`; `sections` extrae bloques/líneas de métodos, resultados, discusión, modelos o datos:

```bash
python paper/experiments/build_evidence_packages.py \
  --sample-manifest paper/experiments/gold_sample/sample_manifest.csv \
  --scopus-csv "extraction_papers/scopus_export_May 26-2026_included.csv" \
  --scope fulltext \
  --text-dir paper/experiments/fulltext_converted \
  --max-fulltext-chars 30000 \
  --output paper/experiments/llm_baselines/fulltext/evidence.jsonl
```

### RQ2: generar schema u ontología con LLM

Desde `evidence.jsonl`, generar primero el artefacto LLM que guiará la condición `llm_schema` o `llm_ontology`. El `--dry-run` no llama APIs: escribe `prompt.md`, `metadata.json` y una plantilla `generated_schema.json` o `generated_ontology.ttl`.

```bash
python paper/experiments/generate_llm_schema_or_ontology.py \
  --evidence paper/experiments/llm_baselines/abstract/evidence.jsonl \
  --artifact schema_json \
  --dry-run \
  --max-records 5 \
  --output-dir paper/experiments/llm_baselines/rq2_schema

python paper/experiments/generate_llm_schema_or_ontology.py \
  --evidence paper/experiments/llm_baselines/abstract/evidence.jsonl \
  --artifact ontology_ttl \
  --dry-run \
  --max-records 5 \
  --output-dir paper/experiments/llm_baselines/rq2_ontology
```

Luego ejecutar extracción contra el schema u ontología generados. Dry-run reproducible, sin API, generando `prompts/*.md` y predicciones vacías (`metadata.status="dry-run"`):

```bash
python paper/experiments/run_llm_json_extraction.py \
  --evidence paper/experiments/llm_baselines/abstract/evidence.jsonl \
  --condition llm_schema \
  --schema-context paper/experiments/llm_baselines/rq2_schema/generated_schema.json \
  --model dry-run-model \
  --dry-run \
  --output paper/experiments/llm_baselines/abstract/llm_schema/predictions.jsonl

python paper/experiments/run_llm_json_extraction.py \
  --evidence paper/experiments/llm_baselines/abstract/evidence.jsonl \
  --condition llm_ontology \
  --ontology paper/experiments/llm_baselines/rq2_ontology/generated_ontology.ttl \
  --model dry-run-model \
  --dry-run \
  --output paper/experiments/llm_baselines/abstract/llm_ontology/predictions.jsonl
```

Ejecución real (no usar en tests) vía Chat Completions compatible con OpenAI:

```bash
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_API_KEY="..."
python paper/experiments/generate_llm_schema_or_ontology.py \
  --evidence paper/experiments/llm_baselines/abstract/evidence.jsonl \
  --artifact schema_json \
  --model gpt-5-mini \
  --temperature 0 \
  --output-dir paper/experiments/llm_baselines/rq2_schema

python paper/experiments/run_llm_json_extraction.py \
  --evidence paper/experiments/llm_baselines/abstract/evidence.jsonl \
  --condition llm_schema \
  --schema-context paper/experiments/llm_baselines/rq2_schema/generated_schema.json \
  --model gpt-5-mini \
  --temperature 0 \
  --output paper/experiments/llm_baselines/abstract/llm_schema/predictions.jsonl
```

Para `llm_ontology`, generar `--artifact ontology_ttl` y pasar `--ontology .../generated_ontology.ttl`. Use `--max-records N` para pruebas acotadas.

## 6. RQ5: preparar consultas CBR downstream

A partir de `predictions.jsonl` con `record_id` y los 19 campos canónicos en `prediction`, generar solo los insumos reproducibles para HeadlessCBR/GUI3 (sin ejecutar Java ni MMR):

```bash
python paper/experiments/predictions_to_cbr_queries.py \
  --predictions paper/experiments/predictions.jsonl \
  --output-dir paper/experiments/rq5_cbr \
  --query-year 2026 \
  --number-of-cases 15
```

Salidas:

- `query_batch_input.csv`: CSV con `;` compatible con `HeadlessCBR query-batch`.
- `query_metadata.csv`: `record_id`, notas de normalización, número de campos activos y errores; sus filas están en el mismo orden que las consultas CBR.

Después, si se desea ejecutar el retrieval CBR, pasar rutas absolutas al wrapper (HeadlessCBR resuelve rutas relativas al directorio de datos):

```bash
mkdir -p paper/experiments/rq5_cbr/cbr_results
scripts/run_cbr.sh \
  --data-dir "$(pwd)/external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data" \
  query-batch \
  "$(pwd)/paper/experiments/rq5_cbr/query_batch_input.csv" \
  "$(pwd)/paper/experiments/rq5_cbr/cbr_results/query_"
```

La primera fila de datos de `query_metadata.csv` corresponde a `query_1.csv`, la segunda a `query_2.csv`, etc.

## Smoke test

Bash/Git Bash:

```bash
python paper/experiments/prepare_gold_sample.py --n 3 --seed 7 \
  --output-dir paper/experiments/_smoke_gold --require-pdf-exists

python - <<'PY'
import json
from pathlib import Path
base = Path('paper/experiments/_smoke_gold')
gold_path = base / 'gold_smoke.jsonl'
pred_path = base / 'predictions_smoke.jsonl'
with (base / 'gold_template.jsonl').open(encoding='utf-8') as src, \
     gold_path.open('w', encoding='utf-8') as gold, \
     pred_path.open('w', encoding='utf-8') as pred:
    for line in src:
        obj = json.loads(line)
        obj['gold'] = {'task': ['fault detection'], 'model': 'cnn', 'linkage': 'title match'}
        gold.write(json.dumps(obj, ensure_ascii=False) + '\n')
        pred.write(json.dumps({
            'record_id': obj['record_id'],
            'prediction': {'task': 'Fault Detection', 'model': ['CNN'], 'linkage': 'title-match'}
        }, ensure_ascii=False) + '\n')
PY

python paper/experiments/evaluate_extraction.py \
  --gold paper/experiments/_smoke_gold/gold_smoke.jsonl \
  --predictions paper/experiments/_smoke_gold/predictions_smoke.jsonl \
  --output-dir paper/experiments/_smoke_eval \
  --fields task,model,linkage
```
