# Validation approach and discussion

</div>

"When you want to know how things really work, study them when they're coming apart."

William Gibson

Content

7.1 Validating the proposed Decision Support System in a practical example 109

7.2 Use case example: Design of a predictive maintenance system for aircraft engine run-to-failure data set under real flight conditions 109

7.3 The concept phase of a predictive maintenance system for the N-CMAPSS database 111

7.4 Component selection using an ontology-enabled case-based recommendation system 113

7.5 Discussion 117

7.6 Lessons learnt from the DSS validation using the N-CMAPSS 119

## 7.1 Validating the proposed Decision Support System in a practical example

As part of the framework validation, a use case example has been developed. This example uses an aircraft engine data set [Cha+21]. The data set contains the run-failure records of 128 aircraft jet engines under real flight conditions and has been generated with the Commercial Modular Aero-Propulsion System Simulation (CMAPSS) model developed by NASA. This data set is called the N-CMAPSS. The purpose is not only to check the capabilities of the proposed ontology-enabled CBR system but also to identify the improvement points for the DSS. The objective for this validation is to implement one of the models proposed by the DSS to fulfil a predictive maintenance function for the N-CMAPSS database. This implementation helps to demonstrate that the DSS is capable to suggest suitable components for predictive maintenance systems, complementing the cross-validation in Chapter 6.

## 7.2 Use case example: Design of a predictive maintenance system for aircraft engine run-to-failure data set under real flight conditions

The N-CMAPSS data set was published in January 2021 and has an objective to facilitate the development of specialized algorithms for predictive maintenance applications by providing a complete set of run-to-failure data with different failure modes. CMAPSS has been used to simulate other well-known data sets for

prognostics purposes, such as PHM08 data [Sax+08]. The N-CMAPSS data set supposes an improvement in the level of fidelity between the simulated data versus the real-life data. Each flight in the N-CMAPSS data set is fully recorded from take-off to landing. Previous versions of CMAPSS data sets offer a simpler approach that only provides one single discrete measure for each engine flight. Another improvement can be seen in the number of failure modes. Previous CMAPSS data sets only had one or two imposed failure modes, and for those sets with two failure modes, there were no explicit records that could be used to discriminate the failure mode that affected each jet engine. The N-CMAPSS data set has up to seven different failure modes and there is an explicit record of the failure mode that affected each engine. Each failure mode has its own set of symptoms that can be identified by the loss of Flow (F) or Efficiency (E) in the rotary components of the engine such as the fan, the Low-Pressure Compressor (LPC), the High-Pressure Compressor (HPC), the Low-Pressure Turbine (LPT), and the High-Pressure Turbine (HPT). This improvement extends the use of the N-CMAPSS data set, not only for prognostics like the previous CMAPPS data sets but also for diagnostics.

According to [Cha+21], five main steps have been followed to generate the data set (see Figure 7.1):

1. The flight data are defined as recorded onboard real commercial jets.

2. The degradation of the engine components is imposed in the simulation so that it is possible to keep track of the failed component in each run-to failure engine.

3. The resulting degraded flight is simulated using the CMAPSS.

4. The health condition is evaluated and the unit continues flying with increasing degradation until the health index of the engine has reached zero.

5. Sensor noise is added to the simulated engine response in order to make the simulated data closer to real-life data.

The flight conditions have been divided into three flight classes depending on the flight length. Class 1 includes all flights that last from one to three hours. Class 2 includes all flights between three to five hours of duration. Class 3 includes all flights that last more than 5 hours. The data set is divided into 8 sub-sets with different failure modes and a different number of engine units. Table 7.1 shows the overview of the N-CMAPSS data set. Each sub-set has its own failure mode except for the sub-set DS02 which has 2 failure modes which are the ones from the sub-sets SD01 and DS03 correspondingly. The overview shows the symptoms that describe each failure mode. For example, the failure mode of sub-set DS01 can be detected by a decrease of the efficiency in the HPC, while the failure mode of sub-set DS04 can be detected by a decrease of the efficiency and flow of the engine fan.

