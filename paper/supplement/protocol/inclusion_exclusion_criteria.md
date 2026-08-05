# Inclusion and Exclusion Criteria for Predictive Maintenance Paper Screening

Source file: `extraction_papers/scopus_export_May 26-2026.csv`  
Purpose: remove papers that were retrieved by keyword matches but are unrelated to predictive maintenance of engineered assets before attempting PDF retrieval again.

## Scope Definition

For this screening, **predictive maintenance** means the use of data, models, monitoring, diagnostics, prognostics, or optimization to support maintenance-related decisions for an **engineered physical asset**.

A paper should normally be included only when it satisfies both conditions below:

1. **Physical asset condition**: the monitored or predicted entity is an engineered physical asset, machine, component, production system, or technical device. Civil/geotechnical infrastructure is excluded unless the target is electromechanical equipment installed in that infrastructure.
2. **Maintenance purpose condition**: the prediction, monitoring, diagnosis, prognosis, or optimization supports maintenance, inspection, repair, replacement, reliability management, asset health assessment, fault management, degradation tracking, remaining useful life estimation, or condition-based decision-making.

Practical screening question:

> If the prediction or monitoring result is correct, would it help decide when to inspect, repair, replace, operate safely, or maintain a physical asset?

If the answer is clearly **yes**, include. If the answer is clearly **no**, exclude. If unclear, send to manual review.

---

## Inclusion Criteria

Include papers that meet at least one of the following criteria and are about engineered physical assets.

### 1. Explicit predictive maintenance or condition-based maintenance

Include papers explicitly about:

- predictive maintenance / PdM
- condition-based maintenance / CBM
- preventive maintenance when data-driven or condition-driven
- maintenance scheduling or maintenance optimization based on asset condition
- maintenance decision-making under degradation or failure risk

### 2. Prognostics and health management of physical assets

Include papers on:

- prognostics and health management (PHM) for equipment, machinery, vehicles, industrial systems, or electromechanical infrastructure equipment
- asset health monitoring
- equipment health monitoring
- machine health monitoring
- health index construction for physical assets
- state-of-health estimation for batteries, fuel cells, power electronics, machinery, or other engineered systems

### 3. Remaining useful life or lifetime prediction

Include papers on:

- remaining useful life (RUL)
- remaining useful lifetime
- residual life / remaining service life
- life prediction, lifetime prediction, or degradation-based reliability prediction

when the target is a physical component, machine, device, or electromechanical/industrial asset.

Examples of usually relevant targets:

- bearings, gearboxes, shafts, motors, pumps, compressors, turbines
- aircraft engines, marine engines, railway vehicles, automotive systems
- batteries, fuel cells, power electronics, transformers, cables, inverters
- CNC tools, cutting tools, industrial robots, manufacturing equipment
- bridges, pavements, pipelines, pressure vessels, offshore/wind structures

### 4. Fault diagnosis, fault detection, fault prediction, or anomaly detection for assets

Include papers where faults/anomalies are associated with technical asset condition or operation, such as:

- bearing fault diagnosis
- gearbox fault detection
- transformer fault prediction
- turbine blade crack detection
- motor vibration anomaly detection
- tool wear monitoring
- cable degradation diagnosis
- photovoltaic inverter failure prediction
- industrial process equipment fault diagnosis

### 5. Structural health monitoring of industrial or electromechanical assets

Include structural health monitoring only when the monitored structure is part of an industrial, energy, transport-vehicle, or electromechanical asset that is in scope for predictive maintenance.

Relevant included examples:

- pressure vessels, pipelines, boilers, tanks, and industrial piping
- offshore wind turbine structures, wind turbine blades, and towers
- aircraft, ship, vehicle, and rail-vehicle structures or components
- bogies, axles, wheels, suspension systems, and other rolling-stock components
- industrial machinery frames, tools, fixtures, shafts, bearings, and rotating machinery
- facility service equipment such as HVAC units, tunnel ventilation fans, pumps, and compressors

Civil/geotechnical infrastructure monitoring is now outside the target scope unless the paper explicitly concerns the maintenance of electromechanical equipment installed in that infrastructure.

### 6. Medical, healthcare, biotech, and pharmaceutical domains when the target is equipment

