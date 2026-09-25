Inspeccioné `paper/main copy.tex`, `paper/main copy.pdf`, `paper/main.pdf`, `paper/README.md`, `paper/figures/` y `paper/references.bib`. No edité archivos.

## 1) Dictamen de redacción/formato

**Dictamen:** manuscrito técnicamente sólido y bastante cercano a envío, pero todavía requiere una pasada de formato editorial antes de considerarlo “camera-ready”. La estructura IMRyD + amenazas + disponibilidad + declaraciones es clara; el tono es prudente y evita sobreafirmar fidelidad factual o utilidad humana. La copia `main copy.tex` está sincronizada con `main.tex`.

Puntos fuertes:
- Narrativa metodológica clara: extracción → puente RDF/CBR → consulta → reranking.
- Limitaciones bien integradas, no escondidas.
- Figuras y tablas existen, cargan y son legibles.
- Bibliografía completa: 26 entradas usadas, sin citas faltantes.

Puntos que impiden readiness plena:
- Convención numérica inconsistente y, en algunos casos, incorrecta por interacción con `babel` español.
- Abstract muy denso aunque no excesivamente largo.
- Anglicismos técnicos sin política consistente.
- Algunos acrónimos aparecen sin definición suficiente.
- Encabezado del apéndice queda huérfano al final de la página 15.

## 2) Problemas restantes de idioma, estilo y estructura

- **Anglicismos abundantes:** `pipeline`, `downstream`, `reranking`, `baseline`, `pool`, `sidecar`, `ranking`, `parseable`. Conviene decidir una política: traducirlos o ponerlos en cursiva la primera vez.
- **“Fidelidad factual”** suena calcado del inglés. Mejor: “fidelidad fáctica”, “exactitud factual” o “exactitud semántica respecto del texto”.
- **Acrónimos por definir o reforzar:** SHACL, ILD, MAP-DPP, DSS e IRI. ILD se usa como métrica pero no queda claramente introducido como acrónimo textual.
- **Marca `myCBR`:** con `\textsc{myCBR}` se ve como `MYCBR`, perdiendo la grafía oficial.
- **Abstract bilingüe ocupa mucho frente inicial:** español + inglés hacen que la introducción empiece en página 2. Si la revista no exige dos resúmenes, conviene dejar solo uno.
- **Repetición de cautelas:** la advertencia “no demuestra fidelidad/ utilidad humana” es metodológicamente correcta, pero aparece muchas veces. Se puede mantener en abstract, alcance, amenazas y conclusión; reducir en zonas intermedias.

## 3) Problemas LaTeX o de compilación

- Compilación existente correcta: `main copy.pdf` tiene 18 páginas.
- No detecté errores, citas indefinidas ni referencias indefinidas.
- BibTeX sin warnings.
- Solo aparecen **2 Underfull hbox** en la tabla 1, no críticos.

Problema importante de formato:
- En captions como `($n=1.821$)`, `babel` español convierte el punto decimal en coma dentro de modo matemático. En el PDF se ve **`n = 1,821`**, que puede leerse como decimal, no como 1.821 documentos. Afecta al menos tablas 2, 3, 8 y texto con `$n=1.796$`.

Usar, por ejemplo:
```latex
$n = 1\,821$
```
o directamente:
```latex
(n = 1821)
```

Otros puntos:
- Figuras usan punto decimal (`0.5650`, `94.8%`) mientras el texto/tablas usan coma decimal. Hay inconsistencia visual.
- Varias figuras/tablas usan `[H]`; funciona, pero rigidiza el flujo.
- El apéndice queda con el título “A. Campos de interoperabilidad” al final de página 15 y la tabla inicia en página 16.

## 4) Cambios concretos sugeridos

**Título actual:**  
“De artículos científicos a recomendaciones CBR diversas: un pipeline auditado OntoCast--OPMAD para mantenimiento predictivo”

**Alternativa más fluida:**  
“De artículos científicos a recomendaciones diversas basadas en CBR: un flujo OntoCast--OPMAD auditado para mantenimiento predictivo”

**Abstract:** reducir densidad. Versión sugerida:

> Este trabajo presenta y audita una cadena para transformar literatura reciente de mantenimiento predictivo en consultas ejecutables para un sistema CBR heredado y en recomendaciones con diversidad controlada. A partir de 3.990 registros Scopus de 2025--2026, 2.768 cumplieron los criterios de inclusión; se recuperaron 1.822 PDF y se analizaron 1.821 documentos únicos. OntoCast, condicionado por OPMAD, produjo hechos RDF/Turtle que se limpiaron, mapearon a un esquema CBR de 19 campos y se ejecutaron contra una base myCBR de 263 casos. La cadena fue operativa para todos los documentos, pero la auditoría mostró pérdida semántica: varios campos quedaron como predeterminados o fueron descartados en la normalización, y solo 126/1.821 artefactos cumplieron las formas SHACL mínimas. En la tarea downstream, con pool 15, top-5 y λ = 0,70, MMR aumentó la disimilitud intra-lista de 0,4216 a 0,5265 y redujo las listas con firmas repetidas de 610 a 5, con una caída de similitud media de 0,5563 a 0,5536. Los comparadores y análisis de sensibilidad indican un compromiso configurable, no superioridad universal. Los resultados avalan interoperabilidad ejecutable y comportamiento de ranking, no fidelidad fáctica ni utilidad humana.

**Tablas:**
- Cambiar `Activo en query` → `Activo en consulta`.
- Cambiar `IC95\%` → `IC del 95\,\%`.
- Corregir todos los `n=1.821` en modo matemático.
- Tabla 8: si es apéndice, considerar numeración `Tabla A.1`.

**Figuras:**
- Regenerar gráficos con coma decimal si el manuscrito se envía en español.
- Revisar figura 4: las anotaciones de IC son legibles, pero pequeñas.
- Figura 6 podría ganar claridad si se separa en dos figuras o se aumenta tamaño vertical.

## 5) Checklist final

- [ ] Corregir separadores de miles en modo matemático: `1\,821`, `1\,796`, etc.
- [ ] Unificar coma/punto decimal entre texto, tablas y figuras.
- [ ] Definir SHACL, ILD, MAP-DPP, DSS e IRI en primera aparición.
- [ ] Decidir política de anglicismos técnicos.
- [ ] Ajustar macro de `myCBR` para conservar la grafía oficial.
- [ ] Evitar el encabezado huérfano del apéndice.
- [ ] Recompilar y verificar log sin underfull/overfull relevantes.
- [ ] Adaptar plantilla, autores, financiación y metadatos según la revista objetivo.