Each unit in the N-CMAPSS data set has unknown initial degradation, meaning that the records did not start at the same point for all of them. The records for each engine in the N-CMAPSS finish when the engine reaches the failed state. Each engine goes through a normal degradation stage in which the fault symptoms are not evident. If a fault appears in the engine, there will be a transition from normal degradation to abnormal degradation that is faster than normal degradation to reach the failed state. The data is composed of 46 variables divided in 5 different groups:

1. Scenario descriptors: variables that are independent of the engine operation that are used to describe the operational modes of the engine.

2. Measurements: Sensors that describe the engine operation.

3. Virtual sensors: complementary measures offered by CMAPSS to assess the engine operation

4. Model health parameters: complementary variables that show the symptoms of the different failure modes.

5. Auxiliary variables: variables for the data set consistency.

Further explanation about the N-CMAPSS data set can be found in [Cha+21] and [FDL07].


> **Figure Description:**

This diagram illustrates a five-step cyclical process for simulating aircraft engine degradation, centered around a circular arrow indicating the flow of operations. Step 1, "Define Flight Conditions," features a NASA DASHlink logo and an image of an airplane. Step 2, "Impose Degradation," includes a line graph plotting "HPT Eff. - θ [-]" on the y-axis (ranging from 0.000 to -0.015) against "Time [cycle]" on the x-axis (0 to 100). The graph shows ten colored lines representing Units 1 through 10, all trending downward as time increases.

Step 3, "Simulate Degraded Flight," displays a schematic labeled "CMAPSS Aircraft Engine Simulator," which depicts the internal components of a jet engine, including the Low-Pressure Compressor (LPC), High-Pressure Compressor (HPC), High-Pressure Turbine (HPT), and Low-Pressure Turbine (LPT), connected by various flow paths and sensors. Step 4, "Flight Until Failure," features a line graph plotting "Health Index H [-]" on the y-axis (0.0 to 1.0) against "Time [cycle]" on the x-axis (0 to 100). This graph also shows ten colored lines for Units 1 through 10, all showing a decline in health index over time. Step 5, "Add Sensor Noise & Store," is represented by a document icon containing a table grid, indicating the final data processing stage before the cycle potentially repeats.



<div align="center">

Figure 7.1: N-CMAPSS data creation process [Cha+21]

</div>

## 7.3 The concept phase of a predictive maintenance system for the N-CMAPSS database

Given that N-CMAPSS is intended for research purposes, it is up to the researchers to define the list of needs and desires for the new predictive maintenance system. For the current research framework, the following list of needs and desires is proposed:

1. Read the N-CMAPSS data format.

2. Identify the variables needed to perform the diagnostics and prognostics.

<div align="center">

Table 7.1: Overview of N-CMAPSS data set [Cha+21]

</div>

<table border="1"><tr><td rowspan="2">Name</td><td rowspan="2">#Units</td><td rowspan="2">Flight classes</td><td rowspan="2">Failure modes</td><td colspan="2">Fan</td><td colspan="2">LPC</td><td colspan="2">HPC</td><td colspan="2">HPT</td><td colspan="2">LPT</td><td rowspan="2">Size(measures)</td></tr><tr><td>E</td><td>F</td><td>E</td><td>F</td><td>E</td><td>F</td><td>E</td><td>F</td><td>E</td><td>F</td></tr><tr><td>DS01</td><td>10</td><td>1,2,3</td><td>1</td><td></td><td></td><td></td><td></td><td></td><td></td><td>√</td><td></td><td></td><td></td><td>7.6M</td></tr><tr><td>DS02</td><td>9</td><td>1,2,3</td><td>2</td><td></td><td></td><td></td><td></td><td></td><td></td><td>√</td><td></td><td>√</td><td>√</td><td>6.5M</td></tr><tr><td>DS03</td><td>15</td><td>1,2,3</td><td>1</td><td></td><td></td><td></td><td></td><td></td><td></td><td>√</td><td></td><td>√</td><td>√</td><td>9.8M</td></tr><tr><td>DS04</td><td>10</td><td>2,3</td><td>1</td><td>√</td><td>√</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>10.0M</td></tr><tr><td>DS05</td><td>10</td><td>1,2,3</td><td>1</td><td></td><td></td><td></td><td></td><td>√</td><td>√</td><td></td><td></td><td></td><td></td><td>6.9M</td></tr><tr><td>DS06</td><td>10</td><td>1,2,3</td><td>1</td><td></td><td></td><td>√</td><td>√</td><td>√</td><td>√</td><td></td><td></td><td></td><td></td><td>6.8M</td></tr><tr><td>DS07</td><td>10</td><td>1,2,3</td><td>1</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>√</td><td>√</td><td>7.2M</td></tr><tr><td>DS08</td><td>54</td><td>1,2,3</td><td>1</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>35.6M</td></tr></table>

