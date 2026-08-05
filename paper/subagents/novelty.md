Nota: no modifiqué archivos.

## 1) Delimitación editorial de novedad

**Novedad defendible del nuevo artículo:** no es “crear OPMAD”, ni “integrar ontologías con CBR”, ni “resolver diversidad en CBR” en abstracto. Lo verdaderamente nuevo es **operacionalizar de forma reproducible y evaluar a gran escala** una cadena completa:

**PDFs → OntoCast fijo con OPMAD → facts RDF/Turtle → CSV CBR de 19 columnas → HeadlessCBR → reranking MMR diverso**

y cuantificar, sobre **1.821 consultas derivadas de facts canónicos** de un corpus de **1.822 PDFs**, el compromiso entre similitud y diversidad.

### Qué ya estaba publicado/localmente consolidado

| Elemento | Ya aparece en | Implicación |
|---|---|---|
| Enfoque de ingeniería de sistemas para PdM y arquitectura lógica | tesis; artículos previos | No venderlo como contribución nueva. |
| OPMAD/OMSSA como vocabulario/ontología de PdM | tesis; Paper 6/7 | Citar como infraestructura reutilizada. |
| DSS ontology-enabled CBR para seleccionar modelos PdM | Paper 6; tesis | No reclamar “nuevo DSS”. |
| Integración OWL/CBR/myCBR, SPARQL/Jena/OWL API, similitud semántica | Paper 7 | No reclamar “primera integración ontología-CBR”. |
| Problema de diversidad en recomendaciones CBR | Paper 6 y tesis lo identifican; Paper_Emmannuel lo aborda | Presentarlo como motivación y punto de partida. |
| Mejora de diversidad mediante CNN/generalización de base de casos | Paper_Emmannuel | Diferenciar MMR como post-procesamiento, no mantenimiento/condensación. |

### Qué sí es nuevo

1. **Automatización reproducible** de extracción LLM/OntoCast alineada con OPMAD y compatible con el esquema CBR heredado.
2. **Adaptador headless y pipeline batch** que elimina dependencia de GUI para consultas masivas.
3. **Evaluación a gran escala**: 1.821 consultas, no 63 casos de validación ni un único caso N-CMAPSS.
4. **Diversificación MMR post-retrieval** sobre pool-15→top-5, preservando top-1, con pesos explícitos para enfoque, tipo, modelo y preprocesamiento.
5. **Evidencia cuantitativa del trade-off**: en la corrida completa, la disimilitud intra-lista sube de **0,5061 a 0,6350**, las listas con modelos repetidos bajan de **610 a 9**, los modelos únicos por lista suben de **4,63 a 5,00**, con pérdida pequeña de similitud media top-5 (**0,5563 a 0,5535**) y top-1 preservado.

---

## 2) Título recomendado

**“Automatización reproducible y diversificación de recomendaciones CBR para mantenimiento predictivo: evaluación a gran escala de OntoCast–OPMAD–CBR con MMR”**

Alternativa más narrativa:

**“Del PDF a recomendaciones diversas: una evaluación reproducible de OntoCast–OPMAD–CBR para reutilización de conocimiento en mantenimiento predictivo”**

---

## 3) Preguntas de investigación

**RQ1.** ¿Puede una cadena OntoCast→OPMAD→CBR convertir de forma reproducible un corpus amplio de artículos de mantenimiento predictivo en consultas compatibles con un DSS CBR heredado?

**RQ2.** ¿Qué cobertura y tasa de recuperación produce la cadena automatizada cuando se evalúa sobre facts canónicos disponibles?

**RQ3.** ¿En qué medida un reranking MMR incrementa la diversidad de las recomendaciones CBR sin degradar sustancialmente la similitud/relevancia?

**RQ4.** ¿Qué limitaciones aparecen al acoplar extracción LLM, vocabulario ontológico fijo y CBR heredado, especialmente en normalización semántica, calidad de facts y cobertura del espacio de soluciones?

---

## 4) Contribuciones propuestas

