No edité archivos.

## 1) Dictamen editorial actual

**Minor revision** — casi listo para envío **si se mantiene el framing actual**: interoperabilidad ejecutable/auditable y comportamiento algorítmico de reranking.  
No considero la falta de validación humana/factual como bloqueo, según la instrucción. El manuscrito **no reclama fidelidad factual ni utilidad humana**; al contrario, lo niega explícitamente en abstract, métodos, discusión, amenazas y conclusión.

## 2) Mejoras logradas respecto al borrador anterior

- `paper/main copy.tex` ya está completo: incluye Resultados, Discusión, Amenazas, Conclusiones, Disponibilidad, Declaraciones y apéndice.
- `paper/main.tex` y `paper/main copy.tex` están sincronizados byte a byte.
- `DIVERSITY_COMPARISON_RESULTS.md` ya está actualizado al corpus de **1.821 documentos únicos**, no al resultado parcial anterior.
- Se integraron resultados antes relegados al suplemento: cobertura de 19 campos, SHACL, defaults, normalización, MMR, sensibilidad y comparadores.
- El lenguaje mejoró mucho: ya no se vende como validación de extracción ni como utilidad decisional.
- Se incorporaron controles fuertes: bootstrap por clúster, pseudorreplicación, `Unknown synchronization`, ablaciones por atributos/año, sensibilidad a λ/pool/pesos/k, max-sum, MAP-DPP y deduplicación.
- La compilación existente no muestra citas ni referencias indefinidas; solo aparecen underfull boxes menores.

## 3) Problemas restantes que bloquean o debilitan el envío

- **Inconsistencia V12/V21 en suplemento:** `paper/supplement/protocol/schema_mapping.md` dice que mapea `CleanedDATA V21-07-2021.csv`, mientras el experimento principal usa V12/263 casos. Hay que aclararlo.
- **Manifiesto reproducible desactualizado:** `paper/supplement/repro/software_manifest.json` contiene hash/tamaño antiguos de `paper/main.tex`; debe regenerarse tras la versión final.
- **Disponibilidad final incompleta:** falta DOI/repositorio definitivo; el texto dice que se añadirá al depositar.
- **Metadatos de envío:** autores, afiliaciones, financiación, correspondencia y política de IA siguen en modo revisión/anónimo.
- **“Pipeline reproducible” debe matizarse:** reproducible desde artefactos canónicos, no necesariamente desde PDFs/LLMs originales bit a bit.
- **Default de tarea:** 94 consultas recibieron tarea predeterminada y esta sí queda activa; conviene reportar/mitigar como sensibilidad.
- **Etiquetas `Facts*` en input type:** algunas sobreviven a la normalización; debilitan la afirmación de variables limpias/semánticas.
- **SHACL bajo:** 126/1.821 conformes. Está bien tratado como limitación, pero debe seguir siendo visible, no maquillado.

## 4) Claims que conviene suavizar o corregir

- “hechos RDF/Turtle” → mejor “afirmaciones RDF/Turtle extraídas” o “artefactos RDF”.
- “pipeline reproducible” → “pipeline reproducible desde artefactos canónicos”.
- “trazable” → “con sidecar de procedencia preservado”, no trazabilidad operacional completa campo→triple→chunk.
- “los autores verificaron referencias, código, cifras y afirmaciones” → suena demasiado amplio; mejor limitar a consistencia interna/código/cifras reportadas.
- “interoperabilidad” sola → usar siempre “interoperabilidad ejecutable/técnica”, no “semántica plena”.

## 5) Cambios concretos antes de enviar, priorizados

1. Corregir la inconsistencia V12/V21 en `schema_mapping.md` y documentos relacionados.
2. Regenerar `software_manifest.json` y confirmar hashes finales.
3. Sustituir DOI/repositorio pendiente por datos reales o frase aceptable para revisión anónima.
4. Matizar “reproducible”, “hechos” y “trazabilidad” en abstract/contribuciones/disponibilidad.
5. Añadir una nota breve sobre las 94 consultas con tarea predeterminada y las etiquetas `Facts*` que sobreviven en `input_type`.
6. Decidir revista/plantilla/idioma; para Q1/Q2 internacional, preparar versión completa en inglés.
7. Completar autores, financiación, correspondencia, declaración de IA y anonimización/metadatos según política de la revista.
8. Ejecutar compilación limpia y verificación de hashes desde un checkout limpio antes del depósito final.
