No he modificado archivos. Revisión basada en `paper/main.pdf` extraído con `pdftotext -enc UTF-8 -layout`.

# Revisión editorial y estrategia de publicación

## 1. Lectura editorial general

**Veredicto:** el manuscrito es sólido como artículo metodológico/reproducible: el problema está bien acotado, las métricas son transparentes y las limitaciones están tratadas con honestidad. Para una revista Q1/Q2 internacional, sin embargo, necesita **más claridad narrativa, versión completa en inglés y mejor encuadre del aporte**: no vende “mejor mantenimiento predictivo”, sino **interoperabilidad ejecutable + diversificación controlada de recomendaciones CBR**.

Un lector no iniciado entiende que el artículo automatiza el paso desde artículos científicos recientes hacia consultas de un sistema CBR y luego diversifica la lista de recomendaciones. Lo que cuesta entender al inicio es: qué es exactamente OPMAD, qué representa un “caso”, por qué myCBR es importante como sistema heredado y por qué la diversidad de modelos ayuda al diseñador.

**Prioridades editoriales:**

1. Si el objetivo es Q1/Q2 internacional, preparar **manuscrito completo en inglés**.
2. Reducir densidad del resumen y de métodos.
3. Añadir una explicación temprana tipo “for non-specialists”: documento → hechos → consulta CBR → lista de modelos.
4. Reforzar el mensaje: *technical interoperability and ranking behavior, not semantic correctness*.
5. Mejorar anonimización y paquete suplementario.

---

## 2. Crítica sección por sección

### Resumen / Abstract

**Fortalezas:** contiene pregunta, pipeline, tamaño de corpus, métrica principal, coste en similitud y limitación clave. Muy honesto.

**Problemas:** está sobrecargado. Hay demasiados detalles operativos: RDF-star cleanup, 19 campos, pool 15, defaults, λ. El abstract ocupa más de lo ideal y se divide entre páginas.

**Acción:** reducir a 200–250 palabras. Mantener solo: problema, pipeline, corpus, resultado principal, límite. Mover detalles finos a métodos.

### Introducción

**Fortalezas:** el flujo problema → CBR/ontología → LLM/KG → diversidad está bien construido. Las preguntas P1–P3 son claras.

**Problemas:** arranca con muchos conceptos antes de dar una imagen simple del sistema. La frase “En trabajos anteriores se desarrolló…” puede romper anonimización si son autocitas.

**Acción:** añadir un párrafo puente: “En términos prácticos, el sistema toma fragmentos de PDF, extrae hechos compatibles con OPMAD, los convierte en una consulta CBR y reordena las recomendaciones para evitar soluciones redundantes”. Reformular autocitas en tercera persona neutral.

### Trabajos relacionados

**Fortalezas:** bien enfocado y no excesivo.

**Problemas:** para Q1 puede parecer corto. Falta una delimitación más explícita frente a: extracción ontológica con LLM, KG construction, CBR con ontologías, diversidad/recommendation reranking y sistemas DSS para mantenimiento.

**Acción:** añadir una tabla de posicionamiento: “trabajo previo / entrada / salida / validación / diferencia con este artículo”.

### Métodos

**Fortalezas:** es la sección más fuerte. Reproducibilidad, defaults, deriva de modelos, selección de casos y métricas están explicados.

**Problemas:** demasiado densa. Los nombres de modelos LLM y el piloto con juez LLM pueden distraer; conviene mover parte al suplemento. También deben justificarse mejor: uso de solo chunks iniciales, corpus 2025–2026, elección del primer caso por IRI y tratamiento de campos descartados.

**Acción:** abrir métodos con una figura/overview y una tabla “decisiones de diseño y justificación”. Separar claramente qué es evaluación principal y qué es amenaza/ablación.

### Resultados

**Fortalezas:** los resultados son claros y bien conectados a P1–P3. Las comparaciones con deduplicación y azar fortalecen el argumento.

**Problemas:** algunas etiquetas pueden confundir: “Firmas de modelos únicas” debería ser “media de firmas únicas por lista”. Table 2 mezcla métricas deterministas con media esperada aleatoria; la nota lo aclara, pero debe ser más visible.

**Acción:** estandarizar ILD/ild, explicar en texto que la mejora de ILD está alineada con la función optimizada y no es validación independiente.

### Discusión

**Fortalezas:** excelente calibración de claims. No sobrepromete.

**Problemas:** falta una sección breve de “implicación para diseñadores/arquitectos”: ¿qué decisión mejora o se hace más auditable?

**Acción:** añadir 1 párrafo con un caso práctico: “el diseñador mantiene el top-1 pero ve alternativas menos redundantes”.

### Amenazas a la validez

**Fortalezas:** muy buena, transparente y completa.

**Riesgo:** puede sonar autodestructiva si no se balancea con “lo que sí demuestra”.

**Acción:** cerrar amenazas con frase positiva: “Estas amenazas no invalidan la interoperabilidad técnica; delimitan las condiciones para afirmar utilidad semántica o humana”.

### Conclusiones

**Fortalezas:** concisas y consistentes.

**Acción:** añadir una oración final más editorial: “El valor del enfoque está en convertir un DSS ontológico existente en una infraestructura auditable de explotación de literatura, no en reemplazar curación experta”.

### Disponibilidad / Declaraciones

**Fortalezas:** buena declaración de datos/código y uso de IA.

**Problemas:** para revisión doble ciego hay riesgos: metadatos PDF con zona horaria, autocitas identificables, posibles rutas/manifestos con información local, financiación anonimizada pero quizá no suficiente. La declaración de IA debe adaptarse a la política de la revista elegida.