1. **Pipeline reproducible** para extracción fija con OPMAD, conversión RDF→CSV CBR y ejecución headless de myCBR.
2. **Esquema de interoperabilidad** entre facts OntoCast y las 19 columnas del CBR histórico.
3. **Método MMR de diversificación post-retrieval**, independiente de modificar la base de casos, con preservación del top-1.
4. **Evaluación empírica a escala de corpus**: 1.821 consultas, métricas de similitud, diversidad, duplicación y cobertura.
5. **Análisis de riesgo metodológico**: normalización de vocabulario, facts con citas adicionales, diferencias entre interoperabilidad técnica y validez semántica.

---

## 5) Estructura IMRyD sugerida

### Introducción
- Problema: los DSS CBR para PdM ayudan a la creatividad estructurada, pero sufren duplicación/homogeneidad en top-k.
- Brecha: trabajos previos demostraron viabilidad del CBR ontológico, pero no automatizaron extracción masiva ni evaluaron diversidad a gran escala.
- Posicionamiento: se reutiliza OPMAD/CBR; la novedad está en automatización + evaluación + MMR.

### Métodos
1. **Materiales**
   - Corpus: 1.822 PDFs en `extraction_papers`.
   - Facts canónicos: 1.821.
   - CBR heredado: base myCBR/OPMAD, esquema de 19 columnas.
2. **Pipeline**
   - OntoCast fijo con OPMAD seed.
   - Limpieza de RDF-star para `rdflib`.
   - Conversión `facts_to_csv.py`.
   - Normalización de consultas al vocabulario CBR.
3. **Baseline**
   - HeadlessCBR top-5 por similitud.
4. **MMR**
   - Pool-15, top-5, λ=0,70.
   - Preservación de top-1.
   - Dissimilarity de soluciones por approach, model type, models, preprocessing.
5. **Métricas**
   - consultas con resultados, similitud top-1, similitud media top-5, modelos únicos, listas con duplicados, disimilitud intra-lista, cambio de orden/conjunto.

### Resultados
- Cobertura: 1.821/1.822 PDFs con facts canónicos.
- Recuperación: 1.821/1.821 consultas con resultados.
- Diversidad:
  - modelos únicos: 4,63→5,00;
  - duplicados: 610→9;
  - disimilitud: 0,5061→0,6350.
- Relevancia:
  - top-1 preservado 1.821/1.821;
  - similitud media top-5 baja solo 0,0028.

### Discusión
- La automatización materializa una perspectiva planteada como futuro en la tesis/Paper 6.
- MMR ataca el síntoma de diversidad sin alterar la base de casos, a diferencia del enfoque CNN de Paper_Emmannuel.
- La pérdida mínima de similitud sugiere que existe redundancia explotable en el pool-15.
- La evaluación es técnica y de ranking, no aún una validación humana de utilidad arquitectónica.
- La calidad semántica de facts y normalización debe auditarse antes de retener nuevos casos en la base.

---

## 6) Riesgo de “salami publication” y mitigación

**Riesgo alto** si el artículo se formula como:
- “nuevo DSS ontology-enabled CBR para PdM”;
- “nueva integración OPMAD-CBR”;
- “primera solución al problema de diversidad CBR en PdM”.

Eso solapa con Paper 6, Paper 7, tesis y Paper_Emmannuel.

**Riesgo bajo/moderado** si se formula como:
- estudio posterior que **automatiza y escala** la infraestructura previa;
- evaluación computacional reproducible;
- comparación baseline vs MMR;
- complemento a CNN/diversity maintenance, no sustituto.

### Cómo citar y diferenciar

- Citar **Paper 6** como origen del DSS OPMAD-CBR y de la identificación del problema de diversidad.
- Citar **Paper 7** como detalle de integración ontología–myCBR y similitud semántica.
- Citar la **tesis** como marco global: ingeniería de sistemas, OPMAD, validación N-CMAPSS y futuras líneas.
- Citar **Paper_Emmannuel** como trabajo local/complementario sobre diversidad mediante CNN/generalización, dejando claro que el presente estudio usa **MMR post-retrieval**, no condensación de la base.
- Citar **OntoCast** y **MMR** como tecnologías externas reutilizadas/adaptadas.

**Frase de diferenciación sugerida:**  
“Este trabajo no propone una nueva ontología ni un nuevo DSS CBR; extiende la línea OPMAD-CBR mediante una cadena reproducible de extracción y consulta a gran escala, y evalúa un mecanismo de diversificación MMR post-retrieval sobre recomendaciones generadas automáticamente.”
