# Revisión metodológica crítica

Basado en el texto extraído de `paper/main.pdf`. No he editado archivos.

## 1. Lectura técnica resumida del pipeline

El manuscrito propone una cadena:

`PDF → OntoCast condicionado por OPMAD → hechos RDF/Turtle → limpieza RDF-star → puente RDF–CBR de 19 campos → consulta headless myCBR → pool top-15 → reranking MMR top-5`.

La unidad experimental es cada PDF único: 1.821 documentos. Cada artefacto RDF genera una consulta contra una base histórica myCBR de 263 casos. Se compara el top-5 original por similitud CBR con un top-5 rerankeado por MMR, preservando siempre el primer resultado. La métrica principal de diversidad es la disimilitud intra-lista calculada con la misma similitud de solución que usa MMR.

Mi lectura: el diseño sí demuestra una **interoperabilidad operativa estrecha** —los artefactos pasan por el puente y producen rankings—, pero no demuestra todavía una **interoperabilidad semántica robusta** ni una reproducibilidad plena de extracción. La propia conclusión es prudente al negar fidelidad semántica y utilidad de usuario; aun así, el término “interoperabilidad reproducible” queda algo sobredimensionado si no se publican artefactos canónicos completos, validaciones SHACL/procedencia y evidencia de que los campos CBR no están dominados por defaults o pérdidas de normalización.

---

## 2. Crítica por subsección de Métodos

### 3.1. Diseño del estudio

**Fortalezas**

- Diseño pareado correcto para aislar el efecto del reranking: misma consulta, mismo pool candidato, dos condiciones.
- Buena delimitación: no se evalúa diagnóstico real ni entrenamiento predictivo.
- La preservación del top-1 se declara como restricción de diseño.

**Objeción probable de revisor**

> “El estudio mide que el software corre, no que las recomendaciones sean técnicamente válidas.”

Es cierto. La unidad de análisis es un artefacto generado automáticamente, no un caso verificado. La tasa del 100 % de consultas con resultado prueba ausencia de fallos de ejecución, pero no pertinencia de las recomendaciones.

**Cómo resolverlo**

- Separar explícitamente tres niveles: interoperabilidad sintáctica, interoperabilidad semántica y utilidad decisional.
- Añadir al menos una muestra dorada anotada por expertos para medir precisión/exhaustividad de extracción y corrección de la consulta CBR.
- Reportar umbrales de “consulta informativa” frente a “consulta vacía/default”.

---

### 3.2. Corpus y cribado

**Fortalezas**

- Flujo cuantitativo claro: 3.990 registros, 2.768 incluidos, 1.822 PDF, 1.821 únicos.
- Se reconoce el sesgo por 946 incluidos sin PDF accesible.
- Hay separación temporal respecto de la base histórica.

**Problemas**

- El corpus depende de Scopus, acceso institucional y disponibilidad legal de PDF. Sin export completo y decisiones por registro, la reproducción externa será difícil.
- La selección de solo artículos en inglés y 2025–2026 limita generalización.
- La ausencia de 946 textos completos no es menor: representa una porción suficientemente grande como para sesgar dominios, editoriales, activos o métodos.
- No queda claro si hubo duplicados semánticos, versiones preprint/artículo o artículos con contenido casi idéntico además del duplicado exacto.

**Objeción probable**

> “El corpus reproducible no es el corpus real, porque no puedo reconstruir qué PDFs fueron usados.”

**Resolución**

Publicar un manifiesto con DOI/EID/título, decisión de cribado, razón de exclusión, hash del PDF cuando sea posible, hash del texto extraído, estado de acceso y vínculo exacto PDF→facts. Los 25 enlaces no exactos mencionados deben auditarse manualmente o excluirse de análisis principal.

---

### 3.3. Extracción OPMAD/OntoCast

**Fortalezas**

- Ontología fija, sin evolución, reduce variabilidad.
- Se documentan trabajadores, reintentos, chunks y modelos usados.
- Se reconoce explícitamente la deriva de modelos LLM.

**Problemas serios**

- La extracción usa “hasta tres chunks iniciales”. Para artículos técnicos, los modelos, métricas, datasets, preprocesamiento y resultados suelen aparecer en métodos/resultados, no necesariamente al inicio. Esto amenaza la completitud de los 19 campos.
- Se usaron tres modelos LLM distintos: 599, 500 y 722 artefactos. Eso introduce un factor experimental no controlado.
- El piloto de diez documentos juzgado por otro LLM no valida calidad.
- La limpieza elimina sentencias RDF-star y, con ellas, procedencia a nivel de triple. Eso contradice parcialmente la ambición de trazabilidad.
- “Parseable after cleanup” no equivale a RDF correcto respecto de OPMAD.

