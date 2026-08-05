# Actualización bibliográfica posterior a revisión

Fecha: 29 de julio de 2026.

Se consultó Scopus mediante API y se conservaron los JSON completos bajo `.searches/paper-revision/`.

| Tema | Consulta refinada | Total |
|---|---|---:|
| LLM + ontología + KG | `TITLE(("large language model" AND ontolog*) OR ("ontology-guided" AND "knowledge graph")) AND TITLE-ABS-KEY(extract* OR construct*)` | 78 |
| diversificación | `TITLE-ABS-KEY((diversif* OR "beyond accuracy") AND (recommender OR "information retrieval") AND (MMR OR xQuAD OR "determinantal point process"))` | 43 |
| mantenimiento + KG/DSS | `TITLE-ABS-KEY("predictive maintenance") AND TITLE-ABS-KEY(("knowledge graph" OR ontolog*) AND ("decision support" OR recommend*))` | 33 |

La búsqueda Semantic Scholar devolvió HTTP 403; no se utilizó como fuente de resultados. Se incorporaron trabajos verificables sobre xQuAD, DPP sobre grafos y recomendación de mantenimiento con KG/GNN. Los metadatos DOI se contrastaron con Crossref. Los intentos de recuperación abierta de los PDF seleccionados no produjeron archivos redistribuibles; no se eludieron paywalls.
