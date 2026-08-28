---
source: "extraction_papers/10.1371_journal.pone.0348497.pdf"
title: "10.1371_journal.pone.0348497"
page_count: 21
converted_at: "2026-08-27T22:50:10Z"
---

<!-- PDF_PAGE: 1 -->





RESEARCH ARTICLE


![figure_001.png](images/figure_001.png)



<div align="center">

# Early fault detection in gearboxes via dynamic principal component analysis-driven multivariate statistical process control

</div>


![figure_002.png](images/figure_002.png)



## OPEN ACCESS

Citation: Pérez-Torres A, Navarrete-Campos J, Fernandez-Lopez R, Figueroa-Zuñiga J, Barcelo-Cerdá S (2026) Early fault detection in gearboxes via dynamic principal component analysis-driven multivariate statistical process control. PLoS One 21(5): e0348497. https:// doi.org/10.1371/journal.pone.0348497

Editor: Arne Johannssen, University of Hamburg: Universitat Hamburg, GERMANY

Received: November 4, 2025

Accepted: April 16, 2026

Published: May 18, 2026

Antonio Pérez-Torres $ ^{1,2} $ $ ^{*} $ , Jean Navarrete-Campos $ ^{3} $ $ ^{*} $ , Reinier Fernández-López $ ^{4} $ $ ^{*} $ Jorge Figueroa-Zúñiga $ ^{3} $ $ ^{*} $ , Susana Barceló-Cerdá $ ^{1} $ $ ^{*} $

Copyright: 2026 Pérez-Torres et al. This is an open access article distributed under the terms of the Creative Commons Attribution License which permits unrestricted use, distribution and reproduction in any medium, provided the original author and source are credited.

1 Department of Applied Statistics and Operational Research, and Quality, Universitat Politècnica de València, València, Spain, 2 Grupo de Investigación y Desarrollo en Tecnologías Industriales (GIDTEC), Universidad Politécnica Salesiana, Cuenca, Ecuador, 3 Departamento de Estadística, Universidad de Concepción, Concepción, Chile, 4 Facultad de Ingeniería y Arquitectura, Universidad Central de Chile, La Serena, Chile

Data availability statement: The dataset is owned by Universidad Politécnica Salesiana (UPS), which funded the research project. The full dataset (415 GB) will also support further publications and is therefore not publicly available. However, a curated subset covering

These authors contributed equally to this work.

* jperezt@ups.edu.ec (AP-T); sbarcelo@eio.upv.es (SB-C)

## Abstract

Early detection of gearbox failure is essential due to their critical role in industrial operations. Therefore, effective condition monitoring techniques are required to identify incipient deviations in operational behaviour. Therefore, this study proposes a dynamic principal component analysis methodology, integrated within a multivariate statistical process control framework, to detect progressive failures in spur gearboxes from vibration signals. The signal is segmented into sub-windows and characterised using condition indicators in the time and frequency domains. Diagnosis is based on Hotelling's $ T^{2} $ statistic and the squared prediction error, which define statistical control limits to discriminate between normal and failure conditions. Empirical validation uses an experimental dataset covering combinations of load, speed, and failure severity. The results demonstrate high sensitivity to progressive degradation and accurate early-stage detection, supporting the multivariate statistical process control approach with dynamic principal component analysis as an effective tool for diagnosis and predictive maintenance in high-criticality industrial environments.

## 1 Introduction

Gearboxes are essential components in the mechanical power transmission of systems operating across various sectors, including aerospace, automotive, energy, manufacturing, mining, and rail transport, among others [1]. Despite their robust designs, gearboxes are subjected to demanding operating conditions that can lead to progressive failures. For example, wear, cracks, fractures, micropitting, misalignment, contact fatigue, and corrosion [2,3]. Therefore, early detection of these failures is

<!-- PDF_PAGE: 2 -->





