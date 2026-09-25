No edité archivos. Hallazgo principal: los artefactos suplementarios contienen resultados suficientes, pero `paper/main copy.tex` no tiene sección de Resultados/Discusión; los resultados aparecen casi sólo en el resumen. Así, el cuerpo del paper está incompleto.

## 1) Métricas principales que sí deberían reportarse en el cuerpo

**Corpus y cobertura**
- Scopus: 3.990 registros; incluidos: 2.768; excluidos: 1.222.
- PDF recuperados: 1.822 archivos; 1.821 documentos únicos; 946 incluidos sin PDF.
- Facts/consultas: 1.821/1.821 artefactos y consultas ejecutables.
- Base CBR: 263 casos; top-k=5; pool=15; λ=0,70; taxonomía de diversidad: 131 términos.
- Sesgo de disponibilidad: recuperación PDF 2025 = 69,7%; 2026 = 58,2%; gold OA = 74,2%, hybrid_gold = 33,3%.

**Auditoría RDF/CBR**
- 1.821 artefactos parseables sólo tras limpieza RDF-star.
- Se retiraron 311.559 bloques de reificación RDF-star.
- 409 artefactos tenían más de un caso; se ignoraron 567 casos adicionales.
- SHACL mínimo: sólo 126/1.821 conformes, 6,9%.
- Cobertura informativa de campos clave:
  - Task: 1.727/1.821 = 94,8%.
  - Case study: 1.544/1.821 = 84,8%.
  - Input type: 1.301/1.821 = 71,4%.
  - Models: 1.395/1.821 = 76,6%.
  - Online/Off-line, failure modes, performance indicator, performance: 0%.
- Campos activos en consulta normalizada:
  - task: 100%.
  - case study: 85,1%.
  - input type: 75,8%.
  - case study type, online/offline, input_for_model: 0%.

**Resultado principal CBR vs MMR**
Debe ir como tabla central:

| Métrica | CBR | CBR+MMR λ=0,70 | Δ |
|---|---:|---:|---:|
| Similitud top-1 | 0,5630 | 0,5630 | 0,0000, por diseño |
| Similitud media top-5 | 0,5563 | 0,5536 | -0,0027; IC95% [-0,0029, -0,0025]; -0,48% |
| Modelos únicos top-5 | 4,6332 | 4,9973 | +0,3641 |
| Listas con modelos repetidos | 610 | 5 | -605 |
| ILD algorítmica | 0,4216 | 0,5265 | +0,1049; IC95% [0,1013, 0,1087]; +24,9% |

También:
- Cambió el orden en 1.821/1.821 consultas.
- Cambió el conjunto top-5 en 1.819/1.821.
- Top-1 preservado en 1.821/1.821, por construcción.
- ILD aumentó en 1.707 consultas, bajó en 112 y empató en 2.
- Similitud media top-5 bajó en 1.193 consultas, empató en 628 y no subió en ninguna.

**Sensibilidad**
- λ=0,5: similitud 0,5522; ILD 0,5295; repetidos 0.
- λ=0,9: similitud 0,5549; ILD 0,5201; repetidos 25.
- Pool 10/15/20/30: ILD 0,5037 / 0,5265 / 0,5614 / 0,5774, con similitud 0,5546 / 0,5536 / 0,5527 / 0,5517.

**Comparadores**
- Exact dedup: similitud 0,5557; ILD 0,4373; repetidos 0.
- MMR λ=0,70: similitud 0,5536; ILD 0,5265; repetidos 5.
- Greedy max-sum: similitud 0,5542; ILD 0,5408.
- MAP-DPP léxico: similitud 0,5540; ILD 0,4981.

## 2) Riesgos

**Circularidad**
- La ILD usa la misma similitud de solución que optimiza MMR. Por tanto, la mejora de ILD no es validación independiente.
- “Modelos únicos” también está alineado con el objetivo, porque la similitud de solución da peso 0,40 a nombres de modelos.
- Debe decirse “aumenta una métrica algorítmica alineada con MMR”, no “mejora la calidad de recomendación”.

**Pseudo-replicación**
- Hay 1.821 consultas, pero sólo:
  - 1.684 firmas normalizadas únicas.
  - 848 rankings baseline ordenados únicos.
  - 699 rankings MMR únicos.
  - 697 conjuntos baseline únicos.
  - 578 conjuntos MMR únicos.
