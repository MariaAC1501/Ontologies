No edité archivos.

## 1) Qué demuestra y qué no demuestra ahora

**Demuestra razonablemente:**
- Que el pipeline es ejecutable sobre 1.821 documentos únicos: facts parseables tras limpieza RDF-star, puente a CSV/19 campos, consultas myCBR y rankings.
- Que la auditoría detecta pérdidas semánticas importantes: defaults, campos descartados, baja conformidad SHACL y atributos realmente activos reducidos.
- Que MMR cambia el comportamiento del ranking: sube ILD de 0,4216 a 0,5265, baja listas con firmas repetidas de 610 a 5 y conserva top-1, con pérdida pequeña de similitud media top-5.
- Que el resultado es un compromiso configurable relevancia-diversidad, no una superioridad universal; los comparadores deduplicación, max-sum y MAP-DPP están bien usados para matizar.

**No demuestra:**
- Fidelidad factual de las extracciones frente al PDF.
- Exhaustividad de los facts, especialmente porque casi todo se extrajo de tres fragmentos iniciales.
- Interoperabilidad semántica plena: solo 126/1.821 artefactos cumplen SHACL mínimo.
- Utilidad decisional humana ni calidad técnica real de las recomendaciones.
- Que los 1.821 documentos puedan incorporarse como casos nuevos sin revisión; el manuscrito ya lo delimita correctamente.

## 2) Reproducibilidad desde artefactos canónicos

**Veredicto:** bastante sólida para reproducir el análisis downstream desde los TTL/facts canónicos, resultados y scripts; todavía no está limpia como paquete final.

Fortalezas:
- Hay README, manifiesto de extracción con hashes, reportes de auditoría, resultados por consulta, scripts y casebase V12 documentada.
- `main.tex` y `main copy.tex` están sincronizados.
- La frontera de reproducibilidad está bien declarada: reproducir desde artefactos canónicos, no regenerar bit a bit la extracción LLM.

Problemas a corregir:
- En `paper/README.md` y en el bloque de reproducción del manuscrito se usa `ontocast_runs/run_*/output/facts_*.ttl`, pero los facts reales están bajo `extraction_papers/ontocast_runs/...`. Desde la raíz, el glob documentado encuentra 0 facts; el correcto encuentra 1.821.
- El `paper/supplement/protocol/schema_mapping.md` parece desactualizado respecto a `pipeline/SCHEMA_MAPPING.md`: sigue enfatizando V21, mientras el experimento usa V12.
- El manifiesto de software/reproducibilidad está desfasado respecto al `paper/main.tex` actual; conviene regenerarlo junto con `SHA256SUMS.txt`.

## 3) Inconsistencias o datos faltantes restantes

- Diferenciar siempre **1.822 filas/PDF** vs **1.821 documentos únicos**. En el manifiesto bruto aparecen 600/500/722 filas por modelo, mientras el texto habla de 599/500/722 artefactos únicos.
- Los 25 enlaces PDF--facts no exactos están reconocidos, pero algunos parecen emparejamientos muy débiles; conviene listar umbrales y tratamiento explícito.
- Campos con cobertura nula o casi nula siguen siendo un cuello de botella: sincronización, modos de falla, desempeño, tipo de activo e input modality no aportan a la consulta.
- La selección de un solo caso en 409 artefactos multicase, ignorando 567 casos adicionales, sigue siendo una fuente importante de posible pérdida/sesgo.
- El año/publication year y el año fijo de consulta deben quedar todavía más separados: uno es metadato extraído/default; el otro es parámetro de myCBR.

## 4) Amenazas de validez faltantes o mal ubicadas

Las amenazas principales están bien cubiertas. Añadiría o movería:

- **Deriva de artefactos canónicos**: paths, hashes y mappings desincronizados son amenaza de reproducibilidad, no solo detalle operativo.
- **Riesgo de linkage PDF--facts**: los 25 no exactos deberían figurar también como amenaza de trazabilidad/datos, no solo sensibilidad.
- **Selección de caso fuente en artefactos multicase**: debe destacarse como amenaza al constructo “documento → consulta”.
- **Disponibilidad de PDF**: ya está reportada, pero puede resaltarse que el corpus analizado no representa todos los incluidos Scopus; 946 incluidos quedaron sin PDF.
- **Circularidad parcial de ILD/MMR**: está bien mencionada; mantenerla visible porque ILD comparte similitud de solución con el objetivo de MMR.

## 5) Cambios concretos recomendados

1. Corregir todos los comandos de reproducción para usar `extraction_papers/ontocast_runs/run_*/output/facts_*.ttl` o documentar explícitamente otro cwd.
2. Sincronizar `paper/supplement/protocol/schema_mapping.md` con `pipeline/SCHEMA_MAPPING.md`, dejando claro V12 vs V21.
3. Regenerar `software_manifest.json` y `SHA256SUMS.txt` tras la versión final.
4. Añadir una mini-tabla “filas vs documentos únicos”: PDFs, SHA únicos, duplicado, modelos por lote, chunks, enlaces exactos/no exactos.
5. Enfatizar en resultados/apéndice una clasificación por campo: extraído, inferido, default, descartado, activo en query.
6. Documentar mejor la regla determinista de selección en artefactos multicase y cuántas consultas quedan afectadas.
7. Para los 25 enlaces no exactos, incluir tabla/archivo referenciado con score, categoría y efecto al excluirlos.
8. Mantener la formulación actual de alcance: interoperabilidad ejecutable y ranking algorítmico, no fidelidad factual ni utilidad humana.
