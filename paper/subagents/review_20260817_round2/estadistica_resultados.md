No edité archivos.

## 1) Verificación de números principales

En general, **no detecto errores numéricos mayores** frente a los CSV/JSON revisados.

- **Corpus/pipeline:** 1.822 PDF, 1.821 documentos únicos, 1.821 facts/consultas, 1 duplicado, 263 casos CBR, pool 15, top-5, $\lambda=0{,}70$, año 2026 y top-1 preservado: coincide con `summary.json`.
- **Resultados principales:** coinciden con `summary.json` y `paired_metric_summary.csv`:
  - Similitud top-1: 0,5630 → 0,5630.
  - Similitud media top-5: 0,5563 → 0,5536; cambio −0,0027 / −0,48%.
  - Firmas únicas: 4,6332 → 4,9973.
  - Listas con firmas repetidas: 610 → 5.
  - ILD: 0,4216 → 0,5265; cambio 0,1049 / 24,89%.
  - Cambios ILD: 1.707 aumentan, 112 disminuyen, 2 empatan.
- **IC y pseudo-replicación:** los IC por consulta de la tabla principal coinciden; también coincide el IC por clúster baseline para ILD [0,0873; 0,1226] y para similitud [−0,0033; −0,0021] en `cluster_bootstrap.csv`.
- **Diagnóstico de pseudo-replicación:** 1.684 firmas normalizadas, 848 rankings baseline, 699 rankings MMR; clústeres máximos 129 y 109: coincide con `pseudoreplication_diagnostics.csv`.
- **Sensibilidad a $\lambda$:** la tabla del manuscrito coincide con `sensitivity_lambda_overview.csv`.
- **Comparadores fuertes:** deduplicación, MMR, max-sum y MAP-DPP coinciden con `strong_reranking_comparators.csv`.
- **Ablaciones de atributos/año:** coinciden con `cbr_attribute_year_ablations.csv`, incluido el colapso a 8 rankings con tarea+año, 16 con tarea+variables, 270 consultas sin top-5 al quitar tarea, y el efecto del año 2021.
- **Sensibilidad extendida:** los valores citados de pool 10→30, pesos alternativos y sin restricción top-1 coinciden con `extended_mmr_sensitivity.csv`.

## 2) Errores, inconsistencias u omisiones estadísticas restantes

- **La tabla principal usa IC por consulta**, aunque la pseudo-replicación es sustancial. El texto menciona los IC por clúster, pero como lector estadístico esperaría que el IC conservador por clúster fuera el principal o apareciera en la misma tabla.
- **El estrato “One step future state forecast” está contaminado por defaults.** Hay 94 tareas predeterminadas y esa categoría tiene n=136; por tanto, la interpretación por tarea debe separar “tarea inferida/extraída” de “tarea por defecto”.
- **Año de publicación vs año de consulta:** el apéndice habla de `Publication Year` con default 2021, pero la recuperación usa `query_year=2026` fijo. Debe aclararse que el “año” en la consulta no es el año extraído del artículo.
- **Activos en query > informativos:** `Case study` e `Input type` tienen más casos activos que informativos en la tabla. No es necesariamente error, pero requiere nota explicativa.
- **Modelos extraídos vs firmas de solución:** conviene aclarar que la diversidad MMR usa las firmas de modelos de los casos recomendados de la base CBR, no necesariamente los modelos extraídos del artículo-consulta.
- **Wilcoxon vs bootstrap en tareas:** para “One step” se reporta p=0,504, pero la media bootstrap de ILD es positiva. Debe explicarse que Wilcoxon evalúa otro estimando/hipótesis, no contradecirlo.
- **Falta una sensibilidad por calidad estructural:** sería útil reportar resultados separados para SHACL conforme vs no conforme, y para artefactos con múltiples casos vs un solo caso.

## 3) Tablas/figuras

Son suficientes para sostener la historia principal, pero ajustaría:

- `tab:main-results`: añadir IC95% por clúster o sustituir los IC por consulta.
- `tab:sensitivity`: incluir también $\lambda=0$ y $\lambda=1$, ya que se discuten en el texto.
- `tab:coverage`: añadir nota sobre defaults activos, especialmente tarea.
- Figura por tarea: marcar estratos pequeños y el estrato con tareas por defecto.
- Tabla de comparadores: añadir diferencias frente a CBR y, si es posible, IC pareados/bootstrap.

## 4) Lenguaje estadístico a corregir

- Cambiar “1.707 consultas mejoraron” por “1.707 consultas aumentaron su ILD”; no implica mejora de utilidad.
- “Pérdida mínima/pequeña” → “pérdida absoluta de −0,0027 en la escala CBR; importancia práctica no calibrada”.
- “El bootstrap por clúster evitó…” → mejor “mitigó” o “redujo la sensibilidad a rankings duplicados”.
- En tareas, usar “exploratorio” y evitar interpretar p-valores como inferencia poblacional.
- Cuando se diga “ganador”, “mayor” o “preferible”, especificar “bajo esta métrica y este pool”.

## 5) Recomendaciones concretas

1. Hacer que los **IC por clúster sean el reporte principal** en la tabla de resultados.
2. Añadir una sensibilidad excluyendo o neutralizando las **94 consultas con tarea por defecto**.
3. Separar el análisis de “One step forecast” en extraído vs default.
4. Aclarar explícitamente que el **top-1 está fijado por diseño** también en resumen/resultados.
5. Incluir $\lambda=0$ y $\lambda=1$ en la tabla de sensibilidad.
6. Añadir nota de que ILD está alineada con la función objetivo de MMR.
7. Reportar, aunque sea en suplemento, resultados por SHACL conforme/no conforme y multi-caso/single-caso.
