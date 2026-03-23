# OPMAD extraction schema mapping

This document maps the 19-column CBR CSV schema in `CleanedDATA V21-07-2021.csv` to the ontology vocabulary in `OPMAD.owl` and to the object/data properties used by `CSVtoOntologyExec.java`.

## Sources read

- `external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/OPMAD.owl`
- `external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/src/User/CSVtoOntologyExec.java`
- `external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/src/User/AppConfiguration.java`
- `external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/CleanedDATA V21-07-2021.csv`

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

## Notes on fields not implemented in the Java loader

`CSVtoOntologyExec.java` does **not** currently materialize columns 6, 8, 9, 13, 14, 15, or 16.

For the extraction target in `pipeline/extraction_schema.py`, those fields are still anchored to real ontology terms in `OPMAD.owl`:

- numeric count fields use `OPMAD:number_if_input_variables` / `OPMAD:Number_of_failure_modes` with `OPMAD:has_interger_value`
- preprocessing and complementary notes use `OPMAD:Design_detail` with `OPMAD:has_design_detail`
- model approach uses `OPMAD:Model_configuration` with `OPMAD:describes_configuration`
- performance fields use `OPMAD:Performance_indicator` and `OPMAD:Performance_value`

This gives OntoCast a complete 19-field extraction target without changing files outside `pipeline/`.

## Sample validation target

The first CSV row parses into the extraction model with:

- `reference = 1`
- `task = "Health modelling"`
- `study_title = "Aircraft engine degradation prognostics based on logistic regression and novel OS-ELM algorithm"`

That is the row used for the required validation command.