3. Pre-process and reduce the N-CMAPSS data set.

4. Detect the transition from normal degradation to abnormal degradation.

5. Identify the failure mode that leads the engine to fail.

6. Determine the current state of a jet engine.

7. Estimate the remaining useful life of a jet engine.

8. Provide a report of the results

The previous list of needs and desires are translated into the following list of functional requirements:

1. The system shall read the N-CMAPSS data set.

2. The system shall model the health of the jet engine.

4. The system shall assess the health state of the engine.

3. The system shall detect incipient faults in the engine.

5. The system shall estimate the remaining useful life of the engine.

6. The system shall provide a report of the predictive maintenance results.

In the first concept of the predictive maintenance systems, the data pre-process and data reduction are not included and they have been performed manually. As can be seen, only functional requirements have been determined. The N-CMAPSS does not provide any performance needs, structural constraints or experiential needs which means that no behavioural, structural or experiential requirements have been added. As the data set comes from an academic case study, no experiential needs or desires have been added. It is important to notice that in practical applications, these three types of requirements are important to be considered as they provide the requirements related to the expected performance of the system, interfaces with other related systems and interface with the system user.

Given the functional requirements, the architecture process presented in Chapter 3 has been followed until obtaining a logical architecture of the new predictive maintenance system. Figure 7.2 presents the logical architecture developed from the functional requirements previously listed. A first component will collect the processed data from the jet engine records. This data will be used to develop the health model of the engine. Later, the engine data and the health model are used for the components in charge of assessing the health state, detect incipient faults, and identify these faults. The outputs of these three components are

the input for the system component in charge of the remaining useful life estimation. The health assessment, fault detection, fault identification and remaining useful life computation will provide the information needed to make the predictive maintenance report by the last system component. The functions of each predictive maintenance system component have been assigned to match with the definitions established in the ontology and the Decision Support System (DSS) so that it can be possible to retrieve the corresponding recommendations.


> **Figure Description:**

This diagram illustrates the architecture of a predictive maintenance system, organized into five primary modules. At the top level, the "Predictive maintenance system" contains the "Data collection module," "Fault detection module," "Health modelling/assessment module," "Fault identification module," "Remaining useful life module," and "Report module."

The "Data collection module" contains a "Collect data" function that outputs "Engine data" to the "Fault detection module," the "Health modelling/assessment module," and the "Fault identification module." The "Fault detection module" contains a "Detect fault" function that outputs a "detected fault" to the "Remaining useful life module" and the "Report module." The "Health modelling/assessment module" contains two functions: "Model health engine evolution," which outputs a "Health index" to the "Fault identification module" and the "Remaining useful life module," and "Assess health state," which outputs a "Health state" to the "Report module." The "Model health engine evolution" function also outputs "Health model and health index" to the "Assess health state" function.

