No edité archivos. Revisé `paper/main copy.tex`, `paper/main_copy_en.tex`, `references.bib`, figuras y suplemento.

## 1) Problemas por prioridad

### Críticos
1. **`paper/main copy.tex` no es enviable tal cual**: termina en Métodos y bibliografía. No contiene Resultados, Discusión, Limitaciones ni Conclusión, aunque el abstract sí anuncia resultados fuertes.
2. **Claims demasiado adelantados al cuerpo**: el manuscrito demuestra interoperabilidad ejecutable y efecto algorítmico de MMR, no fidelidad factual ni utilidad decisional.
3. **Validación humana no ejecutada**: debe presentarse como protocolo/futuro, no como evidencia. Además hay conflicto: el manuscrito habla de “texto congelado”, pero `expert_validation_protocol.md` dice revisar PDF completo.
4. **Cobertura semántica limitada debe ir al cuerpo**: SHACL conforme solo 126/1821; sincronización, desempeño, modos de falla y tipo de caso tienen 0% informativo; tras normalización básicamente sobreviven tarea, activo e input type.
5. **Keywords vacíos en `main copy.tex`**; en `main_copy_en.tex`, “human evaluation” es engañoso si no hubo evaluación humana.

### Importantes
- Título no refleja CBR/diversidad, que son parte central del paper.
- Abstract demasiado denso: contiene corpus, pipeline, parámetros, comparadores y limitaciones en un solo bloque.
- Falta integrar tablas/figuras de resultados ya existentes en `paper/figures/` y suplemento.
- Figuras generadas tienen etiquetas en español; para envío internacional deben regenerarse en inglés.
- Inconsistencias documentales: `paper/README.md` apunta a `paper/main.tex`, que no existe; revisar V12/V21 en documentación.
- La sección de métodos es sólida pero muy larga para no tener resultados después.

### Menores/formato
- En PDF aparece “section 3.7” en español: falta `\crefname{section}{sección}{secciones}` si se mantiene español.
- Contribución (v) en la lista no termina con puntuación.
- Estandarizar “RDF-star”/“RDF*”, “ILD”/“ild”, OPMAD/opmad, myCBR.
- `main_copy_en.tex` compila en IEEEtran y es mejor base formal que `article`, pero también está incompleto.

---

## 2) Cambios concretos a título, abstract, keywords, introducción y contribuciones

### Título recomendado, en inglés
**From Predictive-Maintenance Papers to Diverse Case-Based Recommendations: An Audited OntoCast--OPMAD Pipeline**

Alternativa más técnica:

**Auditing Ontology-Guided Literature Extraction for Predictive-Maintenance CBR and Diversity-Aware Retrieval**

### Keywords
Usaría 5–6:

**Ontology-guided information extraction; predictive maintenance; case-based reasoning; knowledge graphs; large language models; diversity-aware retrieval.**

Evitaría “human evaluation” hasta ejecutar expertos.

### Abstract recomendado, versión internacional

> Predictive-maintenance papers describe assets, signals, tasks, and models that could support case-based design decisions, but converting this literature into structured and auditable inputs remains difficult. This study evaluates an audited pipeline that uses OntoCast constrained by OPMAD to extract RDF/Turtle facts, maps them to a 19-field CBR schema, generates myCBR queries, and analyzes diversity-aware retrieval through maximal marginal relevance. From 3,990 Scopus records published in 2025--2026, 2,768 met the screening criteria and 1,821 unique full-text documents were processed. All documents produced parseable artifacts and executable queries against a historical base of 263 cases after RDF-star cleanup. However, field-level audits revealed substantial semantic loss: several schema fields remained defaults or were discarded during normalization, so executable interoperability should not be interpreted as factual accuracy. In the downstream retrieval task, MMR with pool 15, top-5, and λ=0.70 increased mean intra-list dissimilarity from 0.4216 to 0.5265 and reduced lists with repeated model signatures from 610 to 5, while mean top-5 CBR similarity decreased from 0.5563 to 0.5536. Sensitivity analyses, cluster bootstrap, max-sum, and MAP-DPP comparators showed a configurable relevance-diversity trade-off rather than universal superiority. The results support auditable interoperability and controlled ranking behavior; semantic fidelity and decision utility require expert validation.

### Introducción
Añadir temprano un párrafo puente más directo:

> In practical terms, the pipeline receives a predictive-maintenance paper, extracts OPMAD-compatible facts, converts them into the attributes required by an existing myCBR system, and reranks the retrieved cases to reduce redundant model recommendations.

Después, dejar claro:

