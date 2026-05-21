---
source: "C:/Users/maria/OneDrive - Estudiantes ITCR/TEC/XIII Semestre/Asistencia Montero/Ontologies/Thesis_Manuscript_Final_left_in_blank_pages__Copy__260422_100840_split/part_01_pages_001_100.pdf"
title: "part_01_pages_001_100"
converted_at: "2026-04-23T15:32:23Z"
---


> **Figure Description:**

University logo.



Toulouse Midi-Pyrénées

En vue de l'obtention du

<div align="center">

# DOCTORAT DE L'UNIVERSITÉ DE TOULOUSE

</div>

Délivré par : l'Institut Supérieur de l'Aeronautique et de l'Espace (ISAE)

Présentée et soutenue le 13/01/2022 par :

Juan José MONTERO-JIMENEZ

Knowledge reuse to enhance predictive maintenance systems architecture

ERIC BONJOUR

JURY Professor at University of Lorraine

FRANCES BRAZIER

ANABEL FRAGA-VAZQUEZ

Professor at TU DELFT

Rapporteur

Associate Professor at Universidad Carlos III

Rapporteur

Professor at ISAE-SUPAERO

ELISE VAREILLES

Membre du Jury

BERNARD GRABOT

Professor at ENIT

Membre du Jury

Professor at ISAE-SUPAERO

ROB VINGERHOEDS

Directeur de Thèse

Directeur de Thèse

École doctorale et spécialité :

EDSYS : Génie Industriel 4200046

Unité de Recherche :

ISAE-ONERA CSDV - Commande des Systèmes et Dynamique du Vol

Directeur(s) de Thèse :

Rob VINGERHOEDS et Bernard GRABOT

Rapporteurs :

Eric BONJOUR et Frances BRAZIER

## Acknowledgements

First and foremost, I would like to pass my heartfelt thanks to my supervisors Prof. Rob Vingerhoeds and Prof. Bernard Grabot, theirs door were always open to answer my doubts and provide me with guidance, advise, and support in the realisation of my thesis.

I would like to express my thanks to Tecnológico de Costa Rica, Institut Français d'Amérique Centrale Campus France, ISAE-SUPAERO, and ENIT for sponsoring and supporting my PhD studies in France.

I would like to express my deepest thanks to my wife Estefanny Guillen and my daughter Edith Montero for being that unconditional support that kept me sane along this wonderful process full of ups and downs. It would have been impossible to achieve the success without both of you! I would also like to express my deepest thanks to my parents, sister, and all other the members of my family who were always supporting me at the distance while doing this thesis.

I would like to express my special thanks to Dr.Sebastien Schwartz who was a great teammate, we developed many things together while having a nice work environment. I would also like to express my special thanks to M.Eng Carlos Piedra, M.Eng Sebastian Mata, who helped me check the spanish version of my thesis summary, and along with the group of students from TEC, helped in the creation of the case base for my research. My special thanks to Augusto Miyagawa, Hugo Muñoz, Johanna Mazouzi, Okjin Lee, Tran-vu Nong, and Wendi Ding, students or interns in my research project who helped me in different tasks in the creations of the case-based reasoning system. Also special thanks to Corinne Boisrobert for checking the french version of my thesis summary.

I would like to thank the friends I found in France, Carlos Vaca, Didier Allieres, Stephanny Bardon, Corinne and Phillipe Boisrobert, Franco Peschiera, Vatsal Pant, Jasdeep Singh, the "TICOS en TOULOUSE" and the friends from the Master and DISC department. All of you helped to make wonderful my experience in France and made feel that I was not far from home!

Intentionally left blank

## Contents

# Table of acronyms xiii

## 1 Introduction 1

1.1 The journey begins 1

1.2 Maintenance 2

1.3 Systems concept stage and the system architecture process 4

1.4 Research statements 5

1.5 Organization of the thesis 6

## 2 Towards multi-model approaches to predictive maintenance: A systematic literature survey on diagnostics and prognostics 9

2.1 Exploring the topic and defining the state-of-the-art 9

2.2 Towards multi-model approaches to predictive maintenance: A systematic literature survey on diagnostics and prognostics (Article 1) 10

2.3 Lessons learnt 30

## 3 From needs and desires to a generic logical architecture for predictive maintenance systems 31

3.1 The creative process begins 31

3.2 A systems engineering approach to predictive maintenance systems: from needs and desires to logical architecture (Article 2) 32

3.3 Lessons learnt 41

## 4 Ontology development to support Case-based reasoning systems 43

4.1 Building the framework vocabulary 43

4.2 Ontology 44

4.3 Ontology model for Maintenance Strategies selection and assessment (Article 3) 46

4.4 Terminology framework for predictive maintenance components selection 74

4.5 Lessons learnt 79

## 5 Case-based Reasoning systems development 81

5.1 Reasoning considering the past experiences 81

5.2 The case-based reasoning paradigm 81

5.3 Development of the retrieval engine for predictive maintenance components selection 87

5.4 Lessons learnt 95

6 Building a framework for predictive maintenance models selection 97

6.1 Making the parts work together 97

6.2 Enhancing predictive maintenance architecture process by using ontology-enabled Case-Based Reasoning (Article 4) 98

6.3 Cross-validation 107

6.4 Lessons learnt 108

7 Validation approach and discussion 109

7.1 Validating the proposed Decision Support System in a practical example 109

7.2 Use case example: Design of a predictive maintenance system for aircraft engine run-to-failure data set under real flight conditions 109

7.3 The concept phase of a predictive maintenance system for the N-CMAPSS database 111

7.4 Component selection using an ontology-enabled case-based recommendation system 113

7.5 Discussion 117

7.6 Lessons learnt from the DSS validation using the N-CMAPSS 119

8 Conclusion and perspective for future work 121

8.1 The journey is coming to an end, but a new one starts... 121

8.2 Lessons learnt 121

8.3 Limitations encountered 123

8.4 Contributions summary 124

8.5 Perspectives of future work 125

8.6 Epilogue 127

Bibliography 129

A A fault mode identification methodology based on self-organizing maps 147

B Ontology and CBR integration article 169

C DSS code Guide 179

D Summary in French /

Résumé en français 201

D.1 Introduction . . . . .

Intentionally left blank

## List of Figures

1.1 Generic stages in a system life cycle [INC15] 4

1.2 Solution space exploration using structured creativity. Inspired by [CCS15] 5

1.3 Thesis organization 8

Fig. 1. of Article 1. An overview of Maintenance strategies 12

Fig. 2. of Article 1. Functional decomposition for an example of predictive maintenance system 13

Fig. 3. of Article 1. Number of publications over the last 25 years related to prognostics and diagnostics in maintenance using three search terms in ScienceDirect 14

Fig. 4. of Article 1. Studies distribution for diagnostics and prognostics considering the consulted papers for the second search step 14

Fig. 5. of Article 1. Relationship among Predictive Maintenance, CBM and PHM 15

Fig. 6. of Article 1. Basic Rule-Based System 15

Fig. 7. of Article 1. The case-based reasoning cycle 16

Fig. 8. of Article 1. An example of degradation analysis based on series of data 18

Fig. 9. of Article 1. Potential combinations for multi-model approaches 24

Fig. 10. of Article 1. Generic basic configurations for multi-model approaches 24

Fig. A1. of Article 1. Systematic literature review protocol 25

Fig. 1. of Article 2. Functional, behavioral, structural and experiential requirements 34

Fig. 2. of Article 2. Arcadia method layers summary 35

Fig. 3. of Article 2. Functional decomposition for the predictive maintenance system 37

Fig. 4. of Article 2. Functional architecture for a predictive maintenance system concept 38

Fig. 5. of Article 2. External interfaces of the predictive maintenance system 38

Fig. 6. of Article 2. Generic Logical Architecture for a Predictive maintenance off-line system 39

3.1 An approach to developing a system architecture in the concept stage 42

4.1 Case-Based Reasoning based on a vocabulary framework [Alt+12] 44

4.2 Semantic triple structure with examples 45

Fig. 1. of Article 3. Maintenance strategies maturity model . . . . .

7.2 The logical architecture of a predictive maintenance system for the N-CMAPSS data set . 113

7.3 Correlation matrix of the sensors of the N-CMAPSS data set to be used as input for the SOM117

7.4 Trained SOM for the sub-set DS01 . 118

D.1 Étapes génériques du cycle de vie d’un système (traduit de l’anglais) [INC15] . 203

D.2 Nombre de publications liées à la maintenance prédictive au cours des 25 dernières années 205

D.3 Combinaisons possibles de modèles de maintenance prédictive . 206

D.4 Étapes abordées dans l’approche d’ingénierie des systèmes pour la conception de systèmes de maintenance prédictive . 208

D.5 Raisonnement basé aux cas, développé sur un cadre de vocabulaire [Alt+12] . 209

D.6 Classes et relations dans OPMAD . 211

D.7 Cycle de raisonnement basé aux cas, image inspirée par [AP94] . 212

D.8 Analogie entre le raisonnement basé au cas et les tâches effectuées par un concepteur de systèmes, en notation Capella [Roq18] . 216

D.9 Idée conceptuelle d’incorporation de DSS pour la sélection des composants du système . 216

D.10 Exemple de reprise de dossier à l’aide de l’interface DSS . 217

D.11 Carte auto-organisatrice formée avec l’étude de cas N-CMAPSS . 219

E.1 Etapas genéricas del ciclo de vida de un Sistema (en inglés) [INC15] . 225

E.2 Número de publicaciones relacionadas con mantenimiento predictivo en los últimos 25 años.227

E.3 Posibles combinaciones de modelos de mantenimiento predictivo. . 228

E.4 Pasos abordados en el enfoque de ingeniería de sistemas para el diseño de sistemas de mantenimiento predictivo . 230

E.5 Razonamiento basado en casos desarrollado sobre un marco de vocabulario [Alt+12] . 231

E.6 Clases and relaciones en OPMAD . 233

E.7 Ciclo de razonamiento basado en casos, ilustración inspirada en [AP94] . 234

E.8 Analogía entre razonamiento basado en casos y las tareas que realiza un diseñador de sistemas, en notación Capella [Roq18] . 237

E.9 Idea conceptual de la incorporación del DSS para la selección de componentes de sistemas 238

E.10 Ejemplo de recuperación de caso usando la interfaz del DSS . 239

E.11 Mapa auto-organizativo entrenado con el caso de estudio N-CMAPSS . 241

Intentionally left blank

## List of Tables

Table 1. of Article 1. Distribution of publications per model from 2015 to 2019 in the systematic literature review on Predictive maintenance 14

Table 2. of Article 1. Summary of identified applications for knowledge-based models in this systematic literature review 17

Table 3. of Article 1. Summary of identified applications of statistical models in predictive maintenance 19

Table 4. of Article 1. Summary of identified studies applying stochastic models for predictive maintenance 19

Table 5. of Article 1. Summary of identified applications for machine learning models 20

Table in Appendix B of Article 1. Summary of previous reviews 25

Table 1 of Article 2. Requirements writing format 35

Table 2 of Article 2. Potential stakeholders 36

Table 3 of Article 2. Example of needs and desires list 36

Table 4 of Article 2. Example of initial list of stakeholder' requirements 36

Table 5 of Article 2. Summary of potential techniques for logical components 39

Table 1 of Article 3. The identifier for the terms sources 58

Table 2 of Article 3. Definitions for important classes to describe the condition of an item 59

Table 3 of Article 3. Definitions of the terms in Fig.5 and Fig.6. 60

Table 4 of Article 3. Definitions of classes related to FMECA, cost-benefit-risk analysis, and maintenance reports used for maintenance strategies selection and assessment 64

Table 5 of Article 3. Prefixes to perform SPARQL queries on OMSSA 67

Table 6 of Article 3. SPARQL query to answer the first competency question on Compressor Unit 1 67

Table 7 of Article 3. SPARQL Query to answer the competency questions for the failure mode "Crank damage" 68

Table in Appendix A of Article 3. Relations used in OMSSA 73

4.1 Terms of the Ontology for Predictive Maintenance Architecture and Design. 76

5.1 Similarity functions assignation 93

5.2 OPMAD classes and corresponding variables in the retrieval engine 96

7.1 Overview of N-CMAPSS data set [Cha+21] 112

7.2 Models retrieval for the N-CMAPSS examples 115

7.3 Operational Measurements N-CMAPSS 116

D.1 Affectation des fonctions de similarité 214

E.1 Asignación de funciones de similitud 236

## Table of acronyms

AI Artificial Intelligence

BFO Basic Formal Ontology

CBM Condition-Based Maintenance

CBR Case-Based Reasoning

CCO Common Core Ontologies

DSS Decision Support Systems

EN European Standard

FMECA Failure Mode, Effects and Critical Analysis

FPM Failure Propagation Model

GUI Graphical User Interface

HPC High-Pressure Compressor

HPT High-Pressure Turbine

IEC International Electrotechnical Commission

INCOSE International Council on Systems Engineering

ISO International Organization for Standardization

LPC Low-Pressure Compressor

LPT Low-Pressure Turbine

LSTM Long-Short Term Memory

NASA National Aeronautics and Space Administration

NF Norme Française

NN Neural Network

OMSSA Ontology for Maintenance Strategy Selection and Assessment

OPMAD Ontology for Predictive Maintenance Architecture and Design

OWL2 Web modelling language Version 2

PhD Doctor of Philosophy

PHM Prognostics and Health Management

PdM Predictive Maintenance

RBR Rule-Based Reasoning

RDF Resource Description Framework

RNN Recurrent Neural Network

SDK Software Development Kit

SOM Self Organizing Map

SVM Support Vector Machine

SysML Systems Modelling Language

W3C World Wide Web Consortium

## Introduction

<table border="1"><tr><td></td><td></td><td>A daring beginning is halfway to winning.</td></tr><tr><td></td><td></td><td>Heinrich Heine</td></tr><tr><td>Content</td><td></td><td></td></tr><tr><td>1.1</td><td>The journey begins</td><td>1</td></tr><tr><td>1.2</td><td>Maintenance</td><td>2</td></tr><tr><td></td><td>1.2.1 Corrective Maintenance</td><td>2</td></tr><tr><td></td><td>1.2.2 Preventive Maintenance</td><td>3</td></tr><tr><td></td><td>1.2.3 Predictive Maintenance</td><td>3</td></tr><tr><td>1.3</td><td>Systems concept stage and the system architecture process</td><td>4</td></tr><tr><td>1.4</td><td>Research statements</td><td>5</td></tr><tr><td>1.5</td><td>Organization of the thesis</td><td>6</td></tr></table>

## 1.1 The journey begins

After some years working in the industry in maintenance and subsequently in a research project specifically on predictive maintenance during the M.Sc. in Aerospace Engineering program at ISAE-SUPAERO, my passion and curiosity for the topic drove me to make the decision to continue my research in predictive maintenance and undertake a three-year program to opt for the degree of Doctor of Philosophy (PhD). It was a big challenge at a personal and professional level. Close to the end of the experimentation, one of my thesis advisors shared with me the above-mentioned quote from Heinrich Heine and it made me remember the big bet I made when I decided to start a PhD. The research work consolidated in the current manuscript testifies to the bet I made was fully worth it.

This chapter aims at introducing the context and the motivations for this research which is developed around two main topics: predictive maintenance and systems architecture. On one hand, predictive maintenance is seen as a strategy in the maintenance field which is carried out by specialized systems. On the other hand, systems architecture is part of a concept design stage of complex systems. The principles of systems architecture are applied to enhance the design of predictive maintenance systems.

## 1.2 Maintenance

Maintenance is one of the most important activities during the life cycle of assets to ensure their functionality. It is possible to illustrate the term with basic examples, like a person changing a wheel of a car, or with the most complex ones which could be the use of high technology techniques to predict faults in a critical component of a system. Defining the word maintenance is not simple. The European standard NF EN 13306 X60-319 [Eur09] gives a complete definition that addresses the different aspects of maintenance; one can understand maintenance as "all of technical, administrative and management activities throughout the life cycle of an asset in order to maintain or restore it to the state where it can perform the intended functions".

Moreover, maintenance is strongly related to other important aspects in industry, such as risks in safety, costs, and image and in the end profits for any company. An example of this can be the delay or cancellation of a flight due to technical problems. The customers are ready to take their flight, and a little time before the departure, they receive a notification that the flight has been delayed due to a malfunctioning of the engine and it may last three hours to be evaluated. At this moment, all the customers receive a meal ticket in compensation for the flight's delay which means an unexpected cost. The customers wait three hours and then the airline informs that the fault is worse than expected, it affects directly the safety of the flight, and finally it has been totally cancelled. The customers will demand reimbursement or even higher compensation. The customers can eventually look for another airline to fly to their destination. It is possible that next time these customers will choose a different airline and will share their bad experience with other people, directly affecting the image or prestige of the company.

Considering these kinds of circumstances, proper maintenance should be applied in industry, at the right moment, not too early as it engages high costs and not too late as it increases the risk of failures. There are different strategies that will define the right moment to trigger maintenance actions depending on the risk of an eventual failure.

Maintenance strategies can have different classifications. One of the best-known taxonomies divides maintenance into three main strategies: corrective maintenance, preventive maintenance, and predictive maintenance. A good combination of the three is what makes a system reliable, decreasing the maintenance costs. Some components of a maintainable system do not represent a major problem when they fail and a proactive strategy will not be justified for its implementation; these components will be run until failure following a corrective maintenance strategy. For some other components, an unexpected failure is not acceptable and for them, it is normal to find preventive maintenance strategies that will trigger maintenance actions based on operational intervals. For some critical components, specialized systems can be implemented to monitor their condition and trigger maintenance actions accurately when needed, following a predictive maintenance strategy. A brief introduction to these maintenance strategies is provided hereafter.

## 1.2.1 Corrective Maintenance

This is the oldest type of maintenance; it basically means to replace or repair a failed component of a system in order to restore it to its functional state [Vin+95]. Cavemen already replaced the broken stones of their axes and used tools to restore them. This type of maintenance is inherent to every system, there is no perfect system that can last forever and unfortunately, even for systems that use high technology in maintenance, it remains impossible to avoid unforeseen failures.

Despite that corrective maintenance is a classic strategy, it still is an important topic of research. For example, [FZ15] aims at analyzing the impact of failures in aircraft components in the maintenance and support costs. A good description of what activities are involved in corrective maintenance is provided.

These activities are: "malfunctioning location, malfunctioning isolation, replace, re-install, adjustment verification and fix the damaged parts".

Another recent corrective maintenance study [Wan+14] aims to provide corrective maintenance procedures for engineering equipment, using management based on Failure Modes, Effects and Critical Analysis (FMECA) and representing failure mechanisms using a failure propagation model (FPM). The authors propose a depth-based fault diagnosis and a failure risk metric; a binary decision tree can be built for failures ascertainment for corrective maintenance.

It is important not to confuse a corrective maintenance strategy with corrective maintenance due to an unexpected failure [Hod+21]. When corrective maintenance strategies are assigned to a specific component or maintainable system, a complete analysis has been carried out concluding that the most efficient manner to trigger maintenance actions is when the failure occurs. This kind of failure does not represent a significant impact on the maintainable system. In contrast, corrective maintenance due to an unexpected failure often catches maintenance staff unprepared and it is often the most detrimental in terms of safety and costs. For these cases then preventive and predictive maintenance strategies offer an alternative at increasing the reliability and safety by triggering maintenance actions before a failure happens.

## 1.2.2 Preventive Maintenance

Preventive maintenance is carried out at predetermined intervals or according to prescribed criteria and intends to reduce the probability of failure or the degradation of the functioning of a maintainable system [Leg+17]. Preventive maintenance can also be seen as a set of activities aimed at improving the reliability and availability of a system by triggering maintenance actions before a failure occurs, for instance, based on operational intervals [MU11]. Traditional activities related to preventive maintenance are inspection, cleaning, lubrication, adjustment, alignment, and/or replacement of sub-components that wear out.

The aim of this strategy is to prevent failures to occur. Maintenance actions are defined with corresponding intervals or thresholds (e.g., after a certain time, cycles, rounds, distance). Preventive maintenance implies planned shutdowns which normally are shorter than the unplanned shutdowns which are present in the corrective maintenance. The maintenance action will be triggered when the component reaches the predetermined operational interval threshold even if the component in appearance is in operational condition. Recent trends in preventive maintenance are focused on the optimization of intervals between maintenance actions.

## 1.2.3 Predictive Maintenance

Predictive maintenance (PdM) proposes an alternative strategy to preventive maintenance. Sometimes preventive maintenance actions are triggered too early so the component is still in good operational conditions and could have worked a longer period. Or too late so that an unexpected failure occurs. Consequently, the maintenance action impacts negatively the maintenance costs, even more for a modern industry where the products and equipment are more and more complex, and thus, require higher reliability and better quality. "Eventually preventive maintenance has become a major expense of many industrial companies" [JLB06]. Then, predictive maintenance was born as a solution to define the right maintenance threshold, to monitor the condition of the components, and trigger maintenance action accurately when needed, not too early so that it increases the maintenance costs of a company but not too late so that a failure occurs.

Predictive maintenance is strongly related to Condition-Based Maintenance (CBM) and Prognostics and Health Management (PHM). The three terms address diagnostics and prognostics for maintenance

purposes up to the point that the terms are used as if they were synonyms. Predictive maintenance and Condition-Based Maintenance seem to appear simultaneously around the 1940s. Both terms refer to the maintenance strategy that aims at anticipating failures of machines based on their condition. However, it is not before the early 1990s that this strategy has taken on importance thanks to the implementation of monitoring systems and computational tools able to carry on with the diagnostics tasks. Prognosis was always an inaccurate discipline and even when it is mentioned in predictive maintenance and CBM it remained an unsolved problem. In the early 2000's PHM discipline emerged aiming to cover the gap in prognosis. For the last 20 years, the research in diagnosis and prognosis for maintenance has earned a lot of attention from academy and industry, thanks to the continuous increments in computational power and given the benefits of their implementation. Over the last decade, different contributions have been made under the different terms (predictive maintenance, CBM and PHM) and refer to the same field of research.

## 1.3 Systems concept stage and the system architecture process

According to the INCOSE Handbook [INC15], the life cycle of a system can be divided into six generic stages (see Figure 1.1). The system life cycle starts with the concept stage which aims at exploring possible solutions to meet the initial stakeholders' needs. The concept stage is followed by the development stage in which a detailed design of the system components and their interfaces takes place. After the detailed design, the production stage begins; it is dedicated to the system implementation, meaning the fabrication, coding, creation of the different components and their integration in the whole system. Verification and validation of the system are part of the production stage. Once the system has been validated, it is delivered to the client for its utilization stage. In the utilization stage, the system performs the function for which it was created. The maintenance stage goes in parallel with the utilization stage during the system operation. This maintenance stage aims at keeping the system at its optimal operation. At the end of the system life cycle, the disposal stage aims at managing properly the system residuals when it is taken out from the operation.


> **Figure Description:**

The image is a table consisting of a single row divided into five columns. The first column contains the text "Concept stage". The second column contains the text "Development stage". The third column contains the text "Production stage". The fourth column is split into two stacked cells, with "Utilization stage" in the top cell and "Support stage" in the bottom cell. The fifth column contains the text "Retirement State".



<div align="center">

Figure 1.1: Generic stages in a system life cycle [INC15]

</div>

The concept stage starts by gathering all needs and desires from the stakeholders and formalizing them into stakeholder requirements. These requirements are then used for the creation of the system architecture that will serve as a basis for the detailed design and implementation of the system. The development of the architecture can be divided into three levels [Roq18]; [INC15]: functional architecture, logical architecture and physical architecture. The functional architecture describes how the different sub-functions of a system interact to fulfil a specific objective but does not provide any detail about the components that fulfil each sub-function. The logical architecture provides as much detail as possible of the architecture components and their interfaces but not engaging to any specific technology, meaning that the logical architecture remains generic. The physical architecture provides the details of the technologies that will fulfil each logical architecture component. The union of these three architecture levels can be called as the system architecture and can be then defined as the "fundamental concepts or properties of a system in its environment embodied in its elements, relationships, and in the principles of its design and evolution" [ISO11]. In simple words, architecture is how a set of elements, which could be physical or informational, are organized to fulfil a specific objective.

Creativity plays a vital role in the architecture process, especially when identifying and selecting suitable components to fulfil the logical architecture. This creativity can be non-structured or structured [CCS15].

On one hand, non-structured creativity is based on unconscious processing, an immediate vision of the solution for a problem. However, this creativity process narrows down the solution space and does not always lead to the "best" possible solution. On the other hand, structured creativity follows a method to explore the design space considering the initial function or functions to be fulfilled. An example of structured creativity methods is the components recombination. It supposes that there is more than one option per component available. Different concepts of the system (possible solutions) are obtained by making as many combinations of the possible options of each component. Some of the combinations might not be feasible, some of them might be traditional solutions that are already known, but some others can be innovative solutions that have not been imagined before and at the same time can represent a better solution to fulfil the system requirements.

A conscious exploration of the solution space is necessary to carry out structured creativity for the architecture process. All possible options for each component must be known so that innovative solutions can be determined. The solution space exploration can be a complex and long-lasting task, especially when there exist several options to fulfil the logical components. When applying structured creativity, the number of possible architecture solutions is directly linked to the options to fulfill each logical component. Figure 1.2 presents how the solution space evolves during the architecture process when performing structured creativity to identify innovative solutions. When the possible architectures are known, a trade-off analysis starts to narrow down the solution space by eliminating all non-feasible options and by assessing the feasible ones considering performance indicators and constraints identified in the initial requirements. In the end, the goal is to have one selected architecture from which the detailed design begins. There could be also the case that more than one architecture is selected to continue to the detailed design, but the number remains limited for resources, time, and budget limitations.


> **Figure Description:**

This diagram illustrates a design process using a diamond-shaped model to represent the expansion and contraction of the solution space. At the top, a small blue circle labeled "Initial concept" marks the starting point. A long vertical arrow on the left side points downward, labeled "Solution space exploration using structure creativity," indicating the progression of the process.

The central diamond shape is composed of a series of horizontal ellipses that grow in width from the top down to the center, and then narrow again toward the bottom, ending in a small blue circle labeled "Selected architecture." To the right of the diamond, two diagonal arrows indicate the phases of the process. The first arrow points from the top toward the widest part of the diamond and is labeled "Functional decomposition, Component identification and allocation," which leads to the text "Possible architecture solutions" positioned near the widest section. The second arrow points from the widest section toward the bottom and is labeled "Trade-off analysis for the architecture based on the behavioral, structural and experiential requirements."



<div align="center">

Figure 1.2: Solution space exploration using structured creativity. Inspired by [CCS15]

</div>

## 1.4 Research statements

Predictive maintenance is carried out by specialized systems to perform diagnostics and prognostics tasks and determine the right moment to trigger maintenance actions. The design and development of such

specialized systems is still based on trial and error. There exist several generic architectures in norms and standards, such as for example [MIM01], but the design of a new system starts long ago in the concept stage. A generic architecture does not provide a link to the initial needs and desires for a new predictive maintenance systems and often, these needs and desires are not met with a generic architecture. Besides, a generic architecture does not provide any guidelines to select the suitable technologies that can fulfil the generic components it proposes [MV19].

Predictive maintenance addresses diagnostics and prognostics tasks. But not every predictive maintenance system covers the same functions, for example a new predictive maintenance system may be intended to perform diagnostics in different components of a system and several diagnostics modules of the same type will be needed and no prognostics modules would be included. Generic architectures do not provide a systematic approach to design systems that need only a subset of their proposed components or when several components of the same type are needed.

There exists an important number of options to fulfil the diagnostics and prognostics functions in a predictive maintenance system, and there is no guidelines to help the architect select the suitable models, techniques, or algorithms that can carry out these functions. The exploration of the solution space to determine the suitable components can then be complex and long-lasting. This thesis aims at facilitating the architecture process of predictive maintenance systems by enabling a more efficient way to explore the solution space and propose the most suitable components for the system architecture.

Before deepening in the design of predictive maintenance systems, it is important to understand the research field of predictive maintenance itself and the different available options to perform diagnostics and prognostics. The following research questions are proposed to guide the state-of-the-art study in this topic:

1. What are the current trends in diagnostics and prognostics in predictive maintenance?

2. What kind of models, techniques or methods are used to address diagnosis and prognosis in predictive maintenance?

3. What are the main challenges facing predictive maintenance in diagnostics and prognostics?

After the state-of-the-art study, the research questions are refined according to the study findings and the initial motivation of this research related to the design of predictive maintenance systems (see Chapter 2).

## 1.5 Organization of the thesis

The following manuscript is organized in eight different chapters. The purpose of this section is to explain the structure of the message along with the different chapters. The structure of the thesis is summarized in Figure 1.3.

Chapter 2 addresses the state-of-the-art of predictive maintenance based on the initial research questions introduced in this chapter. This chapter is composed of a published article that includes the current trends in models for diagnostics and prognostics in the maintenance field. The chapter ends by refining the research questions that motivated the rest of the research.

Chapter 3 proposes a systems engineering approach to predictive maintenance design, specifically in the concept stage from the gathering of the initial needs and desires from the stakeholders until the proposal of a logical architecture. The logical architecture remains generic as no specific technology has been chosen to fulfil the architecture components. The chapter is composed of a published conference article and it ends by

presenting the predictive maintenance component selection as the main challenge that will be addressed in the following chapters. A Decision Support System (DSS) that combines ontologies and Case-Based reasoning is proposed as a possible solution to address the component selection in the systematic approach.

Chapter 4 explains one of the building blocks of the Decision Support System: ontologies. Complementary research has been performed specifically on ontologies that have turned out in a journal article, accepted for publication at the time this manuscript was written. The theoretical background of ontologies is introduced, highlighting their importance in the research community due to their capabilities to formally model domain vocabulary and perform reasoning with it. The chapter explains the development of the ontology that is later used in the DSS for component selection.

Chapter 5 explains the second building block of the DSS: Case-Based Reasoning (CBR). The principles of the CBR paradigm are introduced including the phases of the CBR cycle. In a first attempt, the DSS is focused in the retrieval phase of CBR. An explanation of the implementation of the CBR retrieval engine using open source code is provided.

Chapter 6 explains the general framework of the integration of the building blocks of the DSS and how it fits in the systematic approach to design predictive maintenance systems. The chapter is composed of a published conference article which is the continuation of the article presented in Chapter 2. Cross-validation is performed to demonstrate the DSS capabilities.

Chapter 7 is intended to further validate the DSS. A case study is selected to develop the complete approach proposed in the current research and based on the DSS suggestions one example is implemented. The results of this implementation are explained and discussed.

Chapter 8 concludes the thesis by summarizing the lessons learned, enumerating the limitations encountered during the research, and listing the perspectives of future work.


> **Figure Description:**

This diagram is a flowchart illustrating the structure of a research paper across eight chapters, with each chapter represented by a rounded rectangle connected by downward-pointing arrows. To the right of each chapter box, a curly bracket links the chapter title to a brief description of its content.

Chapter 1 is titled "Chapter 1. Introduction," and its corresponding description is "Presentation of the research topic, motivations and research objectives." Chapter 2 is titled "Chapter 2. State of the art predictive maintenance," and its description is "Analysis of the recent research trend in predictive maintenance and refinement of research questions." Chapter 3 is titled "Chapter 3. Concept stage of predictive maintenance systems," and its description is "Proposed framework to address the concept stage of PdM systems from needs and desires until logical architecture."

Chapter 4 is titled "Chapter 4. Ontologies," and its description is "Ontologies as one of the building blocks of the framework for component selection." Chapter 5 is titled "Chapter 5. Case-based reasoning," and its description is "CBR as one of the building blocks of the framework for component selection." Chapter 6 is titled "Chapter 6. DSS framework," and its description is "Proposed framework for predictive maintenance component selection."

Chapter 7 is titled "Chapter 7. Example implementation," and its description is "Validation of the proposed DSS." Finally, Chapter 8 is titled "Chapter 8. Conclusion," and its description is "Lessons learnt, limitations encountered, perspectives of future work, epilogue."



<div align="center">

Figure 1.3: Thesis organization

</div>

<div align="center">

# Towards multi-model approaches to predictive maintenance: A systematic literature survey on diagnostics and prognostics

</div>

"L'homme ne peut découvrir de nouveaux océans tant qu'il n'a pas le courage de perdre de vue la côte."

"Man cannot discover new oceans unless he has the courage to lose sight of the shore."

## Content

André Gide

2. 1 Exploring the topic and defining the state-of-the-art 9

2. 2 Towards multi-model approaches to predictive maintenance: A systematic literature

survey on diagnostics and prognostics (Article 1) 10

2. 3 Lessons learnt 30

## 2.1 Exploring the topic and defining the state-of-the-art

Predictive maintenance has been one of the motivations of the current research. It is an important topic in which several academic laboratories and private enterprises have focused sharply because of its potential benefits. This chapter aims at determining the state-of-the-art in predictive maintenance, defining the techniques and models that can be used for diagnostics and prognostics of maintainable systems. The state-of-the-art allows understanding the current challenges that predictive maintenance faces. These challenges are the source of knowledge to refine the research questions that the rest of the thesis attempts to answer.

The following state-of-the-art study is based on the following research questions:

1. What are the current trends in diagnostics and prognostics for predictive maintenance?

2. What kinds of models, techniques or methods are used to address diagnosis and prognosis in predictive maintenance?

3. What are the current challenges facing predictive maintenance in diagnostics and prognostics?

2. 2 Towards multi-model approaches to predictive maintenance: A systematic literature survey on diagnostics and prognostics (Article 1)

The content in this section corresponds to a published work in the Journal of Manufacturing Systems. $ \circled{C} $ Elsevier 2020. Reprinted, with permission, from Juan José Montero Jimenez, Sebastien Schwartz, Rob Vingerhoeds, Bernard Grabot, Michel Salaun. "Towards multi-model approaches to predictive maintenance: A systematic literature survey on diagnostics and prognostics". Journal of Manufacturing Systems Vol.56 (2020), pp. 539-557 [Mon+20]. This article is referred to as Article 1 in the current manuscript.





<div align="center">

# Towards multi-model approaches to predictive maintenance: A systematic literature survey on diagnostics and prognostics

</div>


> **Figure Description:**

Brand icon



Juan José Montero Jimenez $ ^{a,b,*} $ , Sébastien Schwartz $ ^{a,c} $ , Rob Vingerhoeds $ ^{a} $ , Bernard Grabot $ ^{d} $ Michel Salaun $ ^{a} $

a ISAE-SUPAERO, Université de Toulouse, 10 Avenue Edouard Belin, 31400, Toulouse, France

b TEC-Tecnológico de Costa Rica, Calle 15, Avenida 14, 1 km Sur de la Basílica de los Ángeles, Provincia de Cartago, Cartago, 30101, Costa Rica

c Capgemini DEMS, R&D Dpt., Aeropark, 3 Chemin de Laporte, 31100, Toulouse, France

d ENIT- INP Toulouse, 47, avenue d'Azereix, BP 1629, 65016, Tarbes, France

## ARTICLE INFO

Keywords:

Predictive maintenance

Systematic literature review

Diagnostics

Prognostics

Single-model approaches

Multi-model approaches

## ABSTRACT

The use of a modern technological system requires a good engineering approach, optimized operations, and proper maintenance in order to keep the system in an optimal state. Predictive maintenance focuses on the organization of maintenance actions according to the actual health state of the system, aiming at giving a precise indication of when a maintenance intervention will be necessary. Predictive maintenance is normally implemented by means of specialized computational systems that incorporate one of several models to fulfil diagnostics and prognostics tasks. As complexity of technological systems increases over time, single-model approaches hardly fulfil all functions and objectives for predictive maintenance systems. It is increasingly common to find research studies that combine different models in multi-model approaches to overcome complexity of predictive maintenance tasks, considering the advantages and disadvantages of each single model and trying to combine the best of them. These multi-model approaches have not been extensively addressed by previous review studies on predictive maintenance. Besides, many of the possible combinations for multi-model approaches remain unexplored in predictive maintenance applications; this offers a vast field of opportunities when architecting new predictive maintenance systems. This systematic survey aims at presenting the current trends in diagnostics and prognostics giving special attention to multi-model approaches and summarizing the current challenges and research opportunities.

## 1. Introduction

The use of a modern multi-technological system requires a good engineering approach, optimized operations, and proper maintenance in order to keep the system in an optimal state of operation. Predictive maintenance focuses on the organization of maintenance actions according to the actual health state of the system, aiming at giving a more precise indication of when a maintenance intervention will be necessary. This is performed by using specialized models and techniques that make possible to perform diagnostics and prognostics over the multitechnological system health state.

Predictive maintenance research has a lot of attention in industry and academy due to its potential benefits in terms of reliability, safety and maintenance costs among many other benefits. As explained by [1], predictive maintenance might reduce maintenance costs by 25%-35% eliminate breakdowns by 70%-75% ,reduce breakdown time by 35

%-45 %, and increase production from 25 %-35 %. These percentages do not consider important aspects such as system safety and company image.

This article aims at performing a systematic literature review on predictive maintenance, the state of the art on the models used for diagnostics and prognostics, the current challenges, and new potential opportunities of research. Fast expanding trends such as Industry 4.0 boost the use of predictive maintenance, and the interest on the topic remains increasing. Recent reviews mainly focus on a limited scope: prognostics and data-driven models, as for example [2-4]. This motivates an update of the reviews as every year hundreds of publications related to the topic are published.

The methodology to perform the literature review is based on [5] and concerns a systematic literature review methodology that aims at summarizing the existing work of a specific topic. The systematic literature review helps to carry out the literature review process in a

<div align="center">

# Author's Personal Copy

</div>

structured manner so to obtain a better overview of the subject under study. The systematic literature review protocol includes four main parts: research questions definition, search strategy, study selection, and data synthesis. The research questions are:

- RQ1: What are the current trends in diagnostics and prognostics for predictive maintenance?

- RQ2: What kinds of models, techniques or methods are used to address diagnosis and prognosis in predictive maintenance?

- RQ3: What are the current challenges facing predictive maintenance in diagnostics and prognostics?

The search was divided into two steps; the first one was aimed to check the previous literature reviews on predictive maintenance so to understand the evolution of the topic over the last years. This first search step also helped to identify the model types used for diagnostics and prognostics: knowledge-based, data-driven, physics -based and multi-model approaches. The second search step is based on trial searches using various combinations of search terms derived from the research questions so to identify the main trends in the different models for diagnostics and prognostics. Special attention is given to multimodel approaches, as these models present a promising opportunity to overcome current challenges in predictive maintenance applications. For example, more than one model could be used to address different sources of heterogeneous data, complementary models could be used to reduce uncertainty and improve accuracy on diagnostics and prognostics (see Sections 6 and 7). For both search steps, four sources were consulted: IEEE Xplore, ScienceDirect, Springer and Web of Science. The selection of studies was performed accordingly to the research questions. An assessment on each publication was performed considering the clearness of research objectives, the explanation of proposed model results and the case studies completeness. Appendix A offers further explanation of the structured literature review process followed for this survey.

The rest of the paper is organized as follow: Section 2 introduces predictive maintenance. Section 3 shows some statistics from the systematic literature review. Section 4 shows the findings of the first search step on previews reviews of the topic. Section 5 explains the main single-model approaches identified in the current literature review. Section 6 addresses the multi-model approaches. Section 7 summarizes the identified challenges for predictive maintenance as potential opportunities for future research. Section 8 concludes the current systematic literature review.

## 2. Predictive maintenance

