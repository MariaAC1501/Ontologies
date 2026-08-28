---
source: "extraction_papers/10.3390_s26041090.pdf"
title: "10.3390_s26041090"
page_count: 21
converted_at: "2026-08-27T23:11:09Z"
---

<!-- PDF_PAGE: 1 -->









Article

<div align="center">

# An Intelligent Condition-Monitoring Framework for Alkaline Water Electrolyzers Based on Hybrid Physics-Informed Health Indicators

</div>

Jie Liu $ ^{1} $ , Zhiying Wang $ ^{1} $ , Tingting Ma $ ^{1} $ , Xinyue Chen $ ^{1} $ , Zihao Wang $ ^{1} $ , Chao Huang $ ^{2} $ and Yiyang Dai $ ^{2,*} $

1 Xinjiang Chemical Engineering Design & Research Institute Co., Ltd., Urumqi 830010, China; 15739530259@163.com (J.L.); wangzhy1215@163.com (Z.W.); m15899106271@163.com (T.M.); 18690969510@163.com (X.C.); 18129345757@163.com (Z.W.)

$ ^{2} $ School of Chemical Engineering, Sichuan University, Chengdu 610065, China; 2020223070046@alu.scu.edu.cn $ ^{*} $ Correspondence: daiyy@scu.edu.cn; Tel.: +86-180-1060-5143

## Highlights

## What are the main findings?

- A hybrid physics-informed machine learning (ML) framework is proposed for constructing Health Indicators (HIs) and enabling intelligent condition monitoring of Alkaline Water Electrolyzers (AWEs).

- Trained on a CFD-generated dataset, a Multilayer Perceptron (MLP) model achieves 90.43% accuracy in real-time health state classification, serving as an effective intelligent monitoring agent.

- What are the implications of the main findings?

- The proposed methodology provides a practical solution for predictive maintenance of AWEs operating under volatile renewable energy, enhancing system safety and reliability.

- It demonstrates the significant potential of combining mechanistic models with machine learning for intelligent monitoring in complex industrial systems where sensor data is limited.

## Check for updates

## Abstract

Academic Editors: Junyu Qi, Dandan Peng, Xiaoxi Hu and Peng Chen Received: 23 December 2025 Revised: 3 February 2026 Accepted: 4 February 2026 Published: 7 February 2026 Copyright: $ \textcircled{c} $ 2026 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license.

Alkaline Water Electrolyzers (AWEs) are critical for green hydrogen production but face operational risks due to volatile renewable energy inputs. This study proposes an intelligent condition-monitoring framework that leverages a hybrid physics-informed machine learning (ML) methodology to construct Health Indicators (HIs). The core innovation lies in addressing the challenge of inaccessible internal states. First, a high-fidelity Computational Fluid Dynamics (CFD) model is developed and experimentally validated, serving as a physics-informed data generator to simulate multiphysics behavior under various operating and fault conditions. From this reliable simulation basis, a comprehensive dataset is produced, and eight key operational parameters are derived as HIs. This dataset is then used to train and benchmark three ML models for rapid health state classification. The Multilayer Perceptron (MLP) model achieves superior performance with 90.43% accuracy, effectively translating the validated physical understanding into a fast, deployable intelligent monitoring agent. This work presents a viable pathway for constructing reliable HIs and implementing AI-enhanced condition monitoring for AWEs, contributing to safer and more efficient green hydrogen production.

<!-- PDF_PAGE: 2 -->

Keywords: alkaline water electrolyzer; health indicators; condition monitoring; computational fluid dynamics; machine learning; predictive maintenance; intelligent sensing

## 1. Introduction

The global imperative to decarbonize energy systems has driven growing interest in green hydrogen as a sustainable energy carrier. Produced via water electrolysis powered by renewable energy sources (RES), green hydrogen supports deep emission reductions across transportation, industry, and power generation sectors [1-3]. Among electrolysis technologies, Alkaline Water Electrolyzers (AWEs) are the most mature and commercially deployed option for large-scale production due to their low cost, durability, and reliance on non-precious metal catalysts [4-6]. Consequently, AWEs are expected to form the backbone of the emerging green hydrogen economy.

However, coupling AWEs with intermittent RES introduces operational challenges. Fluctuating power input forces AWEs to operate under dynamic and off-design conditions, accelerating degradation and potentially triggering gas crossover, electrode and separator deterioration, thermal instability, and pressure excursions, which compromise efficiency, safety, and asset integrity [7-10]. These risks highlight the urgent need for intelligent, real-time health monitoring and predictive maintenance, aligned with the industrial shift toward Prognostics and Health Management (PHM) and condition-based maintenance (CBM) [11-13]. In this context, Health Indicators (HIs) provide compact representations of system condition, while Digital Twins (DTs) integrate physics-based models and data analytics to enable diagnosis and prediction [14]. For AWEs, effective HIs should combine measurable external variables with internal state information linked to degradation physics, but many internal states—such as local electrolyte concentration, gas holdup, or membrane stress—are inaccessible to conventional sensors.

Two complementary paradigms address this challenge: physics-based modeling and data-driven machine learning (ML) [15-17]. High-fidelity Computational Fluid Dynamics (CFD) enables detailed analysis of multiphysics phenomena in AWEs, including two-phase flow, current density distribution, temperature gradients, and mass transport [18,19]. When experimentally validated, CFD can generate synthetic datasets covering nominal and fault-induced conditions difficult to reproduce safely in experiments [20,21] supporting studies of flow patterns, bubble dynamics, and performance sensitivity [22,23]. However, CFD alone is computationally intensive and unsuitable for real-time monitoring. ML methods, in contrast, efficiently learn nonlinear relationships among operational variables, enabling fast online inference [24-27]. Integrated CFD-ML approaches have been explored to build surrogate models for performance prediction and optimization [28], but existing works primarily target a limited set of outputs or design efficiency, often lacking interpretability and applicability for PHM.

While recent studies have integrated computational fluid dynamics (CFD) and machine learning (ML) for AWE analysis—such as Sirat et al. [28] for performance enhancement and Bai et al. [20] for simulating flow and electric fields—they primarily aim at predicting or optimizing specific physical parameters. In contrast, this study proposes a novel physics-informed health indicator (HI) construction framework for system-level condition monitoring and health state classification. The core methodological innovation addresses the challenge of internal state inaccessibility by translating measurable operational data into actionable health insights for predictive maintenance. To this end, a novel framework founded on the integration of mechanistic CFD modeling and data-driven ML is developed. The foundation of this framework is an experimentally validated CFD model,

<!-- PDF_PAGE: 3 -->

which ensures the physical fidelity of the generated training data. The core contributions are threefold:

1. Development of a Systematic HIs System for AWE: A semi-quantitative health evaluation framework is established based on common AWE failure modes, defining health classes (from excellent to poor) based on thresholds for eight key operational parameters encompassing efficiency, safety, and stability.

2. Generation of a Physics-Informed and Experimentally Validated Dataset: A 2D multiphysics CFD model is developed and experimentally validated. This validated model is then employed to conduct parametric sweeps, creating a comprehensive and physically reliable dataset for ML training.

3. Benchmarking of ML Algorithms for Intelligent Condition Monitoring: Three distinct ML approaches—Polynomial Regression, SVM, and MLP—are implemented and rigorously compared for the task of classifying the health state of the AWE into the predefined categories. The optimal model is identified based on accuracy, robustness, and computational efficiency.

By leveraging the complementary strengths of physics-based simulation and statistical learning, this hybrid methodology delivers a semi-quantitative health evaluation tool effective for condition monitoring under steady-state or slowly varying operating conditions. It represents a step towards intelligent PHM for electrolysis systems, ultimately contributing to safer, more efficient, and more economical green hydrogen production.

