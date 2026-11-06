# OPMAD source DOIs

## Result

The populated ontology contains 263 cases and 105 article records. After merging one duplicated paper, they represent 104 distinct sources:

- 102 sources have verified DOIs, covering 261 cases.
- Two sources have no DOI identified, covering cases 12 and 182.
- Of the 102 DOIs, 97 were verified from existing identifiers, three were recovered from non-DOI identifiers, and two were corrected.

DOI comparison is case-insensitive. Empty DOI cells mean not identified.

## Files

- [opmad_dois.txt](opmad_dois.txt): 102 unique DOIs, one per line, ordered by first case.
- [opmad_sources.csv](opmad_sources.csv): 104 distinct sources, titles, original identifiers, ontology article IDs, all case IDs, status, and evidence URLs.
- [opmad_case_sources.csv](opmad_case_sources.csv): all 263 cases mapped to their source and DOI, with original titles, identifiers, and years retained.

The source CSV stores multiple original titles and identifiers as JSON arrays. Case IDs and article IDs are separated by semicolons.

## Extraction CSV versions

These are versions of the same case base, not separate extraction runs. Paths below are relative to `CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/`.

| File | Cases | Columns | Difference |
|---|---:|---:|---|
| `Validation/data/CleanedDATA V22-04-2021.csv` | 263 | 19 | April version, used by the validation code. |
| `CBRproject/data/CleanedDATA V12-05-2021.csv` | 263 | 19 | April version with five edited cells. This is the configured ontology input. |
| `CBRproject/data/CleanedDATA V21-07-2021.csv` | 200 | 19 | Exactly cases 1–200 of May, with no cell changes. Cases 201–263 are absent. |
| `CBRproject/data/DataBasefromOntology.csv` | 263 | 12 | Exported back from the populated ontology. Not lossless. |

## Repository evidence and method

Upstream commit: `a17841db47190465536dfef30fdb1527135a8f74`.

1. The configured input is [`CleanedDATA V12-05-2021.csv`](https://github.com/jjmj128/CBR-Ontology-For-Predictive-Maintenance/blob/a17841db47190465536dfef30fdb1527135a8f74/CBR-Ontology/CBRproject/data/CleanedDATA%20V12-05-2021.csv), with 263 rows and columns `Study title` and `Publication identifier`. [`AppConfiguration.java`](https://github.com/jjmj128/CBR-Ontology-For-Predictive-Maintenance/blob/a17841db47190465536dfef30fdb1527135a8f74/CBR-Ontology/CBRproject/src/User/AppConfiguration.java#L26) explicitly selects this file.
2. [`OPMADdatabase.owl`](https://github.com/jjmj128/CBR-Ontology-For-Predictive-Maintenance/blob/a17841db47190465536dfef30fdb1527135a8f74/CBR-Ontology/CBRproject/data/OPMADdatabase.owl) contains 263 `Predictive_maintenance_case` individuals and 105 `Predictive_Maintenance_Article` individuals. Article links `has_title` and `has_identifier` point to individuals with `has_text_value` literals. Each article's suffix is the first case number for its exact title. The importer documents this in [`CSVtoOntologyExec.java`](https://github.com/jjmj128/CBR-Ontology-For-Predictive-Maintenance/blob/a17841db47190465536dfef30fdb1527135a8f74/CBR-Ontology/CBRproject/src/User/CSVtoOntologyExec.java).
3. The CSV case-to-article mapping was checked against the ontology through `Case -> designates -> Predictive_maintenance_system_module -> RO_0010002 → model`, matching the model links on each article. All 263 mappings agree. The exported `DataBasefromOntology.csv` also has the same source titles and identifiers, apart from spaces converted to underscores during ontology serialization.
4. Each retained DOI was looked up in Crossref and its registered title compared with the source title. Missing, truncated, and mismatched identifiers were researched separately. Every DOI row links to its exact Crossref record.
5. Article162 and Article257 identify the same paper, DOI `10.1109/tmech.2017.2666199`. Their seven cases are grouped under one source.

The repository also has `CleanedDATA V21-07-2021.csv`, a 200-case subset. This report covers the full populated ontology, not only that subset. Filter `opmad_case_sources.csv` to `case_id <= 200` for that version's source mapping. `case_count_200_case_version` gives its counts by source.

This is a bibliographic identification of the sources encoded in the repository, not an audit of the extraction claims against each paper's full text. Some original publication years differ from registered metadata. Both values are retained. Years alone were not used to reject title matches.

## Identifier corrections and recoveries

| Cases | Problem in repository | Verified DOI |
|---|---|---|
| 70 | Conference ISBN/copyright string instead of DOI | [10.1109/coase.2017.8256274](https://doi.org/10.1109/coase.2017.8256274) |
| 97–98 | Wrong DOI: `10.1016/j.microrel.2013.03.010` belongs to the battery paper in cases 99–103, not the steam-turbine paper | [10.1109/access.2019.2927488](https://doi.org/10.1109/access.2019.2927488) |
| 107 | Truncated DOI `10.1186/s10033-018-0205-` | [10.1186/s10033-018-0205-x](https://doi.org/10.1186/s10033-018-0205-x) |
| 153–154 | Conference ISBN/copyright string instead of DOI | [10.1109/phm.2012.6228848](https://doi.org/10.1109/phm.2012.6228848) |
| 155 | `Unknown Identifier` | [10.1016/j.ress.2009.08.001](https://doi.org/10.1016/j.ress.2009.08.001) |

Other identifiers only needed formatting cleanup: URL/`DOI:` prefixes, whitespace, serialization underscores around prefixes, or a leading `?`. The source files remain unchanged.

## Sources without an identified DOI

- Case 12 / Article12: Juan José Montero-Jiménez and Rob A. Vingerhoeds, *Enhancing operational fault diagnosis by assessing multiple operational modes*, MOSIM 2018. The repository paraphrases the title and records [`hal-02200480`](https://hal.science/hal-02200480). The [HAL metadata API](https://api.archives-ouvertes.fr/search/?q=halId_s:hal-02200480&fl=title_s,doiId_s,uri_s,conferenceTitle_s,authFullName_s,producedDate_s,docType_s&wt=json) supplies the exact title and no DOI field. Crossref and title searches did not identify a matching DOI.
- Case 182 / Article182: A. M. Riad, H. K. Elminir, and H. M. Elattar, *Evaluation of Neural Networks in the Subject of Prognostics As Compared To Linear Regression Model*, IJET-IJENS 10(6), 52–58 (2010). `103706-5252 IJET-IJENS` is an article code, not a DOI. [Citation 72 in this review](https://pmc.ncbi.nlm.nih.gov/articles/PMC8625866/) identifies the paper without a DOI. A later [paper by Elattar](https://doi.org/10.1007/s40747-018-0082-z) cites the [original PDF URL](http://www.ijens.org/103706-5252%20IJET-IJENS.pdf), which was unavailable during this lookup. Crossref and title searches did not identify a DOI.
