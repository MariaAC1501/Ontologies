# Revisión estadística de Resultados, métricas y evaluación

## 1. Qué se está evaluando realmente —y qué no

El estudio evalúa correctamente un **experimento computacional pareado de ranking**: para cada uno de los **1.821 documentos únicos accesibles**, se genera una consulta CBR y se compara el **top-5 CBR** contra un **top-5 reordenado con MMR** desde un pool de 15, con **top-1 fijo** y `λ=0,70`.

Lo que sí se evalúa:

- Interoperabilidad técnica: PDF → hechos RDF/Turtle → esquema de 19 campos → consulta myCBR.
- Capacidad de producir consultas ejecutables: **1.821/1.821** con al menos cinco resultados.
- Cambio algorítmico del ranking:
  - ILD media: **0,4216 → 0,5265**, Δ=**0,1049**, IC95% bootstrap **[0,1013; 0,1087]**.
  - Firmas `Models` repetidas: **610 → 5**.
  - Similitud media top-5: **0,5563 → 0,5536**, Δ=**−0,0027**.

Lo que no se evalúa:

- Fidelidad semántica de la extracción desde los PDF.
- Relevancia real de las recomendaciones para diseñadores o expertos.
- Superioridad técnica de los modelos recomendados.
- Ground truth de recuperación.
- Utilidad humana, novedad percibida, confianza o impacto en decisiones.
- Independencia estadística plena entre las 1.821 consultas.

La delimitación aparece explícitamente en el manuscrito y es una fortaleza. Aun así, los Resultados deben mantener siempre el lenguaje en términos de **diversidad algorítmica alineada con MMR**, no de “mejores recomendaciones”.

---

## 2. Crítica sección por sección de Resultados

### 4.1 Cobertura e interoperabilidad

El resultado de cobertura —**1.821 artefactos, 1.821 consultas, todas con ≥5 resultados**— es valioso como prueba de ingeniería. Pero el “100%” es un indicador débil si no se acompaña de calidad.

Problemas:

- De los **2.768 registros incluidos**, solo se analizaron **1.821 documentos únicos**; los **946 incluidos sin PDF accesible** representan un sesgo de disponibilidad importante.
- La cobertura se logra tras limpieza RDF-star y defaults; no implica que los campos estén correctamente extraídos.
- Todos los tipos de activo y modalidades de entrada se descartaron por incompatibilidad léxica; por tanto, el esquema de 19 campos no se explota realmente completo.
- En **409 artefactos** había más de un caso y se eligió el primero por IRI; esto puede afectar la consulta usada.

Recomendación: cambiar el énfasis de “cobertura 100%” a “100% de ejecutabilidad técnica entre documentos únicos accesibles y postprocesados”.

### 4.2 Efecto global del reranking

El efecto principal es fuerte dentro de la métrica usada:

- ILD: **+0,1049**, relativo **+24,89%**.
- **1.707** consultas mejoran ILD, **112** empeoran y **2** empatan.
- Firmas únicas: **4,6332 → 4,9973**.
- Listas con repetición: **610 → 5**.
- Similitud media top-5: baja **0,0027**, es decir **−0,48%**.
- Top-1 idéntico: **0,5630 → 0,5630**, pero por diseño.

La principal debilidad es que la ILD usa la misma similitud de solución `s_sol` que entra en MMR. Por tanto, la mejora de ILD no es validación independiente; es evidencia de que el algoritmo mueve la lista en la dirección de su objetivo.

Además, la pérdida de similitud media está amortiguada por el top-1 fijo. Si se excluye el primer resultado, el coste medio en las cuatro posiciones reordenables es aproximadamente **−0,0033**, no −0,0027. Conviene reportar también métricas para posiciones 2–5.

### 4.3 Comparadores simples y ablación

La tabla 2 es útil porque separa duplicación exacta de diversidad taxonómica:

- CBR: similitud **0,5563**, ILD **0,4216**, repetidas **610**.
- Deduplicación exacta: similitud **0,5557**, ILD **0,4373**, repetidas **0**.
- Aleatorio: similitud **0,5316**, ILD **0,4439**, repetidas ≈**217**.
- MMR: similitud **0,5536**, ILD **0,5265**, repetidas **5**.

Interpretación crítica:

- Si el objetivo fuera solo eliminar firmas repetidas, la deduplicación exacta gana: elimina todas las repeticiones con menor pérdida de similitud.
- La ventaja de MMR aparece solo cuando se acepta `s_sol` como medida válida de diversidad entre soluciones no idénticas.
- El baseline aleatorio es muy débil; sirve como control, pero no como comparador competitivo.

La ablación de `Unknown synchronization` es importante: mantenerlo con peso uno cambia materialmente los rankings. Solo coinciden:

- **1.338/1.821** primeros resultados, **73,48%**.
- **1.097/1.821** rankings MMR completos, **60,24%**.
- **1.136/1.821** conjuntos top-5, **62,38%**.

Esto refuerza la decisión de tratarlo como ausente, pero también muestra que los resultados son sensibles a decisiones de normalización/defaults. Habría que reportar tasas de default para todos los campos críticos, no solo sincronización.

### 4.4 Sensibilidad a λ y tareas

La sensibilidad confirma el compromiso esperado, pero también cuestiona la elección de `λ=0,70`.

Valores:

- `λ=0,5`: similitud **0,5522**, ILD **0,5295**, repetidas **0**.
- `λ=0,6`: similitud **0,5533**, ILD **0,5274**, repetidas **0**.
- `λ=0,7`: similitud **0,5536**, ILD **0,5265**, repetidas **5**.
- `λ=0,8`: similitud **0,5543**, ILD **0,5248**, repetidas **14**.
- `λ=0,9`: similitud **0,5549**, ILD **0,5201**, repetidas **25**.

`λ=0,6` parece casi tan relevante como `λ=0,7`, con mayor ILD y cero repeticiones. Si `λ=0,70` fue preespecificado, está bien, pero no debe presentarse como óptimo.

Por tareas, el patrón es heterogéneo:

- RUL: ΔILD **0,1475**, n=371.
- Detección de fallas: **0,0975**, n=782.
- Evaluación de salud: **0,1026**, n=303.
- Pronóstico a un paso: solo **0,0145**, n=136, con **71 mejoras y 65 disminuciones**, Wilcoxon **p=0,504**.
- Modelado de salud n=8 y pronóstico multihorizonte n=6 son meramente exploratorios.

La afirmación “ganancia positiva en las ocho tareas” es cierta para la media, pero debe suavizarse: en pronóstico a un paso no hay patrón pareado claro según signos/rangos.

### 4.5 Ejemplo de lista

El ejemplo es útil y está bien delimitado: muestra variedad, no superioridad.

Consulta 1815:

- Similitud media: **0,5140 → 0,5112**.
- ILD: **0,5156 → 0,6032**.
- Elimina duplicación de Gaussian Process Regression y añade Linear Regression/Rule-Based, Non-linear Least Squares y métodos recursivos.

Faltaría mostrar por qué esas alternativas son útiles para la consulta. Una matriz de distancias `s_sol` o los componentes de MMR ayudarían a interpretar la selección.

---

## 3. Riesgos estadísticos y de evaluación

- **Métrica alineada con optimización:** ILD comparte `s_sol` con MMR; no es métrica independiente.
- **Top-1 fijo:** la preservación de top-1 y su similitud son tautológicas.
- **Pseudorreplicación:** aunque hay **1.684 firmas de consulta normalizada**, solo hay **848 rankings baseline ordenados** y **699 rankings MMR ordenados**; el mayor clúster reúne **129** y **109** consultas.
- **Tamaño efectivo menor:** los IC bootstrap sobre 1.821 consultas pueden ser demasiado estrechos para inferencia poblacional.
- **p-valores poco informativos:** Wilcoxon/signos describen estabilidad del algoritmo, no evidencia sobre problemas independientes.
- **Sin ground truth:** no se sabe si los casos recomendados son correctos o útiles.
- **Sin evaluación humana:** no hay medidas de utilidad, novedad percibida, tiempo de decisión o adopción.
- **Defaults y campos descartados:** la consulta CBR depende de una representación empobrecida.
- **Case base pequeña:** 263 casos históricos generan muchos patrones repetidos.
- **Sensibilidad incompleta:** falta variar pool size, k, pesos de `s_sol`, λ extremos y condición sin top-1 fijo.

---

## 4. Fortalezas del análisis actual

- Diseño pareado correcto: misma consulta bajo CBR y CBR+MMR.
- Reporte claro de efecto, IC bootstrap y sensibilidad.
- Reconocimiento explícito de que ILD no es validación independiente.
- Ablación útil de `Unknown synchronization`.
- Comparadores simples que ayudan a interpretar MMR.
- Diagnóstico honesto de pseudorreplicación.
- Separación temporal entre artículos 2025–2026 y base histórica.
- Lenguaje bastante prudente en Discusión y Conclusiones.

---

## 5. Recomendaciones concretas

1. Añadir una tabla por tarea con baseline, MMR, ΔILD, Δsimilitud, IC, mejoras/empeoramientos y duplicados.
2. Reportar métricas separadas para posiciones 2–5, dado que el top-1 está fijo.
3. Añadir bootstrap por clúster: firma normalizada, ranking baseline y conjunto top-5.
4. Incluir histogramas/ECDF de ΔILD y Δsimilitud; no solo medias.
5. Reportar matriz de contingencia de repeticiones: 610 baseline repetidas, 605 corregidas, 5 persistentes.
6. Comparar contra baselines más fuertes: deduplicación taxonómica, max-sum diversity, DPP/xQuAD, MMR sin top-1 fijo y CNN previo en las mismas consultas.
7. Probar sensibilidad a `pool_size`, `k`, pesos de `s_sol` y λ extremos 0/1.
8. Añadir métricas de diversidad independientes de MMR.
9. Construir un corpus dorado estratificado para precisión/recall/F1 de extracción.
10. Hacer evaluación humana con arquitectos: relevancia, novedad, utilidad, tiempo y confianza.

Lenguaje a suavizar:

- “Demuestra diversidad” → “aumenta una métrica de diversidad alineada con MMR”.
- “Pequeña pérdida” → “pequeña en escala CBR; impacto práctico no evaluado”.
- “Estable por tareas” → “patrón medio positivo, con estratos pequeños y excepción clara en pronóstico a un paso”.
- “Cobertura 100%” → “ejecutabilidad técnica 100% sobre documentos únicos accesibles y postprocesados”.
