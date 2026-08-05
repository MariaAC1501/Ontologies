# Sensibilidad extendida del reranking

La ILD de todas las condiciones se recalculó con los pesos principales 0,20/0,25/0,40/0,15 para conservar comparabilidad.

## Tamaño del pool (top-5, lambda=0,70, top-1 fijo)

| Pool | Similitud media | ILD | Firmas únicas | Listas repetidas |
|---:|---:|---:|---:|---:|
| 10 | 0.5546 | 0.5037 | 4.994 | 11 |
| 15 | 0.5536 | 0.5265 | 4.997 | 5 |
| 20 | 0.5527 | 0.5614 | 4.999 | 1 |
| 30 | 0.5517 | 0.5774 | 4.999 | 1 |

## Comparadores fuertes

| Método | Similitud | ILD principal | Firmas | Tipos | Enfoques | Listas repetidas |
|---|---:|---:|---:|---:|---:|---:|
| CBR top-5 | 0.5563 | 0.4216 | 4.633 | 2.416 | 1.607 | 610 |
| Exact signature dedup | 0.5557 | 0.4373 | 5.000 | 2.544 | 1.645 | 0 |
| MMR lambda=0.70 | 0.5536 | 0.5265 | 4.997 | 2.881 | 1.896 | 5 |
| Greedy max-sum lambda=0.70 | 0.5542 | 0.5408 | 4.980 | 2.789 | 1.900 | 35 |
| Lexical MAP-DPP | 0.5540 | 0.4981 | 5.000 | 3.091 | 1.890 | 0 |

xQuAD no se ejecutó porque el corpus no define intenciones/subtópicos por consulta. Una comparación CNN requiere modificar/reconstruir la memoria CBR y no es un reranker sobre el mismo pool; queda separada conceptualmente.
