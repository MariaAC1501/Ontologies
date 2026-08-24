# OPMAD extraction schema mapping

This document maps the 19-column CBR CSV schema in `CleanedDATA V21-07-2021.csv` to the ontology vocabulary in `OPMAD.owl` and to the object/data properties used by `CSVtoOntologyExec.java`.

## Sources read

- `external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/OPMAD.owl`
- `external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/src/User/CSVtoOntologyExec.java`
- `external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/src/User/AppConfiguration.java`
- `external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/CleanedDATA V21-07-2021.csv`

## Scope of this mapping

This is the target mapping for the 19-column CBR schema. It is not a claim that every OntoCast fact is materialized through the same OPMAD property path by the current bridge, nor that CSV-specific normalizations are equivalent to concepts asserted by OPMAD.

The fixed profile is generated from the authoritative file rather than maintained by hand:

```bash
python3 pipeline/generate_opmad_profile.py
python3 pipeline/generate_opmad_profile.py --check
```

The generator starts from all ontology IRIs in `extraction_schema.py`, copies their complete authoritative descriptions and connected blank-node axioms, and follows OPMAD dependencies. It deliberately omits `owl:imports` so fixed extraction does not fetch a dependency chain. Minimal external BFO/RO/CCO declaration triples needed to interpret copied axioms or schema relations are added with an explicit `rdfs:comment` identifying them as support declarations; they are not OPMAD definitions. The generated file uses canonical, sorted N-Triples (a valid Turtle subset), records the source identity, path, and SHA-256 in its header, and must not be edited manually. Verification requires CBR ontology submodule commit `a17841db47190465536dfef30fdb1527135a8f74`; the exact authoritative `OPMAD.owl` artifact is pinned in the generator as SHA-256 `60cb97d62f1e4bc66d2bdc2eaf45d30422414b51a08c47ee24168aa31acb62ac`. A source update therefore requires an explicit review and update of both pins. The generator reads the source once, then hashes and parses that immutable byte snapshot. A different `--source` is rejected unless `--allow-custom-source` is supplied, in which case the generated header explicitly identifies the result as non-authoritative and records the digest of the exact parsed bytes.

`pipeline/facts_to_csv.py` is a conservative **legacy interoperability bridge** for OntoCast output. It accepts one or more fact TTL paths or globs, strips OntoCast RDF-star reification statements that stock `rdflib` cannot parse, combines the remaining graphs, and writes a UTF-8 semicolon-delimited CSV. OPMAD-sensitive classes and task targets are recognized only in the authoritative `OPMAD#` namespace or the documented historical `OPMAD/seed#` compatibility namespace; matching a local name in any other namespace does not grant OPMAD meaning. External processing such as `schema:Action` remains namespace-specific and supported. The bridge obtains labels from `schema:name`, `rdfs:label`, and the supplied ontology; unavailable values are represented by schema-valid defaults such as `Not reported`, `Unknown synchronization`, or `0`. It derives preprocessing from design details and model approach from the number of extracted models. This behavior is retained for CBR compatibility, not publication analysis.

For publication/review analysis, use the separate nullable JSON/JSONL exporter in [`STRICT_REVIEW_EXPORT.md`](STRICT_REVIEW_EXPORT.md). It constructs records before concatenating outputs, never unions input graphs, preserves document identity and raw evidence, and reports missing, unclear, inapplicable, and failed fields explicitly without CBR defaults.

Consequently, inspect the generated CSV before using it as a production case base. Conversion does not rebuild the CBR ontology or myCBR project; copy the CSV into the CBR data directory and run the `rebuild` command when the new cases must be searchable.

## Namespaces

- `OPMAD:` `http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD#`
- `CCO:` `http://www.ontologyrepository.com/CommonCoreOntologies/`
- `OBO:` `http://purl.obolibrary.org/obo/`

## Mapping summary