The "Fault identification module" contains an "Identify fault (failure mode)" function that receives "Engine data" and "Health index" as inputs and outputs an "identified fault" to the "Remaining useful life module" and the "Report module." The "Remaining useful life module" contains an "Estimate RUL of engine" function that receives "detected fault," "identified fault," and "Health index" as inputs, and outputs "RUL." Finally, the "Report module" contains a "Make report" function that receives "detected fault," "identified fault," "Health state," and "RUL" as inputs. The connections are represented by lines with arrows indicating the flow of data between the specific functions within each module.



<div align="center">

Figure 7.2: The logical architecture of a predictive maintenance system for the N-CMAPSS data set

</div>

## 7.4 Component selection using an ontology-enabled case-based recommendation system

Considering the logical architecture presented in Figure 7.2, there are four different logical components for which the Decision Support System can provide suggestions:

- Health modelling/assessment module

- Fault detection module

- Fault identification module

- Remaining useful life module

For each of these four logical components, a retrieval of possible solutions using the proposed DSS was performed. The results of the retrievals are summarized in Table 7.2. The DSS is capable to provide the similarity to each of the cases in the case base, but the most similar cases will have more relevance. For the current analysis and layout purposes of Table 7.2 only the five highest similarities are considered for each predictive maintenance function.

The results in Table 7.2 demonstrate the capabilities of the DSS to retrieve suitable solutions for each of the logical components. All the proposed models can be adapted to fulfil the intended function. All the

similarities between the target case and retrieved cases were higher than 0.776, meaning that the global similarity between proposed models and the target case was at least of 77.6%. An improvement opportunity for future research can be seen for those retrieved cases with exact same similarity; additional information would be needed to select the most suitable one. For example, for remaining useful life estimation module the DSS proposed five possible models with the same similarity value, no model is ranked higher than the other. An architect will need need further information to perform the trade-off analysis and select the most suitable model to be implemented. Further similarity measures can be added to refine the retrieval process. It is important not to forget that in a first attempt the DSS is intended to provide suitable solutions, but there is a fair amount of remaining work so that the DSS is capable to suggest the most suitable among the others.

It is important to notice that the ontological similarity allowed to propose some models originally used for fault identification to fulfil fault detection and vice-versa. This inferred similarity is accurate as both functions are related to classification tasks. By adding more cases to the case base, more semantic similarities like this one can be found. The current values of similarity are low as the diversity in the case base is high compared to the case base size. Further explanations about the semantic similarity can be found in [MHMJV21], a conference publication performed in the framework of the current research, included in Appendix B.

In order to further validate the DSS recommendations, one of the suggested models has been taken as an example and has been implemented to fulfil the corresponding predictive maintenance function. Taking advantage of the research team experience in Self-Organizing Maps (SOM), an implementation of the health modelling component is performed using the SOM. The DSS recommends the SOM and logistic regression for health modelling as the most suitable models (similarity equal to 0.897) for the N-CMAPSS case study. The following section provides further explanations about the SOM example implementation and its preliminary results.

The methodology to implement the Self-Organizing Maps (SOM) for health modelling has been adopted from [Sch+20], (see Appendix A). Self-Organizing Maps are artificial neural networks with unsupervised training that are capable to cluster instances of data depending on the instance attributes. SOM is normally composed of a square layer of neurons and the different clusters after the SOM training can be graphically represented on the maps as well defined regions. It has been successfully used to model the degradation process of different machines such as jet engines [MV18]. In these cases, the neurons represent the health or degradation of the machine at a specific operational mode. The trained SOM will have a single region but a transition from white (optimal state) to black (failed state). When assessing the health or degradation of a machine using the trained SOM, a neuron will be excited on the map showing how advanced the degradation is or how much the health has decreased. This is the actual goal of the current implementation: to obtain a trained SOM capable to show a transition from optimal state to failed state.

