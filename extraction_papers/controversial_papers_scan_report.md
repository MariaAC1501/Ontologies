# Controversial Included Papers Scan

Date: 2026-06-11  
Corpus scanned: `extraction_papers/scopus_export_May 26-2026_included.csv` before applying the controversial exclusions  
Method: 8 Pi subagents scanned corpus-id ranges and reported currently included records that may still be controversial or out of scope.

## Output files

| File | Description |
|---|---|
| `extraction_papers/controversial_papers_candidates.csv` | All 265 controversial candidates originally found by subagents |
| `extraction_papers/controversial_papers_review_exclude.csv` | 112 candidates the subagents recommended reviewing for exclusion |
| `extraction_papers/controversial_review_exclude_applied.csv` | 112 recommendations applied as exclusions |
| `extraction_papers/controversial_papers_review_exclude_remaining.csv` | Review-exclude candidates still included; now empty |
| `extraction_papers/controversial_papers_candidates_remaining_included.csv` | Remaining controversial/borderline candidates still included, all `review_keep` |
| `extraction_papers/removed_controversial_review_exclude_pdfs_manifest.csv` | PDFs removed after applying controversial exclusions |
| `extraction_papers/controversial_scan_range_*.csv` | Raw range-level subagent outputs |

## Summary

| Group | Count |
|---|---:|
| Included corpus size scanned before applying this pass | 2880 |
| Controversial candidates found | 265 |
| Applied exclusions | 112 |
| Borderline candidates retained for now | 153 |
| Review-exclude candidates still included | 0 |

## Applied exclusions by controversy level

| Level | Count |
|---|---:|
| medium | 60 |
| high | 52 |

## Applied exclusions by normalized reason

| Reason | Count |
|---|---:|
| civil_geotechnical_infrastructure | 26 |
| process_quality_not_maintenance | 22 |
| performance_or_energy_optimization | 17 |
| software_it_cyber | 15 |
| business_social | 13 |
| generic_method_no_asset_case | 9 |
| weak_maintenance_link | 5 |
| sensor_material_only | 5 |

## Remaining borderline retained candidates by level

| Level | Count |
|---|---:|
| low | 79 |
| medium | 74 |

## Remaining borderline retained candidates by reason

| Reason | Count |
|---|---:|
| performance_or_energy_optimization | 26 |
| business_social | 22 |
| process_quality_not_maintenance | 20 |
| civil_geotechnical_infrastructure | 19 |
| generic_method_no_asset_case | 18 |
| sensor_material_only | 16 |
| software_it_cyber | 16 |
| weak_maintenance_link | 13 |
| medical_bio_non_equipment | 3 |

## First applied-exclusion examples

