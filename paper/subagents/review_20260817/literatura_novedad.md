Revisión hecha sin internet y sin editar archivos.

## 1) Novedad real y riesgo de incrementalidad

La novedad defendible es **moderada** y está más cerca de *knowledge engineering / systems integration* que de un método nuevo.

Lo realmente nuevo no es OPMAD, myCBR, OntoCast ni MMR. La contribución defendible es:

- usar **OntoCast condicionado por OPMAD** para extraer hechos de literatura PdM;
- convertir esos hechos RDF/Turtle a un **esquema CBR heredado de 19 campos**;
- ejecutar consultas masivas contra una base myCBR existente;
- auditar cobertura, defaults, SHACL, trazabilidad y sensibilidad;
- añadir MMR como **postproceso reversible** de diversidad.

El riesgo de incrementalidad es **alto** si el paper se presenta como:

- nuevo DSS de mantenimiento predictivo;
- nueva ontología;
- nuevo CBR;
- nueva técnica de diversificación;
- validación de extracción factual desde PDFs.

El framing más seguro es:

> “Una evaluación reproducible de interoperabilidad entre extracción ontológicamente guiada con LLM y un sistema CBR heredado, con análisis downstream de diversidad.”

Además, `paper/main copy.tex` actualmente contiene introducción, relacionados y métodos, pero no resultados/discusión completos. El abstract reclama resultados fuertes; un revisor atacaría que esos resultados no están soportados en el cuerpo del manuscrito solicitado.

---

## 2) Huecos de literatura/citas o familias que faltan

La bibliografía actual cubre fundamentos CBR, ontología, OPMAD/myCBR, MMR, diversidad y algunos LLM–KG. Pero faltan familias importantes:

1. **Ontology-based information extraction / ontology population**  
   El trabajo está poblado por extracción ontológica, pero esa tradición no aparece suficientemente.

2. **LLM-based structured extraction con schemas/constraints**  
   JSON schema, function calling, validación estructural, alucinaciones, extracción con evidencias textuales.

3. **Scientific document information extraction**  
   Extracción desde artículos completos, PDFs, secciones, tablas, métodos/resultados, no solo KG general.

4. **Evaluación de knowledge graphs construidos por LLM**  
   Calidad factual, completitud, consistencia, provenance, entity alignment, SHACL/OWL validation.

5. **RAG, KG-RAG, vector search y semantic search**  
   Son alternativas obvias para “literatura científica → recomendación/consulta”. Hay que explicar por qué CBR simbólico y no embeddings/RAG.

6. **Knowledge graphs / ontologías para PHM, PdM, digital twins e industrial asset management**  
   Actualmente hay muy poca conexión con KGs de mantenimiento industrial más allá de una referencia.

7. **Model recommendation, AutoML y meta-learning**  
   Si el output son modelos candidatos, un revisor puede preguntar por literatura de recomendación/selección de modelos.

8. **Case-base maintenance y competence models**  
   Especialmente porque el trabajo previo de diversidad mediante CNN modifica la memoria CBR; conviene situar MMR frente a edición/condensación/mantenimiento de bases de casos.

9. **Human-centered DSS evaluation**  
   Si se habla de utilidad para diseño conceptual, faltan referencias a evaluación con expertos, confianza, carga cognitiva y utilidad percibida.

---

## 3) Cómo diferenciar este paper

### Frente a OPMAD/myCBR previo

Decir explícitamente:

- OPMAD, myCBR, la base histórica de 263 casos, pesos/similitudes y esquema heredado **no son contribuciones nuevas**.
- Este paper aporta el **puente automático desde literatura reciente a consultas CBR ejecutables**.
- La contribución no es “mejor CBR”, sino **interoperabilidad auditada entre extracción LLM/RDF y CBR legado**.

Frase útil:

> “A diferencia de trabajos previos OPMAD–myCBR, este estudio no diseña la ontología ni el DSS; evalúa cómo poblar sus consultas desde literatura científica mediante extracción ontológicamente guiada y cuantifica las pérdidas de información del puente RDF–CBR.”

### Frente a OntoCast

OntoCast es herramienta, no contribución. Diferenciar así:

- OntoCast produce hechos RDF; este paper estudia si esos hechos sobreviven al paso hacia un esquema CBR operacional.
- La evaluación no debería ser “OntoCast funciona”, sino “OntoCast+OPMAD produce insumos auditables para una tarea downstream concreta”.

### Frente a iText2KG / KG construction

