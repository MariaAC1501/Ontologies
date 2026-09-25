He inspeccionado `paper/main copy.tex` y los reportes/repositorio indicados. No edité archivos.

## 1) Dictamen editorial

**Desk reject si se envía tal cual a Q1/Q2.**  
**Potencial de “major revision”** si se reestructura y se bajan/precisan los claims.

Razones principales:

- `paper/main copy.tex` termina en **Materiales y métodos** y luego bibliografía. No contiene secciones de **Resultados, Discusión, Limitaciones ni Conclusión**. Los resultados aparecen casi solo en el abstract.
- La evidencia más fuerte está en el suplemento, pero no está integrada en el manuscrito.
- La contribución factual está débil: hay protocolo de validación humana (`paper/supplement/audit/expert_validation_protocol.md`), pero **no hay anotación experta ejecutada**.
- La interoperabilidad computacional es sólida, pero la calidad semántica es limitada:
  - SHACL conforme: solo **126/1821** artefactos (`paper/supplement/audit/SHACL_REPORT.md`).
  - Campos clave con 0% informativo: sincronización, desempeño, modos de falla, tipo de activo (`field_coverage_19cols.csv`).
  - Tras normalización, solo quedan activos: tarea 100%, activo 85.1%, input type 75.8%; case type/sync/input modality 0% (`normalized_field_coverage.csv`).
- Hay inconsistencias documentales:
  - `paper/README.md` apunta a `paper/main.tex`, pero ese archivo no existe.
  - `DIVERSITY_COMPARISON_RESULTS.md` reporta 599 consultas y está desactualizado frente al suplemento con 1.821.
  - `pipeline/SCHEMA_MAPPING.md` habla de V21, mientras el experimento principal usa V12/263 casos.

## 2) Problema, novedad y contribución

### Qué está claro

Está clara la cadena técnica:

> Scopus/corpus → PDFs → OntoCast condicionado por OPMAD → RDF/Turtle → puente a 19 campos → consultas myCBR → reranking MMR con diversidad.

También está bien delimitado que el trabajo **no propone** una nueva ontología, un nuevo CBR ni un nuevo algoritmo de diversidad. Eso aparece explícitamente en `paper/main copy.tex`.

La evidencia computacional es fuerte para afirmar:

- 1.821 documentos únicos con artefactos procesables.
- 1.821 consultas ejecutables contra una base myCBR de 263 casos.
- MMR aumenta diversidad algorítmica:
  - ILD: **0.4216 → 0.5265**
  - listas con firmas repetidas: **610 → 5**
  - similitud media top-5: **0.5563 → 0.5536**  
  (`paper/supplement/results/REPORT.md`)

### Qué falta

Falta demostrar que la ontología fue “poblada” con hechos correctos y útiles, no solo que produjo RDF parseable.

Problemas críticos:

- La conversión RDF→CBR usa muchos defaults.
- Muchos campos de los 19 no aportan información real.
- No hay gold standard experto.
- La diversidad se mide con una métrica alineada con el propio objetivo de MMR, por tanto no valida utilidad independiente.
- El manuscrito no muestra resultados, solo los promete.

### Claims que cambiaría

Cambiaría claims fuertes como:

> “poblar una ontología desde papers y hacer recomendaciones”

por algo más defendible:

> “generar afirmaciones RDF tipadas por OPMAD y transformarlas en consultas ejecutables myCBR, con auditoría explícita de cobertura, defaults y pérdidas semánticas”.

Cambiaría:

> “recomendaciones con diversidad”

por:

> “reranking algorítmico de casos candidatos, con reducción de redundancia bajo una similitud de solución definida”.

Cambiaría:

> “conformidad SHACL”

por:

> “la validación SHACL mínima revela baja conformidad estructural: 126/1821 artefactos conformes”.

## 3) Estructura recomendada del paper perfecto

1. **Introducción**
   - Problema: convertir literatura científica en insumos para DSS/CBR.
   - Brecha: extracción LLM/RDF no implica calidad semántica ni utilidad downstream.
   - Contribución precisa: pipeline auditable OntoCast–OPMAD–myCBR–MMR.

2. **Trabajos relacionados**
   - Ontologías y CBR en mantenimiento predictivo.
   - LLMs para knowledge graph extraction.
   - Ontology-guided extraction.
   - Diversidad en recomendadores/CBR: MMR, DPP, xQuAD, CNN.

3. **Datos y corpus**
   - Consulta Scopus.
   - Cribado: 3.990 → 2.768 incluidos.
   - PDFs: 1.822 recuperados, 1.821 únicos.
   - Sesgo de disponibilidad: 946 incluidos sin PDF; tasas por año/OA (`PDF_AVAILABILITY_REPORT.md`).

4. **Pipeline OntoCast–OPMAD**
   - OPMAD seed: clases/propiedades.
   - Configuración de OntoCast/modelos/chunks.
   - RDF-star y limpieza.
   - Qué significa “poblar”: hechos RDF tipados, no verdad factual garantizada.