Phase I (gearbox in a healthy state) and Phase II (low- and high-severity failures), together with the experimental plan and the R code used for data processing, is publicly available in the Figshare repository (DOI: https://doi.org/10.6084/m9.figshare.31274794). Access to the complete dataset may be granted upon reasonable request to the corresponding author or via the Grupo de Investigacion y Desarrollo en Tecnologias Industrial (GIDTEC; https://www.investigacion.ups.edu.ec/grupo/gidtec/).

Funding: Universidad Politécnica Salesiana funded this work through the research project "Modelamiento estadístico-matemático para la toma de decisiones en ciencia y tecnología", of the Grupo de Investigación y Desarrollo en Tecnologías Industriales (GIDTEC), approved under Resolution: 060-003-2026-04-16.

Competing interests: The authors declare that they have no competing interests. One of the authors is affiliated with Universidad Politecnica Salesiana, which provided funding for this research; however, the funder had no role in study design, data collection and analysis, decision to publish, or preparation of the manuscript.

crucial to prevent unplanned shutdowns and ensure the system's continued operational integrity [4,5].

Among the various condition monitoring (CM, understood as the continuous assessment of operating parameters to detect and diagnose failures) methodologies, vibration analysis stands out for its sensitivity in identifying characteristic patterns generated by mechanical failures, particularly in rotating machinery such as gearboxes [6,7]. Specifically, gearbox signals are often affected by noise and by variable operating conditions (speed-load), which drives the use of increasingly complex and high-dimensional diagnostic approaches [8,9].

However, CM in gearboxes has the drawback that failure signatures are often weak at incipient stages and are modulated by the operating regime (speed-load) and by the inherent dynamics of the transmission system, which can mask subtle changes in the signal. In practice, this leads to datasets with multiple simultaneous highly correlated indicators and variability induced by operating conditions, which increases the effective dimensionality of the problem and requires multivariate methods capable of separating nominal variation from deviations attributable to failure [6,7,10].

The vibration signal captures the system's dynamic signature, enabling the extraction of condition indicators (CIs, statistical parameters computed from the signal for feature extraction), which support data-driven diagnosis [11,12]. In addition, advances in data acquisition systems and in multivariate analysis techniques, in particular multivariate statistical process control (MSPC), have established them as practical tools for analysing high-dimensional data [10,13,14].

In this context, MSPC is particularly attractive because it enables the joint monitoring of multiple correlated variables, the establishment of statistical control limits under normal operating conditions (NOC), and the detection of multivariate deviations without requiring labelled failures. This approach is especially pertinent when indicators derived from vibration signals are used, since decisions based on a single variable can be unstable. In contrast, multivariate assessment improves the statistical traceability of changes and reduces ambiguities in the presence of noise [10,15,16].

It is worth noting that principal component analysis (PCA) is a widely used method for dimensionality reduction and for extracting relevant patterns of the system's operational behaviour [2,6,17,18]. However, conventional PCA assumes temporal independence among observations, limiting its applicability in systems with significant temporal dynamics. This limitation is overcome by dynamic PCA (DPCA), which incorporates time-lagged variables, capturing the correlation between variables and the temporal structure of the process [6,19]. This improvement is particularly beneficial in failure diagnosis for rotating machinery, where failures often develop progressively [20-22].

In particular, in segmented vibration signals, autocorrelation and memory effects arising from system dynamics can shift energy between components and residuals, altering the sensitivity of PCA-based schemes if temporal dependencies are ignored. Therefore, DPCA is relevant for gearbox monitoring, as it introduces a temporal

<!-- PDF_PAGE: 3 -->





embedding (lags) that allows the sequential structure to be modelled explicitly and thereby improves the detectability of incipient changes within an MSPC framework [6,12,20].

On the other hand, numerous studies have shown that using DPCA significantly improves sensitivity in failure detection for rotating systems, such as wind turbines, cutting tools, and bearings, especially when the temporal structure of the data is incorporated [12,23-25]. For example, Jin et al. [17] showed that an MSPC scheme based on DPCA achieves higher failure detection rates in bearings by explicitly modelling the inherent dynamics of vibration signals. Thus, within the MSPC context, the DPCA-based approach enables quantification of multivariate deviations within the principal subspace and in the model residuals. Statistical control limits are established to define the system's NOC, and these limits are compared with failure or anomaly scenarios using control charts. Implementing this methodology enables continuous, automated monitoring of critical system states, a vital aspect for maintaining operational reliability [2,7,15,17].

Therefore, this work aims to develop a condition monitoring scheme based on MSPC using DPCA to detect incipient failures in spur gearboxes. As the data source, vibration signals recorded under controlled laboratory conditions are used. The novelty of this work lies not only in integrating dynamic multivariate analysis with statistical control charts, but also in its application to spur gearboxes, for which no precedents have been reported in the literature. This contribution positions the study as a bridge between vibration-based engineering diagnosis and data-driven statistical process control methods, as discussed in [16,26].

Finally, the remainder of the article is organised as follows. Section 2 details the MSPC methodology based on DPCA, emphasising the separation between Phase I and Phase II and the cross-validation-based selection of lags and components. Section 3 describes the test rig and the data. Section 4 presents the empirical results, including the Phase I control limits, the analysis of detection delay across different severity levels in Phase II, and a discussion of why the SPE chart achieves earlier detection when the correlation structure breaks down. Finally, Section 5 summarises the main findings and outlines directions for future work.

## 2 Methodology

DPCA extends standard PCA to model industrial processes with temporal autocorrelation [27,28]. Unlike standard PCA, which assumes independence between consecutive observations, DPCA captures dynamic dependencies arising from transient states or memory effects, which are common in physical systems and industrial control environments [29,30]. A defining feature of DPCA is the explicit incorporation of time lags into the data matrix, which enables effective modelling of the sequential structure inherent to multivariate systems [31,32]. This capability is particularly valuable for monitoring mechanical processes, where gradual or smooth transitions contain relevant information about the evolution of the system's operating state [27,33]. Therefore, each observation is represented as a concatenation of the original series and its time-lagged versions:

$$
\mathbf {F} _ {t} = \left[ \mathbf {f} _ {t} ^ {\top} \quad \mathbf {f} _ {t - 1} ^ {\top} \quad \dots \quad \mathbf {f} _ {t - p} ^ {\top} \right] ^ {\top}, \quad \mathbf {F} _ {t} \in \mathbb {R} ^ {m (p + 1)},
$$

where $ \mathbf{f}_{t}\in \mathbb{R}^{m} $ is the vector of CIs at time t, p denotes the number of lags considered, and m is the number of variables. Stacking these lag-augmented observations by rows yields the DPCA data matrix [34]:

$$
\mathbf {X} _ {D} = \left[ \begin{array}{c} \mathbf {F} _ {1} ^ {\top} \\ \mathbf {F} _ {2} ^ {\top} \\ \vdots \\ \mathbf {F} _ {n} ^ {\top} \end{array} \right] \in \mathbb {R} ^ {n \times m (p + 1)},
$$

where n is the number of observations available after accounting for the lags, Takens' theorem [35] justifies reconstructing the state space of dynamical systems from time-lagged observations.

<!-- PDF_PAGE: 4 -->





The DPCA model is estimated via singular value decomposition (SVD) or the spectral decomposition of $ \mathbf{X}_{D}^{\top}\mathbf{X}_{D} $ [36] which leads to:

$$
\mathbf {T} = \mathbf {X} _ {D} \mathbf {P} _ {k}, \quad \mathbf {P} _ {k} = \left[ \mathbf {p} _ {1}, \dots , \mathbf {p} _ {k} \right],
$$

where $ \mathbf{P}_{k} $ contains the first $ k $ eigenvectors (loadings) and $ \mathbf{T}\in\mathbb{R}^{n\times k} $ are the corresponding scores.

Before fitting the model, the variables are centred and scaled using Phase I statistics, with $ \mu_{P_{0}} \in \mathbb{R}^{m} $ and $ \sigma_{P_{0}} \in \mathbb{R}^{m} $ denoting the vectors of means and standard deviations estimated from NOC data. That is, with the gearbox in a healthy state, denoted as $ P_{0} $ (see Table 1). Each observation is standardised as:

$$
\mathbf {f} _ {t} ^ {\prime} = \left(\mathbf {f} _ {t} - \boldsymbol {\mu} _ {P _ {0}}\right) \oslash \boldsymbol {\sigma} _ {P _ {0}},
$$

where $ \oslash $ denotes element-wise division.

In Phase II, new observations are normalised using these same frozen $ P_{0} $ parameters, ensuring consistency between phases and preventing information leakage.

The hyperparameters (k,p) are selected using a cross-validation (CV) procedure that minimises the Squared Prediction Error (SPE) while maintaining a stable in-control Average Run Length $ ( A R L_{0} ) $ [37-40]. This is defined as:

$$
\mathrm {s c o r e} = \mathrm {m e d i a n} \left(\frac {S P E _ {\mathrm {t e s t}}}{U C L _ {S P E}}\right),
$$

$$
\mathrm {R L} _ {r} = \left\{ \begin{array}{l l} \min \left\{t \in \{1, \dots , N _ {r} \}: S P E _ {r, t} > U C L _ {S P E} \right\}, & \text {i f the set is nonempty}, \\ N _ {r}, & \text {o t h e r w i s e}, \end{array} \right.
$$

$$
A R L _ {0} = \operatorname {m e d i a n} _ {r} \left(\mathrm {R L} _ {r}\right),
$$

$$
\mathrm {s c o r e} \leftarrow \mathrm {s c o r e} \cdot \left\{ \begin{array}{l l} 1 - \frac {\min \left(A R L _ {0}\right) - A R L _ {0}}{\min \left(A R L _ {0}\right)}, & \mathrm {i f} A R L _ {0} < \min \left(A R L _ {0}\right), \\ 1, & \mathrm {o t h e r w i s e}. \end{array} \right.
$$

where $ R L_{r} $ is the run length of run r (the first time instant or segment at which the SPE statistic crosses the upper control limit), $ N_{r} $ is the total number of segments in run r, and the score is a performance index.

<div align="center">

Table 1. Severity of pinion tooth-break failure.

</div>

<table border="1"><tr><td>Severity</td><td>Failure description</td><td>Tooth loss</td></tr><tr><td>$P_{0}$</td><td>Healthy condition</td><td>0.00%</td></tr><tr><td>$P_{1}$</td><td>Failure volume of 4.64 mm^{3</sup> on one tooth</td><td>1.30%</td></tr><tr><td>$P_{2}$</td><td>Failure volume of 14.29 mm^{3</sup> on one tooth</td><td>4.00%</td></tr><tr><td>$P_{3}$</td><td>Failure volume of 26.79 mm^{3</sup> on one tooth</td><td>7.50%</td></tr><tr><td>$P_{4}$</td><td>Failure volume of 40.36 mm^{3</sup> on one tooth</td><td>11.30%</td></tr><tr><td>$P_{5}$</td><td>Failure volume of 72.87 mm^{3</sup> on one tooth</td><td>20.40%</td></tr><tr><td>$P_{6}$</td><td>Failure volume of 109.30 mm^{3</sup> on one tooth</td><td>30.60%</td></tr><tr><td>$P_{7}$</td><td>Failure volume of 145.74 mm^{3</sup> on one tooth</td><td>40.80%</td></tr><tr><td>$P_{8}$</td><td>Failure volume of 250.75 mm^{3</sup> on one tooth</td><td>70.20%</td></tr><tr><td>$P_{9}$</td><td>Failure volume of 357.20 mm^{3</sup> on one tooth</td><td>100.00%</td></tr></table>

https://doi.org/10.1371/journal.pone.0348497.t001

<!-- PDF_PAGE: 5 -->





This scheme uses time-block partitions to prevent temporal leakage and estimates $ A R L_{0} $ under NOC via simulation or resampling of standardised sequences. In this way, the resulting model balances predictive capability with the stability required for statistical monitoring. As a reference, the classical variance-retention criterion is defined as:

$$
k = \min \left\{j \mid \frac {\sum_ {i = 1} ^ {j} \lambda_ {i}}{\sum_ {i = 1} ^ {a} \lambda_ {i}} \geq \gamma \right\},
$$

with a = m (p+1) and a threshold $ \gamma $ that in practice typically lies in the range 0.70-0.90 [23,41]. However, this threshold is replaced by a CV-based optimisation, providing a more robust selection of model complexity.

On the other hand, within the MSPC framework, the DPCA model operates in two complementary phases. In Phase I, NOC are established, $ P_{k} $ and the diagonal matrix $ \Lambda=\operatorname{diag}(\lambda_{1},\dots,\lambda_{k}) $ of retained eigenvalues are fixed, and the control limits at significance level $ \alpha $ are computed. In Phase II, new observations with possible failures are standardised using the NOC parameters, projected onto the frozen $ P_{k} $ , and the Hotelling $ T^{2} $ and SPE statistics are evaluated.

Hotelling's $ T^{2} $ statistic is defined as:

$$
T ^ {2} (t) = \mathbf {t} _ {t} ^ {\top} \Lambda^ {- 1} \mathbf {t} _ {t}
$$

where $ \mathbf{t}_{t} $ is the score vector at time t. The SPE is given by:

$$
S P E (t) = \left\| \mathbf {F} _ {t} - \hat {\mathbf {F}} _ {t} \right\| ^ {2} = \left\| \mathbf {F} _ {t} - \mathbf {P} _ {k} \mathbf {P} _ {k} ^ {\top} \mathbf {F} _ {t} \right\| ^ {2},
$$

where $ \mathbf{F}_{t} $ is the observation at time t and $ \hat{\mathbf{F}}_{t} $ is its projection onto the principal subspace. The first statistic evaluates the multivariate distance within the principal subspace, whereas the second quantifies the residual variance not explained by the model. Upper Control Limits (UCL) are defined for both statistics. For $ T^{2} $ , the UCL is obtained from the Snedecor F distribution with $ n_{0} $ effective Phase I observations (after accounting for p lags):

$$
U C L _ {T ^ {2}} = \frac {k \left(n _ {0} - 1\right)}{n _ {0} - k} F _ {1 - \alpha} \left(k, n _ {0} - k\right).
$$

In contrast, the UCL for SPE uses the Jackson-Mudholkar approximation [42]. To this end, the total number of variables $ a=m(p+1) $ after temporal expansion is considered, and moments of the residual eigenvalues, which reflect the variability not explained by the model, are computed as $ \theta_{i}=\sum_{j=k+1}^{a}\lambda_{j}^{i} $ for $ i=1,2,3 $ , with $ h_{0}=1-\frac{2\theta_{1}\theta_{3}}{3\theta_{2}^{2}} $ . Thus,

$$
U C L _ {S P E} = \theta_ {1} \left(1 + \frac {z _ {1 - \alpha} \sqrt {2 \theta_ {2}} h _ {0}}{\theta_ {1}} + \frac {\theta_ {2} h _ {0} \left(h _ {0} - 1\right)}{\theta_ {1} ^ {2}}\right) ^ {1 / h _ {0}}.
$$

These thresholds define safe operating regions and enable automatic alarm triggering in response to significant deviations, thereby enhancing the capability for effective real-time monitoring [7,15].

As part of the monitoring protocol, Phase I fits the DPCA model and selects (p,k) via block CV to minimise SPE subject to an in-control ARL $ _{0} $ constraint. The pair of limits $ \left( U C L_{T^{2}}, U C L_{S P E}\right) $ is computed at significance level $ \alpha $ and the set $ \left\{\mu_{P_{0}},\sigma_{P_{0}},\mathbf{P}_{k},\Lambda,U C L_{T^{2}},U C L_{S P E}\right\} $ is frozen. In Phase II, each new observation is standardised using the $ P_{0} $ values, dynamically embedded using the frozen p, projected onto the fixed subspace, and $ T^{2}(t) $ and SPE(t) are evaluated against their respective UCLs. For slow degradations, memory charts, Exponentially Weighted Moving Average (EWMA) or Cumulative Sum (CUSUM), are considered, applied to SPE or $ T^{2} $ , with parameters $ (\lambda,k,h) $ tuned via CV $ [37,38] $ .

<!-- PDF_PAGE: 6 -->





To detect gradual or low-magnitude degradations, memory charts are applied to the $ T^{2} $ or SPE statistics. For example, the EWMA chart updates its cumulative value as:

$$
Z _ {t} = \lambda S (t) + (1 - \lambda) Z _ {t - 1}, \quad 0 < \lambda \leq 1,
$$

where $ S ( t ) \in \{ T^{2} ( t ) , S P E ( t ) \} $ is the instantaneous statistic and $ \lambda $ controls the weight of the memory (smaller values increase sensitivity to slow changes). An alarm is triggered when $ Z_{t} $ exceeds its upper control limit $ U C L_{\mathrm{E W M A}}. $

Whereas the CUSUM chart accumulates successive deviations from the expected mean:

$$
C _ {t} = \max \left(0, C _ {t - 1} + S (t) - k\right),
$$

where k is the reference value and h is the decision threshold; an alarm is triggered when $ C_{t} > h $ . Both configurations $ (\lambda,k,h) $ are optimised via block CV in Phase I, ensuring an in-control $ ARL_{0} $ consistent with significance level $ \alpha $ . Operational details are summarised in Algorithms B2 and B3.

## Algorithm 1. Phase I: calibration and freezing.

Require: Dataset $ P_{0} $ ; grid $ \mathcal{P}\times\mathcal{K} $ for (p,k); significance level $ \alpha $ ; target $ ARL_{0} $ ; time-blocked CV scheme

1: Estimate $ \mu_{P_{0}},\sigma_{P_{0}} $ on $ P_{0} $ ; standardize $ P_{0} $ with these parameters

2: for all $ (p,k)\in\mathcal{P}\times\mathcal{K} $ do

3: Define time-blocked folds to avoid leakage

4: for all folds do

5: Fit DPCA on training blocks $ \Rightarrow $ $ P_{k},\Lambda $

6: Compute SPE on validation blocks

7: end for

8: $ SPE(p,k)\leftarrow $ average validation SPE across folds

9: Estimate $ ARL_{0}(p,k) $ under NOC via simulation/resampling at level $ \alpha $

10: end for

11: Select $ (p^{*},k^{*})=\operatorname{arg}\min\ SPE_{00F}(p,k) $ subject to $ ARL_{0}(p,k)\geq ARL_{0}^{\mathrm{target}} $

12: Refit DPCA on full standardized $ P_{0} $ with $ (p^{*},k^{*}) $ to obtain $ P_{k^{*}} $ and $ \Lambda $

13: Compute $ UCL_{T^{2}} $ and $ UCL_{SPE} $ at level $ \alpha $ using the effective sample size $ n_{0} $

14: Freeze and store $ \left\{\mu_{P_{0}},\sigma_{P_{0}},p^{*},P_{k^{*}},\Lambda,UCL_{T^{2}},UCL_{SPE}\right\} $

15: return Frozen parameter set for Phase II

## Algorithm 2. Phase II: monitoring workflow.

Require: Frozen $ \{\mu_{P_{0}},\sigma_{P_{0}},p^{*},\mathbf{P}_{k^{*}},\Lambda,UCL_{T^{2}},UCL_{SPE} \}$

1: (Warm-up) If $ t<p^{*} $ , skip evaluation or start at $ t=p^{*} $

2: $ \mathbf{f}_{t}\leftarrow(\mathbf{f}_{t}-\mu_{P_{0}})/\sigma_{P_{0}} $ $ \triangleright $ Standardize with $ P_{0} $ (no re-estimation)

3: $ \mathbf{F}_{t}\leftarrow[\mathbf{f}_{t}^{\top},\mathbf{f}_{t-1}^{\top},\dots,\mathbf{f}_{t-p^{*}}^{\top}]^{\top} $ $ \triangleright $ Dynamic embedding with frozen $ p^{*} $

4: $ \mathbf{t}_{t}\leftarrow\mathbf{P}_{k^{*}}^{\top}\mathbf{F}_{t} $ $ \triangleright $ Fixed projection with frozen loadings

5: $ T^{2}(t)\leftarrow\mathbf{t}_{t}^{\top}\Lambda^{-1}\mathbf{t}_{t} $

6: $ SPE(t)\leftarrow\|\mathbf{F}_{t}-\mathbf{P}_{k^{*}}\mathbf{P}_{k^{*}}^{\top}\mathbf{F}_{t}\|^{2} $

7: $ A_{T^{2}}\leftarrow $ True if $ T^{2}(t)>UCL_{T^{2}} $ else False

8: $ A_{SPE}\leftarrow $ True if $ SPE(t)>UCL_{SPE} $ else False

9: Optional memory charts: update EWMA/CUSUM on $ T^{2} $ and/or SPE for slow drifts

10: return $ \left(A_{T^{2}},A_{SPE}\right) $

Regarding the model evaluation metrics and the definition of detection delay, let $ t_{0} $ denote the start of the failure segment on the segment scale (see Section 3). For each control statistic $ S(t)\in\{T^{2}(t),SPE(t)\} $ , the detection delay is defined as the number of segments elapsed from failure onset to the first crossing of the upper control limit:

<!-- PDF_PAGE: 7 -->





$$
d _ {S} = \min \left\{t \geq t _ {0}: S (t) > U C L _ {S} \right\} - t _ {0},
$$

where $ d_{S} $ is measured in segments. In particular, $ d_{T^{2}} $ and dSPE denote the detection delays obtained with the $ T^{2} $ and SPE charts, respectively. We also report the medians and interquartile ranges (IQR) of these values, grouped by failure severity level, where $ \mathrm{IQR}(d_{S})=Q_{0.75}(d_{S})-Q_{0.25}(d_{S}) $ . In addition, we quantify three complementary metrics:

(i) $ A R L_{0} $ during Phase I,

(ii) the percentage of out-of-control observations (%OOC) for each statistic, and

(iii) monotonicity with failure severity via Spearman's rank correlation coefficient $ \hat{\rho}. $

These are estimated, along with confidence intervals, using bootstrap resampling. The %OOC quantifies the fraction of segments that exceed the UCL of a given statistic:

$$
\% \mathrm {O O C} _ {S} = 1 0 0 \times \frac {1}{N} \sum_ {t = 1} ^ {N} \mathbb {I} \left(S (t) > U C L _ {S}\right), \quad S \in \{T ^ {2}, S P E \},
$$

where N is the total number of segments evaluated and $ \mathbb{I}(\cdot) $ is the indicator function, which takes the value 1 when the statistic $ S(t) $ lies above the upper control limit and 0 otherwise. Consequently, this function acts as a counter that records the number of out-of-control segments. Under $ P_{0} $ , we expect $ \% OOC\approx100\alpha\% $ , whereas increases in Phase II reflect deviations from NOC.

It is worth noting that the use of the Snedecor F distribution to approximate the control limit for Hotelling's $ T^{2} $ statistic is grounded in classical MSPC developments. In particular, Montgomery [43] shows that under multivariate normality, independence between observations, and estimation of the covariance matrix in Phase I, the $ T^{2} $ statistic can be transformed to follow approximately an F distribution [30].

This approximation provides an operational reference for defining control limits in MSPC schemes. However, it has limitations when the stated assumptions are not strictly satisfied. For example, in scenarios with small sample sizes, pronounced serial dependence, or covariance matrices estimated from limited Phase I information, the $ T^{2} $ statistic may deviate from the F distribution, affecting the calibration of the control limit [22,44]. Therefore, biases may arise in the false-alarm rate (inflation or deflation of $ A R L_{0} $ ) and, in extreme contexts, sensitivity to incipient failures may be reduced.

This phenomenon has been documented in recent studies on monitoring vibration systems and dynamic processes, where dimensionality and temporal dependence influence the empirical distribution of control statistics [7,23]. To mitigate these limitations, our study uses a rigorous Phase I calibration procedure based on time-block CV and $ A R L_{0} $ simulation, which ensures that the $ U C L_{T^{2}} $ employed is empirically matched to the actual data structure under NOC. In this way, any potential deviation from the F distribution is absorbed into the experimental estimation of $ A R L_{0} $ ensuring a consistent false-alarm rate and stability of the monitoring system.

All of the above ensures that the model remains fixed during Phase II; new data are only projected and evaluated against the objective limits defined in Phase I [16,26]. The resulting DPCA-MSPC framework ensures statistical consistency between phases and provides a solid basis for the performance analysis discussed in Section 4.

Next, we detail the two-phase framework, following SPC and multivariate monitoring recommendations for dynamic systems [30,45,46]. This framework is depicted in the flowchart shown in Fig 1.

Phase I: Establishing the in-control model. In this stage, we follow a rigorous methodological sequence to ensure that the DPCA-MSPC model is built from data representative of the healthy state. The procedure is as follows:

<!-- PDF_PAGE: 8 -->






![figure_003.png](images/figure_003.png)



<div align="center">

Fig 1. Workflow of the proposed DPCA-MSPC scheme, distinguishing Phase I (calibration and freezing) and Phase II (monitoring). https://doi.org/10.1371/journal.pone.0348497.g001

</div>

1. Pre-processing, cleaning, and outlier handling. We implement initial filtering to remove windows that are unrepresentative or affected by extreme impulsive noise, in accordance with the condition indicators' consistency criteria.

2. Assessment of fundamental assumptions. We analyse marginal normality, within-segment autocorrelation, and temporal dependence between segments.

3. Transformations and appropriate modelling. Because autocorrelation is present, we apply the DPCA extension to capture the temporal structure, replacing the need for ad hoc transformations and providing a more suitable model for vibration signals.

4. In-control model estimation and optimal selection of hyperparameters (p, k). We implement a time-block CV, minimise SPE, and verify $ A R L_{0} $ via bootstrap simulation.

<!-- PDF_PAGE: 9 -->





5. Computation of $ T^{2} $ and SPE control limits with empirical $ ARL_{0} $ adjustment. We verify control-limit calibration by integrating the classical F approximation with an empirical bootstrap estimate to make $ ARL_{0} $ more robust.

Phase II: Process monitoring. Once the in-control model is fixed, we proceed with strict monitoring under standard multivariate SPC rules:

1. Standardising new data using frozen Phase I parameters. We do not recalibrate any parameters; this avoids contamination of failure information.

2. Constructing time windows and DPCA projection. Each window preserves the temporal structure defined in Phase I, ensuring direct comparability.

3. Online evaluation using $ T^{2} $ and SPE. We apply the UCL limits computed in Phase I. Optional memory charts (EWMA, CUSUM) optimised via CV are also considered.

4. Performance comparison: $ A R L_{0}, $ $ A R L_{1}, $ false-alarm rates, and detection capability. We add comparative metrics that allow the robustness and sensitivity of the monitoring system to be assessed.

To improve the clarity, transparency, and reproducibility of the proposed procedure, Appendix B presents a complete step-by-step workflow based on the real experimental data obtained from the test bench described in Section 3.

## 3 Test bench and data

The test bench used in the experimental phase (Fig 2) consists of a single-stage spur gearbox coupled to a three-phase motor rated at 2 HP, 220 V, and 1,200 rpm. We controlled the motor speed using a variable-frequency drive, enabling simulation of different speed conditions. We integrated an electromagnetic brake on the output shaft to apply different mechanical loads to the test bench.

The gearbox comprises a pinion, $ Z_{1} $ , with 32 teeth and a gear, $ Z_{2} $ , with 48 teeth. To simulate different mechanical degradation scenarios, we deliberately introduced ten severity levels of pinion tooth-break failure, labelled from $ P_{0} $ (healthy condition) to $ P_{9} $ (severe failure), as detailed in Table 1. We evaluated severity levels for specific combinations of rotational speeds (8 Hz, 14 Hz, and 20 Hz) using a variable-frequency drive. We applied load levels using the electromagnetic brake (0 V, 10 V, and 20 V) and replicated each experimental configuration 10 times with 10-second tests. In total, we obtained 900 records per sensor, each with 500,000 acceleration samples (measured in $ m/s^{2} $ ), providing a robust dataset for statistical analysis and diagnostic model validation.

We acquired vibration data in the time domain (Fig 3a) using four vertically mounted accelerometers $ ( A_{1}-A_{4} ) $ , and we subsequently transformed this signal to the frequency domain (Fig 3b) using the fast Fourier transform (FFT). Sensors $ A_{1} $ and $ A_{2} $ were installed on the input shaft, whereas $ A_{3} $ and $ A_{4} $ were located on the gearbox output shaft (the test bench also included acoustic emission, voltage, current-clamp, microphone, encoder, and laser encoder sensors). The sampling frequency of each channel was 50 kHz, providing high temporal resolution for dynamic analysis. We designed this experimental configuration to capture both the direct excitation generated by failures in the input gear teeth and the dynamic response propagated along the test bench. Defects in spur gears produce distinctive vibration signatures, which are influenced by the failure and by the prevailing operating conditions [47,48].

## (a)Time domain

## (b) Frequency domain

Table 2 provides descriptive information for the original vibration signal in the time domain with the pinion in healthy condition $ P_{0} $ (Phase I) and the nine severity levels $ P_{1}-P_{9} $ (Phase II).

<!-- PDF_PAGE: 10 -->






![figure_004.png](images/figure_004.png)



<div align="center">

Fig 2. Test bench layout.

</div>

<div align="center">

https://doi.org/10.1371/journal.pone.0348497.g002

</div>

The vibration signal is first divided into consecutive, non-overlapping time windows, so that each window captures a local portion of the process dynamics and can be treated as an individual observation for monitoring. Under this criterion, we define a segment as a time window containing between five and ten complete cycles of the Gear Mesh Frequency (GMF), with

$$
\mathrm {G M F} = f _ {r} \times Z _ {1},
$$

where $ f_{r} $ is the rotational frequency of the pinion $ Z_{1} $ , this segmentation strategy allows the temporal evolution of the vibration signal to be represented through successive local observations, while preserving sufficient information to detect

<!-- PDF_PAGE: 11 -->






![figure_005.png](images/figure_005.png)




![figure_006.png](images/figure_006.png)



<div align="center">

Fig 3. Vibration signal.

</div>

https://doi.org/10.1371/journal.pone.0348497.g003

<div align="center">

Table 2. Descriptive statistics of the original vibration signal in the time domain.

</div>

<table border="1"><tr><td>Type</td><td>Severity</td><td>Mean</td><td>Median</td><td>SD</td><td>Min</td><td>Max</td><td>Q05</td><td>Q25</td><td>Q75</td><td>Q95</td></tr><tr><td>Reference(PhaseI)</td><td>P0</td><td>0.07</td><td>0.06</td><td>0.76</td><td>-4.79</td><td>5.53</td><td>-1.09</td><td>-0.36</td><td>0.49</td><td>1.30</td></tr><tr><td>Fault(PhaseII)</td><td>P1</td><td>0.07</td><td>0.08</td><td>0.48</td><td>-2.99</td><td>3.26</td><td>-0.69</td><td>-0.20</td><td>0.34</td><td>0.79</td></tr><tr><td>Fault(PhaseII)</td><td>P2</td><td>0.06</td><td>0.06</td><td>1.63</td><td>-9.43</td><td>10.35</td><td>-2.55</td><td>-0.78</td><td>0.87</td><td>2.71</td></tr><tr><td>Fault(PhaseII)</td><td>P3</td><td>0.07</td><td>0.06</td><td>0.83</td><td>-6.15</td><td>5.59</td><td>-1.25</td><td>-0.41</td><td>0.54</td><td>1.39</td></tr><tr><td>Fault(PhaseII)</td><td>P4</td><td>0.08</td><td>0.11</td><td>1.96</td><td>-12.28</td><td>12.70</td><td>-2.99</td><td>-0.87</td><td>0.97</td><td>3.17</td></tr><tr><td>Fault(PhaseII)</td><td>P5</td><td>0.07</td><td>0.15</td><td>2.33</td><td>-9.22</td><td>10.74</td><td>-3.76</td><td>-1.53</td><td>1.54</td><td>3.86</td></tr><tr><td>Fault(PhaseII)</td><td>P6</td><td>0.06</td><td>0.02</td><td>1.23</td><td>-6.75</td><td>6.98</td><td>-1.83</td><td>-0.74</td><td>0.81</td><td>2.13</td></tr><tr><td>Fault(PhaseII)</td><td>P7</td><td>0.06</td><td>0.10</td><td>0.80</td><td>-5.55</td><td>5.55</td><td>-1.23</td><td>-0.42</td><td>0.57</td><td>1.24</td></tr><tr><td>Fault(PhaseII)</td><td>P8</td><td>0.07</td><td>0.13</td><td>1.02</td><td>-4.97</td><td>4.61</td><td>-1.79</td><td>-0.48</td><td>0.70</td><td>1.60</td></tr><tr><td>Fault(PhaseII)</td><td>P9</td><td>0.07</td><td>0.12</td><td>0.84</td><td>-7.87</td><td>8.39</td><td>-1.31</td><td>-0.33</td><td>0.53</td><td>1.17</td></tr></table>

https://doi.org/10.1371/journal.pone.0348497.t002

incipient changes associated with fault development. Moreover, this range (5-10 GMF cycles) balances spectral resolution and sensitivity to transients [49,50]. We compute the $ T^{2} $ and SPE statistics per segment and measure detection delays as the number of segments.

<!-- PDF_PAGE: 12 -->





After segmentation, each time window is characterised by means of a set of condition indicators (CIs) extracted from the corresponding portion of the signal, thereby transforming the raw vibration signal into a sequence of multivariate observations suitable for statistical monitoring. An iterative procedure involving resampling and parameter tuning determined the optimal number of sub-windows per signal, thereby maximising sensitivity to incipient faults and dynamic fluctuations. We extracted 10 CIs from each time sub-window and computed them in both the time and frequency domains.

In the time domain, we used the following CIs: mean, standard deviation, kurtosis, skewness, shape factor, impulse factor, clearance factor, crest factor, zero crossings, and higher-order time moments. In the frequency domain, we considered the following signal features: skewness, kurtosis, centre frequency, standard deviation, root mean square, relative dispersion ratio, shape indicator, second spectral moment, third spectral moment, and fourth spectral moment. The mathematical formulations of these CIs are presented in detail in Table 7 (Appendix A).

## 4 Results and discussion

This section evaluates the performance of the DPCA-MSPC scheme following the methodological workflow described in Section 2, which explicitly distinguishes between the calibration phase (Phase I) and the monitoring phase (Phase II). In Phase I, we select the hyperparameters (p,k) via CV, estimate the loadings $ \mathbf{P}_{k} $ and the spectrum $ \Lambda $ , and set the upper control limits $ UCL_{T^{2}} $ and $ UCL_{SPE} $ at significance level $ \alpha $ . Subsequently, in Phase II, observations associated with progressive failures are standardised using the frozen Phase I parameters, projected onto the DPCA subspace fixed in Phase I, and evaluated solely against those limits, without retraining or threshold readjustment. Under this protocol, we quantify:

(i) the detection delay by severity (median and IQR);

(ii) the monotonic relationship between severity and post-onset maxima (Spearman $ \hat{\rho} $);

(iii) out-of-control rates and alarm triggering; and

(iv) the temporal evolution of $ T^{2} $ and SPE.

The performance metrics are computed at the segment level, defined as a time sub-window containing between 5 and 10 complete cycles of the Gear Mesh Frequency (GMF), as specified in Section 3. Comparability between Phase I and Phase II is ensured because both $ T^{2} $ and SPE are evaluated on homogeneous decision units, and the detection delay is defined as the number of segments from failure onset to the first statistical alarm.

We calibrated the Phase I model on $ P_{0} $ using time-block CV to select $( p,k) $ by minimising SPE while preserving a stable in-control Average Run Length $ ( A R L_{0} ) $ . The selected configuration was $ p=0 $ and $ k=8 $ with $ \alpha=0.01 $ , yielding a median $ A R L_{0}\approx 3 6 $ segments. We computed the upper control limits $ U C L_{T^{2}} $ and $ U C L_{S P E} $ using the Snedecor F approximation and the Jackson-Mudholkar formula, respectively, and then froze them for the whole of Phase II (Table 3). Freezing implies that $( p,k) $ , the loadings $ \mathbf{P}_{k} $ , and the control thresholds are not recalibrated in the presence of failure.

<div align="center">

Table 3. Phase I: frozen control limits and model settings.

</div>

<table border="1"><tr><td>Method</td><td>p</td><td>k</td><td>$\alpha$</td><td>$UCL_{T2}$</td><td>$UCL_{SPE}$</td><td>$ARL_{0}$ median</td></tr><tr><td>DPCA(CV-Selected)</td><td>0</td><td>5</td><td>0.01</td><td>15.09</td><td>9.99</td><td>85</td></tr><tr><td>DPCA($ARL_{0}$-constrained)</td><td>0</td><td>8</td><td>0.01</td><td>23.23</td><td>0.76</td><td>36</td></tr><tr><td>DPCA(Phase I optimal)</td><td>1</td><td>7</td><td>0.01</td><td>18.49</td><td>16.65</td><td>97</td></tr></table>

https://doi.org/10.1371/journal.pone.0348497.t003

<!-- PDF_PAGE: 13 -->





On the other hand, the results in Table 3 highlight the trade-off between in-control stability $ ( A R L_{0} ) $ and failure sensitivity. Configurations with higher $ A R L_{0} $ , such as the DPCA model （ $ p=1 $ ）, reduce the probability of false alarms. However, they can delay the detection of incipient deviations. In contrast, the calibrated specification with $ A R L_{0}=3 6 $ prioritises earlier detection, particularly through the SPE statistic, whose significantly tighter threshold increases the ability to identify subtle changes in the process residual structure. This trade-off is relevant in industrial monitoring contexts, where the target $ A R L_{0} $ depends on system criticality, the costs associated with false alarms, and the operational risk of late detections. Considering both conservative and sensitive configurations enables us to robustly evaluate the DPCA scheme's Phase II performance across different risk profiles. Notably, the model selected via cross-validation focuses on reconstruction performance and does not necessarily coincide with the optimal configuration for process monitoring. In contrast, the Phase I optimal model is defined in terms of in-control performance, maximising $ A R L_{0} $ and reducing false alarm rates. This distinction highlights the need to decouple model selection criteria for prediction and monitoring tasks.

In Phase II under failure conditions $ ( P_{1}-P_{9} ) $ , we standardise each new observation exclusively using the Phase I parameters $ (\mu_{P_{0}} $ and $ \sigma_{P_{0}} $ ), represent it as a dynamic vector $ \mathbf{F}_{t} $ using the p selected in Phase I, and project it onto the frozen loadings $ \mathbf{P}_{k} $ . We then compute $ T^{2} ( t ) $ and $ SPE ( t ) $ and compare them with the limits $ UCL_{T^{2}} $ and $ UCL_{SPE} $ obtained in Phase I (see Algorithm B3). In this scheme, any threshold crossing in Phase II is interpreted directly as a deviation from the NOC defined in Phase I, without requiring model retraining or control-limit readjustment.

Table 4 presents the detection system performance by failure severity and by statistic. Specifically, the SPE statistic yields lower median detection delays than $ T^{2} $ in most scenarios, particularly for higher-severity failures. This pattern suggests that SPE is more sensitive to structural changes in the process residual variability. For severities $ P_{2} $ and $ P_{4} $ , SPE shows notably low median delays, with median SPE delays between 5 and 6 segments, accompanied by low $ ARL_{SPE} $ values, indicating rapid failure detection. In particular, case $ P_{4} $ stands out for low values of $ ARL_{T^{2}}=1.43 $ and $ ARL_{SPE}=1.69 $ . In addition, $ P_{4} $ exhibits reduced standard deviations (SDRL), reflecting highly stable control-scheme behaviour under severe failures. In contrast, severities $ P_{1}, $ $ P_{3}, $ $ P_{5} $ , and $ P_{6} $ show higher median delays and considerably larger ARL values, especially for the $ T^{2} $ statistic.

Accordingly, the associated SDRL values are also high, indicating high variability in detection time and, therefore, lower operational reliability for low- to intermediate-severity failures. This pattern is consistent with the statistical process control literature, where incipient failures tend to be more difficult to identify early [45,46]. The interquartile range of SPE $ ( I Q R_{S P E} ) $ reinforces this interpretation. For high severities, for example, $ P_{2} $ and $ P_{4} $ show a narrow $ I Q R_{S P E} $ indicating detection concentrated within a few segments. In contrast, for $ P_{3} $ and $ P_{5} $ $ I Q R_{S P E} $ widens, reaching values above 50 segments, reflecting greater uncertainty in detector performance. It is worth noting that these results confirm that the proposed Phase

<div align="center">

Table 4. Detection performance by severity failure. Phase II.

</div>

<table border="1"><tr><td>Severity</td><td>Median $T^{2}$ delay</td><td>Median SPE delay</td><td>IQRSPE</td><td>$ARL_{T^{2}}$</td><td>$SDRL_{T^{2}}$</td><td>$ARL_{SPE}$</td><td>SDRLSPE</td></tr><tr><td>$P_{1}$</td><td>24.00</td><td>18.00</td><td>[5.00,43.00]</td><td>31.78</td><td>52.51</td><td>13.20</td><td>25.65</td></tr><tr><td>$P_{2}$</td><td>22.50</td><td>6.00</td><td>[3.00,14.00]</td><td>6.39</td><td>24.72</td><td>7.57</td><td>21.26</td></tr><tr><td>$P_{3}$</td><td>21.00</td><td>17.00</td><td>[4.00,55.20]</td><td>19.01</td><td>46.98</td><td>23.26</td><td>47.97</td></tr><tr><td>$P_{4}$</td><td>28.00</td><td>5.00</td><td>[2.00,13.20]</td><td>1.43</td><td>1.02</td><td>1.69</td><td>1.63</td></tr><tr><td>$P_{5}$</td><td>20.00</td><td>18.00</td><td>[3.00,63.00]</td><td>14.30</td><td>38.82</td><td>16.67</td><td>49.33</td></tr><tr><td>$P_{6}$</td><td>26.00</td><td>18.50</td><td>[5.25,41.20]</td><td>20.46</td><td>41.34</td><td>20.68</td><td>37.25</td></tr><tr><td>$P_{7}$</td><td>21.00</td><td>16.50</td><td>[4.00,38.00]</td><td>3.59</td><td>6.06</td><td>4.97</td><td>8.59</td></tr><tr><td>$P_{8}$</td><td>14.50</td><td>9.00</td><td>[4.25,20.00]</td><td>11.03</td><td>24.17</td><td>24.44</td><td>47.82</td></tr><tr><td>$P_{9}$</td><td>20.50</td><td>15.00</td><td>[7.75,36.20]</td><td>4.43</td><td>9.68</td><td>3.42</td><td>4.43</td></tr></table>

https://doi.org/10.1371/journal.pone.0348497.t004

<!-- PDF_PAGE: 14 -->





II scheme is particularly efficient for medium- and high-severity failures. In addition, using the SPE statistic improves early detection, particularly for medium- and high-severity failures, although variability may remain high in low-severity cases.

Fig 4 shows the overall trend across all severities $ ( P_{1}-P_{9} ) $ : the residual-subspace chart ( SPE ) triggers alarms systematically earlier than $ T^{2} $ (global medians $ \tilde{d}_{SPE}\approx 16.5 $ versus $ \tilde{d}_{T^{2}}\approx 21 $ segments; see Table 4). This behaviour is consistent with failures that, in the first instance, disrupt the multivariate coherence learned in Phase I, transferring energy towards the residual subspace captured by SPE rather than inducing a mean shift within the principal subspace monitored by $ T^{2} $ [37,38]. The asymmetry between SPE and $ T^{2} $ is also observed qualitatively in the segmented time series (see Figs 6-15 in Appendix C): for most induced severities, SPE crosses its frozen Phase I UCL (red line) shortly after failure onset, whereas $ T^{2} $ often remains below its own UCL during the first affected segments. To assess whether this advantage of SPE increases with severity, we analyse the monotonic (non-parametric) association between failure severity $ ( P_{1}-P_{9} ) $ and the post-onset maxima of both control statistics; we use Spearman's correlation $ \hat{\rho} $ with percentile bootstrap confidence intervals.

The results indicate a weak but statistically significant negative association for SPE $ \left( \hat{\rho}\approx-0.10,p<0.01\right) $ and a nonsignificant association for $ T^{2} $ $ \left( \hat{\rho}\approx0.02,p=0.66\right) $ . We computed these correlations on post-onset maxima, not on detection delays. The trend observed for SPE suggests that, as induced severity increases, the residual energy captured by the model also increases, even when multivariate shifts within the principal subspace $ \left( T^{2}\right) $ do not exhibit a clear monotonic relationship. This result is consistent with the previously described failure mechanism: early-stage damage initially perturbs the correlation structure learned under NOC, primarily in the residual space (SPE) rather than in the principal subspace $ \left( T^{2}\right) $

In addition, we quantified the percentage of segments that exceed the Phase I control limits for each statistic $ \% T^{2} $ and $ \% SPE $ and recorded whether alerts were triggered per case $ (T^{2} $ Alert, SPE Alert). Because the limits remain frozen with k=8, variations in out-of-control rates reflect real process changes under fixed thresholds, rather than model readjustment.

<div align="center">

Detection Delay - DPCA Solid line: SPE, Dashed line: Hotelling's $ T^{2} $

</div>


![figure_007.png](images/figure_007.png)



<div align="center">

Fig 4. Detection delay by failure severity (Phase II). Solid line: SPE; dashed: $ T^{2} $ . The SPE chart detects earlier when the correlation structure learnt under NOC is broken.

</div>

https://doi.org/10.1371/journal.pone.0348497.g004

<!-- PDF_PAGE: 15 -->





Analysis of Table 5 shows that, although the means of $ T^{2} $ and SPE remain relatively stable (around 15 and 8, respectively), the maxima increase with severity (up to 881.34 for $ T^{2} $ and 361.05 for SPE), indicating the presence of localised anomalous episodes captured by the model even when the system's mean behaviour remains nearly invariant. Consistent with the delay analysis, SPE tends to yield higher out-of-control rates than $ T^{2} $ . Alert activation under all evaluated conditions confirms the diagnostic capability of the DPCA-MSPC scheme with Phase I frozen thresholds.

Figs 6-15 in Appendix C illustrate the temporal evolution of $ T^{2} $ and SPE for each failure severity level $ (P_{1}-P_{9}) $ . These segmented trajectories show localised exceedances above the Phase I control limits, which correspond to anomalous episodes in the vibration signals associated with tooth defects. These exceedances appear shortly after failure onset and intensify as severity increases, visually confirming the progressive transition from NOC to increasingly critical states under the same frozen statistical threshold.

On the other hand, Table 6 provides a comparative evaluation of the PCA and DPCA schemes using indicators of in-control stability and signalling capability, considering both the $ T^{2} $ and SPE statistics. The results allow the effects of incorporating temporal dynamics into the DPCA model to be identified. The PCA and DPCA models selected by CV without time lags （ $ p=0 $ ）yield identical results across all evaluated metrics. In particular, both methods exhibit an out-of-control (OOC) percentage of 3.62% for $ T^{2} $ and 1.17% for SPE, implying empirical false-alarm rates above the nominal level $ \alpha=0.01 $ . Likewise, the SDRL values associated with $ T^{2} $ (99.61) and SPE (96.97) indicate high dispersion in the signalling delay, reflecting inconsistent temporal stability.

This result empirically confirms that, in the absence of dynamic structure, DPCA is strictly equivalent to PCA and provides no additional improvement in statistical process control. In contrast, the DPCA specification with temporal dynamics （ p=1, k=7 ） introduces relevant quantitative changes. For the $ T^{2} $ statistic, the out-of-control percentage decreases from 3.62% to 2.51% , which represents a relative reduction of approximately 31%. This improvement is accompanied by a reduction in SDRL from 99.61 to 94.60 （ $ \approx $ 5% ), as well as a drop in the alarm probability (p alarm) from 0.71 to 0.58. These results indicate that incorporating time-lag filters helps account for serial variability, stabilises the behaviour of the principal subspace, and reduces the frequency and dispersion of false alarms associated with $ T^{2} $

<div align="center">

Table 5. Statistical results by failure severity.

</div>

<table border="1"><tr><td>Severity</td><td>Mean $ T^{2} $</td><td>Max $ T^{2} $</td><td>Mean SPE</td><td>Max SPE</td><td>% $ T^{2} $</td><td>% SPE</td><td>$ T^{2} $ Alert</td><td>SPE Alert</td></tr><tr><td>$ P_{1} $</td><td>14.98</td><td>283.40</td><td>8.19</td><td>121.34</td><td>13.24</td><td>23.51</td><td>True</td><td>True</td></tr><tr><td>$ P_{2} $</td><td>14.98</td><td>844.88</td><td>8.20</td><td>79.07</td><td>8.11</td><td>33.78</td><td>True</td><td>True</td></tr><tr><td>$ P_{3} $</td><td>14.98</td><td>714.60</td><td>8.15</td><td>198.70</td><td>9.34</td><td>29.47</td><td>True</td><td>True</td></tr><tr><td>$ P_{4} $</td><td>13.99</td><td>510.61</td><td>8.26</td><td>114.37</td><td>5.65</td><td>32.96</td><td>True</td><td>True</td></tr><tr><td>$ P_{5} $</td><td>15.98</td><td>731.89</td><td>8.20</td><td>94.13</td><td>7.49</td><td>34.60</td><td>True</td><td>True</td></tr><tr><td>$ P_{6} $</td><td>16.98</td><td>826.67</td><td>8.26</td><td>361.05</td><td>8.62</td><td>34.70</td><td>True</td><td>True</td></tr><tr><td>$ P_{7} $</td><td>14.98</td><td>720.34</td><td>8.82</td><td>324.61</td><td>14.68</td><td>30.90</td><td>True</td><td>True</td></tr><tr><td>$ P_{8} $</td><td>15.98</td><td>273.24</td><td>8.68</td><td>160.31</td><td>9.45</td><td>37.68</td><td>True</td><td>True</td></tr><tr><td>$ P_{9} $</td><td>14.98</td><td>881.34</td><td>8.36</td><td>90.20</td><td>7.49</td><td>31.21</td><td>True</td><td>True</td></tr></table>

https://doi.org/10.1371/journal.pone.0348497.t005

<div align="center">

Table 6. Comparisons between PCA and DPCA.

</div>

<table border="1"><tr><td>Method</td><td>%OOC $ P_{0} $ $ T^{2}$</td><td>%OOC $ P_{0} $ SPE</td><td>$ SDRLT_{2}$</td><td>p alarm $ T^{2}$</td><td>SDRLSPE</td><td>p alarm SPE</td></tr><tr><td>PCA</td><td>3.62</td><td>1.17</td><td>99.61</td><td>0.71</td><td>96.97</td><td>0.66</td></tr><tr><td>DPCA(p=0,k=5)</td><td>3.62</td><td>1.17</td><td>99.61</td><td>0.71</td><td>96.97</td><td>0.66</td></tr><tr><td>DPCA(p=1,k=7)</td><td>2.51</td><td>2.24</td><td>94.60</td><td>0.58</td><td>97.03</td><td>0.63</td></tr></table>

https://doi.org/10.1371/journal.pone.0348497.t006

<!-- PDF_PAGE: 16 -->





Regarding the SPE statistic, the out-of-control percentage increases from 1.17% to 2.24%, nearly doubling the empirical signalling rate. This increase is accompanied by an almost unchanged SDRL (97.03) and by a slight reduction in p alarm (from 0.66 to 0.63). These results suggest that the temporal dynamics captured by DPCA redistribute process variance, shifting part of the sensitivity towards the residual subspace, where SPE becomes more reactive to short-duration deviations or structural changes not explained by the dynamic principal components.

Fig 5 reveals differences when comparing PCA with dynamic DPCA （ p=1 ). For example, dynamic DPCA exhibits systematically higher values of the SPE statistic in terms of % above the UCL across virtually all severity levels. This separation is particularly marked at intermediate and high severities, where DPCA reaches signalling peaks that far exceed those observed under PCA. This result indicates that incorporating temporal dynamics increases the sensitivity of SPE to persistent residual deviations, consistent with the higher out-of-control percentage observed in Table 6. By contrast, the $ T^{2} $ statistic shows a more moderate behaviour. It is worth noting that both methods (PCA and dynamic DPCA) show increases in % above the UCL as severity increases. However, dynamic DPCA tends to generate smoother profiles and, at several levels, values that are comparable to or even lower than those of PCA. This result is consistent with the reduction in OOC percentage and p alarm reported for $ T^{2} $ in Table 6. It suggests that temporal dynamics help absorb serial dependence within the principal subspace, reducing spurious activation of the $ T^{2} $ statistic. Therefore, using dynamic DPCA is justified in processes with relevant temporal dependence, where anomalies may manifest gradually and differently across subspaces.

<div align="center">

Comparison of % Above the UCL: DPCA vs PCA Average by Severity (Run-Level Summary)

</div>


![figure_008.png](images/figure_008.png)



<div align="center">

Fig 5. Comparison DPCA vs PCA.

</div>

https://doi.org/10.1371/journal.pone.0348497.g005

<!-- PDF_PAGE: 17 -->





Overall, the results show that integrating DPCA within MSPC enables early and accurate detection of deviations from NOC in spur gearboxes through vibration analysis. The proposed model exhibits high sensitivity to subtle changes in system behaviour, reflected in significant increases in Hotelling's $ T^{2} $ and SPE, even at early failure stages.

Although a direct comparison with most previous DPCA studies is not straightforward, as they mainly focus on other types of rotating machinery, the empirical evidence supports the approach's effectiveness. For example, several works report that using DPCA significantly improves failure detection capability in wind turbines, cutting tools, and bearings, particularly by capturing the temporal structure of the signals [12,23-25].

Likewise, the results of this study are consistent with those reported by Baydar et al. [51], who, using singular value decomposition techniques applied to helical gears, identified incipient failures through SPE analysis, even without using Hotelling's $ T^{2} $ . These results reinforce the diagnostic value of multivariate PCA-based approaches for non-invasive characterisation of conditions.

In addition, Jin et al. [17] propose a variant of MSPC for fault-agnostic scenarios, integrating hierarchical clustering (HCA) to improve detection under non-Gaussian conditions. Their proposal highlights the need for adaptive frameworks, which appear promising as future extensions of this work, in particular through adaptive dynamic variants of DPCA.

Moreover, Jorry et al. [23] developed a hybrid strategy combining MSPC with Fourier transforms and genetic algorithms for bearing failure detection, achieving high diagnostic accuracy through time-domain indicators. The authors emphasise the relevance of robust multivariate schemes for rotating machinery monitoring.

From another condition monitoring perspective, the literature shows that, in rotating systems with variable speed, non-stationary operation, or high sensor complexity, strategies such as angular resampling, NOC references based on spectral kurtosis, multi-source fusion, and hybrid approaches based on time-frequency representations and convolutional neural networks can improve diagnostic stability and failure identification [52-56]. Although these mechanisms are not part of the methodological workflow adopted in this study, their findings help to contextualise the challenges associated with operating variability and reinforce the relevance of the proposed DPCA-MSPC scheme; within this framework, MSPC retains its role in early warning and statistical interpretability, while subsequent supervised approaches may be considered complementary tools for discriminating failure types and severity levels.

Finally, the available evidence supports the suitability of the approach adopted in this study, which extends the application of DPCA-MSPC to high-criticality mechanical components such as spur gearboxes. The combination of diagnostic sensitivity, temporal modelling, and computational efficiency positions this methodology as a robust tool for continuous monitoring and decision-making in predictive maintenance under demanding industrial conditions. Therefore, implementing DPCA within MSPC frameworks constitutes a substantive contribution to the development of advanced data-driven diagnostic strategies.

## 5 Conclusions

This study demonstrates that integrating DPCA within an MSPC framework provides an effective, interpretable, and computationally efficient strategy for early failure detection in spur gearboxes. The proposed scheme calibrates model complexity via time-block CV, minimising out-of-sample SPE under a controlled $ A R L_{0} $ constraint, and then freezes the Phase I statistical limits for use in Phase II. For the analysed dataset, the selected configuration was $ (p,k)=(0,8) $ with $ \alpha=0.01 $ applying fixed $ U C L_{T^{2}} $ and $ U C L_{S P E} $ across all failure severities (Table 3).

Combining Hotelling's $ T^{2} $ (principal subspace) and SPE (residual space) provides a complementary and robust characterisation of deviations from NOC. Consistent with the methodological protocol, in Phase II the SPE chart systematically triggers alarms earlier than $ T^{2} $ for all severities $ (\tilde{d}_{SPE}\approx 16.5 $ versus $ \tilde{d}_{T^{2}}\approx 21 $ segments), and the post-onset maxima exhibit a weak but statistically significant monotonic association with severity for SPE (Spearman $ \hat{\rho}\approx-0.10 $ $ p<0.01 $ ), but not for $ T^{2} $ $ (\hat{\rho}\approx 0.02 $ $ p=0.66) $ . This asymmetry is consistent with a physical-statistical mechanism in which early damage manifestations first perturb the correlation structure learned under NOC, injecting energy into the residual space (SPE) before inducing sustained shifts within the principal subspace $ (T^{2}) $

<!-- PDF_PAGE: 18 -->





From a methodological perspective, this work extends the DPCA-MSPC framework to spur gearboxes, which are critical components in many mechanical systems, through an unsupervised, data-driven calibration that does not require labelled failures. Freezing the Phase I limits ensures objective and comparable decisions in Phase II, while jointly using $ T^{2} $ and SPE increases sensitivity to shifts in the principal subspace and to changes in the residual structure. Unlike most previous studies focused on bearings or wind turbines, and to the best of our knowledge, this is the first documented application of an DPCA-MSPC scheme to spur gearbox diagnosis, bridging engineering-oriented vibration analysis and data-driven statistical process control.

Validation was conducted under controlled laboratory conditions, which may limit extrapolation to plant environments with greater variability and noise. Although the test bench provided additional signals (acoustic emission, airborne sound, voltage/current), we deliberately chose not to integrate multi-signal analysis in order to isolate the specific contribution of vibration under an DPCA-MSPC protocol with frozen thresholds.

Future work will proceed in three directions: (i) incorporating adaptive schemes for non-stationary conditions with online parameter adjustment while maintaining a controlled $ A R L_{0} $; (ii) validating the framework in plant settings under variable operating regimes and real disturbances; and (iii) exploring signal fusion and adaptive variants of DPCA to strengthen sensitivity to incipient degradation and improve cross-domain transferability.

## Supporting information

S1 Appendix. A: Condition Indicators, B: Illustration of the DPCA-MSPC framework (Pipeline), and C: Figures should be included.

(ZIP)

## Author contributions

Conceptualization: Antonio Pérez-Torres, Jean Navarrete-Campos, Reinier Fernández-López, Jorge Figueroa-Zuñiga, Susana Barcelo-Cerdá.

Data curation: Antonio Pérez-Torres, Jean Navarrete-Campos, Reinier Fernández-López, Jorge Figueroa-Zuñiga, Susana Barcelo-Cerdá.

Formal analysis: Antonio Pérez-Torres, Jean Navarrete-Campos, Reinier Fernández-López, Jorge Figueroa-Zuñiga, Susana Barcelo-Cerdá.

Funding acquisition: Antonio Pérez-Torres.

Investigation: Antonio Pérez-Torres, Jean Navarrete-Campos, Reinier Fernández-López, Jorge Figueroa-Zuñiga, Susana Barcelo-Cerdá.

Methodology: Antonio Pérez-Torres, Jean Navarrete-Campos, Reinier Fernández-López, Jorge Figueroa-Zuñiga, Susana Barcelo-Cerdá.

Project administration: Antonio Pérez-Torres.

Resources: Antonio Pérez-Torres, Jean Navarrete-Campos, Reinier Fernández-López, Jorge Figueroa-Zuñiga, Susana Barcelo-Cerdá.

Software: Antonio Pérez-Torres, Jean Navarrete-Campos, Reinier Fernández-López, Jorge Figueroa-Zuñiga, Susana Barcelo-Cerdá.

Supervision: Antonio Pérez-Torres, Jean Navarrete-Campos, Reinier Fernández-López, Jorge Figueroa-Zuñiga, Susana Barcelo-Cerdá.

Validation: Antonio Pérez-Torres, Jean Navarrete-Campos, Reinier Fernández-López, Jorge Figueroa-Zuñiga, Susana Barcelo-Cerdá.

<!-- PDF_PAGE: 19 -->





Visualization: Antonio Pérez-Torres, Jean Navarrete-Campos, Reinier Fernández-Lopez, Jorge Figueroa-Zuñiga, Susana Barcelo-Cerdá.

Writing - original draft: Antonio Pérez-Torres, Jean Navarrete-Campos, Reinier Fernández-López, Jorge Figueroa- Zuñiga, Susana Barcelo-Cerdá.

Writing - review & editing: Antonio Pérez-Torres, Jean Navarrete-Campos, Reinier Fernández-López, Jorge Figueroa- Zuñiga, Susana Barcelo-Cerdá.

## References

1. Goswami P, Rai RN. Data-driven sensor selection for industrial gearbox fault diagnosis using principal component analysis. Measurement Science and Technology. 2025;36(3):036111. https://doi.org/10.1088/1361-6501/adb06b

2. Kini KR, Harrou F, Madakyaru M, Sun Y. Enhancing wind turbine performance: Statistical detection of sensor faults based on improved dynamic independent component analysis. Energies. 2023;16(15):5793. https://doi.org/10.3390/en16155793

3. Luan X, Jin M, Liu F. Fault detection based on near-infrared spectra for the oil desalting process. Applied Spectroscopy. 2018;72(8):1199-204. https://doi.org/10.1177/00037028187760

4. Dong E, Zhang Y, Zhan X, Bai Y, Cheng Z. A novel dynamic predictive maintenance framework for gearboxes utilizing nonlinear Wiener process. Measurement Science and Technology. 2024;35(12):126210. https://doi.org/10.1088/1361-6501/ad762e

5. Zhou Y, Jin R, Qiu P. Machine Learning Control Charts for Monitoring Spatio-Temporal Data Streams. Quality and Reliability Engineering Internationa. 2025;In press. https://doi.org/10.1002/qre.3809

6. Zhu C, Liu N, Ji L, Zhao Y, Shi X, Lan X. A multi-source mixed-frequency information fusion framework based on spatial-temporal graph attention network for anomaly detection of catalyst loss in FCC regenerators. Chinese Journal of Chemical Engineering. 2025. https://doi.org/10.1016/j.cjche.2025.02.025

7. Hu H, Feng F, Han J, Zhu J, Song C. Fault Warning Technology Based on Multivariate Statistical Analysis. Journal of Industry and Engineering Management (ISSN: 2959-0612). 2024;2(1):65. https://doi.org/10.62517/jiem.202403110

8. Ma X, Zhai K, Luo N, Zhao Y, Wang G. Gearbox Fault Diagnosis Under Noise and Variable Operating Conditions Using Multiscale Depthwise Separable Convolution and Bidirectional Gated Recurrent Unit with a Squeeze-and-Excitation Attention Mechanism. Sensors. 2025;25(10):2978. https://doi.org/10.3390/s25102978

9. Pérez-Torres A, Navarrete-Campos J, Sánchez RV, Barceló-Cerdá S. Selection of Vibration Signal Features in the Frequency Domain to Determine the Level of Failure Severity in Spur Gearboxes. Journal of Vibration Engineering & Technologies. 2025;13(8):629. https://doi.org/10.1007/s42417-025-02213-w

10. Yin Y, Xu B, Sun L, Wu J. Early Fault Detection Method for Doubly-Fed Induction Generator in Wind Power Systems Based on Multi-Scale Latent Variable Regression. IEEE Transactions on Instrumentation and Measurement. 2025. https://doi.org/10.1109/TIM.2025.3542110

11. Pérez-Torres A, Sánchez RV, Barceló-Cerdá S. Selection of the level of vibration signal decomposition and mother wavelets to determine the level of failure severity in spur gearboxes. Quality and Reliability Engineering International. 2024;40(6):3439-51. https://doi.org/10.1002/qre.3578

12. Jiang L, Cui J, Wang J. A DPCA-based online fault indicator for gear faults using three-direction vibration signals. Journal of Vibroengineering. 2018;20(3):1340-54. https://doi.org/10.21595/jve.2017.18371

13. Ueda RM, Agostino IRS, Souza AM. Analysis and perspectives on multivariate statistical process control charts used in the industrial sector: a systematic literature review. Management and Production Engineering Review. 2022:48-60. https://doi.org/10.24425/mper.2022.142054

14. Newhart KB, Klanderman MC, Hering AS, Cath TY. A holistic evaluation of multivariate statistical process monitoring in a biological and membrane treatment system. ACS Es&t Water. 2023;4(3):913-24. https://doi.org/10.1021/acsestwater.3c00058

15. Jalilibal Z, Karavigh MHA, Maleki MR, Amiri A. Control charting methods for monitoring high dimensional data streams: A conceptual classification scheme. Computers & Industrial Engineering. 2024;191:110141. https://doi.org/10.1016/j.cie.2024.110141

16. Daga AP, Garibaldi L. Diagnostics of rotating machinery through vibration monitoring: signal processing and pattern analysis. Applied Sciences. 2024;14(20):9276. https://doi.org/10.3390/app14209276

17. Jin X, Fan J, Chow TW. Fault detection for rolling-element bearings using multivariate statistical process control methods. IEEE Transactions on Instrumentation and Measurement. 2018;68(9):3128-36. https://doi.org/10.1109/TIM.2018.2872610

18. Li Z, Yan X, Tian Z, Yuan C, Peng Z, Li L. Blind vibration component separation and nonlinear feature extraction applied to the nonstationary vibration signals for the gearbox multi-fault diagnosis. Measurement. 2013;46(1):259-71. https://doi.org/10.1016/j.measurement.2012.06.013

19. Hajarian N, Movahedi Sobhani F, Sadjadi SJ. An improved approach for fault detection by simultaneous overcoming of high-dimensionality, autocorrelation, and time-variability. Plos one. 2020;15(12):e0243146. https://doi.org/10.1371/journal.pone.0243146

20. Inturi V, Sabareesh G, Supradeepan K, Penumakala PK. Principal component analysis based gear fault diagnostics in different stages of a multi-stage gearbox subjected to extensive fluctuating speeds. Journal of Nondestructive Evaluation, Diagnostics and Prognostics of Engineering Systems. 2021;4(3):031005. https://doi.org/10.1115/1.4050265

<!-- PDF_PAGE: 20 -->





21. Li Z, Yan X, Wang X, Peng Z. Detection of gear cracks in a complex gearbox of wind turbines using supervised bounded component analysis of vibration signals collected from multi-channel sensors. Journal of Sound and Vibration. 2016;371:406-33. https://doi.org/10.1016/j.jsv.2016.02.021

22. Ge Z, Kruger U, Lamont L, Xie L, Song Z. Fault detection in non-Gaussian vibration systems using dynamic statistical-based approaches. Mechanical Systems and Signal Processing. 2010;24(8):2972-84. https://doi.org/10.1016/j.ymssp.2010.03.015

23. Jorry V, Duma ZS, Sihvonen T, Reinikainen SP, Roininen L. Statistical batch-based bearing fault detection. Journal of Mathematics in Industry. 2025;15(1):4. https://doi.org/10.1186/s13362-025-00169-w

24. Pozo F, Vidal Y, Salgado O. Wind turbine condition monitoring strategy through multiway PCA and multivariate inference. Energies. 2018;11(4):749. https://doi.org/10.3390/en11040749

25. Rezamand M, Kordestani M, Carriveau R, Ting DSK, Saif M. A new hybrid fault detection method for wind turbine blades using recursive PCA and wavelet-based PDF. IEEE Sensors journal. 2019;20(4):2023-33. https://doi.org/10.1109/JSEN.2019.2948997

26. Daga AP, Garibaldi L. Machine vibration monitoring for diagnostics through hypothesis testing. Information. 2019;10(6):204. https://doi.org/10.3390/ info10060204

27. Zhou S, Zhou X, Liu H. Process monitoring and fault diagnosis method combining bagging DPCA-ICA with moving window Kolmogorov-Smirnov test. The Canadian Journal of Chemical Engineering. 2024;102(7):2495-510. https://doi.org/10.1002/cjce.25211

28. Hao W, Lu S, Lou Z, Wang Y, Jin X, Deprizon S. A novel dynamic process monitoring algorithm: Dynamic orthonormal subspace analysis. Processes. 2023;11(7):1935. https://doi.org/10.3390/pr11071935

29. Qu Q, Dong Y, Zheng Y. Recursive Dynamic inner PrincipalComponent Analysis for Adaptive ProcessModeling. IFAC-PapersOnLine. 2024;58(14):682-7. https://doi.org/10.1016/j.ifacol.2024.08.416

30. Vanhatalo E, Kulahci M, Bergquist B. On the structure of dynamic principal component analysis used in statistical process monitoring. Chemometrics and intelligent laboratory systems. 2017;167:1-11. https://doi.org/10.1016/j.chemolab.2017.05.016

31. Ma X, Chen T, Wang Y. Dynamic process monitoring based on dot product feature analysis for thermal power plants. IEEE/CAA journal of automatica sinica. 2025;12(3):563-74. https://doi.org/10.1109/JAS.2024.124908

32. Treasure RJ, Kruger U, Cooper JE. Dynamic multivariate statistical process control using subspace identification. Journal of Process Control. 2004;14(3):279-92. https://doi.org/10.1016/S0959-1524(03)00041-6

33. Guo L, Wu P, Lou S, Gao J, Liu Y. A multi-feature extraction technique based on principal component analysis for nonlinear dynamic process monitoring. Journal of Process Control. 2020;85:159-72. https://doi.org/10.1016/j.jprocont.2019.11.010

34. Dang VL, Li Y, Sun B, Yin S, Li J. A Novel Dynamic Process Monitoring Method Based on the Autocorrelation and the Cross-Correlation Analysis of Process Variables. Industrial & Engineering Chemistry Research. 2025. https://doi.org/10.1021/acs.iecr.4c04312

35. Takens F. Detecting strange attractors in turbulence. In: Rand D, Young LS, editors. Dynamical Systems and Turbulence, Warwick 1980. Berlin, Heidelberg: Springer Berlin Heidelberg; 1981. p. 366-81.

36. Zhang X, Zhang Y, Liew K. Machine learning predictive model for dynamic response of rising bubbles impacting on a horizontal wall. Computer Methods in Applied Mechanics and Engineering. 2024;429:117157. https://doi.org/10.1016/j.cma.2024.117157

37. Ku W, Storer RH, Georgakis C. Disturbance detection and isolation by dynamic principal component analysis. Chemometrics and Intelligent Laboratory Systems. 1995;30(1):179-96. https://doi.org/10.1016/0169-7439(95)00076-3

38. Lee JM, Yoo C, Lee IB. Statistical monitoring of dynamic processes based on dynamic independent component analysis. Chemical Engineering Science. 2004;59(14):2995-3006. https://doi.org/10.1016/j.ces.2004.04.031

39. Lim J, Lee S. Efficient ARL estimation for general control charts using censored run lengths. Quality Engineering. 2025;37(3):359-68. https://doi. org/10.1080/08982112.2024.2399104

40. Woodall WH. Controversies and contradictions in statistical process control. Journal of quality technology. 2000;32(4):341-50. https://doi.org/10.10 80/00224065.2000.11980013

41. Jolliffe I. Principal component analysis. In: International encyclopedia of statistical science. Springer; 2011. p. 1094-6.

42. Jackson JE, Mudholkar GS. Control procedures for residuals associated with principal component analysis. Technometrics. 1979;21(3):341-9. https://doi.org/10.1080/00401706.1979.10489779

43. Montgomery DC. Introduction to statistical quality control. John wiley & sons; 2020.

44. Arslan M, Shahzad U, Yeganeh A, Zhu H, Malela-Majika JC, Ahmad S. A Robust L-Comoments Covariance Matrix-Based Hotelling's T 2 T2 Control Chart for Monitoring High-Dimensional Non-Normal Multivariate Data in the Presence of Outliers. Quality and Reliability Engineering International. 2025;41(7):3308-17. https://doi.org/10.1002/qre.70025

45. Zwetsloot IM, Jones-Farmer LA, Woodall WH. Monitoring univariate processes using control charts: Some practical issues and advice. Quality Engineering. 2024;36(3):487-99. https://doi.org/10.1080/08982112.2023.2238049

46. Wang K, Xu W, Li J. An efficient and unified statistical monitoring framework for multivariate autocorrelated processes. Computers & Industrial Engineering. 2024;198:110675. https://doi.org/10.1016/j.cie.2024.110675

47. Stander C, Heyns P, Schoombie W. Using vibration monitoring for local fault detection on gears operating under fluctuating load conditions Mechanical systems and signal processing. 2002;16(6):1005-24. https://doi.org/10.1006/mssp.2002.1479

<!-- PDF_PAGE: 21 -->





48. Pérez-Torres A, Sánchez RV, Barceló-Cerdá S. Methodology for Feature Selection of Time Domain Vibration Signals for Assessing the Failure Severity Levels in Gearboxes. Appl Sci. 2025;15:5813. https://doi.org/10.3390/app15115813

49. Bartelmus W, Zimroz R. Vibration condition monitoring of planetary gearbox under varying external load. Mechanical systems and signal processing. 2009;23(1):246-57. https://doi.org/10.1016/j.ymssp.2008.03.016

50. Antoni J, Randall RB. The spectral kurtosis: application to the vibratory surveillance and diagnostics of rotating machines. Mechanical systems and signal processing. 2006;20(2):308-31. https://doi.org/10.1016/j.ymssp.2004.09.002

51. Baydar N, Ball A, Payne B. Detection of incipient gear failures using statistical techniques. IMA Journal of Management Mathematics. 2002;13(1):71-9. https://doi.org/10.1093/imaman/13.1.71

52. He W, Hang J, Ding S, Sun L, Hua W. Robust diagnosis of partial demagnetization fault in PMSMs using radial air-gap flux density under complex working conditions. IEEE Transactions on Industrial Electronics. 2024;71(10):12001-10. https://doi.org/10.1109/TIE.2024.3349520

53. Wang T, Liang M, Li J, Cheng W. Rolling element bearing fault diagnosis via fault characteristic order (FCO) analysis. Mechanical Systems and Signal Processing. 2014;45(1):139-53. https://doi.org/10.1016/j.ymssp.2013.11.011

54. Wang T, Han Q, Chu F, Feng Z. A new SKRgram based demodulation technique for planet bearing fault detection. Journal of Sound and Vibration. 2016;385:330-49. https://doi.org/10.1016/j.jsv.2016.08.026

55. Hang J, Qiu G, Hao M, Ding S. Improved fault diagnosis method for permanent magnet synchronous machine system based on lightweight multi-source information data layer fusion. IEEE Transactions on Power Electronics. 2024;39(10):13808-17. https://doi.org/10.1109/TPEL.2024.3432163

56. Zhao D, Wang T, Chu F. Deep convolutional neural network based planet bearing fault classification. Computers in Industry. 2019;107:59-66. https://doi.org/10.1016/j.compind.2019.02.001