In a first attempt, a simplified implementation is selected. To train the SOM, only sub-set of the N-CMAPSS data is used. The DS01 has been selected as it has only one failure mode. The first challenge in the adaptation of the SOM solution to the N-CMAPSS database is related to the operational modes. To train the SOM, the different operational modes must be distinguishable from one another; unfortunately, the N-CMAPSS is not focused on the different operational modes of the engine but in the complete flight envelope. To solve this challenge an operational mode has been defined when the engine reaches 10000 feet of altitude when the aircraft is climbing. At that operational mode, the throttle-resolver angle will be always higher than 70% and the flight Mach number is always in the same interval. These three variables are presented in the N-CMAPSS as scenario descriptors and are independent of the engine operation.

A second challenge in the adaptation of the SOM for the N-CMAPSS was related to the variables selected for the SOM training. The N-CMAPSS is composed by 45 different variables of different natures: scenario descriptors, operational engine measurements, virtual sensors and model health parameters. For the current implementation, only the scenario descriptors and the operational engine measures (see Table 7.3) have been

<div align="center">

Table 7.2: Models retrieval for the N-CMAPSS examples

</div>

<table border="1"><tr><td>Target case function</td><td>Case</td><td>PdM Function</td><td>Model</td><td>Similarity</td></tr><tr><td rowspan="5">Fault detection</td><td>166</td><td>Fault detection</td><td>Gaussian process classifier</td><td>0.859</td></tr><tr><td>211</td><td>Fault detection</td><td>Piecewise linear model(PWL), Hybrid Kalman Filter, OBEM model</td><td>0.834</td></tr><tr><td>49</td><td>Fault identification</td><td>Support vector machines</td><td>0.776</td></tr><tr><td>48</td><td>Fault identification</td><td>Deep belief network</td><td>0.776</td></tr><tr><td>50</td><td>Fault identification</td><td>Multi-layer perceptron neural network</td><td>0.776</td></tr><tr><td rowspan="5">Fault identification</td><td>48</td><td>Fault identification</td><td>Deep belief network</td><td>0.859</td></tr><tr><td>50</td><td>Fault identification</td><td>Multi-layer perceptron neural network</td><td>0.859</td></tr><tr><td>49</td><td>Fault identification</td><td>Support vector machines</td><td>0.859</td></tr><tr><td>212</td><td>Fault detection</td><td>Piecewise linear model(PWL), Hybrid Kalman Filter, OBEM model</td><td>0.834</td></tr><tr><td>166</td><td>Fault detection</td><td>Gaussian process classifier</td><td>0.794</td></tr><tr><td rowspan="5">Health modelling/assessment</td><td>12</td><td>Health modelling</td><td>Self-organizing maps</td><td>0.897</td></tr><tr><td>1</td><td>Health modelling</td><td>Logistic regression</td><td>0.897</td></tr><tr><td>57</td><td>Health modelling</td><td>Statistical regression model</td><td>0.854</td></tr><tr><td>159</td><td>Health modelling</td><td>Hidden Markov Chains</td><td>0.852</td></tr><tr><td>168</td><td>Health modelling</td><td>Copula based sampling</td><td>0.838</td></tr><tr><td rowspan="5">Remaining useful life estimation</td><td>51</td><td>Remaining useful life estimation</td><td>LSTM(Long-Short Term Memory Neural Network)</td><td>0.895</td></tr><tr><td>53</td><td>Remaining useful life estimation</td><td>Recurrent Neural Network</td><td>0.895</td></tr><tr><td>54</td><td>Remaining useful life estimation</td><td>Gated recurrent unit network</td><td>0.895</td></tr><tr><td>62</td><td>Remaining useful life estimation</td><td>Relevance vector machine</td><td>0.895</td></tr><tr><td>64</td><td>Remaining useful life estimation</td><td>Bayesian linear regression</td><td>0.895</td></tr></table>

selected for the training as they represent the variables that can be obtained from real aircraft engines. The virtual sensors and the model health parameters are part of the simulation and model consistency but they would not be available in real jet engines.

<div align="center">

Table 7.3: Operational Measurements N-CMAPSS