**Objeción probable**

> “La variación de modelos y la pérdida de RDF-star hacen imposible saber si las diferencias provienen del corpus, del extractor o del postproceso.”

**Resolución**

- Congelar y publicar artefactos canónicos.
- Añadir validación SHACL/OWL y reporte de violaciones.
- Medir extracción en muestra estratificada con expertos.
- Conservar la procedencia RDF-star transformándola a reificación RDF 1.1 o named graphs, no eliminarla.
- Repetir una submuestra con un único modelo y comparar estabilidad.

---

### 3.4. Puente RDF–CBR y normalización

**Fortalezas**

- El puente determinista es el componente metodológico más valioso.
- El esquema de 19 campos y el uso de Pydantic son buenas prácticas.
- Se reconoce que compatibilidad sintáctica no implica completitud semántica.

**Problemas críticos**

- En 409 artefactos con más de un caso se elige el primero por orden determinista de IRI. Eso es reproducible, pero no necesariamente correcto.
- El tipo de activo y la modalidad de entrada se descartaron en todas las consultas por incompatibilidad léxica. Esto reduce drásticamente la interoperabilidad semántica.
- `Unknown synchronization` fue generado en todas y luego tratado como ausente. Bien como control, pero evidencia que el campo no se extrajo.
- Algunos numéricos heredados usan cero. Un cero puede confundirse con valor real.
- Si muchos campos se pierden o son defaults, la consulta puede quedar dominada por tarea, año, activo libre y variables.

**Objeción probable**

> “El puente parece compatible porque rellena campos, pero en realidad descarta o inventa información.”

**Resolución**

- Distinguir `missing`, `not reported`, `not applicable`, `unknown` y valores numéricos reales.
- No usar cero como default semántico.
- Publicar estadísticas por campo: cobertura, fuente RDF, regla de normalización, tasa de descarte.
- Sustituir “primer caso por IRI” por una regla basada en evidencia: artículo fuente, título, DOI, rol `Study`, centralidad o score de confianza.
- Añadir una capa de alineamiento léxico/ontológico para recuperar tipo de activo e input modality.

---

### 3.5. Recuperación myCBR

**Fortalezas**

- El adaptador headless es una contribución práctica relevante.
- Se fija el año de consulta en 2026, evitando dependencia del reloj del sistema.
- La separación temporal con base histórica es metodológicamente razonable.

**Debilidades**

- myCBR devolverá cinco vecinos aunque la consulta sea pobre o irrelevante. Por tanto, “todas devolvieron resultados” no mide calidad.
- La base de 263 casos es pequeña frente a 1.821 consultas; los patrones repetidos de ranking eran esperables.
- Los pesos unitarios y la amalgamación euclídea se heredan o se fijan sin análisis de sensibilidad.
- El año puede introducir sesgo si todas las consultas se fijan en 2026 y los casos históricos tienen distribución temporal desigual.

**Objeción probable**

> “La separación temporal no basta: el sistema podría estar recuperando por defaults y recencia, no por contenido técnico.”

**Resolución**

- Reportar contribución por atributo a la similitud global.
- Añadir ablaciones: sin año, sin tarea, sin activo, sin variables.
- Reportar distribución de similitud top-1/top-5 y porcentaje bajo umbral.
- Evaluar cobertura real de la case base por tarea/activo/modelo.

---

### 3.6. MMR

**Fortalezas**

- Fórmula explícita.
- Top-1 fijo, λ, pool y pesos documentados.
- Comparación con deduplicación exacta y aleatorio.

**Problemas**

- La métrica principal de diversidad reutiliza la misma similitud de solución optimizada por MMR. La mejora de ILD es en parte tautológica.
- Los pesos de solución —0,20 enfoque, 0,25 tipo, 0,40 modelos, 0,15 preprocesamiento— son plausibles, pero no validados.
- Pool=15 y top-5 son arbitrarios; solo se sensibiliza λ.
- La deduplicación exacta elimina todas las repeticiones con menor pérdida de similitud. MMR aporta diversidad más fina, pero falta demostrar que esa diversidad sea útil.
- Cinco listas MMR mantienen firmas repetidas; convendría explicar si eso es aceptable por diseño o síntoma de pool limitado.

**Objeción probable**

> “MMR mejora la métrica que él mismo define; no sabemos si mejora recomendaciones.”

**Resolución**

- Añadir métricas independientes: diversidad por familias expertas, cobertura de taxonomía, novelty, serendipity, evaluación humana.
- Sensibilidad a pool ∈ {10, 15, 20, 30}, top-k ∈ {3, 5, 10} y pesos de `ssol`.
- Comparar contra xQuAD, DPP, maximal coverage o reglas por familias de modelos.

---

### 3.7. Métricas y análisis estadístico