Do **not** exclude medical or biotech subject areas automatically. Include papers from these domains when the target is an engineered asset or production equipment.

Include examples:

- predictive maintenance of biomedical equipment
- medical device maintenance or RUL prediction
- MRI machine predictive maintenance
- endoscope degradation or repair/replacement prediction
- dental chair failure analysis
- hospital equipment maintenance scheduling
- lithium-ion battery RUL for portable medical devices
- pharma air compressor fault prediction
- predictive maintenance of biopharmaceutical valves or production equipment
- maintenance of laboratory or biomedical sensors/devices

### 7. Agriculture, food, and biotechnical systems when the target is machinery or equipment

Include papers if they concern machinery, industrial systems, or production equipment, for example:

- agricultural machinery predictive maintenance
- cotton harvester drivetrain fault diagnosis
- food processing equipment condition monitoring
- brewery equipment or sensor-based process equipment maintenance
- biotechnical systems where the monitored object is machinery or hydraulic/mechanical equipment

---

## Exclusion Criteria

Exclude papers that match predictive-maintenance keywords only incidentally and do not address maintenance of engineered physical assets.

### 1. Human clinical outcome prediction

Exclude papers where the target is a patient, disease, clinical outcome, treatment response, diagnosis, prognosis, or health risk.

Exclude examples include papers about:

- heart failure prediction
- postoperative respiratory failure prediction
- liver failure prediction
- kidney graft failure prediction
- melanoma diagnosis or prognosis
- glaucoma surgical outcome prediction
- diabetes or prediabetes prediction
- obesity or weight-loss maintenance
- cardiovascular disease diagnosis
- fetal health classification
- Parkinson tremor monitoring
- ECG-based disease diagnosis
- remote patient monitoring
- public health or population health management

Important distinction:

- **Exclude**: predicting failure or disease in humans.
- **Include**: predicting failure, degradation, RUL, or maintenance needs of medical devices or biomedical equipment.

### 2. Biological organism, biomolecule, microbiology, or fermentation science

Exclude papers where the target is a biological process, organism, protein, gene, enzyme, microbiome, or fermentation pathway rather than equipment maintenance.

Exclude examples include papers about:

- microbiota dynamics
- microbial shift during fermentation
- protein or enzyme degradation in cells
- fungal cell walls
- biosynthetic pathways
- bacterial or gene-cluster analysis
- biogenic amine production during food fermentation
- animal or plant biological performance

Important distinction:

- **Exclude**: biological degradation or biological health as the research object.
- **Include**: degradation, failure, or maintenance of biotech/pharmaceutical production equipment.

### 3. Software, code, cloud-service, or cybersecurity fault prediction

Exclude papers where the target is software quality, code defects, cloud jobs, pods, cyberattacks, or digital service failures rather than physical asset maintenance.

Exclude examples include:

- software fault prediction
- software defect prediction
- technical debt prediction
- code smell detection
- firmware defect prediction without hardware-maintenance context
- Kubernetes pod failure prediction
- cloud task failure prediction
- cloud disaster recovery models
- cyberattack or intrusion prediction
- network attack detection

Important distinction:

- **Exclude by default**: software maintenance and IT service reliability.
- **Manual review**: industrial IoT cybersecurity papers if they are directly tied to maintenance or operational safety of physical assets.

### 4. Business, finance, organizational, or social failure prediction

Exclude papers where the target is business viability, bankruptcy, financial distress, organizational performance, adoption behavior, or social outcomes.

Exclude examples include:

- business failure prediction
- small business viability prediction
- financial distress prediction
- entrepreneurial resilience
- AI adoption by firms
- supply-chain management without equipment maintenance
- hospitality/service management without physical asset maintenance
- staffing or workload prediction not tied to maintenance execution

Important distinction:

- **Exclude**: business failure as an economic outcome.
- **Include**: spare-parts logistics, maintenance crew scheduling, or maintenance supply-chain papers if they support maintenance of physical assets.

### 5. Civil, geotechnical, and infrastructure monitoring outside the target scope

Exclude civil/geotechnical/infrastructure papers where the primary target is the condition, deformation, cracking, deterioration, or safety of built infrastructure or natural ground rather than industrial/electromechanical equipment.

Exclude examples include:

