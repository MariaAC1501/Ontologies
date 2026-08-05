# Material suplementario

Este directorio acompaña al manuscrito. Contiene artefactos derivados, protocolos y auditorías; no redistribuye los PDF protegidos por licencia.

## `results/`

- `summary.json`: experimento principal V12 sin ponderar `Unknown synchronization`.
- `default_sync_control_summary.json`: control que pondera ese default.
- `per_query.csv`: métricas de las 1.821 consultas.
- `queries.csv`: casos extraídos y consultas normalizadas.
- `REPORT.md`: reporte automático.

## `statistics/`

- `paired_metric_summary.csv`: cambios, IC95%, Wilcoxon y tamaños de efecto.
- `task_stratified_metric_summary.csv`: estratos por tarea.
- `sensitivity_lambda_overview.csv`: sensibilidad original a lambda.
- `pseudoreplication_diagnostics.csv`: firmas y rankings repetidos.
- `alternative_baselines.csv`: CBR, deduplicación, azar y MMR.
- `default_sync_ablation.csv`: efecto del desconocido ponderado.
- `analysis_manifest.json`: semilla, remuestras y entradas.

## `audit/`

Auditorías añadidas tras revisión experta:

- `field_coverage_19cols.csv`: cobertura/defaults de los 19 campos.
- `bridge_per_query.csv`: valores y clasificación por artefacto.
- `rdfstar_cleanup_summary.csv`: triples, RDF-star y literales inválidos.
- `rdfstar_provenance_sidecar.csv.gz`: 311.559 asociaciones sentencia--chunk preservadas.
- `shacl_validation_*.csv`: formas SHACL mínimas y violaciones.
- `normalized_field_coverage.csv` y `query_information_patterns.csv`: pérdida durante normalización.
- `cluster_bootstrap.csv`: bootstrap por consulta, firma y patrón de ranking.
- `positions_2_5_summary.csv`, `duplicate_transition.csv` y `delta_distribution_quantiles.csv`.
- `extended_mmr_sensitivity.csv`: lambda 0/1, pool 10--30, k 3/5/10 y pesos.
- `strong_reranking_comparators.csv`: deduplicación, MMR, max-sum y MAP-DPP.
- `cbr_attribute_year_ablations.csv`: atributos de consulta y recencia.
- `extraction_model_batch_effects.csv`: resultados descriptivos por modelo/lote.
- `linkage_confidence_sensitivity.csv`: exclusión de 25 enlaces no exactos.
- `pdf_availability_bias.csv`: sesgo de disponibilidad.
- `expert_validation_protocol.md` y `expert_validation_sample_template.csv`.

**Importante:** la plantilla experta no está anotada. No representa validación humana ni ground truth.

## `protocol/`

- Consulta Scopus, criterios y decisiones de cribado.
- `extraction_manifest.csv`: 1.822 filas con hashes, lote/modelo/chunks y enlace PDF--facts.
- `schema_mapping.md`: mapeo OPMAD/CBR.
- `opmad_extraction_shapes.ttl`: formas SHACL de auditoría.
- Piloto operativo de modelo de extracción.

## `repro/`

- `software_manifest.json`: versiones, commit/submódulos y hashes de entradas/código.
- `environment.txt`: versiones de paquetes principales.

## Reproducción de análisis

Desde la raíz del repositorio:

```powershell
.\.venv\Scripts\python.exe paper\analysis\statistical_analysis.py
.\.venv\Scripts\python.exe paper\analysis\revision_audit.py
.\.venv\Scripts\python.exe paper\analysis\extended_reranking_analysis.py
.\.venv\Scripts\python.exe paper\analysis\cbr_ablation_analysis.py
.\.venv\Scripts\python.exe paper\analysis\corpus_bias_analysis.py
.\.venv\Scripts\python.exe paper\analysis\shacl_validation.py
.\.venv\Scripts\python.exe paper\figures\generate_figures.py
```

`extended_reranking_analysis.py` requiere el pool-30 descrito en `paper/README.md`. Las ablaciones myCBR reutilizan resultados cacheados si están completos.

## Integridad

```bash
find paper/supplement -type f ! -name SHA256SUMS.txt -print0 | sort -z | xargs -0 sha256sum > paper/supplement/SHA256SUMS.txt
sha256sum -c paper/supplement/SHA256SUMS.txt
```
