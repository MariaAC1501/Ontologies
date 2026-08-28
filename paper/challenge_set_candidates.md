# Provisional Challenge-Set Candidates

This is a metadata-level shortlist for the fixed-versus-evolved ontology benchmark. It is not a frozen corpus or publication evidence.

## Source inventory

- The shortlist was initially drawn from 1,822 open-access articles that had been downloaded for historical development runs. That inventory contained 1,277 articles from 2025 and 545 from 2026.
- The 32 selected candidates are now stored under `markdown/<normalized-doi>/`. Each directory contains the source PDF and a converted `document.md`.
- Historical screening and extraction outputs are development artifacts. Final eligibility and case annotations must be established independently.

The shortlist favors clear implemented diagnostic or prognostic models and variation in function, asset, model family, data modality, and case complexity. PDF quality was not used.

## Full-text skim

A machine-assisted skim of the 32 converted articles found no obvious full-text exclusion. Each article contains an implemented method, an engineered asset, and empirical or simulation-based evaluation relevant to diagnosis, prognosis, or health assessment. Final eligibility still requires independent human confirmation.

The Markdown conversions preserve the main prose, headings, equations, and tables well enough for annotation. They do not preserve PDF page boundaries, so the final provenance workflow must add page references from the corresponding PDFs. The conversion for `paper-0527` omits the article title as a top-level heading, but its DOI and article content identify the correct battery paper.

Particularly useful case-boundary stress tests are `paper-0221`, `paper-0340`, `paper-0527`, and `paper-0725`, which bind several functions, models, or model stages within one article. `paper-0005`, `paper-0280`, and `paper-0319` provide useful non-deep-learning contrasts.

The following articles need explicit codebook decisions rather than automatic interpretation from their titles:

| ID | Preliminary interpretation | Full-text issue to adjudicate |
|---|---|---|
| `paper-0026` | Health assessment or health modelling | The model predicts leakage-derived health labels, not elapsed time or cycles to failure, despite the RUL wording in the title. |
| `paper-0104` | Health assessment with a failure-referenced proxy | The paper explicitly describes its RUL value as a fleet-specific normalized health proxy rather than an absolute lifetime prediction. |
| `paper-0319` | Fault-feature extraction and condition assessment | The evaluated contribution restores spectral harmonics. Fault thresholds and the monitoring system are proposed without a labeled fault-classification experiment. |
| `paper-0340` | Health assessment through multi-method fusion | Four prognostic methods are fused into a current scalar health index. The primary output is not a direct RUL estimate. |
| `paper-0343` | Aging-state identification and early warning | The article contains knowledge-graph, dynamic-graph, temporal-fusion, risk, and deployment components with different reported configurations. |
| `paper-0489` | Fault identification and severity assessment | “Prediction” refers to static simulated fault classification and severity estimation, not future-state forecasting. |
| `paper-1679` | Health assessment and maintenance-effectiveness correction | Maintenance-adjusted risk curves are implemented on operational pump data, but intervention effectiveness lies partly outside the core benchmark representation. |

The skim suggests moving the maximum-complexity drivetrain platform (`paper-0725`) to held-out evaluation and using the simpler threshold-based CNC article (`paper-0005`) during development. This leaves complex multi-case examples in development while preserving a demanding unseen case-boundary test.

## Possible development anchors

These eight articles collectively expose ontology evolution to the main case concepts and several difficult relation patterns. The partition remains provisional until full-text verification.

| ID | Article | DOI | Why promising |
|---|---|---|---|
| `paper-0001` | Decision-Aware Multi-Horizon Fault Prediction for Photovoltaic Inverters | `10.3390/s26082463` | Multi-horizon forecasting, a coordinated TimeXer/XGBoost pipeline, and alarm-policy decisions. |
| `paper-0007` | Predicting the Remaining Useful Life of Ship Shafting Using Bayesian Networks with Asymmetric Probability Distributions | `10.3390/sym18030443` | A probabilistic RUL model and an uncommon marine drivetrain asset. |
| `paper-0221` | Multi-Sensor Process Monitoring and Fault Diagnosis for Multi-Mode Industrial Servomotor Systems with Fault Classification and RUL Prediction | `10.3390/pr14050772` | Multiple functions, synchronized sensor types, fault classes, and likely multiple linked cases. |
| `paper-0243` | Gearbox Bearing Crack Growth Prognostics and Uncertainty Quantification with Physics-Informed Machine Learning | `10.5194/wes-11-737-2026` | Physics-informed crack-growth prognosis, RUL, and uncertainty for a wind-turbine gearbox bearing. |
| `paper-0340` | Hybrid Fault Prognosis Using Health Index Fusion | `10.3390/a19040292` | Explicit fusion of physics-based, signal-based, data-driven, and statistical prognostic outputs. |
| `paper-0406` | Diagnosis of Abnormal Sound Defects in Automobile Engines Based on Fusion of Multi-Modal Images and Audio | `10.3390/electronics15071406` | Cross-modal diagnosis and physically informed audio/image relations. |
| `paper-0527` | Simultaneous Estimation of State of Health and Remaining Useful Life for Lithium-ion Batteries Using a Transfer-Learning-Based Fusion Model | `10.5796/electrochemistry.25-00143` | Joint SOH and RUL tasks, transfer learning, and a fused Transformer/BiLSTM model. |
| `paper-0005` | Material-Adaptive Kurtosis Thresholding for Real-Time Multi-Parameter Condition Monitoring in CNC Milling | `10.15282/ijame.23.1.2026.6.1004` | A simple, interpretable threshold model for establishing the basic item--data--function--model case pattern before more complex development examples. |

