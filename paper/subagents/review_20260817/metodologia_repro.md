No edité archivos. Revisé `paper/main copy.tex` y los artefactos indicados.

## 1) Qué demuestra realmente el diseño y qué NO demuestra

**Sí demuestra:**
- Que, para los **1.821 documentos únicos con PDF/facts**, existe una cadena ejecutable: facts Turtle → limpieza RDF-star → CSV/consulta → myCBR → MMR.
- Que el reranking **MMR, con la propia función de similitud de solución usada para medir ILD**, aumenta diversidad algorítmica: ILD 0,4216 → 0,5265; listas con modelos repetidos 610 → 5; similitud media top-5 0,5563 → 0,5536.
- Que hay trazas computacionales útiles: hashes, manifest, cobertura de campos, sesgo de disponibilidad PDF, SHACL, bootstrap por clúster, sensibilidad de MMR.

**No demuestra:**
- Que OntoCast extraiga hechos correctos del texto/PDF.
- Que OPMAD sea mejor que JSON genérico, schema generado por LLM u ontología generada por LLM: esos experimentos están planificados, no ejecutados.
- Que las recomendaciones myCBR sean relevantes o útiles para expertos.
- Que la diversidad MMR mejore decisiones humanas.
- Que el corpus sea representativo: 946/2768 incluidos no tienen PDF, con sesgo fuerte por año/editor/OA.
- Que se haya procesado texto completo: el manifest muestra principalmente `chunks=3` y algunos `chunks=1`.
- Que haya interoperabilidad semántica plena: solo **126/1821** artifacts conforman SHACL mínimo; varios campos clave tienen 0% cobertura informativa.

Además, `paper/main copy.tex` no contiene secciones de Resultados, Discusión ni Conclusiones; los resultados aparecen casi solo en el abstract.

---

## 2) Crítica por componente

### Buscador / Scopus
- La consulta está documentada, pero el diseño es **Scopus-only**, inglés, artículos, 2025–2026; eso limita generalización.
- El cribado tiene criterios detallados, pero falta describir quién cribó, si hubo doble revisión, adjudicación o acuerdo interevaluador.
- La disponibilidad PDF no es aleatoria: 2025 recupera 69,7%, 2026 58,2%; `gold` 74,2%, `hybrid_gold` 33,3%. Por DOI/editor hay sesgos extremos, p.ej. `10.3390` casi completo y `10.1016` muy bajo.
- El corpus analizado es realmente “documentos con PDF recuperado”, no todos los incluidos.

### PDF / texto
- No hay paquetes de texto congelado ni evidencia por página/chunk; por tanto no se puede auditar la entrada real al LLM.
- El pipeline usa `chunks=3` para 1802 casos y `chunks=1` para 19; esto explica que desempeño, modos de falla y sincronización queden vacíos. El manuscrito debe declararlo explícitamente.
- Hay 25 enlaces PDF–facts no exactos; parte del enlace se reconstruye por matching de título porque logs antiguos no conservaron el vínculo.
- El protocolo de validación es inconsistente: el manuscrito dice “texto congelado, no auditar PDF→texto”; el suplemento experto dice “revisar PDF completo”.

### OntoCast / OPMAD
- Buena decisión: usar una OPMAD fija evita ontologías generadas arbitrariamente.
- Problema: extracción con modelos cerrados, varios modelos (`gpt-5-mini`, `gpt-5.4-mini`, `gpt-5.6-luna`) y temperatura 1.0 en logs; no es determinista.
- Hay efecto de lote/modelo: `gpt-5.6-luna` tiene mayor media de campos informativos que otros lotes; no fue asignación aleatoria.
- El benchmark de modelo fue de 10 papers y juez LLM, no humano.
- OPMAD no queda validada como restricción semántica: SHACL mínimo falla masivamente.

### RDF-star / procedencia
- Se retiraron **311.559** bloques RDF-star para parsear con RDF 1.1.
- Existe sidecar comprimido, pero la procedencia no está integrada campo-a-campo en el CSV ni en la consulta myCBR.
- La afirmación de trazabilidad debe acotarse: hay preservación auxiliar, no trazabilidad operacional completa desde recomendación → campo → triple → chunk/página.

### `facts_to_csv` / 19 campos
- El “esquema de 19 campos” es en gran parte nominal:
  - sincronización informativa: 0/1821;
  - desempeño: 0/1821;
  - modos de falla: 0/1821;
  - tipo de activo: 0%;
  - input-for-model: 1,26%;
  - publication identifier: 1,43%;
  - study title: 47,94%.
- Normalización myCBR activa solo: tarea 100%, activo 85%, input type 75,8%; tipo, sincronización e input modality quedan en 0.
- En 409 artifacts había más de un caso y se ignoraron 567 casos adicionales; seleccionar el primero determinísticamente no garantiza que sea el estudio fuente.
- Varios valores `Facts*` pasan como señales si hay múltiples inputs; eso puede introducir ruido.

