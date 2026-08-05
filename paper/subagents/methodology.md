# Informe metodológico para el artículo OntoCast→OPMAD/RDF→CSV→CBR→MMR

## 1. Dictamen ejecutivo

El repositorio sí soporta una arquitectura publicable, pero el artículo debe formularla como **integración reproducible e interoperabilidad técnica**, no como validación semántica completa de extracción ni como nuevo algoritmo de diversidad.

La cadena real auditada es:

```text
PDF
→ OntoCast en modo fijo OPMAD, facts-only
→ RDF/Turtle con tipos OPMAD
→ pipeline/facts_to_csv.py
→ CSV semicolon-delimited de 19 campos
→ HeadlessCBR / myCBR sobre la base heredada
→ reranking MMR de resultados CBR
```

Resultado experimental más actual: `.build/diversity_comparison_1821_unique_full/`.

- PDFs en `extraction_papers`: 1822.
- Facts canónicos analizados: 1821.
- Unidad experimental: **una consulta CBR por artefacto `facts_*.ttl`**, usando el primer caso extraído.
- Base CBR recuperada: **base heredada**, no los 1821 papers como nueva case base.
- Baseline: HeadlessCBR top-5 por similitud.
- Método con diversidad: HeadlessCBR pool-15 + MMR top-5, preservando top-1.
- Mejora observada: disimilitud intra-lista media 0.5061 → 0.6350, con pérdida de similitud media 0.5563 → 0.5535.

## 2. Fórmulas que deben aparecer

### Similitud semántica de conjuntos

Usada en el CBR original para atributos como tarea e input type:

\[
sim(A,B)=1-\log_2\left(1+
\frac{|A\setminus B|+|B\setminus A|}
{|A\setminus B|+|B\setminus A|+|A\cap B|}
\right)
\]

### Similitud textual

\[
sim_{lev}(a,b)=1-\frac{d_{lev}(a,b)}{\max(|a|,|b|)}
\]

### Similitud global CBR

El código delega en myCBR. Documentar como combinación de similitudes locales:

\[
S(q,c)=Agg(\{w_i\,s_i(q_i,c_i)\}_{i=1}^{n})
\]

donde `Agg` es `euclidean` en los experimentos batch y `weighted sum` es alternativa soportada.

### MMR usado en el reranking

\[
x^*=\arg\max_{x\in R\setminus S}
\left[
\lambda\,rel(x)
-
(1-\lambda)\max_{y\in S}sim_{sol}(x,y)
\right]
\]

Con:

- \(rel(x)\): similitud CBR `Sim`.
- \(\lambda=0.70\).
- top-1 preservado por diseño.

### Similitud de solución

\[
sim_{sol}=0.20s_{approach}+0.25s_{type}+0.40s_{models}+0.15s_{preproc}
\]

### Disimilitud intra-lista

\[
ILD(L)=\frac{2}{k(k-1)}\sum_{i<j}(1-sim_{sol}(x_i,x_j))
\]

## 3. Parámetros principales

### OntoCast fijo

Archivo: `pipeline/ontocast_config.env`.

- `RENDER_MODE=facts`
- `SKIP_ONTOLOGY_CRITIQUE=true`
- `ONTOCAST_ONTOLOGY_DIRECTORY=pipeline/seed_ontology`
- `PARALLEL_WORKERS=2`
- `PARALLEL_FACTS_RETRIES=3`
- `MAX_VISITS_PER_NODE=3`
- default runner: `head_chunks=3`
- extracción vía proxy local Pi Codex, no API key directa.

Advertencia: las extracciones históricas no usaron un único modelo. Batches antiguos muestran `gpt-5-mini` / `gpt-5.4-mini`; los restantes y reintentos usan `gpt-5.6-luna`.

### CBR

Archivos clave:

- `tools/cbr/HeadlessCBR.java`
- `scripts/run_cbr.sh`
- `external/.../CleanedDATA V21-07-2021.csv`

El CBR actual recupera desde la base heredada de 200 casos. En las consultas batch:

- top-k baseline: 5.
- pool MMR: 15.
- amalgamación: `euclidean`.
- pesos CBR: 1 para campos no vacíos; 0 para campos vacíos.
- `Publication Year` siempre entra con peso 1 y usa el año actual del sistema.

### MMR

Archivo: `pipeline/diversity_rerank.py`.

- `lambda_relevance=0.70` en `compare_diversity_all_papers.py`.
- pesos solución: `(0.20, 0.25, 0.40, 0.15)`.
- top-1 preservado.
- taxonomía: 131 términos desde `external/Diversity-Improvement-in-CBR/Methods2.py`.

## 4. Métricas y resultados actuales

Fuente: `.build/diversity_comparison_1821_unique_full/summary.json`.

