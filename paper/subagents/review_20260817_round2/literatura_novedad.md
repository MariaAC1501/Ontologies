Revisión sin editar archivos. Inspeccioné `paper/main copy.tex`, `paper/references.bib`, `paper/research_questions_reframe.md` y `paper/supplement/protocol/literature_update_log.md`.

## 1) Novedad actual y riesgo de incrementalidad

La novedad quedó **mejor delimitada** después de la reescritura. El manuscrito ya no intenta vender OPMAD, myCBR, OntoCast ni MMR como novedades. La contribución defendible es:

- un puente reproducible Scopus/PDF/OntoCast--OPMAD/RDF → esquema CBR de 19 campos → consultas myCBR;
- una auditoría explícita de pérdidas, defaults, SHACL, normalización y atributos realmente activos;
- una evaluación downstream de reranking diverso sobre 1.821 consultas automáticas.

El riesgo de incrementalidad bajó de **alto** a **medio**. Sigue existiendo porque todos los bloques principales son heredados o estándar, y no hay comparación contra extracción JSON genérica, RAG/vector search, OntoCast sin OPMAD, ni ontologías inducidas por LLM. Para un venue exigente de IA/LLM puede parecer integración aplicada; para knowledge engineering, DSS aplicado o CBR reproducible es más defendible.

## 2) ¿El framing de contribución ahora es defendible?

Sí, **si se mantiene estrictamente como “interoperabilidad ejecutable y auditada”**.

El framing actual es mucho más seguro porque dice explícitamente:

- no se propone nueva ontología;
- no se propone nuevo CBR;
- no se propone nuevo algoritmo de diversidad;
- no se demuestra fidelidad factual ni utilidad decisional humana;
- MMR es una capa downstream reversible.

Las preguntas P1--P3 son coherentes con la evidencia: ejecutabilidad, pérdida de información y comportamiento algorítmico del ranking. El documento `research_questions_reframe.md` propone un paper más fuerte centrado en comparar extracción ontológicamente guiada contra esquemas/ontologías LLM y extracción no guiada. La versión nueva **no hace eso**; por tanto, no debe insinuar que OPMAD mejora la extracción frente a alternativas. Como system/pipeline paper, el enfoque actual es defendible.

## 3) Huecos de literatura/citas/familias que faltan

La bibliografía sigue siendo corta y algo estrecha. Añadiría, como mínimo, literatura de estas familias:

1. **Ontology-based information extraction / ontology population**  
   Es la tradición directa del trabajo, más allá de LLM-KG general.

2. **Extracción estructurada con LLM bajo esquemas/constraints**  
   JSON schema, constrained decoding, function calling, validación estructural, alucinaciones y evidencia textual.

3. **Scientific document information extraction / PDF parsing**  
   Extracción desde artículos científicos, secciones, tablas, métodos/resultados; también herramientas tipo GROBID/S2ORC/SciERC/SciBERT.

4. **Calidad y evaluación de knowledge graphs**  
   Completitud, consistencia, provenance, entity linking, quality assessment, SHACL como validación estructural, no factual.

5. **RDF-star, provenance y nanopublications/PROV-O**  
   Importante porque se retiran 311.559 bloques RDF-star y se preservan en sidecar.

6. **KG/ontologías/digital twins para mantenimiento predictivo, PHM e industrial asset management**  
   Ahora casi todo descansa en OPMAD y una referencia KG/GNN.

7. **Case-base maintenance / competence / editing / condensation**  
   Necesario para diferenciar mejor MMR como postproceso frente a mantenimiento de memoria.

8. **RAG, KG-RAG, semantic search y vector search**  
   Son alternativas obvias para “literatura científica → recomendación”; deben citarse y descartarse por alcance.

9. **Model recommendation / AutoML / meta-learning**  
   Como el sistema recomienda modelos candidatos, un revisor puede exigir posicionamiento frente a selección automática de modelos.

El `literature_update_log.md` ayuda, pero la búsqueda fue limitada. Yo no la llamaría revisión sistemática; mejor “actualización bibliográfica dirigida”.

## 4) Claims o comparaciones que siguen débiles

- **“Artículos/PDF/texto completo”**: el método usa casi siempre tres fragmentos iniciales, no lectura exhaustiva del PDF. Evitar sugerir extracción de texto completo si no lo es.

- **“Todos los documentos generan consultas”**: correcto como ejecutabilidad, pero débil como calidad. Muchas consultas sobreviven gracias a defaults o campos descartados.

- **“19 campos CBR”**: varios tienen 0% de cobertura informativa. Conviene enfatizar que el esquema es destino de interoperabilidad, no que los 19 campos se extraen útilmente.

- **“SHACL”**: solo 126/1.821 cumplen formas mínimas. SHACL debe aparecer como diagnóstico de límites, no como respaldo fuerte.

- **MMR vs diversidad**: ILD usa una similitud muy cercana a la función optimizada por MMR. Los comparadores ayudan, pero la mejora sigue siendo algorítmica, no prueba externa de mejores recomendaciones.

- **MMR vs CNN previo**: la diferenciación conceptual es buena; la comparación experimental directa sigue abierta. No reclamar superioridad sobre CNN.

- **OntoCast/OPMAD mejora extracción**: no hay baseline. No debe afirmarse ni sugerirse.

## 5) Cambios concretos recomendados antes de enviar

1. Añadir una tabla breve “componente / previo / nuevo en este trabajo / evidencia”, separando OPMAD, myCBR, casebase, OntoCast, puente RDF--CBR, auditorías y MMR.

2. Ampliar Related Work con 8--12 citas críticas de las familias anteriores, especialmente ontology-based IE, scientific IE, KG quality/provenance y RAG/vector search.

3. Añadir una frase explícita en introducción o discusión:  
   “Este estudio no compara OPMAD contra esquemas genéricos, ontologías inducidas por LLM ni RAG; esas alternativas se tratan como trabajo relacionado/futuro.”

4. Matizar cualquier uso de “PDF completo” o “artículos completos” para reflejar el chunking real.

5. Reforzar que los 1.821 documentos son **consultas automáticas**, no nuevos casos validados para retención en la memoria CBR.

6. Mantener el framing actual: **puente reproducible y auditable**, no nueva metodología de extracción ni nuevo recomendador.

Con esos ajustes, el manuscrito queda enviable como contribución de ingeniería/knowledge-engineering aplicada; no como paper fuerte de nuevo método LLM o de validación semántica.