- Máximo clúster: 129 rankings baseline repetidos; 109 rankings MMR repetidos.
- Los p-valores extremos no deben presentarse como inferencia poblacional fuerte.

**Defaults**
- `Unknown synchronization` se descartó correctamente en el análisis principal.
- La ablación con default ponderado cambia bastante los rankings:
  - baseline rankings iguales sólo 1.314/1.821;
  - MMR rankings iguales sólo 1.097/1.821.
- Muchos campos son defaults o genéricos: sincronización 100% default, performance 100% ausente, case study type 100% “Maintainable item”.

**Top-1 fijo**
- La similitud top-1 igual no es resultado empírico: está impuesta.
- Debe reportarse la pérdida en posiciones 2–5: similitud media baja de 0,5546 a 0,5513, Δ=-0,0033.

**Case base pequeña**
- 263 casos históricos para 1.821 consultas.
- Baseline usa 174/263 casos al menos una vez; MMR usa 185/263.
- El top-10 de casos más frecuentes concentra ~29,4% de selecciones baseline y ~32,5% con MMR.
- Riesgo de rankings repetidos y dependencia fuerte de pocos casos históricos.

## 3) Análisis adicionales que exigiría un revisor

1. Validación humana real de fidelidad factual: precisión/recall/F1 por campo, acuerdo entre anotadores y adjudicación.
2. Evaluación de utilidad o relevancia de recomendaciones: jueces expertos, Precision@k, nDCG@k o preferencia pareada.
3. Métricas de diversidad independientes de la función MMR.
4. Análisis por clúster como principal, no sólo por consulta.
5. Ablaciones por calidad de consulta: task-only, task+asset, task+asset+input_type.
6. Ablación sin top-1 fijo con conteo de top-1 cambiado.
7. Sensibilidad a pesos de similitud de solución como resultado explícito.
8. Análisis de sesgo por disponibilidad PDF y por modelo extractor.
9. Reportar estratos pequeños sólo descriptivamente: Health modelling n=8; Multiple steps forecast n=6.
10. Comparar contra extracción JSON/LLM sólo cuando exista gold standard humano.

## 4) Tablas/figuras faltan o sobran

**Faltan en `paper/main copy.tex`**
- Sección `Resultados`.
- Tabla principal desde `paired_metric_summary.csv`.
- Tabla de cobertura/defaults desde `field_coverage_19cols.csv`.
- Tabla SHACL desde `shacl_validation_summary.csv`.
- Tabla de sensibilidad λ desde `sensitivity_lambda_overview.csv`.
- Tabla de comparadores desde `strong_reranking_comparators.csv`.
- Tabla/nota de pseudo-replicación desde `pseudoreplication_diagnostics.csv`.
- Figuras ya generadas pero no insertadas:
  - `paper/figures/metricas_globales.*`
  - `paper/figures/distribucion_cambios.*`
  - `paper/figures/sensibilidad_lambda.*`
  - `paper/figures/sensibilidad_pool.*`
  - `paper/figures/cobertura_campos.*`
  - `paper/figures/delta_ild_por_tarea.*`

**Sobran o deben relegarse**
- P-valores Wilcoxon extremos en el cuerpo; mejor IC y tamaños de efecto, con advertencia de dependencia.
- `DIVERSITY_COMPARISON_RESULTS.md` parece obsoleto: reporta 599 consultas, no 1.821. No debe citarse como resultado vigente.
- La similitud top-1 como “resultado” debe ser sólo control de diseño.

## 5) Lenguaje que debe suavizarse

Cambios recomendados:

- En vez de “MMR mejora la diversidad”, usar:  
  **“MMR incrementó la diversidad algorítmica medida por ILD, una métrica alineada con el criterio optimizado.”**

- En vez de “confirmaron”, usar:  
  **“los comparadores fueron consistentes con la dependencia del resultado respecto del criterio de diversidad.”**

- En vez de “1.821 consultas independientes”, usar:  
  **“1.821 consultas derivadas de documentos, con patrones de ranking repetidos.”**

- En vez de “sin pérdida de relevancia”, usar:  
  **“con preservación top-1 por diseño y una reducción pequeña de similitud media top-5.”**

- En vez de “artefactos conformes/auditables”, usar:  
  **“artefactos parseables tras limpieza y consultas ejecutables; la conformidad SHACL mínima fue limitada.”**

- En vez de “evidencia de utilidad decisional”, usar:  
  **“evidencia de comportamiento algorítmico downstream; la utilidad decisional requiere validación experta.”**
