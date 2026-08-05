# Protocolo preregistrado para validación semántica experta

## Estado

**No ejecutado.** `expert_validation_sample_template.csv` es una plantilla estratificada y no contiene juicios humanos. Ningún resultado del manuscrito se presenta como precisión, exhaustividad, F1 o utilidad humana.

## Objetivo

Estimar fidelidad factual y completitud del puente PDF → hechos RDF → consulta CBR para los campos que determinan la recuperación: tarea, activo, variables de entrada, modelos y título/identificador del estudio fuente.

## Muestra

La plantilla se seleccionó con semilla `20260727`, estratificando por modelo de extracción y tarea. El objetivo operativo es 96 documentos, ampliable a 120 si algún estrato queda con menos de 10 unidades. Deben conservarse los estratos pequeños completos y sobremuestrearse los 25 enlaces PDF--facts no exactos.

## Anotadores

- Dos especialistas independientes en mantenimiento predictivo y representación del conocimiento.
- Sin acceso al ranking CBR/MMR durante la anotación.
- Piloto conjunto de 10 documentos que no se incluirá en la estimación final.
- Desacuerdos resueltos por un tercer experto o una sesión de adjudicación documentada.

## Unidad y evidencia

Cada anotador debe revisar el PDF completo, no solo los chunks enviados al extractor. Para cada campo registra:

1. valor de referencia respaldado por el documento;
2. valor extraído;
3. clase de resultado: correcto, parcialmente correcto, incorrecto, no reportado en la fuente o no aplicable;
4. página/sección que sustenta el juicio;
5. si la entidad corresponde al estudio fuente o a un trabajo citado.

## Métricas

- Campos categóricos de valor único: exactitud, macro-F1 y Cohen κ.
- Campos multivalor: precisión, exhaustividad y F1 micro/macro por conjunto.
- Texto libre: coincidencia normalizada y juicio ordinal 0/1/2, con κ ponderada.
- Identificación del estudio fuente: exactitud binaria.
- Cobertura: proporción con evidencia presente en el PDF y proporción recuperada.
- Resultados estratificados por tarea, modelo LLM, chunks y confianza del enlace PDF--facts.

Los intervalos serán bootstrap por documento. Deben publicarse ejemplos de falsos positivos, falsos negativos y errores de atribución a citas.

## Evaluación humana de las recomendaciones

En una fase separada, arquitectos de mantenimiento compararán listas CBR y CBR+MMR en orden aleatorio y ciego. Medidas mínimas: relevancia, novedad percibida, utilidad para explorar alternativas, confianza, tiempo de decisión y elección final. La diversidad algorítmica no se usará como sustituto de estas medidas.
