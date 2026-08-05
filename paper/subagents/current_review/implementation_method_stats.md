No edité archivos. Inspeccioné datos/scripts y estos son los puntos accionables.

## Hallazgos clave del repositorio

- Corpus local: `extraction_papers/`
  - 1.822 PDF, 1.821 únicos por SHA.
  - 1.821 facts canónicos bajo `extraction_papers/ontocast_runs/run_*/output/facts_*.ttl`.
  - Hay 10 facts extra de benchmark si se usa `ontocast_runs/*/output`; para el artículo debe usarse `run_*`.
- Resultado principal: `.build/diversity_comparison_1821_v12_no_default_sync/`
  - `queries.csv`, `per_query.csv`, `cbr_data/pool_results_*.csv`, `with_diversity/*.diverse.csv`.
- Suplemento: `paper/supplement/`
  - Tiene resúmenes, estadísticas y manifiesto, pero no todos los TTL facts ni pools CBR top-15.
- Tests actuales:
  - `python -m unittest discover -s pipeline/tests -p "test_*.py"` pasa: 32 tests OK.
- Bloqueador reproducible:
  - `paper/analysis/statistical_analysis.py` actualmente se autoimporta a sí mismo como protocolo; así no es un script limpio de reproducción. Debe separarse en `stats_protocol.py` + wrapper.
- Señales metodológicas computables ya observadas:
  - 409 facts contienen >1 caso; 567 casos adicionales no usados.
  - `Online/Off-line`, `Performance`, `Performance indicator`, `Number of failure modes`: 0/1.821 informativos.
  - `Case study type`: siempre `Maintainable item`.
  - `Input for the model`: solo 32/1.821 no-default, pero luego normalizado a vacío.
  - Normalización final: tarea 1.821/1.821; activo 1.549; input type 1.381; sync/input-mode/case-type 0.
  - 121 consultas quedan solo con tarea + año.
  - RDF-star eliminado: 311.559 bloques `rdf:reifies`; todos los facts lo contienen.
  - 5 literales tipados mal formados detectables por `rdflib`.
  - Manifest: 1.797 enlaces exactos/casi exactos, 2 altos, 6 medios, 17 bajos.

---

## Plan implementable priorizado

### P0 — Reparar reproducibilidad básica

| Acción | Entrada | Salida concreta |
|---|---|---|
| Separar protocolo estadístico | `paper/analysis/statistical_analysis.py`, `.build/diversity_comparison_1821_v12_corrected/statistical_analysis_outputs/statistical_analysis.py` | `paper/analysis/stats_protocol.py`, `paper/analysis/statistical_analysis.py` reproducible |
| Archivar checksums de código/datos usados | `pipeline/*.py`, `scripts/*.py`, `tools/cbr/HeadlessCBR.java`, casebase, seed ontology | `paper/supplement/repro/software_manifest.json` |
| Validar suplemento | `paper/supplement/SHA256SUMS.txt` | `paper/supplement/repro/checksum_validation.txt` |
| Evitar dependencia oculta de `.build` en figuras | `.build/.../statistical_analysis_outputs` | copiar o leer desde `paper/supplement/statistics/` |

Comando base a conservar:

```powershell
.\.venv\Scripts\python.exe scripts\compare_diversity_all_papers.py `
  --facts-glob "ontocast_runs/run_*/output/facts_*.ttl" `
  --casebase-csv "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/CleanedDATA V12-05-2021.csv" `
  --top-k 5 --pool-size 15 --lambda-relevance 0.70 `
  --query-year 2026 --drop-default-synchronization `
  --output-dir ".build/diversity_comparison_reproduction"
```

---

### P1 — Auditoría RDF → CBR sin juicio humano

Crear script propuesto:

`paper/analysis/audit_rdf_bridge.py`

Entradas:

- `extraction_papers/ontocast_runs/run_*/output/facts_*.ttl`
- `pipeline/seed_ontology/opmad_seed.ttl`
- `paper/supplement/protocol/extraction_manifest.csv`

Salidas:

- `paper/supplement/audit/rdf_parse_summary.csv`
- `paper/supplement/audit/rdfstar_cleanup_counts.csv`
- `paper/supplement/audit/invalid_typed_literals.csv`
- `paper/supplement/audit/opmad_namespace_variants.csv`
- `paper/supplement/audit/field_coverage_19cols.csv`
- `paper/supplement/audit/multi_case_audit.csv`
- `paper/supplement/audit/rdf_bridge_audit_report.md`

Debe calcular:

- parseo antes/después de limpieza RDF-star;
- triples por archivo;
- bloques RDF-star eliminados;
- namespaces OPMAD `OPMAD#` vs `OPMAD/seed#`;
- cobertura real por los 19 campos;
- defaults: `Not reported`, `Unknown synchronization`, `0`, `2021`;
- número de casos por TTL;
- campos con valores tipo `Facts...`;
- literales XSD inválidos.

Esto refuerza o limita la afirmación de interoperabilidad técnica sin inventar exactitud semántica.

---

### P2 — Auditoría de consulta normalizada

Crear:

`paper/analysis/audit_query_normalization.py`

Entradas:

- `paper/supplement/results/queries.csv`
- `paper/supplement/protocol/extraction_manifest.csv`
- `external/.../CleanedDATA V12-05-2021.csv`

Salidas:

- `paper/supplement/audit/query_informativeness.csv`
- `paper/supplement/audit/normalization_drop_reasons.csv`
- `paper/supplement/audit/cbr_vocabulary_alignment.csv`
- `paper/supplement/audit/query_signature_clusters.csv`

Debe calcular:

- número de campos activos por consulta;
- distribución: tarea sola, tarea+activo, tarea+input, tarea+activo+input;
- campos descartados por incompatibilidad léxica;
- firmas repetidas;
- cobertura frente al vocabulario histórico de myCBR.

Prioridad alta porque demuestra si el CBR se alimenta de 19 campos o de 2–4 señales reales.

---

### P3 — Impacto de defaults y ablaciones CBR

Crear:

`paper/analysis/run_cbr_ablations.py`

Entradas:

- `.build/diversity_comparison_1821_v12_no_default_sync/query_batch_input_pool.csv`
- `.build/diversity_comparison_1821_v12_no_default_sync/cbr_data/`
- `tools/cbr/HeadlessCBR.java`

Salidas:

- `.build/cbr_ablation_<fecha>/summary.csv`
- `.build/cbr_ablation_<fecha>/per_query_ablation.csv`
- `paper/supplement/audit/cbr_ablation_summary.csv`

Condiciones a calcular sin evaluación humana:

1. principal: tarea + activo + input + año;
2. tarea + año;
3. tarea + activo + año;
4. tarea + input + año;
5. sin activo;
6. sin input;
7. `Unknown synchronization` ponderado vs no ponderado;
8. `query_year` 2021/2025/2026/2027;
9. euclidean vs weighted-sum.

Métricas:

- similitud top-1/top-5;
- rankings únicos;
- concentración de patrones;
- cambios de top-1;
- ILD y firmas únicas tras MMR.

---

### P4 — Sensibilidad MMR más completa

Crear:

`paper/analysis/mmr_sensitivity_extended.py`

Entradas:

- `.build/diversity_comparison_1821_v12_no_default_sync/cbr_data/pool_results_*.csv`
- `pipeline/diversity_rerank.py`
- casebase V12

Salidas:

- `paper/supplement/audit/mmr_topk_lambda_weight_sensitivity.csv`
- `paper/supplement/audit/mmr_pool_size_sensitivity.csv`
- `paper/supplement/audit/mmr_oracle_gap.csv`

Análisis:

- top-k ∈ {3, 5, 10};
- λ ∈ {0.5, 0.6, 0.7, 0.8, 0.9};
- pesos de solución: actuales, uniformes, solo modelos, sin preprocesamiento;
- pool ∈ {10, 15, 30, 50};
- “oracle” dentro de pool-15: explorar combinaciones top-5 para estimar si MMR está cerca del frente diversidad/similitud.

Esto evita que el resultado dependa solo de `pool=15`, `top-5`, pesos fijos y λ=0,70.

---

### P5 — Pseudorreplicación e intervalos más robustos

Crear:

`paper/analysis/cluster_bootstrap.py`

Entradas:

- `paper/supplement/results/per_query.csv`
- `paper/supplement/results/queries.csv`

Salidas:

- `paper/supplement/audit/bootstrap_by_query.csv`
- `paper/supplement/audit/bootstrap_by_normalized_signature.csv`
- `paper/supplement/audit/bootstrap_by_baseline_ranking.csv`

Calcular IC bootstrap por:

1. consulta individual;
2. firma normalizada;
3. patrón de ranking baseline;
4. patrón de ranking MMR.

Así se controla que 1.821 consultas producen muchos rankings repetidos.

---

### P6 — Sesgo de corpus y extracción por lote/modelo

Crear:

`paper/analysis/corpus_and_batch_bias_audit.py`

Entradas:

- `extraction_papers/scopus_export_May 26-2026_screened.csv`
- `extraction_papers/failed_pdfs_included_for_retry.csv`
- `paper/supplement/protocol/extraction_manifest.csv`
- `paper/supplement/results/per_query.csv`

Salidas:

- `paper/supplement/audit/pdf_availability_bias.csv`
- `paper/supplement/audit/extraction_model_batch_effects.csv`
- `paper/supplement/audit/linkage_confidence_effects.csv`

Calcular:

- incluidos con PDF vs incluidos sin PDF por fuente, OA, año, confianza;
- métricas y cobertura por `actual_model`;
- métricas por chunks=1 vs chunks=3;
- métricas por retry/sanitización;
- métricas excluyendo los 25 enlaces no exactos.

---

## Recomendación editorial inmediata

Antes de enviar, añadir al suplemento una sección nueva:

`paper/supplement/audit/`

con los CSV anteriores y un `AUDIT_REPORT.md`. Eso permitiría decir con más precisión:

> “La cadena demuestra interoperabilidad ejecutable y auditable; la cobertura semántica de varios campos es limitada y se cuantifica explícitamente.”

Esa formulación es defendible. Decir que el puente demuestra interoperabilidad semántica plena seguiría siendo vulnerable.
