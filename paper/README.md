# Manuscrito LaTeX

Manuscrito anónimo en español preparado para revisión por pares. `paper/main.tex` es la fuente canónica actual y `paper/main copy.tex` se mantiene sincronizado por compatibilidad con borradores previos.

- Fuente canónica: `paper/main.tex`
- Copia sincronizada: `paper/main copy.tex`
- Borrador IEEE en inglés: `paper/main_copy_en.tex` (no canónico)
- Bibliografía: `paper/references.bib`
- PDF canónico: `paper/main.pdf`
- PDF de copia: `paper/main copy.pdf`
- Figuras: `paper/figures/*.pdf`
- Suplemento: `paper/supplement/`
- Análisis: `paper/analysis/`

## Entorno

Windows, Python 3.12, Java/myCBR y MiKTeX. Instalar dependencias:

```powershell
uv pip install --python .\.venv\Scripts\python.exe -r requirements.txt
```

## Experimento principal

El proyecto `PredictMaint_myCBR.prj` contiene 263 casos y corresponde a `CleanedDATA V12-05-2021.csv`; no usar V21 para enriquecer soluciones.

```powershell
.\.venv\Scripts\python.exe scripts\compare_diversity_all_papers.py `
  --facts-glob "extraction_papers/ontocast_runs/run_*/output/facts_*.ttl" `
  --casebase-csv "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/CleanedDATA V12-05-2021.csv" `
  --top-k 5 --pool-size 15 --lambda-relevance 0.70 `
  --query-year 2026 --drop-default-synchronization `
  --output-dir ".build/diversity_comparison_1821_v12_no_default_sync"
```

El año queda fijado porque la recencia histórica depende del año de consulta.

## Pool-30 para sensibilidad extendida

```powershell
.\.venv\Scripts\python.exe scripts\compare_diversity_all_papers.py `
  --facts-glob "extraction_papers/ontocast_runs/run_*/output/facts_*.ttl" `
  --casebase-csv "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/CleanedDATA V12-05-2021.csv" `
  --top-k 5 --pool-size 30 --lambda-relevance 0.70 `
  --query-year 2026 --drop-default-synchronization --skip-build `
  --output-dir ".build/diversity_comparison_1821_v12_pool30_revision"
```

## Regenerar auditorías y figuras

```powershell
.\.venv\Scripts\python.exe paper\analysis\statistical_analysis.py
.\.venv\Scripts\python.exe paper\analysis\revision_audit.py
.\.venv\Scripts\python.exe paper\analysis\extended_reranking_analysis.py
.\.venv\Scripts\python.exe paper\analysis\cbr_ablation_analysis.py
.\.venv\Scripts\python.exe paper\analysis\corpus_bias_analysis.py
.\.venv\Scripts\python.exe paper\analysis\shacl_validation.py
.\.venv\Scripts\python.exe paper\analysis\preserve_rdfstar_provenance.py
.\.venv\Scripts\python.exe paper\figures\generate_figures.py
.\.venv\Scripts\python.exe paper\analysis\build_reproducibility_manifest.py
```

## Compilar

```powershell
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

## Verificación

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s pipeline\tests -p "test_*.py"
```

La versión final debe compilar sin referencias indefinidas ni cajas desbordadas.

## Antes de enviar

1. Elegir revista y adaptar plantilla/idioma.
2. Sustituir autores, afiliaciones, financiación y correspondencia.
3. Archivar repositorio y añadir DOI.
4. Confirmar política de IA generativa y anonimización de metadatos/autocitas.
5. Reproducir desde un checkout limpio y validar `paper/supplement/SHA256SUMS.txt`.
6. Si se desea afirmar fidelidad factual o utilidad humana, ejecutar una validación experta independiente; la versión actual no la incluye.

Los PDF del corpus no se redistribuyen por licencia.
