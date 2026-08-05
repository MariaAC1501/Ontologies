# 1. Dictamen editorial tentativo

**Revisión mayor, con riesgo real de rechazo/desk rejection en una revista selectiva.**

El manuscrito es honesto y técnicamente prometedor, pero su publicabilidad depende de convencer al editor de que la contribución no es solo una integración de componentes ya conocidos. La propia introducción reconoce: **“no propone una nueva ontología, un nuevo motor CBR ni un nuevo algoritmo MMR”**. La novedad queda en la operacionalización de la cadena **PDF → OntoCast/OPMAD → RDF → 19 campos → myCBR headless → MMR**. Eso puede ser publicable como contribución de ingeniería reproducible, pero falta una validación independiente fuerte.

Las P1-P3 están respondidas solo en sentido algorítmico:

- **P1:** sí, 1.821/1.821 consultas ejecutan y devuelven resultados, pero esto mide compatibilidad sintáctica, no fidelidad semántica.
- **P2:** MMR mejora la diversidad medida: ILD de **0,4216 a 0,5265**, firmas repetidas de **610 a 5**, con pérdida de similitud top-5 de **0,0027**. Pero la métrica ILD usa la misma similitud de solución optimizada por MMR.
- **P3:** hay sensibilidad para λ, pero la estabilidad por tarea es débil: hay estratos de **n = 6** y **n = 8**, y en “pronóstico a un paso” el efecto es casi nulo/no claro.

El principal motivo de major revision sería: **el artículo demuestra interoperabilidad técnica y reranking esperado, pero no demuestra que las consultas extraídas desde los PDF sean correctas ni que las recomendaciones sean útiles.**

# 2. Crítica sección por sección

## Resumen / Abstract

Fortalezas: es claro, cuantitativo y bastante honesto. Frases como **“no constituye validación independiente”** y **“not semantic extraction fidelity or improved user utility”** reducen el riesgo de claims exagerados.

Problemas:

- Está muy cargado de detalles técnicos y números. Para un editor, el mensaje central puede perderse.
- La frase **“All unique documents yielded artifacts that could be parsed after explicit RDF-star cleanup”** puede sonar más fuerte de lo que es: parseabilidad tras eliminar RDF-star no implica calidad semántica.
- “Reproducible pipeline” es defendible solo si el paquete suplementario realmente permite repetir el experimento. La dependencia de PDFs no redistribuidos, modelos LLM/versiones y manifiestos parcialmente reconstruidos debilita esa palabra.

## Introducción

La introducción plantea bien el problema: incorporación manual de conocimiento y homogeneidad en recuperación CBR. También delimita la contribución con honestidad: **“no propone una nueva ontología, un nuevo motor CBR ni un nuevo algoritmo MMR.”**

Debilidad editorial: al admitir eso, la contribución debe apoyarse en una evaluación mucho más convincente. Las preguntas P1-P3 son internas al sistema. Falta una pregunta del tipo: ¿las extracciones representan correctamente los artículos?, ¿las recomendaciones son útiles para diseñadores?, ¿la diversidad percibida mejora la toma de decisiones?

P1 puede parecer casi “por construcción” si el puente usa defaults como **Not reported**, **Unknown synchronization** y, según amenazas, incluso una tarea por defecto.

## Trabajos relacionados

Correcto pero limitado. Cubre ontologías+CBR, LLM+KG y diversidad/MMR. Sin embargo, un revisor experto puede objetar que la comparación con literatura de:

- población ontológica automática,
- evaluación de extracción con LLM,
- KG construction from scientific articles,
- CBR recommendation diversity,

es insuficiente. OntoCast se trata como componente usado, pero no queda clara la diferencia frente a otros pipelines de extracción guiada por ontologías.

La relación con Muñoz-Peña et al. [14] es útil, pero queda conceptual. Una comparación empírica con CNN modificado, aunque parcial, fortalecería mucho el artículo.

## Materiales y métodos

Es la sección más fuerte y también donde aparecen los problemas más graves.

Aspectos sólidos:

- Corpus grande: **3.990 registros Scopus**, **2.768 incluidos**, **1.822 PDF**, **1.821 documentos únicos**.
- Separación temporal entre artículos 2025–2026 y base histórica de **263 casos**.
- Pipeline modular.
- Ablación de **Unknown synchronization**.
- Reconocimiento de deriva de modelos LLM: **599 gpt-5-mini, 500 gpt-5.4-mini, 722 gpt-5.6-luna**.