- surrounding-rock deformation or tunnel deformation prediction
- slope, landslide, rock, soil, strata, or geotechnical failure prediction
- road, highway, pavement, pothole, road-surface, or skid-resistance monitoring
- bridge, viaduct, girder, dike, levee, or concrete-structure monitoring
- building, cultural-heritage, masonry, or facility-structure condition assessment
- railway track, ballast, slab-track, rail-surface, turnout, frog, or subgrade condition monitoring
- concrete, reinforced-concrete, cementitious, mortar, asphalt, or construction-material failure prediction
- construction-stage monitoring, construction risk mitigation, or structural safety assessment without a maintenance decision for equipment

Important distinction:

- **Exclude**: civil infrastructure condition monitoring, even if the abstract mentions predictive maintenance or infrastructure monitoring.
- **Include**: electromechanical equipment located inside infrastructure, such as tunnel ventilation fans, pumps, compressors, transformers, cables, railway vehicles/bogies/axles/wheels, TBM cutterheads/cutters, or other machinery.

### 6. Natural/environmental/ecological monitoring without asset maintenance

Exclude papers where the target is a natural system or environmental process rather than an engineered asset.

Exclude examples include:

- forest or tree-canopy modelling
- soil erosion or sedimentation assessment
- agricultural drought monitoring
- crop or leaf segmentation
- lake bathymetry
- wildfire risk modelling without asset-maintenance decision support
- vegetation monitoring without utility/equipment maintenance context
- climate-change impact studies without maintenance of assets

Important distinction:

- **Exclude**: monitoring natural systems for ecological/agricultural/environmental analysis.
- **Include/manual review**: only when there is a clear physical-equipment maintenance target.

### 7. Generic AI, optimization, or process monitoring without maintenance intent

Exclude papers that use prediction, monitoring, digital twins, or AI for objectives unrelated to maintenance or asset condition.

Exclude examples include:

- generic quality control
- production process monitoring without faults/degradation/maintenance
- energy management or predictive control without asset health
- traffic management
- inventory optimization without maintenance linkage
- generic digital twin architecture without asset degradation or maintenance use case
- generic generative AI or Industry 4.0 discussion without a maintenance application

Important distinction:

- **Exclude**: prediction for operational optimization only.
- **Include**: prediction for degradation, fault prevention, maintenance scheduling, or asset-health-based decisions.

### 8. Acronym-only false positives

Exclude papers where maintenance-related acronyms are used with unrelated meanings.

Common false-positive acronym meanings:

| Acronym | Relevant meaning | Exclude when it means |
|---|---|---|
| PDM | predictive maintenance | primary dermal melanoma; pickled/dried mustard; prediabetes mellitus; pulse-density modulation; Poincare discontinuity mapping; positive displacement motor |
| CBM | condition-based maintenance | carbohydrate-binding module; concept bottleneck model; conduction band minimum; circular business model |
| PHM | prognostics and health management | personal health management; population health management; public health management; clinical health management |
| RUL | remaining useful life | include only if the remaining life is of a physical asset/component/device |

Acronym-only matches should not be sufficient for inclusion unless the abstract/title clearly establishes a maintenance context.

---

## Manual Review Criteria

Send a paper to manual review when:

- the title/abstract mentions prediction, monitoring, degradation, or failure, but the target asset is unclear;
- the paper is in medicine/biotech/agriculture but may concern equipment rather than humans/organisms;
- the paper concerns infrastructure or natural hazards and may support maintenance or inspection planning for electromechanical equipment;
- the paper discusses digital twins, IoT, or Industry 4.0 but the maintenance connection is implicit rather than explicit;
- the paper is about software/IT systems embedded in physical infrastructure and may affect operational maintenance or safety;
- the title suggests process monitoring, but the abstract may reveal equipment fault detection or RUL prediction.

Suggested manual-review labels:

- `include`
- `exclude_clinical`
- `exclude_bio`
- `exclude_software_it`
- `exclude_business_social`
- `exclude_environment_natural_system`
- `exclude_generic_ai_control`
- `exclude_acronym_collision`
- `manual_review_unclear_asset`
- `manual_review_unclear_maintenance_purpose`

---

## Decision Rules for Automated Filtering

A conservative automated filter should use both positive and negative signals.