| Métrica | Sin diversidad | Con MMR |
|---|---:|---:|
| Consultas con resultados | 1821/1821 | 1821/1821 |
| Similitud primer resultado | 0.5630 | 0.5630 |
| Similitud media top-5 | 0.5563 | 0.5535 |
| Modelos únicos por lista | 4.63 | 5.00 |
| Listas con modelos repetidos | 610 | 9 |
| Disimilitud intra-lista | 0.5061 | 0.6350 |

Observaciones adicionales desde `per_query.csv`:

- ILD aumentó en 1709 consultas, bajó en 109 y no cambió en 3.
- Cambio medio ILD: +0.1289.
- La similitud media nunca mejora con MMR; baja en 1173 consultas y queda igual en 648.
- Top-1 preservado en 1821/1821 **por construcción**, no como resultado emergente.

## 5. Amenazas a validez y problemas metodológicos

1. **No hay ground truth de relevancia.** Las métricas miden diversidad interna y similitud CBR, no utilidad real para un arquitecto.

2. **Métrica circular.** MMR optimiza diversidad usando `sim_sol`; luego se evalúa con una métrica basada en la misma `sim_sol`.

3. **Pseudorreplicación.** Hay 1821 consultas, pero muchas producen vectores normalizados casi idénticos. Además, la base recuperada tiene solo 200 casos.

4. **Campos descartados por normalización.** En `queries.csv`:
   - `normalized_case_study_type`: 0/1821 no vacío.
   - `normalized_online_offline`: 0/1821.
   - `normalized_input_for_model`: 0/1821.
   - 121 consultas quedan prácticamente solo con tarea.

5. **Valores por defecto del puente.** `facts_to_csv.py` rellena:
   - año por defecto 2021;
   - `Unknown synchronization`;
   - `Not reported`;
   - performance no reportado;
   - número de failure modes = 0;
   - task por defecto: `One step future state forecast`.

6. **No se reconstruye automáticamente la base CBR con los 1821 papers.** La comparación usa los papers extraídos como consultas contra la base heredada.

7. **Trazabilidad incompleta facts→PDF.** `queries.csv` guarda `facts_file`, y los manifiestos guardan PDFs seleccionados, pero no hay un manifiesto enriquecido con `corpus_id`, PDF y `facts_*.ttl` en una sola fila.

8. **Extracción LLM no determinista ni homogénea.** Cambios de modelo, reintentos, sanitización RDF y cuotas afectan reproducibilidad.

9. **Posible filtración.** Si algún paper extraído coincide con los estudios de la base heredada, no hay exclusión de self-match ni control train/test.

10. **`DIVERSITY_COMPARISON_RESULTS.md` está desactualizado.** Documenta 599 consultas; el resultado actual es el de `.build/diversity_comparison_1821_unique_full/`.

## 6. Comandos de reproducción

### Tests deterministas

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s pipeline\tests -p "test_*.py"
```

### Convertir facts a CSV

```powershell
.\.venv\Scripts\python.exe pipeline\facts_to_csv.py `
  --facts "pipeline\test_output\facts_*.ttl" `
  --ontology "pipeline\seed_ontology\opmad_seed.ttl" `
  --output "pipeline\test_output\extracted_cases.csv"
```

### Consulta CBR

```powershell
ontologies-cbr query-one `
  --task "Remaining useful life estimation" `
  --input-for-model "Time series" `
  --input-type "Temperature, Fluid Pressure" `
  --number-of-cases 5
```

### Comparación CBR vs MMR actual

Usar un directorio nuevo:

```powershell
.\.venv\Scripts\python.exe scripts\compare_diversity_all_papers.py `
  --facts-glob "ontocast_runs/run_*/output/facts_*.ttl" `
  --top-k 5 `
  --pool-size 15 `
  --lambda-relevance 0.70 `
  --output-dir ".build\diversity_comparison_repro"
```

## 7. Contribuciones defendibles

Formular así:

1. “Se presenta una integración reproducible entre extracción RDF guiada por OPMAD y una base CBR heredada de mantenimiento predictivo.”
2. “Se implementa un puente determinista RDF/Turtle→CSV de 19 campos compatible con myCBR.”
3. “Se proporciona un adaptador headless para ejecutar CBR sin GUI y habilitar experimentos batch.”
4. “Se evalúa un reranking MMR post-CBR que incrementa la diversidad de soluciones con una pérdida pequeña de similitud media.”
5. “Se documentan límites de trazabilidad, normalización y validez para futuros benchmarks con anotación humana.”

Evitar:

- “El sistema extrae correctamente los 19 campos” sin evaluación humana.
- “La diversidad mejora la calidad de recomendación” sin estudio con usuarios o ground truth.
- “Se implementa el algoritmo CNN de Emmanuel” — el repo actual usa MMR, no CNN.
- “Los 1821 papers forman la nueva case base CBR” — en el experimento son consultas.