iText2KG y KG construction buscan construir grafos. Este trabajo debe decir:

- no propone un KG general;
- usa una ontología experta fija;
- evalúa el paso **KG/facts → decisión CBR**;
- mide defaults, pérdidas, normalización y ejecutabilidad.

### Frente a RAG/vector search

Debe aclararse que:

- RAG/vector search recuperaría textos o chunks semánticamente cercanos;
- aquí se produce una consulta estructurada compatible con similitudes CBR heredadas;
- la salida es más auditable, pero probablemente menos flexible.

Si se reclama ventaja práctica, hace falta baseline con embeddings/RAG. Si no, limitarse a decir que son alternativas no evaluadas.

### Frente a diversidad/CBR previo

La diferencia fuerte es:

- CNN/diversity previo modifica o condensa la base de casos;
- MMR solo reordena un pool recuperado;
- MMR es reversible, no altera la memoria, conserva top-1 por diseño.

No vender MMR como nuevo. Venderlo como **capa downstream controlada**.

---

## 4) Preguntas de investigación mejor formuladas

Las P1–P4 actuales son razonables, pero siguen siendo internas al pipeline. Para una contribución publicable fuerte, reformularía así:

**RQ1. Calidad de extracción ontológicamente guiada**  
¿OntoCast condicionado por OPMAD extrae hechos más correctos, completos y consistentes que extracción JSON genérica o esquemas/ontologías generadas por LLM?

**RQ2. Pérdida de información RDF–CBR**  
¿Qué proporción de los hechos extraídos puede mapearse a los 19 campos CBR, qué campos quedan como defaults y qué atributos sobreviven realmente a la consulta myCBR?

**RQ3. Valor del texto completo**  
¿Qué información relevante para PdM aparece solo en métodos/resultados/texto completo frente a título/resumen/keywords?

**RQ4. Robustez del método**  
¿Cómo varían cobertura, conformidad y rankings al cambiar modelo LLM, chunks, ontología fija vs generada y normalización?

**RQ5. Utilidad downstream**  
¿Las consultas derivadas de extracciones más fieles producen recomendaciones CBR más relevantes, útiles o diversas según expertos?

Si no se hará validación humana todavía, entonces las preguntas deben ser más modestas:

> “¿Puede la cadena producir consultas ejecutables y qué pérdidas/defaults introduce?”  
> “¿Cómo cambia algorítmicamente el ranking al aplicar MMR?”

Pero eso posiciona el paper como system/software paper, no como validación científica fuerte.

---

## 5) Claims que un revisor atacaría

1. **“Extracción estructurada trazable”**  
   La limpieza elimina RDF-star; el reporte indica 311.559 bloques retirados. Eso debilita trazabilidad fina.

2. **“19 campos CBR”**  
   Muchos campos son defaults o no informativos. En auditoría: sincronización, desempeño y modos de falla son 0/1821 informativos; tipo de activo e input modality no quedan activos en consulta.

3. **“Todos los documentos generan consultas”**  
   Eso prueba ejecutabilidad, no corrección. myCBR devuelve vecinos aunque la consulta sea pobre.

4. **“Fidelidad semántica”**  
   No hay gold standard anotado ni precisión/recall/F1. El protocolo humano está especificado, pero no ejecutado.

5. **“Mejora de diversidad”**  
   ILD usa la misma similitud de solución que MMR optimiza. Es una mejora algorítmica alineada con la métrica, no validación independiente.

6. **“Utilidad para mantenimiento predictivo”**  
   No hay juicio experto ni evaluación con diseñadores/arquitectos.

7. **“Robustez estadística sobre 1.821 consultas”**  
   Hay pseudorreplicación: muchos rankings repetidos. Debe enfatizarse cluster bootstrap/patrones únicos.

8. **“Texto completo/PDF”**  
   Si se usaron chunks iniciales, no debe insinuarse extracción exhaustiva del artículo completo.

9. **“OPMAD mejora la extracción”**  
   Aún no hay comparación contra JSON genérico, schema LLM, ontology LLM o RAG.

10. **“Conformidad SHACL”**  
   El reporte SHACL mínimo muestra solo 126/1821 artefactos conformes; no se puede usar SHACL como respaldo fuerte sin matizar.

**Conclusión:** el paper tiene una contribución real, pero debe venderse como **puente reproducible y auditado**, no como validación de extracción semántica ni como nuevo método de recomendación. Para fortalecerlo, la pieza que más falta es una evaluación experta estratificada de extracción y utilidad downstream.