Problemas críticos:

1. **Extracción solo de chunks iniciales.** Se usaron “hasta tres chunks iniciales”. Muchos artículos describen modelos, métricas y resultados en métodos/resultados, no necesariamente al inicio. Esto amenaza directamente los campos CBR.

2. **Piloto de modelo débil.** El piloto de diez documentos, juzgado por otro LLM, con medias **5,5 vs 4,9 sobre 15**, es muy débil. Además, las puntuaciones absolutas son bajas.

3. **Deriva de modelos no controlada.** Tres modelos distintos generan los artefactos finales. El manuscrito lo declara como amenaza, pero no analiza si cambia distribución de campos, tareas o rankings.

4. **Pérdida de procedencia RDF-star.** El postproceso “elimina esas sentencias y conserva los triples regulares”. Esto permite parsear, pero sacrifica evidencia a nivel triple.

5. **Puente con defaults y descarte de campos.** El artículo reconoce que:
   - todos generaron **Unknown synchronization**;
   - tipo de activo y modalidad de entrada se descartaron en todas las consultas;
   - 409 artefactos tenían más de un caso y se tomó el primero por orden de IRI;
   - la base tiene solo **263 casos**.
   
   Esto hace que el “esquema de 19 campos” suene más completo que la consulta realmente usada.

6. **Pesos de MMR y solución poco justificados.** La similitud de solución fija pesos **0,20 / 0,25 / 0,40 / 0,15** para enfoque, tipo, modelos y preprocesamiento. No hay justificación empírica ni sensibilidad a esos pesos.

## Resultados

Los resultados son claros, pero su interpretación debe reducirse.

- La cobertura **1.821/1.821** es impresionante como ingeniería, pero no como validación científica.
- La mejora principal, ILD **0,4216 → 0,5265**, es esperable porque MMR optimiza una función estrechamente relacionada.
- La comparación con deduplicación exacta es reveladora: elimina todas las repeticiones con pérdida de similitud de solo **0,0006**, pero ILD solo sube a **0,4373**. Esto favorece a MMR solo si se acepta la métrica ILD como constructo relevante.
- El resultado por tarea es irregular. En “pronóstico a un paso”, cambio medio ILD **0,0145**, con **71 mejoras y 65 disminuciones**, p = **0,504**. Esto debilita la afirmación de estabilidad entre funciones.

La Tabla 4 ayuda, pero es insuficiente. El ejemplo muestra variedad de firmas, no que esas recomendaciones sean mejores o útiles.

## Discusión

La discusión es inusualmente honesta. Dice explícitamente que P1 es éxito técnico, que P2 no implica equivalencia práctica y que P3 podría requerir λ por tarea.

Sin embargo, la discusión usa la honestidad para posponer problemas centrales. Declarar que no hay fidelidad semántica ni utilidad humana no basta; para publicación fuerte, al menos una muestra anotada por expertos debería estar incluida.

La frase **“materializa una ruta automática desde literatura reciente hasta un DSS heredado”** es defendible, pero solo como ruta técnica, no como adquisición fiable de conocimiento.

## Amenazas a la validez

Es una sección muy buena, pero paradójicamente contiene razones suficientes para una revisión mayor:

- **“No existe ground truth de utilidad ni evaluación con usuarios.”**
- **“No se anotaron precisión, exhaustividad o F1.”**
- **“Todos los tipos de activo y modalidades de entrada se descartaron.”**
- **“Solo aparecieron 848 rankings baseline y 699 rankings MMR ordenados.”**

Estas amenazas no son menores; afectan al núcleo de la contribución.

## Conclusiones

Las conclusiones están bien acotadas: **“interoperabilidad y comportamiento del ranking, no exactitud semántica ni valor para decisiones reales.”** Eso es positivo.

Pero para una revista de sistemas inteligentes, la conclusión puede parecer demasiado limitada: se demuestra que una cadena ejecuta y que MMR diversifica según su propia métrica. Falta evidencia de inteligencia útil, calidad de conocimiento o impacto en decisión.

## Disponibilidad / código / apéndice

La sección es buena en intención, pero necesita reforzarse.

Problemas probables:

- Los PDFs no se redistribuyen, comprensible por licencia, pero entonces la reproducibilidad completa queda limitada.
- El manifiesto tiene **1.797 enlaces exactos o casi exactos**, pero también **25 enlaces no exactos** de confianza alta/media/baja. Esto debe tratarse con más fuerza: ¿se excluyeron en análisis de sensibilidad?
- El comando usa rutas locales como `.venv/Scripts/python.exe`, `ontocast_runs/run_*/output/facts_*.ttl` y una case base externa. Falta una descripción tipo contenedor, commit, DOI, versiones y licencia.
- El apéndice de 19 campos es útil, pero debería acompañarse de estadísticas de completitud por campo en el cuerpo principal.

# 3. Fortalezas principales

- Contribución técnica clara y modular.
- Corpus grande: **1.821 documentos únicos**.
- Buena transparencia sobre limitaciones.
- Pipeline reproducible en principio, con scripts, semillas, CSV y checksums.
- Evaluación pareada apropiada para comparar rankings.
- Sensibilidad a λ y comparadores simples.
- Ablación importante de **Unknown synchronization**.
- Buena delimitación entre interoperabilidad, diversidad algorítmica y calidad semántica.

# 4. Debilidades críticas que un revisor experto atacaría

1. **No hay validación semántica de la extracción.** Sin precisión, recall, F1 o auditoría experta, no sabemos si las consultas representan los artículos.

2. **La métrica principal es circular.** ILD usa la misma función de similitud de solución que MMR optimiza.

3. **El resultado de P1 es sintáctico.** Parsear y consultar no equivale a poblar correctamente una ontología ni a recuperar conocimiento útil.

4. **Demasiados defaults y campos descartados.** El esquema tiene 19 campos, pero varios no se usan efectivamente; tipo de activo y modalidad se descartan en todas las consultas.

5. **Heterogeneidad LLM no controlada.** Tres modelos distintos produjeron artefactos finales.

6. **Base CBR pequeña y rankings repetidos.** Solo **263 casos históricos** y fuerte pseudorreplicación de rankings.

7. **No hay evaluación con usuarios ni arquitectos.** La utilidad de la diversidad es asumida, no demostrada.

8. **Comparador trivial fuerte.** La deduplicación exacta elimina todas las repeticiones con pérdida mínima de similitud; MMR solo gana claramente bajo la ILD definida por los autores.

# 5. Cambios prioritarios antes de enviar

1. **Añadir validación experta de extracción** sobre una muestra estratificada: tarea, modelo LLM, calidad de enlace PDF-facts, campos clave. Reportar precisión/recall/F1 o acuerdo interanotador.

2. **Incluir métricas de completitud por campo**: cuántas consultas tienen tarea real, activo, variables, modelos, desempeño, sincronización, identificador, etc.

3. **Reformular P1-P3** para dejar claro que son preguntas de interoperabilidad/ranking, no de calidad de conocimiento.

4. **Añadir análisis por modelo LLM usado**: gpt-5-mini vs gpt-5.4-mini vs gpt-5.6-luna en completitud, tareas, similitud e ILD.

5. **Hacer sensibilidad de los pesos de `s_sol`**, no solo de λ.

6. **Fortalecer comparación con baselines**: deduplicación exacta, MMR sin preservar top-1, MMR con distintos pool sizes, quizá xQuAD/submodular si aplica.

7. **Tratar pseudorreplicación con cluster bootstrap** por firma normalizada o ranking baseline.

8. **Mejorar paquete reproducible**: DOI, licencia, versiones, entorno, contenedor, prompts, hashes, manifest completo y script de reproducción desde artefactos canónicos.

# 6. Riesgo de claims exagerados o insuficientemente probados

Riesgo moderado. El manuscrito es cuidadoso, pero algunas expresiones siguen siendo vulnerables:

- **“reproducible pipeline”**: parcialmente cierto, pero dependiente de PDFs no redistribuidos, LLMs/versiones y trazabilidad incompleta.
- **“transformar un corpus amplio en consultas técnicamente compatibles”**: defendible, pero debe evitar insinuar extracción correcta.
- **“estabilidad entre funciones”**: débil por estratos pequeños y el caso de pronóstico a un paso.
- **“diversidad”**: debería llamarse siempre **diversidad algorítmica según `s_sol`**, no diversidad funcional o utilidad.
- **“interoperabilidad”**: sí técnica; no necesariamente semántica.

Mi recomendación: mantener el tono honesto actual, pero añadir una validación semántica mínima. Sin ella, el artículo probablemente recibirá **major revision**; en una revista exigente podría ser rechazado por falta de evidencia independiente.