The remainder of this paper is structured as follows: Section 2 details the comprehensive methodology, including the overall framework, the development of the multiphysics CFD model for HI data generation, and the configuration of the ML algorithms for intelligent monitoring. Section 3 presents the case study, describing the specific geometric and operational parameters of the AWE system under investigation. Section 4 presents the results and discussion, first validating the reliability of the CFD-generated dataset and then analyzing and comparing the performance of the different ML models. Finally, Section 5 concludes the paper by summarizing the principal findings, discussing the implications for industrial application, and outlining promising directions for future research.

## 2. Methodology for the Intelligent Condition-Monitoring Framework

The proposed methodology for developing an intelligent condition-monitoring system for AWEs follows a structured two-stage hybrid framework, as illustrated in Figure 1. It is designed to systematically define measurable HIs, generate labeled data reflecting the underlying physics, and develop a fast inference model for online deployment.

<!-- PDF_PAGE: 4 -->


![figure_001.png](images/figure_001.png)



<div align="center">

Figure 1. Overall framework of the hybrid physics-informed ML approach for intelligent AWE condition monitoring.

</div>

## 2.1. Definition of the AWE HIs System

The cornerstone of an effective condition-monitoring system is a suite of quantifiable HIs that exhibit high sensitivity to incipient system degradation and failure modes [29]. The development of the HIs system began with a thorough analysis of common faults and failure mechanisms in AWEs [30-32], as summarized in Table 1. These faults, such as gas crossover, electrode corrosion, and overheating, manifest as observable deviations in key process parameters.

<div align="center">

Table 1. Common faults, phenomena, and consequences in AWEs.

</div>

<table border="1"><tr><td>Faults</td><td>Phenomena</td><td>Consequences</td></tr><tr><td>Gas Crossover</td><td>Increase in HTO(Hydrogen in Oxygen stream)/OTH(Oxygen in Hydrogen stream); Increased bubble velocity.</td><td>Risk of explosion if concentration exceeds threshold.</td></tr><tr><td>Electrode Corrosion</td><td>Decrease in electrode thickness; change in surface morphology.</td><td>Loss of efficiency, increased overpotential.</td></tr><tr><td>Hydrogen Leakage</td><td>Decrease in hydrogen content at outlet; detected by sensors.</td><td>Loss of production, potential explosion hazard.</td></tr><tr><td>Overheating</td><td>Abnormal increase in cell or stack temperature.</td><td>Accelerated degradation, thermal stress, potential shutdown.</td></tr><tr><td>Overpressure</td><td>Abnormal increase in system pressure.</td><td>Mechanical stress, potential for rupture or seal failure.</td></tr><tr><td>Control System Failure</td><td>Uncommanded changes or drift in key parameters(voltage, current, flow).</td><td>Unstable operation, potential to induce other faults.</td></tr></table>

The selection of Health Indicators (HIs) in this study follows three guiding principles:

1. Physical relevance to dominant AWE degradation and failure mechanisms.

2. Measurability or inferability under industrial operating conditions.

<!-- PDF_PAGE: 5 -->

## 3. Sensitivity to off-design and fault-related operating regimes.

Based on these criteria, eight key operational variables were identified as HI candidates including Cell Voltage (V), Current Density (A/m $ ^{2} $ ), Operating Temperature ( $ ^{\circ} \mathrm{C} $ ), System Pressure (atm), Electrolyte pH/KOH Concentration (M), Bubble Velocity (m/s), Coulombic Efficiency (%), and Power Load (W).

These variables provide complementary information on electrochemical performance, thermal behavior, mass transport characteristics, chemical stability, and operational safety. To facilitate a structured health assessment, the selected HI candidates are further organized into three health-related dimensions—efficiency and consistency, power regulation flexibility, and gas purity—which together constitute an integrated AWE health indicator framework.

The conceptual mapping between operational variables, health dimensions, and the overall health state evaluation is illustrated in Figure 2.


![figure_002.png](images/figure_002.png)



<div align="center">

Figure 2. HIs for AWE condition monitoring (note that Coulombic efficiency is a derived indicator inferred from current and gas evolution behavior).

</div>

To translate these continuous parameters into actionable diagnostic information, a semi-quantitative evaluation framework was established. For a given operating condition, each of the key parameters is evaluated against the predefined threshold ranges in Table 2 to determine its individual health sub-state. The overall health state of the AWE is then assigned as the most severe sub-state among all parameters, following a conservative logic similar to multi-dimensional risk assessment. The threshold values are not arbitrarily assigned; they are determined through a combination of theoretical electrochemical constraints, validated CFD-based simulation results under both nominal and fault-induced conditions, and operational expertise, enabling systematic differentiation between normal operation, progressive performance degradation, and high-risk fault regimes.

<div align="center">

Table 2. Criterion of AWE health condition (Voltage and current density are excluded from thresholding due to strong load dependence and redundancy under variable-power operation).

</div>

<table border="1"><tr><td></td><td colspan="6">Threshold Ranges for Health State Classification</td></tr><tr><td>Health State</td><td>Temperature/℃</td><td>Pressure/atm</td><td>pH</td><td>Efficiency%</td><td>Bubble Velocity/m·s-1</td><td>Load/W</td></tr><tr><td>A</td><td>67≤T&lt;71</td><td>0.96≤P&lt;1.02</td><td>14.77≤pH&lt;14.80</td><td>η≥40</td><td>v≤0.15</td><td>p≥0.15</td></tr><tr><td>B</td><td>71≤T&lt;73</td><td>0.93≤P&lt;0.96</td><td>pH≥14.80</td><td>35≤η&lt;40</td><td>0.15&lt;v≤0.18</td><td>0.10≤p&lt;0.15</td></tr><tr><td>C</td><td>T&lt;67</td><td>0.90≤P&lt;0.93</td><td>14.75≤pH&lt;14.77</td><td>30≤η&lt;35</td><td>0.18&lt;v≤2.00</td><td>0.05≤p&lt;0.10</td></tr><tr><td>D</td><td>T≥73</td><td>P&lt;0.90</td><td>pH&lt;14.75</td><td>η&lt;30</td><td>v&gt;2.00</td><td>p&lt;0.05</td></tr></table>

<!-- PDF_PAGE: 6 -->

Although eight HIs were initially examined, only six representative indicators are retained for threshold-based classification in Table 2. This reduction is motivated by the intrinsic coupling among cell voltage, current density, power load, and efficiency, particularly under variable-power and load-following operating conditions typical of renewable-driven AWEs. Under such conditions, fixed thresholding of voltage or current alone cannot reliably distinguish between normal operational variability and genuine degradation or fault behavior. Including all coupled variables would therefore introduce redundancy without improving diagnostic discriminative capability. Consequently, parameters exhibiting relatively independent physical significance and higher sensitivity to fault-related deviations were prioritized to enhance the robustness and interpretability of the semi-quantitative health evaluation.

This HIs system provides the essential "vocabulary" for health assessment. The subsequent steps aim to build a model that can automatically assign these health-state labels (A-D) based on a subset of easily measurable inputs.

To further clarify the relationship between the defined health indicators and the machine learning classifier, a conceptual workflow is illustrated in Figure 3. This diagram depicts the process from CFD-based data generation, HI extraction, to the MLP classifier for health state prediction. In addition, feature importance analysis using SHAP values is integrated, highlighting the contribution of each HI to the classification of all health states. This enhancement provides both a clear visual mapping of the methodology and interpretable insights into model decision-making.


![figure_003.png](images/figure_003.png)



<div align="center">

Figure 3. Conceptual workflow of the HI-based monitoring system for AWEs, showing CFD/experimental data, HI extraction, MLP classifier, and health state classification.

</div>

## 2.2. Physics-Informed Data Generation via CFD Modeling

To generate the labeled dataset required to train the monitoring model, a high-fidelity, physics-based CFD model of a generic AWE unit cell is developed. This model serves as a physics-informed data generator, simulating the complex, coupled electrochemical, thermal, and fluid dynamic processes to compute all eight HIs under a wide range of prescribed operating conditions.

