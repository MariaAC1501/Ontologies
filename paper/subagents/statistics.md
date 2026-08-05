No edité fuentes ni manuscrito. Generé salidas reproducibles en `.build/diversity_comparison_1821_unique_full/statistical_analysis_outputs/` usando bootstrap pareado percentil, semilla fija base `20260727`, `B=20000`.

### Definiciones inspeccionadas en código

- `mean_similarity`: media del campo CBR `Sim` en el top-5.
- `unique_models`: número de cadenas `Models` no vacías distintas en el top-5.
- `intra_list_dissimilarity`: media de `1 - solution_similarity()` sobre los 10 pares del top-5.
- `solution_similarity()`: mezcla ponderada de enfoque, tipo, modelos y preprocesamiento con pesos `(0.20, 0.25, 0.40, 0.15)`.
- `rerank_mmr()`: MMR greedy sobre `pool_size=15`, `top_k=5`, con `keep_top1=True`; por tanto, el top-1 está preservado por construcción.

## Resultados globales pareados, n=1821

| Métrica | Baseline media±DE | Diversidad media±DE | Δ media [IC95% boot] | Δ rel. medias | Mejora/Empeora/Empata | Prueba / efecto |
|---|---:|---:|---:|---:|---:|---|
| Disimilitud intra-lista | 0.5061±0.1488 | 0.6350±0.1555 | 0.1289 [0.1240, 0.1339] | +25.48% | 1709/109/3 | Wilcoxon p=1.57e-286; r_rb=0.979 |
| Similitud media top-5 | 0.5563±0.0600 | 0.5535±0.0601 | -0.0028 [-0.0031, -0.0026] | -0.51% | 0/1173/648 | Wilcoxon p=1.93e-193; r_rb=-1.000 |
| Modelos únicos top-5 | 4.6332±0.5442 | 4.9951±0.0701 | 0.3619 [0.3377, 0.3866] | +7.81% | 604/1/1216 | Sign test p=9.13e-180; efecto≈0.997 |
| Similitud top-1 | 0.5630±0.0614 | 0.5630±0.0614 | 0.0000 [0.0000, 0.0000] | 0.00% | 0/0/1821 | No aplicable |

Indicadores de comparación: orden cambiado `1821/1821`; conjunto de referencias cambiado `1818/1821`; top-1 preservado `1821/1821`. Listas con modelos repetidos: baseline `610/1821` vs diversidad `9/1821`.

## Estratificación por tarea

| Tarea | n | Dissim base→div | Δ Dissim [IC95%] | Dissim +/−/= | SimMedia base→div | Δ SimMedia [IC95%] | Modelos únicos base→div | Δ Modelos únicos [IC95%] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Fault detection | 782 | 0.476→0.598 | 0.122 [0.115, 0.129] | 741/39/2 | 0.550→0.548 | -0.003 [-0.003, -0.002] | 4.715→4.995 | 0.280 [0.246, 0.316] |
| Fault feature extraction | 93 | 0.635→0.763 | 0.127 [0.115, 0.139] | 92/1/0 | 0.538→0.534 | -0.004 [-0.004, -0.003] | 4.742→5.000 | 0.258 [0.172, 0.344] |
| Fault identification | 122 | 0.703→0.770 | 0.066 [0.060, 0.073] | 119/2/1 | 0.536→0.534 | -0.002 [-0.002, -0.002] | 4.656→5.000 | 0.344 [0.262, 0.426] |
| Health assessment | 303 | 0.611→0.769 | 0.158 [0.150, 0.166] | 303/0/0 | 0.547→0.542 | -0.005 [-0.006, -0.004] | 4.634→5.000 | 0.366 [0.307, 0.426] |
| Health modelling | 8 | 0.540→0.668 | 0.128 [0.065, 0.195] | 8/0/0 | 0.612→0.602 | -0.011 [-0.022, -0.001] | 4.500→5.000 | 0.500 [0.125, 0.875] |
| Multiple steps future state forecast | 6 | 0.351→0.412 | 0.061 [0.031, 0.087] | 5/1/0 | 0.539→0.539 | -0.000 [-0.001, 0.000] | 5.000→5.000 | 0.000 [0.000, 0.000] |
| One step future state forecast | 136 | 0.326→0.341 | 0.015 [0.008, 0.021] | 71/65/0 | 0.606→0.606 | -0.000 [-0.001, -0.000] | 5.000→5.000 | 0.000 [0.000, 0.000] |
| Remaining useful life estimation | 371 | 0.454→0.638 | 0.183 [0.170, 0.198] | 370/1/0 | 0.569→0.566 | -0.003 [-0.003, -0.002] | 4.288→4.987 | 0.698 [0.636, 0.760] |