</div>

<table border="1"><tr><td>Symbol</td><td>Description</td><td>Units</td></tr><tr><td>Wf</td><td>Fuel flow</td><td>pps</td></tr><tr><td>Nf</td><td>Physical fan speed</td><td>rpm</td></tr><tr><td>Nc</td><td>Physical core speed</td><td>rpm</td></tr><tr><td>T24</td><td>Total temperature at LPC outlet</td><td>°R</td></tr><tr><td>T30</td><td>Total temperature at HPC outlet</td><td>°R</td></tr><tr><td>T48</td><td>Total temperature at HPT outlet</td><td>°R</td></tr><tr><td>T50</td><td>Total temperature at LPT outlet</td><td>°R</td></tr><tr><td>P2</td><td>Total pressure at fan inlet</td><td>psia</td></tr><tr><td>P15</td><td>Total pressure in bypass-duct</td><td>psia</td></tr><tr><td>P21</td><td>Total pressure at fan outlet</td><td>psia</td></tr><tr><td>P24</td><td>Total pressure at LPC outlet</td><td>psia</td></tr><tr><td>Ps30</td><td>Static pressure at HPC outlet</td><td>psia</td></tr><tr><td>P40</td><td>Total pressure at burner outlet</td><td>psia</td></tr><tr><td>P50</td><td>Total pressure at LPT outlet</td><td>psia</td></tr></table>

LPC: Low Pressure Compressor

HPC: High Pressure Compressor

LPT: Low Pressure Turbine

HPT: High Pressure Turbine

To increase the convergence changes in the SOM training, it is advisable to add the most representative inputs. A good practice is to delete all variables that present a binary or a constant behaviour as they do no provide any useful information about the degradation. A correlation test of the variables is also recommended to avoid adding redundant variables to the SOM training. Both of these tests have been performed on the operational measurements. No variables presented constants or binary records. Figure 7.3 shows a correlation matrix for the operational measures in which the same variables are in the horizontal and vertical axes; the correlation value is shown in the intersection of a vertical and horizontal axis. A correlation threshold has been set at 0.9. If two or more variables have a correlation higher than the threshold, only one of them will be selected at random as they will provide almost the same information. It is important to point out that before the correlation test, all variables were normalized between 0 and 1 which is also a requirement for the SOM training [Sch+20]. After performing the variables assessment, only four of them were selected to train the map, which represents a reduction in the number of variables compared to the study in Appendix A:

1. Total temperature at Low-Pressure Compressor (LPC) outlet.

2. Total temperature at High-Pressure Turbine (HPT) outlet.

3. Total pressure at fan inlet.

4. Total pressure at Low-Pressure Turbine (LPT) outlet

Once the variables have been selected and normalized, the training of the SOM can start. Given the data size a map of 5x5 neurons in square architecture has been selected. Several SOM's were trained and their convergence and behaviour were confirmed in the results. Figure 7.4 shows an example of a trained


> **Figure Description:**

This image is a correlation heatmap displaying the relationships between 14 variables: T24, T30, T48, T50, P15, P2, P21, P24, Ps30, P40, P50, Nf, Nc, and Wf. The variables are listed on both the vertical y-axis and the horizontal x-axis. The heatmap uses a color scale ranging from light beige (near 0.0) to dark brown (near 1.0), with a color bar on the right indicating values at 0.2, 0.4, 0.6, and 0.8. Each cell contains the numerical correlation coefficient between the corresponding row and column variables.