| ID | Level | Reason | Title | Brief reason |
|---|---|---|---|---|
| `paper-0002` | high | process_quality_not_maintenance | ExpLusion: Explanation-driven Late Fusion for enhanced production process monitoring | Focuses on manufacturing quality-control ensemble fusion; asset degradation or maintenance decision is only a keyword-level linkage. |
| `paper-0022` | high | process_quality_not_maintenance | A design concept for data-driven brewing: sensor-based system architecture and ML applications for sustainability in micro-breweries | Micro-brewery sensor architecture emphasizes brewing sustainability, quality forecasting, and fermentation/process control; equipment maintenance is only a possible use case. |
| `paper-0098` | high | civil_geotechnical_infrastructure | Online Track Anomaly Detection: Comparison of Different Machine Learning Techniques Through Injection of Synthetic Defects on Experimental Datasets | Targets railway track defects/anomaly detection, a civil/rail infrastructure condition-monitoring case excluded under the strict criteria. |
| `paper-0440` | high | civil_geotechnical_infrastructure | An Implicit-Explicit Diffusion Model for Industrial Data Imputation | Industrial data imputation method is motivated by control/fault detection/PdM, but evaluates missing-value reconstruction rather than asset condition. |
| `paper-0659` | high | software_it_cyber | Predictive Maintenance and Reliability in Intelligent 5G Networks Based on Graph Neural Networks | Targets 5G radio link failures and QoS alerts rather than maintenance of a clearly defined physical asset. |
| `paper-0767` | high | civil_geotechnical_infrastructure | Artificial intelligence-driven safety assessment of scaffolding using LiDAR sensing | Scaffolding construction safety inspection/PHM is a temporary civil structure context rather than engineered-equipment PdM. |
| `paper-0835` | high | performance_or_energy_optimization | iFANnpp: Nuclear power plant digital twin for robots and autonomous intelligence | NPP digital twin is primarily for robot behavior simulation and plant performance; PdM is incidental with no degradation model. |
| `paper-1109` | high | civil_geotechnical_infrastructure | Predictive Rehabilitation of Clean Water Customer Connections Leveraging Machine Learning Algorithms and Failure Time Series Data | Clean-water service lines are water-distribution infrastructure; strict criteria exclude non-equipment civil infrastructure. |
| `paper-1157` | high | software_it_cyber | Condition Monitoring Technology and Its Testing for 5G-Enabled High-Speed Railway Wireless Communication Networks: Guaranteeing the Reliability of Train–Ground Communication | Condition monitoring of a 5G railway communication network; target is telecom service reliability, not physical-asset maintenance. |
| `paper-1195` | high | process_quality_not_maintenance | A digital pheromone-based approach for in-control/out-of-control classification | Classifies in-control/out-of-control states in potato-chip frying; this is process QC more than asset maintenance. |
| `paper-1234` | high | software_it_cyber | Integrating dynamic features into machine learning models for predicting sewer network failures: a Random Forest approach | Sewer-network pipe failures and blockages are civil water infrastructure, a strict-scope exclusion. |
| `paper-1255` | high | performance_or_energy_optimization | On the Viability of Reused Vehicle Li-Ion Batteries as PV Storage for High-Altitude Rural Areas: Case Study in Cusco-Peru | Second-life battery PV-storage viability for rural heating; no condition monitoring, RUL, or maintenance decision is central. |
| `paper-1278` | high | performance_or_energy_optimization | Quasi-Instantaneous Battery End-of-Discharge Time Prognosis with Non-Stationary Autoregressive Exogenous Inputs | End-of-discharge time prognosis is operational battery depletion/SOC forecasting, not degradation, SOH, or RUL maintenance. |
| `paper-1287` | high | business_social | SMART PRINTING LABS: AI-ENABLED MANAGEMENT SYSTEMS | Smart printing lab framework emphasizes workflow, defects, energy and management; the maintenance link is generic. |
| `paper-1297` | high | process_quality_not_maintenance | Reducing waste and increasing yield in roll-to-roll printing: a case study with global scalability | Roll-to-roll printing waste/yield DMAIC case; condition-based maintenance is only one intervention, not primary PdM. |
| `paper-1332` | high | process_quality_not_maintenance | Improved nicrnisi thin-film thermocouple manufacturing process enables accurate temperature measurement of UAV engines | Thermocouple fabrication/calibration for UAV temperature measurement; no fault diagnosis, prognosis, or maintenance decision. |
| `paper-1421` | high | business_social | A Maintenance 4.0 Framework for Proactive Indoor Air Quality Management in Laboratory Environments | Predicts indoor air quality in labs; maintenance is IAQ/ventilation management, not clearly asset condition. |
| `paper-1457` | high | civil_geotechnical_infrastructure | DefectTwin: When LLM Meets Digital Twin for Railway Defect Inspection | Railway defect inspection with LLM/DT likely concerns rail infrastructure/visual defects rather than vehicles or equipment. |
| `paper-1474` | high | weak_maintenance_link | NeuroFusionNet Adaptive Deep Learning for Intelligent Real-Time Industrial IoT Decisions | Industrial IoT decisions/anomaly detection on environmental telemetry; asset or failure target is unclear. |
| `paper-1549` | high | software_it_cyber | Performance analysis of REST API in a real-time IoT-based vehicle monitoring system | Primary contribution is REST API performance/security for a vehicle monitoring system; PdM is framed as a future use. |
| `paper-1620` | high | generic_method_no_asset_case | Advancing Robotic Systems with Distributed Multi-Agent Digital Twins: A Scalable and Adaptive Framework | Robotics digital-twin framework optimizes navigation/collaboration; predictive maintenance is only a generic claimed capability. |
| `paper-1849` | high | weak_maintenance_link | Acoustic fingerprint in vehicle manufacturing as a basis for future applications | Acoustic fingerprint/database paper presents failure prediction and predictive service as future applications rather than demonstrated PdM. |
| `paper-1899` | high | business_social | Multidimensional Maintenance Maturity Modeling: Fuzzy Predictive Model and Case Study on Ensuring Operational Continuity Under Uncertainty | Maintenance maturity and organizational continuity model lacks asset condition monitoring, diagnosis, or prognostics. |
| `paper-1986` | high | process_quality_not_maintenance | Addressing Aircraft Maintenance Delays Using a DMAIC-FMEA Framework: Insights from a Commercial Aviation Case Study | Aircraft maintenance-delay DMAIC/FMEA case is mainly process, inventory, and quality improvement rather than predictive asset maintenance. |
| `paper-2074` | high | generic_method_no_asset_case | Harnessing Machine Learning for Data Transformation in Industry 5.0 Production Lines | Holistic Industry 5.0 data/interface article; predictive maintenance is asserted without a concrete asset fault, degradation, or maintenance case. |
| `paper-2229` | high | civil_geotechnical_infrastructure | Mechanical response and failure pressure prediction of cracked PVC-UH buried thin-walled pipes | Buried municipal water-supply pipe failure-pressure/material-response study; strict scope treats this as civil infrastructure rather than equipment PdM. |
| `paper-2231` | high | civil_geotechnical_infrastructure | Early Leak and Burst Detection in Water Pipeline Networks Using Machine Learning Approaches | Water distribution leak/burst detection targets utility infrastructure and conservation, not electromechanical equipment maintenance. |
| `paper-2275` | high | weak_maintenance_link | Development and Design Of a 4000 Amp DC Rectifier for Industrial Metal Scrapping | High-current rectifier design for metal recycling; predictive maintenance appears as a built-in feature, not the research focus. |
| `paper-2290` | high | civil_geotechnical_infrastructure | Risk-Based Water Pipe Failure Prediction through Machine Learning and Hydraulic Models | Water transmission-line failure-risk and rehabilitation planning is civil water infrastructure despite maintenance-planning language. |
| `paper-2387` | high | software_it_cyber | Extended theoretical model for water pipeline passive assessment using ambient noise correlation | Theoretical passive-assessment model for water pipeline networks; no electromechanical asset or maintenance decision is demonstrated. |
| `paper-2419` | high | sensor_material_only | Piezoelectric sensor characterization for structural strain measurements | Piezoelectric strain-sensor characterization lacks a specific asset, fault, degradation mechanism, or maintenance decision. |
| `paper-2437` | high | software_it_cyber | Making waves: Generative artificial intelligence in water distribution networks: Opportunities and challenges | GenAI opportunities paper for water distribution networks is broad utility management; PdM is only one possible application. |
| `paper-2538` | high | business_social | Ilorin metropolitan water supply infrastructure (WSI) asset management under limited data | Urban water-supply infrastructure asset management for buried pipes; civil utility infrastructure rather than industrial/electromechanical equipment. |
| `paper-2639` | high | software_it_cyber | Exploring information needed in maintenance backlog-related decision-making in the Finnish road network | Road-network maintenance backlog decision study; civil road infrastructure and budgeting rather than predictive maintenance of equipment. |
| `paper-2734` | high | software_it_cyber | Explainable deep learning models for predicting water pipe failures | Water-distribution-network leak/burst prediction for urban utility pipes; civil infrastructure rather than in-scope industrial pipeline/equipment. |
| `paper-2755` | high | civil_geotechnical_infrastructure | PREDICTING WATER DISTRIBUTION PIPE FAILURES USING MACHINE LEARNING AND CROSS-INFRASTRUCTURE DATA; [NAPOVED OKVAR VODOVODNIH CEVI S STROJNIM UČENJEM IN PODATKI O SOSEDNJI INFRASTRUKTURI] | Urban water distribution pipe failure prediction using cross-infrastructure data; civil utility infrastructure outside strict equipment PdM. |
| `paper-2769` | high | civil_geotechnical_infrastructure | Lifecycle Vulnerability in Urban Water Infrastructure for Predictive Maintenance Planning | Lifecycle vulnerability and predictive maintenance planning for urban water utilities; buried civil assets and planning, not equipment PdM. |
| `paper-2830` | high | software_it_cyber | Data-driven approaches for pipe life prognosis in water distribution networks: the Barcelona water distribution network case study | Water-distribution pipe life prognosis and renewal planning; civil utility network rather than industrial/electromechanical asset maintenance. |
| `paper-2869` | high | software_it_cyber | Research on memory failure prediction based on ensemble learning | Data-center server memory failure prediction; close to IT hardware/service reliability rather than engineered-asset predictive maintenance. |
| `paper-2917` | high | software_it_cyber | Solid-State Drive Failure Prediction Using Anomaly Detection | SSD failure prediction for real-time cloud services/data availability; IT storage reliability boundary case outside strict equipment PdM. |

## Notes

- The 112 `review_exclude` candidates have now been marked excluded and their PDFs removed when present.
- The remaining 153 candidates are lower-priority `review_keep` cases: controversial enough to note, but the subagents recommended retaining them.
- Current corpus counts are summarized in `predictive_maintenance_screening_results.md`.