It should be noted that the present CFD model adopts a two-dimensional representation and a simplified bubble size assumption. These choices are made to balance physical fidelity and computational efficiency, enabling large-scale parametric data generation for health indicator development. While three-dimensional bubble interactions and bubble size distributions may influence local flow structures, the adopted model is sufficient to capture the dominant coupled electrochemical- transport trends relevant to relative health state discrimination. Future work will extend the framework to incorporate 3D effects and population balance models as higher-fidelity experimental data become available. All simulations in this study were conducted using the commercial finite element software COMSOL Multiphysics (Version 6.1).

<!-- PDF_PAGE: 7 -->

## 2.2.1. Electrochemical Reaction Fundamentals

The electrolysis reaction in an AWE cell is governed by the decomposition of water into hydrogen and oxygen under an applied direct current, as expressed by the overall reaction:

$$
\mathrm {H} _ {2} \mathrm {O} \rightarrow \mathrm {H} _ {2} + \mathrm {O} _ {2}
$$

This occurs via two half-reactions at the electrodes immersed in an alkaline electrolyte (typically KOH solution). At the cathode, the Hydrogen Evolution Reaction (HER) takes place:

$$
2 \mathrm {H} _ {2} \mathrm {O} + 2 \mathrm {e} ^ {-} \rightarrow \mathrm {H} _ {2} + 2 \mathrm {O H} ^ {-}
$$

At the anode, the Oxygen Evolution Reaction (OER) occurs:

$$
2 \mathrm {O H} ^ {-} \rightarrow \mathrm {O} _ {2} + \mathrm {H} _ {2} \mathrm {O} + 4 \mathrm {e} ^ {-}
$$

## 2.2.2. Model Geometry and Mesh Strategy

A common approach involves constructing a simplified 2D geometry representing a symmetric cross-section of a unit cell, comprising the electrode compartments and a separating diaphragm. The geometry is discretized using a structured or mapped mesh to balance accuracy and computational cost. Critical regions, especially the electrode surfaces where bubbles nucleate and reactions occur, require mesh refinement (e.g., boundary layers) to accurately capture steep gradients in species concentration, current density, and gas volume fraction.

## 2.2.3. Mathematical Formulation and Governing Equations

The CFD model was implemented using the "Water Electrolyzer" interface in COMSOL, which couples multiple physics interfaces. The core mathematical descriptions include the solution of the governing equations for conservation of mass, momentum, species, and charge, along with the Butler-Volmer electrochemical kinetics. Key constitutive relations and corrections are as follows:

## 1. Electrochemistry and Charge Transport

The local current density distribution is governed by Butler-Volmer kinetics [33]. The presence of generated gas bubbles significantly affects the system by reducing the effective area for reaction and charge transport. To account for this, the effective electrolyte conductivity $ \sigma_{l,eff} $ and the effective exchange current density $ i_{0,eff} $ are corrected using the Bruggeman correlation, which is standard for porous media and two-phase flows in electrochemical cells [34,35]:

$$
\sigma_ {l, e f f} = \left(1 - \phi_ {d}\right) ^ {1. 5} \sigma_ {l}
$$

$$
i _ {0, e f f} = \left(1 - \phi_ {d}\right) i _ {0}
$$

where $ \phi_{d} $ is the local gas volume fraction, and $ \sigma_{l} $ and $ i_{0} $ are the conductivity and exchange current density of the bubble-free electrolyte, respectively.

## 2. Multiphase Flow Dynamics

The bubbly flow of $ \mathrm{H}_{2} $ and $ \mathrm{O}_{2} $ was simulated. within the electrolyte channels is simulated using the Euler-Euler module [36], which is well suited for modeling dispersed gas phases in liquid electrolytes. In the present framework, gas bubbles are represented using a constant, representative diameter, serving as a closure assumption to enable efficient simulation of gas-liquid momentum exchange under varying operating conditions. This treatment focuses on capturing physically consistent trends in two-phase transport behavior rather than resolving detailed bubble population dynamics.

<!-- PDF_PAGE: 8 -->

The momentum exchange between the gas bubbles and the liquid electrolyte includes a bubble dispersion force $ F_{BD} $ to model the turbulent dispersion of bubbles, a critical phenomenon in electrolyzer flows [37]:

$$
F _ {B D} = - \phi_ {d} \rho_ {l} \frac {K _ {g}}{d _ {b}} \left| u _ {s l i p} \right| \nabla \phi_ {d}
$$

where $ \rho_{l} $ is the liquid density, $ K_{g} $ is the dispersion coefficient, $ d_{b} $ is the bubble diameter, and $ u_{slip} $ is the slip velocity between phases.

## 3. Mass, Species, and Energy Transport

Coupled equations for continuity, species conservation $ \mathrm{(K^{+}, O H^{-}} $), and energy balance are solved to obtain spatial distributions of electrolyte concentration and temperature, which in turn influence reaction kinetics and material properties.

## 4. Numerical Methods and Model Purpose

The equations are solved using a segregated steady-state solver on a structured/polyhedral mesh. Convergence is monitored via residuals of all governing equations $ (< 1 0^{-6}) $ . The model is designed primarily as a physics-informed data generator for constructing health indicators and training ML classifiers, providing accurate global trends while enabling efficient exploration of multiple operating and fault scenarios.

## 2.2.4. Parametric Sweep for Dataset Generation

To create a comprehensive dataset that populates the health state space defined by the HIs system, a systematic parametric sweep is performed. Key operational input variables-such as cell voltage, operating temperature, system pressure, and electrolyte concentration-are varied across predefined ranges that encompass both normal and fault-inducing conditions. For each simulated steady-state operating point, the values of the eight target HIs are extracted. Each data sample is then automatically labeled with a health state (A-D) by applying the threshold rules from the HIs system (Table 2), resulting in a physics-consistent, labeled dataset for ML

This process yields a physics-consistent, labeled dataset $ ( U,T,p,c_{K O H},\dots) \rightarrow( H I_{1},H I_{2}, $ $ \dots, H I_{6}, HealthState) $ that forms the basis for training the data-driven monitoring model.

## 2.3. ML Model Development for Intelligent Inference

The computationally intensive CFD model is unsuitable for real-time deployment. This phase focuses on distilling the physical knowledge encoded in the CFD-generated dataset into a fast and accurate data-driven surrogate model for online intelligent monitoring.

## 2.3.1. Data Preprocessing and Feature Engineering

The raw dataset $ D=\{x_{i},y_{i}\}_{i=1}^{N} $ from CFD simulations is preprocessed. Here, $ \mathbf{x}_{i} $ is a vector containing the operational input parameters and potentially derived features, and $ y_{i}\in\{A,B,C,D\} $ is the health state label. Common preprocessing steps include:

1. Handling Missing Values: Removing or imputing samples where CFD simulations failed to converge.

2. Normalization/Standardization: Features often have different scales (e.g., volts, $ ^{\circ} \mathrm{C} $ atm). Min-max normalization or z-score standardization is applied to improve model convergence and performance. Min-max normalization scales a feature xx to the range [0,1]:

$$
x _ {\mathrm {n o r m}} = \frac {(x - \min (x))}{(\max (x) - \min (x))}
$$

<!-- PDF_PAGE: 9 -->

3. Feature Selection/Construction: The input feature vector x is constructed from the most informative and easily measurable parameters. This typically includes the swept input variables (e.g., voltage, temperature) and key calculated outputs from the model that have strong correlations with the health state.

## 2.3.2. Model Training and Benchmarking Strategy

The preprocessed dataset is split into training, validation, and test sets. Multiple ML algorithms are benchmarked for the multi-class classification task (predicting health state A-D). Common choices include:

- Polynomial Regression: Serves as an interpretable baseline. The model's capacity is controlled by the polynomial degree.

- SVM: A robust classifier effective in high-dimensional spaces. Kernels such as linear, polynomial, and radial basis function (RBF) are evaluated to capture potential nonlinear decision boundaries.

