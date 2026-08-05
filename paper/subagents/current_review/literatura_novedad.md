## 1. Juicio sobre novedad e incrementalidad

**Veredicto:** la novedad es **moderada y principalmente de ingeniería reproducible**, no de método científico nuevo. El manuscrito es honesto al decir que no propone nueva ontología, nuevo CBR ni nuevo MMR. Eso fortalece la transparencia, pero también deja la contribución vulnerable: el aporte queda en la **integración ejecutable** PDF/OntoCast/OPMAD/RDF/myCBR/MMR y en la evaluación por lotes.

La brecha está **razonablemente identificada**: poblar manualmente conocimiento desde literatura es costoso y los rankings CBR pueden ser homogéneos. Pero está **insuficientemente defendida frente a literatura externa** y frente a alternativas modernas: extracción estructurada con LLM, RAG, búsqueda semántica/vectorial, ontological information extraction, recomendadores diversificados, AutoML/model recommendation y mantenimiento de bases de casos.

Lo más convincente es la delimitación: el artículo reconoce que demuestra **interoperabilidad técnica y diversidad algorítmica**, no fidelidad semántica ni utilidad humana. Lo más débil es que las preguntas P1–P3 son casi esperables: si se diseñan defaults y postprocesos, la cadena parsea; si se optimiza MMR con una similitud cercana a la métrica, la diversidad sube.

---

## 2. Crítica por sección

### Título y resumen

**Fortalezas**

- El título comunica reproducibilidad, literatura, CBR y mantenimiento predictivo.
- El resumen es transparente con números, corpus, λ, pérdida de similitud y limitaciones.
- La frase final —no se demuestra fidelidad semántica ni utilidad de usuario— es muy buena y evita sobreclaiming.

**Debilidades**

- “Extracción OPMAD” puede interpretarse como que se extrae la ontología OPMAD, no que se extraen hechos condicionados por OPMAD.
- El resumen parece una lista de componentes técnicos. La contribución científica queda diluida.
- La novedad no se formula como problema de investigación, sino como pipeline.
- El uso de “todos los documentos produjeron artefactos analizables” suena fuerte, pero depende de postproceso, defaults y limpieza de RDF-star.

**Sugerencia de framing**

> “A reproducible bridge from ontology-constrained LLM extraction to legacy ontology-enabled CBR for predictive-maintenance model recommendation, with post-hoc diversity control.”

Eso sitúa mejor el trabajo como **puente reproducible y evaluable**, no como nuevo algoritmo.

---

### Introducción

**Dónde convence**

- Identifica bien dos cuellos de botella: incorporación manual de literatura y homogeneidad de resultados CBR.
- Distingue claramente trabajos previos propios: OPMAD y CBR ya existían.
- La promesa de conectar literatura reciente con un DSS heredado es interesante para sistemas de ayuda al diseño conceptual.

**Dónde queda corta**

- Falta justificar por qué los **fragmentos iniciales de artículos** contienen suficiente información para generar consultas CBR útiles.
- No se explica bien la diferencia conceptual entre:
  - extraer un caso desde un artículo,
  - usar el artículo como consulta,
  - poblar la memoria CBR,
  - recomendar modelos a un arquitecto humano.
- Las preguntas P1–P3 son demasiado técnicas:
  - P1 mide compatibilidad sintáctica.
  - P2 mide un efecto esperado de MMR.
  - P3 mide sensibilidad de un parámetro, no una cuestión sustantiva del dominio.
- Falta una comparación conceptual con alternativas obvias: búsqueda semántica, RAG, embeddings, sistemas de recomendación de modelos, AutoML/meta-learning, extracción estructurada con LLM sin ontología.

**Problema central:** la introducción vende una necesidad real, pero la evaluación responde a una pregunta más estrecha: “¿puedo hacer que esta cadena corra y diversifique rankings?”. Eso es valioso, pero debe reconocerse como contribución de **interoperabilidad reproducible**, no como avance fuerte en mantenimiento predictivo o LLM-KG.

---

### Antecedentes y trabajos relacionados

**2.1 Ontologías, CBR y diseño**

Bien para establecer fundamentos, pero demasiado breve. Debería ampliar:

