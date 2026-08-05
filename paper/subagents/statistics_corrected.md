Hecho. No edité manuscrito ni fuentes; solo añadí artefactos bajo:

`C:\repos\Ontologies\.build\diversity_comparison_1821_v12_corrected\statistical_analysis_outputs\`

Archivos principales:
- `paired_metric_summary.csv`
- `task_stratified_metric_summary.csv`
- `sensitivity_lambda_overview.csv`
- `sensitivity_lambda_metric_changes.csv`
- `pseudoreplication_diagnostics.csv`
- `publication_text_es.md`
- `analysis_manifest.json`

Usé solo el experimento corregido V12, case base `CleanedDATA V12-05-2021.csv` con 263 casos, `pipeline.diversity_rerank`, 20.000 bootstraps pareados con semilla `20260727`. No usé `unique_full/V21`.

## Resultados pareados globales, λ=0.70

Todas son métricas algorítmicas de recuperación/reranking.

| Métrica algorítmica | Sin diversidad | MMR λ=0.70 | Δ medio IC95% bootstrap | Δ relativo | Mejora/empeora/empate | Test |
|---|---:|---:|---:|---:|---:|---|
| Similitud primer resultado | 0.5811 | 0.5811 | 0.0000 [0.0000, 0.0000] | 0.00% | 0/0/1821 | no procede |
| Similitud media top-5 | 0.5597 | 0.5518 | -0.0079 [-0.0084, -0.0075] | -1.42% | 0/1459/362 | Wilcoxon p=3.52e-241, r_rb=-1.000 |
| Modelos únicos top-5 | 4.7776 | 5.0000 | +0.2224 [0.2021, 0.2427] | +4.66% | 381/0/1440 | Wilcoxon p=3.01e-80; sign test p=4.06e-115 |
| ILD algorítmica | 0.4273 | 0.5349 | +0.1076 [0.1045, 0.1107] | +25.17% | 1775/44/2 | Wilcoxon p=5.24e-296, r_rb=0.995 |

Nota publicable: la ILD comparte la misma función de similitud entre soluciones que usa MMR para penalizar redundancia; por tanto, es una métrica alineada con el objetivo optimizado, no una validación independiente.

## Sensibilidad exacta, top-k=5, top-1 fijo

`λ=0.70` reprodujo exactamente los rankings existentes: 1821/1821.

| λ | Sim. media top-5 | Modelos únicos | Listas con repetidos | ILD | Cambio conjunto | Top-1 preservado |
|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 0.5496 | 5.000 | 0 | 0.5398 | 1820/1821 | 1821/1821 |
| 0.6 | 0.5505 | 5.000 | 0 | 0.5387 | 1820/1821 | 1821/1821 |
| 0.7 | 0.5518 | 5.000 | 0 | 0.5349 | 1819/1821 | 1821/1821 |
| 0.8 | 0.5574 | 4.995 | 10 | 0.5182 | 1796/1821 | 1821/1821 |
| 0.9 | 0.5585 | 4.988 | 21 | 0.5119 | 1757/1821 | 1821/1821 |

## Estratos por tarea: Δ medio

| Tarea | n | Δ similitud media | Δ modelos únicos | Δ ILD IC95% |
|---|---:|---:|---:|---:|
| Fault detection | 782 | -0.0020 | +0.2826 | +0.0972 [0.0920, 0.1024] |
| Fault feature extraction | 93 | -0.0043 | +0.2473 | +0.1034 [0.0932, 0.1135] |
| Fault identification | 122 | -0.0027 | +0.1803 | +0.1210 [0.1111, 0.1311] |
| Health assessment | 303 | -0.0038 | +0.3663 | +0.1037 [0.0968, 0.1108] |
| Health modelling | 8 | -0.0066 | +0.5000 | +0.1515 [0.0954, 0.2116] |
| Multiple steps future state forecast | 6 | -0.0002 | +0.0000 | +0.0614 [0.0296, 0.0871] |
| One step future state forecast | 136 | -0.0159 | +0.0000 | +0.1034 [0.0942, 0.1130] |
| Remaining useful life estimation | 371 | -0.0236 | +0.0647 | +0.1306 [0.1241, 0.1372] |

## Pseudorreplicación

| Unidad | Únicos | % únicos | Máx. clúster |
|---|---:|---:|---:|
| Firmas de consulta normalizadas | 1684/1821 | 92.48% | 51 |
| Ranking baseline ordenado | 815/1821 | 44.76% | 129 |
| Ranking MMR λ=0.70 ordenado | 655/1821 | 35.97% | 109 |

Texto publicable completo en:  
`C:\repos\Ontologies\.build\diversity_comparison_1821_v12_corrected\statistical_analysis_outputs\publication_text_es.md`
