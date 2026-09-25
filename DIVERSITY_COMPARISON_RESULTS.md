# Comparación de diversidad CBR — corpus completo 1.821 documentos

## Alcance vigente

El experimento principal usa los artefactos canónicos documentados en `paper/supplement/results/REPORT.md` y reproducidos desde `.build/diversity_comparison_1821_v12_no_default_sync`.

- Registros Scopus recuperados: **3.990**.
- Registros incluidos tras cribado: **2.768**.
- PDF recuperados: **1.822** archivos.
- Documentos PDF únicos por SHA-256: **1.821**.
- Artefactos canónicos `facts_*.ttl`: **1.821**.
- Consultas comparadas: **1.821**, una por documento único.
- Base CBR: **263** casos de `CleanedDATA V12-05-2021.csv`.

La diferencia entre 1.822 archivos PDF y 1.821 documentos se debe a un duplicado exacto; no se contabiliza como fallo de extracción.

## Método

- **Sin diversidad:** top-5 por similitud de HeadlessCBR.
- **Con diversidad:** pool top-15 de HeadlessCBR, rerankeado a top-5 con MMR (`lambda_relevance=0.70`) y top-1 preservado.
- La similitud entre soluciones combina enfoque, tipo, modelos y preprocesamiento con pesos `0.20/0.25/0.40/0.15`.
- La taxonomía de diversidad contiene **131** términos leídos de `external/Diversity-Improvement-in-CBR/Methods2.py`.
- `Unknown synchronization` se trata como ausencia y no se pondera.

## Resultados principales

| Métrica | Sin diversidad | Con MMR |
|---|---:|---:|
| Consultas con resultados | 1.821/1.821 | 1.821/1.821 |
| Similitud del primer resultado | 0,5630 | 0,5630 |
| Similitud media top-5 | 0,5563 | 0,5536 |
| Firmas de modelos únicas por lista | 4,6332 | 4,9973 |
| Listas con firmas repetidas | 610 | 5 |
| Disimilitud intra-lista | 0,4216 | 0,5265 |

Cambios frente al baseline:

- Orden top-5 cambiado: **1.821/1.821**.
- Conjunto de referencias top-5 cambiado: **1.819/1.821**.
- Primer resultado preservado: **1.821/1.821** por diseño.
- ILD aumentó en **1.707** consultas, disminuyó en **112** y empató en **2**.

## Interpretación

Estos resultados demuestran comportamiento algorítmico de reranking y reducción de redundancia bajo la similitud de solución definida. No demuestran fidelidad factual de extracción ni utilidad humana de las recomendaciones. La ILD comparte la función `s_sol` usada por MMR, por lo que no es una validación independiente.

## Repetición

```powershell
.\.venv\Scripts\python.exe scripts\compare_diversity_all_papers.py `
  --facts-glob "extraction_papers/ontocast_runs/run_*/output/facts_*.ttl" `
  --casebase-csv "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/CleanedDATA V12-05-2021.csv" `
  --top-k 5 --pool-size 15 --lambda-relevance 0.70 `
  --query-year 2026 --drop-default-synchronization `
  --output-dir ".build/diversity_comparison_1821_v12_no_default_sync"
```

Resultados y auditorías detalladas: `paper/supplement/results/`, `paper/supplement/statistics/` y `paper/supplement/audit/`.