- CBR en mantenimiento predictivo y selección de modelos.
- mantenimiento de bases de casos, case-base editing, competence preservation, instance selection;
- ontologías y knowledge graphs para mantenimiento industrial/digital twins/PHM;
- diferencias entre usar ontología para representación, recuperación, similitud y validación.

El texto dice correctamente que OPMAD y myCBR son heredados, pero debe ser aún más explícito sobre qué partes son reutilizadas sin cambios: ontología, 19 campos, similitudes locales, base histórica, función de recencia, etc.

**2.2 LLMs y grafos de conocimiento**

Es la sección más débil en términos de literatura externa. Citar una roadmap, iText2KG, OntoCast y algunos trabajos recientes no basta para justificar novedad.

Faltan familias como:

- ontology-based information extraction;
- ontology-guided LLM extraction;
- scientific information extraction desde PDFs/artículos;
- validación de salidas RDF/JSON con SHACL, esquemas o constraints;
- evaluación de fidelidad factual de LLMs;
- provenance/RDF-star/nanopublications;
- RAG y KG-RAG como alternativa a CBR;
- comparación entre extracción simbólica y embeddings/vector search.

La frase “no se acepta el grafo como producto final: se define y prueba un puente determinista hacia CBR” es buena. Esa debería ser una idea central del artículo.

**2.3 Diversidad en recuperación**

Es razonable y mejor enfocada. La comparación con CNN modificado es necesaria. Aun así, faltan alternativas de diversificación:

- submodular diversification;
- xQuAD/intent-aware diversification;
- determinantal point processes;
- maximal coverage;
- novelty/serendipity en recomendadores;
- diversidad en CBR más allá de Smyth/McSherry.

Además, MMR es muy conocido y simple. La novedad no puede apoyarse en MMR, sino en **dónde se inserta**, cómo se parametriza con solución CBR y cómo se audita su efecto.

---

### Discusión frente a trabajos previos

**Fortalezas**

- La tabla CNN vs MMR ayuda mucho.
- El manuscrito distingue entre modificar la memoria CBR y reordenar la salida.
- Reconoce que la métrica ILD está alineada con el objetivo de MMR, lo cual es metodológicamente honesto.

**Debilidades**

- Falta una comparación experimental directa con el método CNN previo, aunque sea en subconjunto.
- Si la base de 263 casos y los campos vienen de trabajos anteriores, el lector puede ver el trabajo como “añadir OntoCast + wrapper Java + MMR”.
- El experimento usa artículos como consultas automáticas, no consultas humanas ni casos validados. Eso reduce la fuerza del argumento de utilidad para diseño conceptual.
- La mejora de diversidad puede parecer tautológica: MMR optimiza una función muy cercana a la métrica reportada.

---

## 3. Riesgos de autoplagio, solapamiento o contribución incremental insuficiente

Riesgos principales:

1. **Solapamiento con OPMAD/myCBR previo**  
   Si se reutilizan ontología, esquema, similitudes, case base y narrativa de arquitectura, debe quedar muy claro qué texto, datos y código son previos.

2. **Solapamiento con el trabajo CNN/diversidad**  
   Ambos tratan diversidad en recuperación CBR para mantenimiento predictivo. La diferencia postproceso vs memoria es clara, pero convendría una comparación empírica sobre las mismas consultas o al menos sobre un subconjunto común.

3. **Incrementalidad percibida**  
   Un revisor puede resumir el artículo como: “aplican una herramienta LLM para generar RDF, adaptan a myCBR y aplican MMR”. Sin validación semántica o humana, eso puede parecer demasiado estrecho.

4. **Sobreclaiming de interoperabilidad**  
   El 100 % de cobertura técnica es impresionante, pero se apoya en defaults, limpieza RDF-star y descarte de campos incompatibles. Debe presentarse como “ejecutabilidad de la interfaz”, no como extracción correcta.

5. **Riesgo de métrica circular**  
   La ILD usa la misma similitud de solución que MMR optimiza. El manuscrito lo admite; aun así, necesita una métrica externa o juicio experto para fortalecer la contribución.

---

## 4. Literatura o familias de trabajos que deberían incorporarse o contrastarse

No necesariamente como citas específicas, pero sí como familias a buscar:

