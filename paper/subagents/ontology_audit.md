No modifiqué archivos.

## 1) Resumen ejecutivo

El pipeline es defendible como **prototipo de extracción RDF/OWL asistida por LLM con puente conservador a un CSV CBR de 19 campos**, pero no todavía como extractor semánticamente validado ni como población completa/fiel de una base de casos OPMAD.

Hallazgos principales:

- `pipeline/seed_ontology/opmad_seed.ttl` es sintácticamente válido y contiene todos los términos necesarios para el esquema de 19 campos: 56 clases OWL, 15 object properties y 2 datatype properties.
- Los facts TTL crudos usan RDF-star/RDF 1.2-like con `rdf:reifies <<( ... )>>`; **0/1831** facts parsean directamente con `rdflib`, pero **1831/1831** parsean tras el cleanup de `facts_to_csv.py`.
- Ese cleanup elimina la reificación/provenance; se pierden unas **313k declaraciones RDF-star/prov**.
- Hay fuerte inconsistencia de namespaces: muchos facts usan `OPMAD/seed#` mientras la semilla define las clases en `OPMAD#`; 990 files mezclan ambos namespaces.
- La conversión a CSV valida sintácticamente, pero pierde mucha información y rellena defaults agresivos: `module_synchronization`, `performance_indicator`, `performance` y `number_of_failure_modes` salen siempre como default aunque muchos TTL contienen evidencia directa.
- `facts_to_csv.py` tiene un problema importante si se usa con múltiples TTL a la vez: combina todos los grafos y luego escoge un único task/case/model set global, contaminando documentos entre sí.
- El benchmark de 10 documentos apoya solo una afirmación débil/preliminar: `gpt-5.6-luna` fue mejor que el baseline en esa muestra pequeña, pero con puntuaciones absolutas bajas y sin gold standard humano.

## 2) Evidencia revisada

Audité:

- `pipeline/seed_ontology/opmad_seed.ttl`
- `pipeline/extraction_schema.py`
- `pipeline/facts_to_csv.py`
- `pipeline/SCHEMA_MAPPING.md`
- Facts TTL de todas las ejecuciones en `extraction_papers/ontocast_runs/*/output/`
- Benchmark en `extraction_papers/ontocast_runs/model_benchmark_gpt-5.6-luna_20260722_180908/`

Pruebas:

- `python -m unittest pipeline.tests.test_extraction_schema pipeline.tests.test_facts_to_csv` → **OK, 11 tests**.
- Validación agregada: 1831 fact TTL, 1821 nombres únicos; 10 duplicados son los documentos del benchmark.

## 3) RDF-star, sintaxis y namespaces

### Sintaxis

- Raw TTL: **0/1831 parsean directamente** con `rdflib`.
- Tras `strip_rdf_star_statements`: **1831/1831 parsean**.
- Regular triples tras cleanup: **342,231**.
- Reification blocks eliminados: **313,383**.
- Solo encontré 5 literales ill-typed después del cleanup, por ejemplo decimals/date/integer mal lexicalizados.

Conclusión: puede afirmarse “parseable after RDF-star cleanup”, no “RDF TTL directamente interoperable con herramientas RDF 1.1 estándar”.

### Namespaces

Problemas:

- La seed ontology declara clases como `http://.../OPMAD#Class`, pero muchos facts usan `http://.../OPMAD/seed#Class`.
- La prefix `None:` es legal Turtle, pero mala práctica y confusa.
- Se mezclan `https://schema.org/` y `http://schema.org/`.
- También aparecen vocabularios no mapeados como `cd:`, `dcterms:`, `csvw:`, propiedades generadas tipo `doc:factscauses_1`.

Estadística namespace:

- 990 fact files mezclan `OPMAD#` y `OPMAD/seed#`.
- 710 usan solo `OPMAD/seed#`.
- 100 usan solo `OPMAD#`.
- 31 no contienen términos OPMAD relevantes.

## 4) Cobertura del esquema de 19 campos

La seed ontology cubre todos los términos declarados por `extraction_schema.py`. El problema está en la extracción/conversión, no en que falten clases básicas.

| Campo CSV | Evidencia directa en TTL | Salida bridge CSV | Riesgo |
|---|---:|---:|---|
| Reference | generado | siempre | no estable entre conversiones por fichero |
| Publication Year | 91.9% files | 30.7% no-default | ignora muchas rutas `has_publication_year` |
| Task | 96.4% files | 100% | default oculto a “One step…” cuando falta |
| Case study | 95.6% | 95.7% | razonable pero toma primer item |
| Case study type | 66.9% | 100% | normalmente genérico “Maintainable item” |
| Input for model | 16.1% | 1.7% | casi siempre `Not reported` |
| Number input vars | 6.7% exacto / 84.6% variables | 84.5% | computado por conteo, no siempre textual |
| Input type | 84.6% | 84.5% | multivalor plano por comas |
| Data preprocessing | 73.4% design detail | yes/no siempre | inferido de design details, no campo real |
| Model approach | 41.3% | 100% | inferido por número de modelos |
| Model type | 64.6% | 65.7% | puede incluir clases no-modelo |
| Models | 80.0% | 73.8% | pérdida y mezcla posible |
| Online/Off-line | 29.1% | 0% | siempre `Unknown synchronization` |
| Number failure modes | 14.5% | 0% | siempre `0`, confunde unknown con cero |
| Performance indicator | 74.0% | 0% | siempre `Not reported` |
| Performance | 68.1% | 0% | siempre `Not reported` |
| Complementary notes | 73.4%+keywords | 80.1% | mezcla keywords/design/instruments |
| Study title | 97.6% | 94.7% | ignora a veces `has_title` → usa local name |
| Publication identifier | 77.8% | 1.2% | casi siempre URN generado |

