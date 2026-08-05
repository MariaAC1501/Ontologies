He ejecutado el análisis y guardé el script y salidas en:

`C:/repos/Ontologies/.build/diversity_comparison_1821_v12_no_default_sync/statistical_analysis_outputs/`

Script principal: `statistical_analysis_no_default_sync.py`  
Ablación solicitada: `default_sync_ablation.csv`  
No edité manuscrito ni fuentes.

## Texto publicable sugerido

En el experimento principal sin default de sincronización (`V12`, 263 casos, 1.821 consultas, query-year 2026), `Unknown synchronization` fue descartado como evidencia por defecto. Este experimento debe considerarse el análisis principal, porque evita que un valor desconocido actúe como señal semántica positiva.

Con MMR λ=0,70 y top-1 fijo, la similitud del primer resultado se preservó exactamente (0,5630 vs. 0,5630; 1.821/1.821 top-1 preservados). La similitud media del top-5 disminuyó levemente de 0,5563 a 0,5536 (Δ=-0,0027; IC95% [-0,0029, -0,0025]; Wilcoxon p=1,19e-197; r_rb=-1,000), reflejando el coste esperado en relevancia algorítmica.

A cambio, la diversidad aumentó de forma marcada. Los modelos únicos por top-5 subieron de 4,6332 a 4,9973 (Δ=+0,3641; IC95% [0,3394, 0,3888]; Wilcoxon p=3,99e-123; prueba de signos p=1,51e-182), y la ILD algorítmica aumentó de 0,4216 a 0,5265 (Δ=+0,1049; IC95% [0,1013, 0,1087]; Wilcoxon p=5,93e-286; r_rb=0,978). El orden cambió en 1.821/1.821 consultas y el conjunto top-5 en 1.819/1.821.

La sensibilidad con λ={0,5,0,6,0,7,0,8,0,9} confirmó el compromiso relevancia-diversidad: λ bajos maximizan diversidad e ILD; λ altos recuperan similitud media pero permiten más listas con modelos repetidos. En todos los casos se preservó el top-1 por diseño.

La ablación frente al experimento con default ponderado muestra que el default altera sustancialmente los rankings: para el ranking MMR principal, sólo 1.097/1.821 rankings ordenados fueron idénticos, 1.338/1.821 top-1 coincidieron y 1.136/1.821 conjuntos top-5 fueron iguales. Esta comparación debe reportarse como control descriptivo, no como resultado principal. El análisis sin default es metodológicamente preferible y debe ocupar el lugar central del manuscrito.