- **Ontology-based information extraction** y ontology population.
- **LLM-based structured extraction** con esquemas, validadores, constraints, JSON/RDF/SHACL.
- **Scientific document information extraction** desde PDFs, abstracts, métodos y tablas.
- **Knowledge graphs for predictive maintenance**, PHM, digital twins e industrial asset management.
- **KG-RAG y retrieval-augmented generation** como alternativa a CBR simbólico.
- **Vector search / semantic search** para recomendación desde literatura.
- **Model recommendation / AutoML / meta-learning** para selección de modelos predictivos.
- **Case-base maintenance**: editing, condensation, competence models, coverage/diversity.
- **Diversity in recommender systems** beyond MMR: submodular methods, intent-aware diversification, DPPs, novelty/serendipity.
- **Human-centred evaluation of DSS**: utilidad percibida, carga cognitiva, tiempo de decisión, confianza y adopción.

---

## 5. Cómo reformular contribución y preguntas para que sean publicables

### Contribución reformulada

En vez de:

> “Presentamos una cadena que conecta literatura, OPMAD, CBR y MMR.”

Mejor:

> “Presentamos y auditamos un puente reproducible que transforma extracción LLM restringida por ontología en consultas ejecutables para un sistema CBR heredado de mantenimiento predictivo, cuantificando pérdidas de información, defaults, compatibilidad léxica y el efecto de una capa reversible de diversificación.”

Eso desplaza el foco hacia lo más defendible: **interoperabilidad auditada**.

### Preguntas mejoradas

1. **Interoperabilidad y pérdida de información**  
   ¿Qué proporción de información extraída desde artículos puede mapearse efectivamente al esquema CBR heredado, y en qué campos se pierde o se sustituye por defaults?

2. **Robustez de extracción**  
   ¿Cómo varían cobertura, validez RDF y campos CBR al cambiar modelo LLM, chunking o restricciones ontológicas?

3. **Diversificación con comparadores reales**  
   ¿Cómo se compara MMR contra deduplicación, azar, diversificación submodular y la condensación CNN previa bajo el mismo conjunto de consultas?

4. **Validez semántica**  
   ¿Qué precisión/exhaustividad tienen las consultas generadas frente a un conjunto dorado anotado por expertos?

5. **Utilidad de diseño**  
   ¿Las listas diversificadas ayudan a arquitectos de mantenimiento predictivo a identificar alternativas útiles, no redundantes y justificables?

Sin al menos una de las dos últimas —validación semántica o evaluación humana— el artículo debería posicionarse como **software/system paper**, no como validación de decisión inteligente.

---

## 6. Recomendaciones de revista, audiencia y framing

### Audiencia más adecuada

- Knowledge engineering aplicado.
- Sistemas de ayuda a la decisión.
- CBR aplicado.
- Ingeniería de sistemas para mantenimiento predictivo.
- Software reproducible para IA simbólica/LLM.

### Framing recomendado

**Fuerte:**  
“Interoperabilidad reproducible y auditable entre extracción ontológica con LLM y CBR heredado.”

**Más débil:**  
“Nueva metodología para mantenimiento predictivo” o “mejora de selección de modelos”, porque no hay validación de calidad ni usuarios.

### Revistas/venues posibles

- Si se añade validación semántica o humana: **Expert Systems with Applications**, **Knowledge-Based Systems**, **Engineering Applications of Artificial Intelligence**, **Advanced Engineering Informatics**, **Journal of Intelligent Manufacturing**.
- Si se mantiene como pipeline reproducible: venue de **systems engineering**, **CBR/knowledge engineering conference**, **PHM conference**, **IEEE Access** o revista orientada a software/reproducibilidad.
- Si el paquete de código y artefactos es central: considerar framing tipo **software/data descriptor**, aunque la no redistribución de PDFs limita esa vía.

**Conclusión crítica:** el manuscrito es sólido como integración reproducible y honesta, pero todavía parece una **cadena de ingeniería demasiado estrecha** para una revista exigente si no incorpora comparación externa, validación de extracción o utilidad humana. Su mejor oportunidad es presentarse como puente auditable entre literatura y CBR, no como avance metodológico en LLMs, ontologías o mantenimiento predictivo.