- MLP: A flexible feedforward artificial neural network capable of modeling complex, non-linear relationships between inputs and the health state, representing a state-of-the-art approach for pattern recognition.

The preprocessed dataset is split into a training set (e.g., 70-80%) and a hold-out test set. Each model is trained on the training set via supervised learning. Hyperparameter tuning is performed using techniques like grid search or random search, optimized based on performance on a separate validation set or via cross-validation.

## 2.3.3. Model Evaluation Metrics

The primary evaluation metric is the classification accuracy on the held-out test set. Accuracy is defined as the proportion of correctly classified samples:

$$
\mathrm {A c c u r a c y} = \frac {1}{N _ {\mathrm {t e s t}}} \sum_ {i = 1} ^ {N _ {\mathrm {t e s t}}} \mathbb {I} \left(\hat {y} _ {i} = y _ {i}\right)
$$

where $ \hat{y}_{i} $ is the predicted label, $ y_{i} $ is the true label, and $ \mathbb{I}(\cdot) $ is the indicator function.

While accuracy provides a high-level summary of model performance, a more granular and informative analysis is achieved through the confusion matrix. This n $ \times $ n matrix (where n is the number of classes, here n = 4 for health states A-D) is structured such that each row represents the true health state, and each column represents the predicted health state. The diagonal elements, known as True Positives (TP), indicate the number of instances correctly predicted for each corresponding state, with stronger models exhibiting higher values concentrated along this diagonal. The off-diagonal elements capture misclassifications: False Positives (FP) for a class appear in its corresponding column (excluding the diagonal), representing healthier states incorrectly alarmed as that class, while False Negatives (FN) for a class appear in its corresponding row (excluding the diagonal), indicating instances of that class missed by the model and predicted as other states.

In the context of AWE condition monitoring, analyzing these off-diagonal entries is crucial for identifying critical error types such as missed faults, where a true fault state is incorrectly predicted as healthier, posing a direct safety risk, and false alarms, where a normal or mildly degraded state is incorrectly predicted as a severe fault, potentially leading to unnecessary maintenance and operational disruption. Thus, the confusion matrix not only validates overall accuracy but also assesses the model's diagnostic consistency and its balance between fault sensitivity and operational reliability, ensuring the selected intelligent monitoring agent is robust and trustworthy for real-world deployment [38].

<!-- PDF_PAGE: 10 -->

## 3. Case Study: Application to a Laboratory-Scale AWE

This section details the specific application of the proposed hybrid framework to a concrete laboratory-scale AWE, providing the precise parameters and configurations that instantiate the general methodology.

## 3.1. System Description and Experimental Setup

The subject of this case study is a rectangular, filter-press type AWE cell, a photograph of which is shown in Figure 4. This configuration is widely used in laboratory research for its well-defined geometry and ease of instrumentation.


![figure_004.png](images/figure_004.png)



<div align="center">

Figure 4. Photograph of the laboratory-scale AWE test rig used as the basis for this case study.

</div>

All experiments were performed using a laboratory-scale, bipolar filter-press alkaline water electrolyzer possessing a nominal hydrogen production capacity of $ 2 \mathrm{N m}^{3} / \mathrm{h} $ The test platform enables controlled adjustment of key operating parameters, including current density, electrolyte concentration, temperature, and pressure, providing a reliable experimental basis for model validation and condition-monitoring studies.

## 3.2. CFD Model Implementation

## 3.2.1. Geometry and Mesh

The model geometry, depicted in Figure 5a, represents a simplified 2D cross-section of a symmetric AWE cell, consisting of anode and cathode compartments (2 mm width each) separated by a porous diaphragm (1 mm width), with an electrode height of 0.1 m (Figure 5b). The mesh consisted of approximately 25,000 rectangular elements. A mapped mesh was used in the bulk regions, and a boundary layer mesh with two layers (each $ 3\times1 0^{-5} $ m thick) was applied at the electrode surfaces to capture the critical near-wall phenomena, following the strategy outlined in Section 2.2.2.


![figure_005.png](images/figure_005.png)



<div align="center">

(a)

</div>


![figure_006.png](images/figure_006.png)



<div align="center">

(b)

</div>

<div align="center">

Figure 5. (a) Schematic diagram of an AWE electrolyzer; (b) 2D geometry model used in the CFD simulation (The gravity direction is indicated by the arrow).

</div>

<!-- PDF_PAGE: 11 -->

The CFD mesh is shown in Figure 6, illustrating the mapped bulk mesh and boundary layer refinement at the electrode surfaces.


![figure_007.png](images/figure_007.png)



<div align="center">

Figure 6. CFD mesh used in the simulation: mapped mesh in the bulk regions and two-layer boundary layer at electrode surfaces (layer thickness $ 3\times1 0^{-5} $ m, total ~25,000 elements). (The gravity direction is indicated by the arrow).

</div>

## 3.2.2. Boundary Conditions, Assumptions, and Global Parameters

The model setup and key global parameters are summarized in Figure 7 and Table 3. The assumptions listed in Section 2.2 were applied. The electrolyte inlet velocity was set to 0.1 m/s for both compartments. The baseline operating conditions and material properties were defined as follows:


![figure_008.png](images/figure_008.png)



<div align="center">

Figure 7. Schematic diagram of the initial and boundary conditions applied in the CFD model.

</div>

<div align="center">

Table 3. Global parameters and constants for the specific laboratory-scale AWE CFD model.

</div>

<table border="1"><tr><td>Parameter</td><td>Symbol</td><td>Value</td><td>Unit</td><td>Description</td></tr><tr><td>Compartment Width</td><td>W_H2,W_O2</td><td>2</td><td>mm</td><td>Width of H2and O2compartments</td></tr><tr><td>Diaphragm Width</td><td>W_sep</td><td>1</td><td>mm</td><td>Width of the separator</td></tr><tr><td>Cell Width</td><td>W_cell</td><td>5</td><td>mm</td><td>Total cell width(W_H2+W_sep+W_O2)</td></tr></table>

<!-- PDF_PAGE: 12 -->

<div align="center">

Table 3. Cont.

</div>

<table border="1"><tr><td>Parameter</td><td>Symbol</td><td>Value</td><td>Unit</td><td>Description</td></tr><tr><td>Electrode Height</td><td>Helec</td><td>0.1</td><td>m</td><td>Height of the electrodes</td></tr><tr><td>Temperature</td><td>T</td><td>70</td><td>℃</td><td>Baseline operating temperature</td></tr><tr><td>Pressure</td><td>p_gas</td><td>1</td><td>atm</td><td>Baseline operating pressure</td></tr><tr><td>Bubble Diameter</td><td>d_bubble</td><td>50</td><td>μm</td><td>Assumed constant bubble diameter</td></tr><tr><td>Inlet Velocity</td><td>v_in</td><td>0.1</td><td>m/s</td><td>Electrolyte inlet velocity</td></tr><tr><td>Dispersion Factor(H2)</td><td>K_H2</td><td>5</td><td>m/s</td><td>H2bubble dispersion coefficient</td></tr><tr><td>Dispersion Factor(O2)</td><td>K_O2</td><td>10</td><td>m/s</td><td>O2bubble dispersion coefficient</td></tr><tr><td>Exchange Current(HER)</td><td>i0_ref_H2</td><td>100</td><td>A/m2</td><td>Reference exchange current density for HER</td></tr><tr><td>Exchange Current(OER)</td><td>i0_ref_O2</td><td>1</td><td>A/m2</td><td>Reference exchange current density for OER</td></tr><tr><td>Electrolyte Concentration</td><td>c_KOH</td><td>6</td><td>M</td><td>KOH molarity</td></tr><tr><td>Diaphragm Porosity</td><td>eps_sep</td><td>0.3</td><td>-</td><td>Separator porosity</td></tr></table>

## 3.2.3. Parametric Sweep for Dataset Creation

