Guardé/leí las búsquedas en `C:/repos/Ontologies/.searches/paper` y revisé los artículos guía locales y el repositorio. No edité manuscrito ni fuentes.

## 1) Síntesis crítica y hueco

La literatura ya cubre bien los componentes aislados: CBR y ciclo 4R; ontologías como vocabulario/case-base/similitud semántica; CBR habilitado por ontologías para selección de procesos o diseño; CBR para diseño de mantenimiento predictivo con OPMAD/OMSSA; diversidad en recuperación CBR; y MMR como reranking relevancia–novedad. También hay literatura reciente sobre LLMs para construcción de grafos de conocimiento y mapeos RDF.

El hueco defendible **no** es “usar ontologías con CBR en PdM” ni “mejorar diversidad en CBR”: eso ya existe. El hueco más sólido es la **integración reproducible end-to-end**: extraer RDF desde artículos PdM con un LLM condicionado por OPMAD/OntoCast, convertir esos RDF a los 19 campos legados del CBR, consultar el CBR habilitado por ontologías y aplicar MMR como post-proceso para diversidad, preservando trazabilidad y evaluando el trade-off diversidad/similitud. En el repositorio, este punto se apoya además en el resultado local de diversidad: top-1 preservado, diversidad intra-lista +0.1256 con caída media de similitud top-5 de −0.0021.

## 2) Referencias verificadas y afirmación citable

| # | Referencia | DOI/URL | Afirmación citable |
|---|---|---|---|
| 1 | Aamodt & Plaza (1994) | 10.3233/AIC-1994-7104 | Formaliza CBR como paradigma con variaciones metodológicas y ciclo de razonamiento basado en casos. |
| 2 | López de Mántaras et al. (2005) | 10.1017/S0269888906000646 | Resume las fases retrieval, reuse, revision y retention, justificando focalizar mejoras en recuperación. |
| 3 | Gruber (1993) | 10.1006/knac.1993.1008 | Define ontologías como especificaciones formales portables de conceptualizaciones. |
| 4 | Noy & McGuinness (2001) | https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html | Guía práctica para clases, propiedades, restricciones e instancias; útil para justificar metodología OPMAD. |
| 5 | Amailef & Lu (2013) | 10.1016/j.dss.2012.12.034 | Demuestra CBR soportado por ontología para servicios de respuesta, usando ontología en extracción y recuperación. |
| 6 | Sánchez et al. (2012) | 10.1016/j.eswa.2012.01.082 | Propone similitud semántica basada en características ontológicas, base para similitudes no puramente léxicas. |
| 7 | Qin et al. (2018) | 10.1016/j.knosys.2017.11.013 | Usa ontologías para apoyar CBR en especificación de tolerancias, confirmando el patrón ontology-supported CBR. |
| 8 | Romero Bejarano et al. (2014) | 10.1017/S0890060413000498 | Relaciona CBR, ontologías y modelado de preferencias en diseño de sistemas. |
| 9 | Mabkhot et al. (2019) | 10.1155/2019/2505183 | Presenta DSS ontology-enabled CBR para selección de procesos de manufactura. |
| 10 | Montero Jimenez et al. (2020) | 10.1016/j.jmsy.2020.07.008 | Revisión sistemática PdM; identifica modelos mono/multimodelo para diagnóstico/prognóstico. |
| 11 | Montero-Jimenez et al. (2021) | 10.1109/ISSE51541.2021.9582535 | Antecedente directo: CBR habilitado por ontología para arquitectura de mantenimiento predictivo y problema de diversidad. |
| 12 | Muñoz-Hernández et al. (2021) | https://orion.tec.ac.cr/en/publications/integrating-ontologies-and-case-based-reasoning-for-the-developme | Integra ontologías y myCBR; usa SPARQL/razonamiento para representación, almacenamiento y similitud. |
| 13 | Muñoz-Peña et al. (2025) | 10.1109/ISSE65546.2025.11370002 | Trabajo más cercano en diversidad CBR-PdM: CNN modificado aumenta diversidad y cobertura. |
| 14 | Smyth & McClave (2001) | 10.1007/3-540-44593-5_25 | Discute explícitamente trade-off similitud vs diversidad en CBR. |
| 15 | McSherry (2002) | 10.1007/3-540-46119-1_17 | Propone recuperación consciente de diversidad en CBR. |
| 16 | Carbonell & Goldstein (1998) | 10.1145/290941.291025 | Introduce MMR para combinar relevancia con novedad/diversidad en reranking. |
| 17 | Kaminskas & Bridge (2016) | 10.1145/2926720 | Sistematiza objetivos beyond-accuracy: diversidad, novedad, serendipia y cobertura. |
| 18 | Pan et al. (2024) | 10.1109/TKDE.2024.3352100 | Mapea la convergencia LLM–KG, incluyendo LLM-augmented KGs para construcción/completado. |
| 19 | Lairgi et al. (2024) | 10.1007/978-981-96-0573-6_16 | iText2KG muestra construcción incremental de KGs mediante LLMs. |
| 20 | Mustafa et al. (2025) | https://arxiv.org/abs/2506.03301 | Ejemplo de prompts guiados por ontología/documentación para construir KGs desde instrucciones. |
| 21 | Marketakis et al. (2026) | 10.1145/3748522.3779763 | Usa LLMs para automatizar mapeos de esquemas en construcción de RDF KGs. |
| 22 | Belikov / OntoCast (2025) | 10.5281/zenodo.17796467 | Software citado para extracción de triples semánticos/RDF guiada por ontología desde documentos. |