## Possible held-out articles

| ID | Article | DOI | Main challenge dimension |
|---|---|---|---|
| `paper-0725` | An AI Digital Platform for Fault Diagnosis and RUL Estimation in Drivetrain Systems Under Varying Operating Conditions | `10.3390/machines14010026` | A maximum-complexity held-out test covering fault detection, type and severity identification, RUL, statistical and deep models, and decision fusion. |
| `paper-0012` | Predictive Maintenance of Railway Suspension Systems Using Multi-Level Time–Frequency Vibration Analysis | `10.1007/s42452-026-08531-2` | Multi-level and multi-axis data with deterioration classification. |
| `paper-0021` | Tool-Health Digital Twin for CNC Predictive Maintenance via Innovation-Adaptive Sensor Fusion and Uncertainty-Aware Prognostics | `10.3390/machines14030335` | Digital-twin state estimation, multi-rate sensor fusion, diagnosis, and RUL. |
| `paper-0026` | Physics-Informed Monotonic Conformer for Remaining Useful Life Prediction of Hydraulic Systems | `10.3390/s26072178` | Monotonic physical constraints and deep RUL prediction. |
| `paper-0047` | A Deep Learning Framework for Remaining Useful Life Prediction of Turbofan Engines with Partial Sensor Failure | `10.1371/journal.pone.0347312` | RUL extraction when the study also models missing or damaged sensors. |
| `paper-0104` | SCADA-Based Stator-Winding Prognostics: A Temperature-Weighted Work Index for Industrial Motor Health Monitoring | `10.3390/machines14040425` | A physics-informed health proxy built from asynchronous SCADA data. |
| `paper-0201` | Intelligent Tool Wear Monitoring Using XGBoost, SVR, and DNN Models in NMQL Environment | `10.1038/s41598-026-40968-8` | Several independently evaluated models for the same wear target. |
| `paper-0228` | A Bayesian Prognosis Framework for Rolling Bearings Based on Total Harmonic Distortion Health Indicator and Nonlinear Wiener Process | `10.37965/jdmd.2026.1116` | Health-indicator construction followed by stochastic RUL estimation. |
| `paper-0273` | Physics-Enhanced Orthogonal Sensing for Self-Supervised Anomaly Detection in Rolling Mills | `10.3390/s26092895` | Sensing architecture, physical constraints, self-supervision, and anomaly detection. |
| `paper-0280` | Early Fault Detection in Gearboxes via Dynamic Principal Component Analysis-Driven Multivariate Statistical Process Control | `10.1371/journal.pone.0348497` | A classical statistical process-monitoring baseline rather than deep learning. |
| `paper-0284` | Explainable Machine Learning for Incipient Anomaly Detection in a Compact Molten Salt Heat Exchanger | `10.1038/s41598-025-27112-8` | Incipient faults, overlapping classes, explainability, and an uncommon asset. |
| `paper-0319` | Condition Diagnostics of Marine Centrifugal Pumps Based on Blade-Passing Frequency Harmonics with Analytical DFT Leakage Compensation | `10.2478/pomr-2026-0026` | Analytical signal processing and condition diagnosis without a conventional neural model. |
| `paper-0320` | GPCN: A Decomposition-Based Hybrid Model for Lithium-Ion Capacity Forecasting and RUL Inference | `10.3390/wevj17040171` | CEEMDAN, TCN, and Gaussian-process components linked to forecasting and RUL. |
| `paper-0330` | A Simulation Study on Wear Monitoring and Prognosis in Electro-Mechanical Brakes for a Small Passenger Aircraft | `10.3390/act15030161` | Simulation evidence, wear monitoring, and particle-filter prognosis. |
| `paper-0343` | Identification Model of Distribution Equipment Insulation Aging Enhancement Based on SCADA Knowledge Graph | `10.1186/s42162-026-00639-4` | Knowledge-graph input, multimodal SCADA data, and aging-state identification. |
| `paper-0378` | Intelligent Information Fusion for Safety-Critical Icing Detection via Machine Learning and Reliability Analysis in Wind Turbine Systems | `10.1007/s10791-026-09949-3` | Structural and environmental fusion with five competing classifiers. |
| `paper-0386` | Spatio-Temporal Joint Network for Coupler Anomaly Detection Under Complex Working Conditions Utilizing Multi-Source Sensors | `10.3390/s26092661` | A train coupler, multi-source sensing, and graph-based anomaly detection. |
| `paper-0396` | Subway Door Fault Prediction Employing Stacking Ensemble Learning | `10.1038/s41598-026-43371-5` | Rare-event prediction, physically constrained augmentation, and stacking. |
| `paper-0464` | Physics-Informed Domain Adaptation for Stator Inter-Turn Short Circuit Diagnosis in Synchronous Machines | `10.3390/en19092231` | Simulation-to-real transfer, physical constraints, and fault diagnosis. |
| `paper-0489` | XGBoost for Multi-Fault Diagnosis and Prediction in Permanent Magnet Synchronous Machines | `10.3390/electronics15081759` | Detection, classification, and severity assessment for several fault types. |
| `paper-0546` | An Intelligent Condition-Monitoring Framework for Alkaline Water Electrolyzers Based on Hybrid Physics-Informed Health Indicators | `10.3390/s26041090` | CFD-derived data, health-indicator construction, and health-state classification. |
| `paper-0684` | A Small-Sample Fault Diagnosis Method for High-Voltage Circuit Breaker Spring Mechanisms Based on Multi-Source Feature Fusion and Stacking Ensemble Learning | `10.3390/s26051485` | Mechanical and electrical signals, scarce data, feature fusion, and stacking. |
| `paper-1153` | Stress-Based Fatigue Diagnosis of Wind Turbine Blades Using Physics-Informed AI Reduced-Order Modeling | `10.3390/en19010202` | Reduced-order modeling, a physics-based fatigue index, and anomaly detection. |
| `paper-1679` | Maintenance-Aware Risk Curves: Correcting Degradation Models with Intervention Effectiveness | `10.3390/app152010998` | Maintenance interventions and corrected risk curves that may expose representation gaps in OPMAD. |