### myCBR
- La base histórica de 263 casos sirve como infraestructura downstream, no como verdad.
- La recuperación está fuertemente determinada por pocos campos activos y por año/tarea.
- Las ablaciones muestran sensibilidad importante: `task_year_only` produce solo 8 patrones de ranking y cambia 1361 top-1 frente al main.
- No hay ground truth de “caso correcto” ni evaluación humana de relevancia.

### MMR
- MMR funciona como postproceso reversible y está bien delimitado algorítmicamente.
- Pero el resultado principal es parcialmente circular: se optimiza una similitud de solución y se evalúa con ILD basada en esa misma similitud.
- Top-1 preservado y similitud top-1 idéntica son consecuencia del diseño, no hallazgo.
- Comparadores muestran que MMR no es único: max-sum da ILD mayor; deduplicación elimina repetidos con menor coste de similitud.
- Falta validación de que la diversidad algorítmica sea útil para usuarios.

---

## 3) Riesgos metodológicos concretos

| Severidad | Riesgo |
|---|---|
| Crítica | No hay validación humana de fidelidad factual. |
| Crítica | `paper/main copy.tex` carece de Resultados/Discusión/Conclusiones pese a presentar resultados en el abstract. |
| Crítica | Se sugiere extracción desde literatura/PDF, pero realmente se usaron pocos chunks. |
| Alta | 946 registros incluidos sin PDF generan sesgo de selección. |
| Alta | SHACL mínimo: solo 126/1821 artifacts conformes. |
| Alta | Campos clave de decisión tienen 0% cobertura informativa. |
| Alta | 409 artifacts multi-caso; 567 casos ignorados por regla débil. |
| Alta | Modelos LLM cerrados, temperatura 1.0 y varios lotes/modelos confunden resultados. |
| Media-Alta | PDF–facts linkage parcialmente reconstruido por título. |
| Media | Pseudorreplicación: 1821 consultas pero 848 rankings baseline únicos y 699 MMR únicos. |
| Media | Métrica ILD no independiente del objetivo MMR. |
| Media | Reproducibilidad incompleta: README apunta a `paper/main.tex`, pero no existe; manifest de software tiene commit distinto al actual. |

---

## 4) Evidencias/artefactos que faltan

En manuscrito:
- Resultados completos con tablas de cobertura, SHACL, PDF bias, MMR, sensibilidad y pseudorreplicación.
- Amenazas de validez explícitas.
- Declaración clara de “no validamos fidelidad factual ni utilidad humana”.
- Descripción de chunks, modelos, temperatura, retries y mezcla de lotes.
- Tabla de campos realmente activos en myCBR.
- Disponibilidad de datos/código con commit, hashes y rutas correctas.

En suplemento:
- Gold standard anotado por expertos.
- Texto/chunks congelados usados por OntoCast.
- Evidencia campo-a-campo: valor extraído → triple → chunk/página/frase.
- Raw top-15 pools y listas rerankeadas, no solo métricas agregadas.
- Acuerdo interanotador del cribado Scopus o al menos protocolo ejecutado.
- Resultados reales de baselines JSON/schema/ontology LLM.
- Lockfile reproducible (`uv.lock`, conda env o Dockerfile).
- Manifest actualizado al commit actual y al archivo LaTeX real.

---

## 5) Cambios exactos para dejar la metodología publicable

1. **Reescribir `paper/main copy.tex`**: añadir Resultados, Discusión, Limitaciones y Reproducibilidad; mover los números del abstract a tablas verificables.
2. **Declarar explícitamente**: “Este estudio evalúa interoperabilidad computacional y reranking, no fidelidad factual ni utilidad humana”.
3. **Corregir alcance PDF/texto**: indicar `chunks=3`/`chunks=1`; no llamar “texto completo” si no lo fue.
4. **Ejecutar validación experta** mínima: 96–120 documentos, dos anotadores, adjudicación, F1/precisión/recall por campo, κ, errores por cita vs estudio fuente.
5. **Alinear protocolos**: decidir si la validación será contra texto congelado o PDF completo; no mantener ambas versiones.
6. **Publicar tabla de cobertura de 19 campos** y distinguir campos informativos, derivados y defaults.
7. **Modificar `facts_to_csv` o el método** para seleccionar el estudio fuente por DOI/título/evidencia, no primer caso determinístico.
8. **No pasar `Facts*` como evidencia**; clasificarlos como placeholders salvo evidencia textual.
9. **Agregar trazabilidad campo-a-campo** enlazando CSV/query con RDF-star sidecar y fragmento textual.
10. **Presentar SHACL como limitación**, o corregir extracción hasta obtener conformidad estructural aceptable.
11. **Ejecutar o retirar los baselines LLM** prometidos en RQ4/RQ2.
12. **Describir myCBR completamente**: casebase, distribución, pesos, año, función de similitud y ablations.
13. **Acotar MMR** como trade-off algorítmico; no afirmar mejora de recomendación sin estudio de usuarios.
14. **Actualizar reproducibilidad**: restaurar o renombrar `paper/main.tex`, actualizar `software_manifest.json`, incluir lockfile y archivar facts/query/pools/resultados con DOI.