## 3) BibTeX

```bibtex
@article{Aamodt1994CBR,
  author={Aamodt, Agnar and Plaza, Enric},
  title={Case-Based Reasoning: Foundational Issues, Methodological Variations, and System Approaches},
  journal={AI Communications},
  volume={7},
  number={1},
  pages={39--59},
  year={1994},
  doi={10.3233/AIC-1994-7104},
  url={https://doi.org/10.3233/AIC-1994-7104}
}

@article{LopezDeMantaras2005CBR4R,
  author={L{\'o}pez de M{\'a}ntaras, Ramon and McSherry, David and Bridge, Derek and Leake, David and Smyth, Barry and Craw, Susan and Faltings, Boi and Maher, Mary Lou and Cox, Michael T. and Forbus, Kenneth and Keane, Mark and Aamodt, Agnar and Watson, Ian},
  title={Retrieval, reuse, revision and retention in case-based reasoning},
  journal={The Knowledge Engineering Review},
  volume={20},
  number={3},
  pages={215--240},
  year={2005},
  doi={10.1017/S0269888906000646},
  url={https://doi.org/10.1017/S0269888906000646}
}

@article{Gruber1993Ontology,
  author={Gruber, Thomas R.},
  title={A translation approach to portable ontology specifications},
  journal={Knowledge Acquisition},
  volume={5},
  number={2},
  pages={199--220},
  year={1993},
  doi={10.1006/knac.1993.1008},
  url={https://doi.org/10.1006/knac.1993.1008}
}

@misc{NoyMcGuinness2001Ontology101,
  author={Noy, Natalya F. and McGuinness, Deborah L.},
  title={Ontology Development 101: A Guide to Creating Your First Ontology},
  year={2001},
  publisher={Stanford University},
  url={https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html}
}

@article{AmailefLu2013OntologyCBR,
  author={Amailef, Khaled and Lu, Jie},
  title={Ontology-supported case-based reasoning approach for intelligent m-Government emergency response services},
  journal={Decision Support Systems},
  volume={55},
  number={1},
  pages={79--97},
  year={2013},
  doi={10.1016/j.dss.2012.12.034},
  url={https://doi.org/10.1016/j.dss.2012.12.034}
}

@article{Sanchez2012SemanticSimilarity,
  author={S{\'a}nchez, David and Batet, Montserrat and Isern, David and Valls, Aida},
  title={Ontology-based semantic similarity: A new feature-based approach},
  journal={Expert Systems with Applications},
  volume={39},
  number={9},
  pages={7718--7728},
  year={2012},
  doi={10.1016/j.eswa.2012.01.082},
  url={https://doi.org/10.1016/j.eswa.2012.01.082}
}

@article{Qin2018OntologyCBR,
  author={Qin, Yuchu and Lu, Wenlong and Qi, Qunfen and Liu, Xiaojun and Huang, Meifa and Scott, Paul J. and Jiang, Xiangqian},
  title={Towards an ontology-supported case-based reasoning approach for computer-aided tolerance specification},
  journal={Knowledge-Based Systems},
  volume={141},
  pages={129--147},
  year={2018},
  doi={10.1016/j.knosys.2017.11.013},
  url={https://doi.org/10.1016/j.knosys.2017.11.013}
}

@article{RomeroBejarano2014CBRDesign,
  author={Romero Bejarano, Juan Camilo and Coudert, Thierry and Vareilles, Elise and Geneste, Laurent and Aldanondo, Michel and Abeille, Jo{\"e}l},
  title={Case-based reasoning and system design: An integrated approach based on ontology and preference modeling},
  journal={Artificial Intelligence for Engineering Design, Analysis and Manufacturing},
  volume={28},
  number={1},
  pages={49--69},
  year={2014},
  doi={10.1017/S0890060413000498},
  url={https://doi.org/10.1017/S0890060413000498}
}

@article{Mabkhot2019OntologyCBRManufacturing,
  author={Mabkhot, Mohammed M. and Al-Samhan, Ali M. and Hidri, Lotfi},
  title={An Ontology-Enabled Case-Based Reasoning Decision Support System for Manufacturing Process Selection},
  journal={Advances in Materials Science and Engineering},
  volume={2019},
  pages={1--18},
  year={2019},
  doi={10.1155/2019/2505183},
  url={https://doi.org/10.1155/2019/2505183}
}

@article{MonteroJimenez2020PredictiveMaintenanceSurvey,
  author={Montero Jimenez, Juan Jos{\'e} and Schwartz, S{\'e}bastien and Vingerhoeds, Rob and Grabot, Bernard and Sala{\"u}n, Michel},
  title={Towards multi-model approaches to predictive maintenance: A systematic literature survey on diagnostics and prognostics},
  journal={Journal of Manufacturing Systems},
  volume={56},
  pages={539--557},
  year={2020},
  doi={10.1016/j.jmsy.2020.07.008},
  url={https://doi.org/10.1016/j.jmsy.2020.07.008}
}

@inproceedings{MonteroJimenez2021OntologyCBRPdM,
  author={Montero-Jimenez, Juan Jose and Vingerhoeds, Rob and Grabot, Bernard},
  title={Enhancing predictive maintenance architecture process by using ontology-enabled Case-Based Reasoning},
  booktitle={2021 IEEE International Symposium on Systems Engineering (ISSE)},
  pages={1--8},
  year={2021},
  publisher={IEEE},
  doi={10.1109/ISSE51541.2021.9582535},
  url={https://doi.org/10.1109/ISSE51541.2021.9582535}
}

@inproceedings{MunozHernandez2021OntologiesCBR,
  author={Mu{\~n}oz-Hern{\'a}ndez, Hugo and Vingerhoeds, Rob and Montero-Jim{\'e}nez, Juan Jos{\'e}},
  title={Integrating ontologies and case-based reasoning for the development of knowledge-intensive intelligent systems},
  booktitle={35th Annual European Simulation and Modelling Conference 2021, ESM 2021},
  editor={Armenia, Stefano and Geril, Philippe},
  pages={29--36},
  publisher={EUROSIS},
  year={2021},
  url={https://orion.tec.ac.cr/en/publications/integrating-ontologies-and-case-based-reasoning-for-the-developme}
}

@inproceedings{MunozPena2025DiversityCBR,
  author={Mu{\~n}oz-Pe{\~n}a, Emmanuel and Ding, Wendi and Montero-Jim{\'e}nez, Juan Jos{\'e} and Vingerheods, Rob},
  title={Enhancing Case Retrieval in Case-Based Reasoning Through Improved Solution Space Diversity and Coverage},
  booktitle={2025 IEEE International Symposium on Systems Engineering (ISSE)},
  pages={1--8},
  year={2025},
  publisher={IEEE},
  doi={10.1109/ISSE65546.2025.11370002},
  url={https://doi.org/10.1109/ISSE65546.2025.11370002}
}

@incollection{SmythMcClave2001SimilarityDiversity,
  author={Smyth, Barry and McClave, Paul},
  title={Similarity vs. Diversity},
  booktitle={Case-Based Reasoning Research and Development},
  pages={347--361},
  publisher={Springer},
  year={2001},
  doi={10.1007/3-540-44593-5_25},
  url={https://doi.org/10.1007/3-540-44593-5_25}
}

@incollection{McSherry2002DiversityConscious,
  author={McSherry, David},
  title={Diversity-Conscious Retrieval},
  booktitle={Advances in Case-Based Reasoning},
  pages={219--233},
  publisher={Springer},
  year={2002},
  doi={10.1007/3-540-46119-1_17},
  url={https://doi.org/10.1007/3-540-46119-1_17}
}

@inproceedings{CarbonellGoldstein1998MMR,
  author={Carbonell, Jaime and Goldstein, Jade},
  title={The use of MMR, diversity-based reranking for reordering documents and producing summaries},
  booktitle={Proceedings of the 21st Annual International ACM SIGIR Conference on Research and Development in Information Retrieval},
  pages={335--336},
  publisher={ACM},
  year={1998},
  doi={10.1145/290941.291025},
  url={https://doi.org/10.1145/290941.291025}
}

@article{KaminskasBridge2016BeyondAccuracy,
  author={Kaminskas, Marius and Bridge, Derek},
  title={Diversity, Serendipity, Novelty, and Coverage: A Survey and Empirical Analysis of Beyond-Accuracy Objectives in Recommender Systems},
  journal={ACM Transactions on Interactive Intelligent Systems},
  volume={7},
  number={1},
  pages={1--42},
  year={2016},
  doi={10.1145/2926720},
  url={https://doi.org/10.1145/2926720}
}

@article{Pan2024LLMKG,
  author={Pan, Shirui and Luo, Linhao and Wang, Yufei and Chen, Chen and Wang, Jiapu and Wu, Xindong},
  title={Unifying Large Language Models and Knowledge Graphs: A Roadmap},
  journal={IEEE Transactions on Knowledge and Data Engineering},
  volume={36},
  number={7},
  pages={3580--3599},
  year={2024},
  doi={10.1109/TKDE.2024.3352100},
  url={https://doi.org/10.1109/TKDE.2024.3352100}
}

@incollection{Lairgi2024IText2KG,
  author={Lairgi, Yassir and Moncla, Ludovic and Cazabet, R{\'e}my and Benabdeslem, Khalid and Cl{\'e}au, Pierre},
  title={iText2KG: Incremental Knowledge Graphs Construction Using Large Language Models},
  booktitle={Web Information Systems Engineering -- WISE 2024},
  pages={214--229},
  publisher={Springer Nature Singapore},
  year={2024},
  doi={10.1007/978-981-96-0573-6_16},
  url={https://doi.org/10.1007/978-981-96-0573-6_16}
}

@misc{Mustafa2025ODRLOntologyGuided,
  author={Mustafa, Daham M. and Nadgeri, Abhishek and Collarana, Diego and Arnold, Benedikt T. and Quix, Christoph and Lange, Christoph and Decker, Stefan},
  title={From Instructions to ODRL Usage Policies: An Ontology Guided Approach},
  year={2025},
  eprint={2506.03301},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://arxiv.org/abs/2506.03301}
}

@inproceedings{Marketakis2026RDFSchemaMappings,
  author={Marketakis, Yannis and Lintanff-Castel, Milio and Tzitzikas, Yannis},
  title={Using LLMs to Automate Schema Mappings for RDF Knowledge Graphs Construction},
  booktitle={Proceedings of the 41st ACM/SIGAPP Symposium on Applied Computing},
  pages={1999--2000},
  publisher={ACM},
  year={2026},
  doi={10.1145/3748522.3779763},
  url={https://doi.org/10.1145/3748522.3779763}
}

@misc{Belikov2025OntoCast,
  author={Belikov, Alexander},
  title={OntoCast},
  publisher={Zenodo},
  year={2025},
  doi={10.5281/zenodo.17796467},
  url={https://doi.org/10.5281/zenodo.17796467}
}
```

## 4) Advertencias

- **Solapamiento de novedad:** Montero-Jimenez et al. (2021) ya cubre CBR ontológico para diseño PdM; Muñoz-Hernández et al. (2021) ya cubre integración ontología–myCBR; Muñoz-Peña et al. (2025) ya ataca diversidad en el mismo dominio. La novedad debe formularse como **pipeline reproducible RDF→CBR→MMR**, no como “primer CBR ontológico” ni “primera diversidad CBR”.
- **Referencias sin DOI:** Muñoz-Hernández et al. (2021) debe citarse por URL institucional/Scopus; Noy & McGuinness por URL Stanford.
- **Preprints/software:** Mustafa et al. (2025) es arXiv; OntoCast es software con DOI, no artículo revisado por pares.
- **Búsquedas amplias LLM–KG:** hubo totales muy altos; para afirmaciones concretas conviene citar los registros exactos verificados, no inferir estado del arte desde búsquedas generales.