To generate the dataset for this specific cell, the parametric sweep was executed within the ranges detailed in Table 4, producing 625 data samples. The selected ranges are grounded in operational data from full-scale industrial AWE projects (e.g., China's Da'an and Narisong green hydrogen plants), encompassing both normal and boundary conditions encountered in practice. This ensures that the resulting dataset provides a reliable and industrially relevant basis for constructing health indicators and benchmarking the MLP model. While wider ranges could further evaluate the robustness of different machine learning algorithms, the current scope is sufficient to demonstrate the framework's validity under practical operating scenarios. Extensions to broader conditions are noted as a future research direction.

<div align="center">

Table 4. Parameter ranges for the CFD parametric sweep in the case study.

</div>

<table border="1"><tr><td>Parameter</td><td>Range</td><td>Step Size</td><td>Unit</td></tr><tr><td>Cell Voltage</td><td>1.19-1.23</td><td>0.01</td><td>V</td></tr><tr><td>Temperature</td><td>66-74</td><td>2</td><td>℃</td></tr><tr><td>Pressure</td><td>0.88-1.00</td><td>0.03</td><td>Atm</td></tr><tr><td>KOH</td><td>5.6-6.4</td><td>0.2</td><td>M</td></tr><tr><td>Concentration</td><td></td><td></td><td></td></tr></table>

## 3.3. ML Model Configuration

The dataset for this study, comprising 625 labeled samples generated from the validated CFD model, was used for training and benchmarking the machine learning classifiers. All eight designated health indicators served as the input features. Prior to model training, these features were normalized using min-max scaling to eliminate the influence of differing physical units and scales. The output label was the discrete health state (A, B, C, or D), corresponding to the four predefined categories of system health.

The dataset exhibits a non-uniform distribution across health states, with 294 samples in state A,199 in state B,105 in state C,and 27 in state D. This imbalance reflects realistic AWE operating conditions, where severe fault states occur far less frequently than nominal or mildly degraded states. Given the low-dimensional and physics-constrained nature of the input feature space, the dataset size is sufficient for training compact machine learning models with controlled complexity.

Three distinct machine learning algorithms were implemented and configured to perform this multiclass classification task, with their key hyperparameters carefully selected to balance model capacity and generalization performance.

<!-- PDF_PAGE: 13 -->

The polynomial regression (PR) model was employed as a transparent and interpretable nonlinear baseline to assess the capability and limitations of low-complexity parametric models in representing coupled degradation-related behavior in AWE systems. The model's complexity was controlled by the polynomial degree, which was systematically varied from 2 to 6 during evaluation to identify an appropriate trade-off between model expressiveness and overfitting. By including PR in the benchmarking set, the study provides a reference for understanding the performance gains achieved by higher-capacity models when handling strongly coupled, physics-informed health indicators.

For the SVM classifier, a comprehensive kernel evaluation was conducted. The linear, polynomial, sigmoid, and radial basis function (RBF) kernels were tested to determine the most suitable mapping for the classification boundaries. The penalty parameter C, which controls the tolerance for misclassified samples, was tuned across a range of 1 to 7 to optimize the margin-error trade-off.

The MLP model was designed to capture the nonlinear relationships among the physics-informed health indicators while maintaining a compact architecture suitable for the available dataset size. The network consisted of 10 hidden layers with 8 neurons per layer, a configuration selected based on preliminary exploratory testing to balance model expressiveness and generalization performance. The Rectified Linear Unit (ReLU) activation function was employed in all hidden layers to mitigate vanishing gradient effects and accelerate convergence. Model training was performed for 500 epochs using the Adam optimizer. To reduce overfitting, L2 regularization was applied, with the regularization coefficient $ \alpha $ tuned via grid search on a validation set.

All models were trained, validated, and tested using an identical data splitting protocol to ensure a fair comparison. Their performance was rigorously evaluated based on classification accuracy and a detailed analysis of the confusion matrix, as discussed in Section 4.

## 4. Results and Discussion

## 4.1. Validation of the Physics-Informed Dataset

The reliability of the proposed hybrid monitoring framework is fundamentally predicated on the fidelity of the underlying physics-based model and the physical consistency of the generated HIs. This section presents a two-tier validation strategy: first, the accuracy of the multiphysics CFD model is established through direct comparison with experimental measurements; second, the degradation-relevance and internal consistency of the HIs derived from the validated CFD model are systematically examined.

## 4.1.1. CFD Model Validation Against Experimental Measurements

The predictive capability of the 2D multiphysics CFD model was first verified against experimental data obtained from a laboratory-scale AWE test rig. Experiments were conducted within the parameter ranges defined in Table 4. For each operating condition, the electrolyzer was operated until steady-state behavior was achieved, followed by continuous operation for a duration of 2 h to collect stable performance data. Recorded current signals were time-averaged, with transient disturbances filtered out.

As shown in Figure 8, the CFD-predicted current accurately reproduces the nonlinear dependence on cell voltage and operating temperature observed in the experiments. This current-voltage behavior represents an integrated response of electrochemical kinetics, ohmic losses, heat transfer, and gas-liquid mass transport, and is therefore a robust and practically accessible metric for model validation in operating AWEs. The quantitative comparison yields a mean relative error of 2.41% between the CFD results and experimental measurements, with a maximum deviation below 6.2%.

<!-- PDF_PAGE: 14 -->


![figure_009.png](images/figure_009.png)



<div align="center">

Figure 8. Comparison of CFD-predicted and experimental current.

</div>

It should be noted that, due to the limited accessibility of internal measurements in operating electrolyzers, additional validation metrics such as local gas volume fraction, bubble size distribution, or spatial temperature fields could not be directly obtained without intrusive instrumentation. Accordingly, the present validation focuses on global steady-state electro-thermal performance, which is most relevant to the intended role of the CFD model as a physics-informed data generator for health indicator construction. Within this defined operational envelope, the close agreement observed confirms that the CFD model provides a physically consistent digital representation of the AWE's steady-state behavior.

## 4.1.2. Physical Consistency and Degradation-Relevance of the Generated HIs

Leveraging the validated CFD model, a comprehensive dataset of 625 samples was generated through the parametric sweep detailed in Section 3.2.3. This dataset provides a complete set of eight HIs for each simulated operating point, which are automatically labeled with a health state (A-D) based on the threshold rules in Table 2.

The physical plausibility of this dataset was critically examined by verifying the intrinsic, cause-effect relationships among the HIs, as dictated by fundamental electrochemistry and multiphase flow principles. For instance, analysis of data subsets with fixed voltage, temperature, and pressure confirmed that an increase in electrolyte pH (i.e., higher KOH concentration) leads to a corresponding increase in current density and Coulombic efficiency, while bubble velocity and relative power load decrease. This trend aligns perfectly with theoretical expectations: a higher concentration of $ \mathrm{O H}^{-} $ ions enhances ionic conductivity and electrochemical reaction kinetics, thereby improving efficiency and reducing the gas evolution overpotential at a constant cell voltage. The consistent manifestation of such physico-chemical correlations across the entire dataset confirms that the CFD model operates as a faithful physics-informed data generator.

Furthermore, the operational envelope covered by the dataset—including temperatures from 66 $ ^{\circ} \mathrm{C} $ to 74 $ ^{\circ} \mathrm{C} $ and pressures from 0.88 to 1.00 atm—effectively encompasses the precursor states of common faults such as mild overheating and under-pressure conditions. This demonstrates the model's capability to simulate degradation-relevant operational scenarios, which is crucial for training a monitoring system aimed at early fault detection. While the steady-state CFD model cannot simulate catastrophic, transient fault events (e.g., explosive gas mixing), its strength lies in generating a physics-consistent knowledge base that captures the progressive shifts in operational parameters indicative of incipient degradation. Figure 9 visually exemplifies one such key HI, showing the spatial distribution

<!-- PDF_PAGE: 15 -->

of bubble velocity magnitude within the electrolyzer channel under a specific operating condition, a parameter directly linked to gas crossover risk and efficiency loss.


