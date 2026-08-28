---
source: "extraction_papers/10.3390_s26092661.pdf"
title: "10.3390_s26092661"
page_count: 23
converted_at: "2026-08-27T23:16:32Z"
---

<!-- PDF_PAGE: 1 -->









Article

<div align="center">

# Spatio-Temporal Joint Network for Coupler Anomaly Detection Under Complex Working Conditions Utilizing Multi-Source Sensors

</div>

Zhirong Zhao $ ^{1} $ , Zhentian Jiang $ ^{1} $ , Qian Xiao $ ^{2} $ , Long Zhang $ ^{2,*} $ and Jinbo Wang $ ^{2} $

1 Rolling Stock Branch, CHN Energy Shuohuang Railway Development Co., Ltd., Cangzhou 062350, China; zhirong.zhao.a@ceic.com (Z.Z.); 11074809@ceic.com (Z.J.)

$ ^{2} $ School of Mechatronics and Vehicle Engineering, East China Jiaotong University, Nanchang 330013, China; jxralph@ecjtu.edu.cn (Q.X.); wwwbojw@163.com (J.W.)

* Correspondence: longzh@126.com; Tel.: +86-152-7092-5287

## Abstract

Owing to the intricate mechanical coupling characteristics and the considerable difficulty in extracting synergistic spatio-temporal features from high-dimensional sensor data under fluctuating alternating loads, this study proposes a robust anomaly detection framework that combines Normalized Mutual Information (NMI) and Spatio-Temporal Graph Neural Networks (STGNN). First, NMI is utilized to quantify the nonlinear physical coupling intensity among multi-source sensors, thereby filtering out weakly correlated noise and reconstructing the spatial topological structure of the coupler system. Subsequently, a deep learning architecture incorporating Graph Convolutional Networks (GCN), Gated Recurrent Units (GRU), and one-dimensional convolutional residual connections is developed to capture the dynamic evolutionary characteristics of equipment states across both spatial interactions and temporal sequences. Finally, based on the model's health-state predictions, a moving average algorithm is introduced to smooth the residual sequences, and an anomaly early-warning baseline is established in conjunction with the 3 $ \sigma $ criterion. Experimental validation conducted using field service data from heavy-haul trains demonstrates that, compared to conventional serial CNN and Long Short-Term Memory (LSTM) models, the proposed method exhibits superior fitting performance and robustness against noise, effectively reducing the false alarm rate within normal working intervals. In a real-world case study, the method successfully identified variations in spatial linkage features induced by local damage and triggered timely alerts. Notably, the spatial alarm nodes were highly consistent with the fatigue crack initiation sites identified through on-site magnetic particle inspection. This study provides a viable data-driven analytical framework for the condition monitoring and anomaly identification of critical load-bearing components in heavy-haul trains.

Check for updates


![figure_001.png](images/figure_001.png)



Academic Editor: Steven Chatterton

Keywords: heavy-haul train; coupler and draft gear system; normalized mutual information; spatio-temporal graph neural network; anomaly detection

Copyright: 2026 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license.

## 1. Introduction

Concomitant with the evolution of heavy-haul railways toward increased axle loads and extended train configurations, the service safety and structural integrity of critical load-bearing components, such as coupler and draft gear systems, under complex alternating loads have garnered significant attention [1]. Traditional preventive maintenance

<!-- PDF_PAGE: 2 -->

protocols and manual offline non-destructive testing (NDT) are constrained by operational inefficiency and an inability to capture latent risks in a real-time manner [2]. Consequently, transitioning toward condition-based maintenance (CBM) supported by real-time sensor data has emerged as an imperative strategy for enhancing maintenance precision and ensuring operational reliability [3]. Nevertheless, the mechanical stress and deformation mechanisms inherent in coupler systems are highly sophisticated, but existing data-driven fault diagnosis methodologies predominantly focus on univariate sensor time-series analysis. When applied to dense sensor networks within coupler systems, these approaches struggle to fully characterize the potent nonlinear spatial coupling and dynamic latency features among multi-dimensional signals. This limitation frequently leads to missed detections of incipient faults under complex working conditions, while also increasing susceptibility to false alarms triggered by high-frequency noise interference [4].

In recent years, extensive scholarly efforts have been dedicated to the condition monitoring and assessment of critical mechanical components during service. Early investigations primarily relied on physical failure mechanisms and finite element method (FEM) simulations [5]. Zhang et al. [6] conducted systematic experimental research on the dynamic performance and compressive stability of heavy-haul locomotives under longitudinal forces through a series of field tests involving 10,000-ton trains. By establishing a numerical model that accounts for complex nonlinear contact, Ren et al. [7] predicted that the remaining useful life (RUL) of a 4 mm initial surface crack within a coupler is approximately 700,000 km. Furthermore, Dumitriu [8] analyzed the vertical vibrational responses of bogies by integrating experimental data with rigid-flexible coupling numerical simulations, thereby exploring the feasibility of fault detection methodologies for primary suspension dampers.

While physical-mechanism-based studies offer high fidelity under specific, welldefined conditions, the actual working environments and loading regimes of heavy-haul trains are exceedingly complex. Purely physical models struggle to accurately characterize nonlinear degradation signatures under multi-source variable-amplitude loading. Given these intricate evolutionary patterns, such models often exhibit insufficient precision when describing service states, ultimately failing to satisfy the rigorous demands of practical engineering applications [9].

To address these challenges, researchers have increasingly pivoted toward data-driven methodologies leveraging real-time monitoring data, which has progressively emerged as a focal point of scholarly inquiry in this field [10]. Early data-driven investigations were primarily predicated upon conventional shallow machine learning algorithms. Li et al. [11] integrated wavelet packet decomposition (WPD) with one-class support vector machines (OCSVM) to design an Internet of Things (IoT)-based condition monitoring system for mechanical equipment, facilitating the effective identification of anomalies through signal feature extraction. Similarly, the study conducted by Li et al. [12] incorporated classical machine learning algorithms, such as k-nearest neighbors (k-NN) and clustering, to refine the Multivariate State Estimation Technique (MSET), achieving efficient anomaly pattern recognition by constructing health data intervals. Gomez et al. [13] leveraged WPD to extract energy features from axle-box vibration signals and, coupled with SVM, realized high-reliability real-time diagnostics for railway axle cracks. Furthermore, Dhiman et al. [14] utilized Neighborhood Component Analysis (NCA) for feature selection, combining support vector regression (SVR) with decision tree models to achieve high-precision state prediction for critical wind turbine components.

Nevertheless, traditional machine learning approaches exhibit a profound reliance on domain expertise and manual feature engineering [15]. When confronted with the massive, high-dimensional, and nonlinear monitoring datasets generated by heavy-haul trains

<!-- PDF_PAGE: 3 -->

under complex working conditions, shallow-architecture networks often encounter significant impediments, such as suboptimal feature extraction and inadequate generalization capabilities [16]. These inherent architectural constraints hinder the effective discernment of latent underlying patterns within complex scenarios, resulting in insufficient adaptability within authentic field service environments [17].

To circumvent reliance on manual prior knowledge, deep learning architectures characterized by self-adaptive capabilities have established dominance in the field of condition monitoring. By facilitating automated feature extraction, this paradigm demonstrates superior adaptability when processing massive datasets [18]. Addressing the challenge of limited fault sample acquisition, Liu et al. [19] developed an enhanced autoencoder model integrating CNN and LSTM. By leveraging the frequency-domain characteristics of normal samples, they achieved accurate early warning for unknown faults and significantly bolstered the model's generalization capability in complex industrial environments. Li et al. [20] proposed an unsupervised anomaly detection methodology fusing stacked autoencoders and LSTM, which incorporates WPD to extract multi-feature sequences, enabling effective condition recognition for rotating machinery using entirely unlabeled historical data. Furthermore, Hu et al. [21] introduced a reconstruction approach termed ADMM-1DNet, based on the synthesis of deep neural networks (DNN) and compressed sensor. By mapping the Alternating Direction Method of Multipliers (ADMM) onto a deep network architecture and learning redundant analysis operators, they effectively enhanced the reconstruction precision and feature-preservation capacity of vibration signals under high-noise backgrounds. Exploring non-contact acoustic monitoring scenarios, Zou et al. [22] proposed a multi-channel few-shot learning framework that utilizes a global optimization layer strategy to overcome the challenges of anomaly detection with limited samples in complex environments. Additionally, Hu et al. [23] developed a forecasting framework combining time-series autocorrelation decomposition with CNN, which significantly refines RUL prediction accuracy by deeply integrating both long- and short-term health state features.