Within the maintenance strategies to trigger maintenance actions, three terms are commonly applied: corrective maintenance, preventive maintenance and predictive maintenance. Corrective maintenance triggers the maintenance actions once the failure of a component or system has occurred. Preventive maintenance uses intervals of time such as cycles, kilometres, flights, etc. to determine the right moment to trigger the maintenance actions. As explained by [6], the existence of faults is frequently unknown in preventive maintenance. This may lead to replacing components with still remaining useful life, which may be costly. Predictive maintenance can be presented as a maintenance strategy aiming at defining the accurate moment to trigger actual maintenance actions [7]. Too early interventions could represent a waste of resources by changing components with an important Remaining Useful Life (RUL), too late interventions could lead to catastrophic failures. As strategy, predictive maintenance is complementary to corrective and preventive maintenance. Predictive maintenance finds its bases in using specialized techniques and tools to identify the existence of faults on the technical systems and forecast their remaining useful life. A combination of the three mentioned strategies is needed to reach an efficient maintenance management [7].

Predictive maintenance has the goal of improving maintenance activities, performance, safety and reliability [8]. It is a vast topic with two main scopes diagnostic and prognostic. Diagnostics aims at detecting faults, determining their root cause and determining the current health state of the system to prevent unexpected failures. Prognostics are dedicated to predictions of future states of the system and the remaining useful life. Diagnostics and Prognostics can be performed online or off-line. In online applications, data is gathered, processed and analysed in real time to generate alarms or trigger maintenance or adjustment action while the system is running. Off-line applications focus on gathering all operational information to be analysed later (offline) by the maintenance team. They are not constrained by online realtime limitations [9].

Predictive maintenance is not a new topic. Some studies like [10] state that predictive maintenance already existed in the 1940's and during the current systematic literature review, publications from the 1970's were easily found [11]. However, the last 25 years show a growth of interest of the topic year by year. Two extensions of predictive maintenance are found in literature: Condition-Based Maintenance (CBM) and Prognostics and Health Management (PHM). According to [10], CBM was also introduced in the 1940's while PHM is the most recent term, introduced in the early 2000's [12]. These terms frequently substitute predictive maintenance in literature and there is no consistency on how these terms are used or how they fit together in


> **Figure Description:**

This diagram illustrates a hierarchical classification of maintenance strategies, enclosed within a large dashed-line border labeled "Maintenance Strategies" at the top. The strategies are divided into two primary categories: "Before failure" and "After failure." The "After failure" section, enclosed in a dotted-line box, contains a single box labeled "Corrective."

The "Before failure" section is further divided into two main sub-categories: "Scheduled" and "Health monitoring and management." The "Scheduled" category, enclosed in a dotted-line box, contains a "Classification corrective-preventive-predictive" dashed-line box, which includes a "Preventive" box. Below this, a "Classification time-condition" dashed-line box contains a "Time-based" box. The "Preventive" box is connected by lines to both the "Time-based" box and a "Condition-Based" box.

The "Health monitoring and management" category, also enclosed in a dotted-line box, contains a "Predictive" box. This "Predictive" box is connected by a downward line that branches to connect to both the "Condition-Based" box and a "Prognostics and Health management" box. The "Time-based" and "Condition-Based" boxes are grouped together within the "Classification time-condition" dashed-line box, while the "Preventive" box is part of the "Classification corrective-preventive-predictive" dashed-line box. The entire "Before failure" area is contained within a larger dotted-line boundary.



<div align="center">

Fig. 1. An overview of Maintenance strategies.

</div>

the maintenance field. Over the last years, different contributions are made under different terms and refer to the same field of research. It has an impact on the current review. As result, the three terms were considered for the current review: predictive maintenance, CBM, and PHM. Fig.1 shows an overview of the maintenance strategies. Predictive maintenance is traditionally grouped along with preventive and corrective maintenance [10,13]. CBM is traditionally shown as a counterpart to time-based maintenance [14]. Besides these traditional classifications, Fig.1 shows a simple taxonomy which initially classifies the strategies between two categories with regards the maintenance actions triggering: before or after a failure occurs. For the strategies that trigger maintenance actions before failure there is sub-division between strategies with fixed schedule for maintenance actions and strategies that use health monitoring to decide the precise moment to trigger the maintenance actions. This last group includes the chosen strategies for this literature review. It is important to point out that Fig.1 is not a hierarchical diagram. The lines connecting the different strategies only represent the existence of important commonalities among the connected ones. The clarification of potential confusion in the use of these terms is out of the scope of the current review.

Predictive maintenance is normally implemented through specialized systems which collect data or information from the technical system for diagnostics or prognostics purposes. Norms and standards like OSA-CBM [15,16] offer a list of the traditional functional blocks of these predictive maintenance systems. Fig. 2 shows a functional decomposition of a predictive maintenance system for remaining useful life (RUL) estimation on one machine component subjected to a single failure mode. It shows the traditional functional blocks: collect data (F1), pre-process data (F2), detect and identify faults (F3), assess degradation (F4), compute RUL (F5) and make report (F6). These functional blocks may be present or not in a predictive maintenance system, they could be duplicated or modified depending on the system architecture which relays on the technical system complexity, the requirements for predictive maintenance system and the available knowledge, data and/or information [17]. According to the scope of this literature review, the models used for the functional blocks F3, F4 and F5 are addressed. It is important to point out that one or more models can be used to fulfil one single functional block, see also Section 6.

## 3. Survey process and some statistical results

The systematic literature review shows that predictive maintenance is gaining importance in the research community, especially over the last 25 years. To illustrate this, Fig. 3 shows the number of publications mentioning the terms "predictive maintenance", "condition based maintenance and "prognostics and health management" over the last 25 years in one of the consulted search sources (ScienceDirect). The tendency on IEEE Xplore, Springer and Web of Science is the same. The topic has a high importance in the research community; hundreds of articles are published every year with new contributions. It is important to mention that not all the papers mentioning the terms of interest are directly related to the scope of the current survey. The articles related to maintenance management practices, maintenance policies,

maintenance schedule optimization, are examples of topics discarded in the scrutinity process for this survey as they were out of scope.

During the first search step 23 survey articles were consulted (see Appendix B) to identify the models used for predictive maintenance and the evolution on the trends over the years. The taxonomies used to classify the different models for diagnostics and prognostics in predictive maintenance show slight variations on the terms from one study to another. Two main approaches can be extracted: single-model approaches and multi-model approaches. For single-model approaches there are three model types; for this survey these model types will be named knowledge-based models, data-driven models and physics-based models. Multi-model approaches combine at least two models from the three mentioned models types. Multi-model approaches may have different configurations and sometimes are called hybrid models; however, not all multi-model approaches should be referred to as hybrid (see Section 6).

The identified groups were the basis for the second search step. Following the mentioned taxonomy, Table 1 shows the distribution of consulted articles from 2015 to 2019. The survey also considered studies from previous years; however, due to the scrutiny process recent articles with similar scope and case study substituted older articles. The table shows that recent papers have been consulted to illustrate each category. Further explanation of model types, their current challenges and research opportunities are discussed in Sections 4,5 and 6. Data driven models are divided into three categories to be consistent with the taxonomy shown in Section 5. The three categories are: statistical models, stochastics models and machine learning models.

An important aspect is the distribution of the mentioned models between diagnostics and prognostics as main task for the consulted studies. In the end, out of the consulted articles in the second search step, 48.9 % were dedicated to diagnostics while 51.1 % to prognostics so that it is possible to say that they have equal share. Fig.4 shows the distribution of the consulted studies between single-model approaches and multi-model approaches for diagnostics (left part of Fig.4) and prognostics (right part of Fig.4), for all the consulted articles in the second search step. It is important to point out that diagnostics and prognostics are not always exclusive to each other. To perform prognostics is normal to have a previous diagnostic step to determine the current health state of the technical system to estimate future behaviours of the technical system. The main contribution presented by each consulted study in the second research step was considered to classify the scope between diagnostics and prognostics. For both, diagnostics and prognostics, single-model approaches are more presented than multi-model approaches. For diagnostics, knowledge-based models have a higher importance than for prognostics. Consulted studies on physics-based models were dedicated almost exclusively to prognostics. Data-driven models have the main part of consulted studies for diagnostics and prognostics.

## 4. Findings on the first search step

The first search step was dedicated to previous reviews on predictive maintenance and it helped to study the commonalities among


> **Figure Description:**

This diagram illustrates a hierarchical process flow with a primary objective at the top and six supporting functional steps below it. The central goal, contained within a large, rounded rectangular box at the top, is labeled "Estimate the precise moment to trigger maintenance actions." An upward-pointing arrow connects this top box to a horizontal line that branches downward into six individual, rounded rectangular boxes, each representing a specific functional task.

From left to right, the six functional boxes are labeled as follows: "Collect data (F1)," "Pre-process data (F2)," "Detect faults (F3)," "Assess degradation (F4)," "Compute RUL (F5)," and "Make report (F6)." Each of these six boxes is connected to the horizontal branch line by a vertical line, indicating that these six functions collectively support the primary objective of estimating the precise moment to trigger maintenance actions.



<div align="center">

Fig. 2. Functional decomposition for an example of predictive maintenance system, modified from [17].

</div>


> **Figure Description:**

This bar chart displays the number of publications per year from 1995 to 2019 for three categories: Predictive Maintenance (blue), Prognostics and health management (red), and Condition-based maintenance (green). The vertical axis represents the "Number of publications on which therms are found" ranging from 0 to 300 in increments of 50.

For each year, the publication counts are approximately as follows: In 1995, Predictive Maintenance is ~8. In 1996, Predictive Maintenance is ~8. In 1997, Predictive Maintenance is ~16, Condition-based maintenance is ~11. In 1998, Predictive Maintenance is ~38, Condition-based maintenance is ~11. In 1999, Predictive Maintenance is ~39, Condition-based maintenance is ~30. In 2000, Predictive Maintenance is ~42, Prognostics is ~4, Condition-based maintenance is ~43. In 2001, Predictive Maintenance is ~40, Prognostics is ~7, Condition-based maintenance is ~51. In 2002, Predictive Maintenance is ~44, Prognostics is ~5, Condition-based maintenance is ~45. In 2003, Predictive Maintenance is ~46, Condition-based maintenance is ~39. In 2004, Predictive Maintenance is ~38, Prognostics is ~4, Condition-based maintenance is ~46. In 2005, Predictive Maintenance is ~38, Prognostics is ~2, Condition-based maintenance is ~44. In 2006, Predictive Maintenance is ~62, Prognostics is ~17, Condition-based maintenance is ~94. In 2007, Predictive Maintenance is ~52, Prognostics is ~13, Condition-based maintenance is ~76. In 2008, Predictive Maintenance is ~64, Prognostics is ~24, Condition-based maintenance is ~90. In 2009, Predictive Maintenance is ~67, Prognostics is ~26, Condition-based maintenance is ~118. In 2010, Predictive Maintenance is ~68, Prognostics is ~38, Condition-based maintenance is ~119. In 2011, Predictive Maintenance is ~59, Prognostics is ~32, Condition-based maintenance is ~120. In 2012, Predictive Maintenance is ~99, Prognostics is ~50, Condition-based maintenance is ~194. In 2013, Predictive Maintenance is ~110, Prognostics is ~73, Condition-based maintenance is ~162. In 2014, Predictive Maintenance is ~87, Prognostics is ~58, Condition-based maintenance is ~183. In 2015, Predictive Maintenance is ~133, Prognostics is ~77, Condition-based maintenance is ~218. In 2016, Predictive Maintenance is ~156, Prognostics is ~96, Condition-based maintenance is ~222. In 2017, Predictive Maintenance is ~227, Prognostics is ~113, Condition-based maintenance is ~267. In 2018, Predictive Maintenance is ~266, Prognostics is ~110, Condition-based maintenance is ~244. In 2019, Predictive Maintenance is ~245, Prognostics is ~130, Condition-based maintenance is ~218.



<div align="center">

Fig. 3. Number of publications over the last 25 years related to prognostics and diagnostics in maintenance using three search terms in ScienceDirect.

</div>

<div align="center">

Distribution of publications per model from 2015 to 2019 in the systematic literature review on Predictive maintenance.

</div>

<table border="1"><tr><td>Approach</td><td>Model type</td><td>Models</td><td>2015</td><td>2016</td><td>2017</td><td>2018</td><td>2019</td></tr><tr><td rowspan="3">Single-model approaches</td><td>Knowledge-based models</td><td>Rule-based, Case-based, and fuzzy models</td><td>[18-20]</td><td>[21]</td><td>-</td><td>[22-24]</td><td>[25-28]</td></tr><tr><td>Data-driven models</td><td>Statistical, stochastic and machine learning models</td><td>[29-33]</td><td>[34-37]</td><td>[38-49], [83,84]</td><td>[50-62,7,63-75]</td><td>[76-81]</td></tr><tr><td>Physics-based models</td><td>Laws of physics governing the degradation of the system.</td><td>-</td><td>[82]</td><td>[83,84]</td><td>[85]</td><td>[76,78,86]</td></tr><tr><td>Multi-model approaches</td><td>Different configurations</td><td>Combination of two or more models.</td><td>-</td><td>[87]</td><td>[88]</td><td>[69]</td><td>[76,78,89-94]</td></tr></table>

the terms "predictive maintenance", "condition-based maintenance" (CBM) and "prognostics and health management" (PHM). The use of these terms is not homogeneous in literature. Sometimes CBM and PHM are presented as if they were synonyms to predictive maintenance [95,96], while other studies shown CBM and PHM as extensions or subdivisions of predictive maintenance [6,10,97-99]. Opposite statements are also found clustering predictive maintenance as sub-part of CBM [100]. The three terms were developed by different research communities and today many contributions concern similar maintenance activities done under different names. None of the consulted reviews presents an alignment of the three terms in the same study.

Trying to align these terms, this survey adopts predictive maintenance as the first term to refer the maintenance strategy. CBM is

suggested as an extended version of predictive maintenance where alarms are added to warn when the system has overpassed predetermined thresholds. CBM has been used as preferred term to describe diagnostics tasks in norms [99,101] and in some referential books such as [102]. Likewise, PHM is suggested as an extension of CBM as an answer to the need to improve on predictability and life cycle management of the assets [100,102,103]. Fig. 5 shows a summary of the evolution on the use of the terms considering the consulted reviews. When performing literature research, it is then worthy to consider the three terms.

Besides a general notion of the terminology, the first search step of the current survey allowed the study of evolution of the research trends on the topic. Out of the 22 consulted reviews, the first one dates from


> **Figure Description:**

This image is a pie chart illustrating the distribution of various diagnostic and prognostic modeling approaches. The chart is divided into eight segments, each corresponding to a category listed in the legend to the right. The legend entries, from top to bottom, are: Diagnostics - Knowledge-Based Models (dark blue), Diagnostics - Data-Driven Models (red), Diagnostics - Physics-based Models (green), Diagnostics - Multi-model approaches (purple), Prognostics - Knowledge-Based Models (teal), Prognostics - Data-Driven Models (orange), Prognostics - Physics-based Models (light blue), and Prognostics - Multi-model approaches (pink).

The percentages associated with each segment are as follows: Diagnostics - Knowledge-Based Models accounts for 13.3%, Diagnostics - Data-Driven Models accounts for 18.9%, Diagnostics - Physics-based Models accounts for 1.1%, Diagnostics - Multi-model approaches accounts for 15.6%, Prognostics - Knowledge-Based Models accounts for 4.4%, Prognostics - Data-Driven Models accounts for 28.9%, Prognostics - Physics-based Models accounts for 5.6%, and Prognostics - Multi-model approaches accounts for 12.2%. A thick black line vertically bisects the pie chart, separating the segments into two groups.



<div align="center">

Fig. 4. Studies distribution for diagnostics and prognostics considering the consulted papers for the second search step.

</div>


> **Figure Description:**

This diagram is a flow chart illustrating the evolution of maintenance terminology, consisting of three rectangular boxes arranged horizontally from left to right, connected by arrows pointing to the right. The first box on the left is labeled "Predictive Maintenance," and below it is the text: "First term for diagnostics and prognostics tasks in maintenance by the use of specialized tools and techniques. It remains widely used and sometimes it is presented as it includes CBM and PHM like its sub-strategies."

The middle box is labeled "Condition-based Maintenance," and below it is the text: "Extension of predictive maintenance for some research communities. Initially it incorporated alarms on health monitoring tasks. Norms and standards give privilege to this term for diagnostics and prognostics tasks in maintenance."

The third box on the right is labeled "Prognostics and Health Management," and below it is the text: "Extension of CBM for some research communities. Integrated approach focused on prognostics and life cycle management."



<div align="center">

Fig. 5. Relationship among Predictive Maintenance, CBM and PHM.

</div>

2006 and is frequently cited by others [104]. This first survey dedicates a different section for diagnostics a prognostics, summarizing the most important techniques for each approach (only single-model approaches). Other survey articles have more specific subtopics that where addressed: RUL estimation through vibration data analysis on bearings and gears [105]; prognostics with a bound scope on data-driven or physics based models [106]; or on bibliometric indicators for predictive maintenance [107]. More general overviews on predictive maintenance models were covered by conference papers [97,108]. These conference articles have a limited scope to only few models and examples.

The most complete reviews are [2] and [3], from 2017 and 2018 respectively. These two reviews gave privilege to the term PHM to address the topic and offer an overview from the data collection to the decision making process (all functional blocks mentioned in Section 2); however, their main scope is on predictability and remaining useful life (RUL) estimation. They both respect the taxonomy of four model types (with slight differences in the naming): knowledge-based, data-driven, physics-based and hybrid (partially addressed). These two articles update and extend the work done by previous survey studies on prognostics and RUL estimation [109-111]. The latest consulted survey is from 2019 and is exclusively dedicated to data-driven methods for prognostics tasks, especially those related to machine learning and deep learning [4]. A summary of the previous reviews could be found in Appendix 2.

The consulted reviews on predictive maintenance are mainly focusing on single-model approaches, data-driven models and prognostics. The second search step covers these gaps giving special attention to the use of multi-model approaches in both diagnostics and prognostics. The following Sections (5, 6 and 7) cover the findings of the second search step based on a complementary point of view to recent reviews to cover the mentioned gaps.

## 5. Single-model approaches for predictive maintenance

This section briefly introduces to single-model approaches used for diagnostics or prognostics, their strengths and weaknesses and how

recent studies already implement complementary models to fulfil the intended tasks in predictive maintenance systems and overcome complexity. It is a complementary point of view to recent and complete review that have extensively covered single-model approaches. The models in this section are divided into three model types: knowledgebased models, data-driven models and physics-based model.

## 5.1. Knowledge-based models

Knowledge-based models build upon experiences. Experience can be represented by rules, facts or cases that have been gathered over the years of operation and maintenance of the technical system [9,112,113]. Experience can be used to identify faults, describe the degradation and forecast a potential failure of components or systems. These rules, facts or cases, can be used in computational intelligence techniques to automate the inference on diagnostics and prognostics for maintenance purposes. It was the state of the art of maintenance in the early 1990's. Publications such as [9,114,115] describe how knowledge based models were used to perform diagnostics in technical systems. Knowledge based models remain an important field of research for maintenance purposes and three main topics were identified in the systematic literature review: rule-based models, case-based models and fuzzy knowledge-based models.

Rule-based models are knowledge-based models in which the knowledge is represented by rules in the format "IF-THEN", allowing to perform an inference supposed to simulate a simplified reasoning mechanisms of human experts [112]. Rule-based systems consist of a knowledge base gathering all the rules, a fact base and an inference engine. The inference using rules is an iterative process. Initial "facts" are used as inputs. The inference engine compares these inputs with the set of rules contained in the knowledge base and produces conclusions as outputs. The inference engine uses these conclusions as new facts to be compared again with the set of rules so that new conclusions are obtained. This process is repeated depending on the inference engine design until the reasoning process comes to an end. Fig. 6 shows a simplified generic model of a rule-based system for diagnostics and prognostics.


> **Figure Description:**

The image is a diagram illustrating the architecture of a Rule-Based System. The system is enclosed within a large, dashed-line rectangle labeled "Rule-Based System" at the bottom. Inside this rectangle, there are three main components represented by rounded rectangles arranged horizontally: "User Interface" on the left, "Inference Engine" in the center, and "Knowledge base" on the right.

The components are connected by directional arrows indicating the flow of information. A bidirectional arrow connects the "User Interface" and the "Inference Engine." A single arrow points from the "Knowledge base" to the "Inference Engine." Outside the dashed boundary, there are two stick-figure icons. On the far left, a figure labeled "User" has two horizontal arrows connecting it to the "User Interface," representing bidirectional communication. On the far right, a figure labeled "Expert Knowledge" has a single arrow pointing from it toward the "Knowledge base," representing the input of expert knowledge into the system.



<div align="center">

Fig. 6. Basic RBS inspired on [18].

</div>


> **Figure Description:**

This diagram illustrates the Case-Based Reasoning cycle, organized as a circular process with four main stages: RETRIEVE, REUSE, REVISE, and RETAIN. At the center of the cycle is a box labeled "Previous cases" and "General Knowledge," which interacts bidirectionally with each of the four stages via double-headed arrows.

The process begins at the top with a "Problem" input, which leads into a "New case" box. This "New case" is part of the RETRIEVE stage, where it is compared against the central "Previous cases" to produce a "Retrieved case" alongside the "New case." Moving clockwise to the REUSE stage, the "Retrieved case" informs a "Solved case," which outputs a "Suggested Solution." The REVISE stage follows, where the "Solved case" transitions into a "Tested/Repeated case," which outputs a "Confirmed Solution." Finally, the RETAIN stage processes the "Tested/Repeated case" into a "Learned case," which is then fed back into the central "Previous cases" repository to update the "General Knowledge."



<div align="center">

Fig. 7. The Case-based reasoning cycle [116].

</div>

Case-based models are knowledge-based models whose knowledge representation is through cases, obtained from previously experienced, concrete problem situations [116]. Cases are normally represented by a paired knowledge, like for example (problem, solution), in a case base. When facing a new problem, the most similar case is retrieved from the case base. Once a similar case has been identified, its "solution" is reused to adapt the solution for the new. There is a revision to confirm if the suggested solution solves the new problem. If the solution is confirmed, the new case can be retained as learnt knowledge in the case base. Fig. 7 shows the standard case-based reasoning cycle. Unlike rulebased reasoning, case-based reasoning can be used when the relations between facts cannot be declared explicitly [9]. A case is described by a set of attributes that could be numeric data and/or text-based data. Finding the relevant attributes to describe the cases is a difficult task when developing case-based systems.

Fuzzy knowledge-based models use basically the same format of rules IF-THEN as rule-based systems but the statements use intentionally fuzzy logic [110]. Unlike Boolean logic in which a proposition can only be true or false, in fuzzy logic there are intermediate values to describe the level of truth or falsehood of a statement [117]. Fuzzy logic is strongly related with human perceptions. Symbolic linguistic terms such as 'hot', 'cold', 'small', 'large', etc., are frequently used. This characteristic makes fuzzy logic an important tool for uncertainty management. Fuzzy logic can be also used in case-based reasoning and other data-driven models.

Knowledge-based models find limitations for prognostics as it is very difficult to obtain accurate knowledge for predictability purposes from experience. The identified examples in the current literature review are more related to diagnostic tasks and those which are intended for prognostics also include complementary models to estimate remaining useful life. Another drawback of knowledge-based models is the limited access to experts or knowledge sources to build the systems. Current trends in knowledge-based models use data mining techniques to extract the required knowledge from databases. [118,119] are examples for rules extraction while [22,120] aim at extracting cases from databases. One strong point of knowledge-based models forms the

explicative results they offer [101]. It is possible to explain each reasoning step these models perform, it makes easier to justify their implementation against authority regulations for safety-critical systems, such as aircraft or nuclear power plants. Table 2 shows a summary of the identified applications of knowledge-based models in the current systematic literature review.

## 5.2. Data-driven models

Data-driven models have gained a lot of importance in recent years thanks to the improved availability of computational power and the production of large amounts of data coming every day from technical systems. Modern technical systems include an important number of operational parameters constantly measured and recorded. The resulting high volume of data can be used explicitly or implicitly for many purposes, including maintenance. Information obtained from data can be used to study the degradation of components, the current health state of the system or its remaining useful life. Fig. 8 shows an example of jet-engines degradation assessment based on trend analysis of measured data [7]. For the current survey, data-driven models are classified in three groups: statistical models, stochastic models and machine learning models.

One of the main challenges for data-driven models is the management of uncertainty coming from data [3,104,108,127]. Probability theory plays a vital role in data-driven models, as it is the most common way to manage uncertainty. Other studies use Dempster-Shafer models [31,40] (evidence theory), fuzzy logic [128] or possibility theory to manage data uncertainty.

## 5.2.1. Statistical models

Statistical models aim at analysing the behaviour of random variables based on recorded data. For predictive maintenance, statistical models are used to determine the current degradation and the expected remaining life of the technical systems. This is performed by comparing their current behaviour of measured random variables against known behaviours represented by series of data. Normalization and data

<table border="1"><tr><td>Model</td><td>References</td><td>Tasks</td><td>Case Studies</td><td>Complementary models</td></tr><tr><td>Rule-based models</td><td>[18,19,21,26,118,121,122]</td><td>Fault diagnostic, root cause analysis, RUL estimation(along with complementary techniques)</td><td>Power circuit breakers, overhead cranes, mining excavators, lubricant pipe abrasion, high voltage circuits, xenon lamps, oil pipe lines</td><td>Markov models,Grey theory,Bayesian model,data mining models.</td></tr><tr><td>Case-based models</td><td>[20,9,120,123,124]</td><td>Fault diagnostic,RUL estimation(limited number of applications)</td><td>Induction motors,power equipment,railway systems,simulated jetengines data</td><td>Rule-based systems,data mining models.</td></tr><tr><td>Fuzzy knowledge-based models</td><td>[23,24,125,126]</td><td>Fault identification,uncertainty management</td><td>Grinding wheels,oil pumps,rolling bearings,simulated jet-engines data.</td><td>Data mining models.</td></tr></table>

<div align="center">

Summary of identified applications for knowledge-based models in this systematic literature review

</div>

cleaning are common preliminary tasks performed on data series to obtain the distribution function before the trend analysis. This prevents from outliers, constants, binary or any other variable that is not useful for degradation analysis.

For degradation analysis, the trend analysis of random variables is vital. The random variables must show a correlation with operational time or any other non-random variables that describe the lifecycle of the technical system. This correlation will show the evolution of degradation along the life cycle. For instance [129], used correlation to select the variables to describe the degradation on jet engines data. Covariance evaluations are frequently performed when the degradation is described by several variables [30]. Statistical models are also used for prognostics. Regression analysis will help to determine the relationship between the random variables and the life cycle of the technical systems so that a computation of future behaviours is possible.

Besides regression analysis there are two other statistical approaches that stand out: Autoregressive models and Bayesian models. Autoregressive-moving average models (ARMA) are statistical models for which a future value of a random variable is assumed to be a linear function of past observations and random errors [110]. ARMA models and their variants [50,130-133] are used to forecast future values of data series. Autoregressive-models have the advantage of simplicity in their computation. However, as they rely on statistical degradation trends, their accuracy could be affected when assessing new degradation trends where no previous information was available [3].

Bayesian models are those which apply Bayesian theorem [108], a statistical inference method to estimate conditional probability. It computes the probability of an hypothesis based on the prior (initial) probabilities of events that are related to the hypothesis [134]. Finding these prior probabilities poses the main problem for Bayesian theorem application. For predictive maintenance purposes, Bayesian models can be applied when data including anticipated failures with their corresponding symptoms and life expectancy is available [96,108]. Bayesian models play an important role on data-driven models for predictive maintenance, specially combined with other data-driven models to manage uncertainty [36,53,54,135]. Table 3 presents a summary of the applications of these two statistical approaches identified in this literature review.

Statistical models offer an important number of potential solutions to fulfil diagnostic and prognostic tasks. The main drawbacks of statistical models concern the need of enough previous data to build a reliable model and uncertainty management. For predictive maintenance systems, statistical models are often implemented in multimodel approaches.

## 5.2.2. Stochastic models

Stochastic models are probability models aiming at the study of the evolution of random variables over time [134]. The building blocks of stochastic models are stochastic processes. In the literature review, three main stochastic processes were identified for diagnostics and prognostics: Gaussian processes, Markov processes and Levy processes.

- A Gaussian process is a collection of random variables or any finite variable number of which have a joint Gaussian distribution [137]. Gaussian processes can be used for non-linear regression [138]. This property has motivated the use of Gaussian processes for diagnostics and prognostics in the maintenance field. According to [139] Gaussian processes are flexible models to work with small or large-dimensional datasets for prognostics purposes. However, it requires a high computational power to perform the predictive tasks.

- Markov chains are part of a bigger family of stochastic tools called Markov processes [140]. Markov chains suppose that given a process in its present state, the future depends on the present state independently of the past of the process. According to [110] the main shortcomings of Markov models for predictive maintenance are: 1) the need of large volume of data for training, 2) the impossibility to


> **Figure Description:**

This scatter plot illustrates the progression of system degradation over time, measured in the number of cycles. The horizontal x-axis represents the "Number of cycles," ranging from 0 to 275 in increments of 25. The vertical y-axis represents "Degradation," ranging from 0.0 to 1.1 in increments of 0.1. The data is plotted as a series of blue diamond markers, which are overlaid by a smooth red trend line that tracks the general increase in degradation.

The plot is divided into three distinct operational phases by two vertical dashed blue lines. The first phase, labeled "Nominal condition," spans from 0 to approximately 100 cycles, where degradation remains relatively low and stable. The second phase, labeled "Acceptable degradation," occurs between approximately 100 and 220 cycles, characterized by a steady, accelerating increase in degradation. The third phase, labeled "Failure," begins after the "Safety threshold" at approximately 220 cycles, where degradation values rise sharply toward 1.0. The transition points are explicitly labeled at the top of the graph as "Fault detection" (at 100 cycles) and "Safety threshold" (at 220 cycles). An upward-pointing arrow located in the final phase, near the 250-cycle mark, is labeled "Failure," indicating the point at which the system reaches its maximum degradation state.



<div align="center">

Fig. 8. An example of degradation analysis based on series of data [7].

</div>

model different degradation stages, and 3) the impossibility to model unanticipated failures or faults. As these models cannot be used to model different degradation stages, they are not suitable for reparable components that have been partially restored. It should be noted that the model complexity increases when the degradation does not follow an exponential trend [3].

- Lévy processes are stochastic processes within the family of Markov processes [141]. These processes represent the motion of random variables whose displacements are independent and stationary within time intervals of the same length [142]. Weiner processes, Gamma processes and Poisson processes belong to the category of Lévy processes used for predictive maintenance. Extensive reviews in Lévy processes for predictive maintenance can be found in [59,60]. Lévy share the general limitations of Markov processes. In prognostics, Lévy processes are bound to monotonic degradation processes [3,110].

Table 4 presents a summary of the stochastic models addressed in this literature review. It can be seen that this type of models is more suitable for degradation modelling and RUL estimation because of their regression capabilities. These models have many drawbacks in common, such as for example high computational power requirements, advanced mathematical knowledge to be implemented and uncertainty management. Complementary techniques or models are often used along stochastic models.

## 5.2.3. Machine learning models

Machine learning is a branch of artificial intelligence [96] that uses specialized learning algorithms to build models from data. These models are capable of dealing with and capturing complex relationships among data, difficult to obtain using physics-based, statistical or stochastic models. One key point of machine learning models is their learning process and depends on the application, goal and the available data for the system [146].

- Supervised learning is preferred when the expected outcomes of the model and data under study are known. Its training is an iterative process assessing the output error against the expected one. The training finishes when an "acceptable" level of error is reached.

- Unsupervised learning is used when no preliminary outcomes are known. No error levels are measured to assess or to end the training process. These algorithms use other criteria to end the training process, such the number of training iterations or the progress of a convergence indicator over time [147]. Clustering is an example of tasks performed by unsupervised learning algorithms.

- Reinforcement learning aims to train a model by experience instead of

examples [148]. The model "interacts" with an environment and receives a "reward" depending on the interaction. This reward is linked to a performance indicator that the learning algorithm tries to optimize. The final outcomes of the learning are not known.

Within the identified machine learning models for predictive maintenance applications, artificial neural networks are computational models inspired by biological neural networks in an attempt to mimic their unique processing capabilities [149]. They consist of elementary units called "neurons", usually represented graphically as nodes in a graph. Neurons are processing units which receive several inputs and produce one or multiple outputs that may be the input for other neurons. A neuron's output is equal to the weighted sum of its inputs values by means of an activation function. The learning process of the neural network aims at choosing and adjusting the weights of the neurons' inputs. Neurons are organized into layers. These layers can be organized in different configurations (architectures). For predictive maintenance the most used configurations are multi-layer perceptron neural networks, recurrent neural networks (including long-short term memory neural networks), convolutional neural networks, self-organizing maps and support vector machines with different variants. An extensive explanation of these models can be found in the reviews [3] and [4].

The learning process used to train the neural-network will depend on its architecture and the available data, information or knowledge for training. As [99] suggests, artificial neural networks do not need indepth knowledge of dysfunctions of the technical system which makes artificial neural networks a strong tool to get implicit knowledge from the data.

Table 5 summarizes some applications of machine learning models identified in this literature review. Opposite to other predictive maintenance models, machine learning approaches might not include all the functional blocks F3, F4 and F5 mentioned in Section 2 (see Fig. 2). Some neural network applications with several internal layers of neurons (Deep Learning) aim at letting the algorithm learn from raw data to obtain directly the desired outcome, whether it is diagnostic or prognostic. Even when good results are already obtained, a comprehensive explanation of the trained algorithm behaviour is even more difficult to be justified against regulations on safety-critical systems, such as aircraft or nuclear power plants. Once the model has been trained, it is difficult to explain how it works, what is reasoning behind in the model. Explaining the reasoning inside a trained machine learning model is a promising opportunity of research for the coming years. Even when publications are found in this area (e.g. [150]), they do not cover predictive maintenance applications.

<div align="center">

Summary of identified applications of statistical models in predictive maintenance.

</div>

<div align="center">

Table 3

</div>

<table border="1"><tr><td>Model</td><td>References</td><td>Tasks</td><td>Case Studies</td><td>Complementary models</td></tr><tr><td>Regression analysis</td><td>[34,38,39,76,129,136,75]</td><td>RUL estimation, fault diagnostics, health assessment</td><td>Power transformer, electric cooling fan, simulated jet engine data, air compressor, aluminium plates, lithium-ion batteries, bearings</td><td>Other statistical models, physics-based models</td></tr><tr><td>ARMA</td><td>[50,131-133]</td><td>RUL estimation</td><td>Bearings, aircraft generators, structural damage, semiconductors switches</td><td>Other statistical models, Neural Networks</td></tr><tr><td>Bayesian models</td><td>[36,41,53,135,33]</td><td>Stochastic degradation parameter identification and update. Fault diagnostics</td><td>Laser machines, sensors, high power circuits, circuit boards.</td><td>Stochastic models, other statistical models, Monte-Carlo simulation.</td></tr></table>

<div align="center">

Summary of identified studies applying stochastic models for predictive maintenance.

</div>

<table border="1"><tr><td>Model</td><td>References</td><td>Task</td><td>Case Study</td><td>Complementary models</td></tr><tr><td>Gaussian Process Markov Chains and Hidden Markov chains Levy process</td><td>[77,143][36,52,56,57,122,144][43,58,145]</td><td>Fault diagnostics,RUL predictionProduce stationary distribution for RUL computation,Degradation simulationRUL computation,Degradation Modelling</td><td>Wind Turbines,slow speed bearingsMilling machines,simulated jet-engine data,semiconductor manufacturer machine,continuous stirred tank reactor,asphalt roadsSimulated jet-engine data,high-power white LEDs,automotive engine cranking</td><td>For signal processingBayesian model,genetic algorithm,belief rule-based model,Monte Carlo.Proportional hazard model,combination of different stochastic models</td></tr></table>

<div align="center">

Summary of identified applications for machine learning models.

</div>

<table border="1"><tr><td>Model</td><td>Reference</td><td>Task</td><td>Learning process</td><td>Case Study</td><td>Complementary models</td></tr><tr><td>MLP</td><td>[44,45,63,64]</td><td>Fault identification</td><td>Supervised</td><td>Wind turbine gear boxes, combustion engines, nuclear power plants, rotary machines</td><td>Signal processing models, radial basis function network, multiple NN</td></tr><tr><td>RNN</td><td>[148,46,47,66,74]</td><td>Fault diagnostic, RUL estimation</td><td>Supervised, reinforcement</td><td>Gear boxes, jet engines, mill fans, rolling bearings</td><td>Different NN</td></tr><tr><td>CNN</td><td>[67,73,79,80]</td><td>Fault diagnostics, RUL estimation</td><td>Supervised</td><td>Jet engines, gear boxes, bearings.</td><td>Statistical models, Extreme learning machine, autoencoder</td></tr><tr><td>SOM</td><td>[2,32,68,94,127],</td><td>Degradation modelling, fault detection</td><td>Unsupervised</td><td>Jet Engines, Cyber-physical systems, railway point machines</td><td>Statistical models</td></tr><tr><td>SVM, SVR</td><td>[34,37,70-72,72,81,151]</td><td>Health assessment, fault detection, prognostics</td><td>Supervised, Unsupervised</td><td>Battery cells, metal-mechanics equipment, electrical equipment, chemical industry, chillers, Tennessee Eastman process, industrial simulated data</td><td>Statistical models, RNN (LSTM)</td></tr><tr><td colspan="6">NN: Neural Network. MLP: Multi-layer Perceptron. RNN: Recurrent Neural Network. CNN: Convolutional Neural Network. SOM: Self-Organizing Maps. SVM: Support Vector Machines. SVR: Support Vector Regression.</td></tr></table>

<div align="center">

Table 5

</div>

## 5.3. Physics-based models

Physics-based models use the laws of physics to assess the degradation of components. They demand high skills on mathematics and physics of the phenomena for the application. This kind of mathematical model remains an important topic of research with interest for many disciplines. With an accurate model of the physical behaviour of a system it is possible to perform accurate simulations to study the degradation behaviour on a specific component or a system. Within the identified studies of physics-based models there are fatigue and crack propagation models for mechanical and structural components [102,152]. With the computational power rising over the last decades, the use of finite element methods has increased for damage propagation and failure prediction, some identified examples are [83] on a rotor cage and [85] on solenoid valves. Other physics based model have been used to study the tube erosion of boiler head exchangers [86], clogging prognostics on filters of fluids [82], degradation evaluation of industrial robots [84] and remaining useful life estimation on lithium-ion batteries [76]. Physics-based models offer a possibility to study and assess degradation by means of computational simulations. However, many physics phenomena cannot yet be accurately described. The outcomes of a physics-based model will be as good as the "accuracy" or "completeness" of the model. The operational context of a technical system affects its performance. External influence such as temperature, pressure or any other environmental conditions might drastically change the expected operational parameters and the actual behaviour. Incorporating external influence data is a challenge already mentioned by other studies such as [108,153]. These may be solved by adding complementary models (potentially other physics-based model).

## 6. Multi-model approaches for predictive maintenance

