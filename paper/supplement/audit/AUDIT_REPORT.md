# Auditoría adicional de interoperabilidad y robustez

Esta auditoría es computacional. Cuantifica cobertura, defaults y sensibilidad, pero no reemplaza una anotación experta de fidelidad factual.

## Puente RDF--CBR

- Se procesaron **1.821** artefactos; todos pudieron parsearse después de la limpieza RDF-star.
- Se retiraron **311.559** bloques de reificación RDF-star; la procedencia a nivel de triple no se conserva en el grafo limpio.
- **409** artefactos contenían más de un caso y se ignoraron **567** casos adicionales.
- Sincronización informativa: **0/1821**; desempeño: **0/1821**; modos de falla no cero: **0/1821**.

## Consulta normalizada

- Tarea activa: **1821/1821**; activo: **1549/1821**; variables de entrada: **1381/1821**.
- Tipo de activo, sincronización e input modality activos: **0**, **0** y **0**, respectivamente.

## Robustez estadística

- Al remuestrear patrones de ranking baseline (848 clústeres), el IC95% del cambio medio de ILD fue [0.0873; 0.1226].
- Excluyendo el top-1 fijado por diseño, la similitud media de las posiciones 2--5 cambió -0.0033.
- Al restringir a los 1796 enlaces exactos/casi exactos, el cambio medio de ILD fue 0.1052.

## Interpretación

La evidencia sostiene interoperabilidad ejecutable y auditable. La cobertura semántica de varios campos es limitada; por ello, no se afirma interoperabilidad semántica plena, fidelidad factual ni utilidad humana.