**Fortalezas**

- Análisis pareado adecuado.
- Bootstrap con semilla y 20.000 remuestras.
- Se reconoce pseudorreplicación por rankings repetidos.
- Se incluyen Wilcoxon/signos como secundarios, sin sobrerreclamar p-valores.

**Problemas**

- Las consultas no son independientes: 1.821 consultas producen solo 848 rankings baseline y 699 MMR ordenados.
- El bootstrap por consulta puede estrechar artificialmente intervalos.
- No hay margen de no inferioridad para afirmar que la pérdida de similitud es “pequeña”.
- La similitud CBR es proxy no validado de relevancia.
- En tareas pequeñas, como modelado de salud o pronóstico multihorizonte, los IC son descriptivos, no inferenciales.

**Resolución**

- Bootstrap por clúster de firma normalizada o patrón de ranking.
- Reportar resultados sobre consultas únicas normalizadas.
- Definir margen práctico de pérdida de similitud antes del análisis.
- Añadir análisis de casos donde ILD disminuye.

---

## 3. Riesgos de validez técnica solicitados

- **Defaults:** `Unknown synchronization`, `Not reported` y ceros heredados pueden crear similitudes artificiales o consultas vacías. La ablación muestra que ponderar sincronización cambia materialmente rankings.
- **Campos descartados:** descartar siempre tipo de activo e input modality debilita la afirmación de interoperabilidad de 19 campos.
- **Primer caso por IRI:** reproducible pero arbitrario; puede seleccionar una cita o entidad secundaria, no el estudio principal.
- **Limpieza RDF-star:** resuelve parseo, pero elimina procedencia fina; afecta auditabilidad.
- **Deriva de modelos LLM:** tres modelos distintos convierten la extracción en un lote heterogéneo no controlado.
- **Chunks iniciales:** riesgo alto de omitir métodos/resultados técnicos.
- **Case base histórica:** 263 casos limitan cobertura; muchos rankings repetidos.
- **Separación temporal:** útil, pero no prueba ausencia de sesgo ni relevancia; además todas las consultas usan año 2026.
- **Pool=15/top-5:** elección razonable pero no justificada empíricamente; MMR solo diversifica lo que entra al pool.

---

## 4. Evidencias/ficheros suplementarios que faltan o deben quedar explícitos

Para reproducibilidad/auditoría deberían estar disponibles:

1. Scopus export completo y decisiones de cribado por registro.
2. Manifiesto PDF→texto→facts con hashes y nivel de confianza.
3. Artefactos RDF/Turtle canónicos usados en el análisis.
4. Salidas crudas de OntoCast o, al menos, logs con modelo, versión, prompt, temperatura, fecha y reintentos.
5. Ontología semilla OPMAD exacta, versión, IRIs y imports.
6. Script de limpieza RDF-star y reporte de triples eliminados.
7. Validaciones SHACL/OWL por artefacto.
8. `facts_to_csv.py`, reglas de normalización y estadísticas de cobertura por campo.
9. Proyecto myCBR completo: versión, similitudes locales, pesos, case base y hashes.
10. Adaptador Java headless y comandos exactos.
11. Top-15 candidatos por consulta antes de MMR.
12. Taxonomía de 131 términos y pesos de `ssol`.
13. Scripts estadísticos, semillas, ambiente Python/Java y contenedor o lockfile.
14. Muestra dorada anotada por expertos para extracción y consulta.

---

## 5. Recomendaciones concretas para publicar

1. Reformular la conclusión como **interoperabilidad ejecutable de pipeline**, no interoperabilidad semántica plena.
2. Añadir una evaluación experta mínima: 50–100 documentos estratificados por tarea, anotados para tarea, activo, variables, modelo, sincronización y métricas.
3. Reemplazar defaults ambiguos por valores nulos tipados y excluirlos de similitud salvo evidencia.
4. Justificar o aprender pesos CBR/MMR; como mínimo, hacer sensibilidad de pesos.
5. Sustituir selección por IRI por identificación del estudio principal.
6. Preservar procedencia RDF-star mediante named graphs o reificación compatible.
7. Incluir análisis por cobertura de campo y por contribución de atributos a similitud.
8. Evaluar pool size y top-k, no solo λ.
9. Añadir bootstrap por clúster o análisis sobre firmas únicas.
10. Publicar un paquete reproducible completo con hashes y artefactos intermedios.

**Veredicto metodológico:** el trabajo es prometedor y honesto en varias limitaciones, pero la evidencia actual sostiene sobre todo “el pipeline corre y MMR diversifica según su propia métrica”. Para sostener “interoperabilidad reproducible” en sentido fuerte, faltan validación semántica, trazabilidad de triples, control de defaults y publicación completa de artefactos.