| Col | CSV field | Extraction field | OPMAD target | Property path | Status |
|---|---|---|---|---|---|
| 0 | Reference | `reference` | `OPMAD:Predictive_maintenance_case` | `OPMAD:has_text_value`; `CCO:designates` to module | Implemented in `CSVtoOntologyExec` |
| 1 | Publication Year | `publication_year` | `OPMAD:Publication_year` | `OPMAD:has_publication_year`; `OPMAD:has_interger_value` | Implemented |
| 2 | Task | `task` | subclass of `OPMAD:Predictive_maintenance_module_function` | `OPMAD:has_predictive_maintenance_function` | Implemented |
| 3 | Case study | `case_study` | subclass of `OPMAD:Maintainable_item` | `OBO:BFO_0000051` from module | Implemented |
| 4 | Case study type | `case_study_type` | `OPMAD:item_type` | `CCO:describes` maintainable item | Implemented |
| 5 | Input for the model | `input_for_model` | subclass of `OPMAD:maintainable_item_record` | `OBO:BFO_0000051` from module | Implemented |
| 6 | Number of input variables | `number_of_input_variables` | `OPMAD:number_if_input_variables` | `OPMAD:has_interger_value` | Present in ontology, not materialized by Java loader |
| 7 | Input type | `input_types` | `OPMAD:Data_variable` | `OBO:RO_0010002` from record | Implemented |
| 8 | Data Pre-processing | `data_preprocessing` | `OPMAD:Design_detail` | `OPMAD:has_design_detail` | Proposed extraction mapping |
| 9 | Model Approach | `model_approach` | `OPMAD:Model_configuration` | `OPMAD:describes_configuration`; `OPMAD:has_text_value` | Proposed extraction mapping |
| 10 | Model Type | `model_types` | `OPMAD:Model_type` | `CCO:describes` model | Implemented |
| 11 | Models | `models` | subclass of `OPMAD:Predictive_maintenance_model` | `OBO:RO_0010002` from module/article | Implemented |
| 12 | Online/Off-line | `module_synchronization` | `OPMAD:Module_synchronization` | `OPMAD:has_synchronization` | Implemented |
| 13 | Number of failure modes | `number_of_failure_modes` | `OPMAD:Number_of_failure_modes` | `OPMAD:has_interger_value` | Present in ontology, not materialized by Java loader |
| 14 | Performance indicator | `performance_indicator` | `OPMAD:Performance_indicator` | `CCO:describes` module | Proposed extraction mapping |
| 15 | Performance | `performance` | `OPMAD:Performance_value` | `CCO:is_about` performance indicator | Proposed extraction mapping |
| 16 | Complementary notes | `complementary_notes` | `OPMAD:Design_detail` | `OPMAD:has_design_detail` | Proposed extraction mapping |
| 17 | Study title | `study_title` | `OPMAD:Article_title` | `OPMAD:has_title`; `OPMAD:has_text_value` | Implemented |
| 18 | Publication identifier | `publication_identifier` | `OPMAD:Article_identifier` | `OPMAD:has_identifier`; `OPMAD:has_text_value` | Implemented |

## What `CSVtoOntologyExec` actually does

The Java loader explicitly materializes these column families:

- case identifiers (`Reference`)
- article titles and identifiers
- publication years
- task subclasses
- case study subclasses
- input-record subclasses
- item types
- data variables
- model types
- predictive-maintenance-model subclasses
- module synchronization

It also creates and links:

- `OPMAD:Predictive_maintenance_case`
- `OPMAD:Predictive_Maintenance_Article`
- `OPMAD:Predictive_maintenance_system_module`
- `OPMAD:Predictive_Maintenance_case_base`

Key properties used in the loader:

- `OPMAD:has_title`
- `OPMAD:has_identifier`
- `OPMAD:has_publication_year`
- `OPMAD:has_predictive_maintenance_function`
- `OPMAD:has_synchronization`
- `OPMAD:has_text_value`
- `CCO:designates`
- `CCO:describes`
- `OBO:RO_0010002`
- `OBO:BFO_0000051`

## Task value normalization

Observed task values in the CSV map cleanly to these OPMAD classes:

- `Fault detection` → `OPMAD:Fault_detection`
- `Fault feature extraction` → `OPMAD:Fault_feature_extraction`
- `Fault identification` → `OPMAD:Fault_identification`
- `Health assessment` → `OPMAD:Health_assessment`
- `Health modelling` → `OPMAD:Health_modelling`
- `Multiple steps future state forecast` → `OPMAD:Multiple_steps_future_state_forecast`
- `One step future state forecast` → `OPMAD:One_step_future_state_forecast`
- `Remaining useful life estimation` → `OPMAD:Remaining_useful_life_estimation`

## Authoritative mapping boundary and loader limitations

`CSVtoOntologyExec.java` does **not** currently materialize columns 6, 8, 9, 13, 14, 15, or 16. The profile does not add axioms to fill those gaps.

All named OPMAD terms below exist in `OPMAD.owl`, but the CSV interpretation has these precise limits:

- `OPMAD:number_if_input_variables`, `OPMAD:Number_of_failure_modes`, and `OPMAD:has_interger_value` are authoritative terms. OPMAD does not assert the schema's class-to-value pairing or an attachment property from those count qualities to a case/module; those pairings remain extraction targets only.
- OPMAD asserts that a predictive-maintenance module may have `OPMAD:Design_detail`. It does not define preprocessing booleans or distinguish preprocessing from complementary notes. Encoding either CSV field as a design detail is an extraction-time normalization, not an OPMAD equivalence.
- OPMAD asserts `OPMAD:Model_configuration` restrictions using `OPMAD:describes_configuration` and `OPMAD:has_text_value`. The CSV values `Single model` and `Multi model` are not controlled OPMAD individuals or classes.
- OPMAD's restrictions support `OPMAD:Performance_indicator` describing a module and `OPMAD:Performance_value` being about an indicator. The Java loader still does not materialize those columns.

Thus the schema provides a complete 19-field extraction interface while explicitly separating authoritative vocabulary from CSV normalization. Any future semantic equivalence or attachment path requires an upstream OPMAD source change; this repository profile must not assert one.

## Sample validation target

The first CSV row parses into the extraction model with:

- `reference = 1`
- `task = "Health modelling"`
- `study_title = "Aircraft engine degradation prognostics based on logistic regression and novel OS-ELM algorithm"`

That is the row used for the required validation command.