Single-model approaches hardly address all the diagnostics and prognostics tasks of complex systems; the consulted studies with single-model approaches often proposed complementary models to overcome the weak points of some models. It is increasingly common to find research studies that combine different models in multi-model approaches to overcome complexity of predictive maintenance tasks. Increasing complexity includes the number potential faults and failure modes of the technical system, the type and number of information and/or data sources obtained from it and the number of diagnostics and prognostics tasks that are targeted, all these apart from the design complexity of the selected model. Most of the consulted studies had limited case studies with only few failure modes (sometimes only one) which poses a challenge to extrapolate single-model approaches to real complex systems applications [98,103]. Identified studies that had more complex case studies usually applied multiple models to fulfil the predictive maintenance system tasks.

However, even when the consulted studies in this section usually had simple and limited case studies, multiple models were often involved. As explained in Section 2, predictive maintenance systems include different functional blocks depending on their initial requirements and the complexity of the available knowledge, data and/or information for the implementation. A multi-model approach is often implemented to fulfil all functional blocks for the predictive tasks (except for some deep learning approaches, see Section 5.3).

A related term to multi-model approaches is "hybrid model". Hybrid models are usually presented as the fourth classification of model types along with knowledge-based, data-driven and physics-based. However, there exist many multi-model approaches which cannot be named as hybrid. The definition of a hybrid model evolves over the different consulted publications. After a careful analysis this literature review suggests that hybrid models are part of multi-model approaches in which two or more models are combined to fulfil one single functional block (F3, F4 or F5 in Fig. 2, see Section 2) of the predictive maintenance systems and there is mutual cooperation among the combined


> **Figure Description:**

This diagram illustrates the relationships and potential combinations between three primary modeling approaches: Knowledge-based, Data-driven, and Physics-based. The three main categories are represented as rounded rectangles positioned at the vertices of a triangle: Knowledge-based at the top, Data-driven at the bottom left, and Physics-based at the bottom right. A large dashed oval encompasses the entire structure, labeled "Potential combinations" at the bottom center.

The diagram displays various interaction types represented by boxes connected to lines or curved arrows. A central box labeled "KB+DD+PB" sits in the middle of the triangle, connected by lines to the Knowledge-based, Data-driven, and Physics-based nodes. Direct connections between the main nodes are labeled with rectangular boxes: "KB+DD" connects the Knowledge-based and Data-driven nodes, "DD-PB" connects the Data-driven and Physics-based nodes, and "KB+PB" connects the Knowledge-based and Physics-based nodes.

Additionally, self-referential or internal interactions are shown with curved arrows and boxes: "KB-KB" loops back to the Knowledge-based node, "DD-DD" loops back to the Data-driven node, and "PB-PB" loops back to the Physics-based node. All text labels are capitalized as shown, and the layout emphasizes the integration of these three distinct methodologies.



<div align="center">

KB: Knowledge-based model. DD: Data-driven model. PB: Physics-based model.

</div>

<div align="center">

Fig. 9. Potential combinations for multi-model approaches.

</div>

models to obtain their outputs.

An introduction to the notion of different types of multi-model approaches (under the name of hybrid models) can be found in [154]. The authors classified them into 5 groups: knowledge-based models combined with data-driven models, knowledge-based models combined with physics-based models, combination of multiple data-driven models, data-driven models combined with physics-based models, and a combination of one models of each type. However, multi-model approaches can also include two more categories not mentioned in their proposed hybrid model taxonomy: combination of multiple knowledge-based models and combination of multiple physics based models. Fig. 9 presents a diagram of the potential combinations of multi-model approaches for predictive maintenance purposes.

## 6.1. Configurations for multi-model approaches

Before presenting the findings on the different model combinations and expand on the potential opportunities for future research in multimodel approaches, it is important to explain how they could be combined from a systems architecture point of view. There are many possible combinations, however, there are three basic configurations on top of which more complex architectures can be built: models working in series, models working in parallel, a model working as a subpart of another model (embedded model), see Fig. 10. These configurations explain the flow of information, data or knowledge through the predictive maintenance system. When architecting new predictive maintenance systems, it is important to consider the potential configurations in order to find the "best" solutions to fulfil the requirements for the system.

Two models are in series when the output of a first model is the input for a second one. The functional blocks presented in Section 2 present intuitively a configuration in series where a single model is used to fulfil

each functional block. For example [147] presents a series configuration of SOM along with a statistics model using probability density function to address the functional blocks of degradation modelling and fault detection. Nevertheless, as complexity in the information or data increases, two complementary models could be used in series to fulfil a single functional block. Multi-model approaches using a series configuration are not usually referred to as hybrid, even when combined models are used to fulfil one single functional block; there is no mutual cooperation among the models to obtain the outputs.

Two models are in parallel when they process their input simultaneously and their outputs are combined in a single one. It is important to point out that the input could be the same for both models working in parallel or they could have different but related inputs. For example, given a technical system, one model could address text-based data (from operational or maintenance logs), while another could address measured data from sensors. Paper [2] gives a good example of a multimodel approach in parallel, with a data-driven model to address all the data coming from the technical system along with a physics-based model for RUL computation for bogie components. Two parallel models fulfilling one single functional block are usually referred as a hybrid model as there is mutual cooperation between the models to obtain the final result.

For the embedded configuration a model is incorporated as a subpart of another one. [155] presents for example a neuro-fuzzy model including a hidden Markov model as part of its internal functioning. Actually, neuro-fuzzy models could be seen as an example of a model embedding another one. They implement a fuzzy inference system within a neural-network architecture. Some identified applications of neuro-fuzzy models in the current survey are degradation prognostics on bearings [90] and fault diagnostics on railways track circuits [156]. Paper [94] combines a Kalman filter embedded an online sequential extreme learning machine (OS-ELM) for remaining useful life


> **Figure Description:**

The image displays three schematic diagrams illustrating different configurations of two models, labeled M1 and M2, with respect to their input and output flow. The first diagram, labeled "a. M1 in series with M2," shows an input arrow pointing into a box labeled M1, which is connected by an arrow to a box labeled M2, which then points to an output arrow. The second diagram, labeled "b. M1 in parallel with M2," shows an input arrow that splits into two paths, one leading into a box labeled M1 and the other into a box labeled M2; these two paths then converge into a single output arrow. The third diagram, labeled "c. Embedded model," shows an input arrow pointing into a large box labeled M1, which contains a smaller box labeled M2 inside it, with an output arrow extending from the right side of the large M1 box.



<div align="center">

Fig. 10. Generic basic configurations for multi-model approaches.

</div>

estimation, and refer to it as KFOS-ELM. Another example for embedded models could be a case-based reasoning system embedding a rule-based system for one or more tasks of the case-based reasoning cycle as proposed by [157]. Multiple models in embedded configuration are usually referred as a hybrid model.

The configurations shown in Fig.10 could include more than two models and could be combined among them. This means that one can propose for example a set of many parallel models (more than two) followed by another model to combine their result, which is what paper [69] proposes for fault diagnostics on aircraft turbojet engines. They present nine data-driven models in parallel and in the end, the outputs where assessed and combined with a knowledge based model. Having a clear idea of the basic configurations and their potential combinations allows expending the creativity process at architecting new predictive maintenance systems.

## 6.2. Combinations for multi-model approaches

This section summarizes the survey findings on the different combinations for multi-model approaches presented in Fig. 10. The explanation of the identified examples for each combination includes the architecture configuration used to combine the different models, and which functional blocks of predictive maintenance system they are covering.

## 6.2.1. Multiples knowledge-based models

This type of multi-model approaches has not been widely used in recent research on predictive maintenance applications. A multi-model approach using only knowledge-based models keeps the same challenges as for single-model approaches and besides, it has an additional difficulty component at designing the combination of multiple models. Nevertheless, the combination of multiple knowledge-based models allows addressing complex diagnostics tasks while explaining the reasoning. The authors of [158] present a case-based system combined with a rule-based system for problem diagnostic in IT services, the rulebased system is embedded in reuse phase of the case-based system. A comprehensive review of case-based, reasoning systems combined with other knowledge-based models can be seen in [157].

## 6.2.2. Multiple data-driven models

This approach combines several data-driven models to perform either diagnostics or prognostics. Neural networks are the most used data-driven models to build this kind of multi-model approaches because of the current trends in machine learning and deep-learning research that aim at incorporating more autonomous and intelligent systems. However, as mention in Section 5.2.3 these models still face problems as their results remain non-explicative [101]. Within the examples found in this literature review [159], presents a multi-layer perceptron and a radial basis function neural network in a parallel model to estimate the remaining useful life from input sensors on simulated jet-engines data [160]. performs fault prognostic with a mixture of Gaussian hidden Markov model (stochastic model) to evaluate the health index and fixed size least squares support vector regression (statistical model) for remaining useful life estimation on the same jetengines simulated data. A more recent article [91] suggests a hybrid deep learning neural network for RUL estimation on the simulated jetengines data. The authors propose a parallel analysis of the input data by a convolutional neural network and a long-short term neural network. The fusion of the results is done by three layers of neurons with different activation functions. Some of the presented examples show that the combination of data-driven models gives more accurate results compared to single-model approaches for the same tasks.

## 6.2.3. Multiple physics-based models

Multiple physics-based models can be used to increase the accuracy of a more general model. The precision usually brought by the laws of

physics embedded in a mathematical model may indeed allow improving the accuracy of diagnostics and prognostics estimations. Most of the identified applications of multiple physics-based model approaches present a series configuration. Initially, a model is used to assess the health state of the technical system (diagnostics), then, another model for remaining useful life estimation (prognostics) [161] mixes physics based models (crack and fatigue models) for helicopter gear prognostics [162] applied a physic-based model to predict the machine condition (i.e. diagnostic), complemented by Forman crack growth remaining useful life estimation in a series configuration [163]. presents an example of multiple physics-based models in parallel configuration. The multiple Kalman filter models are used for single fault detection in jet-engines using temperature, pressure and rotation speed as parameters. The use of multiple physical based models is not widespread. Their implementation requires high skills in mathematics, physics and a large knowledge of the technical system under study, making their implementation difficult. However, they offer a large set of opportunities to obtain accurate and explicative results in the predictive maintenance domain. Several commercial solutions for finite-element analysis include multi-physics models working in parallel to improve the accuracy of the technical system model. Such solutions are widely used for structures and fluid dynamics modelling and simulations [83,85].

## 6.2.4. Knowledge-based models with data-driven models

This multi-model approach has allowed taking advantage of the strong points of both model types. Knowledge-based models could incorporate valuable information from human experts to complement the results of data-driven models for diagnostics or prognostics tasks. For example [87], presents a combination of a fuzzy knowledge-based model and Markov chain for degradation prognostics in aero-engines. The already mentioned neuro-fuzzy systems are other examples of fuzzy logic combined with a data-driven model [90,156,69]. presents a rulebased system to summarize and combine the diagnostics coming from multiple neural networks assessing the same aero-engines data base. Knowledge-based combined with data-driven models offer a vast field of opportunities to innovate at architecting new predictive maintenance systems, allowing analyzing more complex and heterogeneous data coming not only from sensors but also from declared data obtained from the technical system operators or extracted from large databases [118,119] by means of data-mining techniques. This declared data, normally assessed by knowledge base systems may reduce the uncertainty in data-driven models. One example of this is presented in [2] on a train suspension case study.

## 6.2.5. Knowledge-based models with physics-based models

These models use the experts' knowledge to improve the accuracy of physics-based models. The number of studies related to this approach is limited for predictive maintenance applications as this combination gathers the main drawbacks from both model types: difficulty to gather the experts' semantic knowledge and high mathematics complexity to develop physics-based models. However, a strong point of this model combination is the high explicative results they may offer. Within the identified studies [164], combines a fuzzy knowledge-based system with a physics based model for different prognostics tasks on mechanical parts. Potential unexplored applications could include hybrid parallel models using knowledge-based systems to address the declared knowledge by the technical system user, combined with a physics-based model to model its degradation. Another application option could be this multi-model approach to incorporate external influence data to predictive maintenance models. External factors affect directly the performance of technical systems and so their degradation. It is a challenging unexplored field that could offer many interesting solutions in the maintenance field.

<div align="center">

# Author's Personal Copy

</div>

## 6.2.6. Data-driven models with physics-based models

This multi-model approach is the most common in recent research because of the increasing popularity of data-driven models and their complementarity with physics-based models for degradation modelling. Within the possible combinations of data-driven and physics-based models, three main combinations were identified for predictive maintenance applications:

- Statistic models with physics-based models such as [165] uses a physics-based model to build a health index that is later analysed by a support vector-machine to estimate the health state of the system, fitted with an exponential regression. A similarity-based approach is finally used to compute the remaining useful life.

- Stochastic models with physics-based models, such as [145] that uses a stochastic process (Wiener process) combined with a data analysis method (Principal Component Analysis) to model the deterioration of the components that is fitted by an exponential physical degradation, and to estimate the remaining useful life on a case study [92]. presents a more recent example of this type of combination. It uses a physics-based model along with hidden Markov chains and particle filter model for RUL computation of railway tracks.

- Neural network models with physics-based models, such as [166] that use a multi-layer network to generate the system health state, then a physical degradation model of exponential type is used to evaluate the remaining useful life. [167] presents a regression vector machine (which is already a combination of two data-driven models) along with a physics based model to predict the remaining useful life of aluminium plates under fatigue stresses. This is not precisely predictive maintenance but the predictability approach can be extended to other mechanical components.

## 6.2.7. Knowledge- based models with data-driven models and physics-based models

This approach combines at least one of each model type. It benefits from the strengths of every model type, the explicability from knowledge-based models, and physics-based models and the ability to analyse past data to gather additional important information. As an illustration [168], combines a physics based models with a support-vector machine to obtain an analytical health index of rolling bearings, the results combination is performed by a fuzzy rule-based system [169]. proposes the combination of the three model types to address the diagnostics and prognostics of rolling bearing, it presented the models to address different but complementary input data. The number of studies in predictive maintenance combining the three model types remains limited, based on the literature findings. As [2,154] state, this combination could be extremely difficult. The implementation of a multi-model approach combining knowledge-based, data-driven and physics-based models not only represents the individual complexity of each model type but also includes the complexity at architecting the whole system and fusing the outputs of each model.

## 6.3. Some general observations on multi-model approaches

The development of multi-model approaches of any type of the mentioned combinations face particular challenges. Besides the difficulty to develop the individual models composing the multi-model approach, their combination poses additional challenges. The lack of systematic approach for designing predictive maintenance systems is an important challenge [108,170]. However, multi-model approaches present a vast field of opportunities in research for the coming years. The number of unexplored alternative combinations remains huge. These multi-model approaches may help incorporating external influence data, semantic knowledge from experts, and the laws of physics governing the degradation of components or systems to manage uncertainty and improve the accuracy in diagnostics and prognostics.

Also, combining different models may give the opportunity to extrapolate diagnostics and prognostics approaches (today focused on single failure mode applications) to complex systems that include many components with many failure modes.

## 7. Summary of the identified challenges and research opportunities

This systematic literature review allowed the study of the different models, the different approaches to implement them, their benefits, drawbacks and challenges for diagnostics and prognostics in predictive maintenance. This section summarizes the most relevant challenges for diagnostics and prognostics identified in the literature review.

- The extrapolation of existing solutions to complex system applications, including multiple components, and their associated faults [98,103]. Most of the identified applications were focused on a single component with a limited number of faults. However, real-life applications are frequently complex systems composed of many components and many faults associated to each component and to the system itself. Multi-model approaches offer a potential solution to overcome complexity in predictive maintenance systems. As [171] states, complexity can be reduced by functional decomposition and later each function can be addressed individually. As explained in Section 2, a predictive maintenance system could have several functional blocks for each component and/or failure mode in a complex system. It is necessary at least one model to fulfil each functional block for each component and failure mode. However, the implementation of these models is not trivial and adds another complexity factor for the model combination.

- The lack of a systematic approach to design and develop predictive maintenance systems [108,170]. There exist standards, norms and generic architectures to develop new predictive maintenance systems, such as OSA-CBM [15]. However, they only focus on the basic functional components of the system and do not cover important aspects regarding performance indicators or context constraints of the technical system. Besides, they do not offer yet a consistent explanation on which models to use depending on the initial needs of the predictive maintenance system. The lack of a systematic approach limits the implementation of predictive maintenance systems on real scale industrial applications. When developing a new predictive maintenance system the number of potential models to solve the problem is too high. For engineers the simple fact of choosing the right model or a reduced set of models remains a challenging task. It turns out to be very difficult to perform an objective selection of models as there are not enough comparative studies of the use of different models on the same tasks for predictive maintenance systems. None of the consulted publications in this survey gives extensive explanations for the selection of the proposed method and the architecture methodologies to create a concept of the system varies from one study to another. Besides, many studies do not present detailed design parameters for their proposed models, or the case study data is not available. All these aspects make it difficult to reproduce results and even more difficult to retrieve models from previous studies for use in new predictive maintenance systems. There are no clear guidelines for selecting the right model or models for a specific task given the operational modes and available data to perform diagnostics and prognostics.

- The fusion of large and different sources of condition monitoring data [3,153]. This challenge is related to the extrapolation of current models in predictive maintenance to complex technical systems. Technical systems may have different types of data sources, for example sensor measurements, maintenance logs, operational logs, design documents, etc. Important knowledge could be gathered from all these sources to implement new predictive maintenance systems. However, the heterogeneity of these data sources makes

knowledge modelling and fusion a difficult task for predictive maintenance purposes. Today, the main part of studies uses time series to perform diagnostics and prognostics and important information coming from text-based data is frequently ignored [17]. Text-based data is difficult to analyse when it is not in a structured form. Current trends in maintenance aim at analysing natural text log to extract information that can be used to improve maintenance tasks. Different models are needed to address text-based data while others address measured data from sensors. Multi-model approaches can be used to fuse heterogeneous data sources.

- The incorporation of external influence data [108,153]. Systems operation may differ depending on their operational context. Changes in the operational context may affect directly the performance of the technical system and consequently the readings on the health monitoring. It may trigger false alarms suggesting fault existence, or it may prevent existing fault identification. This could be addressed by complementary models able to incorporate the external influence for predictive maintenance purposes.

- Uncertainty management [3,104,108,127]. Uncertainty affects directly the accuracy of the diagnostics and prognostics. It can be due to the collected data or to imperfections of the model used for the analysis. It may affect the trustworthiness of the results. Uncertainty management is vital for critical systems subject to authorities' regulations. This is the case for critical systems like nuclear power plants and aircrafts on which the regulations are restrictive to keep safety standards and avoid catastrophic events. Probability theory, Dempster-Shafer theory and fuzzy logic have been the most common techniques used to manage uncertainty observed in the systematic literature review. Multi-model approaches may be a solution to address uncertainty in complex systems.

## 8. Conclusion

This systematic literature review performed on predictive maintenance shows that its importance in research has been increasing dramatically over the last 25 years. The search was performed initially using three related terms: "Predictive Maintenance", "Condition Based Maintenance" and "Prognostics and Health Management". Different contributions were found under the different terms but referring to the same activities. Considering all the terms helped to have a wider overview on the current trends used for diagnostics and prognostics in the maintenance field. The survey allowed to answer research question 1 by identifying two main approaches for model implementation: single

model approach and multi-model approach. The current trends lead towards the use of multi-model approaches as one single model is not able to cover all necessary functional blocks in a predictive maintenance system.

Deepening in both approaches, the survey allowed to answer research question 2. The identified models for single-model approaches can be clustered in knowledge-based models, data-driven models and physics-based models. A brief explanation of the most single models used in recent research was presented in Section 5. It is a complementary point of view to other recent reviews that already covered single model approaches. Most of the consulted papers already used complementary models but they are not presented as multi-model approaches. For multi-model approaches, seven different combinations considering the model type were identified: knowledge-based models combined with data-driven models, knowledge-based models combined with physics-based models, data-driven models combined with physics-based models, combination of multiple data-driven models, combination of multiple knowledge-based models, combination of multiple physics-based models, and the combination of one model from each model type. Some of these combinations have not been widely explored in predictive maintenance applications. Besides, three basic configurations are presented to perform the combination of models: in series, in parallel and embedded. Out of these basic configurations more complex architectures can be conceived. Depending on the configuration and the task to fulfil, multi-model approaches can be named hybrid models; however, not all multi-model approaches are hybrid models. There must be mutual cooperation among the models to be a true hybrid model.

To answer the research question 3, the identified challenges are the extrapolation of current solutions on diagnostics and prognostics to complex systems, the lack of a systematic approach for predictive maintenance system design, fusion of different types of data sources, incorporation of external influence data and uncertainty management. These challenges open a branch of opportunities for future research in the topic.

## Declaration of Competing Interest

Juan José Montero Jiménez, Sébastien Schwartz, Rob Vingerhoeds, Bernard Grabot and Michel Salaun declare that they do not have conflict of interests.

## Appendix A. Systematic literature review process

The methodology used in this paper concerns a systematic literature review methodology that aims at summarizing the existing work of a specific topic [5]. Systematic literature reviews help to carry out the literature review process in a structured manner to ensure impartial results and thus a better overview of the subject under study [5]. stresses the importance of a well-structured protocol to carry out the systematic literature review. This protocol spans from the planning of the review until its reporting. For the work presented here, the protocol consists of four steps: research questions definition, search strategy, study selection, and data synthesis. The protocol is summarized in Fig. A1.

## Research questions

The systematic literature review starts by defining the Research Questions (RQ) that drive the review process to define the state of the art of a specific topic and identify the opportunities for future research, setting the boundaries for the search. As the goal of the survey is an update of models or techniques used for diagnostics and prognostics for predictive maintenance, the research questions were chosen as follow:

- RQ1: What are the current trends in diagnostics and prognostics for predictive maintenance?

- RQ2: What kinds of models, techniques or methods are used to address diagnosis and prognosis in predictive maintenance?

- RQ3: What are the current challenges facing predictive maintenance in diagnostics and prognostics?

## Search strategy

In the search strategy phase, the search terms and resources are selected, as well as the time lapse to be covered by the search. For predictive maintenance, the strategy divides the search into two steps, and both of them considered the last 25 years as time lapse. Older papers were consulted


> **Figure Description:**

This image is a flowchart illustrating a research process. It consists of four rectangular boxes with rounded corners, each containing text, arranged vertically and connected by downward-pointing arrows. The top box contains the text "Research questions," which is connected by an arrow to the second box containing the text "Search strategy." The second box is connected by an arrow to the third box, which contains the text "Study selection." Finally, the third box is connected by an arrow to the bottom box, which contains the text "Data synthesis." All boxes are filled with a light gray color and feature a thin black border.



<div align="center">

Fig. A1. Systematic literature review protocol [5].

</div>

to identify when exactly some of the terms started to be used. Four search sources were selected: IEEE Xplore, ScienceDirect, Springer and Web of Science.

The first search step focuses on existing literature reviews on predictive maintenance to check if any of them answer to the proposed research questions. To do so, the following search terms pattern have been used: ("Predictive" OR "Prognosis" OR "Diagnosis" OR "Prognostics" OR "Diagnostics") AND ("Maintenance" OR "Condition-based" OR "Health Management") AND ("Survey" OR "Review" OR "Benchmark"). This leads to search "Predictive Maintenance Survey" or "Diagnostics Maintenance Benchmark" for example. Since many terms used for predictive maintenance are also present in medical research, a refinement on the search is done by discarding all papers and journals on human medicine and diseases. The search on previous literature reviews topics helped to study the evolution of the topic over the last 14 year since the first review was published in 2006 [104]. It was possible to identify some research opportunities that were used to perform the second research step.

