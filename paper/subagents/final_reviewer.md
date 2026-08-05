No edité ningún archivo.

## Dictamen

**Revisión mayor** — cercano a rechazo si se presenta como artículo Q1 sin experimentos adicionales.  
El manuscrito tiene un núcleo publicable: integración reproducible OntoCast–OPMAD–CBR–MMR, uso correcto de V12/263 casos y cifras globales verificables. Pero el estudio aún demuestra sobre todo **interoperabilidad sintáctica y comportamiento de un reranker circularmente evaluado**, no calidad semántica de extracción ni utilidad de recomendación. Para una revista Q1, la evidencia actual es insuficiente sin validación humana/experta, mejor control de consultas y una comparación más fuerte frente a alternativas.

## Verificación numérica y técnica realizada

- Recomputé desde `.build/diversity_comparison_1821_v12_corrected/per_query.csv`:
  - similitud top-1: **0,5811109 → 0,5811109**
  - similitud media top-5: **0,5596766 → 0,5517569**, Δ **−0,0079196**
  - ILD: **0,4273207 → 0,5348839**, Δ **0,1075632**
  - firmas únicas: **4,7776 → 5,0000**
  - cambio de conjunto: **1819/1821**, top-1 preservado **1821/1821**
- Verifiqué `queries.csv`:
  - `normalized_task`: 1821/1821
  - `normalized_case_study_type`: 0/1821
  - `normalized_case_study`: 1549/1821
  - `normalized_input_for_model`: 0/1821
  - `normalized_input_type`: 1381/1821
  - `normalized_online_offline`: 1821/1821, pero constante: `Unknown synchronization`
- Verifiqué PDFs: **1822 archivos**, **1821 hashes únicos**. El duplicado exacto es:
  - `paper-0333_a_machine_learning_framework_for_long_term_forecasting_of_spare_part_demand_in_end_of_life_p.pdf`
  - `paper-1272_a_machine_learning_framework_for_long_term_forecasting_of_spare_part_demand_in_end_of_life_p.pdf`
- Verifiqué V12/proyecto:
  - `CleanedDATA V12-05-2021.csv`: **263 filas**
  - `PredictMaint_myCBR.prj`: **263 casos** dentro del zip
  - `CleanedDATA V21-07-2021.csv`: **200 filas**, no corresponde al experimento corregido.
- Parseé los 1821 TTL con `load_graph_from_ttl`: todos parsean tras cleanup RDF-star, aunque `rdflib` emite avisos de literales mal tipados.
- Verifiqué DOIs principales vía `doi.org`: no encontré referencias inventadas. Pero la referencia de OntoCast no imprime DOI/URL en el PDF.

## Problemas mayores priorizados

### 1. La validez semántica de la extracción sigue sin demostrarse

El artículo dice correctamente que no valida fidelidad semántica, pero esa ausencia afecta el centro del manuscrito. Si las consultas derivadas de los PDFs son ruidosas, parciales o por defecto, entonces el experimento MMR mide diversidad de rankings generados por entradas débiles, no reutilización fiable de conocimiento científico.

Además, la extracción usa `--head-chunks 3` en las corridas principales y `--head-chunks 1` en reintentos finales. Por tanto, el título y varias frases “PDF → recomendaciones” pueden sugerir lectura completa del artículo cuando en realidad se procesaron chunks iniciales.

**Necesario para Q1:** muestra estratificada anotada por expertos con precisión/recobrado por campo, al menos para tarea, activo, variables, modelos, sincronización, desempeño e identificador.

### 2. Las consultas CBR explotan pocos campos y un campo por defecto entra como evidencia

La normalización descarta completamente tipo de activo e input-for-model. La sincronización queda como `Unknown synchronization` en todas las consultas y, en `query_batch_input_topk.csv`, entra con `w4=1`. Esto no es ausencia de evidencia: es un valor constante ponderado en la similitud. Solo un caso histórico V12 tiene `Unknown synchronization`, por lo que este default puede sesgar rankings.

También hay 409 artefactos con más de un caso extraído y 567 casos adicionales descartados. El código toma “el primer caso determinista”; no demuestra que ese primer caso sea siempre el artículo fuente y no una publicación citada.

**Necesario:** repetir o añadir ablation con defaults vacíos/no ponderados, reportar impacto, y justificar la selección del caso fuente con un identificador explícito.

### 3. Métrica ILD circular y ausencia de validación independiente

El manuscrito reconoce que ILD comparte `s_sol` con MMR. Eso es honesto, pero deja el resultado principal como esperado por construcción. La eliminación de firmas repetidas también depende de una representación textual/taxonómica ad hoc de `Models`.