Existing deep learning architectures predominantly treat multi-dimensional monitoring signals as independent sequences, prioritizing the extraction of temporal features while neglecting the spatial physical topology dictated by mechanical structures and force transmission pathways [24]. Under the complex loading regimes of heavy-haul trains, this disregard for spatial collaborative constraints compromises the sensitivity to incipient anomalies and increases susceptibility to false alarms triggered by local noise interference [25].

To circumvent the bottleneck of synergistically extracting spatio-temporal features from multi-dimensional sensor signals, Graph Neural Networks (GNN) have recently been introduced into the domain of complex equipment condition monitoring, owing to their unique advantages in processing non-Euclidean data and capturing intricate topological dependencies among nodes [26]. Liang et al. [27] proposed an end-to-end framework integrating Graph Attention Networks (GAT) and adaptive Transformers, effectively addressing the deficiencies of conventional models in overlooking multi-sensor spatial correlations. In response to the volatile working conditions of real-world scenarios, Fu et al. [28] developed a multi-scale dynamic STGNN that synergizes GAT mechanisms with long- and short-term temporal branches, significantly bolstering the dynamic adaptability and robustness of equipment anomaly detection. For high-dimensional and noisy industrial control data, Wang et al. [29] leveraged prior knowledge to construct dynamic graph models coupled with denoising modules, presenting a spatio-temporal graph anomaly detection framework suitable for fine-grained condition monitoring. To further enhance the credibility and physical consistency of deep learning models, Liu et al. [30] embedded domain-specific physical

<!-- PDF_PAGE: 4 -->

mechanism knowledge into GNNs, constructing physics-guided spatio-temporal models to achieve high-precision predictions. Furthermore, Wang et al. [31] innovatively extended graph modeling strategies to the frequency domain by constructing graph-mapped spectra reflecting the spatio-temporal dynamics of short-time periodogram spatial configurations, thereby providing a novel perspective for the degradation monitoring of bearing health states. Du et al. [32] developed a mechanism-embedded hybrid graph neural network to improve the generalization ability of anomaly detection in industrial cyber-physical systems under distribution shift and unknown operating conditions. Pan et al. [33] proposed a multi-node network-based blind deconvolution approach with adaptive frequency band segmentation to achieve effective fault feature extraction and fault detection for high-speed train axlebox bearings under low signal-to-noise ratio environments.

Addressing the challenges of topological graph construction and feature extraction, this study focuses on heavy-haul train coupler and draft gear systems and proposes an anomaly monitoring methodology termed NMI-STGNN. This scheme leverages NMI to quantify the correlations among sensors, thereby filtering noise interference while reconstructing the spatial topology. By integrating GCN and GRU, the model is capable of deeply mining the spatio-temporal evolutionary laws of equipment states. Based on prediction residuals and the 3 $ \sigma $ criterion, the system adaptively establishes a health baseline, ensuring high sensitivity in anomaly monitoring. This research provides a reliable theoretical and practical reference for the intelligent operation and maintenance of critical components.

The primary contributions of this work are summarized as follows:

(1) A methodology leveraging NMI is proposed to quantify the nonlinear physical coupling intensity among multi-source sensors within the coupler system. This approach effectively eliminates weakly correlated redundant noise and reconstructs a spatial topological graph structure that faithfully reflects the force transmission and linkage characteristics between components, thereby providing reliable physical prior constraints for subsequent spatial feature extraction.

(2) An STGNN model integrating GCN and GRU is developed, incorporating one-dimensional convolutional residual connections. By overcoming the limitations of conventional univariate temporal models, this architecture enables the deep joint mining of spatial interactions and long-term temporal dynamic evolutionary characteristics of monitoring signals under complex alternating loads, significantly enhancing feature extraction capacity and prediction accuracy in high-frequency noise environments.

(3) An adaptive anomaly early-warning mechanism is designed based on moving average smoothing of prediction residuals and the 3 $ \sigma $ criterion. Validated by authentic field service data from heavy-haul trains, this mechanism not only effectively reduces the false alarm rate under normal complex working conditions but also acutely and precisely captures variations in spatial linkage features induced by local fatigue cracks, such as knuckle damage, achieving high-reliability early anomaly diagnosis for critical components.

The remainder of this paper is organized as follows: Section 2 introduces the fundamental theories underlying GCN and GRU. Section 3 elaborates on the proposed NMI-STGNN anomaly monitoring methodology, including the construction of spatial correlation graphs, the design of the spatio-temporal joint feature extraction model, and the workflow of the adaptive early-warning mechanism. In Section 4, the prediction performance and anomaly warning capabilities of the proposed method are comprehensively validated and comparatively analyzed using authentic field operation data. Finally, Section 5 concludes the paper.

<!-- PDF_PAGE: 5 -->

## 2. Preliminaries

## 2.1. Graph Convolutional Networks

GCNs represent a sophisticated class of deep learning architectures engineered to operate directly on data structured as graphs [34]. Distinct from conventional CNNs optimized for Euclidean domains, GCNs are specifically designed to capture intricate topological relationships between nodes, as illustrated in Figure 1. The fundamental principle involves a simplified spectral decomposition of the graph Laplacian operator, which facilitates the aggregation and transformation of feature information from a node and its adjacent neighbors. Through the hierarchical stacking of multiple layers, the model can effectively extract high-order spatial representations of the constituent nodes within the network [35].


![figure_002.png](images/figure_002.png)



<div align="center">

Figure 1. Graph convolutional network.

</div>

Prior to the execution of graph convolutions, an adjacency matrix incorporating selfconnections, denoted as $ \widetilde{A} $ , is defined to ensure that a node's intrinsic information is preserved during the neighborhood feature aggregation process:

$$
\tilde {A} = A + I
$$

where A represents the original adjacency matrix and I is the identity matrix.

Subsequently, a symmetrically normalized graph Laplacian matrix is constructed to facilitate information smoothing and spatial scaling within the spectral domain:

$$
\hat {L} = \widetilde {D} ^ {- \frac {1}{2}} \widetilde {A} \widetilde {D} ^ {- \frac {1}{2}}
$$

where $ \widetilde{D} $ is the degree matrix of $ \widetilde{A}. $

Building upon these operators, the forward propagation rule for a GCN layer is defined as follows:

$$
H ^ {(l + 1)} = f _ {\rho} \left(\hat {L} H ^ {(l)} \Gamma^ {(l)}\right)
$$

where $ H^{(l)} $ denotes the node feature matrix of the l-th layer, $ \Gamma^{(l)} $ represents the matrix of trainable weights, and $ f_{\rho}(\cdot) $ signifies the non-linear activation function.

## 2.2. Gated Recurrent Units

The GRU is a significant variant of RNNs, specifically engineered for processing time-series data characterized by long-term dependencies [36]. To alleviate the gradient vanishing problem inherent in standard RNNs, the GRU incorporates a gating mechanism to meticulously regulate the flow of information, as illustrated in Figure 2. Compared to LSTM, the GRU architecture is more streamlined. By consolidating the forget and input

<!-- PDF_PAGE: 6 -->

gates into a single update gate, it effectively reduces the parameter count while preserving the robust capacity for complex temporal modeling.


![figure_003.png](images/figure_003.png)



<div align="center">

Figure 2. Schematic diagram of the internal GRU structure.

</div>

At each time step t, the GRU initially computes two gating signals—the update gate $ u_{t} $ and the reset gate $ r_{t} $ —based on the current input $ x_{t} $ and the hidden state from the previous time step $ h_{t-1} $ :

