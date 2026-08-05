# Pausa y replanteamiento de preguntas de investigación

## Diagnóstico

El manuscrito actual documenta de forma completa la implementación OntoCast--OPMAD--CBR--MMR, pero sus preguntas principales son internas al sistema:

- cobertura ejecutable del puente;
- compromiso similitud--diversidad de MMR;
- sensibilidad de parámetros y sanity checks.

Eso produce una contribución de ingeniería reproducible, pero no basta si el objetivo es una publicación científica con una contribución metodológica más fuerte. Además, los parámetros de diversidad y la relación cobertura--diversidad ya fueron tratados en `guide_papers/Paper_Emmannuel.md`; en este manuscrito deberían quedar como análisis secundario o validación de implementación, no como eje del paper.

## Eje recomendado

Recentrar el artículo en OntoCast como método de extracción ontológicamente guiada desde textos completos de artículos científicos de mantenimiento predictivo.

La pregunta general podría ser:

> ¿En qué medida una ontología experta como OPMAD mejora la extracción estructurada de conocimiento desde textos completos, frente a esquemas/ontologías inducidas por modelos de lenguaje y frente a extracción no guiada?

El CBR y la diversidad pueden quedar como tarea downstream demostrativa, no como contribución principal.

## Preguntas de investigación propuestas

### RQ1. Valor de la guía ontológica

¿La extracción OntoCast condicionada por OPMAD produce hechos más correctos, completos y consistentes que la extracción sin ontología o con un esquema genérico?

**Comparadores posibles:**
- OntoCast + OPMAD fija;
- LLM con JSON/schema manual mínimo;
- LLM libre con posterior normalización;
- extracción desde título/resumen como baseline débil.

**Métricas:** precisión, exhaustividad y F1 de entidades/relaciones; tasa de alucinación; conformidad SHACL; evidencia textual trazable.

### RQ2. Ontología experta vs. ontologías generadas por LLM

¿Cómo se compara OPMAD con ontologías o esquemas generados automáticamente por distintos modelos de lenguaje para el mismo corpus y las mismas competency questions?

**Diseño:** pedir a varios LLM que generen una ontología/esquema para extracción de mantenimiento predictivo; usar cada ontología/esquema para extraer los mismos documentos; comparar contra OPMAD.

**Métricas:** cobertura de conceptos expertos, granularidad útil, redundancia, estabilidad entre modelos, facilidad de mapeo a OPMAD/CBR, calidad factual de las extracciones resultantes.

### RQ3. Aporte del texto completo

¿Qué información relevante para mantenimiento predictivo solo se recupera al usar texto completo y no título/resumen/keywords?

**Comparadores:**
- título + resumen;
- introducción/conclusiones;
- métodos/resultados;
- texto completo.

**Métricas:** incremento de recuperación de activos, variables, modelos, preprocesamiento, métricas de desempeño y relaciones modelo--tarea; coste en ruido/alucinación.

### RQ4. Robustez entre modelos de lenguaje

¿La guía ontológica reduce la variabilidad entre modelos de lenguaje en la extracción de hechos desde textos completos?

**Diseño:** ejecutar los mismos documentos con varios modelos bajo dos condiciones: con OPMAD y sin OPMAD / con ontología inducida.

**Métricas:** acuerdo entre modelos, varianza de cobertura, estabilidad de clases/relaciones, consistencia de normalización, cambios en errores críticos.

### RQ5. Utilidad downstream de los hechos extraídos

¿Los hechos extraídos con mayor fidelidad mejoran tareas downstream de decisión, como consulta a CBR o selección de modelos candidatos?

**Rol del CBR:** evaluación secundaria. No preguntar si el adaptador funciona ni si MMR aumenta diversidad; preguntar si una extracción mejor produce recomendaciones más relevantes para expertos.

**Métricas:** juicio experto de relevancia/utilidad/novedad, concordancia con casos esperados, calidad de justificación por evidencia textual.

## Qué mover a análisis secundario

- Ejecución por lotes de myCBR: detalle metodológico/reproducibilidad, no contribución científica central.
- MMR, pool, lambda, k y pesos: análisis downstream o suplemento; no preguntas principales.
- Ablaciones de atributos y recencia: sanity checks del puente CBR.
- SHACL/cobertura de campos: métricas de calidad/interoperabilidad para apoyar RQ1, no fin en sí mismas.

## Diseño mínimo viable para reorientar el paper

1. Construir un corpus dorado estratificado de artículos completos, por ejemplo 80--120 PDFs.
2. Definir competency questions de OPMAD: activo, tarea, variables, modelos, preprocesamiento, configuración, desempeño, evidencia textual.
3. Hacer doble anotación experta o al menos adjudicación experta.
4. Ejecutar OntoCast + OPMAD y 2--3 comparadores LLM.
5. Reportar calidad factual y consistencia estructural.
6. Usar la cadena CBR/MMR solo como demostración downstream: qué cambia cuando la extracción es más fiel.

## Implementación experimental añadida

Los scripts quedan documentados en `paper/experiments/README.md`:

- `prepare_gold_sample.py`: muestra estratificada y plantilla `gold_template.jsonl`.
- `predictions_from_facts.py`: baseline OntoCast+OPMAD desde los facts TTL existentes.
- `build_evidence_packages.py`: paquetes de evidencia `abstract`, `metadata`, `sections` y `fulltext` desde Scopus y textos preconvertidos.
- `generate_llm_schema_or_ontology.py`: generación seca o real de schema/ontología LLM para RQ2.
- `run_llm_json_extraction.py`: comparadores `generic_json`, `llm_schema` y `llm_ontology` con modo `--dry-run` y ejecución real OpenAI-compatible.
- `evaluate_extraction.py`: precisión, exhaustividad, F1, coincidencia exacta y tasa de alucinación por campo.
- `predictions_to_cbr_queries.py`: preparación de consultas CBR downstream para RQ5 sin ejecutar Java ni MMR.
- `build_experiment_matrix.py`: matriz preregistrable de condiciones, modelos y scopes.

## Narrativa de contribución resultante

El paper dejaría de ser "documentamos un pipeline que corre" y pasaría a ser:

> una evaluación controlada de extracción ontológicamente guiada desde textos completos científicos, usando OPMAD como ontología experta y comparándola contra esquemas inducidos por modelos de lenguaje, con una tarea downstream de recuperación CBR para mostrar el impacto práctico de la calidad de extracción.
