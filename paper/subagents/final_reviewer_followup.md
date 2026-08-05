No edité archivos.

## Dictamen final

**No enviar todavía.** La revisión corrigió la mayoría de los problemas críticos anteriores: `Unknown synchronization` ya no entra como evidencia en el análisis principal; la cobertura 1.822/1.821 está bien formulada; se reportan ablación, deduplicación exacta y azar; se delimita chunks/primer caso; se añadió comparación conceptual con CNN; y PDF/DOI/cross-references/floats están esencialmente corregidos.

Pero quedan **errores corregibles que sí impiden envío**.

## Errores aún bloqueantes

1. **Inconsistencias numéricas internas en sensibilidad**
   - `paper/main.tex:304` y PDF p. 7 dicen: “Entre 0,5 y 0,7 se obtuvieron cinco firmas distintas en todas las listas” y que al elevar λ “reaparecieron 10 y 21 listas”.
   - Pero la Tabla 3 y `paper/supplement/statistics/sensitivity_lambda_overview.csv` dicen:
     - λ=0,7: **5** listas repetidas, no “todas distintas”.
     - λ=0,8: **14** repetidas, no 10.
     - λ=0,9: **25** repetidas, no 21.
   - Esto debe corregirse antes de enviar.

2. **Inconsistencia numérica en pseudorreplicación**
   - `paper/main.tex:424` y PDF p. 10 dicen: **815** rankings baseline y **655** rankings MMR ordenados.
   - El suplemento actual (`pseudoreplication_diagnostics.csv`) reporta:
     - ranking baseline ordenado: **848**
     - ranking MMR λ=0,70 ordenado: **699**
   - Es una contradicción directa entre manuscrito y suplemento.

3. **Reproducibilidad suplementaria incompleta si `paper/supplement` es el paquete de envío**
   - El manuscrito afirma que identificadores/manifiestos permiten reconstruir el corpus, pero el suplemento incluido no contiene un manifiesto por documento con PDF/hash/facts/modelo real/chunks/reintentos/sanitización.
   - `queries.csv` da rutas de facts, pero no basta como manifiesto de extracción/corpus.
   - Corregible: añadir ese manifiesto o rebajar la afirmación de reproducibilidad.

## Verificaciones positivas

- Recalculé desde `.build/diversity_comparison_1821_v12_no_default_sync`:  
  similitud top-1 0,5630; similitud top-5 0,5563→0,5536; ILD 0,4216→0,5265; firmas 4,6332→4,9973; repetidas 610→5; top-1 preservado 1.821/1.821.
- `query_batch_input_*`: `Online/Offline` y `w4` están vacíos en 1.821/1.821.
- Cobertura: 1.822 PDF, 1.821 hashes únicos, 1 duplicado exacto, 1.821 facts, 0 documentos únicos sin facts.
- PDF: segundo abstract, referencias cruzadas en español, float del apéndice y DOI de OntoCast están corregidos.

## Limitaciones que son trabajo futuro, no errores corregibles inmediatos

- No hay validación experta de fidelidad semántica de extracción.
- ILD sigue alineada con la función optimizada por MMR.
- No hay comparación experimental MMR vs CNN.
- La selección del primer caso en TTL multi-caso sigue siendo una decisión débil, aunque ahora declarada.

**Conclusión:** tras corregir las inconsistencias numéricas y completar/ajustar la reproducibilidad suplementaria, el manuscrito sería enviable como estudio de interoperabilidad y reranking, no como validación semántica de extracción ni utilidad de recomendación.
