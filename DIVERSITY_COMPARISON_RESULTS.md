# Comparación de diversidad CBR — 2026-07-10

## Alcance

`extraction_papers/` contiene 1,822 PDFs de primer nivel y 599 artefactos
canónicos `facts_*.ttl`: 100 de `run_100_20260611_194110/output` y 499 de
`run_500_20260710_185042/output`. Se ejecutó una consulta CBR por cada uno de
esos 599 papers ya extraídos.

Se excluyeron 82 facts de `output_pre_quota` y un facts de `retries/`, porque
son resultados intermedios o reintentos y los incluirían dos veces. Los 1,223
PDFs restantes no tienen facts canónicos; no se enviaron a OntoCast/LLM.

El resultado completo está en
`.build/diversity_comparison_599_available_20260710/`:

- `REPORT.md` y `summary.json`: métricas agregadas.
- `queries.csv`: caso extraído y consulta normalizada.
- `per_query.csv`: referencias, similitud y diversidad por consulta.
- `cbr_data/`: baseline top-5 y pools top-15.
- `with_diversity/`: listas MMR top-5.

## Método

- **Sin diversidad:** cinco resultados de mayor similitud de `HeadlessCBR`.
- **Con diversidad:** pool de 15 resultados de `HeadlessCBR`, rerankeado a
  cinco con MMR (`lambda_relevance=0.70`) y preservando top-1.
- La disimilitud de soluciones combina enfoque, tipo, modelos y
  preprocesamiento. `pipeline.diversity_rerank` leyó los 131 términos de
  `external/Diversity-Improvement-in-CBR/Methods2.py`; no importa la GUI ni los
  módulos upstream con efectos secundarios.

Algunos facts incluyen publicaciones citadas junto con el estudio fuente. Se
retuvo el primer caso determinista de cada facts file para mantener una consulta
por PDF; 216 casos adicionales se excluyeron por ese motivo.

## Resultados (599 consultas)

| Métrica | Sin diversidad | Con diversidad |
|---|---:|---:|
| Consultas con resultados | 599/599 | 599/599 |
| Similitud del primer resultado | 0.5785 | 0.5785 |
| Similitud media del top-5 | 0.5726 | 0.5705 |
| Modelos únicos por lista | 4.65 | 5.00 |
| Listas con modelos repetidos | 195 | 1 |
| Disimilitud intra-lista (0–1) | 0.4949 | 0.6205 |

Las 599 listas cambiaron de orden; 598 cambiaron el conjunto de referencias y
las 599 preservaron top-1. La ganancia media de diversidad fue **+0.1256** de
disimilitud intra-lista, a cambio de **-0.0021** de similitud media del top-5.
En 540 consultas la disimilitud aumentó, en 58 disminuyó y en una no cambió.

## Repetición

```powershell
.\.venv\Scripts\python.exe scripts\compare_diversity_all_papers.py
```

El comando usa sólo los facts canónicos en `ontocast_runs/*/output/`. Para
ampliar la comparación, hay que extraer facts de los 1,223 PDFs pendientes y
volver a ejecutarlo.