![figure_010.png](images/figure_010.png)



<div align="center">

Figure 9. Contour of bubble velocity magnitude from CFD simulation.

</div>

## 4.2. Performance Benchmarking of Intelligent Monitoring Algorithms

The core task of the intelligent monitoring agent is to perform rapid, accurate health state classification based on a subset of measurable inputs. Three candidate ML models-Polynomial Regression, SVM, and MLP-were rigorously benchmarked to identify the optimal surrogate for real-time inference.

## 4.2.1. Polynomial Regression: An Interpretable Baseline

Polynomial regression served as an interpretable baseline model. Hyperparameter tuning focused on the polynomial degree (Figure 10a). The optimal accuracy of 85.94% was achieved with a 4th-degree polynomial. While this model captured the primary non-linear trends, its performance plateaued, reflecting a limited capacity to model the complex, high-dimensional decision boundaries between health states. The confusion matrix (Figure 10b) reveals a systematic bias towards underestimation (predicting a worse state than actual), leading to a high rate of false alarms. This conservative bias, though undesirable for operational efficiency, stems from the model's simplicity and highlights the need for more sophisticated algorithms to balance sensitivity and specificity in industrial monitoring.


![figure_011.png](images/figure_011.png)



<div align="center">

(a)

</div>


![figure_012.png](images/figure_012.png)



<div align="center">

(b)

</div>

<div align="center">

Figure 10. (a) Model accuracy vs. polynomial degree; (b) Confusion matrix for the optimal polynomial regression model (Degree = 4).

</div>

<!-- PDF_PAGE: 16 -->

## 4.2.2. SVM: Kernel Selection and Limitations

The SVM was evaluated with various kernel functions (Figure 11a). The RBF kernel yielded the best performance (78.13%) as it can create complex, non-linear boundaries. Further tuning of the penalty parameter C (Figure 11b) did not yield significant improvement, with optimal accuracy peaking at 76.22% for C=2. The final confusion matrix (Figure 11c) shows that the SVM struggled with distinguishing between adjacent health classes (e.g., A vs. B, B vs. C), particularly in regions where the HI thresholds defined in Table 2 create subtle, multi-parametric boundaries. This suggests that while SVM is powerful for binary classification, its effectiveness for multi-class problems with interdependent, continuous-valued HIs is limited without extensive feature engineering or a much larger dataset.


![figure_013.png](images/figure_013.png)



<div align="center">

(a)

</div>


![figure_014.png](images/figure_014.png)



<div align="center">

(b)

</div>


![figure_015.png](images/figure_015.png)



<div align="center">

(c)

</div>

<div align="center">

Figure 11. (a) Accuracy of SVM with different kernel functions; (b) Accuracy vs. penalty parameter C for the RBF kernel; (c) Confusion matrix for the optimized SVM model (RBF kernel, C=2).

</div>

## 4.2.3. MLP: A High-Performance Intelligent Agent

Among the evaluated models, the MLP, a feedforward artificial neural network, demonstrated the best overall performance for this task. Tuning the L2 regularization hyperparameter $ \alpha $ was crucial to prevent overfitting and ensure generalizability (Figure 12a). The best-performing MLP configuration $ (\alpha=0.01) $ achieved a peak classification accuracy of 90.43%.


![figure_016.png](images/figure_016.png)



<div align="center">

(a)

</div>


![figure_017.png](images/figure_017.png)



<div align="center">

(b)

</div>

<div align="center">

Figure 12. (a) MLP model accuracy vs. L2 regularization strength $ (\alpha); $ (b) Confusion matrix for the optimized MLP model $ (\alpha=0.01). $

</div>

<!-- PDF_PAGE: 17 -->

The corresponding confusion matrix (Figure 12b) indicates strong performance across all health states. It is observed that the majority of misclassifications occur between neighboring health categories, which reflects the gradual and continuous nature of AWE performance degradation rather than sharply separated fault boundaries. Such behavior is consistent with the underlying physical degradation mechanisms.

In practical condition-monitoring applications, these localized misclassifications are acceptable when combined with temporal trend analysis and conservative decision thresholds, as they reduce the likelihood of overlooking severe fault conditions while supporting early-stage degradation detection. The MLP's key strength lies in its ability to learn hierarchical, non-linear feature representations from the eight HIs, effectively approximating the complex mapping from operational parameters to the integrated health state defined by the proposed semi-quantitative evaluation framework.

In addition to overall classification accuracy, class-wise precision, recall, and F1-score were evaluated to provide a more comprehensive assessment of the monitoring algorithms, particularly for fault-related health states (C and D), which are critical in safety-sensitive AWE operation. Although the differences in overall accuracy among the models are moderate, the class-wise metrics reveal notable improvements in detecting fault conditions.

## 4.2.4. Class-Wise Performance Metrics and Safety Implications

Precision reflects the reliability of fault alarms by quantifying the proportion of correctly identified fault states among all predicted fault instances, while recall measures the model's ability to detect actual degradation or fault conditions. The F1-score provides a balanced metric that accounts for both false positives and false negatives.

As shown in Table 5, fault-related classes (C and D) exhibit lower recall than healthy states in general, highlighting the challenge of correctly identifying degraded conditions. Among the evaluated methods, the MLP demonstrates superior class-wise F1-scores for states C (0.814) and D (0.824), indicating a favorable balance between early fault detection and false-alarm avoidance. Notably, the higher recall for D class (0.875) compared to SVM (0.571) reduces the likelihood of false negatives, which pose the greatest safety risk in real-time AWE operation.

<div align="center">

Table 5. Performance comparison of different machine learning models under different health states.

</div>

<table border="1"><tr><td>Model</td><td>Health State</td><td>Precision</td><td>Recall</td><td>F1-Score</td></tr><tr><td rowspan="4">Polynomial Regression</td><td>A</td><td>1.000</td><td>0.366</td><td>0.536</td></tr><tr><td>B</td><td>0.392</td><td>0.604</td><td>0.475</td></tr><tr><td>C</td><td>0.441</td><td>0.536</td><td>0.484</td></tr><tr><td>D</td><td>0.435</td><td>1.000</td><td>0.606</td></tr><tr><td rowspan="4">SVM</td><td>A</td><td>0.847</td><td>0.942</td><td>0.884</td></tr><tr><td>B</td><td>0.750</td><td>0.750</td><td>0.750</td></tr><tr><td>C</td><td>0.739</td><td>0.607</td><td>0.667</td></tr><tr><td>D</td><td>0.667</td><td>0.571</td><td>0.615</td></tr><tr><td rowspan="4">MLP</td><td>A</td><td>0.975</td><td>0.952</td><td>0.963</td></tr><tr><td>B</td><td>0.836</td><td>0.968</td><td>0.897</td></tr><tr><td>C</td><td>0.960</td><td>0.706</td><td>0.814</td></tr><tr><td>D</td><td>0.778</td><td>0.875</td><td>0.824</td></tr></table>

From an operational perspective, minimizing false negatives is essential, as misclassifying degraded or unsafe conditions as healthy could lead to hazardous scenarios. The MLP's enhanced recall for fault-related states, combined with temporal trend analysis and conservative alarm thresholds, suggests improved robustness for real-time condition monitoring in safety-critical applications.

<!-- PDF_PAGE: 18 -->

## 4.2.5. Feature Importance Analysis Using SHAP

The global SHAP analysis of the MLP model (Figure 13) highlights KOH concentration and bubble velocity as the most influential health indicators, followed by pressure, temperature, efficiency, and load. The SHAP summary plot shows that variations in KOH concentration and bubble velocity strongly affect the predicted health state, indicating their high sensitivity to system changes. Pressure and temperature also contribute moderately, while efficiency and load have minor impact. These results provide insight into the model's decision process and justify the selection of these indicators for effective health state classification.


![figure_018.png](images/figure_018.png)



<div align="center">