**Acción:** limpiar metadatos, anonimizar repositorio/suplemento, detallar herramientas generativas usadas en escritura y separar claramente método LLM vs asistencia editorial.

---

## 3. Problemas de estilo o forma que pueden afectar la revisión

- **Idioma:** para Q1/Q2 internacional, enviar en inglés completo. La versión española sirve como base, no como versión final.
- **Acrónimos:** estandarizar OPMAD/opmad, myCBR/MYCBR, RDF-star/RDF*, ILD/ild.
- **Anglicismos:** decidir política: “reranking”, “pool”, “chunks”, “headless”, “defaults”. Si se conserva, definir una vez y usar consistentemente.
- **Título:** informativo pero largo y denso.
- **Figuras:** buenas en general. Figura 4 usa doble eje; advertir claramente o considerar dos paneles. Figura 5 debe remarcar que estratos pequeños son exploratorios.
- **Tablas:** mejorar etiquetas de métricas y notas de Table 2.
- **Anonimización:** revisar autocitas, frases de continuidad con trabajos previos y metadatos PDF.
- **Referencias/modelos futuros o no estables:** verificar años, DOI, disponibilidad y nombres exactos de modelos LLM antes de enviar.

---

## 4. Recomendaciones de reescritura de alto impacto

### Títulos posibles

**En inglés, recomendado para Q1/Q2:**

1. *From Scientific Papers to Diverse Case-Based Recommendations for Predictive Maintenance: A Reproducible OPMAD–CBR Pipeline*
2. *Reproducible Ontology-Guided Extraction and MMR Diversification for Case-Based Predictive Maintenance*
3. *Linking Literature to Case-Based Reasoning in Predictive Maintenance through Ontology-Constrained Extraction and Diversified Retrieval*

**En español:**

1. *De artículos científicos a recomendaciones diversas: integración reproducible OPMAD–CBR para mantenimiento predictivo*
2. *Extracción ontológica y diversificación de recomendaciones CBR para mantenimiento predictivo*
3. *Interoperabilidad reproducible entre literatura científica y razonamiento basado en casos en mantenimiento predictivo*

### Frase de contribución sugerida

> Este trabajo no evalúa la precisión semántica de la extracción ni la utilidad humana de las recomendaciones; demuestra que una cadena reproducible puede transformar literatura reciente en consultas CBR técnicamente válidas y controlar algorítmicamente la diversidad del top-5 con pérdida marginal de similitud.

### Reescritura estratégica del aporte

Cambiar el énfasis de “usamos LLM para extraer RDF” a:

> La contribución central es una capa de interoperabilidad auditable entre extracción ontológica, un DSS CBR heredado y un mecanismo reversible de diversificación.

---

## 5. Estrategia de publicación

### Mejor encuadre

Enviar como artículo de **knowledge-based systems / engineering AI / decision support**, no como artículo de mantenimiento predictivo clásico. No se propone un nuevo modelo diagnóstico ni pronóstico.

### Revistas posibles por enfoque

- **Knowledge-Based Systems / Expert Systems with Applications:** buen ajuste, pero pedirán mayor novedad metodológica o validación.
- **Engineering Applications of Artificial Intelligence / Advanced Engineering Informatics:** buen encaje si se enfatiza DSS, reproducibilidad e integración.
- **Computers in Industry / Journal of Manufacturing Systems:** viable si se refuerza impacto industrial.
- **Reliability Engineering & System Safety / MSSP / IEEE TII:** más difícil con la versión actual; exigirían validación de utilidad o mantenimiento más fuerte.
- **Conferencias:** ICCBR, PHM, ESREL, IEEE ISSE o workshops de KG/LLM son buenas opciones si se mantiene como contribución técnica.

### Qué versión enviar

- **Para Q2/conferencia:** traducir a inglés, pulir narrativa, reforzar suplemento y mantener claims modestos.
- **Para Q1:** añadir al menos una validación adicional: muestra dorada anotada por expertos, evaluación con usuarios/arquitectos, o comparación directa con métodos alternativos de diversificación/condensación sobre las mismas consultas.

### Suplemento indispensable

- Consulta Scopus completa y criterios de cribado.
- Manifiesto anonimizado de documentos/DOI, sin PDFs.
- Prompts, configuración OntoCast, versiones de modelos, semillas.
- Artefactos canónicos TTL/CSV permitidos por licencia.
- Scripts, lockfile/Docker/Conda, instrucciones cross-platform.
- Resultados por consulta y notebooks de análisis.
- Diccionario de campos y SHACL/validaciones si existen.

---

## 6. Checklist final antes de enviar

- [ ] Traducir todo a inglés si la revista es internacional Q1/Q2.
- [ ] Reducir abstract y hacerlo más narrativo.
- [ ] Definir todos los acrónimos en primera aparición.
- [ ] Estandarizar OPMAD, myCBR, MMR, ILD, RDF-star.
- [ ] Revisar anonimización de autocitas, financiación, metadatos PDF y suplemento.
- [ ] Verificar referencias, DOI, años y disponibilidad.
- [ ] Confirmar que las afirmaciones de disponibilidad coinciden con los archivos realmente entregados.
- [ ] Ejecutar reproducción desde un checkout limpio.
- [ ] Revisar figuras a 300 dpi y tablas con etiquetas inequívocas.
- [ ] Adaptar declaración de IA a la política de la revista.
- [ ] Preparar carta al editor resaltando: interoperabilidad reproducible, evaluación a escala y límites explícitos.
- [ ] No afirmar utilidad semántica/humana salvo que se añada validación experta.