The matrix is symmetric with a diagonal of 1s. The values are as follows: Row T24: 1, 0.94, 0.85, 0.68, 0.94, 0.48, 0.94, 0.99, 0.95, 0.94, 0.84, 0.93, 0.91, 0.95. Row T30: 0.94, 1, 0.8, 0.61, 0.86, 0.26, 0.86, 0.93, 0.99, 0.99, 0.88, 0.99, 0.99, 0.96. Row T48: 0.85, 0.8, 1, 0.95, 0.7, 0.15, 0.7, 0.81, 0.81, 0.8, 0.74, 0.85, 0.73, 0.93. Row T50: 0.68, 0.61, 0.95, 1, 0.55, 0.11, 0.55, 0.65, 0.63, 0.62, 0.63, 0.67, 0.52, 0.8. Row P15: 0.94, 0.86, 0.7, 0.55, 1, 0.71, 1, 0.98, 0.89, 0.89, 0.88, 0.8, 0.84, 0.85. Row P2: 0.48, 0.26, 0.15, 0.11, 0.71, 1, 0.71, 0.57, 0.33, 0.33, 0.44, 0.16, 0.26, 0.26. Row P21: 0.94, 0.86, 0.7, 0.55, 1, 0.71, 1, 0.98, 0.89, 0.89, 0.88, 0.8, 0.84, 0.85. Row P24: 0.99, 0.93, 0.81, 0.65, 0.98, 0.57, 0.98, 1, 0.95, 0.95, 0.9, 0.9, 0.9, 0.93. Row Ps30: 0.95, 0.99, 0.81, 0.63, 0.89, 0.33, 0.89, 0.95, 1, 1, 0.92, 0.97, 0.99, 0.97. Row P40: 0.94, 0.99, 0.8, 0.62, 0.89, 0.33, 0.89, 0.95, 1, 1, 0.92, 0.97, 0.99, 0.97. Row P50: 0.84, 0.88, 0.74, 0.63, 0.88, 0.44, 0.88, 0.9, 0.92, 0.92, 1, 0.84, 0.86, 0.9. Row Nf: 0.93, 0.99, 0.85, 0.67, 0.8, 0.16, 0.8, 0.9, 0.97, 0.97, 0.84, 1, 0.97, 0.97. Row Nc: 0.91, 0.99, 0.73, 0.52, 0.84, 0.26, 0.84, 0.9, 0.99, 0.99, 0.86, 0.97, 1, 0.93. Row Wf: 0.95, 0.96, 0.93, 0.8, 0.85, 0.26, 0.85, 0.93, 0.97, 0.97, 0.9, 0.97, 0.93, 1.



<div align="center">

Figure 7.3: Correlation matrix of the sensors of the N-CMAPSS data set to be used as input for the SOM

</div>

map using the extracted data from the N-CMAPSS database. The clearest neuron represents the optimal operation condition of the engine and the darkest red neuron represents the condition of the engine just before its failure. An assessed engine with this SOM will excite a neuron between these two limits and its degradation can be estimated using the weights of the neuron. A transition from clear to darks is observable in the graphical representation of the SOM. This represents the degradation of the engine at the selected operational mode. For further explanations about the training and interpretation of the SOM, please read the article in Appendix A.

## 7.5 Discussion

It is important to recall that the validation of a Decision Support System (DSS) is a non-trivial task. The validation of the implemented model suggested by the DSS can be used to indirectly validate the DSS but further implementations would be required to confirm the capabilities and accuracy of the proposed DSS for predictive maintenance models selection. In the current implementation, the N-CMPASS represents the target case for which a new predictive maintenance system has to be developed. The ontology-enabled CBR recommendation system (also called DSS in this manuscript) proposed different models to fulfil each predictive maintenance function. One of the models proposed by the DSS for the function health modelling was the Self-Organizing Map (SOM). The SOM implementation successfully showed the degradation trend of jet-engines from nominal operation to failed condition using a subset of the N-CMPASS. The trained SOM can be also used to assess the health/ degradation of other engines of the same type and under the same operation conditions. It is important to clarify that this validation aims to demonstrate the suitability of the model proposed by the DSS, but further comparisons are needed among the suggested models are necessary to determine the best model. While performing the cross-validation presented in Chapter 6 and the current validation based on the SOM implementation, several improvement points have been identified:


> **Figure Description:**

