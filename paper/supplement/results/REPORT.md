# Comparación de diversidad CBR

Directorio de ejecución: `.build\diversity_comparison_1821_v12_no_default_sync`

## Cobertura

- Archivos PDF de primer nivel en `extraction_papers`: **1822**.
- Documentos PDF únicos por SHA-256: **1821**.
- Archivos duplicados adicionales: **1**.
- Artefactos canónicos `facts_*.ttl` disponibles: **1821**.
- Consultas comparadas (una por artefacto): **1821**.
- Documentos únicos sin facts canónicos (estimación por conteo): **0**.

La cobertura distingue archivos de documentos únicos para no contar un duplicado exacto como extracción ausente.

## Método

- Sin diversidad: top-5 por similitud de HeadlessCBR.
- Con diversidad: pool-15 de HeadlessCBR y MMR top-5 (`lambda=0.70`).
- La similitud entre soluciones usa enfoque, tipo, modelos y preprocesamiento; la taxonomía contiene 131 términos leídos de `external/Diversity-Improvement-in-CBR/Methods2.py`.

## Resultados

| Métrica | Sin diversidad | Con diversidad |
|---|---:|---:|
| Consultas con resultados | 1821/1821 | 1821/1821 |
| Similitud del primer resultado | 0.5630 | 0.5630 |
| Similitud media del top-k | 0.5563 | 0.5536 |
| Modelos únicos por lista | 4.63 | 5.00 |
| Listas con modelos repetidos | 610 | 5 |
| Disimilitud intra-lista (0–1) | 0.4216 | 0.5265 |

## Cambios frente al baseline

- Orden top-k cambiado: **1821/1821**.
- Conjunto de referencias top-k cambiado: **1819/1821**.
- Primer resultado preservado: **1821/1821**.

Los datos por consulta están en `per_query.csv`; las consultas normalizadas en `queries.csv`; y las listas CBR y rerankeadas en `cbr_data/` y `with_diversity/`.