### Strong positive signals

A record is more likely to be relevant if the title, abstract, or keywords contain one or more maintenance-purpose terms:

- predictive maintenance
- condition-based maintenance
- condition based maintenance
- maintenance scheduling
- maintenance optimization
- maintenance decision
- asset health
- equipment health
- machine health
- prognostics and health management
- remaining useful life / RUL
- remaining service life
- state of health / SOH
- degradation monitoring
- fault diagnosis
- fault detection
- fault prognosis
- fault prediction
- failure prognosis
- anomaly detection for equipment
- structural health monitoring

and one or more physical-asset terms:

- machine, machinery, equipment, asset, device, component
- bearing, gearbox, shaft, motor, pump, compressor, turbine, engine
- battery, fuel cell, transformer, inverter, cable, power electronics
- CNC, tool, cutting tool, robot, manufacturing system, production equipment
- bridge, pavement, railway, track, tunnel, pipeline, pressure vessel
- aircraft, vehicle, ship, wind turbine, photovoltaic system
- medical device, biomedical equipment, MRI machine, endoscope, dental chair

### Strong negative signals

A record is more likely to be an outlier if the title, source, abstract, or keywords contain domain terms such as:

- heart failure, respiratory failure, liver failure, kidney failure, graft failure
- patient, clinical, disease, surgery, oncology, diabetes, obesity, melanoma, glaucoma
- microbiota, microbial, protein, enzyme, gene, fermentation, Streptomyces, biogenic amine
- software fault, software defect, technical debt, code smell, cloud task, Kubernetes pod
- cyberattack, intrusion detection, denial of service
- business failure, financial distress, SME viability
- forest, soil erosion, sedimentation, crop, drought, lake, landslide, wildfire

However, negative signals should be overridden or manually reviewed if there is a clear in-scope physical-asset maintenance target, especially in medical-device, biotech-production, or electromechanical-equipment contexts.

---

## Examples of Likely Exclusions from the Current CSV

These illustrate the type of outlier to remove; they are not an exhaustive list.

| Example ID | Reason |
|---|---|
| `paper-0010` | PDM means primary dermal melanoma; clinical oncology, not predictive maintenance |
| `paper-0037` | heart failure prediction in medical datasets |
| `paper-0095` | microbiota dynamics during water kefir fermentation |
| `paper-0119` | protein/cell-wall biology; CBM means carbohydrate-binding module |
| `paper-0170` | software fault prediction |
| `paper-0211` | postoperative respiratory failure prediction |
| `paper-0450` | cyberattack detection/prediction |
| `paper-0796` | PDM means pickled/dried mustard fermentation |
| `paper-1122` | small business failure prediction |
| `paper-1537` | business failure prediction |
| `paper-3293` | PDM means prediabetes mellitus |
| `paper-3550` | post-hepatectomy liver failure prediction |
| `paper-3659` | heart failure outcome prediction |
| `paper-3770` | biosynthetic pathway in Streptomyces |
| `paper-3867` | kidney graft failure prediction |

## Examples of Medicine/Biotech-Related Records to Keep

These should not be excluded just because Scopus classifies them under medical/biotech-related areas.

| Example type | Reason to include |
|---|---|
| lithium-ion battery RUL for portable medical devices | physical device/component maintenance and safety |
| implantable cardioverter-defibrillator battery depletion prediction | device battery replacement/maintenance |
| biomedical equipment predictive maintenance | equipment reliability and maintenance |
| MRI machine predictive maintenance | medical equipment maintenance |
| rigid endoscope optical degradation | repair/replacement decision for medical device |
| pharmaceutical air compressor fault prediction | industrial equipment maintenance |
| biopharmaceutical pneumatic valve predictive maintenance | production equipment maintenance |
| medical device residual-current monitoring | condition-based maintenance of equipment |

---

## Recommended Screening Workflow

1. Apply strong negative filters to flag likely outliers.
2. Apply positive physical-asset and maintenance-purpose checks.
3. Automatically exclude only records with strong negative signals and no clear physical-asset maintenance purpose.
4. Automatically include records with strong maintenance-purpose and physical-asset signals.
5. Send ambiguous records to manual review.
6. Re-run PDF retrieval only for `include` and, if desired, `manual_review` records.