## Reserves

These are useful replacements if a shortlisted full text is ineligible, lacks clear case boundaries, or duplicates another article too closely.

| ID | Article | DOI | Reason to retain |
|---|---|---|---|
| `paper-0255` | A Hybrid Ensemble and Explainable AI Framework for Predictive Maintenance of Industrial Equipment | `10.37965/jait.2026.0939` | Ensemble and SHAP extraction, subject to confirming a concrete maintainable item. |
| `paper-0424` | Assessment of a 40-Year-Old Induction Motor Using Hybrid Diagnostic and AI-Based Predictive Techniques | `10.1038/s41598-026-44319-5` | Several diagnostic methods applied to one unusually old operational asset. |
| `paper-0501` | A Simple Comparative Study on the Effectiveness of Bearing Fault Detection Using Different Sensors | `10.3390/machines14030351` | A simple sensor-comparison case with clear fault-detection evidence. |
| `paper-0583` | A Lithium-Ion Battery RUL Method Based on a Wiener-Process Degradation Model and Physics-Informed Neural Network | `10.1155/er/9923180` | Direct comparison of stochastic degradation modeling and a PINN. |
| `paper-0623` | Condition-Based Maintenance Decision-Making of Planetary Gearboxes Using TCN Autoencoders and a Wiener Process | `10.32604/cmc.2025.069194` | Full-lifecycle degradation, anomaly encoding, RUL, and maintenance decisions. |
| `paper-0754` | Domain-Adapted Explainability for Machine Learning Predictions of Rotodynamic Pump Degradation | `10.1177/09576509251387765` | Real pump data and domain-specific explanation requirements. |
| `paper-1551` | Simulating Run-to-Failure SCADA Time Series to Enhance Wind Turbine Fault Detection and Prognosis | `10.5194/wes-10-2563-2025` | Synthetic data generation linked to both detection and prognosis. |
| `paper-1740` | A Machine Learning Approach to Valve Plate Failure Prediction in Piston Pumps Under Imbalanced Data Conditions | `10.3390/app152111542` | A real pump failure case with several balancing strategies. |

## Checks required before freezing the corpus

1. Verify each stored PDF and Markdown conversion against DOI, title, authors, year, and completeness.
2. Confirm that the article implements and evaluates at least one eligible diagnostic or prognostic case.
3. Record a manual pre-characterization of likely function, asset, case count, model-set complexity, and evidence location without using evaluated extraction output.
4. Replace near-duplicates so that one asset or model family does not dominate the challenge set.
5. Verify licences for released annotations and evidence excerpts.
6. Freeze the development and held-out partitions before ontology evolution, prompt selection, or normalization design.