$$
\left\{ \begin{array}{l} u _ {t} = f _ {s i g m o i d} \left(\omega_ {u} \cdot \left[ h _ {t - 1}, x _ {t} \right] + b _ {u}\right) \\ r _ {t} = f _ {s i g m o i d} \left(\omega_ {r} \cdot \left[ h _ {t - 1}, x _ {t} \right] + b _ {r}\right) \end{array} \right.
$$

Specifically, the update gate $ u_{t} $ determines the proportion of information from the previous state to be retained in the current state, while the reset gate $ r_{t} $ regulates the extent to which the previous state influences the current candidate information.

The state update logic then utilizes the reset gate signal to compute the candidate hidden state $ \widetilde{h}_{t} $ for the current step:

$$
\widetilde {h} _ {t} = f _ {\tanh } \left(\omega_ {h} \cdot \left[ r _ {t} \odot h _ {t - 1}, x _ {t} \right] + b _ {h}\right)
$$

Finally, a linear interpolation between the historical state $ h_{t-1} $ and the candidate state $ \widetilde{h}_{t} $ is performed via the update gate $ u_{t} $ to derive the output state $ h_{t} $ for the current time step:

$$
h _ {t} = \left(1 - u _ {t}\right) \odot h _ {t - 1} + u _ {t} \odot \tilde {h} _ {t}
$$

## 3. Proposed Method

To effectively characterize the intricate spatio-temporal coupling patterns among the sensors within the coupler system, this study proposes an anomaly detection methodology integrating NMI and STGNN. The proposed approach encompasses three pivotal phases: spatial graph construction, joint spatio-temporal feature extraction, and smoothed residualbased early warning.

## 3.1. Spatial Graph Construction via NMI

To address the nonlinear coupling characteristics of coupler sensor data under complex working conditions, this study employs NMI instead of the linear correlation coefficient for association measurement. By quantifying high-order correlations between nodes, the topological adjacency matrix of the GNN is reconstructed to achieve precise modeling of the spatial structural features of the coupler system, as illustrated in Figure 3.

<!-- PDF_PAGE: 7 -->


![figure_004.png](images/figure_004.png)



<div align="center">

Figure 3. Construction of the coupler sensor association matrix and spatial topological graph based on NMI.

</div>

Let X and Y represent the time-series monitoring data from two distinct sensors. Their mutual information $ I ( X, Y ) $ is defined as:

$$
I (X, Y) = \iint p (x, y) \log \frac {p (x , y)}{p (x) p (y)} d x d y
$$

where p(x,y) denotes the joint probability density function of X and Y, while p(x) and p(y) are their respective marginal probability density functions. To eliminate the influence of varying information entropy magnitudes across different sensors on the association measurement, a symmetric normalization is applied to the mutual information:

$$
N M I (X, Y) = \frac {I (X , Y)}{\sqrt {H (X) H (Y)}}
$$

where $ H ( X ) $ and $ H ( Y ) $ represent the information entropy of variables X and Y, respectively. The off-diagonal elements of the calculated NMI matrix are strictly distributed within the interval [0,1], where higher values signify more potent physical coupling between the sensors.

To avert interference from weakly correlated noise during node aggregation, a Top-k sparsification strategy is applied to the fully connected NMI matrix. For each sensor node, only the K neighbors with the highest association degrees are retained in this study, K=5, yielding the final sparse binary adjacency matrix A:

$$
A _ {i j} = \left\{ \begin{array}{l l} 1, N M I \left(X _ {i}, X _ {j}\right) \in T o p - k \left(X _ {i}\right) \\ 0, o t h e r w i s e \end{array} \right.
$$

This adjacency matrix A explicitly characterizes the linkage topological relationships within the internal mechanical structure of the coupler, providing structural support for subsequent spatial feature extraction.

This study adopts NMI to construct the graph structure, whose core logic is to mine the dynamic correlations hidden behind sensor signals through statistical methods, endowing the data-driven topological structure with clear physical significance. During the service of the heavy-haul train coupler and draft gear system, longitudinal impact is transmitted through core components such as coupler tongues, coupler bodies, and draft gears. This mechanical interaction, affected by mechanical clearance, frictional contact, and nonlinear damping of the draft gear, exhibits significant nonlinear characteristics. Compared with traditional linear correlation coefficients, NMI can more accurately capture such complex high-order coupling relationships, where high mutual information values directly corre-

<!-- PDF_PAGE: 8 -->

spond to the main stress propagation paths in the system or mechanical components with close physical connections. The sparse adjacency matrix generated by retaining strong correlation connections essentially constructs a virtual framework reflecting the mechanical topology of the coupler system for the model. In the subsequent spatial feature aggregation process, graph convolution operations can simulate the diffusion process of mechanical energy in the physical structure, ensuring that the high-dimensional features extracted by the model are always constrained by the underlying mechanical connection logic. This design not only improves the model's sensitivity to early faint damage but also establishes a strong correlation between the originally black-box deep learning process and the actual force-bearing behavior of the system.

## 3.2. Spatio-Temporal Graph Neural Network Model

Building upon the reconstructed spatial topology, this study engineered an STGNN model comprising GCN, GRU, and 1D-CNN residual connections to facilitate the joint mining of spatio-temporal features from equipment states, as illustrated in Figure 4. The specific architectural parameters of the model are summarized in Table 1. At any time step t within the sliding window, the GCN leverages the adjacency matrix A to aggregate features from sensor nodes and their respective neighbors, enabling the interaction of spatial physical information. The forward propagation process of a single GCN layer is formulated as:

$$
H ^ {(l + 1)} = f _ {r e l u} \left(A H ^ {(l)} W ^ {(l)}\right)
$$

where $ H^{(l)} $ denotes the feature representation of nodes in the l-th layer, $ W^{(l)} $ is the trainable weight matrix for the current layer, and $ f_{relu}(\cdot) $ represents the ReLU activation function. Through matrix multiplication, the model implicitly captures the mechanical response transmission characteristics among adjacent sensors.


![figure_005.png](images/figure_005.png)



<div align="center">

Figure 4. Overall architecture of the NMI-STGNN model.

</div>

<div align="center">

Table 1. The parameters of the NMI-STGNN in this article.

</div>

<table border="1"><tr><td>Network</td><td>Layer</td><td>Filter Number/Kernels Size/Padding</td><td>Output Size</td></tr><tr><td>Input layer</td><td>Raw temporal signal</td><td>1/60/12</td><td>BS×60×12</td></tr><tr><td>Graph Construction</td><td>NMI, Top-K</td><td>12×12/K=5</td><td>12×12</td></tr><tr><td>Spatio-Temporal Block 1</td><td>GCN, GRU, ReLU, Residual</td><td>GCN:32-1;GRU:384-384</td><td>BS×60×12×32</td></tr><tr><td>Spatio-Temporal Block 2</td><td>GCN, GRU, ReLU, Residual</td><td>GCN:32-32;GRU:384-384</td><td>BS×60×12×32</td></tr><tr><td>Fusion layer</td><td>Concat,1×1Conv,ReLU</td><td>33-64-1</td><td>BS×12</td></tr><tr><td>Training config</td><td>MSE Loss,Adam Optimizer</td><td>LR:1×10-4;BS:64;Epochs:100</td><td>BS×12</td></tr><tr><td>Anomaly Detection</td><td>3σ Threshold,Sliding Smoothing</td><td>Win:60</td><td>BS×1</td></tr></table>

BS: Batch Size; LR: Learning Rate; Conv: Convolution; ReLU: Rectified Linear Unit.

<!-- PDF_PAGE: 9 -->

To characterize the dynamic degradation patterns of equipment states over time, the spatial feature sequences extracted by the GCN are fed into the GRU network. The GRU models long-term temporal dependencies within the sliding window—set to a length of 60 in this study—via its update and reset gate mechanisms. Simultaneously, to mitigate feature degradation and gradient vanishing inherent in deep architectures, 1D-CNN residual skip connections are integrated into the spatio-temporal blocks. The fusion output mechanism of the entire spatio-temporal block is described as:

$$
f _ {o u t} = f _ {r e l u} \left(f _ {G R U} \left(f _ {G C N} (X, A)\right) + f _ {c o n v 1 d} (X)\right)
$$

This configuration preserves fine-grained temporal fluctuations from the raw sensor data while extracting high-order spatio-temporal coupling features.

The primary model consists of two stacked spatio-temporal blocks. The architecture concatenates the features from the final time step of the original input with the high-level spatio-temporal features, followed by two 1D-CNN layers for dimensionality reduction mapping to output the predicted values $ \hat{\gamma} $ for each sensor at the next time step. The model is trained using MSE as the loss function:

$$
L _ {M S E} = \frac {1}{B \cdot N} \sum_ {B} ^ {b = 1} \sum_ {N} ^ {i = 1} \left(Y _ {b, i} - \hat {Y} _ {b, i}\right) ^ {2}
$$

where B denotes the batch size and N represents the number of sensor nodes.

## 3.3. Adaptive Early-Warning Mechanism Based on Smoothed Residuals and the 3 $ \sigma $ Criterion

During the training phase, the model exclusively captures the data distribution characteristic of normal working conditions. In the monitoring stage, when structural anomalies such as fatigue cracks or component loosening occur within the coupler system, the resultant physical responses diverge from the established normal linkage patterns, leading to a pronounced escalation in prediction residuals.

The composite residual intensity at time t is quantified as the Root Mean Square Error (RMSE) of the prediction deviations across all core sensors:

$$
E _ {t} = \sqrt {\frac {1}{N} \sum_ {N} ^ {i = 1} \left(Y _ {i , t} - \hat {Y} _ {i , t}\right) ^ {2}}
$$

where $ Y_{i,t} $ and $ \hat{Y}_{i,t} $ represent the actual observed values and the model-predicted values for sensor i at time t, respectively.

Considering the intricacies of industrial field environments, sensor signals are frequently susceptible to stochastic impulse noise, which may precipitate spurious alarms. To enhance reliability, a central moving average algorithm is implemented to refine the raw residual sequence:

$$
S _ {t} = \frac {1}{W _ {\mathrm {s m o o t h}}} \sum_ {W _ {\mathrm {s m o o t h}} / 2} ^ {j = - W _ {\mathrm {s m o o t h}} / 2} E _ {t + j}
$$

where $ S_{t} $ denotes the smoothed residual intensity and $ W_{\mathrm{smooth}} $ signifies the smoothing window size, which is set to 60 in this study.

Subsequently, an adaptive early-warning threshold Th is formulated based on the 3 $ \sigma $ criterion, leveraging the statistical mean u and standard deviation $ \sigma $ derived from the smoothed residuals within the offline training set:

$$
T h = \mu + 3 \sigma
$$

<!-- PDF_PAGE: 10 -->

In the online monitoring phase, a deviation is identified whenever the calculated $ S_{t} $ surpasses the predefined threshold Th, thereby triggering an automated anomaly alert. This mechanism effectively synergizes detection sensitivity with robust noise suppression.

## 4. Experimental Validation and Analysis

To evaluate the efficacy of the proposed methodology, empirical data analysis was performed by leveraging a heavy-haul train condition monitoring project. Car B of the heavy-haul train is illustrated in Figure 5.


![figure_006.png](images/figure_006.png)



<div align="center">

Figure 5. Car B of the heavy-haul train.

</div>

## 4.1. Sensor Layout and Dataset Partitioning

By integrating the mechanical response mechanisms of the coupler and draft gear system with signal quality requirements, this study selected 30 pivotal sensor points on Car B of the heavy-haul train to construct high-dimensional feature vectors. The physical distribution of these measurement points is illustrated in Figure 6 and detailed in Table 2. The monitoring locations encompass critical components, including strain gauges on the front and rear coupler bodies, the knuckles, pin holes, and concave platforms within the force transmission hubs, as well as the primary and secondary springs in the bogie suspension zones. Furthermore, draw-wire displacement sensors were deployed to characterize the relative longitudinal movement of the system. Collectively, these sensors constitute a spatial monitoring network governed by robust topological constraints.


![figure_007.png](images/figure_007.png)



<div align="center">

(a) Left bogie of Car B

</div>


![figure_008.png](images/figure_008.png)




![figure_009.png](images/figure_009.png)



<div align="center">

(c) Right bogie of Car B

</div>

<div align="center">

(b) Front coupler of Car B

</div>


![figure_010.png](images/figure_010.png)



<div align="center">

(d) Rear coupler of Car B

</div>

<div align="center">

Figure 6. Schematic illustration of the sensor layout for the coupler and draft gear system on Car B of the heavy-haul train.

</div>

<!-- PDF_PAGE: 11 -->

<div align="center">

Table 2. Description of the 30 sensor measurement points utilized in the experiment.

</div>

<table border="1"><tr><td>Sensor ID</td><td>Measurement Point Name</td><td>Sensor ID</td><td>Measurement Point Name</td></tr><tr><td>1</td><td>Rear coupler body 1</td><td>16</td><td>Front concave platform 1</td></tr><tr><td>2</td><td>Rear coupler body 5</td><td>17</td><td>Front concave platform 5</td></tr><tr><td>3</td><td>Rear coupler body 9</td><td>18</td><td>Front concave platform 9</td></tr><tr><td>4</td><td>Rear pin hole 1</td><td>19</td><td>Front pin hole 5</td></tr><tr><td>5</td><td>Rear pin hole 5</td><td>20</td><td>Front pin hole 9</td></tr><tr><td>6</td><td>Rear pin hole 9</td><td>21</td><td>Front knuckle 1</td></tr><tr><td>7</td><td>Rear-left primary suspension 1</td><td>22</td><td>Front knuckle 5</td></tr><tr><td>8</td><td>Rear-left primary suspension 5</td><td>23</td><td>Front knuckle 9</td></tr><tr><td>9</td><td>Rear-right primary suspension 1</td><td>24</td><td>Front coupler shank 1</td></tr><tr><td>10</td><td>Rear-right primary suspension 5</td><td>25</td><td>Front coupler shank 5</td></tr><tr><td>11</td><td>Rear-left secondary suspension 1</td><td>26</td><td>Front coupler shank 9</td></tr><tr><td>12</td><td>Rear-left secondary suspension 5</td><td>27</td><td>Draw-wire displacement 2</td></tr><tr><td>13</td><td>Rear-left secondary suspension 9</td><td>28</td><td>Rear-right secondary suspension 1</td></tr><tr><td>14</td><td>Rear knuckle 1</td><td>29</td><td>Rear-right secondary suspension 5</td></tr><tr><td>15</td><td>Rear knuckle 5</td><td>30</td><td>Rear-right secondary suspension 9</td></tr></table>

The experimental dataset was derived from authentic online service records. Specifically, continuous data recorded from 3 December 2025 to 6 January 2026, during which the coupler remained in a healthy operational state, were utilized to establish the normal linkage baseline. The data used for training, normalization, and validation was derived from real-world sensor readings collected during the operational service of the heavy-haul train. Raw data underwent preprocessing to handle missing values and applied Z-score normalization to eliminate numerical disparities arising from the different physical dimensions of the sensors. The dataset was then partitioned, with 90% used for training and the remaining 10% used for testing. This approach facilitates a rigorous evaluation of the model's predictive accuracy and generalization performance on normal operational data.

In addition to the training and test sets, a small portion, 10%, of the training data was further reserved as a validation set. This validation set was used during the training process to monitor the model's performance and ensure it was not overfitting to the training data. The loss curve on the validation set was tracked alongside the training loss to evaluate the model's generalization ability. It is important to note that the introduction of this validation set does not affect the original 90% training and 10% test set split; it was simply used as an additional tool for model tuning and performance evaluation.

Due to the complexity of the field working environment, the raw data exhibit localized missing values and timestamp discontinuities. To ensure the quality and physical continuity of the input data, linear interpolation was employed to fill sporadic null values, and Z-score normalization was applied to eliminate numerical disparities arising from different physical dimensions. Addressing the discontinuities caused by train stops or communication interruptions, a time interval threshold of 300 s was established to segment the original time series into multiple continuous data fragments. Subsequently, within each continuous segment, a sliding window containing 60 time steps was extracted at a fixed step size as the input feature, with the data at the immediate subsequent time step serving as the prediction target. This processing mechanism effectively prevents erroneous concatenation across discontinuous intervals, thereby constructing spatio-temporal sample sequences that conform to actual physical evolutionary laws.

In this study, the experimental data was aligned with the onboard LKJ data, ensuring accurate synchronization of sensor data with the operational timeline. This allows us to track both the train route and the corresponding load information during the experiment, which is crucial for obtaining reliable wear data from the system components. We utilized

<!-- PDF_PAGE: 12 -->

fiber Bragg grating (FBG) strain sensors for data collection. A total of 38 sensor measurement points were deployed across the single coupler. The system operated at a sampling frequency of 100 Hz. Each sensor point transmitted 4-byte wavelength data, and after quantization and calculation, the real-time output data volume was approximately 15,200 bytes (14.84 KB/s) per second. The data transmission and storage load are manageable, ensuring the system's operational feasibility.

Regarding the selection of sensor points, we carefully chose 30 pivotal measurement locations based on their spatial coupling significance, as determined by the NMI-based sensor association matrix. The current configuration of 30 sensors strikes an optimal balance between sensor coverage and computational efficiency. While future work could investigate the impact of varying the number or distribution of sensors, the present configuration ensures high model accuracy without unnecessary complexity. The dimensionality reduction process, guided by NMI, inherently filters out weakly correlated or redundant sensors, focusing on those that provide the most meaningful contributions to the model's performance.

To precisely extract the spatial physical topology of the coupler and draft gear system while eliminating weakly correlated redundant noise, NMI was utilized to quantify the nonlinear coupling intensity among the 30 initial sensor points. The global sensor association matrix calculated based on the healthy training set is illustrated in Figure 7.


![figure_011.png](images/figure_011.png)



<div align="center">

Figure 7. Heatmap of the spatial nonlinear coupling characteristics among sensors.

</div>

Figure 7 illustrates the global NMI-based association matrix constructed from all 30 sensors under healthy operating conditions. Each element in this matrix represents the normalized mutual information between a pair of sensors, where higher values indicate stronger nonlinear coupling and closer physical interaction between the corresponding measurement points. Therefore, this matrix can be interpreted as a quantitative representation of the overall spatial correlation structure and mechanical linkage characteristics within the coupler and draft gear system.

Owing to the force transmission characteristics of the internal mechanical structure of the coupler, sensors located within the same rigid transmission hub or adjacent suspension zones exhibit potent nonlinear synergistic responses, whereas the correlations between distant sensors remain relatively weak.

To quantitatively evaluate the contribution of each sensor to the overall spatial coupling structure, the cumulative association weight of each node was calculated by summing

<!-- PDF_PAGE: 13 -->

its NMI values with all other sensor nodes in the global association matrix. Sensors with higher cumulative association degrees were considered to play a more dominant role in reflecting the principal mechanical transmission paths and critical physical interactions within the coupler system.

Based on the global association matrix shown in Figure 7, this cumulative weighting process effectively identifies the most representative sensors in terms of global coupling significance. Accordingly, the dimensionality reduction from 30 sensors to 12 core sensors is directly derived from the information contained in Figure 7.

To enhance the efficiency of spatial feature aggregation and the robustness against noise, the dimensionality was reduced based on the sum of global association weights for each node. Ultimately, the 12 core monitoring variables with the highest cumulative association degrees were extracted, and their refined spatial association matrix was reconstructed, as depicted in Figure 8 and detailed in Table 3.


![figure_012.png](images/figure_012.png)



<div align="center">

Figure 8. Normalized association matrix of the 12 core sensors.

</div>

<div align="center">

Table 3. The 12 most representative sensors selected via NMI.

</div>

<table border="1"><tr><td>Sensor ID</td><td>Measurement Point Name</td><td>Sensor ID</td><td>Measurement Point Name</td></tr><tr><td>14</td><td>Rear knuckle 1</td><td>26</td><td>Front coupler shank 9</td></tr><tr><td>21</td><td>Front knuckle 1</td><td>22</td><td>Front knuckle 5</td></tr><tr><td>15</td><td>Rear knuckle 5</td><td>20</td><td>Front pin hole 9</td></tr><tr><td>19</td><td>Front pin hole 5</td><td>23</td><td>Front knuckle 9</td></tr><tr><td>9</td><td>Rear-right primary suspension 1</td><td>18</td><td>Front concave platform 9</td></tr><tr><td>4</td><td>Rear pin hole 1</td><td>6</td><td>Rear pin hole 9</td></tr></table>

Figure 8 presents the refined NMI association matrix constructed using the selected 12 sensors, which can be regarded as a subgraph extracted from the global matrix in Figure 7. Compared with Figure 7, this reduced matrix preserves the most critical spatial

<!-- PDF_PAGE: 14 -->

coupling relationships while eliminating weakly correlated connections, thereby forming a compact yet physically meaningful topology for subsequent graph convolution operations.

It should be emphasized that Figure 8 is not a confusion matrix for classification evaluation, but a normalized mutual information (NMI)-based association matrix describing the nonlinear coupling relationships among the selected sensors. The diagonal elements are equal to 1 because each sensor is perfectly correlated with itself after normalization, while the off-diagonal elements represent the strength of nonlinear interactions between different sensor pairs. Therefore, the matrix should be interpreted as a spatial correlation structure rather than a classification result.

This selection strategy effectively retains the most informative and physically meaningful sensors while filtering out weakly correlated and redundant variables, thereby improving computational efficiency and enhancing the robustness of the proposed model. These 12 nodes constitute the fixed graph topology for spatial convolution within the NMI-STGNN.

## 4.2. Condition Monitoring Based on Normal Service Data

Once the graph structure was finalized, the healthy spatio-temporal samples were utilized for model training. The Adam optimizer was employed with a total training duration of 100 epochs. The resulting MSE convergence curve is shown in Figure 9. Both the training loss and validation loss curves are depicted to provide a more comprehensive evaluation of the model's performance. During the initial training phase, the training loss decreased precipitously, while the validation loss also showed a consistent decrease, stabilizing asymptotically around 0.004699. This indicates that the model has sufficiently characterized the dynamic evolutionary patterns under normal working conditions. The comparison between both curves demonstrates the model's ability to generalize well without overfitting, as the validation loss stabilizes similarly to the training loss.


![figure_013.png](images/figure_013.png)



<div align="center">

Figure 9. Training and validation convergence curves of the proposed model.

</div>

To evaluate the effectiveness of the model in learning the normal linkage laws of the coupler system, forward predictions were executed on the test set, followed by an inverse-standardization process. The fitting performance between the actual physical measurements and the predicted values for selected core sensor nodes is presented in Figure 10.

<!-- PDF_PAGE: 15 -->


![figure_014.png](images/figure_014.png)



<div align="center">

Figure 10. Comparison between actual physical responses and predicted results for core sensor nodes.

</div>

Under the complex and volatile working conditions of heavy-haul trains, the raw signals captured by sensor nodes exhibit high-frequency and strenuous nonlinear fluctuations. Nevertheless, the predicted signals generated by the model track the trajectories of the actual values faithfully across multiple temporal scales. High fitting precision is maintained both in stable regions with low-frequency trends and during high-frequency transients induced by alternating load impacts. These results demonstrate that the proposed STGNN effectively decouples and internalizes the robust physical topological constraints and dynamic latency characteristics inherent in the internal components of the coupler during normal service, thereby laying a solid groundwork for establishing a reliable anomaly residual baseline.

Upon confirming the high-precision state prediction capability, the model was deployed on the complete test set, which included unknown condition evolutions and potential physical degradation, to verify its anomaly early-warning performance. The model first calculates the RMSE of the test sequences. To mitigate the interference of stochastic high-frequency noise in the field on the warning mechanism, a central moving average algorithm was introduced to smooth and denoise the raw residuals. Subsequently, the early-warning threshold was adaptively established according to the 3 $ \sigma $ criterion, utilizing the mean and standard deviation derived from the data distribution of the healthy training set.

As illustrated in Figure 11, the solid blue line represents the smoothed system composite residual intensity, while the red dashed line signifies the 3 $ \sigma $ healthy baseline established offline. During the initial monitoring period, the system residuals fluctuate steadily below the threshold, indicating that the mechanical responses of the coupler components conform to the normal spatial linkage laws and no false alarms were triggered.

## 4.3. Comparative Experiments

To further verify the superiority of the proposed model under complex working conditions, a classic CNN-LSTM network from the field of time-series prediction was selected as the baseline model for comparative analysis.

CNN-LSTM is selected as the baseline model mainly because this architecture represents a classic paradigm for modeling spatio-temporal features in multi-dimensional sensor signals. Specifically, CNN is capable of extracting local spatial distribution patterns among different sensors, while LSTM is employed to capture the long-term temporal dependencies embedded in sequential monitoring data. By comparison with this conventional spatio-temporal modeling approach, the performance advantages of the graph

<!-- PDF_PAGE: 16 -->

structure proposed in this study can be more intuitively validated in characterizing complex mechanical topological relationships and processing data defined on non-Euclidean spaces.


![figure_015.png](images/figure_015.png)



<div align="center">

Figure 11. Anomaly early-warning results of the coupler and draft gear system based on smoothed residuals and the 3 $ \sigma $ criterion.

</div>

Regarding parameter settings, this baseline model maintained strictly identical input specifications to the methodology proposed in this study. The specific architecture included a single 1D-CNN layer with 32 output channels and a kernel size of 3, utilizing same padding to preserve complete temporal information. This was followed by two LSTM layers with a hidden dimension of 32 and a dropout rate of 0.3 to prevent overfitting, with the final prediction results mapped via a fully connected layer. The training phase similarly employed MSE as the loss function, utilizing the Adam optimizer with a learning rate of 0.001 and a batch size of 64 over 100 epochs.

The comparison between the actual responses of core sensor nodes and the predicted results of the CNN-LSTM model is illustrated in Figure 12. It can be observed that while CNN-LSTM possesses a degree of temporal modeling capability and can track the overall low-frequency trends of the signals, it exhibits significant fitting bias and lag when encountering high-frequency nonlinear transients induced by heavy-haul alternating impacts. This deficiency stems from its lack of effective perception regarding the spatial physical topology and synergistic constraints among the sensors.


![figure_016.png](images/figure_016.png)



<div align="center">

Monitoring time

</div>

<div align="center">

Figure 12. Comparison between actual physical responses and predicted results for core sensor nodes using the CNN-LSTM model.

</div>

<!-- PDF_PAGE: 17 -->

The aforementioned inaccuracies in prediction directly weaken the reliability of the subsequent healthy baseline construction. The anomaly early-warning results for the CNNLSTM model, presented in Figure 13, indicate that the intense fluctuations in prediction residuals under normal conditions lead to an elevated alarm threshold calculated via the 3 $ \sigma $ criterion, which significantly reduces the noise robustness of the system. During the actual monitoring phase, the residual curve of this model is highly unstable within healthy intervals and is susceptible to triggering false alarms due to local high-frequency signal interference. For instance, a prominent spurious alarm was generated by this model during a normal service period at 16:00 on 5 January 2026.


![figure_017.png](images/figure_017.png)



<div align="center">

Figure 13. Anomaly early-warning results of the coupler and draft gear system based on smoothed residuals and the 3 $ \sigma $ criterion using the CNN-LSTM model.

</div>

These comparative results demonstrate that relying solely on pure sequence models makes it difficult to fully decouple the complex physical mechanisms of the heavy-haul train coupler and draft gear system. The introduction of NMI and STGNN to jointly mine the spatial topology and temporal evolutionary characteristics of multi-dimensional sensor signals is significantly necessary for enhancing the state-tracking accuracy and warning robustness of the system.

To quantitatively evaluate the predictive performance of the models, this study selected MAE, RMSE, and $ R^{2} $ as the primary evaluation metrics. Among these, MAE is utilized to reflect the physical magnitude of the deviation between predicted values and actual observations. RMSE exhibits higher sensitivity to significant outliers within the prediction sequence and is employed to assess the stability of the model. $ R^{2} $ measures the goodness of fit regarding data fluctuations, where a value closer to 1 indicates a more profound capacity of the model to capture complex nonlinear features:

$$
M A E = \frac {1}{n} \sum_ {i = 1} ^ {n} \left| y _ {i} - \hat {y} _ {i} \right|
$$

$$
R M S E = \sqrt {\frac {1}{n} \sum_ {i = 1} ^ {n} \left(y _ {i} - \hat {y} _ {i}\right) ^ {2}}
$$

$$
R ^ {2} = 1 - \frac {\sum \left(y _ {i} - \hat {y} _ {i}\right) ^ {2}}{\sum \left(y _ {i} - \bar {y}\right) ^ {2}}
$$

It should be noted that both MAE and RMSE retain the same physical units as the original sensor measurements after inverse normalization. In this study, since the monitored signals are collected from FBG strain sensors, the units of MAE and RMSE are expressed in

<!-- PDF_PAGE: 18 -->

macrostrain $ (\mu \varepsilon) $ , thereby directly reflecting the magnitude of prediction errors in terms of actual mechanical deformation.

Detailed performance data are presented in Table 4.

<div align="center">

Table 4. Quantitative comparison of predictive performance between the proposed methodology and CNN-LSTM for core sensors.

</div>

<table border="1"><tr><td>Measurement Point Name</td><td>Model Type</td><td>MAE(με)</td><td>RMSE(με)</td><td>R2(-)</td></tr><tr><td rowspan="2">Rear knuckle 5</td><td>NMI-STGNN</td><td>8.8274</td><td>14.1751</td><td>0.9699</td></tr><tr><td>CNN-LSTM</td><td>13.9001</td><td>13.9001</td><td>0.9379</td></tr><tr><td rowspan="2">Front knuckle 5</td><td>NMI-STGNN</td><td>6.6304</td><td>9.7280</td><td>0.9838</td></tr><tr><td>CNN-LSTM</td><td>10.0819</td><td>14.3601</td><td>0.9647</td></tr><tr><td rowspan="2">Rear-right primary suspension 1</td><td>NMI-STGNN</td><td>8.6493</td><td>10.8754</td><td>0.9873</td></tr><tr><td>CNN-LSTM</td><td>16.1557</td><td>25.3166</td><td>0.9313</td></tr><tr><td rowspan="2">Front pin hole 5</td><td>NMI-STGNN</td><td>7.7411</td><td>10.4974</td><td>0.9875</td></tr><tr><td>CNN-LSTM</td><td>22.7705</td><td>29.3084</td><td>0.9023</td></tr></table>

The NMI-STGNN proposed in this study demonstrates significantly superior predictive accuracy compared to the baseline CNN-LSTM across the four core sensor nodes. As detailed in Table 4, both MAE and RMSE for NMI-STGNN exhibit substantial decreases across all measurement points. Notably, at the Front pin hole 5 measurement point, which is significantly influenced by complex working conditions, the proposed method reduces the MAE from 22.7705 to 7.7411, representing a remarkable error reduction rate of 66.0%. Furthermore, the $ R^{2} $ metrics for all core nodes remain stable above 0.96, reaching a maximum of 0.9875, which demonstrates an exceptional capacity for nonlinear feature fitting and dynamic tracking. This significant enhancement validates the superiority of the proposed approach in extracting spatial interactions and temporal dynamic evolutionary characteristics of equipment states. By reconstructing the spatial physical topology of the coupler system via NMI, the model establishes a more precise and noise-robust health monitoring baseline compared to pure sequence models when processing alternating load impacts from heavy-haul trains.

## 4.4. Monitoring Based on Abnormal Operational Data

To verify the recognition capability of the proposed methodology in real mechanical degradation scenarios, this section conducts experiments using empirical data collected from 3 December to 18 December 2025. Building upon the original 30 sensors, the Rear knuckle 9 measurement point was added to construct a 31-dimensional high-dimensional feature vector. Field records indicate that due to abnormal alternating impact loads and localized stress concentration, this measurement point experienced a significant strain surge around 05:00 on 18 December 2025.

The experimental data were strictly partitioned chronologically, with the initial 95% of healthy samples used to establish the system baseline and the remaining 5% covering the abnormal evolution period reserved as the test set. The prediction comparison results for core measurement points are presented in Figure 14.

During the initial period of the test set where no anomalies occurred, the actual signals of each node maintained a high degree of fit with the predicted signals, indicating that the model precisely internalized the normal spatio-temporal evolutionary laws of the coupler system. However, near 05:00 on 18 December the abnormal deformation of the local physical structure disrupted the original spatial topological constraints within the coupler. Consequently, the actual monitoring values of affected points, such as Rear knuckle 9, exhibited strenuous nonlinear deviations. At this juncture, the model continued to perform inference based on spatial linkage weights derived from the healthy state, leading to a

<!-- PDF_PAGE: 19 -->

pronounced residual separation between the predicted and actual values. This feature separation serves as the core criterion for identifying early equipment faults.


![figure_018.png](images/figure_018.png)



<div align="center">

Figure 14. Comparison between actual physical responses and predicted results for core sensor nodes during the abnormal evolution phase.

</div>

To quantitatively evaluate the health status of the entire coupler system and filter out local high-frequency noise interference, the model performs a moving average smoothing of the RMSE residuals of the test set. The adaptive early-warning threshold is established using the 3 $ \sigma $ criterion, based on the residual distribution of the training set. This threshold represents the upper bound of the normal operational range, with any residual exceeding this value indicating an anomaly. The final system-level anomaly monitoring results, as shown in Figure 15, are based on this threshold.


![figure_019.png](images/figure_019.png)



<div align="center">

Figure 15. System anomaly early-warning results based on smoothed residuals and the 3 $ \sigma $ criterion under real working conditions.

</div>

During the early phase of the test set, the system composite residual intensity fluctuated steadily below the 3 $ \sigma $ warning baseline, and no false alarms were triggered. As time progressed to approximately 05:00 on 18 December, the residual curve exhibited two sharp mutation peaks that substantially surpassed the warning baseline, triggering an automated system alert. This alarm interval aligns perfectly with the actual physical timestamp when the rear knuckle experienced a severe abnormal response in the field. These comparative experiments sufficiently demonstrate that the proposed methodology can not only sensitively capture global spatial linkage failures caused by single-point physical degradation

<!-- PDF_PAGE: 20 -->

but also effectively resist noise interference under complex conditions, achieving intelligent state early-warning with high sensitivity and low false alarm rates for heavy-haul train coupler systems.

Figures 16 and 17 present the system-level anomaly early-warning results of the CNN-LSTM baseline model under real working conditions. As shown in Figure 16, the actual physical response begins to exhibit severe abnormal deviation precisely at 05:00 on 18 December. However, the predicted values generated by the CNN-LSTM completely fail to capture this mutation, remaining stubbornly flat. Consequently, as depicted in Figure 17, the system's residual intensity does not cross the warning baseline to trigger an alarm until approximately 06:30. This significant delay of an hour and a half poses a severe safety risk in practical heavy-haul train operations. The poor performance of the CNN-LSTM model can be attributed to two main factors. First, without the NMI-based feature selection to isolate core sensors, the model processes all variables indiscriminately, leading to severe information redundancy and noise interference that dilute critical anomaly signals. Second, as a pure sequence model, CNN-LSTM inherently lacks the capacity to extract spatial synergistic constraints among multi-dimensional sensors, rendering it extremely insensitive to early, sudden fault mutations.


![figure_020.png](images/figure_020.png)



<div align="center">

Figure 16. Comparison between actual physical responses and predicted results for core sensor nodes during the abnormal evolution phase using CNN-LSTM.

</div>


![figure_021.png](images/figure_021.png)



<div align="center">

Figure 17. System anomaly early-warning results based on smoothed residuals and the 3 $ \sigma $ criterion under real working conditions using CNN-LSTM.

</div>

On 23 December 2025, field inspectors performed a magnetic particle inspection on the knuckle based on the system warning information, and Figure 18 displays the physical images from the inspection process. The inspection conclusions confirmed that

<!-- PDF_PAGE: 21 -->

the initiation site of the fatigue crack discovered during the process was highly consistent with the location of the 9th sensor point, where the strain data had previously exhibited severe deviation in the monitoring system. This precise spatial correspondence indicates that the substantial damage to the internal physical structure of the knuckle disrupted the local stress balance, serving as the direct cause of the nonlinear mutations in the sensor features. This field validation via magnetic particle inspection not only substantiates the acute capability of the proposed model to capture early weak crack signals but also provides a reliable physical criterion and closed-loop data support for the intelligent operation and maintenance of coupler systems.


![figure_022.png](images/figure_022.png)



<div align="center">

Figure 18. Physical photograph of the magnetic particle inspection of the knuckle on 23 December 2025.

</div>

## 5. Conclusions

To address the safety monitoring requirements of heavy-haul train coupler and draft gear systems under complex alternating loads, this study proposes an anomaly monitoring methodology integrating NMI and STGNN. The main conclusions are summarized as follows:

(1) NMI was introduced to effectively quantify the nonlinear physical coupling intensity among multi-source sensors. By sparsifying the fully connected matrix, interference from weakly correlated noise was successfully eliminated, and a spatial physical topology reflecting the internal mechanical linkage laws of the coupler was reconstructed, providing accurate structural support for spatial feature extraction.

(2) A deep learning framework fusing GCN, GRU and 1D-CNN with residual connections is constructed. The model enables collaborative mining of spatial correlations and temporal evolution patterns in monitoring signals, thereby effectively capturing the complex physical topology constraints and dynamic time-lag characteristics inherent in the coupler and draft gear system during regular operation.

(3) An early-warning mechanism based on predictive residual smoothing and the adaptive 3 $ \sigma $ criterion was established. By applying moving average denoising to the residual sequence, the anti-interference capability of the system in complex industrial environments was significantly enhanced, achieving an effective balance between warning sensitivity and noise robustness.

(4) Field data validation indicates that the NMI-STGNN model achieves significantly higher prediction accuracy than the traditional CNN-LSTM model. For all key sensor nodes, the MAE and RMSE are notably reduced, while the coefficient of determination

<!-- PDF_PAGE: 22 -->

$ \mathrm{R}^{2} $ stably maintains above 0.96, which effectively suppresses false alarms under normal operating conditions.

(5) In real fault cases, the anomalous nodes identified by the model highly coincide with the fatigue crack initiation sites discovered via magnetic particle inspection, confirming the acute capability of this method to capture early faint anomaly signals. This research provides a reliable, physically consistent, data-driven solution for the real-time monitoring and condition-based maintenance of critical heavy-haul train components.

Author Contributions: Conceptualization, Z.Z. and Z.J.; methodology, L.Z.; software, J.W.; validation, Q.X., J.W. and L.Z.; formal analysis, Z.J.; data curation, Z.J.; writing—original draft preparation, Z.Z.; writing—review and editing, Z.J.; visualization, Q.X.; supervision, L.Z.; project administration, Z.Z.; funding acquisition, Z.Z. All authors have read and agreed to the published version of the manuscript.

Funding: This research was supported by the Open Collaboration and Innovation Fund Project of the Wheel-Rail Interaction Laboratory at the National Engineering Research Center for High-Speed Rail and Urban Rail Transit Systems, A Study on the Mechanism of Abnormal Wheel Wear During Deceleration via Combined Electric and Air Braking on Extra-Long Steep Gradients and Train Operating Strategies (Grant No. 2024YJ131).

Institutional Review Board Statement: Not applicable.

Informed Consent Statement: Not applicable.

Data Availability Statement: The dataset is available on request from the authors.

Acknowledgments: The authors would like to thank the editor and referees for their valuable comments.

Conflicts of Interest: Authors Zhirong Zhao and Zhentian Jiang were employed by the company Rolling Stock Branch, CHN Energy Shuohuang Railway Development Co., Ltd. The remaining authors declare that the research was conducted in the absence of any commercial or financial relationships that could be construed as a potential conflict of interest.

## References

1. Hu, X.; Yang, Y.; Wei, M.; Chen, Q.; Zhou, Z.; Wang, K. Research on Abnormal Wear Mechanism of the Coupler System in Heavy-Haul Trains. Veh. Syst. Dyn. 2024, 63, 1568-1596. [CrossRef]

2. Elele, U.; Nekahi, A.; Arshad, A.; Fofana, I. Towards Online Ageing Detection in Transformer Oil: A Review. Sensors 2022, 22, 7923. [CrossRef] [PubMed]

3. de Azevedo, H.D.M.; Araújo, A.M.; Bouchonneau, N. A Review of Wind Turbine Bearing Condition Monitoring: State of the Art and Challenges. Renew. Sustain. Energy Rev. 2016, 56, 368-379. [CrossRef]

4. Wang, C.; Zhu, T.; Yang, B.; Yin, M.; Xiao, S.; Yang, G. Remaining Useful Life Prediction Framework for Crack Propagation with a Case Study of Railway Heavy Duty Coupler Condition Monitoring. Reliab. Eng. Syst. Saf. 2023, 230, 108915. [CrossRef]

5. Olivier, B.; Verlinden, O.; Kouroussis, G. A Vehicle/Track/Soil Model Using Co-Simulation between Multibody Dynamics and Finite Element Analysis. Int. J. Rail Transp. 2019, 8, 135-158. [CrossRef]

6. Zhang, Z.; Chu, G.; Lv, K.; Wang, F.; Zhang, Y. Experimental Investigation on the Dynamic Performance of a Heavy Haul Locomotive and Its Coupler and Buffer System under Longitudinal Forces. Proc. Inst. Mech. Eng. Part F J. Rail Rapid Transit 2025, 240, 465-476. [CrossRef]

7. Ren, X.; Wu, S.; Xing, H.; Fang, X.; Ao, N.; Zhu, T.; Li, Q.; Kang, G. Fracture Mechanics Based Residual Life Prediction of Railway Heavy Coupler with Measured Load Spectrum. Int. J. Fract. 2022, 234, 313-327. [CrossRef]

8. Dumitriu, M. Condition Monitoring of the Dampers in the Railway Vehicle Suspension Based on the Vibrations Response Analysis of the Bogie. Sensors 2022, 22, 3290. [CrossRef] [PubMed]

9. Li, X.; Liu, X.; Yue, C.; Wang, L.; Liang, S.Y. Data-Model Linkage Prediction of Tool Remaining Useful Life Based on Deep Feature Fusion and Wiener Process. J. Manuf. Syst. 2024, 73, 19-38. [CrossRef]

10. Liu, J.; Wang, X.; Xie, F.; Wu, S.; Li, D. Condition Monitoring of Wind Turbines with the Implementation of Spatio-Temporal Graph Neural Network. Eng. Appl. Artif. Intell. 2023, 121, 106000. [CrossRef]

11. Li, C.; Mo, L.; Tang, H.; Yan, R. Lifelong Condition Monitoring Based on NB-IoT for Anomaly Detection of Machinery Equipment. Procedia Manuf. 2020, 49, 144-149. [CrossRef]

<!-- PDF_PAGE: 23 -->

12. Li, Y.; Dai, W.; Zhu, L.; Zhao, B. A Novel Fault Early Warning Method for Mechanical Equipment Based on Improved MSET and CCPR. Measurement 2023, 218, 113224. [CrossRef]

13. Gomez, M.J.; Castejón, C.; Corral, E.; García-Prada, J.C. Railway Axle Condition Monitoring Technique Based on Wavelet Packet Transform Features and Support Vector Machines. Sensors 2020, 20, 3575. [CrossRef]

14. Dhiman, H.S.; Deb, D.; Carroll, J.; Muresan, V.; Unguresan, M.-L. Ind Turbine Gearbox Condition Monitoring Based on Class of Support Vector Regression Models and Residual Analysis. Sensors 2020, 20, 6742. [CrossRef]

15. Zhang, L.; Wang, J.; Xiao, Q.; Luo, Y.; Wang, Z.; Wang, C.; Liu, J. A Bearing Fault Diagnosis Method with Implementation of Multiscale Time-Frequency Feature Fusion and Bidirectional Information Interaction. IEEE Sens. J. 2025, 25, 23740-23756. [CrossRef]

16. Cai, G.; Zhao, J.; Song, Q.; Zhou, M. System Architecture of a Train Sensor Network for Automatic Train Safety Monitoring. Comput. Ind. Eng. 2019, 127, 1183-1192. [CrossRef]

17. Liu, J.; Wang, C.; Wang, R.; Xiao, Q.; Wang, X.; Wu, S.; Zhang, L. A Novel Multiscale Adaptive Graph Adversarial Network for Mechanical Fault Diagnosis. Knowl.-Based Syst. 2025, 309, 112787. [CrossRef]

18. Zhang, L.; Wang, J.; Liu, J.; Wang, C.; Luo, Y.; Li, G. Bearing Diagnosis for Unknown Working Conditions: Mixed Enhancement and Adaptive Triplet Learning. Struct. Health Monit. 2026. [CrossRef]

19. Liu, X.; Meng, X.; Ning, L.; Xu, F.; Li, Q.; Zhao, C. A Deep Learning-Based Method for Mechanical Equipment Unknown Fault Detection in the Industrial Internet of Things. Sensors 2025, 25, 5984. [CrossRef]

20. Li, Z.; Li, J.; Wang, Y.; Wang, K. A Deep Learning Approach for Anomaly Detection Based on SAE and LSTM in Mechanical Equipment. Int. J. Adv. Manuf. Technol. 2019, 103, 499-510. [CrossRef]

21. Hu, J.; Guo, J.; Rui, Z.; Wang, Z. ADMM-1DNet: Online Monitoring Method for Outdoor Mechanical Equipment Part Signals Based on Deep Learning and Compressed Sensing. Appl. Sci. 2024, 14, 2653. [CrossRef]

22. Zou, F.; Li, X.; Li, Y.; Sang, S.; Jiang, M.; Zhang, H. GOL-SFSTS Based Few-Shot Learning Mechanical Anomaly Detection Using Multi-Channel Audio Signal. Knowl.-Based Syst. 2024, 284, 111204. [CrossRef]

23. Hu, G.; Fu, S.; Zhong, S.; Lin, L.; Liu, Y.; Zhang, S.; Guo, F. Remaining Useful Life Prediction of Mechanical Equipment Based on Time-Series Auto-Correlation Decomposition and CNN. Meas. Sci. Technol. 2024, 35, 105104. [CrossRef]

24. Araújo, T.O.; Netto, M.L.; Justo, J.F. Multi-Agent Sensor Fusion Methodology Using Deep Reinforcement Learning: Vehicle Sensors to Localization. Sensors 2026, 26, 1105. [CrossRef]

25. Zhang, X.; Zhang, X.; Zhu, L.; Gao, C.; Ning, B.; Zhu, Y. A Graph-Data-Based Monitoring Method of Bearing Lubrication UsingMulti-Sensor. Lubricants 2024, 12, 229. [CrossRef]

26. Li, J.; Sun, Y.; Liu, H.; Li, Y. A Study on Structural Damage Diagnosis Method for Aero-Engines Based on Dynamic Topology-Aware Graph Neural Networks. Aerosp. Sci. Technol. 2026, 168, 111071. [CrossRef]

27. Liang, P.; Li, Y.; Wang, B.; Yuan, X.; Zhang, L. Remaining Useful Life Prediction via a Deep Adaptive Transformer Framework Enhanced by Graph Attention Network. Int. J. Fatigue 2023, 174, 107722. [CrossRef]

28. Fu, Y.; Ma, J.; He, D.; Jin, Z.; Cao, H.; Yu, B. Multi-Scale Dynamic Spatio-Temporal Graph Network for Anomaly Detection of Wind Turbine Main Bearing under Time-Varying Conditions. Eng. Appl. Artif. Intell. 2025, 162, 112753. [CrossRef]

30. Liu, Y.; Qiu, Y.; Feng, Y.; Zhou, H.; Xiong, X.-L. Spatiotemporal Physics-Guided Graph Neural Network for Wind Farm Power Prediction. Eng. Appl. Artif. Intell. 2026, 171, 114301. [CrossRef]

31. Wang, T.; Liu, Z.; Lu, G.; Liu, J. Temporal-Spatio Graph Based Spectrum Analysis for Bearing Fault Detection and Diagnosis. IEEE Trans. Ind. Electron. 2021, 68, 2598-2607. [CrossRef]

32. Du, X.; Zhou, C.; Tian, Y.-C.; Xu, B. Anomaly Detection Based on Graph Neural Networks Incorporating with Domain Knowledge for Industrial Cyber-Physical Systems. Expert Syst. Appl. 2026, 298, 129645. [CrossRef]

33. Pan, Y.; Yi, C.; Liao, X.; Lin, Y.; He, P.; Lin, J. Detecting Unexpected Faults of High-Speed Train Axlebox Bearings Using Multi-Node Network Structure. Measurement 2025, 246, 116641. [CrossRef]

34. Li, L.; Liu, L.; Du, X.; Wang, X.; Zhang, Z.; Zhang, J.; Zhang, P.; Liu, J. CGUN-2A: Deep Graph Convolutional Network via Contrastive Learning for Large-Scale Zero-Shot Image Classification. Sensors 2022, 22, 9980. [CrossRef] [PubMed]

35. Cui, Z.; Zhang, J.; Noh, G.; Park, H.J. ADSTGCN: A Dynamic Adaptive Deeper Spatio-Temporal Graph Convolutional Network for Multi-Step Traffic Forecasting. Sensors 2023, 23, 6950. [CrossRef] [PubMed]

36. Fanta, H.; Shao, Z.; Ma, L. SiTGRU: Single-Tunnelled Gated Recurrent Unit for Abnormality Detection. Inf. Sci. 2020, 524, 15-32. [CrossRef]

Disclaimer/Publisher's Note: The statements, opinions and data contained in all publications are solely those of the individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to people or property resulting from any ideas, methods, instructions or products referred to in the content.