Figure 13. Global SHAP analysis of the MLP model showing the contribution of each health indicator to health state classification.

</div>

## 4.3. Computational Efficiency and Practical Deployment Considerations

A critical consideration for real-time intelligent sensing is the trade-off between accuracy and computational latency. The training times for the final models were recorded: Polynomial Regression (9.91 ms), SVM (1.66 ms), and MLP (53.73 ms). While the MLP required the longest training time-a one-time offline cost-its inference time for a new data point is orders of magnitude faster (typically < 1 ms on modern hardware), making it perfectly suitable for real-time monitoring. Figure 14 synthesizes the accuracy-computational cost landscape. The MLP, occupying the high-accuracy region, is unequivocally the most suitable candidate for constructing the core intelligent monitoring agent. Its higher computational cost is justified by the paramount need for reliability in safety-critical applications like AWE operation. The model effectively translates the high-fidelity but slow physicsbased understanding (CFD) into a fast, deployable software sensor for health state.


![figure_019.png](images/figure_019.png)



<div align="center">

Figure 14. Comparative analysis of the three ML models in terms of classification ac-curacy and computational training time.

</div>

<!-- PDF_PAGE: 19 -->

## 5. Conclusions

This study developed and validated a hybrid physics-informed ML framework for intelligent condition monitoring of AWEs, addressing challenges related to operational reliability. The work makes distinct contributions aligned with intelligent sensing and prognostics for complex industrial systems:

- Establishment of a Validated Physics-Based Foundation: A high-fidelity 2D multiphysics CFD model was developed and experimentally validated, serving as a credible "digital testbed." This ensures that the generated dataset accurately captures key interactions within an AWE, providing a physically consistent knowledge base for training data-driven models.

- Physics-Informed Data Generation for AI Training: The CFD model generated a comprehensive labeled dataset reflecting the electrochemical-thermal-fluid interactions of an AWE. This approach addresses the scarcity of real-world fault data, providing a systematic basis for constructing health indicators and developing data-driven monitoring agents.

- Development of an Accurate Intelligent Monitoring Agent: Using the physics-informed dataset, an MLP model was identified as the optimal surrogate, achieving 90.43% accuracy in health state classification. This model operationalizes the hybrid framework, acting as a fast and interpretable software sensor that infers overall system health from accessible measurements.

The resulting methodology demonstrates how incorporating domain-specific physics enhances the interpretability and reliability of data-driven monitoring, offering a foundation for predictive maintenance that can improve safety, optimize maintenance schedules, and support more efficient green hydrogen production.

The current study is based on steady-state CFD simulations, and therefore the applicability of the framework to transient or highly dynamic operating scenarios, such as fluctuating renewable power inputs, has not yet been fully assessed. Future work will extend the approach to dynamic conditions using temporal feature analysis and sequence-based models (e.g., LSTM), conduct experimental validation of the HI system and MLP model on a physical AWE test rig, and explore integration with prognostic algorithms for RUL estimation. The incorporation of explainable AI techniques is also planned to enhance trust and facilitate adoption in practical industrial applications.

Overall, this work provides a structured and physically informed methodology for intelligent condition monitoring of AWEs, establishing a reliable framework for future extensions toward dynamic and real-world operating scenarios.

Author Contributions: Conceptualization, J.L. and Y.D.; methodology, Z.W. (Zhiying Wang); software, T.M.; validation, X.C., Z.W. (Zihao Wang) and C.H.; formal analysis, X.C.; investigation, Z.W. (Zihao Wang); resources, C.H.; data curation, T.M.; writing—original draft preparation, J.L.; writing—review and editing, Y.D. and Z.W. (Zhiying Wang); visualization, X.C.; supervision, Y.D.; project administration, Y.D.; funding acquisition, Y.D. All authors have read and agreed to the published version of the manuscript.

Funding: This research was funded by the National Key Research and Development Program of China (2021YFB4000505).

Institutional Review Board Statement: Not applicable.

Informed Consent Statement: Not applicable.

Data Availability Statement: The authors confirm that the data underlying the results presented in this study, are available from the corresponding author upon reasonable request.

<!-- PDF_PAGE: 20 -->

Conflicts of Interest: Jie Liu, Zhiying Wang, Tingting Ma, Xinyue Chen, and Zihao Wang are employees of Xinjiang Chemical Engineering Design & Research Institute Co., Ltd., which may be perceived as a potential conflict of interest. The remaining authors declare no commercial or financial relationships that could be construed as a potential conflict of interest.

## Abbreviations

The following abbreviations are used in this manuscript:

<table border="1"><tr><td>AWE</td><td>Alkaline Water Electrolyzer</td></tr><tr><td>HIs</td><td>Health Indicators</td></tr><tr><td>CFD</td><td>Computational Fluid Dynamics</td></tr><tr><td>ML</td><td>Machine Learning</td></tr><tr><td>MLP</td><td>Multilayer Perceptron</td></tr><tr><td>SVM</td><td>Support Vector Machine</td></tr><tr><td>PHM</td><td>Prognostics and Health Management</td></tr><tr><td>CBM</td><td>Condition-Based Maintenance</td></tr><tr><td>DT</td><td>Digital Twin</td></tr><tr><td>RES</td><td>Renewable Energy Source(s)</td></tr><tr><td>HER</td><td>Hydrogen Evolution Reaction</td></tr><tr><td>OER</td><td>Oxygen Evolution Reaction</td></tr><tr><td>RBF</td><td>Radial Basis Function</td></tr><tr><td>SHAP</td><td>SHapley Additive exPlanations</td></tr></table>

SHAP SHapley Additive exPlanations

## References

1. Mingolla, S.; Gabrielli, P.; Manzotti, A.; Robson, M.J.; Rouwenhorst, K.; Ciucci, F.; Sansavini, G.; Klemun, M.M.; Lu, Z. Effects of emissions caps on the costs and feasibility of low-carbon hydrogen in the European ammonia industry. Nat. Commun. 2024, 15, 3753. [CrossRef]

2. Fan, G.; Zhang, H.; Sun, B.; Pan, F. Economic and environmental competitiveness of multiple hydrogen production pathways in China. Nat. Commun. 2025, 16, 4284. [CrossRef]

3. Yavari, A.; Harrison, C.J.; Gorji, S.A.; Shafiei, M. Hydrogen 4.0: A Cyber-Physical System for Renewable Hydrogen Energy Plants. Sensors 2024, 24, 3239. [CrossRef]

4. Tuysuz, H. Alkaline Water Electrolysis for Green Hydrogen Production. Acc. Chem. Res. 2024, 57, 558-567. [CrossRef]

5. Sebbahi, S.; Assila, A.; Alaoui Belghiti, A.; Laasri, S.; Kaya, S.; Hlil, E.K.; Rachidi, S.; Hajjaji, A. A comprehensive review of recent advances in alkaline water electrolysis for hydrogen production. Int. J. Hydrogen Energy 2024, 82, 583-599. [CrossRef]

6. Emam, A.S.; Hamdan, M.O.; Abu-Nabah, B.A.; Elnajjar, E. A review on recent trends, challenges, and innovations in alkaline water electrolysis. Int. J. Hydrogen Energy 2024, 64, 599-625. [CrossRef]

7. Kwon, J.; Choi, S.; Park, C.; Han, H.; Song, T. Critical challenges and opportunities for the commercialization of alkaline electrolysis: High current density, stability, and safety. Mater. Chem. Front. 2024, 8, 41-81. [CrossRef]

8. Cheng, H.; Xia, Y.; Wei, W.; Zhou, Y.; Zhao, B.; Zhang, L. Safety and efficiency problems of hydrogen production from alkaline water electrolyzers driven by renewable energy sources. Int. J. Hydrogen Energy 2024, 54, 700-712. [CrossRef]

9. Lee, H.; Gu, J.; Lee, B.; Cho, H.-S.; Lim, H. Prognostics and health management of alkaline water electrolyzer: Techno-economic analysis considering replacement moment. Energy AI 2023, 13, 100251. [CrossRef]