**Necesario:** añadir métricas independientes: diversidad por familias expertas de modelos, cobertura de enfoques, novedad percibida o evaluación humana de utilidad/relevancia. También comparar MMR contra baselines simples: eliminar duplicados de firma, reranking aleatorio desde pool-15, greedy por modelo único, MMR sin top-1 fijo.

### 4. Novedad defendible, pero estrecha frente a Paper 6, Paper 7 y Emmanuel

El manuscrito ya delimita bien que no propone OPMAD, ni myCBR, ni MMR. Aun así, para Q1 la novedad queda principalmente en ingeniería reproducible y evaluación a escala. Frente a Emmanuel, falta una comparación experimental o al menos una discusión cuantitativa más directa: CNN modifica/condensa memoria; MMR postprocesa rankings. Son complementarios, pero el lector esperará evidencia de cuándo conviene cada uno.

**Necesario:** comparación controlada MMR vs CNN si el código/datos lo permiten, o tabla conceptual rigurosa con supuestos, costos, efectos y limitaciones.

### 5. Confusión 1822/1821 en artefactos suplementarios

El manuscrito afirma correctamente que 1822 PDFs corresponden a 1821 documentos únicos por duplicado exacto. Pero `.build/.../summary.json` y `REPORT.md` dicen `pdfs_without_facts_estimate: 1` / “PDFs aún sin facts canónicos: 1”. Eso contradice la explicación del manuscrito.

**Corrección obligatoria:** cambiar la metadata y el reporte para distinguir “archivo PDF duplicado” de “PDF sin facts”. Incluir los dos nombres de archivo duplicados o sus hashes.

### 6. Reproducibilidad incompleta de modelos/chunks

La distribución 599/500/722 por modelo es plausible y coincide con los runs, pero no está suficientemente empaquetada como manifest publicable por documento. En particular, el run de 500 usa config con `LLM_MODEL_NAME=gpt-5-mini`, aunque el proxy log indica `gpt-5.4-mini`.

**Necesario:** manifest una fila por documento: PDF, hash, facts file, run, modelo real, proxy, chunks, reintentos, sanitización, fecha, estado parseo.

## Problemas menores

- En el PDF, las referencias cruzadas aparecen en inglés: “figure”, “table”, “equation”. Deben ser “figura”, “tabla”, “ecuación”.
- El segundo resumen aparece con encabezado **“Resumen”** y luego “Abstract.” en línea. Es un fallo visible.
- La Tabla 4 del apéndice flota dentro de la sección de referencias. Debe fijarse antes de `\bibliography` o forzar barrera de floats.
- Figura 3 tiene etiquetas de IC95% muy pequeñas/superpuestas; visualmente no es publicable.
- La cita de OntoCast aparece como “Alexander Belikov. Ontocast, 2025.” sin DOI/URL en la bibliografía, aunque el DOI existe.
- El caption “n = 1,821” usa coma en modo inglés; en español debe evitar ambigüedad con decimal.
- La tabla ejemplo debería indicar `query_index=1191` y/o facts file para trazabilidad.
- Reducir anglicismos no necesarios: “rerankeado”, “baseline”, “chunks”, “pool”, o definirlos consistentemente.

## Correcciones textuales concretas sugeridas

- Título/abstract:
  - Cambiar “PDF → OntoCast…” por “PDFs procesados en chunks iniciales → OntoCast…”, salvo que se procese texto completo.
- Resumen:
  - Añadir: “La ILD se calculó con la misma similitud de solución usada por MMR.”
- Corpus:
  - Reemplazar “PDFs sin facts” por “un archivo PDF duplicado exacto; no hubo documento único sin facts canónico”.
- Métodos, puente:
  - Añadir: “`Unknown synchronization` se envió como valor no vacío en esta corrida; se evalúa en amenazas porque puede actuar como evidencia por defecto.”
- Resultados:
  - Matizar “100% de cobertura” como “100% de ejecución técnica de consultas”, no cobertura semántica.
- Conclusiones:
  - Cambiar “cadena reproducible” por “cadena reproducible sobre artefactos canónicos preservados”; la extracción LLM original no es determinista.

## Checklist antes de envío

1. Añadir gold standard experto estratificado y métricas de extracción.
2. Repetir análisis con defaults no ponderados, especialmente sincronización.
3. Corregir metadata 1822/1821 y manifest PDF→facts.
4. Incluir manifest por modelo/chunks/reintentos.
5. Añadir comparación o discusión fuerte frente a Emmanuel/CNN.
6. Añadir métricas de diversidad independientes de `s_sol`.
7. Corregir cross-references, segundo abstract, floats y figuras.
8. Asegurar que OntoCast tenga DOI/URL visible.
9. Archivar código/datos con DOI y hashes.
10. Eliminar o degradar p-valores inferenciales; mantenerlos como descriptivos por pseudorreplicación.