5. **Puente RDF–CBR**
   - Mapeo de 19 campos.
   - Qué campos realmente sobreviven.
   - Defaults y pérdidas.
   - Tabla central con `field_coverage_19cols.csv` y `normalized_field_coverage.csv`.

6. **Evaluación 1: interoperabilidad**
   - Parseabilidad.
   - Consultas ejecutables.
   - SHACL.
   - Multi-casos ignorados: 409 artefactos con >1 caso; 567 casos adicionales no usados.

7. **Evaluación 2: fidelidad semántica**
   - Idealmente: muestra anotada por expertos.
   - Comparadores: OntoCast+OPMAD vs JSON genérico vs esquema LLM vs ontología LLM.
   - Si no se ejecuta, mover esto a trabajo futuro y no formularlo como RQ respondida.

8. **Evaluación 3: recuperación CBR y diversidad**
   - Baseline myCBR top-5.
   - MMR pool-15/top-5/λ=0.70.
   - Sensibilidad por λ, pool 10–30, max-sum, MAP-DPP.
   - Pseudorreplicación y bootstrap por clúster.

9. **Discusión**
   - Qué queda demostrado: interoperabilidad ejecutable y comportamiento de reranking.
   - Qué no: verdad factual, utilidad humana, superioridad decisional.
   - Implicaciones para DSS en mantenimiento predictivo.

10. **Limitaciones**
   - PDF availability bias.
   - 263 casos históricos.
   - Baja cobertura de campos.
   - Falta de validación experta.
   - Dependencia de modelos LLM y de myCBR heredado.

11. **Conclusión**
   - Contribución real: framework auditable para transformar literatura en consultas CBR.
   - Próximo paso: validación experta y utilidad downstream.

## 4) Cambios priorizados

### CRÍTICOS

1. Añadir Resultados, Discusión, Limitaciones y Conclusión a `paper/main copy.tex`.
2. Integrar los datos del suplemento en el manuscrito, especialmente:
   - `field_coverage_19cols.csv`
   - `normalized_field_coverage.csv`
   - `SHACL_REPORT.md`
   - `AUDIT_REPORT.md`
   - `EXTENDED_RERANKING_REPORT.md`
3. Ejecutar validación experta o rebajar claramente el alcance.
4. Corregir claims: “interoperabilidad ejecutable” sí; “fidelidad factual” no demostrada.
5. Resolver inconsistencias:
   - `paper/main.tex` inexistente.
   - `DIVERSITY_COMPARISON_RESULTS.md` obsoleto.
   - V12 vs V21 en documentación.
6. Mostrar explícitamente que la consulta myCBR no usa realmente los 19 campos completos.

### IMPORTANTES

1. Añadir tabla de pérdidas RDF→19 campos→consulta normalizada.
2. Reportar resultados negativos con honestidad: 0% en sincronización, desempeño y modos de falla.
3. Reorganizar las RQs: separar extracción, interoperabilidad, CBR y diversidad.
4. Dejar MMR como tarea downstream, no como contribución principal.
5. Usar bootstrap por clúster en el paper, no solo p-values.
6. Añadir ejemplo trazable de un paper: texto → RDF → CSV → query → top-5.
7. Ajustar abstract: demasiado largo y contiene demasiados resultados sin soporte en el cuerpo.
8. Completar keywords.

### OPCIONALES

1. Traducir a inglés si se apunta a Q1/Q2 internacional.
2. Preparar paquete reproducible con DOI.
3. Ampliar SHACL con shapes más exigentes.
4. Añadir visualización de cobertura por campo.
5. Añadir evaluación de utilidad por expertos sobre listas recomendadas.

## 5) Frases y títulos recomendados

### Títulos posibles

- **“From Scientific Literature to Case-Based Decision Support: An Audited OPMAD–OntoCast Pipeline for Predictive Maintenance”**
- **“Ontology-Guided Extraction from Predictive-Maintenance Papers: Auditing OPMAD Population, myCBR Query Generation, and Diversity-Aware Retrieval”**
- **“Executable Interoperability, Not Ground Truth: An Audit of Ontology-Guided Literature Extraction for Predictive-Maintenance CBR”**
- **“De literatura científica a consultas CBR: extracción guiada por OPMAD y reranking diverso en mantenimiento predictivo”**

### Frases de contribución recomendadas

- “Este trabajo evalúa una cadena ejecutable para transformar artículos científicos en consultas myCBR compatibles con OPMAD.”
- “La contribución no es un nuevo algoritmo de extracción ni de diversidad, sino una evaluación auditable de interoperabilidad entre extracción ontológica y recuperación CBR.”
- “Los resultados demuestran ejecutabilidad y reducción algorítmica de redundancia, no fidelidad factual ni utilidad decisional validada por expertos.”
- “La auditoría revela tanto el potencial como las pérdidas semánticas del puente RDF–CBR.”
- “MMR se usa como tarea downstream para observar el efecto de la representación extraída sobre listas candidatas, no como validación independiente de recomendación.”