- No se propone nueva ontología.
- No se propone nuevo CBR.
- No se propone nuevo algoritmo de diversidad.
- La contribución es la **interoperabilidad auditada** entre extracción ontológica, CBR heredado y reranking.

### Contribuciones reformuladas
Reducir de seis a cuatro contribuciones fuertes:

1. A reproducible OntoCast--OPMAD-to-CBR pipeline that converts scientific papers into executable myCBR queries.
2. A field-level audit of RDF--CBR mapping, defaults, SHACL conformance, provenance, and normalization loss.
3. A paired downstream evaluation of CBR and CBR+MMR over 1,821 queries, with cluster bootstrap, parameter sensitivity, and strong reranking comparators.
4. A reproducibility package and expert-validation protocol delimiting what remains unvalidated: factual fidelity and human decision utility.

---

## 3) Secciones que faltan

En `main copy.tex` faltan obligatoriamente:

1. **Resultados**
   - Interoperabilidad: parseabilidad, consultas ejecutables, RDF-star cleanup.
   - Cobertura de campos: incluir `field_coverage_19cols.csv`.
   - Normalización: tarea 100%, activo ~85%, input type ~76%; otros 0%.
   - SHACL: 126/1821 conformes.
   - CBR/MMR: tabla principal con similitud, firmas, ILD.
   - Sensibilidad: λ, pool 10–30, comparadores max-sum/MAP-DPP/deduplicación.
   - Ejemplo trazable de una consulta.

2. **Discusión**
   - Responder P1–P4 explícitamente.
   - Separar lo demostrado de lo no demostrado.

3. **Limitaciones / amenazas a la validez**
   - Sin gold standard experto.
   - Sesgo de disponibilidad de PDF.
   - Campos predeterminados.
   - Pseudorreplicación de rankings.
   - Dependencia de LLM/modelos/chunks.
   - Base histórica de solo 263 casos.

4. **Conclusión**
   - Reafirmar interoperabilidad ejecutable y diversidad algorítmica.
   - No afirmar utilidad semántica/humana.

5. **Disponibilidad de datos/código, financiación, conflictos, uso de IA**
   - Ya hay buen material en suplemento; integrarlo.

Nota: mucho de esto ya parece existir en `paper/paper_ideas_es.tex`; conviene migrarlo a la plantilla final elegida.

---

## 4) Recomendaciones IEEE/Elsevier y acrónimos

### Si es IEEE
- Usar `main_copy_en.tex` como base, no `article`.
- Mantener solo abstract e IEEEkeywords en inglés.
- No usar `caption`, `subcaption` ni `[H]`; preferir `figure`, `figure*`, `table`, `table*`.
- Revisar que todas las figuras estén en inglés y en PDF vectorial.
- Añadir autores/anónimo según política.
- Revisar si IEEE requiere DOI en referencias; `IEEEtran.bst` no los está mostrando casi nunca.

### Si es Elsevier
- Migrar a `elsarticle`.
- Usar `frontmatter`, `abstract`, `keyword`.
- Añadir Highlights si la revista lo pide.
- Incluir CRediT author statement, Declaration of competing interest, Data availability.

### Acrónimos
Definir una vez y usar siempre igual:

- case-based reasoning (CBR)
- large language models (LLMs)
- Resource Description Framework (RDF)
- Shapes Constraint Language (SHACL)
- maximal marginal relevance (MMR)
- intra-list dissimilarity (ILD)
- RDF-star o RDF*, elegir uno
- OPMAD siempre en mayúsculas; myCBR con esa capitalización.

---

## 5) Checklist antes de enviar

- [ ] Elegir una sola plantilla: IEEEtran o Elsevier.
- [ ] Usar manuscrito completo con Resultados/Discusión/Limitaciones/Conclusión.
- [ ] Completar keywords.
- [ ] Reducir y enfocar abstract.
- [ ] Integrar resultados del suplemento en tablas/figuras.
- [ ] Regenerar figuras en inglés.
- [ ] Resolver contradicción del protocolo humano: texto congelado vs PDF completo.
- [ ] Rebajar claims: interoperabilidad sí; fidelidad factual no.
- [ ] Revisar SHACL y cobertura como resultados, no solo suplemento.
- [ ] Verificar referencias, DOI, años y disponibilidad.
- [ ] Revisar anonimización, metadatos PDF y rutas locales.
- [ ] Ejecutar compilación limpia y reproducción desde checkout limpio.
- [ ] Validar `SHA256SUMS.txt`.
- [ ] Adaptar declaración de IA a la revista.
- [ ] No enviar a Q1/Q2 sin validación experta o sin claims mucho más modestos.
