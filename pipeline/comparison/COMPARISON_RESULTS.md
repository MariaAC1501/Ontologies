# Comparison: Fixed OPMAD vs Evolved Ontology Extraction

## Summary Metrics

| Metric | Fixed OPMAD | Evolved Ontology |
|--------|------------|------------------|
| Total triples | 80 | 113 |
| Domain classes used | 16 | 15 |
| Instances extracted | 25 | 15 |
| Unique properties | 16 | 29 |
| Named entities | 25 | 15 |

## Domain Classes

### Fixed OPMAD classes

- `Action`
- `CollegeOrUniversity`
- `Person`
- `Technology`
- `Thing`
- `Algorithm`
- `InformationBearingArtifact`
- `Clustering`
- `Data_mining_technique_function`
- `Data_variable`
- `Design_detail`
- `Maintainable_item`
- `Predictive_Maintenance_Article`
- `Predictive_maintenance_model`
- `Predictive_maintenance_system_module`
- `text`

### Evolved ontology classes

- `CreativeWork`
- `Machine`
- `QualityManagement`
- `ARIMAForecasting`
- `HistoricData`
- `IndustrialIoTSystem`
- `PredictiveModeling`
- `MachineWithArms`
- `ProgrammableLogicController`
- `RS485Port`
- `WindingMachine`
- `Device`
- `Hardware`
- `Person`
- `text`

## Entity Overlap Analysis

- Entities found by **both**: 5
- Entities **only in fixed OPMAD**: 20
- Entities **only in evolved ontology**: 10

### Entities found by both

- **98a5233a5eff**: fixed=`text` / evolved=`text`
- **FactsAdityaSane**: fixed=`Person` / evolved=`Person`
- **FactsAmeethKanawaday**: fixed=`Person` / evolved=`Person`
- **FactsSlittingMachine**: fixed=`Maintainable_item` / evolved=`Machine, MachineWithArms, WindingMachine`
- **d4405e390c93**: fixed=`text` / evolved=`text`

### Entities only in fixed OPMAD extraction

- `FactsAdaptor` (Thing)
- `FactsArimaForecasting` (Algorithm)
- `FactsArimaModel` (Predictive_maintenance_model)
- `FactsCloud` (Thing)
- `FactsClustering` (Clustering)
- `FactsCollegeOfEngineeringPune` (CollegeOrUniversity)
- `FactsCsvFormat` (InformationBearingArtifact)
- `FactsDaisyChaining` (Design_detail)
- `FactsDataAnalysis` (Data_mining_technique_function)
- `FactsDataCollection` (Action)
- `FactsIoT` (Technology)
- `FactsIpc` (Thing)
- `FactsMachineLearningForPredictiveMaintenance` (Predictive_Maintenance_Article)
- `FactsMqttProtocol` (Action)
- `FactsPlc` (Predictive_maintenance_system_module)
- `FactsPressure` (Data_variable)
- `FactsRs485Port` (Thing)
- `FactsTension` (Data_variable)
- `FactsTimeStamp` (Data_variable)
- `FactsWidth` (Data_variable)

### Entities only in evolved ontology extraction

- `ARIMAForecasting` (ARIMAForecasting)
- `FactsIIoTSystem` (IndustrialIoTSystem)
- `FactsMachineLearning` (CreativeWork, PredictiveModeling)
- `FactsPredictiveMaintenance` (PredictiveModeling)
- `FactsQualityManagement` (QualityManagement)
- `Factsdata` (HistoricData)
- `Factsipc` (Device)
- `Factsoperator` (Person)
- `Factsplc` (Device, ProgrammableLogicController)
- `Factsrs485_port` (Hardware, RS485Port)

## Seed Ontology Coverage

- OPMAD seed classes: 56
- Covered by evolved ontology: 0
- Missed by evolved ontology: 56
- Novel classes in evolved: 15

### OPMAD classes not discovered by evolution

- `Algorithm`
- `Article_identifier`
- `Article_title`
- `Artifact`
- `ArtifactIdentifier`
- `Association_discovery`
- `BFO_0000001`
- `BFO_0000002`
- `BFO_0000004`
- `BFO_0000017`
- `BFO_0000019`
- `BFO_0000020`
- `BFO_0000030`
- `BFO_0000031`
- `BFO_0000034`
- `Classification`
- `Clustering`
- `Data_mining_technique_function`
- `Data_variable`
- `Database`
- `DescriptiveInformationContentEntity`
- `Design_detail`
- `DesignativeInformationContentEntity`
- `DesignativeName`
- `Deviation_detection`
- `DirectiveInformationContentEntity`
- `Fault_detection`
- `Fault_feature_extraction`
- `Fault_identification`
- `Future_state_forecast`
- `Health_assessment`
- `Health_modelling`
- `InformationBearingArtifact`
- `InformationContentEntity`
- `InformationProcessingArtifact`
- `Maintainable_item`
- `Model_configuration`
- `Model_type`
- `Module_synchronization`
- `Multiple_steps_future_state_forecast`
- `Number_of_failure_modes`
- `One_step_future_state_forecast`
- `Performance_indicator`
- `Performance_value`
- `Predictive_Maintenance_Article`
- `Predictive_maintenance_case`
- `Predictive_maintenance_model`
- `Predictive_maintenance_module_function`
- `Predictive_maintenance_system_module`
- `Publication_year`
- `Regression`
- `Remaining_useful_life_estimation`
- `Sequential_pattern_discovery`
- `item_type`
- `maintainable_item_record`
- `number_if_input_variables`

### Novel classes discovered by evolution (not in OPMAD)

- `ARIMAForecasting`
- `CreativeWork`
- `Device`
- `Hardware`
- `HistoricData`
- `IndustrialIoTSystem`
- `Machine`
- `MachineWithArms`
- `Person`
- `PredictiveModeling`
- `ProgrammableLogicController`
- `QualityManagement`
- `RS485Port`
- `WindingMachine`
- `text`

## Interpretation

This comparison was generated automatically from the extraction outputs.
See `pipeline/comparison/compare.py` for methodology.

