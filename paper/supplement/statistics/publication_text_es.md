# Análisis estadístico principal sin evidencia por defecto de sincronización

Ámbito principal: `.build/diversity_comparison_1821_v12_no_default_sync` (V12/263 casos, 1.821 consultas, query-year 2026). En este análisis `Unknown synchronization` se descarta como evidencia por defecto; por tanto, este experimento sin default debe ser el resultado principal del manuscrito. El directorio `.build/diversity_comparison_1821_v12_final` se usa sólo como ablación descriptiva del default ponderado.

Todas las cantidades son métricas algorítmicas de recuperación/reranking, no medidas de desempeño predictivo ni validación clínica/industrial. La ILD se calcula con la misma función de similitud entre soluciones que entra en MMR y debe leerse como métrica alineada con el objetivo optimizado.

Estratos por tarea: Fault detection: 782; Remaining useful life estimation: 371; Health assessment: 303; One step future state forecast: 136; Fault identification: 122; Fault feature extraction: 93; Health modelling: 8; Multiple steps future state forecast: 6.

## Resultados pareados globales

| Métrica | Sin diversidad | Con MMR λ=0.70 | Δ medio (IC95%) | Δ relativo (IC95%) | Mejora/empeora/empate | Wilcoxon p; r_rb | Sign test |
|---|---|---|---|---|---|---|---|
| similitud algorítmica del primer resultado | 0.5630 | 0.5630 | 0.0000 [0.0000, 0.0000] | 0.00% [0.00%, 0.00%] | 0/0/1821 | no procede (todo empates) |  |
| similitud algorítmica media del top-5 | 0.5563 | 0.5536 | -0.0027 [-0.0029, -0.0025] | -0.48% [-0.52%, -0.44%] | 0/1193/628 | 1.19e-197; -1.000 |  |
| modelos únicos en el top-5 | 4.6332 | 4.9973 | 0.3641 [0.3394, 0.3888] | 7.86% [7.29%, 8.44%] | 605/0/1216 | 3.99e-123; 1.000 | 1.51e-182 |
| disimilitud intra-lista (ILD) algorítmica | 0.4216 | 0.5265 | 0.1049 [0.1013, 0.1087] | 24.89% [23.91%, 25.93%] | 1707/112/2 | 5.93e-286; 0.978 |  |

## Sensibilidad exacta por λ (pool-15 del experimento sin default, top-k=5, top-1 fijo)

| λ | Sim. media top-5 | Modelos únicos | Listas con repetidos | ILD | Cambio conjunto | Top-1 preservado | Patrones únicos |
|---|---|---|---|---|---|---|---|
| 0.5 | 0.5522 | 5.000 | 0 | 0.5295 | 1821/1821 | 1821/1821 | 647 |
| 0.6 | 0.5533 | 5.000 | 0 | 0.5274 | 1821/1821 | 1821/1821 | 666 |
| 0.7 | 0.5536 | 4.997 | 5 | 0.5265 | 1819/1821 | 1821/1821 | 699 |
| 0.8 | 0.5543 | 4.992 | 14 | 0.5248 | 1818/1821 | 1821/1821 | 748 |
| 0.9 | 0.5549 | 4.986 | 25 | 0.5201 | 1798/1821 | 1821/1821 | 822 |

## Ablación descriptiva frente al default ponderado

| Ámbito | Rankings iguales | Top-1 iguales | Conjuntos iguales | Δ sim. top-5 | Δ modelos únicos | Δ ILD |
|---|---|---|---|---|---|---|
| Baseline CBR | 1314/1821 | 1338/1821 | 1330/1821 | -0.0034 | -0.1444 | -0.0058 |
| MMR λ=0.70 | 1097/1821 | 1338/1821 | 1136/1821 | 0.0019 | -0.0027 | -0.0084 |

Las diferencias son no-default-sync menos default ponderado. La ablación muestra que el default ponderado cambia muchos rankings; debe presentarse como control, no como resultado principal, porque `Unknown synchronization` representa ausencia de información y no evidencia semántica positiva.

## Diagnóstico de pseudorreplicación

| Unidad | Únicos | % únicos | Máx. clúster | Mediana clúster |
|---|---|---|---|---|
| firma de consulta normalizada | 1684 | 92.48% | 51 | 1.0 |
| ranking baseline ordenado | 848 | 46.57% | 129 | 1.0 |
| conjunto baseline no ordenado | 697 | 38.28% | 129 | 1.0 |
| ranking MMR lambda=0.70 ordenado | 699 | 38.39% | 109 | 1.0 |
| conjunto MMR lambda=0.70 no ordenado | 578 | 31.74% | 109 | 1.0 |

## Texto publicable sugerido

En el experimento principal sin default de sincronización (V12/263 casos, 1.821 consultas, query-year 2026), el postprocesamiento MMR con λ=0,70 y top-1 fijo preservó por construcción el primer resultado y mantuvo inalterada su similitud algorítmica. La similitud media del top-5 descendió de forma pequeña, mientras que la diversidad algorítmica aumentó de forma clara: los modelos únicos por lista se aproximaron al máximo de 5,0 y la ILD media aumentó marcadamente. Este resultado debe interpretarse como redistribución algorítmica de recomendaciones, no como evidencia de mayor exactitud predictiva.

La sensibilidad sobre λ mostró el compromiso esperado entre relevancia y diversidad. Valores menores de λ incrementaron más la diversidad, con menor similitud media; valores mayores preservaron más relevancia CBR, pero redujeron la ganancia de diversidad. En todos los escenarios se preservó el top-1 por diseño.

Debe advertirse pseudorreplicación potencial: las 1.821 consultas no equivalen a 1.821 configuraciones independientes, porque muchas consultas comparten firmas normalizadas y patrones de ranking. Por ello, las pruebas pareadas describen estabilidad algorítmica sobre consultas generadas, no inferencia sobre una población independiente de problemas de mantenimiento predictivo.

El experimento sin default debe ser el análisis principal del artículo: tratar `Unknown synchronization` como evidencia por defecto puede reforzar similitudes espurias derivadas de valores desconocidos; descartarlo produce una evaluación semánticamente más conservadora y metodológicamente preferible.