The image is a heatmap titled "Dataset" that displays a 5x5 grid of values represented by varying shades of red, where lighter shades indicate lower values and darker shades indicate higher values. The x-axis and y-axis are both labeled with integers from 0 to 4. The grid is organized such that the values increase as one moves from the bottom-left toward the top-right. Specifically, the bottom-left cell (0,0) is the lightest in color, while the top-right cell (4,4) is the darkest. The intensity of the red color increases progressively along both the rows and columns, creating a gradient effect where the highest values are concentrated in the upper-right quadrant of the matrix.



<div align="center">

Figure 7.4: Trained SOM for the sub-set DS01

</div>

- Problems with the diversity in the retrieved cases: Even if it was not the case for this N-CMAPSS case study, in some retrievals of the cross-validation, the DSS proposed the same model several times with different references in the case base. This is a problem from a systems engineering point of view. An architect looking for innovative solutions needs a diverse list of possible solutions from the DSS. Further work can be done to avoid this diversity problem. Cases generalization and some other case diversity techniques can be applied to overcome this problem [De +05]. Such a situation could also be attributed to a potential problem of the coverage of the solution space. If the stored cases correspond only to a small portion of the solution space, the models suggested by the DSS can be very similar. For the current study this is not the case; models from all over the solution space have been considered. The state-of-the-art study in Chapter 2 allowed determining that the solution space for predictive maintenance systems is composed of data-driven models, knowledge-based models, physics-based models and multi-model approaches that combine at least two models from any of the three mentioned model families. The case base for the DSS was built considering all the solution space but the validation showed that this can be improved. A refinement of the solution space can be done with regards to each predictive maintenance function. For diagnostics functions such as for example "feature extraction" only data-driven models have been identified while creating the the case base. Another example can be seen for the function "remaining useful life estimation" where only data-driven and physics-based models have been identified. A refinement of the solution space considering each predictive maintenance function separately can help to improve the case base and the diversity in the models retrieved with the DSS.

- Additional information to perform the trade-off analysis: Several retrieved models for the same predictive maintenance function have the same similarity. Implement several solutions using different models that have the same similarity may not always be feasible for time and resources limitations. This poses a challenge for the architect to select the most suitable. Some other attributes could be added to the case so that the retrieved information can be used to perform a trade-off analysis so that the DSS can help the architect to make an accurate decision with regard to the model selection. Performance indicators, computational power required, implementation complexity, implementation cost, are some examples of complementary variables that can help to assess the models proposed by

the DSS. The additional attributes can be also used to add the preferences or initial constraint set by the DSS user from the beginning. Some users may be interested only in data-driven models, then the solution could be limited before the retrieval of models.

- Information about the adaptation of the proposed model: The current version of the DSS can be improved by including additional information for the adaptation of the suggested model in the target case. This is not only useful for the trade-off analysis, but also for the detailed design and implementation stage of the predictive maintenance system. The implementation of the SOM for health modelling has shown that some hyper-parameters of the models must be changed. A complementary guide for the adaptation of the suggested models can be added to facilitate its implementation in the target case. An expert system may guide the architect with the adaptation steps for each of the models. For time limitations, this is not possible for the current research.

## 7.6 Lessons learnt from the DSS validation using the N-CMAPSS

The validation of the proposed DSS for predictive maintenance component selection has been presented in this chapter. The capabilities of the DSS have been tested with the implementation of one of the suggested models for health modelling for the N-CMAPSS case study. This validation helped to demonstrate not only that the proposed DSS is capable to suggest suitable components for predictive maintenance systems, but also it allowed to identify improvement points of the DSS. A DSS is difficult to validate with a limited amount of data and with a limited number of implementations of the suggested models, but the success in the implementation of the SOM for health modelling of the N-CMAPSS case study indirectly validates the DSS capabilities. In the following and last chapter, the lessons learnt in the research are summarized in the conclusions and the perspectives of future work proposed.

Intentionally left blank

<div align="center">