## Sensibilidad de λ, top-1 preservado, top-k=5

| λ | Dissim div mean | Δ Dissim [IC95%] | SimMedia div mean | Δ SimMedia [IC95%] | Modelos únicos div mean | Δ Modelos únicos [IC95%] | Ref. set cambiado |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 0.6421 | 0.1360 [0.1310, 0.1410] | 0.5503 | -0.0061 [-0.0069, -0.0052] | 4.9978 | 0.3646 [0.3405, 0.3893] | 1819 (99.89%) |
| 0.6 | 0.6379 | 0.1319 [0.1270, 0.1368] | 0.5524 | -0.0039 [-0.0043, -0.0035] | 4.9978 | 0.3646 [0.3399, 0.3899] | 1818 (99.84%) |
| 0.7 | 0.6350 | 0.1289 [0.1240, 0.1339] | 0.5535 | -0.0028 [-0.0031, -0.0026] | 4.9951 | 0.3619 [0.3377, 0.3871] | 1818 (99.84%) |
| 0.8 | 0.6333 | 0.1272 [0.1223, 0.1322] | 0.5540 | -0.0023 [-0.0025, -0.0021] | 4.9901 | 0.3569 [0.3322, 0.3817] | 1811 (99.45%) |
| 0.9 | 0.6280 | 0.1219 [0.1171, 0.1267] | 0.5547 | -0.0016 [-0.0017, -0.0015] | 4.9857 | 0.3526 [0.3278, 0.3773] | 1796 (98.63%) |

### Texto breve para Resultados

El reranking MMR con diversidad preservó el primer resultado en todas las consultas, pero modificó el orden del top-5 en 100% y el conjunto de referencias en 99.84%. La disimilitud intra-lista aumentó de 0.5061 a 0.6350, con un cambio medio pareado de 0.1289 (IC95% bootstrap 0.1240–0.1339). Los modelos únicos por lista aumentaron de 4.633 a 4.995, mientras que las listas con modelos repetidos disminuyeron de 610 a 9. Este incremento de diversidad se acompañó de una reducción pequeña de similitud media top-5, Δ=-0.0028 (IC95% -0.0031 a -0.0026; -0.51%). La sensibilidad para λ=0.5–0.9 mostró el intercambio esperado: menor λ produjo mayor diversidad pero mayor pérdida de similitud media.

### Crítica y recomendaciones

- Reportaría como primarios: Δ pareado medio con IC95% bootstrap, proporciones mejora/empeora/empate, y tamaños de efecto.
- Para disimilitud y similitud media, Wilcoxon pareado es aceptable como análisis secundario.
- Para modelos únicos, preferiría sign test exacto o una tabla McNemar de “modelo repetido sí/no”; el Wilcoxon sobre un conteo acotado con muchos empates es menos interpretable.
- No reportaría pruebas sobre top-1: está preservado por construcción.
- No trataría los 10 pares intra-lista ni los 5 resultados como observaciones independientes.
- Hay pseudorreplicación: aunque hay 1821 facts únicos, sólo hay 1687 firmas de consulta normalizada y 1030 patrones baseline→diversidad únicos; algunos patrones se repiten hasta 109 veces. Por tanto, los p-valores son principalmente descriptivos/algorítmicos y probablemente sobrestiman la evidencia inferencial si se interpretan como consultas iid.