## 5) Pérdida de información al convertir a 19 campos

La pérdida es significativa:

- Se elimina provenance RDF-star por chunk.
- Se descartan autores, afiliaciones, datasets, métricas detalladas, métodos, relaciones causales, parámetros, DOI estructurado, etc.
- `performance` y `performance_indicator` existen en muchos TTL, pero el bridge no los materializa.
- `has_synchronization` existe en ~29% de files, pero no se extrae.
- Unknown se convierte en valores plausibles: `2021`, `0`, `One step future state forecast`, `Single model`.
- Los multivalores se serializan con comas; si un nombre contiene coma, no hay round-trip limpio.
- Si se pasan múltiples facts al CLI, se combinan en un solo grafo y se pueden contaminar campos entre documentos.

## 6) Calidad semántica observada

Hay validez sintáctica después de cleanup, pero calidad semántica heterogénea:

- Se observan recursos con múltiples nombres contradictorios, p.ej. una persona con varios `schema:name`.
- A veces clases de OPMAD aparecen como individuos/document resources.
- Hay self-relations y triples poco significativos.
- Algunos retries generan facts casi solo `schema.org`, sin contenido de mantenimiento predictivo.
- Ejemplo: `run_retry_final_8_sanitized.../facts_f2bee3e4193d.ttl` describe indexing/journal metadata, no un caso OPMAD útil.

Por tanto, no basta decir “TTL válido”; hay que separar parseability de fidelity/semantic usefulness.

## 7) Benchmark de 10 documentos

Defendible:

- Comparación controlada de 10 documentos, fixed ontology, facts-only, `head_chunks=3`.
- Todos los 20 outputs parsean tras cleanup.
- `gpt-5.6-luna` supera al baseline en esta muestra: 6/10 wins, score total 55 vs 49, media 5.5 vs 4.9, +14.9% triples.
- Trade-off: latencia media candidata 36.55s/request vs baseline histórico 18.36s.

No defendible:

- Superioridad general estadísticamente significativa.
- Precisión/recall real del extractor.
- Calidad absoluta alta: las medias son bajas sobre 15.
- Evaluación humana: el juez fue LLM, no anotadores expertos.
- Extracción full-paper: se usaron primeras páginas/chunks.

## 8) Qué puede afirmarse en un paper

Sí:

- “Construimos una seed ontology OPMAD autocontenida para fixed-ontology extraction.”
- “Definimos un esquema Pydantic de 19 campos compatible con el CSV CBR.”
- “Generamos 1821 artefactos TTL únicos; todos son parseables como RDF regular tras eliminar reificación RDF-star.”
- “El bridge produce CSV sintácticamente válido con defaults conservadores.”
- “Un benchmark preliminar de 10 documentos favoreció a `gpt-5.6-luna` frente al baseline.”

No:

- “El sistema extrae completos los 19 campos.”
- “Los CSV resultantes son semánticamente fieles al paper.”
- “La ontology valida o garantiza consistencia OWL.”
- “Los facts son RDF-star interoperable sin postproceso.”
- “El benchmark demuestra superioridad general del modelo.”

## 9) Amenazas a validez

- Defaults inflan validez sintáctica.
- No hay gold standard humano.
- RDF-star se elimina, perdiendo provenance.
- Namespace mismatch `OPMAD#` vs `OPMAD/seed#`.
- Posible contaminación multi-documento en `facts_to_csv.py`.
- Evaluador LLM en benchmark.
- Solo primeras páginas/chunks.
- Reintentos y duplicados entre ejecuciones.
- Model/proxy drift: configs y logs no siempre nombran igual el modelo real.

## 10) Mejoras futuras prioritarias

1. Normalizar namespace a `OPMAD#`; eliminar prefix `None:`.
2. Convertir cada fact TTL independientemente; no combinar grafos salvo con named graphs.
3. Extraer rutas OPMAD reales: `has_title`, `has_identifier`, `has_publication_year`, `has_synchronization`, performance, failure modes.
4. Reemplazar defaults engañosos por `Unknown/Not reported` explícito o campos nullable.
5. Preservar RDF-star provenance o convertirla a named graphs/reificación RDF 1.1.
6. Añadir SHACL shapes para los 19 campos.
7. Añadir tests de multi-file conversion, namespaces mixtos y performance/sync extraction.
8. Evaluar con muestra estratificada humana y métricas precision/recall/F1.