10. Hu, S.; Chen, H.; Mao, X.; Tian, Z.; Fu, H.; Chen, D.; Xu, X. Analysis of the safe operating boundaries and approaches to expansion in alkaline water electrolysis systems. Int. J. Hydrogen Energy 2025, 191, 152310. [CrossRef]

11. Diversi, R.; Speciale, N. A Multidimensional Health Indicator Based on Autoregressive Power Spectral Density for Machine Condition Monitoring. Sensors 2024, 24, 4782. [CrossRef] [PubMed]

12. Bublil, T.; Cohen, R.; Kenett, R.S.; Bortman, J. Machine Health Indicators and Digital Twins. Sensors 2025, 25, 2246. [CrossRef]

13. Dittmar, F.; Agarwal, H.; Tübke, J. Prognostics and health management (PHM) of proton exchange membrane water electrolyzers: A review-based guideline. Int. J. Hydrogen Energy 2025, 106, 806-824. [CrossRef]

14. Kenett, R.S. Engineering, Emulators, Digital Twins, and Performance Engineering. Electronics 2024, 13, 1829. [CrossRef]

15. Wu, Y.; Sicard, B.; Gadsden, S.A. Physics-informed machine learning: A comprehensive review on applications in anomaly detection and condition monitoring. Expert Syst. Appl. 2024, 255, 124678. [CrossRef]

<!-- PDF_PAGE: 21 -->

16. Onyelowe, K.C.; Kamchoom, V.; Hanandeh, S.; Anandha Kumar, S.; Zabala Vizuete, R.F.; Santillán Murillo, R.O.; Zurita Polo, S.M.; Torres Castillo, R.M.; Ebid, A.M.; Awoyera, P.; et al. Physics-informed modeling of splitting tensile strength of recycled aggregate concrete using advanced machine learning. Sci. Rep. 2025, 15, 7135. [CrossRef]

17. Kapusuzoglu, B.; Mahadevan, S. Information fusion and machine learning for sensitivity analysis using physics knowledge and experimental data. Reliab. Eng. Syst. Saf. 2021, 214, 107712. [CrossRef]

18. Daoudi, C.; Bounahmidi, T. Overview of alkaline water electrolysis modeling. Int. J. Hydrogen Energy 2024, 49, 646-667. [CrossRef]

19. Rodriguez, J.; Amores, E. CFD Modeling and Experimental Validation of an Alkaline Water Electrolysis Cell for Hydrogen Production. Processes 2020, 8, 1634. [CrossRef]

20. Bai, J.; Guan, X.; Yang, N. Three-dimensional CFD simulation of alkaline electrolyzers: Flow pattern and electric field. Chem. Eng. J. 2025, 515, 163908. [CrossRef]

21. Zarghami, A.; Deen, N.G.; Vreman, A.W. CFD modeling of multiphase flow in an alkaline water electrolyzer. Chem. Eng. Sci. 2020, 227, 115926. [CrossRef]

22. Kanemoto, R.; Araki, T.; Misumi, R.; Mitsushima, S. Numerical modeling of two-phase flow considering multiple bubble sizes in an alkaline water electrolyzer. Chem. Eng. Sci. 2025, 304, 120986. [CrossRef]

23. Jacobsen, A.N.; Mahravan, E.; Kragh-Schwarz, M.V.; Catalano, J.; Fooroghi, P. Multiphysics simulations of alkaline water electrolyzer cells—A sensitivity study on the effect of two-phase flow modeling. Electrochim. Acta 2025, 541, 147148. [CrossRef]

24. Shams, M.H.; Niaz, H.; Na, J.; Anvari-Moghaddam, A.; Liu, J.J. Machine learning-based utilization of renewable power curtailments under uncertainty by planning of hydrogen systems and battery storages. J. Energy Storage 2021, 41, 103010. [CrossRef]

25. Cheng, G.; Luo, E.; Zhao, Y.; Yang, Y.; Chen, B.; Cai, Y.; Wang, X.; Dong, C. Analysis and prediction of green hydrogen production potential by photovoltaic-powered water electrolysis using machine learning in China. Energy 2023, 284, 129302. [CrossRef]

26. Babay, M.-A.; Adar, M.; Chebak, A.; Mabrouki, M. Dynamics of Gas Generation in Porous Electrode Alkaline Electrolysis Cells: An Investigation and Optimization Using Machine Learning. Energies 2023, 16, 5365. [CrossRef]

27. Jensen, V.H.; Moretti, E.R.; Busk, J.; Christiansen, E.H.; Skov, S.M.; Jacobsen, E.; Kraglund, M.R.; Bhowmik, A.; Kiebach, R. Machine learning guided development of high-performance nano-structured nickel electrodes for alkaline water electrolysis. Appl. Mater. Today 2023, 35, 102005. [CrossRef]

28. Sirat, A.; Ahmad, S.; Ahmad, I.; Ahmed, N.; Ahsan, M. Integrative CFD and AI/ML-based modeling for enhanced alkaline water electrolysis cell performance for hydrogen production. Int. J. Hydrogen Energy 2024, 83, 1120-1131. [CrossRef]

29. Lee, C.-Y.; Li, S.-C.; Chen, C.-H.; Huang, Y.-T.; Wang, Y.-S. Real-Time Microscopic Monitoring of Flow, Voltage and Current in the Proton Exchange Membrane Water Electrolyzer. Sensors 2018, 18, 867. [CrossRef]

30. Zhang, Q.; Xu, W.; Xie, L.; Su, H. Dynamic fault detection and diagnosis for alkaline water electrolyzer with variational Bayesian Sparse principal component analysis. J. Process Control 2024, 135, 103173. [CrossRef]

31. Zhang, Q.; Lu, S.; Xie, L.; Xu, W.; Su, H. Dynamic fault detection and diagnosis of industrial alkaline water electrolyzer process with variational Bayesian dictionary learning. Int. J. Hydrogen Energy 2024, 71, 1492-1506. [CrossRef]

32. Cheng, H.; Xia, Y.; Wei, W. Self-Optimization Control for Alkaline Water Electrolyzers Considering Electrolyzer Temperature Variations. IEEE Trans. Ind. Electron. 2025, 72, 2700-2711. [CrossRef]

33. Ursua, A.; Marroyo, L.; Gubia, E.; Gandia, L.M.; Diéguez, P.M.; Sanchis, P. Influence of the power supply on the energy efficiency of an alkaline water electrolyser. Int. J. Hydrogen Energy 2009, 34, 3221-3233. [CrossRef]

34. Ursua, A.; Sanchis, P. Static-dynamic modelling of the electrical behaviour of a commercial advanced alkaline water electrolyser. Int. J. Hydrogen Energy 2012, 37, 18598-18614. [CrossRef]

35. Abdin, Z.; Webb, C.J.; Gray, E.M. Modelling and simulation of an alkaline electrolyser cell. Energy 2017, 138, 316-331. [CrossRef]

36. Mohamed Mohsin, H.; Zhuo, Y.; Shen, Y. Eulerian-Eulerian-VOF multifluid modelling of liquid-gas reacting flow for hydrogen generation in an alkaline water electrolyser. Fuel 2024, 373, 132164. [CrossRef]

37. Haug, P.; Kreitz, B.; Koj, M.; Turek, T. Process modelling of an alkaline water electrolyzer. Int. J. Hydrogen Energy 2017, 42, 15689-15707. [CrossRef]

38. Lei, Y.; Zhao, J.; Wang, Y.; Xue, C.; Gao, L. Flexible Sensing for Precise Lithium-Ion Battery Swelling Monitoring: Mechanisms, Integration Strategies, and Outlook. Sensors 2025, 25, 7677. [CrossRef]

Disclaimer/Publisher's Note: The statements, opinions and data contained in all publications are solely those of the individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to people or property resulting from any ideas, methods, instructions or products referred to in the content.