The second search step is based on trial searches using terms derived from the identified models in the first search step. The search terms have been refined for this search step. The following terms pattern have been used: ("Predictive" OR "Prognostics" OR "Diagnostics" OR) AND ("Maintenance" OR "Condition-based" OR "Health monitoring") AND ("Data-driven" OR "Physics-based" OR "Knowledge-based" OR "Hybrid" OR "Multi-model). The terms "diagnosis" and "prognosis" were not used in this second search step as there were no differences when using "diagnostics" and "prognostics" in the first search step.

## Study selection

The search considers publications from four different search sources. The types of publications could be from journals articles, conference proceedings, workshops, symposiums, bulletins or book chapters. For the scrutiny of relevant publications, a first analysis through the titles is performed. The search was limited to publications in the English language. If a publication appeared in more than one search list, it was considered only once. All publications out of the scope of the research questions were discarded such as publications regarding maintenance scheduling optimization, maintenance management, corrective maintenance, scheduled maintenance, signal processing, and requirements elicitation for maintenance systems. Some publications turned out to be extensions of previous published works. In such cases, only the most recent and complete were considered. The references of these identified publications were consulted to identify relevant studies missed in the search process. In the end, 187 relevant publications were found, from which 23 are previous reviews and 164 correspond to the second search step.

After the scrutiny, a quality assessment of the publications took place to consider only the most relevant publications. For the first research step, all identified reviews were kept. For the second research step, four characteristics were assessed for the quality assessment: the clearness of research objectives, the explanation of proposed model to fulfil a specific task, the case study explanation, and the comparison to other models or approaches.

The consulted studies were ranked with points. For each study, each characteristic is ranked with one out three possible values: 0, 0.5 and 1. The max score for a publication is 4 points. For this review, publications with a score higher than 3 points were kept. This process narrowed down the number of publications from 187 to 158; from which 23 are previous reviews and 135 correspond to the second search step. An important reason to discard certain papers was the absence of sufficient explanation of the case study and/ comparisons with other existing models to fulfil the same tasks.

The current paper includes 175 references, 158 are from the structured literature review and 17 of them are for theoretical background of some models. These background references were not identified in the systematic literature review.

<div align="center">

Appendix B. Summary of previous reviews

</div>

<table border="1"><tr><td rowspan="2">Year</td><td rowspan="2">Author</td><td rowspan="2">REF.</td><td colspan="3">Single model approach</td><td rowspan="2">Multi-model approach</td></tr><tr><td>Physics-based</td><td>Data-driven</td><td>Knowledge based</td></tr><tr><td>2006</td><td>Jardine et al.</td><td>[104]</td><td>Physics of failure</td><td>Statistical models, AI models(FFNN,CCNN)</td><td>Experts systems,Fuzzy Logic</td><td>No</td></tr></table>

## Author's Personal Copy

<div align="center">

J.J. Montero Jimenez, et al.

</div>

<table border="1"><tr><td>2006</td><td>Kothamasu et al.</td><td>[6]</td><td>N/A</td><td>Statistics and Stochastic models. Bayesian models and Markov models</td><td>Rule-based systems and Fuzzy logic</td><td>No</td></tr><tr><td>2007</td><td>Vachtsevanos et al.</td><td>[102]</td><td>FEM, Physics of failure</td><td>ANN, stochastic and statistics</td><td>Expert systems</td><td>Yes</td></tr><tr><td>2009</td><td>Dragomir et al.</td><td>[109]</td><td>Physics of failure</td><td>AI techniques, ANN, NFL, Bayesian, Markov models</td><td>N/A</td><td></td></tr><tr><td>2009</td><td>Liu et al.</td><td>[113]</td><td>N/A</td><td>HMM, ANN,</td><td>Experts systems, Fuzzy Logic</td><td>No</td></tr><tr><td>2010</td><td>Peng et al.</td><td>[172]</td><td>First principle modeling.</td><td>ANN, state space model, hazard rate, proportional hazard rate, gray model</td><td>Experts systems, Fuzzy Logic</td><td>Yes</td></tr><tr><td>2011</td><td>Sikorska et al.</td><td>[110]</td><td>Physics of failure</td><td>Statistical models, stochastic models, ANN</td><td>Experts systems, Fuzzy Logic</td><td>Yes</td></tr><tr><td>2012</td><td>Prajapati et al.</td><td>[10]</td><td>N/A</td><td>Statistics, stochastic, artificial intelligence</td><td>Expert systems</td><td>Yes</td></tr><tr><td>2014</td><td>Okoh et all</td><td>[111]</td><td>Physics of failure</td><td>Statistics and Stochastic.</td><td>Experts systems</td><td>Yes</td></tr><tr><td>2014</td><td>Liao and Köttig</td><td>[154]</td><td>In hybrid models</td><td>In hybrid models</td><td>In hybrid models</td><td>Yes</td></tr><tr><td>2015</td><td>An et al.</td><td>[106]</td><td>Physics of failure</td><td>Neural Networks, Gaussian process regression</td><td>Out of scope</td><td>Yes</td></tr><tr><td>2015</td><td>Bailey et al.</td><td>[173]</td><td>Physics of failure</td><td>Statistical, Machine learning.</td><td>Out of scope</td><td>Yes</td></tr><tr><td>2015</td><td>Schmidt and Wang</td><td>[108]</td><td>Physics of failure</td><td>Stochastic, Statistic, ANN (Bayesian)</td><td>Experts systems</td><td>Yes</td></tr><tr><td>2016</td><td>Elattar et al.</td><td>[174]</td><td>Physics of failure</td><td>Probabilistic models, machine learning</td><td>Reliability-models</td><td>Yes</td></tr><tr><td>2016</td><td>Vanraj et al.</td><td>[175]</td><td>FEM</td><td>ANN with BPN, SOM</td><td>N/A</td><td>No</td></tr><tr><td>2017</td><td>Alaswad and Xiang</td><td>[98]</td><td>N/A</td><td>Markov, Gamma process, Gaussian, among others.</td><td>N/A</td><td>No</td></tr><tr><td>2017</td><td>Javed et al.</td><td>[96]</td><td>Physics of failure</td><td>Machine learning, ANN, Bayesian, MC, NFL, CBR.</td><td>Included in the data-driven models.</td><td>Yes</td></tr><tr><td>2017</td><td>Wang et al.</td><td>[105]</td><td>Physics of failure</td><td>Statistical models, machine learning</td><td>N/A</td><td>No</td></tr><tr><td>2017</td><td>Atamuradov et al.</td><td>[2]</td><td>Paris&#x27; Law, Forman Law, Others</td><td>ARIMA, Gaussian models, ANN, Bayesian Network</td><td>Experts systems, Fuzzy Logic</td><td>Yes</td></tr><tr><td>2018</td><td>Lei et al.</td><td>[3]</td><td>Physics of failure</td><td>Statistics, Stochastic, ANN, SVM/RVM</td><td>N/A</td><td>Yes</td></tr><tr><td>2018</td><td>Sakib and Wuest</td><td>[97]</td><td>N/A</td><td>MC Bayesian, MC, Machine learning, Monte Carlo.</td><td>N/A</td><td>No</td></tr><tr><td>2019</td><td>Zhang and Yang</td><td>[4]</td><td>N/A</td><td>ANN, DNN, Logistic regression, SVM, Random Forest, auto-encoder.</td><td>N/A</td><td>No</td></tr></table>

## References

[1] Sullivan GP, Pugh R, Melendez AP, Hunt WD. Operations & maintenance best practices: a guide to achieving operational efficiency. U S Dep Energy, Fed Energy Manag Progr. 2010. https://doi.org/10.2172/1034595.

[2] Atamuradov V, Medjaher K, Dersin P, Lamoureux B, Zerhouni N. Prognostics and health management for maintenance practitioners - review, implementation and tools evaluation. Int J Progn Heal Manag 2017.

[3] Lei Y, Li N, Guo L, Li N, Yan T, et al. Machinery health prognostics: a systematic review from data acquisition to RUL prediction. Mech Syst Signal Process 2018;104:799-834. https://doi.org/10.1016/j.ymsssp.2017.11.016.

[4] Zhang W, Yang D, Wang H. Data-driven methods for predictive maintenance of industrial equipment: a survey. IEEE Syst J 2019;13:2213-27. https://doi.org/10.1109/JSYST.2019.2905565.

[5] Kitchenham B, Charters S. Guidelines for performing systematic literature reviews in software engineering. Eng Rep EBSE-2007-01, Keele Univ Univ Durham 2007. https://doi.org/10.1145/1134285.1134500.

[6] Kothamasu R, Huang SH, Verduin WH, Kothamasu R, Huang SH, Verduin WH. System health monitoring and prognostics -a review of current paradigms and practices. Int J Adv Manuf Technol 2006;28:1012-24. https://doi.org/10.1007/978-1-84882-472-0_14.

[7] Montero Jimenez JJ, Vingerhoeds R. Enhancing operational fault diagnosis by assessing multiple operational modes. Proc. - Int. Conf. Model. Optim. Simul. MOSIM 2018. 2018. p. 237-44.

[8] Adams S, Malinowski M, Heddy G, Choo B, Beling PA. The WEAR methodology for prognostics and health management implementation in manufacturing. J Manuf Syst 2017;45:82-96. https://doi.org/10.1016/j.jmsy.2017.07.002.

[9] Vingerhoeds RA, Janssens P, Netten BD, Aznar Fernández-Montesinos M. Enhancing off-line and on-line condition monitoring and fault diagnosis. Control Eng Pract 1995;3:1515-28. https://doi.org/10.1016/0967-0661(95)00162-N.

[10] Prajapati A, Bechtel J, Ganesan S. Condition based maintenance: a survey. J Qual Maint Eng 2012;18:384-400. https://doi.org/10.1108/13552511211281552.

[11] Scott D, Westcott VC. Predictive maintenance by ferrography. Wear 1977;44:173-82. https://doi.org/10.1016/0043-1648(77)90094-1.

[12] Tinga T, Loendersloot R. Aligning PHM, SHM and CBM by understanding the physical system failure behaviour. Proc. Eur. Conf. Progn. Heal. Manag. Soc. 201

[13] Kothamasu R, Huang SH, Verduin WH. System health monitoring and prognostics - A review of current paradigms and practices. Handb Maint Manag Eng 2006;28:1012-24. https://doi.org/10.1007/978-1-84882-472-0_14.

[14] Albrice D, Branch M. A deterioration model for establishing an optimal mix of time-based maintenance (TbM) and condition-based maintenance (CbM) for the enclosure system. Fourth Build. Enclos. Sci. Technol. Conf. 2015.

[15] MIMOSA. Open system architecture for condition-based maintenance (OSA-CBM) Available on 2001Http://WwwMimosaOrg/Mimosa-Osa-Cbm/.

[16] Lebold M, Reichard K, Byington CS, Orsagh R. OSA-CBM architecture development with emphasis on XML implementations. Maint Reliab Conf 2002.

[17] Montero Jiménez JJ, Vingerhoeds R. A system engineering approach to predictive maintenance systems: from needs and desires to logical architecture. 5th IEEE Int. Symp. Syst. Eng. 2019, Edinburgh 2019. https://doi.org/10.1109/ISSE46696.2019.8984559.

[18] Hussain A, Lee SJ, Choi MS, Brikci F. An expert system for acoustic diagnosis of power circuit breakers and on-load tap changers. Expert Syst Appl 2015;42:942-33. https://doi.org/10.1016/j.eswa.2015.07.079.

[19] Zhou A, Yu D, Zhang W. A research on intelligent fault diagnosis of wind turbines based on ontology and FMECA. Adv Eng Informatics 2015;29:115-25. https://doi.org/10.1016/j.aei.2014.10.001.

[20] Gang M, Linru J, Guchao X, Jianyong Z. A model of intelligent fault diagnosis of power equipment based on CBR. Math Problems Eng 2015.

[21] Chemweno P, Pintelon L, Jongers L, Muchiri P. I-RCAM: intelligent expert system for root cause analysis in maintenance decision making. 2016 IEEE Int. Conf. Progn. Heal. Manag. ICPHM 2016 2016. https://doi.org/10.1109/ICPHM.2016.7542830.

[22] Zhong Z, Xu T, Wang F, Tang T. Text case-based reasoning framework for fault diagnosis and predication by cloud computing. Math Probl Eng 2018:10. https:// doi.org/10.1155/2018/9464971.

[23] Baban M, Baban CF, Moisi B. A fuzzy logic-based approach for predictive maintenance of grinding wheels of automated grinding lines. 2018 23rd Int. Conf. Methods Model. Autom. Robot. MMAR 2018 2018. https://doi.org/10.1109/MMAR.2018.8486144.

[24] Berredjem T, Benidir M. Bearing faults diagnosis using fuzzy expert system relying on an Improved Range Overlaps and Similarity method. Expert Syst Appl 2018;108:134-42. https://doi.org/10.1016/j.eswa.2018.04.025.

[25] Li-Qiang H, Chao-Feng H, Zhao-Quan C, Long W, Teng R. Track circuit fault prediction method based on grey theory and expert systems. J Vis Commun Image Represent 2019;58:37-45.

[26] Tang X, Xiao M, Liang Y, Zhu H, Li J. Online updating belief-rule-base using Bayesian estimation. Knowl-Based Syst 2019;171:93-105. https://doi.org/10.1016/j.knosys.2019.02.007.

[27] Boral S, Chaturvedi SK, Naikan VNA. A case-based reasoning system for fault detection and isolation: a case study on complex gearboxes. J Qual Maint Eng 2019;25:213-35. https://doi.org/10.1108/JQME-05-2108-0039.

[28] Vafaei N, Ribeiro RA, Camarinha-Matos LM. Fuzzy early warning systems for condition based maintenance. Comput Ind Eng 2019;128:736-46. https://doi.org/10.1016/j.cie.2018.12.056.

[29] Bagheri B, Siegel D, Zhao W, Lee J. A stochastic asset life prediction method for large fleet datasets in big data environment. ASME 2015 Int. Mech. Eng. Congr. Expo. Vol. 14 Emerg. Technol. Saf. Eng. Risk Anal. Mater. Genet. to Struct. 2015. https://doi.org/10.1115/IMECE2015-52458.

[30] Menon S, Jin X, Chow TWS, Pecht M. Evaluating covariance in prognostic and system health management applications. Mech Syst Signal Process 2015;58-59:206-17. https://doi.org/10.1016/j.ymssp.2014.10.012.

[31] Verbert K, De Schutter B, Babuška R. Reasoning under uncertainty for knowledge-based fault diagnosis: a comparative study. IFAC-Papers OnLine 2015;48:422-7. https://doi.org/10.1016/j.ifacol.2015.09.563.

[32] Jin W, Shi Z, Siegel D, Dersin P, Douziech C, Pugnaloni M, et al. Development and evaluation of health monitoring techniques for railway point machines. 2015 IEEE Conf. Progn. Heal. Manag. Enhancing Safety, Effic. Availability, Eff. Syst. Through PHAf Technol. Appl. PHM 2015 2015. https://doi.org/10.1109/ICPHM.2015.7245016.

[33] Dababneh A, Ozbolat IT. Predictive reliability and lifetime methodologies for circuit boards. Int J Ind Manuf Syst Eng 2015;37:141-8. https://doi.org/10.1016/

j.jmsy.2015.08.001.

[34] Berecibar M, Devriendt F, Dubarry M, Villarreal I, Omar N, Verbeke W, et al. Online state of health estimation on NMC cells based on predictive analytics. J Power Sources 2016. https://doi.org/10.1016/j.jpwSOUR.2016.04.109.

[35] Mosallam A, Medjaher K, Zerhouni N. Data-driven prognostic method based on Bayesian approaches for direct remaining useful life prediction. J Intell Manuf 2016;27:1037-48. https://doi.org/10.1007/s10845-014-0933-4.

[36] Zhang D, Bailey AD, Djurdjanovic D. Bayesian identification of hidden Markov models and their use for condition-based monitoring. IEEE Trans Reliab 2016. https://doi.org/10.1109/TR.2016.2570561.

[37] Xiao Y, Wang H, Xu W, Zhou J. Robust one-class SVM for fault detection. Chemomet Intell Lab Syst 2016;151:15-25. https://doi.org/10.1016/j.chemolab.2015.11.010.

[38] Lee W-J. Anomaly detection and severity prediction of air leakage in train braking pipes. Int J Progn Heal Manag 2017;8:12. https://doi.org/10.1007/978-3-319-60045-1_22.

[39] Barraza-Barraza D, Tercero-Gómez VG, Beruvides MG, Limón-Robles J. An adaptive ARX model to estimate the RUL of aluminum plates based on its crack growth. Mech Syst Signal Process 2017;82:519-36. https://doi.org/10.1016/j.ymssp.2016.05.041.

[40] Verbert K, Babuska R, De Schutter B. Bayesian and Dempster-Shafer reasoning for knowledge-based fault diagnosis-A comparative study. Eng Appl Artif Intell 2017;60:136-50. https://doi.org/10.1016/j.engappai.2017.01.011.

[41] Li G, Wang X, Yang A, Rong M, Yang K. Failure prognosis of high voltage circuit breakers with temporal latent Dirichlet allocation. Energies 2017;10:1913. https://doi.org/10.3390/en10111913.

[42] Chen Z, Li Y, Xia T, Pan E. Hidden Markov model with auto-correlated observations for remaining useful life prediction and optimal maintenance policy. Reliab Eng Syst Saf 2017;184:123-36. https://doi.org/10.1016/j.ress.2017.09.002.

[43] Yung KC, Sun B, Jiang X. Prognostics-based qualification of high-power white LEDs using Lévy process approach. Mech Syst Signal Process 2017;82:206-16. https://doi.org/10.1016/j.ymsp.2016.05.019.

[44] Singh K, Malik H, Sharma R. Condition monitoring of wind turbine gearbox using electrical signatures. 2017 Int. Conf. Microelectron. Devices, Circuits Syst. ICMDCS 2017 2017. https://doi.org/10.1109/ICMDCS.2017.8211718.

[45] Gajewski J, Vališ D. The determination of combustion engine condition and reliability using oil analysis by MLP and RBF neural networks. Tribol Int 2017;115:557-72. https://doi.org/10.1016/j.triboint.2017.06.032.

[46] Zhao R, Wang D, Yan R, Mao K, Shen F, Wang J. Machine health monitoring using local feature-based gated recurrent unit networks. IEEE Trans Ind Electron 2017;65:1539-48. https://doi.org/10.1109/TIE.2017.2733438.

[47] Dong D, Li XY, Sun FQ. Life prediction of jet engines based on LSTM-recurrent neural networks. 2017 Progn. Syst. Heal. Manag. Conf. PHM-Harbin 2017 - Proc. 2017. https://doi.org/10.1109/PHM.2017.8079264.

[48] Mathew J, Luo M, Khiang Pang C. Regression kernel for prognostics with support vector machines. 22nd IEEE Int. Conf. Emerg. Technol. Fact. Autom. 2017.

[49] Shuangshuang J, Zhenhuan W, Yudong F, Guoan Y. The remaining life prediction of the fan bearing based on genetic algorithm and multi-parameter support vector machine. 5th Int. Conf. Mech. Automot. Mater. Eng. 2017.

[50] Haque MS, Bin Shaheed MN, Choi S. RUL estimation of power semiconductor switch using evolutionary time series prediction. 2018 IEEE Transp. Electrif. Conf. Expo, ITEC 2018 2018. https://doi.org/10.1109/ITEC.2018.8450131.

[51] Wan A, Gu F, Chen J, Zheng L, Hall P, Ji Y, et al. Prognostics of gas turbine: a condition-based maintenance approach based on multi-environmental time similarity. Mech Syst Signal Process 2018;109:150-65. https://doi.org/10.1016/j.ymsp.2018.02.027.

[52] Hu Y-W, Zhang H-C, Liu S-J, Lu H-T. Sequential Monte Carlo method toward online RUL assessment with applications. Chin J Mech Eng 2018:31. https://doi.org/10.1186/s10033-018-0205-x.

[53] Tang D, Sheng W, Yu J. Dynamic condition-based maintenance policy for degrading systems described by a random-coefficient autoregressive model: A comparative study. Eksploat I Niezawodn - Maint Reliab 2018;20:590-601. https:// doi.org/10.17531/ein.2018.4.10.

[54] Wang ZQ, Hu CH, Fan HD. Real-time remaining useful life prediction for a nonlinear degrading system in service: application to bearing data. IEEE/ASME Trans Mechatron 2018;23:211-22. https://doi.org/10.1109/TMECH.2017.2666199.

[55] Zhao S, Makis V, Chen S, Li Y. Evaluation of reliability function and mean residual life for degrading systems subject to condition monitoring and random failure. IEEE Trans Reliab 2018;67:13-25. https://doi.org/10.1109/TR.2017.2779322.

[56] Kinghorst J, Geramifard O, Luo M, Chan HL, Yong K, Folmer J, et al. Hidden Markov model-based predictive maintenance in semiconductor manufacturing: a genetic algorithm approach. IEEE Int. Conf. Autom. Sci. Eng. 2018. https://doi.org/10.1109/COASE.2017.8256274.

[57] Wu Z, Luo H, Yang Y, Lv P, Zhu X, Ji Y, et al. K-PdM: KPI-oriented machinery deterioration estimation framework for predictive maintenance using cluster-based hidden Markov model. IEEE Access 2018;6:41676-87. https://doi.org/10.1109/ACCESS.2018.2859922.

[58] Man J, Zhou Q. Prediction of hard failures with stochastic degradation signals using Wiener process and proportional hazards model. Comput Ind Eng 2018;125:480-9. https://doi.org/10.1016/j.cie.2018.09.015.

[59] Zhang Z, Si X, Hu C, Lei Y. Degradation data analysis and remaining useful life estimation: a review on Wiener-process-based methods. Eur J Oper Res 2018;271:775-96. https://doi.org/10.1016/j.ejor.2018.02.033.

[60] Vališ D, Mazurkiewicz D. Application of selected Levy processes for degradation modelling of long range mine belt using real-time data. Arch Civ Mech Eng 2018;18:1430-40. https://doi.org/10.1016/j.acme.2018.05.006.

[61] Aye SA, Heyns PS. Prognostics of slow speed bearings using a composite integrated Gaussian process regression model. Int J Prod Res 2018;56:4860-73. https://doi.org/10.1080/00207543.2018.1470340.

[62] Kong D, Chen Y, Li N. Gaussian process regression for tool wear prediction. Mech Syst Signal Process 2018;104:556-74. https://doi.org/10.1016/j.ymssp.2017.11.021.

[63] Ayo-Imoru RM, Cilliers AC. Continuous machine learning for abnormality identification to aid condition-based maintenance in nuclear power plant. Ann Nucl Energy 2018;118:61-70. https://doi.org/10.1016/j.anucene.2018.04.002.

[64] Luwei KC, Yunusa-Kaltungo A, Sha'aban YA. Integrated fault detection framework for classifying rotating machine faults using frequency domain data fusion and artificial neural networks. Machines 2018:6.

[65] Luo H, Huang M, Zhou Z. Integration of Multi-Gaussian fitting and LSTM neural networks for health monitoring of an automotive suspension component. J Sound Vib 2018;428:87-103. https://doi.org/10.1016/j.jsv.2018.05.007.

[66] Hinchi AZ, Tkiouat M. Rolling element bearing remaining useful life estimation based on a convolutional long-short-Term memory network. Procedia Comput Sci 2018;127:123-32. https://doi.org/10.1016/j.procs.2018.01.106.

[67] Li X, Ding Q, Sun JQ. Remaining useful life estimation in prognostics using deep convolution neural networks. Reliab Eng Syst Saf 2018;172:1-11. https://doi.org/10.1016/j.ress.2017.11.021.

[68] Von Birgelen A, Buratti D, Mager J, Niggemann O. Self-organizing maps for anomaly localization and predictive maintenance in cyber-physical production systems. Procedia CIRP 2018;72:480-5. https://doi.org/10.1016/j.procir.2018.03.150.

[69] Nyulászi L, Andoga R, Butka P, Fóžő L, Kovacs R, Moravec T. Fault detection and isolation of an aircraft turbojet engine using a multi-sensor network and multiple model approach. Acta Polytech Hungarica 2018;15:189-209.

[70] Li S, Fang H, Shi B. Multi-step-ahead prediction with long short term memory networks and support vector regression. Chinese Control Conf. 2018. https://doi.org/10.23919/ChiCC.2018.8484066.

[72] Onel M, Kieslich CA, Guzman YA, Pistikopoulos EN. Simultaneous fault detection and identification in continuous processes via nonlinear support vector machine based feature selection. Comput Aided Chem Eng 2018;44:2077-82. https://doi.org/10.1016/B978-0-444-64241-7.50341-4.

[71] Laib dit Leksir Y, Mansour M, Moussaoui A. Localization of thermal anomalies in electrical equipment using Infrared Thermography and support vector machine. Infrared Phys Technol 2018;89:120-8. https://doi.org/10.1016/j.infrared.2017.12.015.

[73] Ren L, Sun Y, Cui J, Zhang L. Bearing remaining useful life prediction based on deep autoencoder and deep neural networks. J Manuf Syst 2018;48:71-7. https:// doi.org/10.1016/j.jmsy.2018.04.008.

[74] Zhang J, Wang P, Yan R, Gao RX. Long short-term memory for machine remaining life prediction. J Manuf Syst 2018;48. https://doi.org/10.1016/j.jmsy.2018.05.011.78-76.

[75] Xu M, Jin X, Kamarthi S, Noor-E-Alam M. A failure-dependency modeling and state discretization approach for condition-based maintenance optimization of multi-component systems. J Manuf Syst 2018;47:141-52. https://doi.org/10.1016/j.jmsy.2018.04.018.

[76] Downey A, Lui Y-H, Hu C, Laflamme S, Hu S. Physics-based prognostics of lithiumion battery using non-linear least squares with dynamic bounds. Reliab Eng Syst Saf 2019;182:1-12.

[77] Li Y, Liu S, Shu L. Wind turbine fault diagnosis based on Gaussian process classifiers applied to operational data. Renew Energy 2019;134:357-66. https://doi.org/10.1016/j.jrenene.2018.10.088.

[78] M.Mehdi Hassani.N S, Xiaoning J, Jun N. Physics-based Gaussian process for the health monitoring for a rolling bearing. Acta Astronatica 2019;154:133-9.

[79] Huang W, Cheng J, Yang Y, Guo G. An improved deep convolutional neural network with multi-scale information for bearing fault diagnosis. Neurocomputing 2019;359:77-92. https://doi.org/10.1016/j.neucom.2019.05.052.

[80] Chen Z, Gryliias K, Li W. Mechanical fault diagnosis using convolutional neural networks and extreme learning machine. Mech Syst Signal Process 2019:133. https://doi.org/10.1016/j.ymssp.2019.106272.

[81] Chaoqun D, Chao D, Ning L. Reliability assessment for CNC equipment based on degradation data. Int J Adv Manuf Technol 2019;100:421-34.

[82] Eker OF, Camci F, Jennions IK. Physics-based prognostic modelling of filter clogging phenomena. Mech Syst Signal Process 2016;75:395-412. https://doi.org/10.1016/j.ymssp.2015.12.011.

[83] Climente-Alarcon V, Nair D, Sundaria R, Antonino-Daviu JA, Arkkio A. Combined model for simulating the effect of transients on a damaged rotor cage. IEEE Trans Ind Appl 2017. https://doi.org/10.1109/TIA.2017.2691001.

[84] Qiao G, Weiss BA. Quick health assessment for industrial robot health degradation and the supporting advanced sensing development. J Manuf Syst 2018;48:51-9. https://doi.org/10.1016/j.jmsy.2018.04.004.

[85] Li J, Xiao M, Liang Y, Tang X, Li C. Three-dimensional simulation and prediction of solenoid valve failure mechanism based on finite element model. IOP Conf. Ser. Earth Environ. Sci. 2018. https://doi.org/10.1088/1755-1315/108/2/022035.

[86] Cholette ME, Yu H, Borghesani P, Ma L, Geoff K. Degradation modeling and condition-based maintenance of boiler heat exchangers using gamma processes. Reliab Eng Syst Saf 2019;183:184-96.

[87] Liao WZ, Li D. An improved prediction model for equipment performance degradation based on Fuzzy-Markov Chain. IEEE Int. Conf. Ind. Eng. Eng. Manag. 2016. https://doi.org/10.1109/IEEM.2015.7385597.

[88] Chang Y, Fang H, Zhang Y. A new hybrid method for the prediction of the remaining useful life of a lithium-ion battery. Appl Energy 2017;206:1564-78. https://doi.org/10.1016/j.apenergy.2017.09.106.

[89] Hanachi H, Liu J, Kim IY, Mechefske CK. Hybrid sequential fault estimation for multi-mode diagnosis of gas turbine engines. Mech Syst Signal Process 2019;115:225-68. https://doi.org/10.1016/j.ymssp.2018.05.054.

[90] Jiang Y, Zhu H, Ding C, Pfeiffer O. A novel ensemble fuzzy model for degradation prognostics of rolling element bearings. J Intell Fuzzy Syst 2019;37:4449-55. https://doi.org/10.3233/JIFS-17927.

[91] Al-Dulaimi A, Zabihi S, Asif A, Mohammadi A. A multimodal and hybrid deep neural network model for remaining useful life estimation. Comput Ind 2019;108:186-96. https://doi.org/10.1016/j.compind.2019.02.004.

[92] Chiachio J, Chiachio M, Prescott D, Andrews J. A knowledge-based prognostics framework for railway track geometry degradation. Reliab Eng Syst Saf 2019;181:127-41. https://doi.org/10.1016/j.ress.2018.07.004.

[93] Che C, Wang H, Fu Q, Ni X. Combining multiple deep learning algorithms for prognostic and health management of aircraft. Aerosp Sci Technol 2019:94. https://doi.org/10.1016/j.ast.2019.105423.

[94] Lu F, Wu J, Huang J, Qiu X. Aircraft engine degradation prognostics based on logistic regression and novel OS-ELM algorithm. Aerosp Sci Technol 2019;84:661-71. https://doi.org/10.1016/j.ast.2018.09.044.

[95] Ferreiro S, Konde E, Fernandez S, Prado A. Industry 4.0: predictive intelligent maintenance for production equipment. Eur. Conf. Progn. Heal. Manag. Soc. 2016.

[96] Javed K, Gouriveau R, Zerhouni N. State of the art and taxonomy of prognostics approaches, trends of prognostics applications and open issues towards maturity at different technology readiness levels. Mech Syst Signal Process 2017;94:214-36. https://doi.org/10.1016/j.vmssp.2017.01.050.

[97] Sakib N, Wuest T. Challenges and opportunities of condition-based predictive maintenance: a review. 6th CIRP Glob. Web Conf. "Envisaging Futur. Manuf. Des. Technol. Syst. Innov. era." Elseiver B.V. 2018:267-72.

[98] Alaswad S, Xiang Y. A review on condition-based maintenance optimization models for stochastically deteriorating system. Reliab Eng Syst Saf 2017;157:54-63. https://doi.org/10.1016/j.ress.2016.08.009.

[99] International Organization for Standardization (ISO). ISO 13379-1:2012 - Condition monitoring and diagnostics of machines - Data interpretation and diagnostics techniques - Part 1: general guidelines. 2012.

[100] Gouriveau R, Medjaher K, Zerhouni N. From prognostics and health systems management to predictive maintenance 1: monitoring and prognostics. 2016. https://doi.org/10.1002/9781119371052.

[101] Vogl GW, Weiss Ba, Donmez MA. Standards for prognostics and health management (PHM) techniques within manufacturing operations. Annu Conf Progn Heal Manag Soc 2014.

[102] Vachtsevanos G, Lewis F, Roemer M, Hess A, Wu B. Intelligent fault diagnosis and prognosis for engineering systems. 2007. https://doi.org/10.1002/9780470117842.

[103] Zerhouni N, Atamuradov V, Medjaher K, Dersin P, Lamoureux B. Prognostics and health management for maintenance practitioners-review, implementation and tools evaluation. Artic Int J Progn Heal Manag 2017;8:31. https://doi.org/10. 1016/j.euprot.2015.07.015.

[104] Jardine AKS, Lin D, Banjevic D. A review on machinery diagnostics and prognostics implementing condition-based maintenance. Mech Syst Signal Process 2006;20:1483-510. https://doi.org/10.1016/j.ymssp.2005.09.012.

[105] Wang D, Tsui KL, Miao Q. Prognostics and health management: a review of vibration based bearing and gear health indicators. IEEE Access 2017;6:665-76. https://doi.org/10.1109/ACCESS.2017.2774261.

[106] An D, Kim NH, Choi JH. Practical options for selecting data-driven or physics-based prognostics algorithms with reviews. Reliab Eng Syst Saf 2015;133:223-36. https://doi.org/10.1016/j.resch.2014.09.014.

[107] Noman MA, Nasr ESA, Al-Shayyea A, Kaid H. Overview of predictive condition based maintenance research with bibliometric indicators. J King Saud Univ - Eng Sci 2018. https://doi.org/10.1016/j.jksues.2018.02.003.

[108] Schmidt B, Wang L. Predictive maintenance: literature review and future trends. Conf Proc 25th Int Conf Flex Autom Intell Manuf 2015;1:232-9.

[109] Dragomir OE, Gouriveau R, Dragomir F, Minca E, Zerhouni N. Review of prognostic problem in condition-based maintenance. Eur. Control Conf. (ECC'09) 2009. https://doi.org/10.1128/JB.00591-09.

[110] Sikorska JZ, Hodkiewicz M, Ma L. Prognostic modelling options for remaining useful life estimation by industry. Mech Syst Signal Process 2011;25:1803-36. https://doi.org/10.1016/j.ymssp.2010.11.018.

[111] Okoh C, Roy R, Mehnen J, Redding L. Overview of remaining useful life prediction techniques in through-life engineering services. Procedia CIRP 2014;16:158-63. https://doi.org/10.1016/j.procir.2014.02.006.

[112] Boullart L. A gentle introduction to artificial intelligence. In: Boullart L, Krijgsman A, Vingerhoeds RA, editors. Appl. Artif. Intell. Process Control. Pergamon Press; 1992. p. 5-40.

[113] Liu H, Yu J, Zhang P, Li X. A review on fault prognostics in integrated health management. ICEMI 2009 - Proc. 9th Int. Conf. Electron. Meas. Instruments 2009. https://doi.org/10.1109/ICEMI.2009.5274082.

[114] Majstorovic VD, Milacic VR. Expert systems for maintenance in the CIM concept. Comput Ind 1990;15:83-93.

[115] Freyermuth B. Knowledge based incipient fault diagnosis of industrial robots. IFAC Proc Vol 1991;24:369-75.

[116] Agnar A, Plaza E. Case-Based reasoning: Foundational issues, methodological variations, and system approaches. AI Commun 1994;7:39-59. https://doi.org/10.3233/AIC-1994-7104.

[117] Vepa R. Introduction to fuzzy logic and fuzzy sets. In: Boulart L, Krijgsm A, Vingerhoeds RA, editors. Appl. Artif. Intell. Process Control. 1991. p. 146-63

[118] Ruiz PP, Foguem BK, Grabot B. Generating knowledge in maintenance from Experience Feedback. Knowl-Based Syst 2014;68:4-20. https://doi.org/10.1016/j.

knosys.2014.02.002.

[119] Grabot B. Rule mining in maintenance: analysing large knowledge bases. Comput Ind Eng 2018;139:105501 https://doi.org/10.1016/j.cie.2018.11.011.

[120] Ramasso E. Investigating computational geometry for failure prognostics. Int J Progn Heal Manag 2014;5:18.

[121] Kumar P, Srivastava RK. An expert system for predictive maintenance of mining excavators and its various forms in open cast mining. 2012 1st Int. Conf. Recent Adv. Inf. Technol. RAIT-2012 2012. https://doi.org/10.1109/RAIT.2012.6194607.

[122] Zhou ZJ, Hu CH, Xu DL, Chen MY, Zhou DH. A model for real-time failure prognosis based on hidden Markov model and belief rule base. Eur J Oper Res 2010;207:269-83. https://doi.org/10.1016/j.ejor.2010.03.032.

[123] Yang BS, Jeong SK, Oh YM, Tan ACC. Case-based reasoning system with Petri nets for induction motor fault diagnosis. Expert Syst Appl 2004;27:301-11. https://doi.org/10.1016/j.eswa.2004.02.004.

[124] Li S, Lv C, Guo Z, Wang M. Health condition-based maintenance decision intelligent reasoning method. Proc. 2012 Int. Conf. Qual. Reliab. Risk, Maintenance, Saf. Eng. ICQR2MSE 2012 2012. https://doi.org/10.1109/ICQR2MSE.2012. 6246263.

[125] Phillips P, Diston D. A knowledge driven approach to aerospace condition monitoring. Knowl-Based Syst 2011;24:915-27. https://doi.org/10.1016/j.knosys.2011.04.008.

[126] Kothamasu R, Huang SH. Adaptive Mamdani fuzzy model for condition-based maintenance. Fuzzy Sets Syst 2007;158:2715-33. https://doi.org/10.1016/j.fss.2007.07.004.

[127] Sankararaman S, Daigle MJ, Goebel K. Uncertainty quantification in remaining useful life prediction using first-order reliability methods. IEEE Trans Reliab 2014;63:603-19. https://doi.org/10.1109/TR.2014.2313801.

[128] Moutinho MN. Fuzzy diagnostic systems of rotating machineries, some Eletronorte's applications. 2009 15th Int. Conf. Intell. Syst. Appl. to Power Syst. ISAP' 09 2009. https://doi.org/10.1109/ISAP.2009.5352882.

[129] Coble JB, Hines JW. Applying the general path model to estimation of remaining useful life. Int J Progn Heal Manag 2011;2:13.

[130] Du X, Zhou Y, Dong S. Residual life prediction from statistical features and a GARCH modeling approach for aircraft generators. Proc Inst Mech Eng Part G J Aerosp Eng 2014;228:137-46. https://doi.org/10.1177/0954410012472838.

[131] Zhan Y, Mechefske CK. Robust detection of gearbox deterioration using compromised autoregressive modeling and Kolmogorov-Smirnov test statistic. Part II: experiment and application. Mech Syst Signal Process 2007;21:1983-2011. https://doi.org/10.1016/j.ymssp.2006.11.006.

[132] Zhan Y, Mechefske CK. Robust detection of gearbox deterioration using compromised autoregressive modeling and Kolmogorov-Smirnov test statistic-Part I: compromised autoregressive modeling with the aid of hypothesis tests and simulation analysis. Mech Syst Signal Process 2007;21:1953-82. https://doi.org/10.1016/j.ymssp.2006.11.005.

[133] Cheng C, Yu L, Chen L. Structural nonlinear damage detection based on ARMA-GARCH model. Appl Mech Mater 2012;204-208:2891-6. https://doi.org/10.4028/www.scientific.net/AMM.204-208.2891.

[134] Ghahramani S. Fundamentals of probability: with stochastic processes. Third edition 2015. https://doi.org/10.1201/b19602.

[135] Pourbabae B, Meskin N, Khorasani K. Multiple-model based sensor fault diagnosis using hybrid Kalman filter approach for nonlinear gas turbine engines. 2013 Am Control Conf 2013. https://doi.org/10.1109/TCST.2015.2480003.

[136] Hu C, Youn BD, Wang P, Taek Yoon J. Ensemble of data-driven prognostic algorithms for robust prediction of remaining useful life. Reliab Eng Syst Saf 2012;103:120-35. https://doi.org/10.1016/j.ress.2012.03.008.

[137] Rasmussen CE, Williams CKI. Gaussian process for machine learning. the MIT Press; 2006.

[138] Rasmussen CE. Gaussian processes in machine learning. In: Bousquet O, von Luxburg U, Ratsch G, editors. Adv. Lect. Mach. Learn. Springer; 2003. p. 63-71.

[139] Kan MS, Tan ACC, Mathew J. A review on prognostic techniques for non-stationary and non-linear rotating systems. Mech Syst Signal Process 2015;62-63:1-20. https://doi.org/10.1016/j.ymsssp.2015.02.016.

[140] Markov A. Extension of the limit theorems of probability theory to a sum of variables connected in a chain. Append. B R. Howard. Dyn. Probabilistic Syst. Vol. 1 Markov Chain. John Wiley and Sons; 1971. https://doi.org/citeulike-article-id:911035.

[141] Protter PE. Stochastic integration and differential equations. Second edition Springer; 2005.

[142] Rudnicki R, Tyran-Kamińska M. Piecewise deterministic processes in biological models. Springer; 2017.

[143] Aye SA, Heyns PS. An integrated Gaussian process regression for prediction of remaining useful life of slow speed bearings based on acoustic emission. Mech Syst Signal Process 2017;84:485-98. https://doi.org/10.1016/j.ymssp.2016.07.039.

[144] Kobayashi K, Kaito K, Lethanh N. A statistical deterioration forecasting method using hidden Markov model for infrastructure management. Transp Res Part B Methodol 2012;46:544-61. https://doi.org/10.1016/j.trb.2011.11.008.

[145] Le Son K, Fouladirad M, Barros A, Levrat E, Iung B. Remaining useful life estimation based on stochastic deterioration models: a comparative study. Reliab Eng Syst Saf 2013;112:165-75. https://doi.org/10.1016/j.resh.2012.11.022.

[146] Russel S, Norvig P. Artificial intelligence-A modern approach. 3rd edition 2012. https://doi.org/10.1017/S0269888900007724.

[147] Schwartz S, Montero Jiménez JJ, Salain M, Vingerhoeds R. A fault mode identification methodology based on self-organizing map. Neural Comput Appl 2020:1-19.

[148] Koprinkova-Hristova P. Reinforcement learning for predictive maintenance of

industrial plants. Inf Technol Control 2014;11:21-8. https://doi.org/10.2478/itc 2013-0004.

[149] Wells G. An introduction to neural networks. In: Boullart L, Krijgsm A, Vingerhoeds RA, editors. Appl. Artif. Intell. Process Control. 1992. p. 164-200.

[150] Hailesilassie. Rule extraction algorithm for deep neural networks: a review. Int J Comput Sci Inf Secur 2016;14:371-81.

[151] Zhao Y, Wang S, Xiao F. Pattern recognition-based chillers fault detection method using Support Vector Data Description (SVDD). Appl Energy 2013;112:1041-8. https://doi.org/10.1016/j.apenergy.2012.12.043.

[152] Nasution FP, Sævik S, Gjøsteen JKØ. Fatigue analysis of copper conductor for offshore wind turbines by experimental and FE method. Energy Procedia 2012;24:271-80. https://doi.org/10.1016/j.egypro.2012.06.109.

[153] Si XS, Wang W, Hu CH, Zhou DH. Remaining useful life estimation - A review on the statistical data driven approaches. Eur J Oper Res 2011;213:1-14. https://doi.org/10.1016/j.ejor.2010.11.018.

[154] Liao L, Kottig F. Review of hybrid prognostics approaches for remaining useful life prediction of engineered systems, and an application to battery life prediction. IEEE Trans Reliab 2014;63:191-207. https://doi.org/10.1109/TR.2014.2299152.

[155] Soualhi A, Razik H, Clerc G, Doan DD. Prognosis of bearing failures using hidden markov models and the adaptive neuro-fuzzy inference system. IEEE Trans Ind Electron 2014;61:2864-74. https://doi.org/10.1109/TIE.2013.2274415.

[156] Chen J, Roberts C, Weston P. Fault detection and diagnosis for railway track circuits using neuro-fuzzy systems. Control Eng Pract 2008;16:585-96. https://doi.org/10.1016/j.conengprac.2007.06.007.

[157] Prentzas J, Hatzilygeroudis I. Combinations of case-based reasoning with other intelligent methods. CEUR Workshop Proc. 2008. https://doi.org/10.3233/his-2009-0096.

[158] Tung YH, Tseng SS, Weng JF, Lee TP, Liao AYH, Tsai WN. A rule-based CBR approach for expert finding and problem diagnosis. Expert Syst Appl 2010. https://doi.org/10.1016/j.eswa.2009.07.037.

[159] Peel L. Data driven prognostics using a Kalman filter ensemble of neural network models. 2008 Int. Conf. Progn. Heal. Manag. PHM 2008 2008. https://doi.org/10.1109/PHM.2008.4711423.

[160] Li X, Qian J, Wang GG. Fault prognostic based on hybrid method of state judgment and regression. Adv Mech Eng 2013. https://doi.org/10.1155/2013/149562.

[161] Kacprzynski GJ, Sarlashkar A, Roemer MJ, Hess A, Hardman W. Predicting remaining life by fusing the physics of failure modeling with diagnostics. JOM 2004;56:29-35. https://doi.org/10.1007/s11837-004-0029-2.

[162] Oppenheimer CH, Loparo KA. Physically based diagnosis and prognosis of cracked rotor shafts. Compon. Syst. Diagn., Progn. Heal. Manag. 2002;II. https://doi.org/

10. 1117/12.475502.

[163] Meskin N, Naderi E, Khorasani K. A multiple model-based approach for fault diagnosis of jet engines. IEEE Trans Control Syst Technol 2013;21:254-62. https://doi.org/10.1109/TCST.2011.2177981.

[164] Swanson DC. A general prognostic tracking algorithm for predictive maintenance. IEEE Aerosp. Conf. Proc. 2001. https://doi.org/10.1109/aero.2001.931317.

[165] Wang P, Youn BD, Hu C. A generic probabilistic framework for structural health prognostics and uncertainty management. Mech Syst Signal Process 2012;28:622-37. https://doi.org/10.1016/j.ymssp.2011.10.019.

[166] Riad AM, Elminir HK, Elattar HM. Evaluation of neural networks in the subject of prognostics as compared to linear regression model. Int J Eng Technol 2010;10:52-8.

[167] Neerukatti RK, Liu KC, Kovvali N, Chattopadhyay A. Fatigue life prediction using hybrid prognosis for structural health monitoring. J Aerosp Inf Syst 2014;11:211-32. https://doi.org/10.2514/1.1010094.

[168] Hong J, Miao X, Han L, Ma Y. Prognostics model for predicting aero-engine bearing grade-life. Proc. ASME Turbo Expo 2009. https://doi.org/10.1115/ GT2009-59641.

[169] Orsagh RF, Sheldon J, Klenke CJ. Prognostics/diagnostics for gas turbine engine bearings. IEEE Aerosp. Conf. Proc. 2003. https://doi.org/10.1109/AERO.2003.1234152.

[171] Crawley E, Cameron B, Selva D. System architecture: strategy and product development for complex systems. Pearson Higher Education, Inc.; 2015.

[170] Lee J, Wu F, Zhao W, Ghaffari M, Liao L, Siegel D. Prognostics and health management design for rotary machinery systems - reviews, methodology and applications. Mech Syst Signal Process 2014;42:314-34. https://doi.org/10.1016/j.ymssp.2013.06.004.

[172] Peng Y, Dong M, Zuo MJ. Current status of machine prognostics in condition-based maintenance: a review. Int J Adv Manuf Technol 2010;50:297-313. https://doi.org/10.1007/s00170-009-2482-0.

[173] Bailey C, Sutharsarst T, Yin C, Stoyanov S. Prognostic and health management for engineering systems: a review of the data-driven approach and algorithms. J Eng 2015;2015:215-22. https://doi.org/10.1049/joe.2014.0303.

[174] Elattar HM, Elminir HK, Riad AM. Prognostics: a literature review. Complex Intell Syst 2016;2:125-54. https://doi.org/10.1007/s40747-016-0019-3.

[175] Vanraj Goyal D, Saini A, Dhami SS, Pabla BS. Intelligent predictive maintenance of dynamic processing techniques-A review. Proc. - 2016 Int. Conf. Adv. Comput. Commun. Autom. ICACCA Systems Using Condition Monitoring and Signal 2016 2016. https://doi.org/10.1109/ICACCA.2016.7578870.

## 2.3 Lessons learnt

Article 1 of the current manuscript has shown an extensive study on the current trends of predictive maintenance. It allowed determining that multi-model approaches are increasingly used to address complex problems of diagnostics and prognostics. Multi-model approaches benefit from the strong points of different models allowing to overcome single-model approach limitations. The state-of-the-art analysis allowed to refine the research questions for the current thesis. These refined research questions are:

1. How to address the design of predictive maintenance systems?

2. How to suggest a suitable approach for a predictive maintenance system solution?

3. How to select a suitable model or combination of models given a new predictive maintenance problem to solve?

4. How can a designer benefit from the experience of existing systems to develop new predictive maintenance solutions?

These questions are inspired by the first two identified challenges of Article 1: the extrapolation of existing solutions to complex system applications, and the lack of a systematic approach to design and develop predictive maintenance systems. The following chapters explain the proposed framework of the current thesis that attempts to answer these questions.

<div align="center">

# From needs and desires to a generic logical architecture for predictive maintenance systems

</div>

<table border="1"><tr><td></td><td></td><td colspan="2">“Creativity is intelligence having fun.”</td></tr><tr><td></td><td></td><td colspan="2">Albert Einstein</td></tr><tr><td>Content</td><td></td><td></td><td></td></tr><tr><td>3.1</td><td>The creative process begins</td><td>31</td><td></td></tr><tr><td>3.2</td><td>A systems engineering approach to predictive maintenance systems: from needs and desires to logical architecture(Article2)</td><td>32</td><td></td></tr><tr><td>3.3</td><td>Lessons learnt</td><td>41</td><td></td></tr></table>

## 3.1 The creative process begins

The first refined question is about the design of new predictive maintenance systems. In the research statement presented in Chapter 1, it was explained that the design and development of predictive maintenance systems is still based on trial and error. Despite the existence of several generic architectures in norms and standards, such as for example [MIM01], the concept stage of such systems is not fully covered. There is a gap in the development of such systems from the gathering of needs and desires for the new system until the creation of the architecture that meets the initial needs and desires.

Creating a new system should always start by listening to those who are related or interested in the project, referred to as stakeholders. They provide all the needs and desires to be fulfilled by a new system. These needs and desires are the information source to establish the list of stakeholder requirements of the new system. The current research proposes a systems engineering approach to cover the concept stage of predictive maintenance systems. Special importance is given to the gathering of needs and desires and their translation into a formal set of stakeholder requirements. This provides the basis to build the system architecture for a new predictive maintenance system.

3. 2 A systems engineering approach to predictive maintenance systems: from needs and desires to logical architecture (Article 2)

The content in this section corresponds to a published work in the 5th IEEE International Symposium of Systems Engineering (ISSE) held in 2019 in Edinburgh, United Kingdom. $ \circled{C} $IEEE 2019. Reprinted, with permission, from Juan José Montero Jiménez and Rob Vingerhoeds. "A System Engineering Approach to Predictive Maintenance Systems: from needs and desires to logical architecture." In: 5th IEEE Int. Symposium on Systems Engineering 2019, Edinburgh, 2019 [MV19]. This article is referred to as Article 2 in the current manuscript.

<div align="center">

# A Systems Engineering Approach to Predictive Maintenance Systems: from needs and desires to logical architecture.

</div>

Juan José Montero Jiménez

ISAE-SUPAERO, Toulouse, France

juan-jose.montero-jimenez@isae-supaero.fr

TEC, Tecnológico de Costa Rica

juan.montero@itcr.ac.cr

Rob Vingerhoeds

ISAE-SUPAERO

Université de Toulouse

Toulouse, France

b.vingerhoeds@isae-supaero.fr

Abstract—Predictive maintenance is an important field of research to determine the exact moment to trigger maintenance actions. Despite the potential benefits of predictive maintenance in terms of maintenance cost reduction and safety improvement, its implementation faces many shortcomings. One of the main shortcomings is the lack of a systematic approach to developing predictive maintenance systems. Existing generic architectures like OSA-CBM remain insufficient to address all requirements for new systems. A systems engineering approach starting from the needs and desires obtained from the stakeholders until a logical architecture is a potential solution. Specific analysis on the needs and desires is used to elicit, classify and prioritize the requirements for an easier transition to designing the systems architecture. The architecture process builds on the ARCADIA method.

Keywords— Predictive Maintenance, Systems engineering requirements elicitation, Architecture Process.

## I. INTRODUCTION

Safe and efficient operation is of crucial importance for modern technical systems. Maintenance constitutes a vital discipline along the systems life-cycle to ensure their functionality. Within the maintenance strategies three types could be distinguished: corrective, preventive and predictive maintenance. In particular predictive maintenance is under a lot of attention at the moment and aims at analyzing relevant data to define the best possible moment to trigger maintenance actions [1]. Triggering too late may lead to failure occurrence, causing financial loses, sometimes image damage and may even lead to causalities and/or losses of human lives. Triggering too early may lead to replacing components that are not faulty through costly interventions.

Predictive maintenance proposes a solution by monitoring the health state of the technical system, identifying incipient faults and forecasting the moment of failure. Such predictive maintenance activities include several online and off-line tasks on the system information coming from different knowledge sources so to better understand the faults evolutions over time and trigger the corresponding action before failures occur. Current fast expanding trends such as machine learning, internet of things, Industry 4.0, big data, boost predictive maintenance implementation to reach safer, more reliable and more efficient technical systems.

Despite important benefits linked to use of predictive maintenance [2], its implementation faces many shortcomings. One of the root causes may concern to the absence of a systematic development approach fur such systems. Some generic architecture approaches to predictive maintenance, such as Open System Architecture for

Condition-Based Maintenance (OSA-CBM $ ^{\mathrm{TM}} $ ）[3] and the functional architecture presented in [4], propose different functional components of predictive maintenance systems. However, constraints can be identified on these solutions that may limit the usability to a smaller subset of applications or more complex scopes. Important missing parts concern for example performance indicators, potential structural constraints or partial imposed solutions, human factors, etc., hardly addressed in these generic architectures. The lack of performance indicators is pointed by [5] as one of main blocking points to validate new predictive maintenance systems.

The purpose of the current study is to propose a systematic development method for off-line predictive maintenance applications using a systems engineering approach covering from the earliest conceptual stages, to the concept identification and architecture proposal. The motivation is to have a wider overview on the needs and desires of the stakeholders related to a new predictive maintenance system, aiming to identify important information that may be missed by existing architectural approaches. It also includes a requirements prioritization process that aims at reducing ambiguity among the initial list of needs and desires, setting the boundaries of the new system scope. These preliminary steps help in the architecture process to determine the most suitable solution for a new predictive maintenance system.

The current study builds on existing concept design theories [6], [7], the notion of prioritization in taking into account requirements during the development process [8], and on the ARCADIA method [9]. These three building blocks allow for a structured development process, in this paper applied to predictive maintenance. The paper is organized as follows. Section 2 describes the predictive maintenance challenges as studied within the framework of this research. Section 3 resumes the theoretical framework of the approach of the architecture process. Section 4 presents the system engineering approach to predictive maintenance systems development at conceptual phases. Section 5 extends the architecture analysis using the case study. Section 6 draws conclusions and indicates some path for future research on this topic.

## II. PREDICTIVE MAINTENANCE CONTEXT

Predictive maintenance is a maintenance strategy aiming at monitoring the health state of the system, detecting incipient faults and forecasting potential failure in the future to trigger the maintenance actions accurately when they are needed. As such it is a complementary strategy to corrective and preventive maintenance. A good

combination of the three techniques is vital to keep the system reliable [1]. Condition Based Maintenance (CBM) and Prognostics and Health Management (PHM) are strongly related to predictive maintenance. There exists a terminology disagreement between the definition of these terms on literature, for this study, CBM and PHM are considered as extensions of predictive maintenance.

Two main approaches can be identified ([10] - [13]): a diagnostics approach aims at determining the current health state of the system and the identification of the faults through the symptoms, and a prognostics approach aims at forecasting future failures and the remaining useful life of the technical systems.

For both approaches a vast set of techniques exist, suitable to specific cases of technical systems depending on the availability of knowledge on the concerned technical system and its complexity. One can see knowledge-based models, data-driven models and physics-based models [13]. In addition, as it is almost impossible to model any real-life application by using only one single technique [14], hybrid models combining several techniques are gaining attention. As each technique has its own characteristic advantages concerning the availability of knowledge, knowledge representation, learning capabilities, etc., a technique should be selected to best fit a given task. The different parts of predictive maintenance could therefore benefit from the best knowledge representation technique for each task [14].

As each technical system has its own application context, generic architectures approaches like OSA-CBM [3], which is based on the standard ISO-13374 [15], may not be suitable for the development of a new predictive maintenance system. Important missing information such as performance indicators, structural constraints and the operability by the users is not considered in these generic approaches. As [5] suggests, performance requirements are often blocking points to develop predictive maintenance systems. This lack of a systematic approach to develop new predictive maintenance systems motivates the current study.

## III. SYSTEMS ENGINEERING APPROACH AT THE CONCEPTUAL PHASE

A system, as defined by the International Council of System Engineering (INCOSE), is "an integrated set of elements, subsystems, or assemblies that accomplish a defined objective" [16]. A systems engineering approach will give objectivity to problem solution by analyzing and understanding the desired behavior of the system, the interactions between the internal components to achieve the desired objective all along the system life-cycle, as well as the interfaces to the outside world.

One of the critical phases in any systems development is the concept design stage that focusses on the concept: understanding the implications of a system mission and core functionality, a business case together with requirements, their interconnections and dependencies specified in e.g. key performance indicators and trade-off indicators. Expressed (and potentially clarified) stakeholder needs and desires are translated into requirements. This stage results in a document describing a system mission, desired functionality, initial (qualified) requirements, and performance indicators (to determine in a later stage whether the desired functionality performance has been delivered). It also includes a description of a logical

architecture of the system design and its subsystems (the upper-level architecture) that meets system requirements: a preliminary design of the product or service to develop [7].

The section presents a combination of three complementary methods that allow developers to be guided through the conceptual stage of a system.

## A. Requirement elicitation and different type of requirement

John Gero suggested in [6] that three types of requirements exist (functional, behavioral, and structural), a proposal later extended to include a fourth type (experiential) [7] (see Fig.1). Specifically: functional requirements state functions that a system must provide and are directly related to the mission of a system; behavioral requirements specify desired system behavior of a design with respect to its mission, together with key performance indicators with which this behavior can be determined; structural requirements define requirements for components/sub-systems of a system and their interdependencies, and experiential requirements define the desired impact of a system in the real world with real people [7]. Each of these categories has a unique contribution to the design and development process. For example, the functional requirements correspond in a first step to the system capabilities that the designer needs to address, etc. An important step in system development is therefore the understanding and translation of stakeholders' needs and desires into functional, structural, behavioral, and experiential requirements.

As requirements elicitation method, this needs and desires analysis approach (FBSE analysis, for Functional, Behavioral, Structural and Experiential) helps to integrally address the requirements of the stakeholders for the predictive maintenance system. It could be performed iteratively and recursively at the different levels of the system as some components of the system are systems themselves that need a complete design process on which a systems engineering approach should be also applied.

## B. Requirements prioritization

Starting from better organized requirements, split into functional, behavioral, structural and experiential, it may be beneficial to prioritize the obtained requirements, so to end up with a reduced complexity, thus increasing the chances on successful development. Prioritization reduces ambiguity on initial needs and desires and helps to define the system boundaries, as suggested by [8]. Different types of requirement prioritization techniques can be identified [17], of which nominal and ordinal techniques are used in the current study so that the requirements are properly classified and ranked. Nominal techniques classify the requirements into different categories, approach that can be complemented by ordinary scales to rank the importance of requirements within the categories.

<table border="1"><tr><td>Function</td><td>The purpose of the system</td><td>Why? For whom? Where?</td></tr><tr><td>Behavior</td><td>The way a system acts</td><td>How? When?</td></tr><tr><td>Structure</td><td>The components of a system and their relationships</td><td>What?</td></tr><tr><td>Experience</td><td>Feelings, emotions, perceptions associated with the system</td><td>With whom? By whom? With what effect?</td></tr></table>

<div align="center">

Fig.1. Functional, behavioral, structural and experiential requirements [7]

</div>

FBSE analysis as presented in the previous sub-section corresponds to a nominal prioritization. This helps development engineers to know with which requirements to work at any point in time during the development stage. Nevertheless, a complementary ordinal prioritization method is proposed to further reduce complexity. The current study builds upon the method proposed by [8].

The ordinal prioritization method divides the requirements into three categories: critical, important and desired. The method is used for ranking the requirements importance within their category. Critical requirements contain the three to seven absolute necessities for the system success [8]. Important requirements are not strictly necessary for success but they contribute to it. Finally desired requirements denote wishes. Requirements will have the format shown in Table I after prioritization.

## C. Systems Architecture Process

Systems architecture is the "the embodiment of concept, the allocation of physical/informational function to elements of form, and the definition of relationship among the elements and with the surrounding context" [8]. Architecting is a creative process in which the architect searches for innovative solutions to a specific problem.

The architecture process in the current study builds on ARCADIA method [9]. This is a multi-layer Model Based Systems Engineering approach (see Fig. 2). Four layers are available to represent the system architecture.

The first layer is the operational analysis on which is defined what the users of system need to accomplish. This layer summarizes the stakeholders' requirements obtained from the previous sub-sections.

The second layer is the analysis of the system needs, what the system has to accomplish for the users. Functional analysis takes place at this layer. It starts by the definition of the primary function of the system to be fulfilled. The primary function should be as neutral as possible, it means without suggesting the final solution to the problem. This avoids narrowing down the solution space from the beginning of the project. This primary function is meant to be identified from the prioritized stakeholder requirements. Then, the primary function is decomposed into sub-functions. Decomposition is a common method used to manage the complexity of the primary function and explore the potential solutions for system architecture. Functional analysis includes functional exchanges which are the internal interactions among the sub-functions to fulfill the primary function. Depending on the system complexity, each sub-function of the system may represent a complete subsystem for which the whole system engineering approach should be performed. The consistent set of functions and the different interactions among them represents the functional architecture.

The third layer is the logical architecture, how the system will work to fulfill expectations. This layer helps to summarize the identified concept and its decomposition into the different functional levels. Having the functional

<div align="center">

TABLE I. REQUIRMENTS WRITING FORMAT

</div>

<table border="1"><tr><td>Critical requirements</td><td>Important requirements</td><td>Desired requirements</td></tr><tr><td>The system shall...</td><td>The system should...</td><td>The system might...</td></tr></table>


> **Figure Description:**

This diagram illustrates a multi-layered systems engineering framework, divided into two main sections: "Need understanding" (top) and "Solution Architectural design" (bottom). The framework is organized into four horizontal layers, each associated with "ViewPoints" and specific architectural components. On the right, text labels define each layer: "Operational Analysis" (What the users of the system need to accomplish), "Functional & Non Functional Need" (What the system has to accomplish for the user), "Logical Architecture" (How the system will work to fulfill expectations), and "Physical Architecture" (How the system will be developed and built).

The top section, "Need understanding," contains two layers. The top layer, "Operational Analysis," features a set of nodes labeled A1, A2, and A3 connected by arrows, with A2 pointing to A1 and A3, and a dashed line connecting A2 to A1. To the right, a stack of documents labeled "Reqs" interacts with this layer via a double-headed arrow. Below this, the "Functional & Non Functional Need" layer contains nodes F1, F2, F3, F4, and F5. Arrows connect these nodes, with F1 pointing to F2 and F3, F2 pointing to F4, and F5 positioned between F2 and F4. Dashed lines trace dependencies from the Operational Analysis layer down to this layer.

The bottom section, "Solution Architectural design," contains two layers. The "Logical Architecture" layer consists of components C1, C2, and C3. Within C1 are nodes F1, F6, F21, and F22, with arrows indicating internal relationships. C2 and C3 are separate blocks, with C2 connected to C3 via a double arrow. Dashed lines connect nodes from the layer above to F1, F21, and F22. The "Physical Architecture" layer at the bottom contains components C11, C12, C2, C3, C4, and C1'. Nodes F1, F6, F21, F22, and F7 are distributed across these components. Below these components are labeled blocks for "Bases" and "Processors." 

Throughout the diagram, vertical arrows connect the "Reqs" stack to the Logical and Physical Architecture layers, indicating traceability. The entire structure is visually represented as stacked planes, with "ViewPoints" labeled on each level to denote the perspective of the architectural model.



<div align="center">

A: Operational activity F: Function C: Component

</div>

<div align="center">

Fig. 2. Arcadia method layers summary, recreated from [9].

</div>

architecture, each sub-function is allocated to logical components. Structured creativity could be used for allocating the functions to logical components [8]. The external and internal interfaces are identified as well as some system requirements. This set of logical components and the external and internal interfaces compose the logical architecture which starts to give technical meaning to the system. Further functional decomposition is performed at this layer depending on the system complexity. System requirements are identified along this architecture process.

The fourth and final layer is the Physical architecture, how the system will be developed and built. Here the rest of the system requirements are identified since the physical components to fulfill the logical architecture are selected.

## IV. SYSTEMS ENGINEERING APPROACH TO PREDICTIVE MAINTENANCE SYSTEMS

In this paragraph, the systems engineering approach to developing a predictive maintenance system is presented. The approach starts with a thorough analysis of the potential stakeholders and their needs and desires related to a predictive maintenance system. This analysis continues with an FBSE analysis so to classify the obtained requirements into functional, behavioral, structural and experiential. Then a requirements prioritization takes place, so to guide the developer on which requirements to address at which point in time. In the next phase, the ARCADIA method is being adopted so to work in a step-wise approach to the logical architecture.

The approach is illustrated with information from a case-study at the basis of the PHM'08 challenge [18]. In this challenge, engine condition monitoring on a 90,000 lb thrust class commercial jet aircraft engine was used. After every flight, performance engineers evaluate the evolution of engine critical parameters and derive from those analyzes to anticipate or to avoid incidents, to evaluate the effects of incidents or to provide a clear "no problem for the next few flights" indication. In the challenge the attention was at the data discovery, finding the engine problems present in the data sets. In the current study, we use the information on this particular example to illustrate the development process for predictive maintenance systems.

## A. Defining stakeholders'needs and desires

Needs and desires consider the base of what stakeholders expect from the system under development. Many possibilities exist to elicit these needs and desires (e.g. interviews, observation, work process analysis ...). In a first step, the stakeholders must be identified. Some potential stakeholders for a predictive maintenance system are summarized in Table II. Of course, depending on the technical system context some of these stakeholders may not be present or others not mentioned may be added to the list.

An initial list of needs and desires for predictive maintenance is gathered from a literature review [10] - [13], [18], [19] and is summarized in Table III. An ID is given for the traceability purpose of the needs and desires.

Let us note that not all the needs and desires are listed here. This list may be extended with specific needs and desires for a specific application. In the example of the jet engine, one may think of specific links to other tools or needs related to safety and reliability of the system.

## B. Eliciting and prioritizing requirements

Next, the aforementioned FBSE analysis is performed on the initial list of needs and desires. The goal is to classify the needs and desires into functional, behavioral, structural and experiential requirements. This will have an important impact on the set-up and elaboration of the system architecture. Then, the mentioned ordinary scale prioritization technique is used to rank of importance of the requirements.

In the case of the jet engine, the requested tasks included to compute the remaining useful life of the jet engines, considering the measured data coming from the engines sensors. These initial tasks were included in the list of initial needs and desires. Table IV now presents the list of initial stakeholders' requirements after applying the FBSE analysis and the ordinary scale prioritization method on the needs and desires on Table III. The related ID's of the original needs and desires are indicated.

As can be seen in Table IV, at the beginning of the development more functional requirements than behavioral or structural requirements were listed. Behavioral and structural requirements tend to appear step-by step as the design process goes into more detailed levels. Translating behavioral needs and desires into requirements demands a clear set of performance indicators coming for example from the technical system, the stakeholder goals and authorities' regulations. A good starting point to determine the performance indicator of the predictive maintenance system is a Failure Modes, Effects and Criticality Analysis (FMECA) over the technical system [20]. This analysis will

<div align="center">

TABLE II. POTENTIAL STAKEHOLDERS

</div>

<table border="1"><tr><td>Stakeholder</td><td>Illustration jet engine</td></tr><tr><td>Technical System owner</td><td>Airline, or rental company</td></tr><tr><td>Technical System user</td><td>Operating airline, MRO,...</td></tr><tr><td>Technical System manufacturer</td><td>Jet engine manufacturer</td></tr><tr><td>Predictive maintenance system developer(s)</td><td>Development company</td></tr><tr><td>Maintenance department or predictive maintenance system user</td><td>Operations departments at airlines, MRO&#x27;s,...</td></tr><tr><td>Corresponding authorities</td><td>FAA, EASA,...</td></tr></table>

<div align="center">

TABLE III. EXAMPLE OF NEEDS AND DESIRES LIST (NOT COMPLETE)

</div>

<table border="1"><tr><td>N°</td><td>List of needs and desires for predictive maintenance:</td></tr><tr><td>1</td><td>Improve safety of the systems compare to current condition</td></tr><tr><td>2</td><td>Reduce downtime of the system compare to current condition</td></tr><tr><td>3</td><td>Reduce maintenance costs compare to current condition</td></tr><tr><td>4</td><td>Identify what technique fits best to each predictive maintenance case.</td></tr><tr><td>5</td><td>Avoid unexpected breakdowns</td></tr><tr><td>6</td><td>Detect incipient faults</td></tr><tr><td>7</td><td>Identification of different types of faults</td></tr><tr><td>8</td><td>Determination of the current health state of the system</td></tr><tr><td>9</td><td>Failures Features selection and extraction</td></tr><tr><td>10</td><td>Enhance degradation determination accuracy</td></tr><tr><td>11</td><td>Remaining Useful Life (RUL) determination</td></tr><tr><td>12</td><td>Optimize maintenance schedules (time and cost performance indicators associated)</td></tr><tr><td>13</td><td>Decision making support in maintenance</td></tr><tr><td>14</td><td>Implementation of self-maintenance and self-adjustment</td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td>N</td><td>Additional need or desire</td></tr></table>

N Additional need or desire

<div align="center">

TABLE IV. EXAMPLE OF INITIAL LIST OF STAKEHOLDERS' REQUIREMENTS (NOT COMPLETE)

</div>

<table border="1"><tr><td>ID</td><td>Requirements</td><td>Traceability to Table III</td></tr><tr><td>F1</td><td>The system shall read the technical system data.</td><td>17-28</td></tr><tr><td>F2</td><td>The system should pre-process and “clean” the raw data.</td><td>17-20-23-24-25</td></tr><tr><td>F3</td><td>The system should detect incipient faults.</td><td>6-7-17</td></tr><tr><td>F4</td><td>The system should determine the current health state of the system.</td><td>5-7-8-17</td></tr><tr><td>F5</td><td>The system shall determine the remaining useful life.</td><td>11-17-29</td></tr><tr><td>F6</td><td>The system might suggest maintenance actions to the user.</td><td>13-17</td></tr><tr><td>F#</td><td>The system “additional functional requirement”</td><td>**</td></tr><tr><td>B1</td><td>The system should present a computational error less than “TBD”</td><td>27</td></tr><tr><td>B2</td><td>The system shall reduce the unexpected breakdown by “TBD”</td><td>2-3</td></tr><tr><td>B3</td><td>The system shall increase the system safety by “TBD”</td><td>1</td></tr><tr><td>B#</td><td>The system “additional behavioral”</td><td>**</td></tr><tr><td>S1</td><td>The system shall be compatible with the technical system (capable to read the technical system data format).</td><td>31</td></tr><tr><td>S2</td><td>The system shall have its own configuration management.</td><td>38</td></tr><tr><td>S3</td><td>The system should use specialized techniques and methods.</td><td>18</td></tr><tr><td>S#</td><td>The system might allow updates or upgrades.</td><td>**</td></tr><tr><td>E1</td><td>The system shall have a “friendly” interface with the user.</td><td>35</td></tr><tr><td>E#</td><td>The system “additional experiential requirement”</td><td>**</td></tr></table>

TBD: "To Be Defined".

(**): traceability to a potential additional need or desire.

lead to the critical failures for which the predictive maintenance system must be intended. Besides, historical maintenance, safety and financial reports or records are other sources of information to establish performance indicators.

It is important to point out that predictive maintenance can be seen as an improvement of other maintenance practices. This means that, building on previous maintenance strategy programs gives useful information. These prior maintenance programs may contain initial parameters to be improved from which the behavioral, structural and experiential requirements are established.

## C. Architecture process for the Predictive Maintenance System

For the jet engine example, using the FBSE analysis, six functions have been identified and prioritized. These functions are part of a higher level function related to every predictive maintenance system: "Estimate the precise moment to trigger maintenance actions". Next the identified functional requirements are proposed as sub-functions of the primary function (see Fig. 3).

This functional decomposition suggests the first mapping between functions and components of the system, allocating one function to each component. For validation and verification purposes is advisable to allocate one function to one component of the system.

## 1) Functional architecture

The functional architecture is built on top of the functional decomposition (see Fig. 4). It includes the interactions between the different functions (functional exchanges). For the jet-engine example, the collected data from the technical system (F1) is taken by F2 to be preprocessed. Later, F3 assesses the data to detect failures; if a failure is detected F4 may request additional preprocessed data to determine the degradation over time. Likewise, if the prognostics function is to be part of the predictive maintenance system under development (F5), it may request additional pre-processed data to compute the remaining useful life. The output of F2 serves as input for F3, F4 and F5 and it may include a sub-function to store the pre-processed data. The outputs of F3, F4 and F5 are the inputs for F6 in charge of generating the reports and/or triggering the maintenance actions in automated systems. The "request data" functional exchanges from F3, F4 and F5, as well as the external exchanges of the system, are not shown on Fig. 4 for layout purposes.

## 2) External interfaces identification

For an off-line predictive maintenance system, the inputs come from technical system databases that have stored historical data on the system to be maintained. The outputs link the system to a user interface and once again to the technical system data bases to keep track of the diagnostics and prognostics assessments, as well as eventual intermediate results of the analysis. These input and outputs represent the external interfaces of the predictive maintenance system. Fig. 5 shows the model of the predictive maintenance system interacting with the external actors through the external interfaces. These external actors are the technical system data bases and the predictive maintenance user. Blue boxes in Fig. 5 represent the system and the external actors, the link between them represent the external interfaces. Green boxes represent the functions of the system and actors, continuous lines between these green boxes are the functional exchanges. Dashed lines represent the functional exchanges flow through the external interfaces

## 3) Logical Architecture

Having the functional architecture of Fig. 4 and the external interfaces of Fig. 5, a logical architecture is proposed. Here the functions are allocated to logical components. As for the external interfaces, the interaction between the logical components of the system is analyzed to determine the internal interfaces of the system. Functional exchanges from Fig. 4 are the starting point for this internal interface analysis. As mentioned in section 3, structured creativity could be used for defining the logical component for the system. Fig. 6 shows a generic logical architecture for the predictive maintenance system. It proposes one logical component for each function. This allows the verification of each functional requirement separately. Besides the internal components, this logical architecture also presents the internal interfaces and the data flow through them. Internal functional exchanges between functions have been hidden for layout purposes on Fig. 6 but are shown on Fig. 4.

At this stage, the proposed logical architecture remains generic. Logical components are to be replaced by suitable algorithms to complete the logical architecture (data-driven, knowledge-based, physical-based, hybrid...). An extensive review of the different algorithms that have been used to fulfill the different logical components used for the PHM'08 Challenge can be found in [19]. These publications have


> **Figure Description:**

This diagram illustrates a hierarchical process flow with a primary objective at the top and six supporting functional steps below it. The top-level box contains the text "Estimate the precise momment to trigger maintenance actions" (note the typo "momment" as it appears in the source). An upward-pointing arrow connects this central objective to a horizontal line that branches downward to six distinct, light-green rectangular boxes, each labeled with a small circular icon and a specific function identifier.

The six functional boxes, arranged from left to right, are labeled as follows: "Collect data (F1)", "Pre-process data (F2)", "Detect and identify faults (F3)", "Assess degradation (F4)", "Compute RUL (F5)", and "Make report (F6)". Each box is connected to the horizontal line above it by a vertical line, indicating that these six functions collectively support the primary objective of estimating the precise moment to trigger maintenance actions.



<div align="center">

Fig. 3. Functional decomposition for the predictive maintenance system

</div>


> **Figure Description:**

This diagram illustrates a functional workflow process consisting of six distinct stages, labeled F1 through F6, represented as light green rounded rectangles. The process begins at the top left with "Collect data (F1)," which outputs "Raw data" to the "Pre-process data (F2)" block located below it. The "Pre-process data (F2)" block has three output paths: one labeled "Pre-processed data" leading to the "Assess degradation (F4)" block at the top right, a second "Pre-processed data" path leading to the "Compute RUL (F5)" block in the middle right, and a third path leading to the "Detect and identify faults (F3)" block at the bottom left.

The "Detect and identify faults (F3)" block outputs a "Fault detected" signal to the "Assess degradation (F4)" block and a "Fault detection report" to the "Make report (F6)" block at the bottom right. The "Assess degradation (F4)" block outputs "Health state" to the "Compute RUL (F5)" block. The "Compute RUL (F5)" block then outputs a "RUL Report" to the "Make report (F6)" block. Finally, the "Make report (F6)" block has an output labeled "Health state report" extending to the right. Each functional block features small interface icons (triangles and squares) indicating input and output connection points, and each block is marked with a small circular "SF" icon. The flow of information is indicated by lines connecting these blocks, with labels describing the data being transferred between each stage.



<div align="center">

Fig. 4. Functional architecture for a predictive maintenance system concept

</div>

given special attention to functions F2, F3, F4 and F5 (see also Table V). It is important to point out that the suitable techniques rely on the available data sources and the predictive maintenance system scope. As can be seen in Table V, due to the nature of the original PHM'08 Challenge on which the jet engine example is based, data-driven techniques are more often found as potential solutions than other techniques. If the data sources include semantic knowledge (e.g. pilot feedback on witnessed engine behavior, or maintenance logs), one will see the set of suitable logical components evolve with other algorithms and potentially the architecture itself may evolve. When several solutions are identified to fulfill the functional components, trade-offs must be made; the architecture is assessed against performance indicators (the behavioral requirements). For the jet engine case study, the computational error on the remaining useful life was considered as the main performance indicator giving the best score to the statistical similarity based methods used by [21] at the time of the PHM'08 Challenge. These trade-off analyses as well as the physical architecture are out of the scope of this study.

## V. DISCUSSION

Generic architectures such as OSA-CBM [3] propose the functional blocks as starting points of a new predictive maintenance system. However, the new system may have a different scope that does not include all the proposed functional blocks or including new ones. Also, important information regarding the system performance, compatibility with existing systems and operability by the users may be missed when starting from a generic

architecture. When a new predictive maintenance system is developed, it must be tailored to its context, considering all the needs and desires of relevant stakeholders. A generic architecture could be considered as a pre-established baseline and as the INCOSE Handbook [16] states; this could be a trap of tailoring that may bring the new system development to fail. Every new system has its own particular requirements.

Newer architecture approaches, like the one presented by [4], mention the importance of considering the stakeholders' requirements to develop a new predictive maintenance systems. However, they do not present a methodology to gather and interpret the initial list of needs and desires so that a consistent list of prioritized requirements could be obtained. Also, their scope remains on generic architectures which share the same tailoring problems mentioned in the previous paragraph.

The proposed approach in this study has as advantage over other existing generic architectures on the importance given to the conceptual phase. By performing a systems engineering approach, important information is obtained from the stakeholders' needs and desires. In terms of functional blocks (functional requirements), the logical architecture, obtained with the proposed methodology may be similar to the mentioned generic architectures. Nevertheless, the behavioral, structural and experiential requirements give a better overview of what the stakeholders expect from the system.

Behavioral requirements will help to assess the performance of the new predictive maintenance system. These requirements would facilitate later the validation process once the system is developed. Structural and experiential requirements will help to design the external interfaces of the system with other related systems or/and the system users.

Besides, by performing the requirements prioritization, the ambiguity among the requirements decrease, allowing a better understanding of what the system shall, should or might do. This information is vital to tailor the architecture for a new predictive maintenance system.

Finally the proposed approach employs the ARCADIA methodology to develop the logical architecture. Unlike other generic approaches that only show the architecture as functional blocks using a modeling language (UML/SysML), it offers a whole methodology organized by layers to develop the architecture for every new system. The information obtained from the FBSE analysis and the prioritization may be easily integrated in the architecture using ARCADIA.


> **Figure Description:**

This diagram illustrates the interaction between three main components: Technical System databases, the Predictive Maintenance (PdM) System, and the PdM System User. The Technical System databases block contains a sub-component labeled "Store technical system data" which is associated with "Technical System Data." The PdM System block contains a central sub-component labeled "Estimate the precise moment to trigger maintenance actions." The PdM System User block contains a sub-component labeled "Operate PdM System" which is associated with "Launch PdM analysis."

The components are connected via various data flows. A solid green line connects "Technical System Data" to the PdM System, and another solid green line connects the PdM System back to "Technical System Data." A dashed orange line also connects the "Store technical system data" component to the PdM System. A solid green line connects the PdM System to the "Operate PdM System" component, and a dashed orange line connects the PdM System to the "Operate PdM System" component. Additionally, a solid green line connects the "Operate PdM System" component back to the PdM System. The diagram includes two specific data labels: "PdM report" (appearing twice, once near the PdM System and once near the PdM System User) and "Requested data" (near the PdM System).

The diagram uses specific symbols: a small square with a white interior and a green border represents an external interface to databases, while a small square with a blue interior and a green border represents a Human-Machine Interface. Each sub-component block contains a small circular icon labeled "SF." The overall layout is organized into three distinct vertical sections, with the PdM System acting as the central hub for data exchange between the databases and the user.



<div align="center">

Fig. 5. External interfaces of the system

</div>


> **Figure Description:**

This diagram illustrates the architecture of a Logical Predictive Maintenance System, organized into three main horizontal layers: Technical System databases at the top, the Logical Predictive Maintenance System in the middle, and the PdM System User at the bottom. The top layer contains a "Technical System databases" block with a sub-process labeled "Store technical system data (F0)". An "External interface to databases" connects this layer to the central system.

The central "Logical Predictive Maintenance System" layer is divided into two main columns. The left column contains three modules: "Data collecting module" with "Collect data (F1)", "Data preprocessing module" with "Pre-process data (F2)", and "Fault detection module" with "Detect and identify faults (F3)". These are connected by "Raw data interface" and "Pre-processed data interface" lines. The right column contains three modules: "Health assessment Module" with "Assess degradation (F4)", "Prognosis Module" with "Compute RUL (F5)", and "Reports Module" with "Make report (F6)". These are connected via "Diagnosis Interface", "Pre-processed data interface", "Fault detection interface", and "Prognosis interface" lines.

Data flow is represented by dashed orange lines with arrowheads indicating direction, connecting the various modules and interfaces. Solid blue lines represent structural or logical connections between the modules and the system boundaries. The bottom layer, "PdM System User," contains a single process block labeled "Operate PdM System (F7)" (implied by the sequence), which connects to the central system via a "Human-machine interface." The entire diagram uses a standardized notation for modules, interfaces, and process flows to map the functional decomposition of the predictive maintenance workflow.



<div align="center">

Fig. 6. Generic Logical Architecture for a Predictive maintenance off-line system.

</div>

<div align="center">

TABLE V. SUMMARY OF POTENTIAL TECHNIQUES FOR LOGICAL COMPONENTS

</div>

<table border="1"><tr><td>Logical component</td><td>Type of techniques</td><td>Examples</td></tr><tr><td>Data Pre-processing</td><td>Statistical tests</td><td>CovarianceNormalization</td></tr><tr><td>Fault identification</td><td>ClusteringClassification</td><td>Support VectorMachineNeural NetworksKalman filterBayesian Inference</td></tr><tr><td>DegradationAssessment</td><td>RegressionClassificationStochasticNon-parametric</td><td>Statistical similarityNeural NetworksMarkov Chains</td></tr><tr><td>Remaining Usefullife computation</td><td>RegressionClassificationNon-Parametric</td><td>Linear regressionNeural NetworksMarkov ChainsCase-based reasoning</td></tr></table>

## VI. CONCLUSION AND PERSPECTIVES OF FUTURE WORK

Predictive maintenance is having a lot of attention because of its potential benefits in terms of safety improvement and maintenance cost reduction. The realization of such systems remains complicated, despite existing generic architectures and standards. The lack of a

systematic approach to developing predictive maintenance systems remains one important shortcoming on.

A systems engineering approach to developing predictive maintenance systems is proposed to address the identified shortcoming. It starts by the analysis of the stakeholders' needs and desires, translating and classifying them into functional, behavioral, structural and experiential requirements. Then these requirements are prioritized with an ordinary scale method to rack the importance of each requirement for the predictive maintenance system. The identified and prioritized requirements are the basis for the architecture process.

The architecture development process begins with the functional analysis on the identified functional requirements. Functional decomposition is proposed for complexity management of the predictive maintenance system. The functional exchange between functions is studied to propose the functional architecture. The external actors and the interactions with the function are studied.

The logical architecture builds on top of the functional architecture. The functions are allocated to logical components and the external and internal interfaces are identified. The proposed logical architecture remains generic and it could evolve depending on the available data of technical system and the scope for the new predictive maintenance system.

Future research will be focused on the extension of the present approach on systems with heterogeneous types of available data and the methodologies to assess the different potential architectures to fulfill the predictive maintenance system.

## ACKNOWLEDGEMENTS

The authors want to acknowledge the "Tecnológico de Costa Rica" for funding this research.

The authors want to thank Prof. Bernard Grabot from the "École Nationale d'Ingénieurs de Tarbes" for his valuables comments on previous versions of this manuscript.

## REFERENCES

[1] J. J. Montero Jimenez and R. Vingerhoeds, "Enhancing operational fault diagnosis by assessing multiple operational modes," in Proceedings - International Conference in Modelling, Optimization and Simulation MOSIM 2018, 2018, pp. 237-244.

[2] G. P. Sullivan, R. Pugh, A. P. Melendez, and W. D. Hunt, "Operations & Maintenance Best Practices: A Guide to Achieving Operational Efficiency," U. S. Department of Energy, Federal energy management program. 2010.

[3] MIMOSA, "Open System Architecture for Condition-Based Maintenance (OSA-CBM)," http://www.mimosa.org/mimosa-osacbm/, 2001.

[4] R. Li, W. J. C. Verhagen, and R. Curran, "A functional architecture of prognostics and health management using a system engineering approach.." in Proceedings of the European Conference of the PHM Society, 2018, p. Vol 4 No 1.

[5] A. Saxena, I. Roychoudhury, and J. R. Celaya, "Requirements Specifications for Prognostics: An Overview," in Proceedings of AIAA Infotech@Aerospace 2010, 2010.

[6] J. S. Gero, "Design Prototypes: A knowledge Representation Schema for Design," AI Mag., vol. 11, no. 4, pp. 26-36, 1990.

[7] F. Brazier, P. van Langen, S. Lukosh, and R. A. Vingerhoeds, "Design, Engineering and Governance of Complex Systems," in Projects and People - Mastering success, H. L. M. Bakker and J. P. Kleynen, Eds. NAP Foundation Press, 2018, pp. 34-59.

[8] E. Crawley, B. Cameron, and D. Selva, System Architecture: Strategy and Product Development for Complex Systems. Pearson Higher Education, Inc., 2015.

[9] P. Roques, Systems Architecture Modeling with the Arcadia Method 1st Edition. ISTE Press, 2018.

[10] N. Zerhouni, V. Atamuradov, K. Medjaher, P. Dersin, and B. Lamoureux, "Prognostics and Health Management for Maintenance Practitioners-Review, Implementation and Tools Evaluation," Artic. Int. J. Progn. Heal. Manag., vol. 8, no. 60, p. 31, 2017.

[11] B. Schmidt and L. Wang, "Predictive Maintenance: Literature review and future trends," Conf. Proc. 25th Int. Conf. Flex. Autom. Intell. Manuf., vol. 1, pp. 232-239, 2015.

[12] N. Sakib and T. Wuest, "Challenges and Opportunities of Condition-based Predictive Maintenance: a Review," in 6th CIRP Global Web Conference: "Envisaging the future manufacturing, design, technologies, and systems in innovation era," 2018, pp. 267-272.

[13] Y. Lei, N. Li, L. Guo, N. Li, T. Yan, and J. Lin, "Machinery health prognostics: A systematic review from data acquisition to RUL prediction," Mech. Syst. Signal Process., vol. 104, pp. 799-834, 2018.

[14] R. A. Vingerhoeds, P. Janssens, B. D. Netten, and M. Aznar Fernández-Montesinos, "Enhancing off-line and on-line condition monitoring and fault diagnosis," Control Eng. Pract., vol. 3, no. 11, pp. 1515-1528, 1995.

[15] International Organization for Standardization (ISO), ISO 13374-1:2003 Condition monitoring and diagnostics of machines Data processing, communication and presentation Part 1: General guidelines. 2003.

[16] INCOSE, Systems Engineering Handbook. A guide for system life cycle processes and activities. Fourth Edition. Wiley, 2015.

[17] P. Achimugu, A. Selamat, R. Ibrahim, and M. N. R. Mahrin, "A systematic literature review of software requirements prioritization research," Inf. Softw. Technol., 2014.

[18] A. Saxena, K. Goebel, D. Simon, and N. Eklund, "Damage propagation modeling for aircraft engine run-to-failure simulation," in 2008 International Conference on Prognostics and Health Management, PHM 2008, 2008.

[19] E. . Ramasso and A. . Saxena, "Review and analysis of algorithmic approaches developed for prognostics on CMAPSS dataset," PHM 2014 - Proc. Annu. Conf. Progn. Heal. Manag. Soc. 2014, 2014.

[20] G. W. Vogl, B. a Weiss, and M. A. Donmez, "Standards for Prognostics and Health Management (PHM) Techniques within Manufacturing Operations," Annu. Conf. Progn. Heal. Manag. Soc., 2014.

[21] T. Wang, J. Yu, D. Siegel, and J. Lee, "A similarity-based prognostics approach for remaining useful life estimation of engineered systems," in 2008 International Conference on Prognostics and Health Management, PHM 2008, 2008.

## 3.3 Lessons learnt

Once the initial needs and desires for a new predictive maintenance system have been gathered, they need to be formalized into requirements. There exist several methods to elicit requirements. One of them is the Functional, Behavioral, Structural and Experiential analysis (FBSE) [Bra+18], which is an extension of the FBS analysis introduced by John Gero in [Ger90] and [GK07]. This method classifies the requirements into four main groups:

- Functional requirements: gather all intended functions of the system. These requirements derive from the purpose of the system, they answer the "why?" the system is being created.

- Behavioral requirements: are related to system performance. Behavioral requirements answer the "how?" and the "when?" of the development of the new system.

- The structural requirements: refer to the constraints imposed for the system development. Structural requirements are those related to "what" is fixed or expected previous to the concept design. For example, authorities' constraints, connectivity with the existing system and available technologies.

- Experience requirements: are related to feelings, emotions and perceptions created by the system to the users. These are the most difficult requirements to elicit as some of them can be subjective and thus difficult to validate. Experiential requirements could be translated into more specific requirements that are clustered into the three first groups. The benefit of adding this fourth group of requirements is to avoid ignoring important needs from human factors.

The FBSE analysis is a consistent methodology for a systems architect as it allows the direct identification of all expected functions from the system. The functional requirements are the starting point to explore the solution space of a new system. These functions can be decomposed into sub-functions depending on the complexity of the functions. Decomposition of functions is a well-known process to manage complexity. Crawley et al. [CCS15] explain that two levels of decomposition are enough to describe a system; if more elements are needed for a function, it is advisable to treat it as a subsystem and perform the system engineering process separately. The architect organizes the functions and sub-functions making links among them using functional interfaces. The organization of the functions, sub-functions and functional interfaces is known as the functional architecture of a system [INC15].

After defining the functional architecture, the architect can start to propose logical components to fulfil each function and each interface. This is known as the logical architecture of the system. The logical architecture aims at defining a much detail as possible of the system without narrowing down the solution space to a specific technology, programming language or environment. The objective of the logical architecture is to present how the system will work to fulfil the expectations. Once the logical architecture is complete, an exploration of the solution space starts to identify suitable technologies, programming languages, methods, materials to fulfil the logical components.

The selection of these components is done at the software, hardware and structural levels of the system. This is known as physical architecture and states details of how the system will be developed and built. If several possible solutions to fulfil the logical architecture are identified, the architect must assess them based on the behavioural and structural requirements obtained from the FBSE analysis. The union of the functional architecture, logical architecture and physical architecture constitutes the complete system architecture.


> **Figure Description:**

This flowchart illustrates a sequential process for developing a predictive maintenance system, consisting of six primary stages represented by yellow rounded rectangles, each marked with an "OR" icon. The process begins at the top with "Gather needs and desires for a new predictive maintenance system," which flows downward to "Formalize stakeholder requirements," then to "Classify and prioritize requirements," followed by "Perform Functional Analysis," "Develop Logical Architecture," and finally "Develop physical architecture" at the bottom.

Between each sequential step, there is a connector icon labeled with the output of the preceding stage: "Needs and desires for the new predictive maintenance system" follows the first step, "Formal stakeholder requirements" follows the second, "Functional requirements" follows the third, "Functional Architecture" follows the fourth, and "Logical Architecture" follows the fifth. Additionally, a feedback or supplementary loop originates from the right side of the "Classify and prioritize requirements" stage and connects to the final "Develop physical architecture" stage; this line is labeled with "Behavioral, structural and experiential requirements" accompanied by a connector icon.



<div align="center">

Figure 3.1: An approach to developing a system architecture in the concept stage

</div>

Recalling the refined research proposed at the end of Chapter 2:

1. How to address the design of predictive maintenance systems?

2. How to suggest a suitable approach for a predictive maintenance system solution?

3. How to select a suitable model or combination of models given a new predictive maintenance problem to solve?

4. How can a designer benefit from the experience of existing systems to develop new predictive maintenance solutions?

This chapter proposes a systematic approach to address the concept stage of predictive maintenance systems to provide an answer to the first refined research question. The different steps from the gathering of the initial needs and desires from the stakeholder until the logical architecture definition have been covered and different methods have been proposed to address them. However, the rest of the refined research questions are still to be answered. In predictive maintenance, the solution space is vast and complex as was shown in Chapter 2. There are no specific rules an architect can follow to select the suitable models and approaches to solve new predictive maintenance problems. In this research, an hypothesis to overcome this problem is proposed: the implementation of a Decision Support System (DSS) based on Case-Based Reasoning (CBR) and supported by ontologies could help the architect select suitable components based on past experiences extracted from successful implementations of predictive maintenance systems. The following three chapters are dedicated to the development of the DSS and how it fits in the proposed framework of predictive maintenance systems design. Chapter 4 and Chapter 5 explain the building blocks of the proposed framework: ontologies and CBR. Chapter 6 is then dedicated to explaining their integration in the DSS.

<div align="center">

# Ontology development to support Case-based reasoning systems

</div>

“Your understanding of what you read and hear is, to a very large degree, determined by your vocabulary, so improve your vocabulary daily.”

Zig Ziglar

Content

4.1 Building the framework vocabulary 43

4.2 Ontology 44

4.3 Ontology model for Maintenance Strategies selection and assessment (Article 3) 46

4.4 Terminology framework for predictive maintenance components selection 74

4.4.1 OPMAD scope 74

4.4.2 OPMAD terms and relations 75

4.4.3 OPMAD instantiation 79

4.5 Lessons learnt 79

## 4.1 Building the framework vocabulary

Recalling the research statement proposed at the end of the Chapter 3, a Decision Support System (DSS) is proposed to suggest suitable components to fulfil the generic components of the logical architecture. The DSS is built upon two main technologies: Case-Based Reasoning (CBR) and ontologies. CBR is a reasoning paradigm that aims to solve new problems based on the experiences of similar problems solved in the past. CBR is addressed in Chapter 5, but a brief introduction is necessary to understand the role that plays the ontologies in the DSS developed in the current research. CBR systems are developed on a vocabulary framework [Alt+12]; [Sán+12]. This vocabulary is necessary to give structure to the stored cases of solved problems in a case base, to the similarity measures that compare the new problem with those in the case base, and to the necessary knowledge to adapt the retrieved solution for the new problem (see Figure 4.1. In the proposed framework, an ontology is chosen to serve as terminology framework. An ontology model provides the terms, definitions, and relations among terms that are used to build the case structure, the similarities, and adaptation knowledge in the DSS. This chapter is dedicated to the theoretical background and the development of the ontology model for the proposed DSS.

Section 4.2 provides a brief introduction to ontologies. Originally, an ontology was developed to study predictive maintenance terminology within the maintenance strategies domain. This was called the Ontology


> **Figure Description:**

The image is a conceptual diagram illustrating the components of a system, represented by a large circle containing a smaller, dashed-line circle divided into three equal sectors. The outer ring, which encompasses the entire diagram, is labeled "Vocabulary" at the top, bottom-left, and bottom-right positions. Inside the inner dashed circle, the three sectors are labeled "Case base" at the top, "Similarity measures" at the bottom-left, and "Adaptation knowledge" at the bottom-right. 

The diagram includes bidirectional arrows indicating relationships between these components. A double-headed arrow connects "Similarity measures" and "Adaptation knowledge" horizontally. Additionally, two other double-headed arrows originate from the center of the diagram, pointing outward toward the "Case base" sector and the "Similarity measures" sector, and toward the "Case base" sector and the "Adaptation knowledge" sector, respectively. The background of the inner circle is white, while the outer ring has a light gray fill.



<div align="center">

Figure 4.1: Case-Based Reasoning based on a vocabulary framework [Alt+12]

</div>

model for Maintenance strategy Selection and Assessment (OMSSA). In the later stages of the research, the benefits of ontologies as complementary knowledge models for CBR systems were recognized. To support the CBR system for predictive maintenance models recommendation, an ontology was created taking OMSSA as reference. Section 4.3 is dedicated to explaining the development of OMSSA, the terms, their relations and the methodology followed for its creation. It also includes the verification of the ontology using a simple case study. OMSSA has been consolidated in an article that has been accepted for publication in the Journal of Intelligent Manufacturing. In Section 4.4, a novel the ontology model to support the CBR system for predictive maintenance component selection is developed. This second ontology model received the name of Ontology for Predictive Maintenance Architecture and Design (OPMAD) and the description of its development includes the bridges for its integration with CBR in the DSS. The integration of ontologies and CBR is further addressed in Chapter 6 where the justification and benefits of their combination are also discussed.

## 4.2 Ontology

The word ontology finds its roots in philosophy where it can be defined as "a particular theory of being or existence" [RN12]. From an ontological point of view, all things are concepts whether concrete or abstract. In etymology, ontology is related to epistemology. While ontology is oriented to define the reality of things, "what exists in the world"; epistemology refers to the human perception of things through their senses, "what a person believes about the ontology". With the emergence of computer and information science, the word ontology has been adopted and its meaning has evolved. It conserves its roots in which all things are considered concepts but the scope and applications of the word is oriented to knowledge representation. To avoid ambiguity, all the content in this manuscript with regard to ontology (after this point) is seen in the light of the information science perspective.

In information science, an ontology is a formal explicit description of concepts in a domain of discourse, properties of each concept describing its features, attributes, and restrictions [NM01]. One of the most common goals in developing ontologies is "sharing a common understanding of the structure of information among people and software agents” [Gru93]; [Mus92]. This means that the vocabulary used by people in a specific domain of knowledge is enabled to be "machine-readable". All concepts in an ontology are represented by classes that are linked by properties (also called relations). Ontologies are defined using formal languages. One of the most recognized is the Web Ontology Language in its second version (OWL2) which is supported by the World Wide Web Consortium (W3C) [Wor12]. But also it is normal to graphically represent ontologies with graphs whose nodes are the ontology classes and the edges are the ontology relations among the classes. By only considering the graphical representation, ontologies can

be confused with semantic networks or frame-based representations. Frame-based representations can be seen as an extension of semantic networks and ontologies can also be seen as an extension of frame-based representations. Semantic nets could be used to represent anything (not just word concepts) and can be seen in many ways equivalent to generic graph representations [Hoe09]. The main contribution of the frame-based view was that it fixed a knowledge representation perspective. The frame proposal fixes the perspective on descriptions of situations in general, and objects and processes in a particular situation. However, semantic networks and frame-based models lack of formal logic-based semantics [HLP08]. Ontologies are based on Description Logics (DL) which provide logical formalism to overcome the deficiency in logic-based semantics of other knowledge representation methods [DMB16]; [HLP08].

The W3C supports the creation and use of ontologies because of their importance for the semantic web. The semantic web is an extension of the current web, where the information is well-structured and defined so that it can be processed by a machine [NB18]. The W3C recommends the use of the OWL2 language for the semantic web ontologies [MO+14]. Ontologies in OWL2 are compatible with information written in the Resource Description Framework (RDF). In RDF, information is represented in semantic triples: subject-predicate-object. OWL2 ontologies are primarily exchanged as RDF documents. This means that all knowledge stored in an ontology can be also represented in semantic triples. Two related classes will represent the subject and the object of the triple, while the relation between the two classes represents the predicate of the triple. RDF structure provides a flexible means to model, store and manage information; other methods requiring variable-length fields would require a more complicated implementation. Figure 4.2 presents the RDF structure of subject-predicate-object as well as the example of the representation of two sentences in RDF: e.g. "the machine has failure mode" and "failure mode has failure cause". For both sentences, the predicate (the relation of ownership between the subject and the object) is "has". For the first sentence, the subject is "the machine" and the object is "failure mode". For the second sentence "failure mode" is now the subject while the object is "failure cause". This shows that the concepts in RDF (classes in ontologies) can be subjects or objects depending on the predicate.


> **Figure Description:**

The image is a diagram illustrating a semantic relationship structure. At the top, there is a schematic representation consisting of two rounded rectangles labeled "Subject" on the left and "Object" on the right, connected by a horizontal arrow pointing from left to right, with the word "Predicate" written above the arrow. Below this schematic, two rows of text demonstrate specific instances of this relationship. The first row reads "The machine" on the left, "has" in italics in the center, and "Failure Mode" on the right. The second row reads "Failure Mode" on the left, "has" in italics in the center, and "Failure cause" on the right.



<div align="center">

Figure 4.2: Semantic triple structure with examples

</div>

Ontologies help to make the knowledge explicit, defining the relations among different terms. They allow a deep analysis on domain knowledge, helping to identify semantic rules among the terms. These rules can be used to develop algorithms that perform automated inferences based on domain knowledge. Taking the example of Figure 4.2, as "the machine" has a "failure mode" and the "failure mode" has a "failure cause", one can infer that "the machine" has a "failure cause".

Ontologies enable the reuse of domain knowledge. For example, an ontology can represent all the terms related to time and another can represent all terms related to geographical locations; both ontologies can be reused to model the knowledge of another domain such as "sports events", which usually includes terms from time and geographical locations. The time and geographical locations ontologies can be also used to model the knowledge of "university courses". Even when "sports events" and "university courses" are different domains of knowledge, the definition of the terms related to time and the geographical location remains the same. Recent trends in ontology development are oriented towards the use of structured and standardized methodologies that include the use of generic ontologies (domain-neutral) such as BFO [Int20b] as a basis to build domain-specific ontologies or other reference ontologies. This boosts the reuse of knowledge already modelled in ontologies.

4. 3 Ontology model for Maintenance Strategies selection and assessment (Article 3)

<div align="center">

# An Ontology Model for Maintenance Strategy Selection and Assessment

</div>

Juan José Montero Jimenez $ ^{* }^{1,2} $ , Rob Vingerhoeds $ ^{1} $ , Bernard Grabot $ ^{3} $ , Sébastien Schwartz $ ^{1} $

* Corresponding author

$ ^{1} $ ISAE-SUPAERO, Université de Toulouse, 10 Avenue Edouard Belin, 31400 Toulouse, France

$ ^{2} $ TEC-Tecnológico de Costa Rica, Calle 15, Avenida 14., 1 km Sur de la Basílica de los Ángeles, Provincia de Cartago, Cartago, 30101, Costa Rica

$ ^{3} $ ENIT- INP Toulouse, 47, avenue d'Azereix - BP 1629 - 65016 Tarbes, France

## Abstract

Within maintenance management activities, engineers need to select maintenance strategies so to carry out the technical maintenance actions. A single equipment is composed of several components with different failure modes. There should be a maintenance strategy for each of them; while some of the components can be run-to-failure applying corrective maintenance, some others cannot afford a failure, and preventive or predictive strategies should be implemented. Selecting and assessing maintenance strategies is a complex task for which information from many sources should be retrieved. Information from a Failure Mode, Effects and Criticality Analysis (FMECA), a cost-benefit-risk analysis, Computational Maintenance Management Systems (CMMS), is often used by engineers to select and assess maintenance strategies. A selected strategy is often not evaluated over time to check its effectiveness. The strategy may need adjustments or substituted by a more efficient one, for example, a condition-based strategy substituting a time-based one. To facilitate maintenance strategies selection and assessment, the current study proposes an Ontology model for Maintenance Strategy Selection and Assessment (OMSSA). OMSSA serves as a formal terminology framework in maintenance strategies that can be used to develop smart computational agents that can help in the decision-making process for selecting and assessing maintenance strategies. To facilitate its future reuse and integration with other ontologies in the industrial domain, OMSSA builds following the state-of-the-art in ontology development by using a top-level domain-neutral ontology, the Basic Formal Ontology (BFO).

Keywords: Maintenance strategy, ontology, knowledge base, knowledge reuse.

## Introduction

Maintenance, as defined by the standard BS EN 13306 (European Committee for Standardization 2017), is the "combination of all technical, administrative and management activities throughout the life cycle of an asset in order to maintain or restore it to the state where it can perform the intended functions." Maintenance exists since the first humans substituted the broken parts of their first tools, and it has evolved along with the increment of the complexity of

<div align="center">

# This article has been published in the Journal of Intelligent Manufacturing

</div>

artificial assets. Today it plays a vital role in keeping technical systems in optimal operating conditions.

Within maintenance management activities of modern industrial systems, engineers need to select maintenance strategies so to carry out the technical maintenance actions. These maintenance strategies are directly linked to triggering events such as a failure (corrective maintenance), a safe operating time interval (preventive maintenance), or an abnormal symptom (predictive maintenance) that launches a maintenance action. Selecting the right maintenance strategy can be a complex task. It depends on several factors, such as the detrimental effects of an unforeseen failure, the maintenance costs, the maintenance personnel skills, and the access to technological tools to carry out the most advanced maintenance actions (Emovon et al. 2018). Information from different sources should be assessed to perform the right maintenance strategy selection, such as Failure Mode, Effects and Criticality Analysis (FMECA), a cost-benefit-risk analysis, Computational Maintenance Management Systems (CMMS). Besides, a selected strategy is often not assessed over time to confirm its effectiveness or suitability. Smart Decision Support Systems (DSS) can be developed to help engineers in such complex tasks. These smart DSS can be developed on the basis of a well-structured vocabulary framework. The definition of concepts, attributes, and relations among concepts can help to structure the knowledge around maintenance strategies, allowing their better selection and assessment.

For this aim, the current study proposes an Ontology model for Maintenance Strategy Selection and Assessment (OMSSA). From the practical point of view, the objective of OMSSA is to provide a vocabulary structure that can be used for the development of smart agents such as DSS to help engineers in the selection, assessment, and even in the implementation of maintenance strategies. From the scientific point of view, the OMSSA contribution can be seen as a structured meta-knowledge representation in the domain of maintenance strategies.

Ontologies are formal, explicit descriptions of concepts in a domain of discourse, the properties of each concept describing its features, attributes, and restrictions (Noy and McGuinness 2001). One of the most common goals in developing ontologies is "sharing a common understanding of the structure information among people and software agents" (Gruber 1993; Musen 1992). However, there are also several other motivations to create ontology models, such as enabling reuse and analysis of domain knowledge or making domain assumptions explicit. Ontologies are powerful tools for knowledge representation. The described concepts are represented by classes, while the properties represent the relations between the terms. An ontology with individual instances for its classes constitutes an ontology-based knowledge base (Noy and McGuinness 2001; Qin et al. 2016). This knowledge base can be used for several purposes in the artificial intelligence field. For example, it can provide a formal terminology framework allowing to perform reasoning based on semantic rules.

OMSSA provides a formal terminology framework in maintenance strategy selection and assessment, considering not only traditional approaches but also the current trends towards the use of advanced diagnosis and prognosis tools to trigger maintenance actions. Its development is part of a bigger research project in knowledge reuse for maintenance systems. For the OMSSA, the taxonomy of corrective maintenance, preventive maintenance, and predictive maintenance has been selected to classify the maintenance strategies. These three terms have been widely used in

## This article has been published in the Journal of Intelligent Manufacturing

the research community and across the industry (Emovon et al. 2018; Kothamasu et al. 2006; Montero Jimenez et al. 2020). Even when a good combination of the three strategies is vital to keep a technical system in nominal operation (Montero Jimenez and Vingerhoeds 2018), there is a trend to implement proactive techniques to avoid unforeseen failures that can affect a technical system operation. For OMSSA, special attention is given to the current trends in maintenance management towards the implementation of predictive maintenance systems to reach a safer, more reliable, and more efficient operation of technological systems.

The rest of the paper is organized as follows: "Sect. Maintenance strategies" introduces the topic of maintenance strategies, the selected taxonomy for maintenance strategies used in OMSSA, and the maturity model of the evolution of the maintenance strategies. "Sect. Ontology engineering" is dedicated to ontology engineering and the methodology used to develop OMSSA, based on the alignment to a top-level domain-neutral ontology to facilitate its future reuse. "Sect. Ontologies in maintenance" summarizes the related studies on ontologies in the maintenance domain and analyses their limitations for addressing the current trends of maintenance strategies. The requirements and vocabulary sources for OMSSA are introduced. "Sect. Ontology for Maintenance Strategy Selection and Assessment (OMSSA)" explains the most important terms and relations for maintenance strategy management using a graphical representation for different parts of the model. "Sect. Evaluation and discussion" is dedicated to the verification and validation of the ontological model, as well as its illustration on a case study. "Sect. Conclusion and future work perspectives" concludes this paper by presenting the final remarks and perspective for future work.

## Maintenance strategies

Maintenance strategies are part of maintenance management. They aim to establish how and when maintenance action should be performed to restore or maintain a specific artifact, component, or system into its nominal operational state. Maintenance strategies are often established by experts who know the different failures that a system can encounter, taking into consideration the likelihood and the detrimental impacts (human lives, environmental damage, costs, production losses) of each failure occurrence. One classic approach to establish maintenance strategies is the Failure Modes, Effects, and Criticality Analysis (FMECA) (International Electrotechnical Commission (IEC) 2018), in which a maintenance strategy is assigned to each failure mode of each component of an equipment.

Maintenance strategies can be divided into three groups depending on the triggering event of the maintenance action: corrective maintenance, preventive maintenance, and predictive maintenance:

- Corrective maintenance is triggered by a failure. However, there is an important difference between a run-to-failure strategy and a maintenance action produced by an unexpected failure. The second one cannot be considered as a strategy as it was not planned (Hodkiewicz et al. 2021). It is important not to confuse a corrective strategy with an undesired failure. The undesired failure is actually a sign that preventive or predictive strategies assigned to the failed component and should be re-evaluated.

## This article has been published in the Journal of Intelligent Manufacturing

- Preventive maintenance actions are triggered by fixed time recommendations coming from safety operating time intervals or preventive scheduled stops of an item. Classic approaches such as Reliability Centered Maintenance (RCM) provide a set of strategies based on preventive action such as failure finding, fixed time restoration and fixed time replacement (Moubray 1997).

- Predictive maintenance strategies propose an alternative to preventive actions. They aim at triggering the maintenance actions based on the condition of a machine. Predictive maintenance is carried out by specialized models or tools that help maintenance engineers for an intelligence-based decision-making process to trigger maintenance actions. Classic approaches such as RCM summarize these strategies as "condition-based," providing a limited insight on how these strategies are actually developed. Recent trends in maintenance show that predictive maintenance strategies can have three types of triggering events: early fault detection, health/degradation threshold overshoot, and future failure forecasting. These three triggering events could affect the scheduling of maintenance actions based on the condition of the item. Anticipating failures allows the optimization of maintenance schedules as the maintenance actions will be triggered accurately when needed (Montero Jimenez et al. 2020). Condition monitoring quality is an important issue for predictive maintenance strategies (Castaño et al. 2020). It is important to ensure accurate monitoring so that the recorded data can be used to train the specialized models that carry out the diagnosis and prognosis tasks.

From corrective maintenance to predictive maintenance, there is an evolution in the implementation of maintenance strategies, from the simplest ones to the most advanced. This evolution can be represented by a maturity model. The more advanced the strategy, the more benefits it could bring, but also the higher the implementation cost and the complexity. The final step in this maturity model is the strategies based on prognostics which remain a challenge for their implementation and are often included in the Prognostics and Health Management (PHM) discipline (Montero Jimenez et al. 2020). Fig. 1 shows the proposed maturity model for maintenance strategies considering the triggering event.


> **Figure Description:**

This diagram illustrates a progression of maintenance strategies arranged along an upward-sloping trend, where the vertical axis represents "Benefits" and the horizontal axis represents the progression of maintenance sophistication. The diagram consists of five rounded rectangular boxes arranged in a step-like, ascending pattern from left to right.

The first box on the bottom left is labeled "Corrective maintenance. After failure." The second box, positioned slightly higher and to the right, is labeled "Preventive maintenance. Fixed time event." The third box, higher still, is labeled "Predictive maintenance level 1. Early fault detection." The fourth box is labeled "Predictive maintenance level 2. Health threshold assessment (CBM)." The final, highest box on the right is labeled "Predictive maintenance level 3. Failure forecasting (PHM)." An arrow extends from the top right of the final box, indicating continued progression.



<div align="center">

Cost and qualification for implementation

</div>

<div align="center">

# This article has been published in the Journal of Intelligent Manufacturing

</div>

Fig. 1. Maintenance strategies maturity model

## Ontology Engineering

Several specific methodologies exist for ontology development that are not simply interchangeable: two different methodologies will not lead to the same final ontology. (Keet 2018) presents an extensive comparison of the different methodologies and how they should be selected depending on the objectives of the ontology. As OMSSA aims at formalizing the knowledge of a specific domain, the selected methodology is a variant of "Ontology development 101" (Noy and McGuinness 2001). The main reason why this methodology was selected is because of its capability and simplicity for building new ontologies by reusing terms from top-level ontologies. Having a top-level ontology improves the interoperability of ontologies and thus facilitates their future reuse. For OMSSA, the selected top-level ontology is the Basic Formal Ontology (BFO) (Arp et al. 2016; International Organization for Standardization (ISO) 2020a, 2020b). To facilitate the alignment to BFO, some mid-level reference ontologies can be used. These ontologies provide a set of terms and relations that are common among different but related knowledge domains. For OMSSA, the alignment to BFO is performed using the Relation Ontology (RO) and the Common Core Ontologies (CCO) as these ontologies provide a good set of terms and relations to model ontologies in the industrial domain.

This section explains the different "blocks" used for OMSSA development. OMSSA was developed using the current version of the platform Protégé (Stanford University 2020). This platform supports the latest specifications of the OWL 2 set by the World Wide Web Consortium.

## Ontology development 101

"Ontology Development 101" is a seven-step iterative methodology used to create ontologies (Noy and McGuinness 2001). Each step is explained hereafter:

1. Determine the scope of the ontology, meaning the main goal for which the terminology framework will be created. At this point, important aspects such as the ontology domain or the intended use of the ontology must be defined. To do so, a set of "competency questions" can be proposed to delimitate the ontology scope. Competency questions are a set of questions that an ontology-based knowledge base should be able to answer, emulating the way an expert would answer (Grüninger et al. 1995a).

2. Consider reusing existing ontologies. This step is vital to ensure the alignment of the new ontology with related ontologies that already exist. Some terms and relations can be retrieved from these existing ontologies. For OMSSA, some ontologies are being completely reused (imported) as upper-level ontologies (BFO, RO, CCO), and some important terms and relations linked to OMSSA scope have been extracted from other domain-specific ontologies (see Sect. Ontology engineering).

3. Enumerate terms. Here, the main terms related to the selected scope are listed. A classification of these terms is not needed at this step, as it will be performed in the following steps.

4. Define the classes. The first classification of the enumerated terms is performed to define the classes of the new ontology. Classes are the means to represent the different entities in ontologies. They must be written in the singular form.

## This article has been published in the Journal of Intelligent Manufacturing

5. Define properties of classes. Here, the internal structure of concepts is described. The properties of the classes represent the links among the classes. Verbs in third-person conjugation are often used to represent these properties.

6. Define constraints. The classes and properties among these classes can have several constraints, such as for example value type, allowed values, and cardinality.

7. Create instances. This last step aims at instantiating the new ontology. Once the ontology has individual instances for its classes, it becomes an ontology-based knowledge base. So, for many reference ontologies, the instantiation does not take place as they are intended to be as generic as possible. Sometimes, this instantiation is done for validation purposes, and later the ontology is published without the specific instances.

These steps can be iterative. Often, missing terms are identified in later steps of ontology development. This leads to the iteration of previous steps to make sure that all classes, properties, and constraints are properly defined for the new identified terms.

## BFO as a top-level ontology

BFO is a top-level ontology that serves as starting point for the development of other reference ontologies and/or domain-specific ontologies (Arp et al. 2016; International Organization for Standardization (ISO) 2020b). It serves as a generic framework that offers a set of domain-neutral classes in which more specific terms can be clustered. Using a top-level ontology is advisable when developing domain-specific ontologies as it facilitates the interoperability with other related ontologies that use the same terms and relations (International Organization for Standardization (ISO) 2020a, 2020b). BFO has been successfully used by the Open Biological and Biomedical Ontology (OBO) Foundry (Arp et al. 2016). BFO is also used along with the Descriptive Ontology for Linguistic and Cognitive Engineering (DOLCE) by the Industrial Ontologies Foundry (IOF) to develop proof-of-concept ontologies (Karray et al. 2019; Sanfilippo et al. 2019). The future reuse and alignment of OMSSA to IOF ontologies motivated the selection of BFO as top-level ontology.

BFO starts from the most basic class entity, divided into two main subclasses: continuant and occurrent (Arp et al. 2016; International Organization for Standardization ISO) 2020a, 2020b; Rodrigues and Abel 2019). Continuants refer to entities that continue to exist through time, for example objects, functions, and qualities. Occurrents refer to entities that occur, meaning that they are spread not only in space but also in time; for example, processes belong to this class. Based on these two main entities, BFO proposes a set of domain-neutral classes that can be used to model any domain-specific ontology. Fig. 2 shows the BFO 2.0 structure, which is a stable version since 2015 (Arp et al. 2016). In the current study, continuants are represented in blue and occurrents in green.

## This article has been published in the Journal of Intelligent Manufacturing


> **Figure Description:**

This diagram is a hierarchical taxonomy tree originating from a top-level box labeled "entity." From "entity," the tree branches into two primary categories: "continuant" (blue boxes) and "occurrent" (green boxes). The "continuant" branch further divides into "specifically dependent continuant," "generally dependent continuant," and "independent continuant." The "specifically dependent continuant" branch leads to "realizable entity" and "quality." "Realizable entity" further branches into "disposition" (which leads to "function") and "role." "Quality" is linked to "relational quality."

The "independent continuant" branch splits into "inmaterial entity" and "material entity." "Inmaterial entity" leads to "site," "continuant fiat boundary," and "spatial region." "Continuant fiat boundary" further branches into "two-dimensional continuant fiat boundary," "one-dimensional continuant fiat boundary," and "zero-dimensional continuant fiat boundary." "Spatial region" branches into "three-dimensional spatial region," "two-dimensional spatial region," "one-dimensional spatial region," and "zero-dimensional spatial region." "Material entity" branches into "object," "object aggregate," and "fiat object part."

The "occurrent" branch splits into "temporal region," "spatiotemporal region," "process boundary," and "process." "Temporal region" further branches into "one-dimensional temporal region" and "zero-dimensional temporal region." "Process" branches into "history" and "process profile." All relationships are indicated by arrows pointing upward toward parent categories, representing a hierarchical classification structure where each box is a sub-type of the box above it.



<div align="center">

Fig. 2. Basic Formal Ontology structure, based on (International Organization for Standardization (ISO) 2020b).

</div>

Building an ontology using a top-level ontology such as BFO could be complicated because all new domain-specific classes must be clustered under domain-neutral classes. These upper-level classes have their own properties and constraints that are inherited by the domain-specific classes. Some consistency issues might arise when creating the relations at the lower levels of the ontology. Nevertheless, having a top-level domain-neutral ontology promotes more important data interoperability and thus enables ontology reuse (International Organization for Standardization (ISO) 2020b).

## Reuse of Relation Ontology and Common Core Ontologies

Relation Ontology (RO) (Foundry 2020) and Common Core Ontologies (CCO) (Rudnicki 2020a, 2020b) are mid-level domain-neutral BFO-compliant ontologies. RO provides domain-neutral relations among different classes, from which more specific relations can be derived in a specific domain. CCO is composed of eleven ontologies that have as objective the representation and taxonomy integration of generic classes and relations across all domains of interest. Within CCO, the following ontologies are found: Information Entity Ontology, Agent Ontology, Quality Ontology, Event Ontology, Artifact Ontology, Geospatial Ontology, Time Ontology, Units of Measure Ontology, Currency Unit Ontology, Extended Relation Ontology and Modal Relation Ontology (Rudnicki 2020a). The import structure of CCO in its version 1.3 is presented in Fig. 3.

## This article has been published in the Journal of Intelligent Manufacturing


> **Figure Description:**

This diagram illustrates a hierarchical structure of ontologies, beginning at the top with the "Basic Formal Ontology" in a grey box. A downward arrow connects this to the "Extended Relation Ontology." From the "Extended Relation Ontology," two downward arrows branch out to the "Geospatial Ontology" on the left and the "Time Ontology" on the right. A separate, unconnected box labeled "Modal Relation Ontology" sits to the right of these.

Below the "Geospatial Ontology" and "Time Ontology," a single downward arrow leads to the "Information Entity Ontology." From the "Information Entity Ontology," a series of downward arrows branch out to six distinct categories: "Agent Ontology," "Artifact Ontology" (which has a downward arrow pointing to "Facility Ontology"), "Currency Unit Ontology," "Event Ontology," "Quality Ontology," and "Units of Measure Ontology."

At the bottom of the diagram, upward-pointing arrows from the "Agent Ontology," "Artifact Ontology," "Currency Unit Ontology," "Event Ontology," "Quality Ontology," and "Units of Measure Ontology" converge into a single box labeled "All Core Ontology." To the right of this, there is a separate, unconnected box labeled "Obsolete Terms." All boxes are rectangular with rounded corners, and the connections are represented by straight lines with arrows indicating the direction of the hierarchy.



<div align="center">

Fig. 3. Import structure of CCO version 1.3 (Rudnicki 2020a)

</div>

In maintenance management, many concepts can be clustered in the CCO class Information_Content_Entity. This class includes pieces of information used to describe, designate, or direct other entities. For maintenance, the concepts under this CCO class are used to describe the maintainable items attributes, condition data, costs, models, specifications, among others. To model all these information entities and the phenomena they describe in real life, OMSSA directly imports the Information Entity Ontology, the Artifact Ontology, and the Event Ontology from CCO. Due to the import structure of CCO, the Time Ontology, Geospatial Ontology, and the Extended Relation Ontology are indirectly imported from CCO, and consequently, RO and BFO are also imported.

It is important to mention that by importing the Information Entity Ontology, the "aboutness" paradigm to represent data properties is adopted for OMSSA. In contrast to UML, where attributes are listed inside each class, the "aboutness" paradigm represents these properties as separated classes. These classes are linked to the main class with the relation CCO: isAbout. This facilitates the management of data properties by machines (Smith and Ceusters 2015).

As for BFO, CCO and RO allow having a mid-level set of domain-neutral ontologies that facilitate the alignment of core or application ontologies. Having this set of mid-level ontologies aligned to BFO improves the interoperability of core and domain ontologies such as OMSSA with those of the industry domain that share the same structure. BFO and CCO serve as a generic ontology development structure to ensure uniformity in the use of generic terms.

## Relations in OMSSA

One of the important aspects of ontologies concerns the object properties that gather the relations among the different classes. As mentioned in the previous section, the Relations Ontology RO and the extended relations ontology from CCO are implemented as a basis to represent the relations of the different classes for OMSSA. It is important to mention that more

## This article has been published in the Journal of Intelligent Manufacturing

specific relations could be used depending on the ontology domain but are contained as subrelations of those in the RO or the Extended Relation Ontology from CCO.

Using these generic relations prevents inconsistency in the ontology. These relations are intended for specific types of BFO classes. Several inconsistencies might arise when developing the ontology. For example, the relation "precedes" can only be used to relate two occurents. In this context the assertion "a fault precedes the failure" cannot be directly proposed because a fault is considered as a continuant while the failure is an occurrent (definitions and classification of the terms are presented later in this article). To solve this inconsistency, a fault can be linked to another occurrent which is degradation using the relation "participates in", and the class degradation process is linked to the class failure with the relation "precedes". The assertions to link all these terms become "a fault participates in the degradation" and "the degradation precedes the failure". Having this fixed set of generic relations demands a deeper understanding of the terms of the ontologies. It turns out to be a complex task to link all terms in the ontology, but it also allows a better and more complete analysis of the used classes and their actual relations. It helps to identify missing terms and to prevent inconsistency in the ontology.

Only a few domain-specific relations have been added in OMSSA. They concern sub-relations of other domain-neutral object properties imported from RO and CCO. The added relations help to avoid inconsistency or ambiguity among different class properties. The sub-properties proposed in OMSSA help to distinguish the difference between two similar relations. The relations used in OMSSA, including their definition and the graphical representation in the current study, can be found in the Appendix.

## Ontologies in maintenance

Ontologies describe the knowledge of a specific domain through a formal representation of concepts and relations (Nuñez and Borsato 2018). The use of ontologies can simplify the data exchange and interoperability among dissimilar systems, serving as a framework for answering queries about that data (Cao et al. 2019; Panov et al. 2014). Ontologies are often built upon the World Wide Web Consortium (W3C) standards such as the Ontology Web Language (OWL) and are often used to formalize vocabulary for the semantic web (Antoniou et al. 2012; Lu et al. 2019; Nuñez and Borsato 2018; Talhi et al. 2019). Ontologies provide a terminology framework that allows information from a specific domain of knowledge to be processed by a machine. Ontologies have already been used in the maintenance domain. Formal terminology frameworks have been developed to support tasks such as maintenance management, condition monitoring, and prognostics, and health management.

IMAMO (Industrial MAintenance Management Ontology) (Karray et al. 2012) presents a domain ontology for industrial maintenance management. The main goal was to establish a common and shared terminology set for maintenance support systems. The methodology used for its development is METHONTOLOGY (Fernandez et al. 1997). The authors used UML to graphically represent the selected terms and their relationships. IMAMO reasoning assessment was performed using the PowerLOOM tool. IMAMO integrates and reuses terms from other ontology

## This article has been published in the Journal of Intelligent Manufacturing

models such as the SMAC-model (Matsokis et al. 2010) and the MIMOSA-CRIS model (MIMOSA 2001). Maintenance strategies management is not included in the IMAMO approach.

An ontology-based model for prognostics and health management of machines OntoProg, is presented in (Nuñez and Borsato 2017) and (Nuñez and Borsato 2018). The scope of these ontologies is to detail the initial phase of Prognostics and Health Management (PHM) to support intelligent decision systems. These systems can potentially be developed to provide health condition of machines and support smart manufacturing. The ontology model was built following the "Ontology Development 101" (Noy and McGuinness 2001) with the OWL2 language (the current version of the Ontology Web Language) using the Protégé OWL editor. These ontologies reuse accurate terms from maintenance standards and norms that are also used in OMSSA. These ontologies are domain-specific and focus only on PHM, and thus, they leave the maintenance strategies terminology out of scope.

A core ontology for condition monitoring, CM-core, defines a basic set of concepts to understand the condition monitoring domain (Cao et al. 2019). Such a core ontology serves as a basis for other domain ontologies that can be used in several applications. It also builds upon the "Ontology Development 101" (Noy and McGuinness 2001) and uses UML to represent the ontology. As for the previous two ontologies, it focuses only on condition monitoring, which is part of current trends for maintenance strategies but not presented as such in CM-core. ROMAIN (Karray et al. 2019) is a Reference Ontology for industrial MAINtenance, compliant with the Basic Formal Ontology (BFO 2.0) (See Sect. BFO as a top-level ontology) (Arp et al. 2016; International Organization for Standardization (ISO) 2020a, 2020b). It aims at giving a standard vocabulary framework for maintenance management inspired by Reliability Centered Maintenance (RCM) strategies. The strong point of ROMAIN is the alignment with BFO, which is a top-level domain-neutral ontology. It allows the alignment of application ontologies with upper-level domain and reference ontologies. ROMAIN offers a robust set of classes for CMMS data, for example, the classes to define maintenance work orders records that describe maintenance actions. Many of these classes are reused in OMSSA since ROMAIN and OMSSA are BFO compliant. However, ROMAIN has a limited set of concepts related to maintenance strategies. ROMAIN aligns to a classical RCM classification for maintenance strategies, and the concepts involved in the selection of such strategies are not presented.

Another related work is presented in (Lupp et al. 2020), in which template libraries are suggested to build an ontology for the evaluation of maintenance strategies. This research is oriented on a novel methodology to build and maintain modular ontologies using maintenance strategies assessment as the use case. The terminology applied to describe the use case does not cover the current trends in maintenance strategies.

As part of a multidisciplinary effort to construct open access ontologies that can be used for industrial purposes, the Industrial Ontology Foundry (IOF) has been created in 2016 (IOF 2020). Within the IOF, there is a specific group working for maintenance management. At the moment of the creation of OMSSA, no stable versions of the ontologies from IOF were available. However, IOF ontologies are BFO compliant and use some mid-level reference ontologies that have been considered for OMSSA. This will allow a future alignment of OMSSA to other IOF ontologies. The top-level and mid-level ontologies reused in OMSSA are presented in chapter 4.

## This article has been published in the Journal of Intelligent Manufacturing

The above-mentioned ontologies have at least one of the following limitations:

- Their scope does not cover maintenance strategies or present a limited scope where important concepts for maintenance strategy selection are not considered.

- Their maintenance strategy taxonomy does not include the current trends in predictive maintenance. This leaves behind concepts that are currently important when selecting maintenance strategies.

- Their development framework does not consider the alignment to a top-level domainneutral ontology which complicates their reuse and/or interoperability with other related ontologies.

OMSSA aims at covering the gaps in the above-mentioned ontologies by fulfilling the following requirements:

- Capture the core notions related to the maintenance strategies.

- Consider the current trends in maintenance strategies.

- Be aligned with a top-level domain-neutral ontology.

- Use the established terminology by norms, standards, and domain experts of maintenance strategies.

Given this research opportunity, the scope for the OMSSA was defined as maintenance strategy selection and assessment. As part of the ontology scope delimitation, a set of competency questions are proposed. These questions can be used for the model evaluation as they serve as a fidelity measure of the model with real-life phenomena (March and Smith 1995). Maintenance experts would be able to recommend a specific strategy to address a specific failure mode of an item or asset. The following competency questions are proposed to delimit the OMSSA scope:

1. What are the failure modes associated with an item or asset?

2. What is the cause of a failure mode?

3. What is the criticality of a failure mode?

4. What is the recommended maintenance strategy for a failure mode?

5. What is the triggering event specification for a specific maintenance action?

6. What is the benefit of implementing a specific maintenance strategy?

7. What is the risk of implementing a specific maintenance strategy?

As terms sources for OMSSA, several maintenance standards ((European Committee for Standardization 2017; International Electrotechnical Commission (IEC) 2018; International Organization for Standardization (ISO) 1997, 2003, 2012a; MIMOSA 2001)) , expert knowledge and existing related ontologies have been consulted. Special attention is given to the terms that are aligned to BFO, as it is selected as the top-level ontology for the current model. An identifier has been assigned to the most relevant sources of terms. These identifiers are summarized in Table 1 and later used in the following section for traceability purposes of OMSSA terms.

## This article has been published in the Journal of Intelligent Manufacturing

<div align="center">

Table 1. The identifier for the terms sources

</div>

<table border="1"><tr><td>Reference</td><td>Identifier</td><td>Reference</td><td>Identifier</td></tr><tr><td>(European Committee for Standardization 2017)</td><td>1</td><td>(International Electrotechnical Commission (IEC) 2018)</td><td>10</td></tr><tr><td>(Montero Jimenez et al. 2020)</td><td>2</td><td>(International Organization for Standardization (ISO) 2012b)</td><td>11</td></tr><tr><td>(Nuñez and Borsato 2018)</td><td>3</td><td>(Saxena et al. 2010)</td><td>12</td></tr><tr><td>(Karray et al. 2012)</td><td>4</td><td>(Keller et al. 2001)</td><td>13</td></tr><tr><td>(MIMOSA 2001)</td><td>5</td><td>(Kacprzynski et al. 2002)</td><td>14</td></tr><tr><td>(Karray et al. 2019)</td><td>6</td><td>(Rudnicki 2020a)</td><td>15</td></tr><tr><td>(Arp et al. 2016)</td><td>7</td><td>(INCOSE 2015)</td><td>16</td></tr><tr><td>(International Organization for Standardization (ISO) 1997)</td><td>8</td><td>(Rudnicki 2020b)</td><td>17</td></tr><tr><td>(International Organization for Standardization (ISO) 2003)</td><td>9</td><td>(Protter 2005)</td><td>18</td></tr></table>

## Ontology for Maintenance Strategy selection and Assessment (OMSSA)

Maintenance management trends are now more oriented towards the analysis of data to establish the right moment to trigger maintenance actions based on the condition of the maintainable system. The condition is a quality that is normally used to describe the capabilities of an item to fulfill its function. Condition can be described by four different values: nominal, degraded, critical, and failed (Ramasso and Gouriveau 2010). For each item, there must be a specification to be able to assess its current condition:

- Nominal_condition refers to the range of parameters in which the item is intended to operate.

- Degraded_condition refers to an item that can perform its intended function but is not within the nominal operation parameters.

- Critical_condition is a sub-class of degraded_condition in which the item has overshot the safety degradation thresholds, and a failure is imminent.

- Failed_condition refers to the complete impossibility of the item to perform its intended function after a failure.

Fig. 4 shows a generic example of the evolution of the health/degradation of an item. The horizontal axis represents the life cycle of the item, and the vertical axis is an index that represents its health or degradation, for example, the reliability. The time in which the item works within the limits of nominal_condition is described by a process that ends when a fault appears. The fault will affect the item operation, accelerating its degradation. Within the accelerated degradation process, there is a safety degradation threshold that defines the starting point of the critical_condition. The safety degradation threshold is imposed by a safety operating margin to prevent the actual failure. Table 2 summarizes the definitions for all terms in Fig. 4.


> **Figure Description:**

This scatter plot illustrates the progression of a system's health over time, with the vertical axis labeled "Health/Degradation Index" ranging from 0 to 1.2 and the horizontal axis labeled "Operating cycles" ranging from 0 to 250. The data points, represented by blue dots, follow a trend line that remains relatively low and stable during the "Nominal operation process" (from 0 to approximately 150 cycles) before rising sharply during the "Degradation process" (from approximately 150 to 190 cycles).

The chart is divided into three horizontal zones: "Nominal condition" (0 to ~0.3 on the index), "Degrading condition" (~0.3 to ~0.9), and "Critical condition" (~0.9 to 1.0). A "Safety margin" is indicated between the 0.9 and 1.0 index levels. Several key events are annotated: "Fault start" is marked at approximately 150 cycles where the index is around 0.3, "Degradation threshold" is indicated by a vertical red line at 150 cycles, and "Failure" is marked at approximately 190 cycles where the index reaches 1.0. The plot uses a grid background and includes horizontal and vertical red dashed lines to delineate these thresholds and the failure point.



<div align="center">

Fig. 4. Condition evolution over the item life cycle

</div>

<div align="center">

Table 2. Definitions for important classes to describe the condition of an item

</div>

<table border="1"><tr><td>Class</td><td>OMSSA Formal definition</td><td>Based on(see Table 1)</td></tr><tr><td>Condition</td><td>A BFO:quality sub-class that an OMSSA:item bears.It qualifies the operation state of the item.It states the operational parameters of the item described by OMSSA:condition data and prescribed by OMSSA:condition specification.</td><td>1,6</td></tr><tr><td>Condition data</td><td>A CCO:Descriptive Information Content Entity that consists of a set of propositions that describes OMSSA:Condition</td><td>3,4,8</td></tr><tr><td>Degradation</td><td>A CCO:Decrease of function.It represents a detrimental change in the operating condition of an item, normally as a result of a fault.</td><td>1,6,8,11</td></tr><tr><td>Degraded condition</td><td>An OMSSA:Condition sub-class that qualifies an OMSSA:item operating out of its optimal parameters</td><td>1,8,11</td></tr><tr><td>Failed condition</td><td>An OMSSA:Condition sub-class that qualifies the impossibility of an OMSSA:Item to perform its intended function.</td><td>1,8,11</td></tr><tr><td>Fault</td><td>A BFO:quality sub-class.It qualifies a abnormal behavior or defect the OMSSA:item bears.It is described by OMSSA:symptoms</td><td>1,3,4,11</td></tr><tr><td>Nominal condition</td><td>An OMSSA:Condition sub-class that qualifies the optimal operation of an OMSSA:Item</td><td>1,8,11</td></tr><tr><td>Nominal operation process</td><td>A CCO:stasis subclass that defines the time in which an item remains in nominal condition.This class is equivalent to CCO:Nominal stasis</td><td>1,11</td></tr><tr><td>Item</td><td>A CCO:Object subclass equivalent to CCO:Artifact.An Object that was designed by some Agent to realize a certain function.</td><td>1,4,6,11</td></tr></table>

Condition is described by the condition_data, which is at the same time the input for other processes to determine the triggering events for maintenance actions (see Fig. 5). These processes are carried out by a predictive maintenance system and can be used to detect incipient faults (fault_detection), assess degradation until a specific threshold (degradation_threshold_overshoot), and forecast the remaining useful life of the item or one of its components (failure_forecasting). Nevertheless, there are two other triggering events that do not use advanced predictive maintenance techniques but cannot be ignored: the failure of the item and a fixed_time_recommendation prescribed by a preventive maintenance_plan.


> **Figure Description:**

This diagram illustrates a process flow for a predictive maintenance system. At the top, a "Predictive maintenance system module" (blue box) connects to a red-dashed box containing three green processes: "Fault detection process," "Degradation assessment process," and "Prognostic process." The connection from the module to these processes is labeled "participatesIn." A "Condition monitoring" box (green) has an output labeled "hasOutput" leading to a "Condition data" box (blue), which then feeds into all three processes within the red-dashed box with a connection labeled "isInputOf."

The three processes in the red-dashed box have outgoing connections labeled "precedes." The "Fault detection process" precedes "Fault detection" (green box). The "Prognostic process" precedes "Degradation threshold overshoot" (green box). Additionally, "Condition data" precedes "Failure forecasting" (green box). The boxes "Failure" (green), "Failure forecasting" (green), "Degradation threshold overshoot" (green), and "Fault detection" (green) all connect to a "Triggering event" (green box) and a "Fixed time action recommendation" (green box). A "Preventive maintenance plan" (blue box) connects to "Fixed time action recommendation" with a label "prescribes." Finally, the "Triggering event" connects to a "Maintenance action" (green box) with a label "precedes." The text at the top reads, "This article has been published in the Journal of Intelligent Manufacturing."



<div align="center">

Fig. 5. Relations among the different triggering events

</div>

<div align="center">

Table 3. Definitions of the terms in Fig. 5 and Fig. 6.

</div>

<table border="1"><tr><td>Class</td><td>OMSSA Formal definition</td><td>Based on(see Table 1)</td></tr><tr><td>Condition Monitoring</td><td>A BFO:a process that has as output OMSSA:Condition data</td><td>1,10,11</td></tr><tr><td>Corrective Maintenance</td><td>An OMSSA:maintenance strategy whose triggering event is the failure occurrence</td><td>1,2,10,11</td></tr><tr><td>Degradation assessment process</td><td>A BFO:process performed on an OMSSA:item by an OMSSA:predictive maintenance module to assess degradation until this degradation overshoots a specific threshold.</td><td>1,2,7,10,11</td></tr><tr><td>Degradation threshold overshoot</td><td>An OMSSA:triggering event subclass related to predictive maintenance strategy.It is prescribed by a degradation assessment module of a predictive maintenance system.</td><td>1,2,10,11</td></tr><tr><td>Failure</td><td>An OMSSA:triggering event subclass related to corrective maintenance strategy.The impossibility of an item to perform its intended function triggers a maintenance action</td><td>1,2,6,10,11</td></tr><tr><td>Failure forecast</td><td>An OMSSA:triggering event subclass related to predictive maintenance strategy.It is prescribed by a failure forecast module of a predictive maintenance system.</td><td>1,2,10,11</td></tr><tr><td>Fault detection</td><td>An OMSSA:triggering event subclass related to predictive maintenance strategy.It is prescribed by a fault detection module of a predictive maintenance system.</td><td>1,2,10,11</td></tr><tr><td>Fault detection process</td><td>A BFO:process performed on an OMSSA:item by an OMSSA:predictive maintenance module to detect incipient faults</td><td>1,2,7,10,11</td></tr><tr><td>Fixed time recommendation</td><td>An OMSSA:triggering event subclass related to preventive maintenance strategy.It is prescribed by a preventive maintenance plan.A recommendation based on fixed operation intervals or from fixed basic inspections triggers a maintenance action.</td><td>1,2,10,11</td></tr><tr><td>Maintenance action</td><td>A BFO:process performed on an OMSSA:item to restore or keep it in its operational state.</td><td>1,2,7,10,11</td></tr><tr><td>Maintenance strategy</td><td>A CCO:directive information content entity resulting from maintenance strategy development process.It prescribes the expected triggering event for each maintenance action on an item</td><td>1,2,7,10,11</td></tr><tr><td>Predictive Maintenance</td><td>An OMSSA:maintenance strategy whose triggering events are based on the condition of the OMSSA:Item but before a failure.There are three possible triggering events</td><td>1,2,5,10,11</td></tr><tr><td>Predictive maintenance system</td><td>A CCO:information processing artifact used to analyze the item condition data and perform fault detection,health/degradation assessments,and/or life expectancy estimations.</td><td>1,2,10,11</td></tr><tr><td>Preventive Maintenance</td><td>An OMSSA:maintenance strategy whose triggering event is a predefined fixed time event,after an operation time interval or at a given preventive maintenance date.</td><td>1,2,10,11</td></tr><tr><td>Preventive Maintenance plan</td><td>A CCO:plan subclass.It includes all preventive recommendations to trigger maintenance actions</td><td>1,2,10,11</td></tr><tr><td>Prognostic process</td><td>A BFO:process performed on an OMSSA:item by an OMSSA:predictive maintenance module to estimate the time to a future failure of an item or one of its components.</td><td>1,2,7,10,11</td></tr><tr><td>Triggering event</td><td>A BFO:process boundary that is the starting point for a maintenance action</td><td>1,2,7,10,11</td></tr></table>

## This article has been published in the Journal of Intelligent Manufacturing

Having a clearer idea of the different triggering events presented in Fig. 5 and the maintenance strategy taxonomy introduced in "Sect. Maintenance strategies", the next step allows setting the relations between the triggering events and the maintenance strategies. Fig. 6 shows these relations in which a corrective_maintenance strategy is related to a failure, a preventive_maintenance strategy is related to a fixed_time_recommendation, and a predictive_maintenance strategy is related to fault_detection, degradation_threshold_overshoot, or a failure_forecast. These relations will allow classifying the different maintenance actions in the different maintenance strategies. Table 3 summarizes the concepts presented in Figs. 5 and 6.


> **Figure Description:**

The diagram illustrates a conceptual relationship between maintenance strategies and triggering events, organized into two main groups represented by green and blue boxes. On the left, a green box labeled "Triggering event" points upward to a green box labeled "BFO: Process boundary." The "Triggering event" box is connected to a vertical line that branches into five green boxes: "Failure," "Fixed time recommendation," "Fault detection," "Degradation threshold overshoot," and "Failure forecasting."

On the right, three blue boxes representing maintenance types—"Corrective Maintenance," "Preventive Maintenance," and "Predictive Maintenance"—are connected to a vertical line that leads to a blue box labeled "Maintenance strategy." This "Maintenance strategy" box points upward to a blue box labeled "CCO: Directive Information content entity." 

Relationships between the two groups are indicated by thin blue arrows labeled "isSubjectOf." Specifically, an arrow points from "Corrective Maintenance" to "Failure," an arrow points from "Preventive Maintenance" to "Fixed time recommendation," and an arrow points from "Predictive Maintenance" to both "Fault detection," "Degradation threshold overshoot," and "Failure forecasting."



<div align="center">

Fig. 6. Relations between triggering events and maintenance strategies

</div>

The maintenance_strategy_development_process is composed of different analyses and technical developments (see Fig. 7). There should be at least one maintenance_strategy for each failure_mode of an item. Failure modes and their impacts must be well known so that the most suitable strategy could be suggested. The Failure Mode, Effects and Criticality Analysis (FMECA) (International Electrotechnical Commission (IEC) 2018) is often used to assess the impact of failure modes of an item, their potential causes, risks (effects), and criticality (Zhou et al. 2015).

The FMECA can be used as the starting point for the maintenance strategy development. Several proactive strategies can be suitable to address a failure mode, starting with fixed time recommendation and coming to a precise failure prognostic. The selection of the most suitable proactive strategy depends on the technology readiness for each application, on the operational context, the implementation cost, and the potential benefits and risks of implementing predictive maintenance. FMECA has a report (represented as OMSSA class) composed of the CCO: Information Content Entities explaining the different aspects that have been considered to select a specific maintenance strategy. Among these information entities, one can find the functional failure of an item, the failure mode, the cause of failure, the

## This article has been published in the Journal of Intelligent Manufacturing

failure_effect, the criticality, and failure_likeliness. The instances for all these entities are compulsory to be known when selecting a maintenance strategy using a FMECA.

A Cost-Benefit-Risk_Analysis is a complementary method that is used to assess the suitability of a strategy when several options are possible; especially when it includes the implementation of specialized systems for health monitoring, fault detection and identification, health assessment, and failure forecast that represent an important initial investment but are also attractive in terms of potential benefits. As (Saxena et al. 2010) explains, a Cost-Benefit Risk_Analysis is vital to justify the implementation of more advanced maintenance strategies. As for FMECA, the Cost-Benefit-Risk_Analysis has a corresponding report class in OMSSA. This report contains important information content entities that are considered to select a new maintenance strategy, especially when justifying the transition of existing preventive strategies to predictive ones or when upgrading the type of predictive strategy. Among these information content entities, one can find the implementation_benefit of the new strategy, its related implementation_risk, and implementation_cost. It is important to mention that for the Cost-Benefit-Risk_Analysis some data should be gathered from other sources such as the FMECA and the CMMS. One of these data is the maintenance_cost that has been accumulated by an item in a specific interval of time; it is likely to justify the implementation of new maintenance strategies by the reduction of these costs.

The most advanced strategies that aim at performing accurate diagnosis and prognosis on the item rely on specialized tools, methods, and systems for decision support. These tools or systems demand engineering work for their design and implementation. That is why a technical development process is also included as part of the maintenance strategy development. oThe engineering work performed in this process leads to a preventive_maintenance_plan and/or a predictive_maintenance_system, depending on the item to be maintained and its operational context.

As it can be seen, the maintenance strategy development has many interdependencies among the different engineering activities. It is important to point out that there are other factors that can affect the development of a maintenance strategy and are not part of these engineering processes, such as production policies or authorities' regulations. These can be seen as "external" dependencies as the maintenance engineer may not directly intervene on them. These external dependencies are included in OMSSA in the class maintenance_strategy_dependency.


> **Figure Description:**

This image is a diagram illustrating a maintenance strategy development process. At the top, the text "This article has been published in the Journal of Intelligent Manufacturing" appears. The diagram consists of various rectangular nodes connected by arrows with labeled relationships. Blue nodes represent general entities, while green nodes represent processes. A large red dashed box encompasses the "Maintenance strategy development process" and its sub-components: "FMECA," "Cost-Benefit-Risk Analysis," and "Technical development process."

The relationships are as follows: "Item" hasFunction "BFO: Function," which is "isAbout" "Function description." "Function description" is "isInputOf" "FMECA." "FMECA" precedes "Cost-Benefit-Risk Analysis." "FMECA" hasOutput "Failure Mode." "Cost-Benefit-Risk Analysis" hasOutput "Maintenance cost." "Maintenance strategy" hasOutput "Maintenance strategy development process," which is a "BFO: Process." "Maintenance strategy" is also connected to "CCO: Directive ICE." The "Maintenance strategy development process" hasProcessPart "FMECA," "Cost-Benefit-Risk Analysis," and "Technical development process." 

The "Technical development process" hasOutput "Technical project plan," "Preventive maintenance plan," and "Predictive maintenance system." Additionally, "Maintenance Strategy Dependency" is "isInputOf" "Maintenance strategy development process." The entire structure maps the logical flow from item function description through failure analysis and cost-benefit assessment to the final technical and maintenance planning outputs.



<div align="center">

Fig. 7. Relations for the maintenance strategy development process

</div>

Once the maintenance strategy is selected to address a failure mode of an item, a maintenance action is specified in which the expected triggering event will be defined. This specification can be later compared to the actual triggering event of a maintenance action that is normally recorded in a work order report. This comparison between the specification and the report helps to validate and assess the maintenance strategy over time. A knowledge base created with OMSSA can store all the maintenance strategies assigned to the components of an item, some queries on the maintenance records can automate the assessment on the proposed strategies allowing to re-adjust or change the strategy when it is no longer suitable. Fig.. 8 shows the classes and the relations that can be used to assess the maintenance strategy for a given failure mode. For OMSSA purposes, the concepts related to the work orders reports have been imported from ROMAIN (see "Sect. Ontology engineering") as it already offers a complete set of information content entities that can be used to describe a maintenance action. OMSSA reuses these ROMAIN classes and aligns them to the newer version of CCO (version 1.3). An important class incorporated in OMSSA as part of the maintenance work order report is the Triggering event report. Table 4 summarizes the definitions of classes related to FMECA, cost-benefit-risk analysis, and maintenance reports used for maintenance strategies selection and assessment.


> **Figure Description:**

This image is a header and a diagram.

The header text reads "This article has been published in the Journal of Intelligent Manufacturing". The diagram is a conceptual map consisting of rectangular nodes connected by labeled arrows. The central node is "Maintenance action" (green), which is preceded by a "Triggering event" (green) and itself precedes a "Nominal operation process" (green). The "Maintenance action" node has an output labeled "hasOutput" pointing to a "Maintenance cost" node (blue).

To the left, a "Maintenance strategy" node (blue) has two parts, indicated by a "hasPart" arrow branching to "Maintenance action specification" (blue) and "Triggering event specification" (blue). To the right, a "Maintenance work order report" node (blue) is connected to the "Maintenance action" node by a "Describes" arrow. The "Maintenance work order report" node also has a "hasPart" relationship pointing to a "Triggering event report" node (blue). All nodes are rectangular with rounded corners, and the relationships are defined by directed lines with italicized labels.



<div align="center">

Fig.. 8. Relations between the classes to assess maintenance strategies

</div>

<div align="center">

Table 4. Definitions of classes related to FMECA, cost-benefit-risk analysis, and maintenance reports used for maintenance strategies selection and assessment.

</div>

<table border="1"><tr><td>Class</td><td>OMSSA Formal definition</td><td>Based on(see Table 1)</td></tr><tr><td>Cause of failure</td><td>A CCO:Descriptive Information Content Entity that describes the cause of a failure mode.It is about a CCO:Cause that can lead to an OMSSA:Failure</td><td>1,10,11</td></tr><tr><td>Cost-Benefit-Risk analysis</td><td>A BFO:process,which is part of the strategy development process,it aims at evaluating the implementation of a more advanced maintenance strategy for an item compared to the current one.It considers the failure risk,the cost,and the benefits of its implementation.</td><td>12,13,14</td></tr><tr><td>Cost-Benefit-Risk analysis Report</td><td>A CCO:report subclass.It carries the information content entities that describe the result of an OMSSA:Cost_benefit_risk_analysis.</td><td>12,13,14</td></tr><tr><td>Criticality</td><td>A CCO:ordinal measurement information content entity that places the failure risk into some rank order that is used in the FMECA</td><td>1,10,11</td></tr><tr><td>Failure effect</td><td>A CCO:Descriptive Information Content Entity that describes the impacts of a failure in terms of safety,environment,and operation.It is normally measured by rank.It is about a CCO:Effect that results from an OMSSA:Failure</td><td>1,10,11</td></tr><tr><td>Failure likeliness</td><td>A CCO:ordinal measurement information content entity that states the likelihood of a failure occurrence,based statistical information,reliability analysis,or design information</td><td>1,10,11</td></tr><tr><td>Failure mode</td><td>It is a CCO:Descriptive information content entity that describes a failure of an item and the corresponding fault that can cause the failure.It is an output of the Failure Modes,Effects,and Criticality Analysis(FMECA).</td><td>1,10,11</td></tr><tr><td>Failure Modes,Effects,and Criticality Analysis</td><td>A BFO:process aiming at defining the possible failures of an item based on the non-fulfillment of its intended function.It defines the effects (consequences) and criticality of the failure.</td><td>1,10,11</td></tr><tr><td>Failure Modes,Effects,and Criticality Analysis Report</td><td>A CCO:report subclass.It carries the information content entities that describe the result of an OMSSA:Cost_benefit_risk_analysis.</td><td>12,13,14</td></tr><tr><td>Function</td><td>A function is a disposition that exists in virtue of the bearer's physical make-up,and this physical make-up is something the bearer possesses because it came into being,either through evolution(in the case of natural biological entities) or through intentional design(in the case of artifacts),in order to realize processes of a certain sort.(Axiom label in BFO2 Reference:[064-001])</td><td>6,7,9</td></tr><tr><td>Function description</td><td>A CCO:Descriptive Information Entity subclass that describes a BFO:Function</td><td>7,9</td></tr><tr><td>Implementation benefit</td><td>A CCO:Descriptive information content entity sub-class that describes a benefit of implementing a preventive maintenance plan or a predictive maintenance system as part of the maintenance strategies.</td><td>12,13,14</td></tr></table>

<div align="center">

This article has been published in the Journal of Intelligent Manufacturing

</div>

<table border="1"><tr><td>Implementation cost</td><td>A CCO: Descriptive information content entity subclass that quantifies the cost of implementing a more advanced maintenance strategy by means of a preventive maintenance plan and/or a predictive maintenance system.</td><td>12,13,14</td></tr><tr><td>Implementation risk</td><td>A CCO: Descriptive information content entity. It describes the risk of implementing a new predictive maintenance strategy, plan, or system.</td><td>12,13,14</td></tr><tr><td>Maintenance work order record specification</td><td>A CCO: Descriptive information content entity that describes a maintenance action</td><td>1,6,11,15</td></tr><tr><td>Maintenance action specification</td><td>A CCO: Directive information content entity that states the specifications of a maintenance action</td><td>1,11,15</td></tr><tr><td>Maintenance cost</td><td>A CCO: Descriptive information content entity subclass that quantifies the cost of any maintenance action performed on an OMSSA: item</td><td>1,10,11</td></tr><tr><td>Maintenance strategy development process</td><td>A BFO: process subclass. It includes all activities and sub-processes to select the right maintenance strategy to apply for the different failure modes of an item.</td><td>1,10,11</td></tr><tr><td>Technical development process</td><td>A BFO: process sub-class. It refers to all technical activities carried out to implement a predictive maintenance system or a preventive maintenance plan.</td><td>15,16,17</td></tr><tr><td>Technical project plan</td><td>A CCO: plan subclass. It describes the plan of the implementation of a technical project</td><td>15,16,17</td></tr><tr><td>Triggering event record</td><td>A CCO: Descriptive information content entity. It describes the actual triggering event for a specific maintenance action in a maintenance report.</td><td>6,15,16,17</td></tr><tr><td>Triggering event specification</td><td>A CCO: Directive information content entity that states the expected triggering event for a maintenance action</td><td>6,15,17,18</td></tr></table>

## Evaluation and discussion

The evaluation of the model is composed of two main steps: verification and validation. The definitions of verification and validation are derived from (INCOSE 2015). The verification aims at providing evidence of the consistency of the model, meaning that it fulfills the technical requirements for its development. The validation provides evidence that the model when in use, fulfills the objectives for which it was developed.

As OMSSA was developed using the Protégé editor, the verification can be carried out using one of the reasoners embedded in the editor. Different reasoners can be installed and used to verify the model's consistency. These reasoners can be configured to verify different aspects of class inferences, object property inferences, data property inferences, and individual inferences such as hierarchy, domain, range, and conflicting disjoint assertions (Nuñez and Borsato 2018). It is important to make sure that when establishing relations among classes and instances, there are no contradictory or duplicated statements. The HermiT OWL reasoner (Glimm et al. 2014), embedded as a Protégé plug-in, was used to verify OMSSA consistency. During the verification process, several inconsistency alarms were detected, forcing the restructuration of several relations among OMSSA classes. The model presented in "Sect. BFO as a top-level ontology" corresponds to a stable version with no inconsistency warnings from the reasoners.

Once the verification of the model is fulfilled, the validation process to assess the fidelity of the model with its initial application requirements takes place. For OMSSA, the scope is limited to maintenance strategy selection and assessment. Ontologies are meant to be vocabulary frameworks for practical applications. It is important to understand how it can be integrated into practical applications (Ferrer et al. 2018). Fig. 9 shows the principle of the implementation of OMSSA in practical applications. OMSSA can be retrieved directly from its online repository and is

## This article has been published in the Journal of Intelligent Manufacturing

aimed to be instantiated with information from different sources such as FMECA, cost-benefit-risk analysis, or CMMS engineering information, among other sources of data. Once the ontology is populated, it becomes a knowledge base of a specific domain that can be used by smart agents such as Decision Support Systems (DSS). There exist ontology libraries that can be used to integrate the different components of the system. For example, the OWL API (Horridge and Bechhofer 2011) provides a Java-based platform to create the interfaces between the ontology and the data sources and between the knowledge base (instantiated ontology) and a smart agent such as the DSS. To do so, different types of queries can be implemented, such as Description Logic (DL) queries, SPARQL queries, and SQWRL queries (Muñoz-Hernández et al. 2021).

To validate its functionality, OMSSA was populated with the information of a generic FMECA based on a real air compressor. This 10HP air compressor supplies 10 l/s of air at 8 bar to a pneumatic cutting machine. The FMECA was developed by maintenance experts who determined the failure modes, their causes, effects, and criticality for all the air compressor components. These variables led the experts to suggest suitable maintenance strategies. As OMSSA was instantiated with the air compressor case study, it becomes a knowledge base on maintenance strategies for an air compressor (Noy and McGuinness 2001).


> **Figure Description:**

This diagram illustrates the architecture of a system involving four main components represented as rectangular boxes, each containing a smaller yellow box. In the top-left, the "OMSSA" component contains a box labeled "Provide terminology Framework," which has an arrow pointing to the "Domain-specific Knowledge Base" component on the top-right. This arrow is labeled "Classes, relations, axioms...". The "Domain-specific Knowledge Base" contains a box labeled "Stores instantiated ontology."

In the bottom-left, the "Data-sources (FMECA-CMMS-Cost/Benefit/Risk Analysis-Engineering Info...)" component contains a box labeled "Provide instances." An arrow leads from this box to the "Domain-specific Knowledge Base," labeled "Instances (data)."

In the bottom-right, the "Decision Support Systems (DSS)" component contains a box labeled "Support decision making procces." There is a bidirectional relationship between the "Domain-specific Knowledge Base" and the "Decision Support Systems (DSS)." An upward-pointing arrow from the DSS to the Knowledge Base is labeled "queries (SPARQL, DL, SQWRL)," and a downward-pointing arrow from the Knowledge Base to the DSS is labeled "terms, relations, lists, semantic similarity, semantic rules...".



<div align="center">

Fig. 9. Implementation of OMSSA for practical applications

</div>

To measure OMSSA fidelity to the real world, the ontology-based knowledge base (meaning the instantiated ontology) should be able to answer questions like an expert would do (Grüninger et al. 1995b; Heravi et al. 2014; Raad and Cruz 2015; Steiner and Albert 2017). To do so, the competency questions used to delimit the ontology scope can be used as a guideline. Validation of the knowledge modeling is performed by answering these competency questions with SPARQL queries on the instantiated ontology. To do so, the SPARQL plug-in for Protégé was used (Redmond 2012). As part of the SPARQL queries writing, a set of prefixes for OMSSA and all reused ontologies for its development (BFO, CCO, and RO). It simplifies the writing of the SPARQL queries for OMSSA validation. Table 5 summarizes the proposed prefixes for OMSSA validation using the SPARQL queries.

## This article has been published in the Journal of Intelligent Manufacturing

The air compressor is composed of four main items that are instantiated as: compressor_unit_1, electric_motor_1, drying_unit_1, and transmission_1. To illustrate the applicability of OMSSA, the first competency question (What are the failure modes associated with an item or asset?) will be answered by querying the instantiated OMSSA to obtain all failure modes related to the electric_motor_1. The result of the SPARQL query showed all registered failure modes for the electric motor (see Table 6 and Fig. 10 ). The other competency questions (questions 2 to 7 in the Ontologies in Maintenance section) are related to each failure mode. A query was performed to answer these competency questions for the failure mode Crank_damage (see Table 7 and Fig. 11). This query allowed to show the cause_of_failure, the criticality, the maintenance_strategy, and the expected triggering_event to perform the maintenance_action of changing the oil. Answering simple queries such as those in tables 6 and 7 will help validate the consistency of the modeled knowledge in the ontology. It is important to point out that OMSSA is not only limited to FMECA classes but also modeled the knowledge for the maintenance strategy assessment and upgrade to more advanced strategies. To do so, OMSSA contains classes that can be instantiated from CMMS and cost-benefit-risk analysis reports and other engineering information sources.

The four requirements proposed for OMSSA development have been satisfied. The first requirement established in Maintenance Ontology Section for OMSSA was to "capture the core notions related to the maintenance strategies". By performing these query-based tests, the consistency of the vocabulary related to maintenance strategies in OMSSA was validated. OMSSA includes the vocabulary related to advanced strategies triggered by diagnostics and prognostics; this validates the proposed requirement for OMSSA related to include the current trends in maintenance strategies. As OMSSA uses BFO as top-level ontology, CCO as mid-level ontologies, and its scope is limited by competency questions inspired in the domain knowledge, the proposed requirement related to OMSSA alignment is also met. As the terms for OMSSA were extracted from standards and norms and domain experts for maintenance strategies, the requirement with regards to the vocabulary sources for OMSSA is also satisfied.

<div align="center">

Table 5. Prefixes to perform SPARQL queries on OMSSA

</div>

<table border="1"><tr><td>PREFIX rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#</td></tr><tr><td>PREFIX owl: http://www.w3.org/2002/07/owl#</td></tr><tr><td>PREFIX rdfs: http://www.w3.org/2000/01/rdf-schema#</td></tr><tr><td>PREFIX xsd: http://www.w3.org/2001/XMLSchema#</td></tr><tr><td>PREFIX OMSSA: http://www.semanticweb.org/j.montero-jimenez/ontologies/2020/7/OMSSA#</td></tr><tr><td>PREFIX bfo: http://purl.obolibrary.org/obo/</td></tr><tr><td>PREFIX ro: http://www.obofoundry.org/ro/ro.owl#</td></tr><tr><td>PREFIX exro: http://www.ontologylibrary.mil/CommonCore/Upper/ExtendedRelationOntology#</td></tr><tr><td>PREFIX ieo: http://www.ontologylibrary.mil/CommonCore/Mid/InformationEntityOntology#</td></tr></table>

Table 6. SPARQL query to answer the first competency question on Compressor Unit 1

<table border="1"><tr><td colspan="2">SELECT ?item ?FailureMode</td></tr><tr><td colspan="2">WHERE{?item rdfs:label“Compressor Unit 1”?item OMSSA:has_failure_mode ?FailureMode}</td></tr></table>

<div align="center">

This article has been published in the Journal of Intelligent Manufacturing

</div>

<table border="1"><tr><td>Item</td><td>FailureMode</td></tr><tr><td>Compressor Unit 1</td><td>Crank damage</td></tr><tr><td>Compressor Unit 1</td><td>Paper seal leak</td></tr><tr><td>Compressor Unit 1</td><td>Outlet valve damage</td></tr><tr><td>Compressor Unit 1</td><td>Frame damage</td></tr><tr><td>Compressor Unit 1</td><td>Cylinder rings damage</td></tr><tr><td>Compressor Unit 1</td><td>Piston damage</td></tr></table>

<div align="center">

Fig. 10. Answer to the SPARQL query on Table 6

</div>

<div align="center">

Table 7. SPARQL Query to answer the competency questions for the failure mode "Crank damage"

</div>

<table border="1"><tr><td>SELECT ?item ?FailureMode ?Cause ?Criticality ?MaintenanceStrategy ?TriggeringSpecification
WHERE{ ?item exro:has_function ?Function.
?item OMSSA:has_failure_mode ?FailureMode.
?FailureMode rdfs:label“Crank damage”.
?FailureMode OMSSA:is_subject_of_failure_cause ?Cause.
?FailureMode OMSSA:is_subject_of_criticality ?Criticality.
?MaintenanceStrategy ieo:is_About ?FailureMode.
?MaintenanceStrategy OMSSA:has_maintenance_action ?MaintenanceaAction.
?MaintenanceAction OMSSA:has_triggering_specification ?Triggering
Specification}</td></tr></table>

<table border="1"><tr><td>Item</td><td>FailureMode</td><td>Cause</td><td>Criticality</td><td>MaintenanceStrategy</td><td>TriggeringSpecification</td></tr><tr><td>Compressor Unit 1</td><td>Crank damage</td><td>Insufficient lubrication</td><td>High_criticality</td><td>Predictive oil change</td><td>Oil degradation detection</td></tr></table>

<div align="center">

Fig. 11. Answer to SPARQL query on Table 7

</div>

OMSSA covers important terms related to the maintenance strategy selection and assessment, allowing the implementation of intelligent decision support systems that can perform automated tasks in the maintenance strategy domain. For example, ontologies enable the processing and sharing of knowledge that can be used at different tasks of Case-Based Reasoning (CBR) systems, such as representing the input problem, enhancing similarity assessments, case representation, case abstraction, and case adaptation (Prentzas and Hatzilygeroudis 2008). Some examples of ontological-based similarity retrieval applications can be found in (Fernandez et al. 2011; Qin et al. 2016). The knowledge represented in OMSSA can be used to develop a smart system that can deal with the management of maintenance strategies, selecting the strategy to address different failure modes of an item, and assessing over time the efficiency and accuracy of the selected strategy. The creation of such reasoning among the OMSSA classes is out of the scope of the current article. As mentioned, OMSSA is part of a bigger research project in knowledge reuse for maintenance decision support systems. An extended version of OMSSA has already been used to support a DSS that uses CBR principles to select the suitable model or algorithm to implement predictive maintenance strategies given a specific use case (Montero Jiménez et al. 2021); OMSSA plays an important role in the semantic similarity computation which is needed for the CBR retrieve engine. This also validates the applicability of OMSSA for practical

## This article has been published in the Journal of Intelligent Manufacturing

implementations, not only supporting the maintenance strategy selection but also helping in the implementation of advanced strategies oriented to perform accurate diagnostics and prognostics of productive assets.

The structured methodology followed to develop OMSSA allows its alignment to other BFO-compliant ontologies, such as for example, those that are currently under development by the Industry Ontology Foundry. It is important to point out that ontologies evolve over time as knowledge in the different domains also evolves. The structured method used to develop OMSSA helps in the traceability of classes and relations, facilitating its future maintenance and update.

## Conclusion and future work perspectives

The present study has considered the most important terms and the semantic relations among them in the maintenance strategy domain. All these terms and relations were used to build an ontological model called OMSSA (Ontology model for Maintenance Strategy Selection and Assessment) using the methodology "Ontology Development 101". OMSSA is aligned to a top-level ontology (BFO) through some mid-level domain neutral ontologies (CCO). This alignment allows OMSSA to comply with standardized ontology development practices, which facilitates its future reuse. The ontology model was verified using semantic reasoners to prove its consistency among the different terms.

A concept of the implementation of OMSSA for practical applications was proposed. OMSSA aims to be instantiated with data from FMECA, cost-benefit-risk analysis reports, CMMS, among other types of engineering data sources, to provide enough information that can be used in maintenance strategy selection and assessment. OMSSA validation was performed using information from FMECA of an air compressor to instantiate some of the OMSSA classes. Using the competency questions as a guideline to perform some SPARQL queries on the knowledge base allowed to retrieve information and answer the questions as experts in the field would do. The classes and relations modeled in OMSSA provide an overview of the knowledge around maintenance strategies that was not fully covered before. Instantiated OMSSA can be used as a terminology framework for the creation of smart decision support systems in the domain of maintenance strategies. For example, these smart DSS could emulate the experts' reasoning by implementing rules or cases extracted from the ontology to assign maintenance strategies, assess the assigned ones, and justify the implementation of more advanced strategies based on accurate diagnosis and prognosis.

As part of the perspective of future work, a comparison can be performed between the smart agents developed with OMSSA for maintenance strategy selection and established methodologies such as Multi-Criteria Decision Making Methods (MCDM). OMSSA can also be extended and used as a reference ontology for a more specific ontology of predictive maintenance systems design. This terminology framework can serve as a protocol for a smart decision support system for the design of predictive maintenance systems.

## Acknowledgments

The authors want to acknowledge the contribution of M.Eng. Carlos Piedra Santamaria from Tecnológico de Costa Rica for providing the FMECA analysis applied on the air compressor that was used as a case study for OMSSA validation.

## Conflict of interest

Juan José Montero Jiménez, Bernard Grabot, Rob Vingerhoeds and Sebastien Schwartz declare no conflict of interest for the current study.

## OMSSA repository

OMSSA can be accessed by the following link: https://github.com/jjmj128/OMSSA

## References

Antoniou, G., Groth, P., Harmelen, F. van, & Hoekstra, R. (2012). A Semantic Web Primer. The MIT Press (Third edit.). MIT Press.

Arp, R., Smith, B., & Spear, A. D. (2016). Building Ontologies with Basic Formal Ontology. Building Ontologies with Basic Formal Ontology. https://doi.org/10.7551/mitpress/9780262527811.001.0001

Cao, Q., Zanni-Merk, C., & Reich, C. (2019). Towards a core ontology for condition monitoring. In Procedia Manufacturing. https://doi.org/10.1016/j.promfg.2018.12.029

Castaño, F., Haber, R. E., Mohammed, W. M., Nejman, M., Villalonga, A., & Martinez Lastra, J. L. (2020). Quality monitoring of complex manufacturing systems on the basis of model driven approach. Smart Structures and Systems, 26(4), 495-506. https://doi.org/10.12989/sss.2020.26.4.495

Emovon, I., Norman, R. A., & Murphy, A. J. (2018). Hybrid MCDM based methodology for selecting the optimum maintenance strategy for ship machinery systems. Journal of Intelligent Manufacturing, 29, 519-531. https://doi.org/10.1007/s10845-015-1133-6

European Committee for Standardization. (2017). CEN EN 13306: Maintenance-Maintenance terminology. European Committee for Standardization. ICS 01.040.03; 03.080.10.

Fernández, M., Cantador, I., López, V., Vallet, D., Castells, P., & Motta, E. (2011). Semantically enhanced Information Retrieval: An ontology-based approach. Journal of Web Semantics, 9(1), 434-452. https://doi.org/10.1016/j.websem.2010.11.003

Fernandez, M., Gómez-Perez, A., & Juristo, N. (1997). Methontology: from ontological art towards ontological engineering. In Proceedings of the AAAI97 Spring Symposium Series on Ontological Engineering.

Ferrer, B. R., Mohammed, W. M., Martinez Lastra, J. L., Villalonga, A., Beruvides, G., Castano, F., & Haber, R. E. (2018). Towards the Adoption of Cyber-Physical Systems of Systems Paradigm in Smart Manufacturing Environments. In Proceedings - IEEE 16th International Conference on Industrial Informatics, INDIN 2018. https://doi.org/10.1109/INDIN.2018.8472061

Foundry, T. O. (2020). Relation Ontology (RO). http://www.obofoundry.org/ontology/ro.html. Accessed 22 July 2020 Glimm, B., Horrocks, I., Motik, B., Stoilos, G., & Wang, Z. (2014). HermiT: An OWL 2 Reasoner. Journal of Automated Reasoning. https://doi.org/10.1007/s10817-014-9305-1

Gruber, T. R. (1993). A translation approach to portable ontology specifications. Knowledge Acquisition, 5(2), 199-220. https://doi.org/10.1006/knac.1993.1008

Grüninger, M., Fox, M. S., & Gruninger, M. (1995a). Methodology for the Design and Evaluation of Ontologies. In International Joint Conference on Artificial Intelligence (IJCAI95), Workshop on Basic Ontological Issues in Knowledge Sharing. https://doi.org/citeulike-article-id:1273832

Heravi, B. R., Lycett, M., & de Cesare, S. (2014). Ontology-based standards development: Application of OntoStanD to ebXML business process specification schema. International Journal of Accounting Information Systems, 15(3), 275-297. https://doi.org/10.1016/j.accinf.2014.01.005

Hodkiewicz, M., Lukens, S., Brundage, M. P., & Sexton, T. (2021). Rethinking Maintenance Terminology for an Industry 4.0 Future. International Journal of Prognostics and Health Management, 2021(1), 14.

https://www.phmsociety.org/node/2794. Accessed 1 March 2021

Horridge, M., & Bechhofer, S. (2011). The OWL API: A Java API for OWL ontologies. Semantic Web, 2(1), 11-21. https://doi.org/10.3233/SW-2011-0025

INCOSE. (2015). Systems Engineering Handbook. A guide for system life cycle processes and activities. Fourth Edition. Wiley.

International Electrotechnical Commission (IEC). (2018). IEC60812, Analysis techniques for system reliability- Procedure for failure mode and effects analysis (FMECA).

International Organization for Standardization (ISO). (1997). Information technology — Vocabulary — Part 14: Reliability, maintainability and availability.

International Organization for Standardization (ISO). (2003). ISO 13374-1:2003 Condition monitoring and diagnostics of machines Data processing, communication and presentation Part 1: General guidelines.

International Organization for Standardization (ISO). (2012a). ISO 13372 - Condition monitoring and diagnostics of machines - Vocabulary.

International Organization for Standardization (ISO). (2012b). ISO 13379-1:2012 - Condition monitoring and diagnostics of machines - Data interpretation and diagnostics techniques - Part 1: General guidelines.

International Organization for Standardization (ISO). (2020a). ISO/IEC 21838-1 Information technology - Top-level Ontologies (TLO) - Part 1: Requirements.

International Organization for Standardization (ISO). (2020b). ISO/IEC 21838-2 - Information technology - Top-level ontologies (TLO) - Part 2: Basic Formal Ontology (BFO).

IOF. (2020). Industrial Ontology Foundry. https://www.industrialontologies.org/?page_id=164. https://www.industrialontologies.org/?page_id=164. Accessed 6 October 2020

Kacprzynski, G. J., Roemer, M. J., & Hess, A. J. (2002). Health management system design: Development, simulation and cost/benefit optimization. In IEEE Aerospace Conference Proceedings. https://doi.org/10.1109/AERO.2002.1036148

Karray, M. H., Ameri, F., Hodkiewicz, M., & Louge, T. (2019). ROMAIN: Towards a BFO compliant reference ontology for industrial maintenance. Applied Ontology, 14(2), 155-177. https://doi.org/10.3233/AO-190208

Karray, M. H., Chebel-Morello, B., & Zerhouni, N. (2012). A formal ontology for industrial maintenance. Applied Ontology. https://doi.org/10.3233/AO-2012-0112

Keet, M. (2018). An Introduction to Ontology Engineering. Texts in computing Vol 20. ISBN 978-1-84890-295-4.

Keller, K., Simon, K., Stevens, E., Jensen, C., Smith, R., & Hooks, D. (2001). A process and tool for determining the cost/benefit of prognostic applications. In AUTOTESTCON (Proceedings). https://doi.org/10.1109/autest.2001.949432

Kothamasu, R., Huang, S. H., Verduin, W. H., Kothamasu, R., Huang, S. H., & Verduin, W. H. (2006). System health monitoring and prognostics -a review of current paradigms and practices. International Journal of Advanced Manufacturing Technology, 28(9), 1012-1024. https://doi.org/10.1007/978-1-84882-472-0_14

Lu, Y., Wang, H., & Xu, X. (2019). ManuService ontology: a product data model for service-oriented business interactions in a cloud manufacturing environment. Journal of Intelligent Manufacturing, 30, 317-334. https://doi.org/10.1007/s10845-016-1250-x

Lupp, D. P., Hodkiewicz, M., & Skjæveland, M. G. (2020). Template libraries for industrial asset maintenance: A methodology for scalable and maintainable ontologies. In CEUR Workshop Proceedings (Vol. 2757, pp. 49-6

March, S. T., & Smith, G. F. (1995). Design and natural science research on information technology. Decision Support Systems, 15, 251-266. https://doi.org/10.1016/0167-9236(94)00041-2

Matsokis, A., Karray, H. M., Chebel-Morello, B., & Kiritsis, D. (2010). An ontology-based model for providing Semantic Maintenance. In 1st IFAC Workshop on Advanced Maintenance Engineering, Services and Technology, Vol 43, Issue 3 (pp. 12-17). https://doi.org/10.3182/20100701-2-pt-4012.00004

MIMOSA. (2001). Open System Architecture for Condition-Based Maintenance (OSA-CBM). Available on http://www.mimosa.org/mimosa-osa-cbm/.

Montero Jimenez, J. J., Schwartz, S., Vingerhoeds, R., Grabot, B., & Salaun, M. (2020). Towards multi-model approaches to predictive maintenance: A systematic literature survey on diagnostics and prognostics. Journal of Manufacturing Systems, 56, 539-557. https://doi.org/10.1016/j.jmsy.2020.07.008

Montero Jimenez, J. J., & Vingerhoeds, R. (2018). Enhancing operational fault diagnosis by assessing multiple operational modes. In Proceedings - International Conference in Modelling, Optimization and Simulation MOSIM 2018, 27th 29th June (pp. 237-244). Toulouse, France: MOSIM2018.

Montero Jiménez, J. J., Vingerhoeds, R., & Grabot, B. (2021). Enhancing predictive maintenance architecture process by using ontology-enabled Case-Based Reasoning. In Proceedings - 7th IEEE International Symposium on System Engineering. Virtual: IEEE.

Moubray, J. (1997). RCM II: Reliability Centered Maintenance. Industrial Press.

Muñoz-Hernández, H., Montero-Jiménez, J. J., & Vingerhoeds, R. (2021). Integrating ontologies and case-based reasoning for the development of knowledge-intensive systems. In Proceedings - 35th European Simulation and

## This article has been published in the Journal of Intelligent Manufacturing

Modelling Conference. Accepted for publication.

Musen, M. A. (1992). Dimensions of knowledge sharing and reuse. Computers and Biomedical Research, 25(5), 435-467. https://doi.org/10.1016/0010-4809(92)90003-S

Noy, N. F., & McGuinness, D. L. (2001). Ontology Development 101: A Guide to Creating Your First Ontology. Stanford Knowledge Systems Laboratory. https://doi.org/10.1016/j.artmed.2004.01.014

Nuñez, D. L., & Borsato, M. (2017). An ontology-based model for prognostics and health management of machines. Journal of Industrial Information Integration, 6, 33-46. https://doi.org/10.1016/j.jii.2017.02.006

Nuñez, D. L., & Borsato, M. (2018). OntoProg: An ontology-based model for implementing Prognostics Health Management in mechanical machines. Advanced Engineering Informatics, 38, 746-759. https://doi.org/10.1016/j.aei.2018.10.006

Panov, P., Soldatova, L., & Dzeroski, S. (2014). Ontology of core data mining entities. Data Mining and Knowledge Discovery, 28, 1222-1265. https://doi.org/10.1007/s10618-014-0363-0

Prentzas, J., & Hatzilygeroudis, I. (2008). Combinations of case-based reasoning with other intelligent methods. In CEUR Workshop Proceedings. https://doi.org/10.3233/his-2009-0096

Protter, P. E. (2005). Stochastic Integration and Differential Equations, Second Edition. (B. Rozovski & M. Yor, Eds.). Springer.

Qin, F., Gao, S., Yang, X., Li, M., & Bai, J. (2016). An ontology-based semantic retrieval approach for heterogeneous 3D CAD models. Advanced Engineering Informatics, 30, 751-768. https://doi.org/10.1016/j.aei.2016.10.001

Raad, J., & Cruz, C. (2015). A survey on ontology evaluation methods. In IC3K 2015 - Proceedings of the 7th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management. https://doi.org/10.5220/0005591001790186

Ramasso, E., & Gouriveau, R. (2010). Prognostics in switching systems: Evidential Markovian classification of real-time neuro-fuzzy predictions. In 2010 Prognostics and System Health Management Conference, PHM '10. https://doi.org/10.1109/PHM.2010.5413442

Redmond, T. (2012). SPARQL Query tab for Protégé. Protégé wiki. https://protegewiki.stanford.edu/wiki/SPARQL_Query. Accessed 22 October 2020

Rodrigues, F. H., & Abel, M. (2019). What to consider about events: A survey on the ontology of occurrents. Applied Ontology, 14(4), 343-378. https://doi.org/10.3233/AO-190217

Rudnicki, R. (2020a). An Overview of the Common Core Ontologies 1.3. Buffalo, NY: National Institute of Standards and Technology (NIST). https://www.nist.gov/system/files/documents/2019/05/30/nist-ai-rfi-cubrc_inc_004.pdf

Rudnicki, R. (2020b). Common core ontologies. https://github.com/CommonCoreOntology/CommonCoreOntologies. Accessed 22 July 2020

Sanfilippo, E. M., Kitamura, Y., & Young, R. I. M. (2019). Formal ontologies in manufacturing. Applied Ontology, 14(2), 119-125. https://doi.org/10.3233/AO-190209

Saxena, A., Roychoudhury, I., & Celaya, J. R. (2010). Requirements Specifications for Prognostics : An Overview. In Proceedings of AIAA Infotech@Aerospace 2010. https://doi.org/10.2514/6.2010-3398

Smith, B., & Ceusters, W. (2015). Aboutness: Towards foundations for the information artifact ontology. In CEUR Workshop Proceedings.

Stanford University. (2020). Protégé website. https://protege.stanford.edu/. Accessed 22 July 2020

Steiner, C. M., & Albert, D. (2017). Validating domain ontologies: A methodology exemplified for concept maps. Cogent Education, 4(1). https://doi.org/10.1080/2331186X.2016.1263006

Talhi, A., Fortineau, V., Huet, J. C., & Lamouri, S. (2019). Ontology for cloud manufacturing based Product Lifecycle Management. Journal of Intelligent Manufacturing, 30, 2171-2192. https://doi.org/10.1007/s10845-017-1376-5

Zhou, A., Yu, D., & Zhang, W. (2015). A research on intelligent fault diagnosis of wind turbines based on ontology and FMECA. Advanced Engineering Informatics, 29(1), 115-125. https://doi.org/10.1016/j.aei.2014.10.001

<div align="center">

# This article has been published in the Journal of Intelligent Manufacturing

</div>

<div align="center">

Appendix. Relations used in OMSSA

</div>

<table border="1"><tr><td>Relation</td><td>Definition</td><td>Representation</td></tr><tr><td>is a</td><td>Entity A is an entity B means that A is subclass of B.</td><td></td></tr><tr><td>RO: bearer of</td><td>A relation between an independent continuant (the bearer) and a specifically dependent continuant (the dependent), in which the dependent specifically depends on the bearer for its existence.</td><td>bearerOf</td></tr><tr><td>RO: has quality</td><td>For types E and Q where E is a type of Entity and Q is a type of Quality, E has quality Q if and only if for every instance e of E there is some instance q of Q such that e has quality q. Here has quality denotes the primitive instance level relation. Inverse of quality of.</td><td>hasQuality</td></tr><tr><td>CCO: is about</td><td>A primitive (i.e. undefined) relationship between an information entity and some entity.</td><td>inAbout</td></tr><tr><td>CCO: is subject of</td><td>The inverse of is about, which relates an Entity to some Information Content Entity.</td><td>isSubjectOf</td></tr><tr><td>OMSSA: is subject failure effect</td><td>A CCO: is_subject_of_sub-property to define the relationship between a failure mode and a failure event</td><td>isSubjectOf</td></tr><tr><td>OMSSA: is subject of failure likeliness</td><td>A CCO: is_subject_of_sub-property to define the relationship between a failure mode and its likeliness to happen</td><td>isSubjectOf</td></tr><tr><td>RO: prescribes</td><td>For all classes T1 and T2, if T1 prescribes T2, then there is some instance of T1, t1, that serves as a rule or guide to some instance of T2, t2 (if T2 is a type of BFO: occurrent) or that serves as a model for some instance of T2, t2 (if T2 is a type of BFO: continuant).</td><td>prescribes</td></tr><tr><td>OMSSA: prescribes implementation risk</td><td>A RO: prescribes sub-property to define the relationship between a technical project plan and its implementation risk</td><td>prescribes</td></tr><tr><td>OMSSA: prescribes implementation benefit</td><td>A RO: prescribes sub-property to define the relationship between a technical project plan and its implementation benefit</td><td>prescribes</td></tr><tr><td>OMSSA: prescribes implementation cost</td><td>A RO: prescribes sub-property to define the relationship between a technical project plan and its implementation cost</td><td>prescribes</td></tr><tr><td>RO: describes</td><td>For all classes T1 and T2, if T1 describes T2 then there is some instance of T1, t1 that presents the characteristics by which some instance of T2, t2 can be recognized or visualized.</td><td>describes</td></tr><tr><td>RO: has output</td><td>A relation between a processual entity and a Continuant such that the presence of the Continuant at the end of the processual entity is a necessary condition for the completion of the processual entity.</td><td>hasOutput</td></tr><tr><td>RO: is input of</td><td>Inverse of has input, a relation between a processual entity and a Continuant such that the presence of the Continuant at the beginning of the processual entity is a necessary condition for the start of the processual entity.</td><td>isInputOf</td></tr><tr><td>RO: has part</td><td>A core relation that holds between a whole and its part.</td><td>hasPart</td></tr><tr><td>OMSSA: has action specification</td><td>A RO: has_part_sub-property the represents a relation between a maintenance strategy and its maintenance action specification</td><td>hasPart</td></tr><tr><td>OMSSA: has triggering specification</td><td>A RO: has_part_sub-property the represents a relation between a maintenance strategy and its triggering event specification</td><td>hasPart</td></tr><tr><td>RO: has function</td><td>A relation between an independent continuant (the bearer) and a function, in which the function specifically depends on the bearer for its existence.</td><td>hasFunction</td></tr><tr><td>RO: precedes</td><td>A relation between two occurrents. Occurrent x precedes occurrent y if and only if the time point at which x ends is before or equivalent to the time point at which y starts.</td><td>preceeds</td></tr><tr><td>RO: participates in</td><td>A relation between a continuant and a process, in which the continuant is somehow involved in the process.</td><td>participatesIn</td></tr></table>

## 4.4 Terminology framework for predictive maintenance components selection

The previous section explained the development of an Ontology Model for Maintenance Strategy Selection and Assessment (OMSSA). Once a specific strategy is selected, an important work remains to be done for the strategy implementation, especially for advanced strategies based on accurate diagnosis and prognosis. If a predictive maintenance strategy is selected to address a specific system of interest, several decisions remain to be made to select the suitable components of the predictive maintenance system that will address the selected strategy.

This section expands the scope of OMSSA to incorporate the vocabulary framework that can be used for the selection of suitable components for new predictive maintenance systems. The expanded ontology reuses several classes, relations and axioms from OMSSA, and is referred to as Ontology for Predictive Maintenance Architecture and Design (OPMAD). Figure 4.3 summarizes the import structure for OPMAD. The Basic Formal Ontology (BFO) is used as top-level ontology and the Common Core Ontologies (CCO) are used as mid-level ontologies. BFO and CCO provide a set of domain-neutral classes that facilitate future reuse and integration of ontologies using the same structure. OPMAD also imports some classes from ROMAIN [Kar+19] as it served as domain reference ontology for OMSSA.


> **Figure Description:**

This diagram is a flowchart illustrating a sequence of relationships between six distinct components, each represented by a rounded rectangle containing a text label. The flow begins at the leftmost component, labeled "BFO," which is connected by a rightward-pointing arrow to the component labeled "CCO." From the "CCO" component, the flow branches into two separate paths: one arrow points upward and to the right toward the "ROMAIN" component, and another arrow points downward and to the right toward the "OMSSA" component. A vertical arrow connects the "ROMAIN" component to the "OMSSA" component, indicating a downward flow between them. Finally, an arrow extends from the "OMSSA" component to the right, connecting it to the final component labeled "OPMAD."



<div align="center">

Figure 4.3: OPMAD import structure

</div>

## 4.4.1 OPMAD scope

OPMAD aims to support the DSS for component selection of new predictive maintenance systems. It follows the same development methodology as OMSSA. To delimit the scope of the ontology, the following competency questions have been considered:

- What are the functions of a predictive maintenance system?

- What models have been used to fulfil each function of the system?

- What are the maintainable systems on which predictive maintenance has been implemented?

- For a given situation, is the predictive maintenance system implemented online or offline?

- What performance indicators have been used to assess a model that fulfils a predictive maintenance function?

- What data is analyzed by the predictive maintenance models?

- Given multi-model approaches, what is the models' configuration in the system?

- In which reference is the predictive maintenance implementation documented?

## 4.4.2 OPMAD terms and relations

Figure 4.4 presents the most important classes and relations in OPMAD. For layout purposes, the sub-classes are not shown in the figure; the full list of OPMAD classes can be found in Table 4.1. The acronym PdM is used for predictive maintenance in the figure. As the objective of OPMAD is to support the DSS to identify suitable models for predictive maintenance systems, the explanation for the ontology classes and their relations starts from the class Predictive Maintenance Model, and is based on the terms and relations presented in Figure 4.4. It is important to point out that the relations are adopted from BFO and CCO to comply with the upper level ontologies. A Predictive Maintenance Model is carried in a Predictive Maintenance Module which is a component of a Predictive Maintenance System. Each Predictive Maintenance Module has a Predictive Maintenance Function; this research is focused on diagnostics and prognostics functions.

The predictive maintenance model embedded in the module is directly linked to a Maintainable item which is the class that describes the technical maintainable system for which the predictive maintenance system is developed. The Maintainable item is classified by the class Maintainable item type which was added for similarity computation purposes in the DSS; this type of classes help to compare the new problem to be addressed with the solved problem in a case base of a CBR system. Maintainable items belonging to the same type share important degradation characteristics and thus the same predictive maintenance models can be proposed to solve the same predictive maintenance functions.

The Maintainable item has its own Function which is affected by a Failure that manifests itself through a Failure Mode. A Maintainable item has one or several failure modes which are also subject of the Predictive Maintenance Model. The predictive maintenance model has as input the Condition Data which is used to perform diagnostics and prognostics. Two important qualities for the implementation of a predictive maintenance model is its type and configuration. The Predictive Maintenance Model Type will classify the model within the families of knowledge-based, data-driven and physics-based models. This model type classification helps for similarity and preferences purposes in the DSS.

The Predictive Maintenance Model Configuration shows if a model should be complemented by other models to fulfil its function; the use of multiples models can improve performance but it increases development complexity. The Predictive Maintenance Module is qualified by the Synchronization and the Performance indicator. These two qualities provide useful information on how the predictive maintenance models embedded in the modules should be tested and synchronized with the Maintainable item.

All this information on predictive maintenance models, maintainable items, their failure models, etc, is gathered in Predictive Maintenance Case which is documented and published through a Predictive Maintenance Article, a special type of Article that is focused on predictive maintenance. From these predictive maintenance articles, some bibliometric indicators are also included in the ontology to be used in the CBR system. These bibliometric indicators are provided as solution attributes so that the engineer can easily find the information source of a specific case. The Predictive Maintenance Article Title, Predictive Maintenance Article Identifier and Predictive Maintenance Article Publication Year can be used for similarity purposes and/or as information source for further details of the predictive maintenance models and their implementation.


> **Figure Description:**

This diagram is a conceptual ontology or entity-relationship map illustrating the components and relationships within a Predictive Maintenance (PdM) system. The central node is the "PdM Module," which is a part of the "PdM System" and possesses a "PdM Module function." The "PdM Module" also "isCarrierOf" a "PdM Model," which "IsAbout" a "Maintainable item." The "PdM Module" has two "Synchronization" relationships (one labeled "hasQuality"). The "PdM Model" has a "hasConfiguration" relationship with "PdM Model configuration" and a "hasType" relationship with "PdM Model type," while also having a "hasInput" relationship with "Condition Data."

The "Maintainable item" is central to the lower half of the diagram. It has a "hasType" relationship with "Maintainable item type," a "hasCaseStudy" relationship with "PdM Case," and a "hasFailureMode" relationship with "Failure Mode." The "Maintainable item" also has a "hasFunction" relationship with "Function." The "PdM Module function" is linked to "Function" via an "is a" relationship. "Failure Mode" "describes" a "Failure," and "Failure" is linked to "Function" via an "isAffectedBy" relationship.

"Condition Data" has a "hasType" relationship with "Condition Data Type." At the bottom, "PdM Case" is linked to "PdM Article" via an "isCarrierOf" relationship. "PdM Article" is the subject of "IsAbout" relationships originating from "PdM Article title," "PdM Article identifier," and "PdM Article Publication year." All relationships are represented by directed arrows with italicized labels indicating the nature of the connection between the rectangular entity boxes.



<div align="center">

Figure 4.4: Classes and relations in OPMAD

</div>

<div align="center">

Table 4.1: Terms of the Ontology for Predictive Maintenance Architecture and Design.

</div>

<table border="1"><tr><td colspan="4">Begin of Table 4.1</td></tr><tr><td>Class</td><td>Sub-class of</td><td>Definition</td><td>Source</td></tr><tr><td>Article identifier</td><td>CCO: Artifact identifier</td><td>An Artifact Identifier entity that designates some article</td><td>Based on CCO: Artifact identifier definition</td></tr><tr><td>Article title</td><td>CCO: Designative name</td><td>A Designative Name for some article</td><td>Based on CCO: Designative name definition</td></tr><tr><td>BFO: Function</td><td>BFO: Disposition</td><td>See BFO definition</td><td>BFO</td></tr><tr><td>Case</td><td>CCO: Designative name</td><td>A designative information content entity that designates a name to a case in a case base.</td><td>Based on CCO: Journal Article and the case definition for Case-Based Reasoning</td></tr><tr><td>Case-base</td><td>CCO: Information bearing artifact</td><td>An information Bearing Artifact that is designed to bear a set of cases for case-based reasoning. A CCO: Database subclass</td><td>Based on CCO: Journal Article and the case-base definition for Case-Based Reasoning</td></tr></table>

<table border="1"><tr><td colspan="4">Continuation of Table 4.1</td></tr><tr><td>Class</td><td>Sub-class of</td><td>Definition</td><td>Source</td></tr><tr><td>CCO: Artifact</td><td>BFO: Independent continuant</td><td>See CCO definition</td><td>CCO [Rud20a]; [Rud20b]</td></tr><tr><td>Data variable</td><td>CCO: Descriptive ICE</td><td>A descriptive information content entity that describes the variable in the maintainable item data</td><td>Domain-specific definition</td></tr><tr><td>Design detail</td><td>BFO: quality</td><td></td><td>Domain specific definition</td></tr><tr><td>Failure mode</td><td>CCO: Descriptive ICE</td><td>Manner in which a failure occurs</td><td>IEC 60812:2018</td></tr><tr><td>Fault detection</td><td>OPMAD: Predictive maintenance module function</td><td>A function whose purpose is the search of faults by assessing some Maintainable item parameters</td><td>Domain-specific definition [MV19]; [MIM01]</td></tr><tr><td>Fault feature extraction</td><td>OPMAD: Predictive maintenance module function</td><td>A function whose purpose is the identification of symptoms that correspond to a specific fault</td><td>Domain specific definition [MV19]; [MIM01]</td></tr><tr><td>Fault identification</td><td>OPMAD: Predictive maintenance module function</td><td>A function whose purpose is the comparison of the symptoms against known criteria to identify a specific fault</td><td>[MV19]; [MIM01]</td></tr><tr><td>Future state forecast</td><td>OPMAD: Predictive maintenance module function</td><td>A function whose purpose is the forecast of the condition for the next cycle operational cycle based on the current state of the maintainable item</td><td>Domain-specific definition [MV19]; [MIM01]</td></tr><tr><td>Health assessment</td><td>OPMAD: Predictive maintenance module function</td><td>A function whose purpose is to rate the current condition of a maintainable item against a predefined scale</td><td>Domain-specific definition [MV19]; [MIM01]</td></tr><tr><td>Health modelling</td><td>OPMAD: Predictive maintenance module function</td><td>A function whose purpose is to establish a scale to rate the condition of a maintainable item</td><td>Domain-specific definition [MV19]; [MIM01]</td></tr><tr><td>Maintainable item data</td><td>CCO: Information bearing artifact</td><td>An information Bearing Artifact that is designed to bear information from the maintainable item that can be used for predictive maintenance</td><td>Domain-specific definition</td></tr><tr><td>Item type</td><td>CCO: Descriptive ICE</td><td>A descriptive information content entity that describes the family of an item from the predictive maintenance perspective</td><td>Domain-specific definition</td></tr><tr><td>Maintainable item</td><td>BFO: Independent continuant</td><td>Subject being considered for maintenance</td><td>IEC 60812:2018 [Int18]</td></tr></table>

<table border="1"><tr><td>Class</td><td>Sub-class of</td><td>Definition</td><td>Source</td></tr><tr><td>Model type</td><td>CCO: Descriptive ICE</td><td>A descriptive information content entity that describes the family of an item from the predictive maintenance perspective</td><td>Domain-specific definition</td></tr><tr><td>Models configuration</td><td>CCO: Descriptive ICE</td><td>An arrangement of models in a predictive maintenance module</td><td>Based on Oxford definition of configuration. Adapted for predictive maintenance models applications</td></tr><tr><td>Module synchronization</td><td>BFO: quality</td><td>A quality of a predictive maintenance module with regards the operation synchronization with the Maintainable item</td><td>Domain-specific definition</td></tr><tr><td>Number of input variables</td><td>BFO: quality</td><td>A quality that states the number of input variables that are used in a predictive maintenance model for a specific item in a predictive maintenance case.</td><td>Domain-specific definition</td></tr><tr><td>Number of failure modes</td><td>BFO: quality</td><td>A quality that states the number of failures modes that are known from a maintainable item</td><td>Domain-specific definition</td></tr><tr><td>Performance indicator</td><td>CCO: Descriptive ICE</td><td>A Directive Information Content Entity that describes the way to measure the performance of a predictive maintenance module</td><td>Domain-specific definition</td></tr><tr><td>Performance value</td><td>CCO: Descriptive ICE</td><td>A numerical or string value to rate the quality Performance indicator</td><td>Domain-specific definition</td></tr><tr><td>Predictive Maintenance Article</td><td>CCO: Information bearing artifact</td><td>An Information Bearing Artifact that is designed to bear a specific brief composition on predictive maintenance topic as part of a Journal Issue or conference proceedings</td><td>Based on CCO: Journal Article definition</td></tr><tr><td>Predictive maintenance Model</td><td>CCO: Directive ICE</td><td>A Directive Information Content Entity that consist of a set of propositions for predictive maintenance purposes</td><td>Based on CCO: Directive Information Content Entity definition adapted to the context of predictive maintenance</td></tr><tr><td>Predictive maintenance module</td><td>CCO: Information processing artifact</td><td>A component of a predictive maintenance system that fulfils one specific function</td><td>Domain-specific definition</td></tr><tr><td>Predictive maintenance module function</td><td>BFO: function</td><td>An realizable entity that is the purpose of a predictive maintenance module</td><td>Derived from BFO: function definition</td></tr><tr><td>Predictive maintenance system</td><td>CCO: Information processing artifact</td><td>A set of components that work together for predictive maintenance purposes</td><td>Domain-specific definition</td></tr></table>

<table border="1"><tr><td colspan="4">Continuation of Table 4.1</td></tr><tr><td>Class</td><td>Sub-class of</td><td>Definition</td><td>Source</td></tr><tr><td>Publication year</td><td>CCO: Descriptive ICE</td><td>A integer value that represents the Gregorian year in which an article was published</td><td>Domain-specific definition</td></tr><tr><td>Remaining useful life estimation</td><td>OPMAD: Predictive maintenance module function</td><td>A function whose purpose is the forecast of the remaining operational life based on the current state of the maintainable item</td><td>Domain-specific definition</td></tr><tr><td colspan="4">End of Table 4.1</td></tr></table>

## 4.4.3 OPMAD instantiation

The last step in ontology development is its instantiation. It consists of including individuals in the ontology classes. An instantiated ontology can be seen as a knowledge base of a specific knowledge domain. In the context of the current research, a knowledge base built from OPMAD will contain the data of successful implementations of predictive maintenance systems. The developed knowledge base is in fact the case base that is going to be used for the DSS. OPMAD has been populated with information coming from the publications considered in a recent structured literature survey about predictive maintenance [Mon+20]. Articles analysis and instantiation are manual processes. These tasks demand a deep understanding of the predictive maintenance domain as the vocabulary in the articles is very heterogeneous and not always standardized. Further explanation on how the different classes were instantiated and their purpose for the CBR system is provided in Chapter 5 as part of the case structure definition and case base creation.

## 4.5 Lessons learnt

This chapter addressed the creation of ontologies in the field of maintenance strategies, giving special attention to predictive maintenance solutions and their design. The chapter explained the principles of ontologies, the state-of-the-art and best practices for their development. The developed ontologies use the Basic Formal Ontology (BFO) as top-level ontology and the Common Core Ontologies (CCO) as mid-level ontologies. The Ontology Development 101 methodology was selected to carry out the ontologies creation. An Ontology model for Maintenance Strategy Selection and Assessment (OMSSA) has been created as a terminology framework for maintenance strategies. An extension to OMSSA, the Ontology for Predictive Maintenance Architecture and Design (OPMAD) was proposed as the terminology framework for the proposed knowledge reuse framework to select predictive maintenance models. Both ontologies have been created using the Protégé ontology editor and their consistency has been tested using the Hermit reasoner embedded in the editor. Further explanations about the integration of the ontology and the CBR system can be found in the next chapter. The developed ontologies aim at storing the case base and provide the ontological semantic similarity for some of the case attributes. The creation of the ontology is itself a contribution of the current thesis as it can be reused in other industrial applications

Intentionally left blank

<div align="center">

# Case-based Reasoning systems development

</div>

"Bad reasoning, as well as good reasoning, is possible; and this fact is the foundation of practical side of logic."

Charles Sanders Pierce

Content

5.1 Reasoning considering the past experiences 81

5.2 The case-based reasoning paradigm 81

5.2.1 Case-based reasoning cycle 82

5.2.2 MyCBR introduction: workbench and SDK 84

5.3 Development of the retrieval engine for predictive maintenance components selection 87

5.3.1 Case representation 87

5.3.2 Similarity assessment 93

5.3.3 Retrieval engine user interface 95

5.4 Lessons learnt 95

## 5.1 Reasoning considering the past experiences

Case-Based Reasoning (CBR) is a paradigm that leverages past problem-solving experience, in form of concrete solving cases, when it comes to solving new problems [RS89]; [Kol93]. Case-based reasoning was briefly introduced in Chapter 2. It is used by case-based models which are part of the knowledge-based models family. Case-based reasoning has a vast field of applications spanning from medical to industrial applications; CBR has been used to benefit from previous experiences (cases) that have been solved in the past. In the current thesis framework, CBR is implemented to retrieve possible components (models) that can be used in predictive maintenance systems. This section provides further insights into CBR, its phases and its characteristics.

## 5.2 The case-based reasoning paradigm

Case-based reasoning is a memory-based artificial intelligence solving methodology [De +05]. Case-Based reasoning was developed under the philosophy that human beings think and reason using analogies and

examples, rather than IF-THEN structures, the latter forming the basis for rule-based reasoning. A good example can be seen in the way a mechanic solves a problem with a car. If for example a mechanic is confronted with a car that does not accelerate properly, they remind of several comparable previous problems. The mechanic might recall previous similar situations, where for example brakes were clamping to the wheel or where the carburettor was not functioning optimally. It might be that the current situation reminds the mechanic of a problem with a chain wheel of a motorbike. Starting from this previous experience (knowledge), they can derive ideas for repairing the carburettor. From this earlier knowledge, the technician can deduce where and how to approach the problem, even though with the current type of car, they never actually encountered this problem.

Case-based reasoning tries to implement this way of reasoning. The following definition is used here:

Solve a new problem by remembering a previous similar situation and by reusing information and knowledge of that situation.

Case-based reasoning is therefore a paradigm in which specific knowledge of previously experienced problem situations is being used to solve a new problem. This is being done by finding similar previous cases and reusing previous experiences. In fact, it leads to a form of incremental, sustained learning, where information from new situations is kept for future use. The essence of case-based reasoning is that knowledge of previous experiences is represented in the form of "cases", instead of rules or constraints relations. A case is a declaration of a set of characteristic features, such as:

- the specific previously experienced problem situation,

- the previously applied solution,

- and sometimes also the procedure or method to obtain this solution.

In the example of the mechanic, 3 cases were mentioned. Features to represent the problem of a case are the bad acceleration, type of the vehicle and engine. The feature to describe the solution can have descriptions of the clamping brakes, the carburettor or the chain wheel respectively. Notice that the knowledge about the problem-solving process is implicitly available in the cases. No explicit relations, such as why the solutions were applied, are declared. New arising problems are declared in the occurring problem features, such as the bad acceleration. Cases with similar features as the occurring problem are searched, their solutions and methods are retrieved from the case-base and applied to the current problem.

## 5.2.1 Case-based reasoning cycle

Solving the problem is performed in a cyclic process of several steps: the CBR-cycle [AP94]. This cycle is composed of four phases: retrieve, reuse, revise and retain. Figure 5.1 shows the steps of the CBR cycle. This figure already shown in the Article 1, but it is recalled in this section to facilitate the CBR cycle explanations.

The CBR cycle is triggered when a new problem is encountered. This first phase aims at retrieving the most similar cases from a knowledge base that stores all previous cases. The target (new) case is compared to the existing cases in the knowledge base using different similarity measurements. The closest retrieved case is proposed as a possible solution in the reuse phase. Some adaptation might be needed to implement the solution in the target case. After suggesting and implementing the solution the revision phase takes place. If the suggested solution achieves to solve the problem, it is confirmed and in the last phase, it is retained in


> **Figure Description:**

This diagram illustrates the Case-Based Reasoning cycle, organized as a circular process with four main stages: RETRIEVE, REUSE, REVISE, and RETAIN. At the center of the cycle is a box labeled "General Knowledge" containing a stack of documents labeled "Previous cases."

The process begins at the top with a "Problem" input, which leads to a "New case" box. An arrow points from the "New case" into the "Previous cases" stack within the "General Knowledge" box. From the "Previous cases," an arrow points to a "Retrieved case" box, which is adjacent to another "New case" box. This "Retrieved case" flows into the "REUSE" stage, leading to a "Solved case" box. An arrow pointing out from the "Solved case" indicates a "Suggested Solution."

The cycle continues to the "REVISE" stage, where the "Solved case" connects to a "Tested/Repeated case" box. An arrow pointing out from the "Tested/Repeated case" indicates a "Confirmed Solution." This box then leads into the "RETAIN" stage, which connects to a "Learned case" box. An arrow points from the "Learned case" back into the "Previous cases" stack in the center. Double-headed arrows connect the "General Knowledge" center to each of the four stages (RETRIEVE, REUSE, REVISE, and RETAIN), indicating continuous interaction between the stages and the central knowledge base.



<div align="center">

Figure 5.1: Case-based reasoning cycle. Inspired on [AP94]

</div>

the knowledge base so that it can be reused in future similar problems. Further details of each CBR phase is provided in the following sub-sections.

## 5.2.1.1 Case retrieval

Traditionally the case retrieval is performed by the comparison of attributes from the target case and the stored cases in the case base. If the case is composed by different heterogeneous attributes, a decomposition of the similarity measures by attribute is often performed. Later, the global similarity is obtained by an amalgamation function that gives a weight value to each individual similarity. As [De +05] explains, similarity can be divided into surface similarity and structural similarity. For surface similarity, each case attribute is represented as a real number in [0,1] and the similarity is computed according to a similarity measure. Structured similarity deepens in the case similarity assessment by extensive use of the domain knowledge. It can be computationally expensive but more relevant cases can be retrieved.

Recent trends in case retrieval include not only similarity measures when identifying the most suitable case. Sometimes the closest case retrieved by similarity measures can be impossible to adapt to the new problem. One alternative is adaptation-guided retrieval. Here the assessment is not only oriented on how "similar" a case is but how "useful" it can be [Ber+01]. Another alternative to pure similarity-based retrieval is diversity-conscious retrieval. Very often, the most similar retrieved cases are very similar to one another and this may result in a limited offer of possible solutions to the CBR system user. Proposing a set of diverse similar cases can contribute to exploring the possible solutions to the problem, improving the traditional similarity-based case retrieval.

## 5.2.1.2 Case reuse

Now that a case has been selected to solve the problem, it has to be decided what part of the case can be re-used. This will depend on the differences between the retrieved case and the problem. Here as well, much domain knowledge is used. In particular, rule-based and model-based reasoning is used in this stage. Two ways of re-use of the solution can be seen:

- transformational reuse

- derivational reuse

Transformational reuse entails copying the solution described in the retrieved case. The solution can be adapted based on differences between the features of the problem and the retrieved case. The focus is on the equivalence of the solutions. This requires a strong domain-dependent model. Derivational reuse, in contrast, implies the reuse of the method or procedure used to construct the retrieved case to construct a new solution. This means that not the solution as such is copied, but the methodology behind the solution.

## 5.2.1.3 Case revision

At this stage, the solution is applied to the problem. From this, new information ((partial) success, failure, etc.) and new knowledge emerge. The results have to be evaluated, to see if a further adaptation of the solution is necessary to solve the problem. The differences between the expected results and the real results have to be explained and possible repairs or improvements to the solution have to be derived to really solve the problem.

## 5.2.1.4 Case retain

In the final stage of the CBR cycle, learning takes place. This learning entails remembering successful solutions as positive experiences and failing solutions as negative experiences. In this way, the system can benefit both in a positive and negative manner from its own behaviour. Case-based adjustment can be done automatically, but usually it is done offline with the help of human experts. Learning can be done by introducing new cases in the case base, explaining the new experience, fine-tuning existing case bases, based on new information and assigning importance to certain cases/features. In fact, learning is a "by-product" of problem-solving. Case-based reasoning offers an integrated problem solving and learning paradigm. New trends in artificial intelligence aim at automating this learning process by the incorporation of other models such as neural networks or rule-based systems. This automates the case-base maintenance, improving the case update, case addition and the elimination of obsolete cases.

## 5.2.2 MyCBR introduction: workbench and SDK

MyCBR is an open-source similarity-based retrieval tool for Case-Based Reasoning (CBR) [Alt+12]. It is a joint effort of the Competence Centre CBR at the German Research Center for Artificial Intelligence, and the School of Computing and Technology at the University of West London. MyCBR offers two possible options for CBR solutions. The first one is a stand-alone application called myCBR Workbench in which it is possible to model and test highly sophisticated, knowledge-intensive similarity measures in a friendly user interface. The second one is an open-source Software Development Kit (SDK). The SDK is written in Java and includes all classes and methods to develop CBR applications and integrate them into other systems. Projects created in the Workbench are easily modifiable and run using the SDK. MyCBR workbench can be used to fast prototype CBR retrieval tools that are later integrated with the SDK. The SDK is intended to integrate the CBR engines created wit MyCBR to Java or Android-based applications. Figure 5.2 shows the intended use of MyCBR workbench and MyCBR SDK. It is important to point out that some advanced capabilities such as string-based similarity functions are only available in the SDK and can not be prototyped in the workbench.