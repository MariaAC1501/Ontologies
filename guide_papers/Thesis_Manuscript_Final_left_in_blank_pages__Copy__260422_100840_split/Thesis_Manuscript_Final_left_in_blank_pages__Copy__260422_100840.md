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


## Continued from pages 101-200

When developing a CBR retrieval system using myCBR, the first step is determining the case attributes. Cases are represented by a coupled vector of attributes Case = [Problem attributes, Solution Attributes]. The problem attributes are used to measure the similarity of a target case and the cases in a case base. The solution attributes are stored as part of the solution information for the cases.

Once the attributes have been determined, the second step is the local similarity assignation to each problem attribute. MyCBR provides several options to compute similarity for each problem attribute. Within the available options, three similarity functions have been used for the current research:

1. Integer/Float similarity: this similarity function is used for numeric attributes. The similarity is obtained by a difference between a reference value and the input values of the function. A mathematical function is needed to define how the similarity decreases as the input values get further from the reference value. This mathematical function can be linear, exponential or determined by discrete points in the Cartesian plane. Figure 5.3 shows the procedure to edit simple integer similarity functions in MyCBR Workbench [Alt+12].

2. Symbol: this similarity measure is advisable for variables with a fixed set of options. These options are organized in a similarity matrix and some numerical values are given to establish the similarity among the options. Figure 5.4 presents a generic example of a symbol similarity matrix and how it is managed in MyCBR Workbench. This similarity function has been modified for some attributes in the current research to interact with the ontology model. The similarity matrix values are automatically obtained from the classes and relations of an ontology using feature-based similarity approach proposed by [San+12]. This feature-based similarity between two terms a and b is equal to 1 minus the normalized dissimilarity between a and b, as it is shown in equation 5.1.

$$
s i m _ {n o r m} (a, b) = 1 - \log_ {2} \left(1 + \frac {\left| \phi (a) \right\rangle \phi (b) | + \left| \phi (b) \right\rangle \phi (a) |}{\left| \phi (a) \right\rangle \phi (b) | + \left| \phi (b) \right\rangle \phi (a) | + \left| \phi (b) \cap \phi (a) \right|}\right)
$$

where $ |\phi (a)\backslash \phi (b)| $ are the features of a that are not present in b, $ |\phi (a)\backslash \phi (b)| $ are the features of b that are not present in a, and $ |\phi (b)\cap \phi (a)| $ are the features that both a and b have in common.

3. String: attributes similarity is obtained based on open text strings. Unlike the Symbol type attribute


> **Figure Description:**

This diagram illustrates the architecture of a Case-Based Reasoning (CBR) system, divided into three main components: the Workbench, the myCBR Project, and the SDK [API], which interacts with a Java- or Android-based Application. The Workbench is divided into three sections: "Modelling the domain" (containing Vocabulary/Attributes/Concepts, Similarity measures, and Adaptation knowledge), "Retrieval Engine" (for testing retrieval within the model), and "Case base editing" (for adding/removing cases, importing/exporting CSV/XML data, and creating/editing/optimising case bases). A yellow arrow labeled "testing retrieval" points upward from the retrieval engine to the domain model, while a green arrow labeled "optimisation" points downward from the domain model to the case base editing section.

The myCBR Project component consists of a "CBREngine" with a "[Model]" section, an "Explanation Knowledge" block, and a "Case base(s)" block. A green arrow labeled "Provide Model" connects the domain model to the CBREngine, and a yellow arrow labeled "Provide case base(s)" connects the case base editing section to the case base(s) block. Two curved red arrows indicate a bidirectional relationship between the "Explanation Knowledge" block in the engine and the "Explanation Knowledge" block associated with the case base.

The SDK [API] acts as an interface between the myCBR Project and the Application. It facilitates four primary interactions: a green arrow labeled "load/control a project" points toward the CBREngine, a red arrow labeled "post query" points toward the engine's explanation knowledge, a blue arrow labeled "retrieve cases" points away from the case base(s) toward the application, and a yellow arrow labeled "Load/control case bases" points toward the case base(s). The final component on the far right is a dark grey rectangle labeled "Java- or Android based Application."



<div align="center">

Figure 5.2: MyCBR platform description, [Alt+12]

</div>


> **Figure Description:**

This image is a screenshot of the myCBR software interface, specifically the "CCMSimple" modeling tab, annotated with explanatory text boxes. The main window displays a project tree on the left containing items like "Car," "Body," "CCM," "Car Code," "Color," "Doors," "Gas," "Manufacturer," "Miles," "Model," "Power," and "Price." Below this is a "Similarity Measures" panel listing "CCMSimple" and "CCMFunc." The central area shows the "Distance Function" configuration, where "asymmetric" is selected, and "quotient" is chosen. Two columns of radio buttons and input fields are present: the left column (case < query) has "Constant" (1.0), "Step at" (0), "Polynomial with" (1.0), and "Smooth-Step at" (0); the right column (case > query) has "Constant" (1.0), "Step at" (2500.0), "Polynomial with" (1.0), and "Smooth-Step at" (2500.0).

A graph at the bottom plots a "Function" (a red line) against an x-axis ranging from -5,000 to 5,000 and a y-axis from 0.00 to 1.00. The line starts at 0.00 at x = -5,000, rises linearly to 1.00 at x = 0, and remains at 1.00 from x = 0 to x = 5,000.

Annotations explain the interface features: "Symmetry allows you to choose to specify a symmetric or asymmetric function, choosing asymmetric activates the input for both sides of the function (C<Q and C>Q)"; "Difference calculates a numerical value for the difference between Q)uery and (C)ase values"; "Quotient calculates a quotient out of the (Q)uery and (C)ase values"; "Left side: The function specifies the similarity for (C)ase values lower than the (Q)uery value"; "Right side: The function specifies the similarity for (C)ase values higher than the (Q)uery value"; "Constant: Enter a value that the function will return as a constant"; "Modell a step in the function and the value at which it should occur"; "Modell the polynomial change of similarity with a basic value"; and "Modell a smooth step in the function at a given value."



<div align="center">

Figure 5.3: Simple integer similarity example, [Alt+12]

</div>

that has a certain number of categories, String type has only the restriction of having sentences or words as input. MyCBR offers three options to compute string-based similarity which are: Equality, Ngram and Levenshtein. For the current case study, the Levenshtein function was selected to compute the similarity string-based attributes. Levenshtein function offers a flexible means to compute similarity based on each character of the string [Lev66]. This is especially useful when there is a vast set of options that are unknown when building similarities. It also tolerates little orthographic errors from the user when typing the maintainable item of the target case. MyCBR offers string-based similarity only in its SDK; this similarity function is not yet available in MyCBR workbench.

The CBR system developed in this research was developed using the MyCBR SDK. The SDK was privileged over the Workbench for three main reasons:

1. String-based similarity functions are only available in the SDK.

2. The SDK provides access to modify the similarity functions. This allows the implementation of ontology-based similarity which is not originally included in MyCBR.

3. The SDK provides a flexible means to integrate the developed CBR retrieval solutions with other components of a Decisions Support System (DSS).

The complete development of the retrieval engine using the SDK and its integration with other parts of the DSS has been documented in a JavaDoc HTML and in the coding guide in Appendix C


> **Figure Description:**

This image is a screenshot of the myCBR software interface, annotated with explanatory text boxes. The interface shows a "Projects" panel on the left listing attributes for the concept "Car," including "Body," "CCM," "Car Code," "Color," "Doors," "Gas," "Manufacturer," "Miles," "Model," "Power," and "Price." The "Body" attribute is selected, and a "Similarity Measures" panel below shows "BodyFunc" is selected. The main window displays a similarity matrix table for "BodyFunc" with radio buttons for "Symmetry" (set to "symmetric") and "asymmetric."

The similarity matrix table contains the following rows and columns labeled "station_wagon," "roadster," "fastback," "sedan," "convertible," and "coupe." The values in the matrix are as follows: for "station_wagon," the values are 1.0, 0.0, 0.0, 0.8, 0.0, 0.5; for "roadster," 0.0, 1.0, 0.5, 0.0, 0.7, 0.0; for "fastback," 0.0, 0.5, 1.0, 0.0, 0.2, 0.2; for "sedan," 0.8, 0.0, 0.0, 1.0, 0.0, 0.7; for "convertible," 0.0, 0.7, 0.2, 0.0, 1.0, 0.0; and for "coupe," 0.5, 0.0, 0.2, 0.7, 0.0, 1.0.

Annotations explain that the table editor is used to describe the similarity mode table for slot type symbols, particularly when values cannot be ordered absolutely or hierarchically. It notes that choosing "symmetric" makes the matrix symmetric, while "asymmetric" makes it asymmetric. A red line highlights the diagonal of the matrix, with an annotation stating that this diagonal splits the symmetric or asymmetric halves of the matrix and that the colors of the fields serve as an optical aid to visualize the values. Additional annotations confirm that the attribute "Body" of the concept "Car" is selected and that the default auto-generated similarity measure for the attribute "body" is active.



<div align="center">

Figure 5.4: Symbol similarity matrix example, [Alt+12]

</div>

## 5.3 Development of the retrieval engine for predictive maintenance components selection

While the previous section provided the theoretical background of Case-Based Reasoning (CBR), this section explains the development of the retrieval engine for the predictive maintenance (PdM) component selection which is part of the DSS proposed in this thesis framework.

## 5.3.1 Case representation

"A case is a piece of knowledge in a particular context representing an experience that teaches an essential lesson to reach the goal of the reasoner" [Kol93]. Cases are often represented in a coupled form [problem, solution], in which similarities are applied on the "problem" part so that the "solution" part is retrieved. Case representation is composed of three main parts [BKP05]:

1. Defining the attributes of the case.

2. Defining the structure for the case content.

3. Organizing the case base.

## 5.3.1.1 Defining the attributes of the case

For the use case of predictive maintenance design, the cases are composed of three main attributes and some other complementary attributes. A case consists of a model that fulfils a specific predictive maintenance function on a determined system of interest. These three attributes are represented in OPMAD as:

- Predictive maintenance model: Every recorded case will have one or several models used to fulfil a specific Predictive maintenance function.

- Predictive maintenance module function: this attribute includes the function or functions that are fulfilled by predictive maintenance system for a specific maintainable item.

- Maintainable item: this class gathers the different machines, equipment, components or technological systems on which the model was applied and validated on each consulted article. The instances included in this class can match the subclasses of CCO: Artifact. The CCO: Artifact class and its subclasses structure were not directly reused to define the predictive maintenance case as CCO: Artifact has a more general purpose that goes beyond maintainable items.

Some complementary attributes have also been included to support the similarity assessment and the solution suggestion:

- Maintainable item type: the use case for the new predictive maintenance system may not be the same as the recorded implementations in the case base; however, they might share some similarities that could be considered to adjust a potential solution. Case studies may find some similarities if they are within the same "family" of applications as for example rotary machines or electronics devices.

- Condition data: This attribute gathers the instances that describe the inputs for a predictive maintenance model. Each model can be linked to several instances of the class condition data. For example, a neural network to fulfil a fault detection function of jet engines can have as condition data variables temperature, pressure, spinning speed, health index, reliability among others.

- Condition data type: this attribute aims helping in the similarity assessment. It is a complementary measure to Condition data class. It divides the condition data into different categories (see case base creation section).

- Predictive maintenance model type: this attribute aims at providing additional information to the proposed solution. It clusters the models into different categories (see case base creation section).

- Predictive maintenance model configuration: this attribute provides important information about the implementation of predictive maintenance models. It is part of the solution attributes.

- Module synchronization: this class aims at providing information of the synchronization between the Predictive maintenance module and the maintainable item. This is a problem attribute based on the structural requirements of a new predictive maintenance system. Online applications deal with real-time data which is constantly assessed to perform diagnostics or prognostics. Off-line applications gather information from an operative cycle to be assessed later. Online models normally are embedded in small control and monitoring boards with limited processing and storage memory while the offline application may be carried out by high-performance computers. Online scopes look for fast results in real time to trigger immediate actions in operation. Off-line scopes may target the maximum accuracy as there is more freedom in terms of time to perform the computations.

- Predictive maintenance article title: It is part of the solution attributes and its purpose is to provide traceability to a predictive maintenance case information source.

- Predictive maintenance article identifier: this attribute is intended to be part of the solution attributes of the case as it provides the traceability link to find the case information source. This source can be needed to find more detailed information about the case.

- predictive maintenance article publication year: this attribute is intended to be part of the similarity measures for the retrieval engine. Newer publications are privileged over older ones.

Some other attributes are part of the case but they are not intended to be part of the similarity assessment attributes or the solution suggestion. These attributes have been added for consistency in the ontology:

- Predictive maintenance system: this attribute aims at naming the system that has one of several predictive maintenance modules to fulfil one or several predictive maintenance functions on a Maintainable item.

- Predictive maintenance module: this attribute has been created to link the Predictive maintenance model with the Predictive maintenance model complying with BFO and CCO standards. The edges between these classes help compute some local similarities for the CBR system (see local similarities section).

- Predictive maintenance article: this attribute aims to be the link between the predictive maintenance case and information entities extracted from research articles such as predictive maintenance article title, predictive maintenance article identifier, and predictive maintenance article publication year.

## 5.3.1.2 Defining the structure for the case content

An extensive review on case representation techniques can be found in [ESE15]. The selection of the case representation is directly related to the similarity assessment that will be performed. Traditional methods for case representation include:

- Feature vector representation: this is the simplest representation of a case in which the cases are composed by a set of attributes that are used to describe the problem and the solution. The case retrieval is performed by the weighted sum of the similarities between the target case attributes and the cases in the case base. This case representation has limited capabilities to support semantic similarity as there is no representation of the knowledge domain.

- Frame-based representation: Frames provide a natural way for structured and concise knowledge representation. Frames are composed of different slots to organize knowledge. Each case is represented by a frame and each frame slot represents a case attribute. Frame-based representations have been (partially) formalized by description logic [BKP05]. The notion of "cases as terms" [Pla95] argues that viewing structured cases as terms in feature logics (a particular brand of description logics) helps in better understanding several aspects of case-based reasoning.

- Object-oriented representation: this case representation is suitable for complex case data structures. Cases are represented as a set of objects that have their own set of attributes.

- Textual representation: this case representation is suitable when cases are written in natural language texts. Specialized methods can be used to address these cases in an automated of semi-automated way.

- Hierarchical representation: In this approach, a case is represented at multiple levels of detail, possibly using multiple vocabularies. When solving a new problem, similar cases are retrieved from the case base at different levels of abstraction, their solutions are then combined and refined until achieving a final solution [BW96].

- Predicate-based representation: a predicate is a relation among objects, and it consists of a condition part and an action part, IF (condition) and THEN (action). Predicates that have no conditional part are facts. Cases can be represented as a collection of predicates [PS04]. The advantage of predicate representation is that it uses both rules and facts to represent a case, and it enables a case-based designer to build hybrid systems that are integrated rule/case-based [BKP05].

The above-mentioned case representation techniques have limitations in knowledge representation. They have few (if any) structures to describe the relations and constraints among the case features [BKP05]. Case representations using ontologies aims at solving this problem as ontologies provide not only the set of terms that constitute a case but also the relations among these attributes. Ontologies can be useful for designing knowledge-intensive CBR applications because they have powerful capabilities in knowledge acquisition, representation, and semantic understanding [GPH13]. Taking advantage of the created ontology for the current study, the case representation and structure is described using the proposed ontology in Chapter 4. Figure 4.4 showed the different attributes (classes in ontology) of the case represented in OPMAD. These ontology classes can be divided into two different groups: the problem attributes and the solution attributes:

- Problem Attributes = [PdM Function, Maintainable Item, Maintainable Item Type, Condition Data Type, Module synchronization, PdM Article Publication year]

- Solution Attributes = [PdM Model,PdM Model Configuration,PdM Model Type,Module Performance Indicator,PdM Article Identifier,PdM Article Title]

## 5.3.1.3 Organizing the case base

The case base corresponds to an instantiated version of OPMAD. The OPMAD structure provides the guidelines for the case base organization. The ontology has been populated using predictive maintenance cases retrieved from an extensive literature review about implemented predictive maintenance systems. The review presented in Chapter 2 was the starting point. An explanation of how the articles were consulted to instantiate OPMAD classes is presented hereafter:

1. Predictive maintenance case: the instances of this class are recorded in the form of "CaseN", where N is an integer value starting from 1 that denotes the order in which the cases have been recorded. A case of a paper is identified when three interrelated attributes are found: the Predictive maintenance function that is fulfilled by a predictive maintenance system, the Model that fulfils the function, and the Maintainable item for which the predictive maintenance system has been developed. In a single article, it is likely to find several cases because of different factors such as:

- There is a comparison of different models to fulfil the same PdM function. If several models are developed to fulfil the same PdM function, there is an instance in the database for each implemented model.

- There are different PdM functions addressed by different models. The study can address more than one PdM function in a single PdM system. If every function is addressed by a different model, there is an instance for each addressed function.

- A model that fulfils a PdM function has been implemented on different maintainable items. Some studies apply their approach to many case studies. An instance is recorded for each case study.

2. Predictive maintenance system: the instances of this class are named in the form of "SystemN", where N is a consecutive number according to the order in which the articles that explain these systems were consulted.

3. Predictive maintenance module: the instances of this class do not provide much information for the case retrieval or for the solution suggestion. These instances of Predictive maintenance module are named in the format of "ModuleN" where N is the case number it belongs to.

4. Predictive maintenance module function: the predictive maintenance functions can be clustered in eight different types (sub-classes). The instances receive the name of their subclass plus an integer number that records the order in which they were recorded. For example, instances of the sub-class Fault detection will be named as "faul detection1", "fault detection2", ..., "fault detection N", where N is the total number of instances of the sub-class Fault detection. The Predictive maintenance function sub-classes are:

4. 1. Features extraction: this PdM function identifies features from data that can be used for diagnostics or prognostics.

4. 2. Fault detection: this PdM function aims at detecting a faulty condition on a technical system given some symptoms.

4. 3. Fault identification/isolation: this PdM function allows to identify the source of the faulty condition when at least two faults present similar symptoms.

4. 4. Degradation modelling: a fault is not static; it evolves over time until it becomes a failure. This progression of the fault is usually called degradation. This PdM function aims at providing a representation of such degradation. Reliability and health indexes are some examples of values that can be used to model the degradation on maintainable items.

4. 5. Health assessment/degradation analysis: this PdM function aims at determining the current state of maintainable items based on a pre-existing degradation model.

4. 6. Next state forecasting: this PdM function aims at forecasting the health state of a maintainable item. It is a applicable when the life cycle of the maintainable item can be divided into discrete steps. This prognostics function aims at determining one-step-ahead or multiple-step-ahead if a failure is likely to happen.

4. 7. Remaining useful life (RUL) calculation: this PdM function aims at calculating the remaining work cycles the technical system or one of its components can work before failure.

5. Predictive maintenance model: the instances of this class are not limited by any type of restrictions. The instances of this class have been left as "open-text" as it is normal to find articles proposing new models that have been named by the article authors. Some of the instances in the Model class can be used in the future as subclasses in a more detailed version of OPMAD that has a more detailed level of instantiation.

6. Maintainable item: the instances of this class have been left as "open-text" as it is normal to find articles proposing new models that have been named by the article authors. Some of the instances in the Maintainable item class can be used in the future as subclasses in a more detailed version of OPMAD that has a more detailed level of instantiation.

7. Maintainable item type: the instances of this class aim at helping in the similarity measure between a target case and the cases in the case base. It is a complementary measure to Maintainable item class. The instances for this class have for the moment been limited to the following values:

(a) Rotary machines

(b) Reciprocating machines

(c) Electrical components

(d) Structures

(e) Energy cells and batteries

(f) Lubricants

8. Condition data: the instances of this class include all variables that are input for a Predictive maintenance model. The instances of this class can be found in different cases. Special attention must be paid to the instances of this class if one article includes more than one.

9. Predictive maintenance case: each case can have different data used as input for the predictive maintenance model. For example, there could be a model which aims to model degradation and later performs health assessment. For the first function, the model might use sensors data such as temperature and pressure. The output of the model would be a health index which is at the same time part of the inputs for the health assessment.

10. Condition data type: the instances of this class are limited to the following four options:

(a) Signals: direct measurements from the technical system sensors whose reads are signals. Signal processing models are usually needed to extract features that can be used for diagnostics and prognostics. These signals can come from different types of sensors, such as: temperature, vibrations, pressure, spinning speed among others.

(b) Time series (Discrete measurements or values): a single value is obtained to describe the state of input from the technical system at a specific work cycle. It can be obtained from sensors, models outputs or other data sources.

(c) Structured text-based: this type of variable is similar to time series. The data is recorded in discrete events, but the variables are text-based with a limited number of possible options for the instances. It allows an easier analysis.

(d) Text-based maintenance/operation logs: declared knowledge obtained from those who operate or maintain the technical system. Includes symptoms that are not measured by any other means but the human perception. Specialized techniques are needed to address natural language processing.

11. Predictive maintenance model type: it clusters the single-model approaches into three main instances: knowledge-based models, data-driven models and physics-based models. For multi-model approaches, there could be any combination of the proposed instances.

12. Predictive maintenance model configuration: the instances in this class provide information about the implementation of a Predictive maintenance model. In a first attempt, the instances are limited to two possible options: single model approach and multi-model approach. A more detailed analysis is possible by adding the specific configuration of the multi-model approaches as they can be implemented in parallel, in series, or embedded one in another [Mon+20].

13. Module synchronization: the instances of this class are limited to three possible options: "online", "off-line", and "not mentioned".

14. Module performance indicator: this class aims at storing the instances of performance indicators used to validate a model that fulfils a specific predictive maintenance function. For example, fault detection is usually assessed with the percentage of accurate detection, remaining useful life estimation is validated with a standard deviation of the results. More than one performance indicator can be included for each instance. No limited number of options are set for the instances in this class.

15. Predictive maintenance article: the instances of this class are named in the form of "Article N", where N is the consecutive number that keeps track of the order the articles were consulted. The instances of this class do not provide much information for the solution suggestion as the traceability to the case information source is done through the mentioned information entities of the article. However, its existence is justified for ontology consistency and compliance with BFO standards.

16. Predictive maintenance article title: the instances of these classes are strings that provide the article title given by its authors.

17. Predictive maintenance article identifier: the instances are strings that gather the alphanumeric code used as publication identifier; for example, the DOI, HAL Id, conference Id, among many other options. The DOI will be the privileged one if more than one ID is available.

18. Predictive maintenance article publication year: the instances of this class are recorded as integer values.

## 5.3.2 Similarity assessment

The similarity assessment is performed in two steps. First, a local similarity is performed for each of the problem attributes, and in the end, all these local similarities are consolidated in a single value called global similarity.

## 5.3.2.1 Local similarities

Once the case structure is defined for each problem attributes, a similarity measure must be assigned. Table 5.1 summarizes the problem attributes and the similarity functions that have been assigned to each of them. Seven attributes define the problem but the retrieval engine user is able to provide as input six of them. The PdM Article Publication year is automatically computed by the system. An integer similarity function based on discrete points has been assigned to the PdM Article Publication year. It provides a local similarity of 1 to cases that are 5 years old or less. For older cases, the similarity decreases linearly until it reaches the value of 0 at 40 years old. Cases older than 40 years will receive a local similarity of 0 for the PdM Article Publication year attribute.

<div align="center">

Table 5.1: Similarity functions assignation

</div>

<table border="1"><tr><td>Attribute</td><td>Similarity function</td></tr><tr><td>PdM Function</td><td>Symbol(Ontology)</td></tr><tr><td>Maintainable item</td><td>String(Levenshtein)</td></tr><tr><td>Maintainable item type</td><td>Symbol(Equality)</td></tr><tr><td>Condition Data</td><td>Symbol(Ontology)</td></tr><tr><td>Condition Data Type</td><td>Symbol(Equality)</td></tr><tr><td>Module synchronization</td><td>Symbol(Equality)</td></tr><tr><td>PdM Article Publication Year</td><td>Integer(Points function)</td></tr></table>

The attribute PdM function has been assigned with a symbol similarity function in MyCBR. The similarity matrix has been filled out using the feature-based ontological similarity presented in [San+12]. For this attribute the ontological similarity is computed based on the classes PdM model, PdM module, and PdM function of the ontology (see Figure 5.5). A PdM Module is linked to the PdM model by the relation isCarrierOf and at the same time is linked to the PdM function by the relation hasFunction. An inferred relation has been obtained between PdM model and PdM function. Using this inferred relation, the similarity is computed based on the models that have been used to fulfil a specific function. For example, a model such as Support Vector Machines (SVM) has been used in several cases for fault detection or fault identification; this increases the similarity between these two PdM functions.


> **Figure Description:**

The image is a diagram illustrating relationships between three entities: PdM Module, PdM Model, and PdM function. The PdM Module is positioned at the top center. A solid line extends from the left side of the PdM Module downward to the PdM Model, labeled with the text "isCarrierOf" along the vertical segment. A second solid line extends from the right side of the PdM Module downward to the PdM function, labeled with the text "hasFunction" along the vertical segment. A horizontal, dashed red arrow connects the PdM Model on the left to the PdM function on the right, with the text "InferredRelation" positioned below this dashed line.



<div align="center">

Figure 5.5: Classes and relations used to compute the ontological similarity for PdM function Similarly, the attribute condition data has been assigned with a symbol similarity function whose

</div>

matrix has been filled out using the feature-based ontological similarity presented in [Sán+12]. For this attribute, the similarity is built based on an inferred relation between PdM module and condition data (see Figure 5.6). A PdM module of a specific case can have a list of variables that define the condition data (several instances for each case). The user will enter the list of variables of the target case and there will be similarity assessment for each condition data variable against the corresponding lists in the stored cases of the case base. In the end, the local similarity is based on the amount of condition data variables that match between the target case and the stored cases. For example, a target case has the variables "temperature", and "pressure", the closest case in the case base has the variables "pressure", "temperature", and "spinning speed", the ontological similarity obtained with equation 5.1 would be approximately 0,70 as there is only one different element between each list. For this similarity function, an additional typo error tolerance has been added. The DSS user enters the condition data variables manually and a typo error is likely to happen. The similarity assessment among the variables is done using the Levenshtein distance [Lev66]. In the first attempt, a limit of two different characters has been selected for typo error tolerance. This means that if a user writes for example "tepmerature" instead of "temperature" the function is still able to perform the similarity assessment correctly.


> **Figure Description:**

This diagram illustrates the relationships between three entities: "PdM Module," "Maintainable item record," and "Condition data." The "PdM Module" is positioned at the bottom left, the "Maintainable item record" is at the top center, and the "Condition data" is at the bottom right. A solid black arrow originates from the "PdM Module" and points to the "Maintainable item record," labeled with the text "hasPart" above the horizontal segment of the line. A second solid black arrow originates from the "Maintainable item record" and points to the "Condition data," labeled with the text "isCarrierOf" above the horizontal segment of the line. Finally, a red dashed double-headed arrow connects the "PdM Module" directly to the "Condition data," with the text "InferredRelation" positioned below this connection.



<div align="center">

Figure 5.6: Classes and relations used to compute the ontological similarity for condition data

</div>

The attributes Maintainable item type, Condition Data Type, and Module synchronization have been assigned a symbol similarity function as provided by MyCBR. For each of these attributes, all the possible options are known and can be directly selected by the retrieval engine user. The equality in the symbol function means that the similarity is binary, if the user selects one option from the available ones for each of these attributes, there will be a local similarity equal to 1 to each case that has the same attribute value and 0 when the case has a different value. No partial similarity has been assigned among the options in the similarity matrix of the symbol function. This can be changed in the future as more relations from the ontology can be used to compute partial similarity among the attribute instances.

The attribute Maintainable item has been assigned with a string-based similarity function as provided by MyCBR. Levenshtein distance is used to compare a string entered by the retrieval engine user and the corresponding case attribute in the stored cases.

## 5.3.2.2 Global similarity: aggregation functions

After the similarity computation for each of the problem attributes, the combination of all these individual similarities in global similarity takes place. Each attribute has a weight and an amalgamation function calculates the final similarity based on local similarities and weights. The weights aim to give special importance to specific problem attributes. In a first attempt, all attributes get the weight of 1, meaning they have the same importance. MyCBR offers two different options to compute the global similarity: weighted sum and euclidean distance.

- Weighted sum: as the name says, is the sum of similarities considering the weight of each one. The equation 5.2 shows the calculation performed to find the global similarity.

$$
s i m _ {g l o b a l} = \sum_ {i = 1} ^ {n} w _ {i} \cdot s i m _ {i}
$$

The values of n, w and sim are respectively the numbers of variables, the weight and the similarity of variable i.

- Euclidean distance: the euclidean distance between two points in an euclidean space is a number, measuring the length of a line segment between the two points. In the scope of the project, the distance is equal to global similarities. The equation 5.3 shows the calculation performed to find the similarity.

$$
s i m _ {g l o b a l} = \sqrt {\sum_ {i = 1} ^ {n} w _ {i} \cdot s i m _ {i} ^ {2}}
$$

In the current research, both amalgamation functions can be used by the user. It is important to point out that to compute the global similarity, only the available attributes are considered. This means that if the architect counts only on two or three attributes out of the seven that describe the problem, the global similarity will be computed based on those two or three attributes.

## 5.3.3 Retrieval engine user interface

The retrieval engine developed with MyCBR is the core of the DSS for predictive maintenance component selection in this research framework. A Graphical User Interface (GUI) has been developed to help in the verification and validation of the system. Figure 5.7 shows the developed GUI for the developed retrieval engine.

It is important to recall that the CBR system development and the ontology development were done in parallel. The ontology classes that define the problem attributes received different names compared to those used for the CBR system variables. Table 5.2 shows the OPMAD classes and the corresponding names in the retrieval engine code. The distinction of these names has helped to avoid ambiguity in the code.

The GUI has a pull-down menu for those problem attributes with a fixed number of options. Free-text cells have been added for the problem attributes maintainable item and condition data. The weight for each problem attribute can be directly assigned in the GUI (by default these weights are equal to 1). In the GUI it is possible to selected how many cases to retrieve from the case base and the aggregation (amalgamation) function to compute the global similarity between the target case and the retrieved cases. The list of the most similar cases is shown in the white field just below the attributes that the user can modify. The user triggers the retrieval by clicking on the SUBMIT QUERY button at the bottom of the GUI.

## 5.4 Lessons learnt

This chapter addressed the creation of the CBR retrieval engine using the MyCBR platform. The principles of CBR have been introduced including the different phases of the CBR cycle. MyCBR is intended for the retrieval phase of CBR systems. The platform offers a stand-alone application called MyCBR workbench for fast prototyping of retrieval engines. MyCBR also offers an open-source System Development Kit (SDK)


> **Figure Description:**

This image is a software interface screenshot.

The image displays a graphical user interface titled "Predictive maintenance with CBR method - GUI 2." The interface is divided into sections for "Input variables" and "Additional inputs," each paired with a "Variable weights" column. Under "Input variables," there are six rows, each containing a label, a dropdown menu, and a weight field set to 1.0. The labels are "PdM function :", "Maintainable item type :", "Maintainable item :", "Condition data type :", "Module sychonization :", and "Condition data :". Under "Additional inputs," there is a field for "Number of cases to retrieve:" (currently blank) and a dropdown menu for "Aggregation function to use:" (currently set to "euclidean").

Below these inputs is a "User dialog" box containing the text: "Welcome to the myCBR Graphical User Interface ! * Input Variables : variables used in the query to retrieve and calculate similarities. - Predictive maintenance function, Maintainable item type, Module Synchronization, , Input type : Drop down list - Maintainable item : Free text - Condition data : Free text list separated by a coma. Example: (temperature, pressure, vibrations) * Additional inputs : inputs to complement the retrieval method. - Number of cases to retrieve : Integer number. - Aggregation function to use : Drop down list". At the very bottom of the window is a button labeled "SUBMIT QUERY."



<div align="center">

Figure 5.7: Retrieval engine Graphical User Interface (GUI)

</div>

<div align="center">

Table 5.2: OPMAD classes and corresponding variables in the retrieval engine

</div>

<table border="1"><tr><td>OPMAD class</td><td>CBR variable</td></tr><tr><td>PdM Function</td><td>Task</td></tr><tr><td>Maintainable item</td><td>Case study</td></tr><tr><td>Maintainable item type</td><td>Case study type</td></tr><tr><td>Condition Data</td><td>Input for the model</td></tr><tr><td>Condition Data Type</td><td>Input type</td></tr><tr><td>Module synchronization</td><td>Online/Off-line</td></tr><tr><td>PdM Article Publication Year</td><td>Publication year</td></tr></table>

that allows the integration of the retrieval engines with other systems in a Java-based environment. As the SDK has been selected over the workbench to develop the retrieval engine in this research as the SDK provides more capabilities than the workbench. The case structure and the case base have been defined using the OPMAD classes defined in Chapter 4. The case base corresponds to an instantiated version of OPMAD. The process to instantiate OPMAD from an extensive literature review includes the definition of the different variables to search and the possible options for each variable; this allows a better case base structure and facilitates the retrieval. For each problem attribute, a local similarity is selected among the possible options: integer, symbol, ontology-based, open text. Two different aggregation functions have been added to compute the global similarity between a target case and those cases stored in the case base. A GUI has been developed to facilitate the verification and validation of the retrieval engine.

The developed retrieval engine is the core of the DSS for the selection of predictive maintenance components. The next chapter is oriented on showing the complete framework of the ontology-enabled CBR system for the selection of predictive maintenance components. The verification and validation of the retrieval engine developed in this section are addressed in Chapters 6 and 7. Development details of the retrieval engine are provided in the code guide in Appendix C.

<div align="center">

# Building a framework for predictive maintenance models selection

</div>

Manufacturing is more than just putting parts together. It’s coming up with ideas, testing principles and perfecting the engineering as well as final assembly.”

James Dyson

Content

6.1 Making the parts work together 97

6.2 Enhancing predictive maintenance architecture process by using ontology-enabled Case-Based Reasoning (Article 4) 98

6.3 Cross-validation 107

6.4 Lessons learnt 108

## 6.1 Making the parts work together

Chapters 4 and 5 introduced the two technologies that are used to develop the Decision Support System (DSS) for predictive maintenance component selection. The proposed DSS is intended to overcome the problems encountered when selecting suitable approaches and models in the systems engineering approach to predictive maintenance design presented in Chapter 3. As complex systems may represent an important investment at high risk, the architect can not only rely on an immediate vision of a possible solution (unstructured creativity). The architect needs to explore the solution space looking for suitable components and their possible combinations (structured creativity) to propose a systems architecture able to meet the initial requirements of the system. Exploring the solution space of a new system can be a long-lasting task, especially when the architect has several of options from which they can select logical components. The proposed DSS can help the architect to save time in the exploration of the solution space to find suitable components to fulfill the logical architecture.

This chapter presents the framework for the proposed DSS. It explains how the proposed ontology and the CBR retrieval engine are integrated, and how the DSS fits in the creative work performed by the systems architect. The framework has been consolidated in a conference article. This chapter also includes a complementary section that extends the cross-validation performed to test the DSS capabilities.

6. 2 Enhancing predictive maintenance architecture process by using ontology-enabled Case-Based Reasoning (Article 4)

The content in this section corresponds to a published work in the 7th IEEE International Symposium of Systems Engineering (ISSE) held virtually in 2021. $ \circled{C} $IEEE 2021. Reprinted, with permission, from Juan José Montero Jiménez, Rob Vingerhoeds, and Bernard Grabot. "Enhancing predictive maintenance architecture process by using ontology-enabled Case-Based Reasoning." In: 7th IEEE Int. Symposium on Systems Engineering 2021, Virtual, 2021 [MVG21].

<div align="center">

# Enhancing predictive maintenance architecture process by using ontology-enabled Case-Based Reasoning

</div>

Juan José Montero-Jiménez

Tecnológico de Costa Rica

Cartago, Costa Rica

ISAE-SUPAERO

Toulouse, France

Rob Vingerhoeds

Email: juan.montero@itcr.ac.cr

ISAE-SUPAERO, France

Toulouse, France

Email: rob.vingerhoeds@isae-supaero.fr

Bernard Grabot

ENIT

Tarbes, France

Email: bernard.grabot@enit.fr

Abstract—A common milestone in systems architecture development is the logical architecture. It provides a detailed overview of the system components and their interfaces but keeps the architecture as generic as possible, meaning that no component is bound to a specific technology. Subsequently, the architect searches for physical/informational components to fulfill the logical architecture and can apply structured creativity to look for innovative solutions. This search can turn out to be a difficult and long-lasting task depending on the system complexity. Too many options may be available to fulfill the logical system components and not always the most suitable ones are identified. This problem is for instance encountered in the design of new predictive maintenance systems, especially when selecting the components to carry out the diagnostics and prognostics. The current study proposes to support the choice of suitable components combining case-based reasoning and ontologies. A domain ontology has been developed as a terminology framework to support the case base, case structure and similarity measures for a case-based reasoning Decision Support System (DSS). The DSS uses attributes of the new problem to solve and suggests the most similar cases from past experiences. The retrieved solutions can be adapted to develop a new predictive maintenance architecture. The decision support system has been tested with data coming from proved predictive maintenance solutions documented in scientific publications.

Index Terms—System architecture, case-based reasoning, predictive maintenance, knowledge reuse, structured creativity, decision-support system.

## I. INTRODUCTION

The life cycle of complex systems is composed of several stages starting from the concept phase [1], which can be seen as a very crucial stage. Following a systems engineering approach, the concept phase starts by gathering the needs and desires from all stakeholders, that are then translated into a formal set of requirements to be classified and prioritized to facilitate their analysis. Once the set of stakeholders' requirements is agreed by all parties a creative process starts to find the solution or solutions that meet the requirements. This is then formalized in a system architecture before a detailed design and the system implementation start in the development stage. The system architecture formally describes and represents the system elements and their relationships [1].

Developing a system architecture can be a complex task in which many options are available. Several methods exist to

carry out this architecture process. Very often these methods cover a functional analysis of the system that includes a functional decomposition allowing to handle complexity [1] [3]. Logical components are proposed to fulfill each subfunction. Once the logical components are defined, physical/informational components are selected and allocated to the logical components to complete the systems architecture.

Proposing suitable components to fulfill the logical architecture is an important challenge for the system architect. Sometimes, the architect may have an immediate vision of a solution, yet this does not always lead to the most efficient one. As the development of complex systems may represent an important investment, structured creativity is increasingly used in the concept stage [2]. This means the architect explores the solution space of the system using a structured methodology, identifying and proposing several possible solutions and performing trade-off analysis to identify the most suitable ones. Exploring the solution space of a new system can be longlasting task, specially when the architect has many options for suitable components. Also, no explicit design rules exist to perform such component selection.

To overcome this challenge, this study proposes a searching tool that combines Case-Based Reasoning (CBR) and Ontologies. CBR is a problem solving paradigm based on previous experiences that can be used for design purposes. Ontologies are semantic knowledge representations that can model the terminology of a specific domain. The proposed approach aims at allowing the architect to save time when exploring the solution space and at the same time providing inspiration by offering diverse possible solutions to fulfill the logical components. In contrast to other implementations of CBR for systems design [4], [5], the proposed tool incorporates a domain ontology that serves as terminology framework for the CBR system. It helps to model the case structure, store the case base and compute semantic similarity for retrieval purposes in CBR.

This paper is organized as follows: section II explains the context of the research by introducing the building blocks of the proposed framework: Case-Based Reasoning (CBR), ontologies, and ontology-enabled CBR systems. Section III presents the design of predictive maintenance systems and

their architectures, domain to which the proposed approach is applied. Section IV explains the proposed approach of the use of an ontology-enabled CBR system to enhance structured creativity. Section V presents the implementation of this approach for predictive maintenance systems design. Section VI describes the results of the resulting Decision Support System (DSS) and section VII concludes the paper by summarizing the lessons learnt and providing perspectives of future work.

## II. BACKGROUND

The current study aims at implementing an ontology-based CBR system that can be used to retrieve suitable components for predictive maintenance (PdM) systems. The objective is to propose to system architects a means to explore the solution space more efficiently so not to miss important potential solutions. This section provides a background of CBR, ontologies, and their combination in recent knowledge modelling and reuse works.

## A. Case-based Reasoning (CBR)

Case-based reasoning is a paradigm that leverages past problem solving experience, in form of concrete solving cases, when it comes to solving new problems [6]. Casebased reasoning tries to implement this way of reasoning. The following definition for CBR is used here:

Solve a new problem by remembering a previous similar situation and by reusing information and knowledge of that situation.

Case-based reasoning is a paradigm in which specific knowledge of previously experienced problem situations is being used to solve a new problem, by finding close previous cases, adapting and reusing those previous experiences. It leads to a form of incremental, sustained learning, where information from new situations is kept for future use.

Solving a problem with CBR is performed in a cyclic process of several steps, the so-called CBR-cycle [7], triggered by a new problem: solving the target case. The first phase aims at retrieving the most similar cases from a knowledge base that stores all previous cases. The target case is compared to the stored cases in a the case base using different similarity measurements. The most similar retrieved case is proposed as possible solution in the reuse phase. Some adaptation may be needed to implement the solution for the target case. Subsequently, revision phase takes place to ensure that the suggested solution achieves to solve the problem. Once the solution is validated, in a last phase it is stored in the knowledge base so that it can be reused in future similar problems.

## B. Ontology

In information science, an ontology is a formal explicit description of concepts in a domain of discourse, properties of each concept describing its features, attributes and restrictions [8]. One of the goals in developing ontologies is "sharing a common understanding of the structure information among

people and software agents" [9]. This means that the vocabulary used by people in a specific domain of knowledge is "machine readable". All concepts in an ontology are represented by classes which are linked by properties (also called relations). Ontologies are built using formal languages. One of the most recognized languages is the Web Ontology Language in its second version (OWL2) which is recommended by the World Wide Web Consortium (W3C) [10] because of its importance for the semantic web. The semantic web is an extension of the current web, where the information is well-structured and well-defined so that it can be processed by a machine [11].

Ontologies in OWL2 are compatible with information written in Resource Description Framework (RDF) [10]. In RDF, information is represented in semantic triples: subjectpredicate-object. OWL2 ontologies are primarily exchanged as RDF documents; all the knowledge stored in an ontology can be also represented by semantic triples. Two related classes will represent the subject and the object of the triple, while the relation between the two classes represents the predicate of the triple. RDF structure provides a flexible means to model, storage and manage information [10]; other methods requiring variable-length fields would require a more complicated implementation.

Ontologies can help to make the knowledge explicit, defining the relations among different terms. This allows deep analysis on domain knowledge, helping to identify semantic rules among the terms. These rules can be used to develop algorithms that perform automated inferences based on the domain knowledge.

## C. State-of-the-art of ontology-enabled CBR

For any CBR application, a very important step is the definition of a domain vocabulary that will serve to model the cases, the case base, the similarity measures and the solution adaptation knowledge [12], [13]. CBR was formalized before ontologies gained importance in the artificial intelligence field. Recent research trends incorporate ontologies to facilitate natural language modelling and processing. For CBR, ontologies can be used to enhance case indexing and retrieval, to improve semantic similarity estimation, to improve case representation, to improve case adaptation, and to improve case retention in a case base [14]. Ontologies provide the terminology framework to better describe the case attributes. In [15], an ontology was used as vocabulary framework for a case-based reasoning system that automates emergency response services. The authors use the ontology in the information extraction process, during the lexical analysis. Later, the ontology is used in the case retrieval by helping to determine the similarities for the case attributes.

Ontologies provide the possibility to compute the similarity between two semantic terms by the use of the ontology-based similarity. As [16] explains, ontology-based similarity can be determined by two different manners: by computing the ontological distance or by comparing the features of the terms. As ontologies can be represented by graphs in which the

terms are in the nodes and the relations among the terms are the edges, the ontological distance between two terms is the shortest edges path from one term to another. Featurebased similarity is obtained by comparing the properties of the classes. This feature based similarity can vary depending on the scope. Selecting the different features will yield to different similarities.

Ontologies can also be used to model the cases and the case base in CBR. The ontology classes can be instantiated with the different cases of the case base. An instantiated ontology can be referred to as a knowledge base of the a specific domain [8]. This knowledge base stores the information in the Resource Description Framework (RDF) which can be easily retrieved and managed. In [17], an ontology is presented to support a CBR system for mechanics tolerance specification in which the case base is built on top of the ontology. Another example uses an ontology to build the case base of a CBR system for decision support on manufacturing process selection [18]. Specifically in systems design, [4] proposes an integrated approach using an ontology and a CBR system to propose design solutions based on the initial requirements and preferences. The authors propose a generic design approach in which the cases are built from requirement attributes and the solution obtained from previous experiences with similar requirements.

## III. PREDICTIVE MAINTENANCE SYSTEMS

Current trends in systems architecture aim at incorporating structured creativity methods to explore the solution space in the concept phase of complex systems. The current study aims at integrating CBR and a domain ontology to facilitate the architect work of retrieving suitable components for predictive maintenance systems.

Within the maintenance strategies to trigger maintenance actions, three terms are commonly used: corrective maintenance, preventive maintenance and predictive maintenance. Corrective maintenance triggers the maintenance actions once the failure of a component or system has occurred. Preventive maintenance trigger the maintenance actions by using fixed operation intervals of the component or system; such as time, cycles, kilometres, flights, among others. Predictive maintenance (PdM) aims at determining the right moment to trigger the maintenance actions based on the condition of the maintainable system under consideration [19]. Current fast expanding tools and technologies such as machine learning, internet of things, Industry 4.0, big data, boost predictive maintenance implementation to reach safer, more reliable and more efficient technical systems. Predictive maintenance is often studied within the disciplines of Condition-Based Maintenance (CBM) and Prognostics and Health Management (PHM).


> **Figure Description:**

This diagram illustrates a hierarchical process flow with a central objective at the top and six supporting functional steps below it. The main objective, contained within a large, horizontally oriented rounded rectangle, is labeled "Estimate the precise moment to trigger maintenance actions." An upward-pointing arrow connects this central objective to a horizontal line that branches downward into six individual rounded rectangular boxes.

Each of the six boxes represents a specific function, labeled as follows from left to right: "Collect data (F1)," "Pre-process data (F2)," "Detect faults (F3)," "Assess degradation (F4)," "Compute RUL (F5)," and "Make report (F6)." Each of these six boxes is connected to the horizontal branch line by a vertical line, indicating that these functions collectively contribute to the primary objective of estimating the precise moment to trigger maintenance actions.



Predictive maintenance is carried out by specialized systems whose main function is to estimate the precise moment to trigger maintenance actions. This main function can be decomposed into six different sub-functions (Figure 1: collect data, pre-process data, detect faults, assess degradation, compute

<div align="center">

Fig. 1. Functional decomposition for a predictive maintenance system. [20]

</div>

remaining useful life and make recommendation report). This functional decomposition is widely used to develop the architecture of predictive maintenance systems.A new predictive maintenance system may require components to fulfill all subfunctions or a smaller subset of them [20]. For example, a system can be intended only to cover a fault detection, then the architecture should have components to collect data (F1), pre-process data (F2), detect the fault (F3) and make a recommendation report (F6).

Specifically for the diagnosis and prognosis sub-functions there exist several models that can fulfill the requirements. These models can be implemented individually following a single model approach for each sub-function or many of them can be combined in a multi-model approach [19]. These models can be divided into three main families:

- Knowledge-based models: these models are built from expert knowledge and experience from which it is possible to explicitly define rules, cases and constraints that can be used to perform reasoning. These explicit models highly rely on the access to experts which can be a challenge for their development.

- Physics-based models: these models use the laws of physics to assess the degradation of components. They demand high skills on mathematics and physics of the phenomena for the application.

- Data-driven models: these models use data records that often consist of time series. Data-driven models have gained a lot of importance in recent years thanks to the improved availability of computational power and the large amounts of data produced every day by technical systems.

Predictive maintenance systems accurately illustrate the problem for system architects to select suitable components that fulfill the logical architecture. There are no explicit rules that guide the architect throughout the components selection to fulfill the logical architecture when developing a new predictive system. There exist several models that can be used to carry out the diagnosis and prognosis functions of the system; and these models are often combined as one single model hardly addresses a single task of a predictive maintenance system [19]. A decision support system can help the architect to select the model or combination models that have been used in the past accentuates the need for supporting architects for components selection.

## IV. ONTOLOGY ENABLED CASE-BASED REASONING FOR SYSTEMS ARCHITECTURE

When developing a new system architecture, the architect often looks for inspiration from previous experiences and related systems that already exist. The idea to integrate CaseBased Reasoning (CBR) and ontologies for systems architecture comes from an analogy between CBR and the structured creativity process, as well as the need to formally model the domain vocabulary that allows the knowledge reuse. This section explains the analogy between CBR and structured creativity. A first concept of the integration of a ontologyenabled CBR Decision Support System (DSS) is introduced as means to help the architect to look for inspiration from previous experiences. The analogy and the concept of the DSS, here intended for predictive maintenance systems, are generic and can be used for the development of other types of complex systems as well.

## A. The analogy between structured creativity and CBR for systems architecture

A common milestone in the systems architecture development is the logical architecture. Structured creativity at the logical architecture is based on the combination of different possible physical/informational components that can fulfill the logical components. This allows the exploration of the solution space and may help the architect to identify innovative solutions for a new system. If several possible solutions are identified a trade-off analysis may be necessary to select the most suitable one. The selected architecture serves as a basis for detailed design of the systems. The knowledge gathered from the new implemented system can be used by the architect to develop future systems.

There is an analogy between the structured creativity work performed by the architect to select suitable components to fulfill the logical architecture and the four phases of CaseBased Reasoning: retrieve, reuse, revise and retain. A graphical representation of this analogy is presented in Figure 2 (in Capella notation [3]). All activities before the logical architecture are outside the scope for the current study and for layout simplification, these activities have been summarized in a single box on Figure 2.

- The proposed analogy relates the retrieve phase of CBR with the search performed by the architect on previous related systems that may serve as inspiration for the development of the new system.

- The reuse phase of CBR would be the allocation of the identified components to fulfill the new system architecture.

- The revise phase of CBR would start by the trade-off analysis done by the architect to identify the most suitable components. This phase continues until the verification and validation of the implemented system which are usually performed by other actors than the architect.


> **Figure Description:**

This diagram illustrates a system architecture development process involving an Architect and a team of Design, implementation, verification, and validation engineers. The process begins in the Architect's domain, where the first step is to "Develop concept phase until a generic logical architecture." This leads to a "Generic logical architecture (New Problem)" which feeds into the "Search possible components from previous experiences (Retrieval Phase)." This retrieval phase draws from a separate box labeled "Historical records of previous experiences," which contains a step to "Store knowledge from previous experiences."

The "Search possible components" step produces "Logical components," which then leads to the "Allocate posible components to logical architecture (Reuse phase)." This step also receives input from the "Historical records" box in the form of "Identified suitable components." The output of the allocation phase is "Possible physical architectures," which proceeds to the "Trade-off analysis on the architecture possibilities (start of the revise phase)." From this analysis, a "Selected architecture" is passed down to the "Design, implementation, verification and validation engineers" domain.

Within the engineers' domain, the "Selected architecture" flows into the "Design and implement the system" step. This produces an "Implemented system," which flows into the "Verify and valdiate system (end of revise phase)" step. The output of this verification and validation process is "Information from implemented system," which is sent back to the "Keep records from the validated system (retain phase)" step located within the Architect's domain. Finally, this retention step produces a "New record from the validated system," which is fed back into the "Historical records of previous experiences" box, completing the feedback loop. Each process step is represented by a yellow rectangle containing an icon of a circular orange badge, and the flow between steps is marked with arrows labeled with the nature of the data or artifacts being transferred.



- After validation of the new system, the architect may keep the records to be used in the future; this would be the retain phase of CBR.

<div align="center">

Fig. 2. Analogy between case-based reasoning and the tasks performed by a systems architect, in Capella notation [3]

</div>

This analogy remains generic in terms of the system to be developed. All the activities are carried out "manually" by the architect and the records from previous experiences may not be structured to facilitate their reuse. This manual approach may work when the amount of previous experiences is limited so that the solution space to be explored by the architect remains manageable. When the number of previous experiences is high or the requirements complex, the selection of the most suitable components may not be easily achieved. Retrieving knowledge from an important number of previous architectures may consume too much time and important options may be missed.

## B. A Decision Support System concept using CBR and ontologies

Considering this analogy between CBR and the structured creativity work, different algorithms can be proposed to support the architect in the different phases of the architecture work. In a first step, the current research focused on the development of a Decision Support System (DSS) able to perform the search and recommendation of suitable physical/informational components. This can help the architect save time in the concept phase, and allows a broader analysis done by machines, analysis that can be hardly addressed by humans.

Figure 3 presents a concept of the DSS and how it fits in the analogy presented on Figure 2. This concept is composed of three main parts: the case base, the retrieve engine, and the domain specific ontology. The case base stores the cases from the past in a structured format to facilitate reuse. The

architect will present to the retrieve engine the information from the new system under development and will obtain a set of the most similar cases retrieved from the case base that will serve as inspiration when selecting suitable components for the logical architecture.

Within this structure the ontology plays a vital role. The cases, attributes of these cases and the similarities among the different text based variables are often described in natural language. Modeling this natural language and making it machine readable is necessary to automate the case retrieval.

## V. IMPLEMENTATION ON THE PREDICTIVE MAINTENANCE CASE STUDY

The proposed approach assumes that the logical architecture of the system has been developed. A systematic approach to develop new predictive maintenance systems has been proposed in [20]. The ontology-enabled CBR Decision Support System (DSS) proposed here is for predictive maintenance models (components) selection to fulfill the logical architecture of a new system, especially to fulfill the diagnosis and prognosis functions. The stakeholder requirements for the DSS are as follows:

1) The system shall suggest suitable models to fulfill a specific diagnosis and prognosis function.

2) The system shall provide a list of diverse potential solutions for each logical component.

3) The system shall provide a structured framework to store the knowledge form previous predictive maintenance systems.

4) The system shall base the recommendation on known attributes of the new predictive maintenance system such as function to fulfill, the maintainable system and the available condition data from the maintainable system.

5) The system shall provide design information from the suitable models such as: performance indicators, input variables and models configuration.

## A. Domain ontology development

The ontology for this study was developed using the methodology Ontology Development 101 [8]. To delimit the scope of the ontology a set of competency questions should be considered. The ontology must be able to answer these questions. In this study, these competency questions have been defined in cooperation with experts in predictive maintenance and aim at gathering useful information that can be used in the design of new predictive maintenance systems. In a first attempt, the scope of the ontology is limited by the following competency questions:

- What are functions of a predictive maintenance system?

- What are the systems on which predictive maintenance has been implemented?

- What models have been used to fulfill each function of the system?

- For a given predictive maintenance case, is the predictive maintenance system implemented online or off-line?

- What performance indicators have been used to assess a model that fulfills a predictive maintenance function?

- What data is analyzed by the predictive maintenance models?

- If several models are being used to fulfill a specific function, what is the models configuration in the system?

- Where is the predictive maintenance implementation documented?

The ontology model was developed using a top-level domain-neutral ontology, the Basic Formal Ontology (BFO) [21]. It also uses a set of mid-level domain-neutral ontologies, the Common Core Ontologies (CCO) [22]. BFO and CCO


> **Figure Description:**

This diagram illustrates a Case-Based Reasoning (CBR) system architecture involving three primary actors: the Retrieval System Manager, the Architect, and the Design, implementation, verification, and validation engineers. The Retrieval System Manager box contains a process to "Maintain case base (including the retain phase of CBR)," which sends a "New case" to the "Store cases" process within the "CBR Retrieval System." The CBR Retrieval System also contains a "Retrieve engine" that "Retrieve[s] suitable models from previous experiences" using "Previous cases" from the "Store cases" block and "Terms, definitions, similarities" from the "Ontology Model," which serves to "Provide terminology framework." The "Ontology Model" also sends "Terms, definitions, relations" back to the "Store cases" block.

The Architect block initiates the process by "Develop[ing] concept phase until logical architecture," which provides "attributes of the current problem" to the "Retrieve engine." The "Retrieve engine" then provides "Suitable Models" to the Architect, who proceeds to "Allocate models to logical components (Reuse Phase of CBR)." This step produces "Logical architecture" and leads to "Architecture posibilites," which then feeds into "Architecture trade-off (start of the revise phase of CBR)."

The "Architecture trade-off" step produces a "Selected architecture" that is sent to the "Design, implementation, verification and validation engineers" block. Within this block, the process begins with "Design and implement system," which produces an "Implemented system" that is then processed by "Verification and validation (end of the revise phase of CBR)." Finally, this block outputs a "Verified and validated architecture (revised solution)" that returns to the "Retrieval System Manager" to complete the cycle. All process blocks are represented as yellow rectangles, and data flows are indicated by arrows with labels describing the information being transferred.



<div align="center">

Fig. 3. Incorporation of an CBR retrieve system to facilitate logical components selection in the architecture process

</div>


> **Figure Description:**

This diagram is a conceptual ontology or entity-relationship model illustrating the components and relationships within a Predictive Maintenance (PdM) system. The central node is the "PdM Module," which is connected to a "PdM System" via a "hasPart" relationship. The "PdM Module" also has a "hasQuality" relationship with "Module Sychronization" and "Module Performance indicator," and a "hasFunction" relationship with "PdM Module function." The "PdM Module" is further linked to "PdM Model" via "isCarrierOf."

The "PdM Model" serves as a hub for several relationships: it has a "hasConfiguration" link to "PdM Model configuration," a "hasType" link to "PdM Model type," a "hasInput" link to "Condition Data," and an "IsAbout" link to "Maintainable item." "Condition Data" is linked to "Condition Data Type" via "hasType." The "Maintainable item" is a central entity connected to "Maintainable item type" via "hasType," "Function" via "hasFunction," and "Failure Mode" via "hasFailureMode." "Function" is also linked to "PdM Module function" via an "is a" relationship and to "Failure" via "isAffectedBy." "Failure Mode" is linked to "Failure" via a "describes" relationship.

At the bottom of the diagram, "PdM Case" is linked to "Maintainable item" via "hasCaseStudy" and to "PdM Article" via "isCarrierOf." "PdM Article" is further connected to "PdM Article title," "PdM Article identifier," and "PdM Article Publication year," all of which share an "IsAbout" relationship with the "PdM Article" entity. The diagram uses rectangular boxes for entities and directed arrows labeled with the specific nature of the relationship between them to define the structural hierarchy and semantic connections of the PdM domain.



<div align="center">

Fig. 4. Classes and relations in the ontology to support CBR for PdM component selection

</div>

have also been used in other ontologies in the industrial domain. The standardization on the developed ontology by adopting these upper level ontologies facilitates its future reuse and integration with other ontologies in the industrial domain. The Ontology was created using Protégé $ \textcircled{c} $ (version 5.5.0) and its consistency was verified using the ontology reasoner HermiT OWL (version 1.4.3.456).

Figure 4 summarizes the most important classes and relations in the ontology for CBR decision support system for predictive maintenance components selection. For the validation of the current approach, the ontology was populated with information coming from the publications considered in a recent structured literature survey about predictive maintenance [19]. The OWL API [23] was used to populate the ontology and to provide the classes and methods for the integration of the ontology and the CBR system.

## B. CBR decision support using MyCBR SDK

MyCBR is an open-source similarity-based retrieval tool for Case-Based Reasoning (CBR) [12] that offers two possible options for CBR solutions: a stand-alone application called myCBR Workbench and a Software Development Kit (SDK). The SDK is written in Java and includes all classes and methods to develop CBR applications and integrate them to other systems.

When developing a CBR retrieval system using myCBR, the first step is to determine the case structure. Cases are represented by a coupled vector of attributes Case = [Problem attributes, Solution Attributes]. The problem attributes are used to measure the similarity of a target case and the cases stored in the case base. The solution attributes are stored as part

of the solution information for the cases. Taking as reference the classes in the domain ontology, for predictive maintenance design the case vector will have the following structure:

- Problem Attributes = [PdM Function, Maintainable Item, Maintainable Item Type, Condition Data Type, Module synchronization, PdM Article Publication year]

- Solution Attributes = [PdM Model, PdM Model Configuration, PdM Model Type, Module Performance Indicator, PdM Article Identifier, PdM Article Title]

Once the case structure is defined, a similarity measure must be assigned to each problem attribute. In myCBR the similarity for each problem attribute is referred to as local similarity. MyCBR offers a complete set of similarity measures to compute local similarities. For the current study three main types of similarities have been used: integer/float similarity, symbol similarity and string similarity [12]. The domain ontology plays a vital role in the computation of some of the local similarities. For example, for the predictive maintenance (PdM) functions an ontological similarity approach based on the ontological features is adopted to obtain the similarity among the options [16]. This similarity is computed based on the models that have been historically used to fulfill each function. All the cases stored in the ontology are used to compute this similarity and if the case base is updated with new cases in the future, the similarity will be automatically updated. This similarity measure was selected for the attributes PdM Function, Maintainable Item Type, Condition Data Type, and Module synchronization.

After the similarity computation for each attribute of the problem, the combination of all these individual similarities in a global similarity takes place. Each attribute has a weight and an amalgamation function calculates the final similarity based on local similarities and weights. MyCBR offers two different options to compute the global similarity: weighted sum and Euclidean distance.

- Weighted sum: the sum of similarities considering the weight of each one (equation 1).

$$
s i m _ {g l o b a l} = \sum_ {i = 1} ^ {n} w _ {i} \cdot s i m _ {i}
$$

The values of n, $ w_{i} $ and $ sim_{i} $ are respectively the number of variables, the weight and the similarity of variable i.

- Euclidean distance: distance between two points in Euclidean space. It represents the length of a line segment between the two points (equation 2).

$$
s i m _ {g l o b a l} = \sqrt {\sum_ {i = 1} ^ {n} w _ {i} \cdot s i m _ {i} ^ {2}}
$$

For both amalgamation functions there is a re-scaling normalization between 0 and 1, with 1 being the maximum global similarity between the target case and a retrieved case. This

maximum global similarity is achieved when the target case attributes are identical to those of the retrieved case. This maximum global similarity can be achieved independently from the number of problem attributes that are introduced to the DSS. If the architect uses only on two or three attributes to describe the target case, a global similarity of 1 can be obtained based on those two or three attributes.

## VI. RESULTS AND DISCUSSION

The case base stored in the domain ontology was instantiated with 263 cases obtained from the 135 research papers consulted in [19]. For a cross-validation of the ontologyenabled CBR Decision Support System (DSS), the cases were randomly divided into two sets. A set of 200 cases was used as case base in the ontology, the other 63 cases were used as test set.

## A. Verification

The DSS verification checked how each local similarity performs. For this, several searches were realized using a reduced set of problem attributes. The verification results are described hereafter:

- With searches using one single attribute it was possible to validate the similarity measures assigned to the problem attributes: PdM Function, Maintainable Item, Maintainable Item Type, Condition Data Type and Module synchronization. These are the variables that the user can directly introduce as inputs for the DSS. When presenting only one out of these five possible attributes to define the target case, the DSS retrieved with similarity of 1 every case from the case base that shared the same attribute value as for the target case, independently from the assessed attribute.

- When increasing one by one the number of attributes of the target case, this behaviour was consistent. Several combinations using a reduced set of attributes were tested to confirm the DSS consistency to retrieve the most similar cases.

- The more attributes shown to the DSS, the fewer cases with similarity of 1 or close to one were retrieved. This is an expected behaviour because the stored cases in the case base are diverse. It was rare to find two cases in the case base with the same problem attributes and when it happened, the solution attributes of the retrieved cases were completely different.

- For some of target cases in the testing set, the maximum similarity reached was between 0.7 and 0.8 proving that when no identical cases were found an thus, the maximum global similarity of one can not be reached.

- The searches using a reduced number of attributes also helped verify the similarity measure implemented for the PdM Article Publication year, the only attribute that the user does not specify in the DSS to describe the target case and it is used to compute the global similarity. The current year is automatically retrieved from the operative system and it is compared

against the year of publication of each PdM article. Models applications in newer papers are favored over similar applications from the past. With a reduced number of problem attributes it was possible to confirm that cases from recent publications had a higher similarity to the target case compared to those from older publications.

## B. Validation

The cross-validation of the DSS checked that the stakeholder requirements of section V were met.

- Requirement 1 states that the DSS must suggest suitable components to fulfill diagnosis and prognosis functions in predictive maintenance systems. In practice, an architect needs at least one suitable model to develop the architecture but may look for inspiration from the retrieved cases with highest similarity. In the first attempt the acceptance criteria for the DSS is to provide at least 1 suitable model that can fulfill the PdM function of the target case. For each of the 63 cases it was possible to retrieve the similarity to the 200 cases in the case base. A list of the 5 most similar cases for each target case in the testing set was retrieved. For all the test cases at least one suitable model with similarity above 0.7 was retrieved. For each test case, the implemented PdM model is known. In 40% of the tested cases the implemented PdM model matched to one of proposed solutions by the DSS. In 40% of the tested cases all the proposed solutions by the DSS were implemented for the same PdM function. For the other 60% there was at least one recommended PdM model that was originally used for a different PdM function but being possible to adapt it to the target case. For example, for a target case to fulfill a fault detection function, the DSS proposed a classification model that was used for fault identification in the retrieved case. Classification techniques are suitable for both PdM functions. With these results, the acceptance criteria of the first requirement has been fulfilled; the capability of ontology-enabled CBR decision support system to recommend suitable models to fulfill a specific function of a predictive maintenance system has been confirmed.

- The validation highlights an important point of improvement with regard to the diversity in the retrieved cases. This is related to the second requirement. In at least half of the tested cases, within the list of the 5 most similar cases retrieved by the DSS, two or three cases proposed the same PdM model as potential solution. It is important to notice that this is not a problem of repeated cases in the case base, the similarities of the retrieved cases are different among them but sometimes they propose the exact same solution. Diversity in retrieved cases is a common problem in CBR [13], especially when several different potential solutions are expected from the retrieval phase. Diversity in the retrieved cases can help architects to develop innovative solutions. The identified problem narrows down the solution space recommended

by the ontology-enabled CBR system to the architect and represents an improvement of the DSS for future work.

- As the case base is stored in the domain ontology the third requirements is met. The ontology is a formal and structured knowledge representation that stores the predictive maintenance implementations of the past that can be reused.

- The case structured in the DSS was determined in such a way to fulfill requirements 4 and 5. The problem attributes are based on known parameters of the new predictive maintenance system and the solution attributes of the retrieved cases provide useful information for the design of the system.

For the verification and validation of the proposed DSS, both amalgamation functions were tested with no significant differences in the results. For this current study, all the attributes were assumed to have the same importance, so no special weights were assigned to the local similarities. As such they had a default value of 1.

## VII. CONCLUSION AND FUTURE WORK PERSPECTIVES

The current study presents the use of a ontology-enabled Case-Based Reasoning (CBR) recommendation system to select suitable components for predictive maintenance systems architecture. The proposed approach benefits from the semantic knowledge modelled using a domain ontology. It allows to build the similarity measures for different attributes of the CBR system. The ontology stores the case base for the CBR that was created using the myCBR platform. The validation shown that the ontology-enabled CBR system is capable to retrieve suitable components to fulfill specific predictive maintenance functions. The retrieval capability was validated with all problem attributes that have been introduced individually and combined to the recommendation system. The retrieved cases can help architects as inspiration to develop innovative solutions for new predictive maintenance systems.

Future work perspectives include the refinement of the case retrieval functions, case base maintenance to improve the diversity in the retrieved cases, and the integration of a trade-off analysis that can help the architect perform the selection among the retrieved components. Future perspective also include the incorporation of algorithms to address other CBR phases such as adaptation of the retrieved cases for the target problem and case base maintenance after retaining newer cases. As the analogy of CBR and structured creativity was proposed as a generic approach, its implementation in other case studies is also considered in the future work perspectives.

## ACKNOWLEDGMENT

## REFERENCES

The authors would like to thank the students Johanna Mazouzi from ISAE-ENSMA, Augusto Miyagawa and Hugo Muñoz-Hernandez from ISAE-SUPAERO, for their collaboration in this research.

[1] INCOSE, Systems Engineering Handbook. A guide for system life cycle processes and activities. Fourth Edition. Wiley, 2015.

[2] E. Crawley, B. Cameron, and D. Selva, System Architecture: Strategy and Product Development for Complex Systems. Pearson Higher Education, Inc., 2015.

[3] P. Roques, Systems Architecture Modeling with the Arcadia Method 1st Edition. ISTE Press, 2018.

[4] J. C. Romero Bejarano, T. Coudert, E. Vareilles, L. Geneste, M. Aldanondo, and J. Abeille, "Case-based reasoning and system design: An integrated approach based on ontology and preference modeling," Artificial Intelligence for Engineering Design, Analysis and Manufacturing: AIEDAM, vol. 28, pp. 49-69, 2014.

[5] A. Tidemann, F. O. Bjørnson, and A. Aamodt, "Case-based reasoning in a system architecture for intelligent fish farming," in Frontiers in Artificial Intelligence and Applications, 2011.

[6] J. Kolodner, Case based reasoning. Morgan Kaufmann, 1993.

[7] A. Agnar and E. Plaza, "Case-Based reasoning: Foundational issues, methodological variations, and system approaches," AI Communications, vol. 7, no. 1, pp. 39-59, 1994.

[8] N. F. Noy and D. L. McGuinness, "Ontology Development 101: A Guide to Creating Your First Ontology," Tech. Rep., 2001.

[9] T. R. Gruber, "A translation approach to portable ontology specifications," Knowledge Acquisition, vol. 5, no. 2, pp. 199-220, 1993.

[10] World Wide Web Consortium, "OWL 2 Web Ontology Language," 2012. [Online]. Available: http://www.w3.org/TR/2012/REC-owl2-overview-20121211/

[11] D. L. Nuñez and M. Borsato, "OntoProg: An ontology-based model for implementing Prognostics Health Management in mechanical machines," Advanced Engineering Informatics, vol. 38, pp. 746-759, 2018.

[12] K. Althoff, T. Roth-Berhofer, K. Bach, and C. Severin, "Documentation: myCBR," 2006. [Online]. Available: http://mycbrproject.org/%0Adownloads/myCBR_3_tutorial_slides.pdf

[13] R. L. De Mantaras, D. Mcsherry, D. Bridge, D. Leake, B. Smyth, S. Craw, B. Faltings, M. L. Maher, M. T. Cox, K. Forbus, M. Keane, A. Aamodt, and I. Watsoni, "Retrieval, reuse, revision and retention in case-based reasoning." The Knowledge Engineering Review, vol. 20, no. 3, pp. 215-240, 2005.

[14] J. Prentzas and I. Hatzilygeroudis, "Combinations of case-based reasoning with other intelligent methods," in CEUR Workshop Proceedings, 2008.

[15] K. Amailef and J. Lu, "Ontology-supported case-based reasoning approach for intelligent m-Government emergency response services," Decision Support Systems, vol. 55, pp. 79-97, 2013.

[16] D. Sánchez, M. Batet, D. Isern, and A. Valls, "Ontology-based semantic similarity: A new feature-based approach," Expert Systems with Applications, vol. 39, pp. 7718-7728, 2012.

[17] Y. Qin, W. Lu, Q. Qi, X. Liu, M. Huang, P. J. Scott, and X. Jiang, "Towards an ontology-supported case-based reasoning approach for computer-aided tolerance specification," Knowledge-Based Systems, vol. 141, pp. 129-147, 2018.

[18] M. M. Mabkhot, A. M. Al-Samhan, and L. Hidri, "An ontology-enabled case-based reasoning decision support system for manufacturing process selection," Advances in Materials Science and Engineering, 2019.

[19] J. J. Montero Jimenez, S. Schwartz, R. Vingerhoeds, B. Grabot, and M. Salaün, "Towards multi-model approaches to predictive maintenance: A systematic literature survey on diagnostics and prognostics," Journal of Manufacturing Systems, vol. 56, pp. 539-557, 2020.

[20] J. J. Montero Jiménez and R. Vingerhoeds, "A System Engineering Approach to Predictive Maintenance Systems: from needs and desires to logical architecture." in 5th IEEE Int. Symposium on Systems Engineering 2019., Edinburgh, 2019.

[21] International Organization for Standardization (ISO), ISO/IEC 21838-2 Information technology - Top-level ontologies (TLO) - Part 2: Basic Formal Ontology (BFO), 2020.

[22] R. Rudnicki, "An Overview of the Common Core Ontologies 1.3," Buffalo, NY, p. 29, 2020. [Online]. Available: https://www.nist.gov/system/files/documents/2019/05/30/nistai-rfi-cubrc_inc_004.pdf

[23] I. Palmisano, "OWLAPI Documentation," 2020. [Online]. Available: https://mvnrepository.com/artifact/net.sourceforge.owlapi/owlapi-distribution/5.1.17

## 6.3 Cross-validation

This section extends the cross-validation discussion presented in Article 4 included in Section 6.2. The cross-validation of the ontology-enabled Case-Based Reasoning (CBR) system (the Decision Support System) allows demonstrating that this knowledge reuse technique can be used for the component selection of predictive maintenance systems. It is important to recall that in this first step, the validation is oriented to show that a Decision Support System (DSS) is capable to propose suitable components to fulfil specific predictive maintenance functions. No trade-off analysis has been implemented yet to assess the models proposed by the DSS. The validation focuses on the fact that the suggested models can be adapted to fulfil a specific function and that the list of suggested solutions covers all the solution space.

Cross-validation is a technique that can be used to test the effectiveness of trained artificial intelligence models. For the current approach, a train-test split approach is selected to perform the cross validation. For the test set, 63 out of the 263 cases in the case base were randomly extracted and the rest have been left in case base as training set. For each of the 63 extracted cases, the problem attributes were presented to the DSS using a GUI. The attention was centred on the 10 most similar cases when performing the retrieval. Figure 6.1 shows an example of a retrieval test in which all the target case problem attributes are matched with the corresponding attributes of case 35. This full match between the attributes turns out in a global similarity of 1.


> **Figure Description:**

This image is a software interface screenshot.

The interface is titled "Predictive maintenance with CBR method - GUI 2" and contains two main sections: "Input variables" and "Additional inputs." The "Input variables" section features a table with six rows, each having a label, a dropdown menu, and a "Variable weights" column set to 1.0 for all entries. The rows are: "PdM function :" (Remaining useful life estimation), "Maintainable item type :" (Rotary machines), "Maintainable item :" (Rolling bearings), "Condition data type :" (Vibrations), "Module sychonization :" (Off-line), and "Condition data :" (Time series). The "Additional inputs" section includes a field for "Number of cases to retrieve:" set to 10, and a dropdown for "Aggregation function to use:" set to "euclidean."

Below these inputs is a "User dialog" box displaying the text: "I found Case35 with a similarity of 1.000 as the best match. The 10 best cases shown in a table:". This is followed by a table with two columns labeled "Case" and "Description." The first row of the table contains "Case35" and "Sim = 1.000" in the first column, and a detailed description in the second column: "Reference, Similarity and Input variables," "Reference: 35," "Task: Remaining useful life estimation," "Case study type: Rotary machines," "Case study: Rolling bearings," "Online/Off-line: Off-line," "Input for the model: Time series," "Models: Convolutional Neural Network," "Input type: Vibrations," "Publication Year: 2018," and "Publication identifier: DOI: 10.1109/ACCESS.2018.2804930." At the very bottom of the window is a button labeled "SUBMIT QUERY."



<div align="center">

Figure 6.1: Retrieval example using the GUI of the DSS

</div>

The solution space of the predictive maintenance models can be divided into two groups as explained in [Mon+20]. The first group is composed of single model approaches, divided into three main categories: knowledge-based models, data-driven models and physics-based models. The second group is composed of multi-model approaches, in which at least two models from any of the three mentioned categories are combined to fulfil a specific function of the PdM system. Predictive maintenance is composed of diagnostics and prognostics tasks. According to the literature review [Mon+20], diagnostics tasks such as fault detection, fault identification, and health state modelling can be addressed by models of the three categories of single model approaches or multi-model approaches. In contrast, for prognostics tasks, it is difficult to find knowledge-based models applications. For example, prognostics functions such as remaining useful life estimation and next state forecast functions are normally fulfilled by physics-based models, data-driven

models, and multi-model approaches combining physics-based and data-driven models. The cross-validation of the DSS allowed to confirm this behaviour. The retrievals for diagnostics tasks proposed single model and multi-model solutions considering models from the three categories of models. The retrievals for prognostics also proposed single model and multi-model solutions, but the proposed models were only from data-driven and physics-based categories. This helps to confirm that the solution space is well covered.

For each test case, the retrieved cases are ranked based on the similarity of problem attributes. For some of the tests, two or more retrieved cases had the same maximum similarity value. From a systems engineering perspective this represents a limitation because no further information is provided to perform the trade-off analysis and selected the most suitable one. Another limitation was identified with regards the diversity in the retrieved cases. For some target cases the DSS retrieved two or more cases that proposed the same model to fulfil a specific PdM function. An architect looking for inspiration to develop innovative solutions will need the DSS to propose a diverse set of models. Retrieving two cases with the exact same solution is not useful for the solution space exploration.

The above mentioned limitations are improvement points for the DSS to be considered in the future. A more detailed analysis can also be performed including the effort to adapt the solution of a retrieved case for the target case. This can help to perform the trade-off analysis on the retrieved options and consequently improve the performance of the DSS.

## 6.4 Lessons learnt

This chapter presented the Decision Support System framework and can help the architect in the selection of predictive maintenance components and approaches. The chapter explains the integration of OPMAD and the CBR retrieval engine developed with myCBR platform. It also explains how the DSS can fit in the architecture process and how an architect can benefit from it to automate the solution space exploration allowing a more accurate structured creativity by only retrieving the most suitable components for a new predictive maintenance system.

Recalling the refine research questions introduced in Chapter 2:

1. How to address the design of predictive maintenance systems?

2. How to suggest a suitable approach for a predictive maintenance system solution?

3. How to select a suitable model or combination of models given a new predictive maintenance problem to solve?

4. How can a designer benefit from the experience of existing systems to develop new predictive maintenance solutions?

The presented framework attempts to answer the first refined research question. It combines the systems engineering approach for the concept stage presented in Chapter 3 and the use of a DSS for the selection of suitable components for the logical architecture. The DSS implementation attempts to answer the rest of the research questions. It allows to store the past experiences of predictive maintenance implementations and retrieves the most suitable ones depending on the new predictive maintenance system to develop. The DSS not only suggests the models that can fulfil a specific predictive maintenance function but also other important aspects that can be used for the detailed design and implementation. To further validate the proposed framework and the DSS capabilities, the next chapter presents a practical example on which the framework and the DSS are used. An implementation of one of the suggested models by the DSS is used to indirectly validate the accuracy of the DSS recommendations.

<div align="center">

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

# Conclusion and perspective for future work

</div>

“No tengas miedo de la perfección,

nunca la alcanzarás.”

“Have no fear of perfection,

you’ll never reach it.”

Salvador Dali

Content

8.1 The journey is coming to an end, but a new one starts... 121

8.2 Lessons learnt 121

8.3 Limitations encountered 123

8.4 Contributions summary 124

8.5 Perspectives of future work 125

8.5.1 Perspectives related to the systems engineering approach to predictive maintenance systems design 125

8.5.2 OMSSA and OPMAD perspectives 125

8.5.3 Ontology-enabled case-based reasoning system perspectives 126

8.6 Epilogue 127

## 8.1 The journey is coming to an end, but a new one starts...

Research never ends but the current manuscript has already covered a wide field in the design of predictive maintenance systems and how the knowledge reuse from previous experiences can enhance the architecture process of such systems. Acknowledging that for the addressed topics there is still a long way to be covered, this chapter concludes the content of this manuscript by summarizing the lessons learnt, the limitations encountered, the research contributions, and more importantly the perspectives of future work that can serve as inspiration for future research lines.

## 8.2 Lessons learnt

To summarize the lessons learnt during this research it is necessary to come back to the research questions that initially motivated this work. In the introduction the first research questions was introduced:

1. What are the current trends in diagnostics and prognostics in predictive maintenance?

2. What are the main challenges in predictive maintenance?

3. What are the main research opportunities in the field of predictive maintenance?

These questions motivated an extensive literature review, that allowed to understand that predictive maintenance is carried out by specialized tools that incorporate models able to perform diagnostics and prognostics. The implementation of these models can be divided in two different approaches: single-model approaches and multi-model approaches. Single model approaches can be divided into three main model families: data-driven models, knowledge-based models and physics-based models. Multi-model approaches include at least two models from any of the mentioned model families. Depending on the multi-model approaches configuration, they can be called hybrid models. Recent trends in predictive maintenance push towards the implementation of multi-model approaches as one single model hardly addresses all the predictive maintenance functions for a complex system. The literature review allowed to determine the current challenges in predictive maintenance which include:

- Lack of a systematic method to design predictive maintenance systems.

- The extrapolation of existing solutions to complex system applications.

- The fusion of large and different sources of condition monitoring data.

- The incorporation of external influence data.

- Uncertainty management.

The main part of the challenges are focused in the concept stage and the design of new predictive maintenance systems. This motivated a refinement of the research questions:

1. How to address the design of predictive maintenance systems?

2. How to suggest a suitable approach for a predictive maintenance systems solution?

3. How to select a suitable model or combination of models given a new predictive maintenance system to solve?

4. How can a designer benefit from the experience of existing systems to develop new predictive maintenance solutions?

With regards to the first refined question, a systems engineering approach is proposed in the current research to address the concept stage of new predictive maintenance systems. This systematic approach starts by gathering all initial needs and desires from the stakeholders. The needs and desires are translated into a formal set of stakeholder requirements which are divided into four main categories: functional requirements, behavioural requirements, structural requirements and experiential requirements. The classified requirements are prioritized and later used at different phases of the system architecture process.

While developing this systems engineering approach, a challenge was identified at the logical architecture which also matches with the other refined research questions. The logical architecture shows as much detail as possible of the new system but without engaging it to any specific technology, meaning that the logical architecture still remains generic. The selection of predictive maintenance models to fulfil the logical components became the main scope of the current research. While performing the literature review, hundreds

of publications with successful cases of implemented predictive maintenance systems were consulted; the information from these implementations is not being efficiently used. The hypothesis was proposed: a Case-Based Reasoning (CBR) system can help an architect to retrieve efficiently a suitable model or set of models to perform a structured creativity process and fulfil the logical components in a new predictive maintenance system.

The CBR paradigm was selected as it offers means of reasoning to solve problems based on previous experiences. It is more flexible than rule-based reasoning and it is suitable for the current research as no specific rules exist to link the predictive models to a specific function in the system or to a specific case study. To develop a CBR system one of the most important aspects is a strong vocabulary basis from which the cases and the similarities can be modelled. For the current research, the state-of-the-art in vocabulary development for CBR was considered. It concerns ontologies, which are formal terminology representations that have a wide field of applications, especially in the semantic web. The research in ontologies allowed to identify an opportunity to make a contribution in the topic. Two Ontologies have been developed for the current research, the first one called OMSSA corresponds to a terminology framework to select and assess maintenance strategies. The second one, called OPMAD, is an OMSSA extension and covers the vocabulary involved in the design of predictive maintenance systems. OPMAD is the ontology that is used as a vocabulary framework for the proposed DSS.

It is important to mention that CBR and ontologies not always were implemented together. In recent years, both technologies have been increasingly used together because ontologies boost the use of the vocabulary basis for CBR applications. In the proposed framework, an ontology-enabled CBR recommendation system (a DSS) was developed to help the architect in the selection of suitable predictive maintenance models. A crossed validation helped to demonstrate that the proposed DSS was capable to suggest suitable components for specific predictive maintenance functions. To further validate the DSS, an implementation example was performed using the N-CMAPPS case study. The DSS proposed the Self-Organizing Maps (SOM) among the possible options to address health modelling. During the implementation of the SOM, it was possible not only to confirm the capabilities of the DSS but also to identify its improvement points. These improvement points are part of the perspectives of future works presented in this chapter.

In general, the research allowed to understand the principles of knowledge reuse with the CBR paradigm and how it can be used for architecture and design purposes. The implementation of the DSS allowed suggesting suitable components to fulfil generic components of a logical architecture of a predictive maintenance system.

## 8.3 Limitations encountered

As for any other research project, several limitations have been found on the way. This section aims at sharing part of the personal experience when performing the current research. Two main limitations have been faced. These are not specific for the current research but rather generic in the current context:

The first one and most important would be the limitation of time. It is understood that research never ends and at the end of any PhD thesis there will always remaining works to be done. For the current research, this is not an exception. Besides the normal workload that a PhD thesis represents, the time frame in which it was developed was also characterized by a global pandemic that forced to close the laboratories in France and all over the world. This affected the research schedule and forced the research objectives refinement. The research topic had to change in the middle of the second year and impacts due to the pandemic were considered to remake the research schedule.

The second limitation was related to the lack of access to practical examples that can be used to further

validate the DSS capabilities. There were conversations with different companies and groups able to provide practical examples that could have been included in this research validation. Bureaucracy and lack of interest from the external actors did not allow to have the case studies on time to be added to the current manuscript. Conversations with public companies in Costa Rica still undergoing so that the research can be continued in the near future.

Having faced these limitations enriches the research experience. It helps the researcher to be resilient and creative when facing problems out of their hands.

## 8.4 Contributions summary

The current manuscript is composed of four articles that have been published or submitted for being considered for publication in international journals and/or conferences. The main contributions of the PhD research have been consolidated in the articles as follows:

1. The review article summarized the state-of-the-art in diagnostics and prognostics. A proposal to differentiate hybrid models from multi-model approaches has been provided. The tendencies towards the implementation of multi-model approaches have been pointed out. By the time this manuscript was finished, the review article was cited more than thirty times. The literature review can be seen as a scientific contribution as it provides a starting point for those researchers interested in predictive maintenance.

2. The systems engineering approach to predictive maintenance systems design has been the first scientific contribution published in an international conference during the PhD development. In contrast to existing generic architectures for the design of predictive maintenance systems, the proposed systematic approach addresses the concept stage of predictive maintenance systems from the initial needs and desires until the logical architecture. It helps the architect to accurately determine the components of the system and keep traceability with the initial needs and desires obtained from the stakeholders.

3. Even if ontologies were not the main scope of the current research, a fair amount of research work has been performed in the domain and it has produced its own research outcomes. The creation of OMSSA, an ontology model for maintenance strategy selection and assessment provides a terminology framework that can be used by smart agents to automate the complex tasks of maintenance strategies management. An extension to OMSSA (OPMAD) is the ontology used to create the case base and the similarity measures of the DSS for predictive maintenance component selection. The research work performed in creating OMSSA has been consolidated in a journal article accepted for publication at the moment this manuscript was written.

4. The main scope of the current research has produced a decision support system able to query successful cases of predictive maintenance system implementations that can help a systems architect to select suitable predictive maintenance models to fulfil diagnostics and prognostics tasks. The first outcomes of this research have been published in a conference paper which has been published at an international conference while this manuscript was being completed.

## 8.5 Perspectives of future work

While working in research it is not possible to explain and prove everything. In order to accomplish the research objectives in a fixed time frame, some of the intermediate research steps have to be simplified and sometimes pragmatic decisions are made. When accomplishing the results, it is important to put things in perspective to spot the improvement points and list them as perspectives of future work. Research never ends, and one of the main parts of any PhD manuscript is to indicate what was missing and expected to be done in order to continue the research line. The perspectives of future work are organized in three main groups:

1. Perspectives related to the systems engineering approach to predictive maintenance systems design

2. Perspectives related to the ontologies developed in the current research

3. Perspective related to the ontology-enabled case-based recommendation system for predictive maintenance component selection.

## 8.5.1 Perspectives related to the systems engineering approach to predictive maintenance systems design

- Refine the list of predictive maintenance system needs, desires and requirements: after publishing the article related to the concept stage of predictive maintenance systems several needs, desires and requirements were identified that were not originally considered. The list of possible needs, desires and requirements for new predictive maintenance systems can be improved. These lists can be stored in a knowledge base that can be used by automated smart agents to help the engineers assess the initial needs and desires for a predictive maintenance system and suggest the corresponding stakeholder requirements. A DSS could be developed to define the correct stakeholder requirements based on the initial needs and desires for the new predictive maintenance system.

- Include trade-off analysis technique in the systematic framework: Trade-off analyses are present in several points during the concept stage. Due to time constraints, it was not addressed in this thesis. The integration of a trade-off analysis tool can help to improve the DSS and facilitate the selection of the components of the architecture.

- Include the formalization of system requirements: an important aspect of a systems engineering approach is the elicitation of system requirements. Even when the creation of these requirements is in theory before the architecture process, in practice these requirements are normally established in parallel with the development of the system architecture or even at the end when all the performances for the different logical components are known. These requirements are important for the detailed design stage. The elicitation of these requirements was out of the scope of the current research but it is an interesting complementary topic for future research.

## 8.5.2 OMSSA and OPMAD perspectives

- Refine classes and relations: ontology development is a fast evolving topic. There are several initiatives to provide top-level and mid-level ontologies in different domains. The industrial domain is not the exception. Further work will be needed to align OMSSA and OPMAD to these standardized ontologies so that to boost their integration and reuse in other applications. This work includes the refinement of classes and relations among them.

- Extend reasoning in the ontology: OMSSA and OPMAD have been useful in the current research but as ontologies, they have been underutilised. Ontologies have several capabilities that were not exploited. One of them is the implementation of semantic rules. This extends the reasoning options and can be used as a complementary means to the CBR system.

## 8.5.3 Ontology-enabled case-based reasoning system perspectives

- Expand the use of the ontology for more local similarity functions: as it was already mentioned, the ontology has been useful but underutilised. Some other similarity measures that have been assigned a binary symbol similarity measure can be rearranged to use ontology-based similarities.

- Use the ontology to estimate the weights for the global similarity computation: related to the previous remark. the ontology can also be used to compute the weights of each local similarity when computing the global similarity. In the first attempt of global similarity computation performed in this research, all local similarities received the same weight. An improvement in the global similarity computation could be by giving a rank of importance to each local similarity. The weights can be computed using the populated ontology.

- Expand the Decision Support System by developing other phases of the CBR cycle, such as the adaptation phase: The scope for the DSS was on the retrieval phase of the CBR cycle. The system can be expanded to facilitate the adaptation phase of the suggested components for the new predictive maintenance system. This extension can also include the trade-off analysis on different components suggested by the DSS. The results of the current research shown several improvement opportunities that should be addressed in the future before eventual deployment of the DSS.

- Refine the instantiation process to avoid diversity problems but keeping all the solution space covered: As it was mentioned in the validation chapter, the instantiation of the case base should be refined. An improvement opportunity can be to divide the solution space according to the different predictive maintenance functions and make sure that the solution space is fully covered for each of them. Generalized cases for each predictive maintenance function can solve the problem of diversity in the retrieval cases.

- Trade-off analysis to better select the technique among the proposed ones: it was already mentioned as the perspective of future work for the systematic approach to design predictive maintenance systems. Regarding the DSS, the trade-off analysis can help the architect discriminate among the suggested components by the DSS. In the validation it was mentioned that sometimes the DSS suggested two different components with the same similarity. Adding some extra attributes such as performance indicators can help the architect make the right decision for their problem.

- Compare against other techniques for DSS: In a first attempt, the objective of the current research was to prove that case-based reasoning can be combined with ontologies to develop a Decision Support System for component selection for new predictive maintenance systems and it worked. Further research would be dedicated to assess the performance of the proposed DSS against other technologies that can be used for the same purposes such as machine learning algorithms. Such comparison was not considered as it exceeded the scope of the current research.

## 8.6 Epilogue

The content of the current manuscript has come to an end. It attempted to summarize the research experiences accumulated over the last three years specifically in the topic of predictive maintenance systems design, an interesting topic that still leaves a lot challenges to be solved. A systematic methodology to address the concept phase of such systems has been proposed and within this framework a more specific challenge was identified for suitable components selection. A Decision Support System composed of an ontology-enabled cased-based reasoning retrieval engine has been proposed to overcome the challenge of suitable component selection based on past experiences. The results demonstrated the capabilities of the proposed DSS but also allowed to spot important improvement opportunities that should be considered in future research.

Intentionally left blank

## Bibliography

[AA10] Edgar J. Amaya and Alberto J. Alvares. "SIMPREBAL: An expert system for real-time fault diagnosis of hydrogenerators machinery". In: Proceedings of the 15th IEEE International Conference on Emerging Technologies and Factory Automation, ETFA 2010. 2010. ISBN: 9781424468508. DOI: 10.1109/ETFA.2010.5641302.

[AGC18] Panagiotis Aivaliotis, Konstantinos Georgoulias, and George Chryssolouris. "A RUL calculation approach based on physical-based simulation models for predictive maintenance". In: 2017 International Conference on Engineering, Technology and Innovation: Engineering, Technology and Innovation Management Beyond 2020: New Challenges, New Approaches, ICE/ITMC 2017 - Proceedings. 2018. ISBN: 9781538607749. DOI: 10.1109/ICE.2017. 8280022.

[AH17] Sylvestre A. Aye and Philippus S. Heyns. "An integrated Gaussian process regression for prediction of remaining useful life of slow speed bearings based on acoustic emission". In: Mechanical Systems and Signal Processing 84.A (2017), pp. 485-498. ISSN: 10961216. DOI: 10.1016/j.ymssp.2016.07.039.

[AH18] Sylvester A. Aye and Stephan Heyns. "Prognostics of slow speed bearings using a composite integrated Gaussian process regression model". In: International Journal of Production Research 56.14 (2018), pp. 4860-4873. ISSN: 1366588X. DOI: 10.1080/00207543.2018.1470340.

[AIC18] Ronke M. Ayo-Imoru and Anthonie C. Cilliers. "Continuous machine learning for abnormality identification to aid condition-based maintenance in nuclear power plant". In: Annals of Nuclear Energy 118 (2018), pp. 61-70. ISSN: 18732100. DOI: 10.1016/j.anucene.2018.04.002.

[AKC15] Dawn An, Nam H. Kim, and Joo Ho Choi. "Practical options for selecting data-driven or physics-based prognostics algorithms with reviews". In: Reliability Engineering and System Safety 133 (2015), pp. 223-236. ISSN: 09518320. DOI: 10.1016/j.ress.2014.09.014.

[AL13] Khaled Amailef and Jie Lu. "Ontology-supported case-based reasoning approach for intelligent m-Government emergency response services". In: Decision Support Systems 55 (2013), pp. 79-97. ISSN: 01679236. DOI: 10.1016/j.dss.2012.12.034.

[Alt+12] Klaus Althoff et al. Documentation: myCBR. 2012. URL: http://www.mycbr-project.org/3.1-doc/index.html.

[Ant+12] Grigoris Antoniou et al. A Semantic Web Primer. Third edit. MIT Press, 2012. ISBN: 9780262018289.

[AP94] Agnar Aamodt and Enric Plaza. "Case-Based reasoning: Foundational issues, methodological variations, and system approaches". In: AI Communications 7.1 (1994), pp. 39-59. ISSN: 09217126. DOI: 10.3233/AIC-1994-7104.

[ASF14] Pekka Aarnio, Ilkka Seilonen, and Mats Friman. "Semantic repository for case-based reasoning in CBM services". In: 19th IEEE International Conference on Emerging Technologies and Factory Automation, ETFA 2014. 2014. ISBN: 9781479948468. DOI: 10.1109/ETFA. 2014.7005195.

[ASS16] Robert Arp, Barry Smith, and Andrew D. Spear. Building Ontologies with Basic Formal Ontology. 2016. DOI: 10.7551/mitpress/9780262527811.001.0001.

[AX17] Suzan Alaswad and Yisha Xiang. "A review on condition-based maintenance optimization models for stochastically deteriorating system". In: Reliability Engineering and System Safety 157 (2017), pp. 54-63. ISSN: 09518320. DOI: 10.1016/j.ress.2016.08.009.

[Bag+15] Behrad Bagheri et al. "A Stochastic Asset Life Prediction Method for Large Fleet Datasets in Big Data Environment". In: ASME 2015 International Mechanical Engineering Congress and Exposition. Volume 14: Emerging Technologies; Safety Engineering and Risk Analysis; Materials: Genetics to Structures. 2015. ISBN: 978-0-7918-5757-1. DOI: 10.1115/ IMECE2015-52458.

[Bai+15] Chris Bailey et al. "Prognostic and health management for engineering systems: a review of the data-driven approach and algorithms". In: The Journal of Engineering 2015.7 (2015), pp. 215-222. ISSN: 2051-3305. DOI: 10.1049/joe.2014.0303.

[Baj+09] Gautam Bajracharya et al. "Optimization of maintenance for power system equipment using a predictive health model". In: 2009 IEEE Bucharest PowerTech: Innovative Ideas Toward the Electrical Grid of the Future. 2009. ISBN: 9781424422357. DOI: 10.1109/PTC.2009. 5281928.

[BAJ17] Oguz Bektas, Amjad Alfudail, and Jeffrey A. Jones. "Reducing Dimensionality of Multiregime Data for Failure Prognostics". In: Journal of Failure Analysis and Prevention 17 (2017), pp. 1268-1275. ISSN: 15477029. DOI: 10.1007/s11668-017-0368-2.

[BB09] Donald W Benbow and Hugh W Broome. The Certified Reliability Engineer Handbook. 2009. ISBN: 978-0-87389-721-1. DOI: 10.1017/CBO9781107415324.004. arXiv: arXiv: 1011.1669v3.

[BB+17] Diana Barraza-Barraza et al. "An adaptive ARX model to estimate the RUL of aluminum plates based on its crack growth". In: Mechanical Systems and Signal Processing 82 (2017), pp. 519-536. ISSN: 10961216. DOI: 10.1016/j.ymssp.2016.05.041.

[BB18] Toufik Berredjem and Mohamed Benidir. "Bearing faults diagnosis using fuzzy expert system relying on an Improved Range Overlaps and Similarity method". In: Expert Systems with Applications 108 (2018), pp. 134-142. ISSN: 09574174. DOI: 10.1016/j.eswa.2018.04.025.

[BBM18] Marius Baban, Calin Florin Baban, and Beniamin Moisi. "A Fuzzy Logic-Based Approach for Predictive Maintenance of Grinding Wheels of Automated Grinding Lines". In: 2018 23rd International Conference on Methods and Models in Automation and Robotics, MMAR 2018. 2018. ISBN: 9781538643259. DOI: 10.1109/MMAR.2018.8486144.

[Ber+01] Ralph Bergmann et al. "Utility-Oriented Matching: A New Research Direction for Case-Based Reasoning". In: Proceedings of the Ninth German Workshop on Case-Based Reasoning. 2001.

[Ber+16] Maitane Berecibar et al. "Online state of health estimation on NMC cells based on predictive analytics". In: Journal of Power Sources (2016). ISSN: 03787753. DOI: 10.1016/j.jpowsour.2016.04.109.

[BKP05] Ralph Bergmann, Janet Kolodner, and Enric Plaza. "Representation in case-based reasoning". In: Knowledge Engineering Review 20.3 (2005), pp. 209-213. ISSN: 02698889. DOI: 10. 1017/S0269888906000555.

[Bos+13] Kosta P. Boshnakov et al. "Predictive maintenance model-based approach for objects exposed to extremely high temperatures". In: 2013 Signal Processing Symposium, SPS 2013. 2013. ISBN: 9781467363198. DOI: 10.1109/SPS.2013.6623621.

[Bra+18] Frances Brazier et al. "Design, Engineering and Governance of Complex Systems". In: Projects and People - Mastering success. Ed. by H.L.M. Bakker and J.P. Kleynen. NAP Foundation Press, 2018, pp. 34-59.

[But96] Karen L. Butler. "An Expert System Based Framework for an Incipient Failure Detection and Predictive Maintenance System". In: Proceeding of the Int Conf on Intelligent Sys Application to Power Sys (1996). ISSN: 0020-7543. DOI: 10.1080/002075400188933. arXiv: arXiv:1011.1669v3.

[BW96] Ralph Bergmann and Wolfgang Wilke. "On the role of abstraction in case-based reasoning". In: Proceeding of the 3rd European Workshop on Case-Based Reasoning. Berlin: Springer, 1996, pp. 29-43.

[CA+17] Vicente Climente-Alarcon et al. "Combined Model for Simulating the Effect of Transients on a Damaged Rotor Cage". In: IEEE Transactions on Industry Applications (2017). ISSN: 00939994. DOI: 10.1109/TIA.2017.2691001.

[Cas+20] Fernando Castaño et al. "Quality monitoring of complex manufacturing systems on the basis of model driven approach". In: Smart Structures and Systems 26.4 (2020), pp. 495- 506. ISSN: 17381991. DOI: 10.12989/sss.2020.26.4.495. URL: http://techno press.org/content/?page=article\&journal=sss\&volume=26\&num= 4{\&}ordernum=7.

[CCN19] Duan Chaoqun, Deng Chao, and Li Ning. "Reliability assessment for CNC equipment based on degradation data". In: The International Journal of Advanced Manufacturing Technology 100 (2019), pp. 421-434.

[CCS15] Edward Crawley, Bruce Cameron, and Daniel Selva. System Architecture: Strategy and Product Development for Complex Systems. Pearson Higher Education, Inc., 2015.

[Cer+16] Mariela Cerrada et al. "Fault diagnosis in spur gears based on genetic algorithm and random forest". In: Mechanical Systems and Signal Processing 70-71 (2016), pp. 87-103. ISSN: 10961216. DOI: 10.1016/j.ymssp.2015.08.030.

[CFZ17] Yang Chang, Huajing Fang, and Yong Zhang. "A new hybrid method for the prediction of the remaining useful life of a lithium-ion battery". In: Applied Energy 206 (2017), pp. 15641578. ISSN: 03062619. DOI: 10.1016/j.apenergy.2017.09.106.

[CH11] Jamie B. Coble and Wesley Hines. "Applying the General Path Model to Estimation of Remaining Useful Life". In: International Journal of Prognostics and Health Management 2.1 (2011), p. 13. ISSN: 21532648.

[Cha+21] Manuel Arias Chao et al. "Aircraft Engine Run-to-Failure Dataset under Real Flight Conditions for Prognostics and Diagnostics". In: Data 2021, Vol. 6, Page 5 6.1 (2021), p. 5. DOI: 10.3390/DATA6010005. URL: https://www.mdpi.com/2306-5729/6/1/5/htmhttps://www.mdpi.com/2306-5729/6/1/5.

[Che+16] Peter Chemweno et al. "I-RCAM: Intelligent expert system for root cause analysis in maintenance decision making". In: 2016 IEEE International Conference on Prognostics and Health Management, ICPHM 2016. 2016. ISBN: 9781509003822. DOI: 10.1109/ICPHM. 2016.7542830.

[Che+17] Zhen Chen et al. "Hidden Markov model with auto-correlated observations for remaining useful life prediction and optimal maintenance policy". In: Reliability Engineering and System Safety 184 (2017), pp. 123-136. ISSN: 09518320. DOI: 10.1016/j.ress.2017.09.002.

[Chi+19] Juan Chiachio et al. "A knowledge-based prognostics framework for railway track geometry degradation". In: Reliability Engineering and System Safety 181 (2019), pp. 127-141. ISSN: 09518320. DOI: 10.1016/j.ress.2018.07.004.

[Cho+19] Michael E. Cholette et al. "Degradation modeling and condition-based maintenance of boiler heat exchangers using gamma processes". In: Reliability Engineering and System Safety 183 (2019), pp. 184-196.

[CNY10] Wahyu Caesarendra, Gang Niu, and Bo Suk Yang. "Machine condition prognosis based on sequential Monte Carlo method". In: Expert Systems with Applications 37.3 (2010), pp. 2412-2420. ISSN: 09574174. DOI: 10.1016/j.eswa.2009.07.014.

[CRW08] Jiehua Chen, Clive Roberts, and Paul Weston. "Fault detection and diagnosis for railway track circuits using neuro-fuzzy systems". In: Control Engineering Practice 16 (2008), pp. 585-596. ISSN: 09670661. DOI: 10.1016/j.conengprac.2007.06.007.

[CYC12] Cong Cheng, Ling Yu, and Liu Jie Chen. "Structural nonlinear damage detection based on ARMA-GARCH model". In: Applied Mechanics and Materials 204-208 (2012), pp. 2891- 2896. ISSN: 16609336. DOI: 10.4028/www.scientific.net/AMM.204-208.2891.

[CZMR19] Qiushi Cao, Cecilia Zanni-Merk, and Christoph Reich. "Towards a core ontology for condition monitoring". In: Procedia Manufacturing. 2019. DOI: 10.1016/j.promfg.2018.12.029.

[De +05] Ramon Lopez De Mantaras et al. "Retrieval, reuse, revision and retention in case-based reasoning". In: The Knowledge Engineering Review 20.3 (2005), pp. 215-240. ISSN: 02698889. DOI: 10.1017/S0269888906000646.

[De +18] Massimiliano De Benedetti et al. "Anomaly detection and predictive maintenance for photovoltaic systems". In: Neurocomputing 310 (2018), pp. 59-68. ISSN: 18728286. DOI: 10.1016/j.neucom.2018.05.017.

[DHK13] Nadjette Dendani-Hadiby and M. Tarek Khadir. "A fault diagnosis application based on a combination case-based reasoning and ontology approach". In: International Journal of Knowledge-Based and Intelligent Engineering Systems 17.4 (2013), pp. 305-317. ISSN: 13272314. DOI: 10.3233/KES-130280.

[DLS17] Dong Dong, Xiao Yang Li, and Fu Qiang Sun. "Life prediction of jet engines based on LSTM-recurrent neural networks". In: 2017 Prognostics and System Health Management Conference, PHM-Harbin 2017 - Proceedings. 2017. ISBN: 9781538603703. DOI: 10.1109/PHM.2017.8079264. arXiv: arXiv:1512.04143v1.

[DMB16] Landon T. Detwiler, Jose L.V. Mejino, and James F. Brinkley. "From frames to OWL2: Converting the Foundational Model of Anatomy". In: Artificial Intelligence in Medicine 69 (2016), pp. 12-21. ISSN: 18732860. DOI: 10.1016/j.artmed.2016.04.003.

[DMD18] Chaoqun Duan, Viliam Makis, and Chao Deng. "An integrated framework for health measures prediction and optimal maintenance policy for mechanical systems using a proportional hazards model". In: Mechanical Systems and Signal Processing 111 (2018), pp. 285-302. ISSN: 10961216. DOI: 10.1016/j.ymssp.2018.02.029.

[Dow+19] Austin Downey et al. "Physics-based prognostics of lithium-ion battery using non-linear least squares with dynamic bounds". In: Reliability Engineering and System Safety 182 (2019), pp. 1-12.

[Dra+09] Otilia Elena Dragomir et al. "Review of prognostic problem in condition-based maintenance". In: European Control Conference, (ECC'09). 2009. ISBN: 9783952417393. DOI: 10.1128/JB.00591-09.

[DS18] Samalis Santini De León and Daniel Selva. "A rule-based tool for science traceability of Mars exploration mission architectures". In: IEEE Aerospace Conference Proceedings. 2018. ISBN: 9781538620144. DOI: 10.1109/AERO.2018.8396804.

[DZD14] Xiaofei Du, Yuanjun Zhou, and Shiliang Dong. "Residual life prediction from statistical features and a GARCH modeling approach for aircraft generators". In: Proceedings of the Institution of Mechanical Engineers, Part G: Journal of Aerospace Engineering 228.1 (2014), pp. 137-146. ISSN: 20413025. DOI: 10.1177/0954410012472838.

[ECJ14] Omer Faruk Eker, Fatih Camci, and Ian K Jennions. "A Similarity-based Prognostics Approach for Remaining Useful Life Prediction". In: Second European Conference of the Prognostics and Health Management Society 2014. 2014.

[ECJ16] Omer F. Eker, Fatih Camci, and Ian K. Jennions. "Physics-based prognostic modelling of filter clogging phenomena". In: Mechanical Systems and Signal Processing 75 (2016), pp. 395-412. ISSN: 10961216. DOI: 10.1016/j.ymssp.2015.12.011.

[EER16] Hatem M. Elattar, Hamdy K. Elminir, and Alaa el-din Mohamed Riad. "Prognostics: a literature review". In: Complex & Intelligent Systems 2.2 (2016), pp. 125-154. ISSN: 2199-4536. DOI: 10.1007/s40747-016-0019-3.

[ENM18] Ikuobase Emovon, Rosemary A. Norman, and Alan J. Murphy. "Hybrid MCDM based methodology for selecting the optimum maintenance strategy for ship machinery systems". In: Journal of Intelligent Manufacturing 29 (2018), pp. 519-531. ISSN: 15728145. DOI: 10.1007/s10845-015-1133-6.

[ESE15] Shaker El-Sappagh and Mohammed Elmogy. "Case Based Reasoning: Case Representation Methodologies". In: International Journal of Advanced Computer Science and Applications 6.11 (2015), pp. 192-208. ISSN: 2158107X. DOI: 10.14569/ijacsa.2015.061126.

[Eur09] European standard NF EN 13306X60-319. Maintenance — Terminologie de la maintenance. 2009.

[Eur17] European Committee for Standardization. CEN EN 13306: Maintenance-Maintenance terminology. 2017.

[FDL07] Dean K Frederick, Jonathan DeCastro, and Jonathan Litt. User's guide for the Commercial Modular Aero-Propulsion System Simulation (C-MAPSS). Tech. rep. Washington, DC: NASA, 2007.

[Fer+11] Miriam Fernández et al. "Semantically enhanced Information Retrieval: An ontology-based approach". In: Journal of Web Semantics 9.1 (2011), pp. 434-452. ISSN: 15708268. DOI: 10.1016/j.websem.2010.11.003.

[Fer+18] Borja Ramis Ferrer et al. "Towards Adoption of Cyber-Physical Systems of Systems Paradigm in Smart Manufacturing Environments". In: Proceedings - IEEE 16th International Conference on Industrial Informatics, INDIN 2018. 2018. ISBN: 9781538648292. DOI: 10.1109/INDIN.2018.8472061.

[FGPJ97] Mariano Fernandez, Asuncion. Gómez-Perez, and Natalia Juristo. "Methontology: from ontological art towards ontological engineering". In: Proceedings of the AAAI97 Spring Symposium Series on Ontological Engineering. 1997.

[Fou20] The OBO Foundry. Relation Ontology (RO). 2020. URL: http://www.obofoundry.org ontology/ro.html (visited on 07/22/2020).

[Fra57] Alexander S. Fraser. "Simulation of Genetic Systems by Automatic Digital Computers I". In: Australian Journal of Biological Science 10 (1957), pp. 484-491.

[Fre91] Bernd Freyermuth. "Knowledge based incipient fault diagnosis of industrial robots". In: IFAC Proceedings Volumes (IFAC-PapersOnline) 24.6 (1991), pp. 369-375.

[FZ15] Liu Fang and Huang Zhaodong. "System Dynamics Based Simulation Approach on Corrective Maintenance Cost of Aviation Equipments". In: Procedia Engineering. Vol. 99. Elsevier Ltd, 2015, pp. 150-155. DOI: 10.1016/j.proeng.2014.12.519.

[Gan+15] Ma Gang et al. "A model of intelligent fault diagnosis of power equipment based on CBR". In: Mathematical problems in engineering Article ID 203083 (2015).

[Ger90] John S. Gero. "Design Prototypes: A knowledge Representation Schema for Design". In: AI Magazine 11.4 (1990), pp. 26-36.

[GF95] Michael Grüninger and Mark Stephen Fox. "Methodology for the Design and Evaluation of Ontologies". In: International Joint Conference on Artificial Intelligence (IJCAI95), Workshop on Basic Ontological Issues in Knowledge Sharing. 1995. DOI: citeulike- article-id:1273832.

[GK07] John S. Gero and Udo Kannengiesser. "A function-behavior-structure ontology of processes". In: Artificial Intelligence for Engineering Design, Analysis and Manufacturing: AIEDAM. 2007. DOI: 10.1017/S0890060407000340.

[GMZ16] Rafael Gouriveau, Kamal Medjaher, and Noureddine Zerhouni. From Prognostics and Health Systems Management to Predictive Maintenance 1: Monitoring and Prognostics. 2016.ISBN:9781119371052.DOI:10.1002/9781119371052.

[Goy+16] Deepam Goyal et al. "Intelligent predictive maintenance of dynamic systems using condition monitoring and signal processing techniques-A review". In: Proceedings - 2016 International Conference on Advances in Computing, Communication and Automation, ICACCA 2016. 2016. ISBN: 9781509006731. DOI: 10.1109/ICACCA.2016.7578870.

[GPH13] Yuan Guo, Yinghong Peng, and Jie Hu. "Research on high creative application of case-based reasoning system on engineering design". In: Computers in Industry 64.1 (2013), pp. 90-103. ISSN: 0166-3615. DOI: 10.1016/J.COMPIND.2012.10.006.

[Gru93] Thomas R. Gruber. "A translation approach to portable ontology specifications". In: Knowledge Acquisition 5.2 (1993), pp. 199-220. ISSN: 10428143. DOI: 10.1006/knac.1993.1008.

[Guo+17] Liang Guo et al. "A recurrent neural network based health indicator for remaining useful life prediction of bearings". In: Neurocomputing 240 (2017), pp. 98-109. ISSN: 18728286. DOI: 10.1016/j.neucom.2017.02.045.

[GV17] Jakub Gajewski and David Vališ. "The determination of combustion engine condition and reliability using oil analysis by MLP and RBF neural networks". In: Tribology International 115 (2017), pp. 557-572. ISSN: 0301679X. DOI: 10.1016/j.triboint.2017.06.032.

[Han+19] Houman Hanachi et al. "Hybrid sequential fault estimation for multi-mode diagnosis of gas turbine engines". In: Mechanical Systems and Signal Processing 115 (2019), pp. 225-268. ISSN: 10961216. DOI: 10.1016/j.ymssp.2018.05.054.

[HB11] Matthew Horridge and Sean Bechhofer. "The OWL API: A Java API for OWL ontologies". In: Semantic Web 2.1 (2011), pp. 11-21. ISSN: 15700844. DOI: 10.3233/SW-2011-0025.

[HLC14] Bahareh Rahmanzadeh Heravi, Mark Lycett, and Sergio de Cesare. "Ontology-based standards development: Application of OntoStanD to ebXML business process specification schema". In: International Journal of Accounting Information Systems 15.3 (2014), pp. 275- 297. ISSN: 14670895. DOI: 10.1016/j.accinf.2014.01.005.

[HLP08] Frank van Harmelen, Vladimir Lifschitz, and Bruce Porter. Handbook of Knowledge Representation. 2008. ISBN: 9780444522115. DOI: 10.1016/S1574-6526(07)03013-1.

[Hod+21] Melinda Hodkiewicz et al. "Rethinking Maintenance Terminology for an Industry 4.0 Future". In: International Journal of Prognostics and Health Management 2021.1 (2021), p. 14. URL: https://www.phmsociety.org/node/2794.

[Hoe09] Rinke Hoekstra. Ontology representation: Design patterns and ontologies that make sense. IOS Press, 2009. ISBN: 9781607500131. DOI: 10.3233/978-1-60750-013-1-i.

[HSC18] Moinul Shaidul Haque, Mohammad Noor Bin Shaheed, and Seungdeog Choi. "RUL Estimation of Power Semiconductor Switch using Evolutionary Time series Prediction". In: 2018 IEEE Transportation and Electrification Conference and Expo, ITEC 2018. 2018. ISBN: 9781538630488. DOI: 10.1109/ITEC.2018.8450131.

[HT18] Ahmed Zakariae Hinchi and Mohamed Tkiouat. "Rolling element bearing remaining useful life estimation based on a convolutional long-short-Term memory network". In: Procedia Computer Science 127 (2018), pp. 123-132. ISSN: 18770509. DOI: 10.1016/j.procs. 2018.01.106.

[Hu+12] Chao Hu et al. "Ensemble of data-driven prognostic algorithms for robust prediction of remaining useful life". In: Reliability Engineering and System Safety 103 (2012), pp. 120- 135. ISSN: 09518320. DOI: 10.1016/j.ress.2012.03.008.

[Hu+18] Ya-Wei Hu et al. "Sequential Monte Carlo Method Toward Online RUL Assessment with Applications". In: Chinese Journal of Mechanical Engineering 31.5. https://doi.org/10.1186/s10033-018-0205-x (2018). ISSN: 1000-9345. DOI: 10.1186/s10033-018-0205-x.

[Hus+15] Akhtar Hussain et al. "An expert system for acoustic diagnosis of power circuit breakers and on-load tap changers". In: Expert Systems with Applications 42.24 (2015), pp. 9426-9433. ISSN: 09574174. DOI: 10.1016/j.eswa.2015.07.079.

[INC15] INCOSE. Systems Engineering Handbook. A guide for system life cycle processes and activities. Fourth Edition. Wiley, 2015.

[Int03] International Organization for Standardization (ISO). ISO 13374-1:2003 Condition monitoring and diagnostics of machines — Data processing, communication and presentation Part 1: General guidelines. 2003.

[Int12a] International Organization for Standardization (ISO). ISO 13372 - Condition monitoring and diagnostics of machines Vocabulary. 2012.

[Int12b] International Organization for Standardization (ISO). ISO 13379-1:2012 - Condition monitoring and diagnostics of machines Data interpretation and diagnostics techniques Part 1: General guidelines. 2012.

[Int18] International Electrotechnical Commission (IEC). IEC60812, Analysis techniques for system reliability- Procedure for failure mode and effects analysis (FMECA). 2018.

[Int20a] International Organization for Standardization (ISO). ISO/IEC 21838-1 Information technology - Top-level Ontologies (TLO) - Part 1: Requirements. 2020.

[Int20b] International Organization for Standardization (ISO). ISO/IEC 21838-2 - Information technology - Top-level ontologies (TLO) - Part 2: Basic Formal Ontology (BFO). 2020.

[Int97] International Organization for Standardization (ISO). Information technology — Vocabulary Part 14: Reliability, maintainability and availability. 1997.

[IOF20] IOF. Industrial Ontology Foundry. 2020. URL: https://www.industrialontologies.org/?page{\_}id=164 (visited on 10/06/2020).

[ISO11] ISO/IEC/IEE. 42010:2011 Systems and Software Engineering — Architectural Description Ed. by ISO/IEC 42010:2011 International Organization for Standardization (ISO)/International Electrotechnical Commission (IEC). 2011.

[JGZ17] Kamran Javed, Rafael Gouriveau, and Noureddine Zerhouni. "State of the art and taxonomy of prognostics approaches, trends of prognostics applications and open issues towards maturity at different technology readiness levels". In: Mechanical Systems and Signal Processing 94 (2017), pp. 214-236. ISSN: 10961216. DOI: 10.1016/j.ymssp.2017.01.050.

[Jin+15] Wenjing Jin et al. "Development and evaluation of health monitoring techniques for railway point machines". In: 2015 IEEE Conference on Prognostics and Health Management: Enhancing Safety, Efficiency, Availability, and Effectiveness of Systems Through PHAf Technology and Application, PHM 2015. 2015. ISBN: 9781479918935. DOI: 10.1109/ ICPHM.2015.7245016.

[JLB06] Andrew K.S. Jardine, Daming Lin, and Dragan Banjevic. "A review on machinery diagnostics and prognostics implementing condition-based maintenance". In: Mechanical Systems and Signal Processing 20.7 (2006), pp. 1483-1510. ISSN: 08883270. DOI: 10.1016/j. ymssp.2005.09.012. arXiv: 0208024 [gr-qc].

[Kar+19] Mohamed Hedi Karray et al. "ROMAIN: Towards a BFO compliant reference ontology for industrial maintenance". In: Applied Ontology 14.2 (2019), pp. 155-177. ISSN: 18758533. DOI: 10.3233/AO-190208.

[KCL18] Dongdong Kong, Yongjie Chen, and Ning Li. "Gaussian process regression for tool wear prediction". In: Mechanical Systems and Signal Processing 104 (2018), pp. 556-574. ISSN: 10961216. DOI: 10.1016/j.ymssp.2017.11.021.

[KCMZ12] Mohamed Hedi Karray, Brigitte Chebel-Morello, and Noureddine Zerhouni. "A formal ontology for industrial maintenance". In: Applied Ontology 7.3 (2012), pp. 1-20. ISSN: 15705838. DOI: 10.3233/AO-2012-0112.

[KCMZ15] Racha Khelif, Brigitte Chebel-Morello, and Noureddine Zerhouni. "Experience Based Approach for Li-ion Batteries RUL Prediction". In: IFAC-PapersOnLine. 2015. DOI: 10. 1016/j.ifacol.2015.06.174.

[Kee18] Maria Keet. An Introduction to Ontology Engineering. Texts in computing Vol 20, 2018, p.289.

[Kel+01] Kirby Keller et al. "A process and tool for determining the cost/benefit of prognostic applications". In: AUTOTESTCON (Proceedings). 2001. DOI: 10.1109/autest.2001. 949432.

[KH07] Ranganath Kothamasu and Samuel H. Huang. "Adaptive Mamdani fuzzy model for conditionbased maintenance". In: Fuzzy Sets and Systems 158.24 (2007), pp. 2715-2733. ISSN: 01650114. DOI: 10.1016/j.fss.2007.07.004.

[Kin+18] Jakob Kinghorst et al. "Hidden Markov model-based predictive maintenance in semiconductor manufacturing: A genetic algorithm approach". In: IEEE International Conference on Automation Science and Engineering. 2018. ISBN: 9781509067800. DOI: 10.1109/COASE. 2017.8256274.

[KKL12] Kiyoshi Kobayashi, Kiyoyuki Kaito, and Nam Lethanh. "A statistical deterioration forecasting method using hidden Markov model for infrastructure management". In: Transportation Research Part B: Methodological 46.4 (2012), pp. 544-561. ISSN: 01912615. DOI: 10.1016/j.trb.2011.11.008.

[Kol93] Janet Kolodner. Case based reasoning. Morgan Kaufmann, 1993, p. 612.

[Kol94] Janet L. Kolodner. "Understanding creativity: A case-based approach". In: Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics). 1994. ISBN: 9783540583301. DOI: 10.1007/3-540-58330-0_73.

[Kot+06] Ranganath Kothamasu et al. "System health monitoring and prognostics -a review of current paradigms and practices". In: International Journal of Advanced Manufacturing Technology 28.9 (2006), pp. 1012-1024. ISSN: 02683768. DOI: 10.1007/978-1-84882-472-0_14. arXiv: arXiv:1011.1669v3.

[KRH02] Gregory J. Kacprzynski, Michael J. Roemer, and Andrew J. Hess. "Health management system design: Development, simulation and cost/benefit optimization". In: IEEE Aerospace Conference Proceedings. 2002. ISBN: 078037231X. DOI: 10.1109/AERO.2002.1036148.

[KS12a] Erik E. Kostandyan and John D. Sorensen. "Physics of failure as a basis for solder elements reliability assessment in wind turbines". In: Reliability Engineering and System Safety 108 (2012), pp. 100-107. ISSN: 09518320. DOI: 10.1016/j.ress.2012.06.020.

[KS12b] Prakash Kumar and R. K. Srivastava. "An expert system for predictive maintenance of mining excavators and its various forms in open cast mining". In: 2012 1st International Conference on Recent Advances in Information Technology, RAIT-2012. 2012. ISBN: 9781457706974. DOI: 10.1109/RAIT.2012.6194607.

[LDS18] Xiang Li, Qian Ding, and Jian Qiao Sun. "Remaining useful life estimation in prognostics using deep convolution neural networks". In: Reliability Engineering and System Safety 172 (2018), pp. 1-11. ISSN: 09518320. DOI: 10.1016/j.ress.2017.11.021.

[Le +13] Khanh Le Son et al. "Remaining useful life estimation based on stochastic deterioration models: A comparative study". In: Reliability Engineering and System Safety 112 (2013), pp. 165-175. ISSN: 09518320. DOI: 10.1016/j.ress.2012.11.022. arXiv: 1011.1669.

[Leg+17] Václav Legát et al. "Preventive maintenance models - Higher operational reliability. Maintenance and Reliability". In: Eksploatacja i Niezawodnosc 19.1 (2017), pp. 134-141. ISSN: 15072711. DOI: 10.17531/ein.2017.1.19.

[Lei+18] Yaguo Lei et al. "Machinery health prognostics: A systematic review from data acquisition to RUL prediction". In: Mechanical Systems and Signal Processing 104 (2018), pp. 799-834. ISSN: 10961216. DOI: 10.1016/j.ymssp.2017.11.016.

[Lev66] Vladimir Levenshtein. "Binary codes capable of correcting deletions, insertions, and reversals". In: Soviet Physics Doklady 10.8 (1966), pp. 707-710.

[LFS18] Sai Li, Huajing Fang, and Bing Shi. "Multi-Step-Ahead Prediction with Long Short Term Memory Networks and Support Vector Regression". In: Chinese Control Conference, (CCC). 2018. ISBN: 9789881563941. DOI: 10.23919/ChiCC.2018.8484066.

[LGS13] Kaibo Liu, Nagi Z. Gebraeel, and Jianjun Shi. "A Data-level fusion model for developing composite health indices for degradation modeling and prognostic analysis". In: IEEE Transactions on Automation Science and Engineering 10.3 (2013), pp. 652-664. ISSN: 15455955. DOI: 10.1109/TASE.2013.2250282.

[LHS20] Daniel P Lupp, Melinda Hodkiewicz, and Martin G Skjæveland. "Template libraries for industrial asset maintenance: A methodology for scalable and maintainable ontologies". In: CEUR Workshop Proceedings. Vol. 2757. 2020, pp. 49-64.

[LHZ18] Huan Luo, Miaohua Huang, and Zhou Zhou. "Integration of Multi-Gaussian fitting and LSTM neural networks for health monitoring of an automotive suspension component". In: Journal of Sound and Vibration 428 (2018), pp. 87-103. ISSN: 10958568. DOI: 10.1016/j.jsv.2018.05.007.

[Li+12] Sha Li et al. "Health condition-based maintenance decision intelligent reasoning method". In: Proceedings of 2012 International Conference on Quality, Reliability, Risk, Maintenance, and Safety Engineering, ICQR2MSE 2012. 2012. ISBN: 9781467307888. DOI: 10.1109/ ICQR2MSE.2012.6246263.

[Li+16] Qi Li et al. "Remaining useful life estimation for deteriorating systems with time-varying operational conditions and condition-specific failure zones". In: Chinese Journal of Aeronautics 29.3 (2016), pp. 662-674. ISSN: 10009361. DOI: 10.1016/j.cja.2016.04.007.

[Li+17] Gaoyang Li et al. "Failure Prognosis of High Voltage Circuit Breakers with Temporal Latent Dirichlet Allocation". In: Energies 10.11 (2017), p. 1913. ISSN: 1996-1073. DOI: 10.3390/en10111913.

[Li+18] Jianfeng Li et al. "Three-dimensional Simulation and Prediction of Solenoid Valve Failure Mechanism Based on Finite Element Model". In: IOP Conference Series: Earth and Environmental Science. 2018. DOI: 10.1088/1755-1315/108/2/022035.

[Liu+09] Hao Liu et al. "A review on fault prognostics in integrated health management". In: ICEMI 2009 - Proceedings of 9th International Conference on Electronic Measurement and Instruments. 2009. ISBN: 9781424438624. DOI: 10.1109/ICEMI.2009.5274082.

[Liu+18] Datong Liu et al. "An on-line state of health estimation of lithium-ion battery using unscented particle filter". In: IEEE Access (2018). ISSN: 21693536. DOI: 10.1109/ACCESS.2018. 2854224.

[LK18] Changyong Lee and Daeil Kwon. "A similarity based prognostics approach for real time health management of electronics using impedance analysis and SVM regression". In: Microelectronics Reliability 83 (2018), pp. 77-83. ISSN: 00262714. DOI: 10.1016/j.microre1.2018.02.014.

[LLS19] Yanting Li, Shujun Liu, and Lianjie Shu. "Wind turbine fault diagnosis based on Gaussian process classifiers applied to operational data". In: Renewable Energy 134 (2019), pp. 357- 366. ISSN: 18790682. DOI: 10.1016/j.renene.2018.10.088.

[LMM18] Yazid Laib dit Leksir, Moufid Mansour, and Abdelkrim Moussaoui. "Localization of thermal anomalies in electrical equipment using Infrared Thermography and support vector machine". In: Infrared Physics and Technology 89 (2018), pp. 120-128. ISSN: 13504495. DOI: 10. 1016/j.infrared.2017.12.015.

[LQ+19] Hu Li-Qiang et al. "Track circuit fault prediction method based on grey theory and expert systems". In: Journal of Visual Communication and Image Representation 58 (2019), pp. 37- 45.

[LWX19] Yuqian Lu, Hongqiang Wang, and Xun Xu. "ManuService ontology: a product data model for service-oriented business interactions in a cloud manufacturing environment". In: Journal of Intelligent Manufacturing 30 (2019), pp. 317-334. ISSN: 15728145. DOI: 10.1007/s10845-016-1250-x.

[LYKS18] Kenisuomo C. Luwei, Akilu Yunusa-Kaltungo, and Yusuf A. Sha'aban. "Integrated Fault Detection Framework for Classifying Rotating Machine Faults Using Frequency Domain Data Fusion and Artificial Neural Networks". In: Machines 6.59 (2018).

[LYM16] Lei Lu, Jihong Yan, and Yue Meng. "Dynamic Genetic Algorithm-based Feature Selection Scheme for Machine Health Prognostics". In: Procedia CIRP 56 (2016), pp. 316-320. ISSN: 22128271. DOI: 10.1016/j.procir.2016.10.026.

[Mab+18] Mohammed M. Mabkhot et al. Requirements of the smart factory system: A survey and perspective. 2018. DOI: 10.3390/MACHINES6020023.

[MAK14] Nadakatti Mahantesh, Parida Aditya, and Uday Kumar. "Integrated machine health monitoring: A knowledge based approach". In: International Journal of Systems Assurance Engineering and Management 5 (2014), pp. 371-382. ISSN: 09764348. DOI: 10.1007/s13198013-0178-1.

[MASH19] Mohammed M. Mabkhot, Ali M. Al-Samhan, and Lotfi Hidri. "An ontology-enabled casebased reasoning decision support system for manufacturing process selection". In: Advances in Materials Science and Engineering (2019). ISSN: 16878442. DOI: 10.1155/2019/ 2505183.

[Mat+10] Aristeidis Matsokis et al. "An ontology-based model for providing Semantic Maintenance". In: IFAC Proceedings Volumes (IFAC-PapersOnline). 2010. ISBN: 9783902661784. DOI: 10.3182/20100701-2-pt-4012.00004.

[MBZ95] Mary Lou Maher, M. Bala Balachandran, and Dong Mei Zhang. Case-Based Reasoning in Design. 1st Editio. Psychology Press, 1995.

[McD+18] Darren McDonnell et al. "Predicting the unpredictable: Consideration of human and organisational factors in maintenance prognostics". In: Journal of Loss Prevention in the Process Industries 54 (2018), pp. 131-145. ISSN: 09504230. DOI: 10.1016/j.jlp.2018.03.008. arXiv: 1612.08814.

[MD97] Mary Lou Maher and Andrés Gómez De Silva Garza. "Case-based reasoning in design". In: IEEE Expert-Intelligent Systems and their Applications 12.2 (1997), pp. 34-41. ISSN: 08859000. DOI: 10.1109/64.585102.

[Men+15] Sandeep Menon et al. "Evaluating covariance in prognostic and system health management applications". In: Mechanical Systems and Signal Processing 58-59 (2015), pp. 206-217. ISSN: 10961216. DOI: 10.1016/j.ymssp.2014.10.012.

[MHMJV21] Hugo Muñoz-Hernández, Juan José Montero-Jiménez, and Rob Vingerhoeds. "Integrating ontologies and case-based reasoning for the development of knowledge-intensive systems". In: Proceedings of the 35th annual European Simulation and Modelling Conference. 2021, pp. 29-36. ISBN: 978-9-492859-18-1.

[MIM01] MIMOSA. Open System Architecture for Condition-Based Maintenance (OSA-CBM). 2001.

[MLK17] Josey Mathew, Ming Luo, and Chee Khiang Pang. "Regression kernel for prognostics with support vector machines". In: 22nd IEEE International Conference on Emerging Technologies and Factory Automation (ETFA). 2017.

[MM90] Vidosav D. Majstorovic and Vladimir R. Milacic. "Expert Systems for Maintenance in the CIM Concept". In: Computers in Industry 15 (1990), pp. 83-93.

[MMZ16] Ahmed Mosallam, Kamal Medjaher, and Noureddine Zerhouni. "Data-driven prognostic method based on Bayesian approaches for direct remaining useful life prediction". In: Journal of Intelligent Manufacturing 27.5 (2016), pp. 1037-1048. ISSN: 15728145. DOI: 10.1007/s10845-014-0933-4.

[MNK13] Nader Meskin, Esmaeil Naderi, and Khashayar Khorasani. "A multiple model-based approach for fault diagnosis of jet engines". In: IEEE Transactions on Control Systems Technology 21.1 (2013), pp. 254-262. ISSN: 10636536. DOI: 10.1109/TCST.2011.2177981.

[MO+14] Gabriela Medina-Oliva et al. "Predictive diagnosis based on a fleet-wide ontology approach". In: Knowledge-Based Systems 68 (2014), pp. 40-57. ISSN: 09507051. DOI: 10.1016/j. knosys.2013.12.020.

[Mon+20] Juan José Montero Jimenez et al. "Towards multi-model approaches to predictive maintenance: A systematic literature survey on diagnostics and prognostics". In: Journal of Manufacturing Systems 56 (2020), pp. 539-557. ISSN: 02786125. DOI: 10.1016/j.jmsy. 2020.07.008.

[Mon+21] Juan Jose Montero Jiménez et al. "An Ontology Model for Maintenance Strategy Selection and Assessment". In: Journal of Intelligent Manufacturing. (2021). DOI: 10.1007/s10845-021-01855-3.

[Mou09] Marcelo Nascimento Moutinho. "Fuzzy diagnostic systems of rotating machineries, some Eletronorte's applications". In: 2009 15th International Conference on Intelligent System Applications to Power Systems, ISAP '09. 2009. ISBN: 9781424450985. DOI: 10.1109/ ISAP.2009.5352882.

[Mou97] John Moubray. RCM II: Reliability Centered Maintenance. Industrial Press, 1997, p. 423. ISBN: 978-0831130787.

[MS95] Salvatore T. March and Gerald F. Smith. "Design and natural science research on information technology". In: Decision Support Systems 15 (1995), pp. 251-266. ISSN: 01679236. DOI: 10.1016/0167-9236(94)00041-2.

[MU11] Kamran S. Moghaddam and John S. Usher. "Sensitivity analysis and comparison of algorithms in preventive maintenance and replacement scheduling optimization models". In: Computers and Industrial Engineering 61.1 (2011), pp. 64-75. ISSN: 03608352. DOI: 10.1016/j.cie.2011.02.012.

[Mus92] Mark A. Musen. "Dimensions of knowledge sharing and reuse". In: Computers and Biomedical Research 25.5 (1992), pp. 435-467. ISSN: 00104809. DOI: 10.1016/0010-4809(92) 90003-S.

[MV18] Juan José Montero Jimenez and Rob Vingerhoeds. "Enhancing operational fault diagnosis by assessing multiple operational modes". In: Proceedings - International Conference in Modelling, Optimization and Simulation MOSIM 2018, 27th-29th June. Toulouse, France: MOSIM2018, 2018, pp. 237-244.

[MV19] Juan José Montero Jiménez and Rob Vingerhoeds. "A System Engineering Approach to Predictive Maintenance Systems: from needs and desires to logical architecture." In: 5th IEEE Int. Symposium on Systems Engineering 2019, Edinburgh, 2019. DOI: 10.1109/ ISSE46696.2019.8984559.

[MVG21] Juan José Montero Jiménez, Rob Vingerhoeds, and Bernard Grabot. "Enhancing predictive maintenance architecture process by using ontology-enabled Case-Based Reasoning". In: 7th IEEE International Symposium on System Engineering. 2021. DOI: 10.1109/ISSE51541. 2021.9582535.

[MXJ19] Seyed M.Mehdi Hassani.N, Jin Xiaoning, and Ni Jun. "Physics-based Gaussian process for the health monitoring for a rolling bearing". In: Acta Astronatica 154 (2019), pp. 133-139.

[MZ18] Jianing Man and Qiang Zhou. "Prediction of hard failures with stochastic degradation signals using Wiener process and proportional hazards model". In: Computers and Industrial Engineering 125 (2018), pp. 480-489. ISSN: 03608352. DOI: 10.1016/j.cie.2018.09.015.

[NB17a] David Lira Nuñez and Milton Borsato. "An ontology-based model for prognostics and health management of machines". In: Journal of Industrial Information Integration (2017). ISSN: 2452414X. DOI: 10.1016/j.jii.2017.02.006.

[NB17b] David Lira Nuñez and Milton Borsato. "An ontology-based model for prognostics and health management of machines". In: Journal of Industrial Information Integration 6 (2017), pp. 33-46. ISSN: 2452414X. DOI: 10.1016/j.jii.2017.02.006.

[NB18] David Lira Nuñez and Milton Borsato. "OntoProg: An ontology-based model for implementing Prognostics Health Management in mechanical machines". In: Advanced Engineering Informatics 38 (2018), pp. 746-759. ISSN: 14740346. DOI: 10.1016/j.aei.2018.10.006.

[NM01] Natalya F. Noy and Deborah L. McGuinness. Ontology Development 101: A Guide to Creating Your First Ontology. Tech. rep. 2001. DOI: 10.1016/j.artmed.2004.01.014.

[NO17] Vladislavs Nazaruks and Janis Osis. "A survey on domain knowledge representation with frames". In: ENASE 2017 - Proceedings of the 12th International Conference on Evaluation of Novel Approaches to Software Engineering. 2017. ISBN: 9789897582509. DOI: 10.5220/ 0006388303460354.

[Nom+18] Mohammed A. Noman et al. Overview of predictive condition based maintenance research using bibliometric indicators. 2018. DOI: 10.1016/j.jksues.2018.02.003.

[NSG12] Fachri P. Nasution, Svein Sævik, and Janne K.Ø. Gjøsteen. "Fatigue analysis of copper conductor for offshore wind turbines by experimental and FE method". In: Energy Procedia 24 (2012), pp. 271-280. ISSN: 18766102. DOI: 10.1016/j.egypro.2012.06.109.

[Nyu+18] Ladislav Nyulászi et al. "Fault Detection and Isolation of an Aircraft Turbojet Engine Using a Multi-Sensor Network and Multiple Model Approach". In: Acta Polytechnica Hungarica 15.2 (2018), pp. 189-209.

[Oko+14] Caxton Okoh et al. "Overview of Remaining Useful Life prediction techniques in Throughlife Engineering Services". In: Procedia CIRP 16 (2014), pp. 158-163. ISSN: 22128271. DOI: 10.1016/j.procir.2014.02.006.

[One+18] Melis Onel et al. "Simultaneous Fault Detection and Identification in Continuous Processes via nonlinear Support Vector Machine based Feature Selection". In: Computer Aided Chemical Engineering 44 (2018), pp. 2077-2082. ISSN: 15707946. DOI: 10.1016/B978-0-444-64241-7.50341-4.

[ORM17] Criston, Okoh, Rajkumar Roy, and Jorn Mehnen. "Predictive Maintenance Modelling for Through-Life Engineering Services". In: Procedia CIRP. 2017. ISBN: 22128271 (ISSN) DOI: 10.1016/j.procir.2016.09.033. arXiv: 0208024 [gr-qc].

[PBG12] Ashok Prajapati, James Bechtel, and Subramaniam Ganesan. "Condition based maintenance: A survey". In: Journal of Quality in Maintenance Engineering 18.4 (2012), pp. 384-400. ISSN: 13552511. DOI: 10.1108/13552511211281552. arXiv: 2014WR016527 [10.1002].

[PD11] Paul Phillips and Dominic Diston. "A knowledge driven approach to aerospace condition monitoring". In: Knowledge-Based Systems 24.6 (2011), pp. 915-927. ISSN: 09507051. DOI: 10.1016/j.knosys.2011.04.008.

[PDZ10] Ying Peng, Ming Dong, and Ming Jian Zuo. "Current status of machine prognostics in condition-based maintenance: A review". In: International Journal of Advanced Manufacturing Technology 50.1-4 (2010), pp. 297-313. ISSN: 02683768. DOI: 10.1007/s00170009-2482-0. arXiv: 0208024 [gr-qc].

[Pey+09] Flavien Peysson et al. "Expert knowledge impact on damage trajectory analysis based prognostics". In: IFAC Proceedings Volumes (IFAC-PapersOnline). 2009. ISBN: 9783902661463. DOI: 10.3182/20090630-4-ES-2003.0231.

[PH08] Jim Prentzas and Ioannis Hatzilygeroudis. "Combinations of case-based reasoning with other intelligent methods". In: CEUR Workshop Proceedings. 2008. DOI: 10.3233/his 2009-0096.

[Pla95] Enric Plaza. "Cases as terms: A feature term approach to the structured representation of cases". In: First International Conference, ICCBR-95. Vol. 1. Springer Verlag, 1995, pp. 265-276. DOI: 10.1007/3-540-60598-3_24.

[PMK13] Bahareh Pourbabaee, Nader Meskin, and Khashayar Khorasani. "Multiple-Model Based Sensor Fault Diagnosis Using Hybrid Kalman Filter Approach for Nonlinear Gas Turbine Engines". In: 2013 American Control Conference (Acc). 2013. ISBN: 9781479901760. DOI: 10.1109/TCST.2015.2480003.

[Pro05] Philip E. Protter. Stochastic Integration and Differential Equations, Second Edition. Ed. by B Rozovski and M Yor. Springer, 2005.

[PS04] Sankar Pal and Simon Shiu. Foundations of soft case-based reasoning. Wiley, 2004, p. 299.

[PSD14] Panče Panov, Larisa Soldatova, and Sašo Džeroski. "Ontology of core data mining entities". In: Data Mining and Knowledge Discovery 28 (2014), pp. 1222-1265. ISSN: 13845810. DOI: 10.1007/s10618-014-0363-0.

[QA+17] Santiago Quintana-Amate et al. "A new knowledge sourcing framework for knowledge-based engineering: An aerospace industry case study". In: Computers and Industrial Engineering 104 (2017), pp. 35-50. ISSN: 03608352. DOI: 10.1016/j.cie.2016.12.013.

[Qin+16] Feiwei Qin et al. "An ontology-based semantic retrieval approach for heterogeneous 3D CAD models". In: Advanced Engineering Informatics 30 (2016), pp. 751-768. ISSN: 14740346. DOI: 10.1016/j.aei.2016.10.001.

[Qin+18] Yuchu Qin et al. "Towards an ontology-supported case-based reasoning approach for computer-aided tolerance specification". In: Knowledge-Based Systems 141 (2018), pp. 129- 147. ISSN: 09507051. DOI: 10.1016/j.knosys.2017.11.013.

[RA19] Fabrício Henrique Rodrigues and Mara Abel. "What to consider about events: A survey on the ontology of occurrents". In: Applied Ontology 14.4 (2019), pp. 343-378. ISSN: 18758533. DOI: 10.3233/AO-190217.

[Ram14] Emmanuel Ramasso. "Investigating computational geometry for failure prognostics". In: Int. Journal on Prognostics and Health Management 5.005 (2014), p. 18. ISSN: 21532648.

[Ram15] Luis Ramos. "Semantic Web for manufacturing, trends and open issues: Toward a state of the art". In: Computers and Industrial Engineering 90 (2015), pp. 444-460. ISSN: 03608352. DOI: 10.1016/j.cie.2015.10.013.

[Ras03] Carl Edward Rasmussen. "Gaussian Processes in Machine Learning". In: Advanced Lectures on Machine Learning. Ed. by Olivier Bousquet, Ulrike von Luxburg, and Gunnar Ratsch. Springer, 2003, pp. 63-71.

[RC15] Joe Raad and Christophe Cruz. "A survey on ontology evaluation methods". In: IC3K 2015 - Proceedings of the 7th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management. 2015. ISBN: 9789897581588. DOI: 10.5220/0005591001790186.

[Red12] Timothy Redmond. SPARQL Query tab for Protégé. 2012. URL: https://protegewiki stanford.edu/wiki/SPARQL{\_}Query (visited on 10/22/2020).

[RFG14] Paula Potes Ruiz, Bernard Kamsu Foguem, and Bernard Grabot. "Generating knowledge in maintenance from Experience Feedback". In: Knowledge-Based Systems 68 (2014), pp. 4-20. ISSN: 09507051. DOI: 10.1016/j.knosys.2014.02.002.

[RG10] Emmanuel Ramasso and Rafael Gouriveau. "Prognostics in switching systems: Evidential Markovian classification of real-time neuro-fuzzy predictions". In: 2010 Prognostics and System Health Management Conference, PHM '10. 2010. ISBN: 9781424447565. DOI: 10.1109/PHM.2010.5413442.

[RN12] Stuart Russel and Peter Norvig. Artificial intelligence—a modern approach 3rd Edition. 2012. ISBN: 9780136042594. DOI: 10.1017/S0269888900007724. arXiv: 9809069v1 [arXiv:gr-qc].

[Rom+14] Juan Camilo Romero Bejarano et al. "Case-based reasoning and system design: An integrated approach based on ontology and preference modeling". In: Artificial Intelligence for Engineering Design, Analysis and Manufacturing: AIEDAM 28 (2014), pp. 49-69. ISSN: 14691760. DOI: 10.1017/S0890060413000498.

[Roq18] Pascal Roques. Systems Architecture Modeling with the Arcadia Method 1st Edition. ISTE Press, 2018. ISBN: 9781785481680.

[RS89] Christopher K Riesbeck and Roger C Schank. Inside case-based reasoning. 1989. ISBN: 0-89859-767-6 (Hardcover).

[Rud20a] Ron Rudnicki. An Overview of the Common Core Ontologies 1.3. Buffalo, NY, 2020. URL: https://www.nist.gov/system/files/documents/2019/05/30/nist-ai-rfi-cubrc{\_}inc{\_}004.pdf.

[Rud20b] Ron Rudnicki. Common core ontologies. 2020. URL: https://github.com/CommonCoreOntology/ CommonCoreOntologies (visited on 07/22/2020).

[RW06] Carl Edward Rasmussen and Christopher K. I. Williams. Gaussian process for machine learning. the MIT Press, 2006.

[SA08] Abdel-Badeeh M Salem and Marco Alfonse. "Ontology versus semantic networks for medical knowledge representation". In: Proceedings of the 12th WSEAS international Conference on COMPUTERS. 2008. ISBN: 9789606766855.

[SA17] Christina M. Steiner and Dietrich Albert. "Validating domain ontologies: A methodology exemplified for concept maps". In: Cogent Education 4.1 (2017). ISSN: 2331186X. DOI: 10.1080/2331186X.2016.1263006.

[Sán+12] David Sánchez et al. "Ontology-based semantic similarity: A new feature-based approach". In: Expert Systems with Applications 39 (2012), pp. 7718-7728. ISSN: 09574174. DOI: 10.1016/j.eswa.2012.01.082.

[Sax+08] Abhinav Saxena et al. "Damage propagation modeling for aircraft engine run-to-failure simulation". In: 2008 International Conference on Prognostics and Health Management, PHM 2008. 2008. ISBN: 9781424419357. DOI: 10.1109/PHM.2008.4711414.

[SC15] Barry Smith and Werner Ceusters. "Aboutness: Towards foundations for the information artifact ontology". In: CEUR Workshop Proceedings. 2015.

[Sch+20] Sebastien Schwartz et al. "A fault mode identification methodology based on self-organizing map". In: Neural Computing and Applications 32 (2020), pp. 13405-13423.

[SHM11] Joanna Z. Sikorska, Melinda Hodkiewicz, and Lin Ma. "Prognostic modelling options for remaining useful life estimation by industry". In: Mechanical Systems and Signal Processing 25.5 (2011), pp. 1803-1836. ISSN: 08883270. DOI: 10.1016/j.ymssp.2010.11.018.

[Shu+17] Jin Shuangshuang et al. "The Remaining Life Prediction of the Fan Bearing Based on Genetic Algorithm and Multi-parameter Support Vector Machine". In: 5th International Conference on Mechanical, Automotive and Materials Engineering. 2017.

[Si+11] Xiao Sheng Si et al. "Remaining useful life estimation - A review on the statistical data driven approaches". In: European Journal of Operational Research 213.1 (2011), pp. 1-14. ISSN: 03772217. DOI: 10.1016/j.ejor.2010.11.018.

[SKY19] Emilio M. Sanfilippo, Yoshinobu Kitamura, and Robert I.M. Young. "Formal ontologies in manufacturing". In: Applied Ontology 14.2 (2019), pp. 119-125. ISSN: 18758533. DOI: 10.3233/AO-190209.

[SMS17] Karanvir Singh, Hasmat Malik, and Rajneesh Sharma. "Condition monitoring of wind turbine gearbox using electrical signatures". In: 2017 International Conference on Microelectronic Devices, Circuits and Systems, ICMDCS 2017, 2017. ISBN: 9781538617168. DOI: 10.1109/ ICMDCS.2017.8211718.

[SRC10] Abhinav Saxena, Indranil Roychoudhury, and Jose R Celaya. "Requirements Specifications for Prognostics : An Overview". In: Proceedings of AIAA Infotech@Aerospace 2010. 2010. ISBN: 9781600867439 (ISBN). DOI: 10.2514/6.2010-3398.

[Sta20] Stanford University. Protégé website. 2020. URL: https://protege.stanford.edu/ (visited on 07/22/2020).

[Sul+10] Greg P. Sullivan et al. Operations & Maintenance Best Practices: A Guide to Achieving Operational Efficiency. U. S. Departament of Energy, Federal energy management program, 2010. ISBN: 18773373463. DOI: 10.2172/1034595.

[SW15] Bernard Schmidt and Lihui Wang. "Predictive Maintenance: Literature review and future trends". In: Conference: Proceedings of the 25th International Conference on Flexible Automation and Intelligent Manufacturing 1 (2015), pp. 232-239.

[SW18] Nazmus Sakib and Thorten Wuest. "Challenges and Opportunities of Condition-based Predictive Maintenance: a Review". In: 6th CIRP Global Web Conference: "Envisaging the future manufacturing, design, technologies, and systems in innovation era". Elseiver B.V., 2018, pp. 267-272.

[Tal+19] Asma Talhi et al. "Ontology for cloud manufacturing based Product Lifecycle Management". In: Journal of Intelligent Manufacturing 30 (2019), pp. 2171-2192. ISSN: 15728145. DOI: 10.1007/s10845-017-1376-5.

[TL14] Tiedo Tinga and Richard Loendersloot. "Aligning PHM, SHM and CBM by understanding the physical system failure behaviour". In: Proceedings of the European Conference of the Prognostics and Health Management Society. 2014. ISBN: 978-1-936263-16-5.

[TSY18] Diyin Tang, Wubin Sheng, and Jinsong Yu. "Dynamic condition-based maintenance policy for degrading systems described by a random-coefficient autoregressive model: A comparative study". In: Eksploatacja i Niezawodnosc 20.4 (2018), pp. 590-601. ISSN: 15072711. DOI: 10.17531/ein.2018.4.10.

[Vac+07] George Vachtsevanos et al. Intelligent Fault Diagnosis and Prognosis for Engineering Systems. 2007.ISBN:047172999X.DOI:10.1002/9780470117842.

[VBD17] Kim Verbert, Robert Babuska, and Bart De Schutter. "Bayesian and Dempster-Shafer reasoning for knowledge-based fault diagnosis-A comparative study". In: Engineering Applications of Artificial Intelligence 60 (2017), pp. 136-150. ISSN: 09521976. DOI: 10. 1016/j.engappai.2017.01.011.

[VD18] Wim J.C. Verhagen and Lennaert W.M. De Boer. Predictive maintenance for aircraft components using proportional hazard models. 2018. DOI: 10.1016/j.jii.2018.04.004.

[VDB15] Kim Verbert, Bart De Schutter, and Robert Babuška. "Reasoning under uncertainty for knowledge-based fault diagnosis: A comparative study". In: IFAC-PapersOnLine 48 (2015), pp. 422-427. ISSN: 24058963. DOI: 10.1016/j.ifacol.2015.09.563.

[Vep91] Rajan Vepa. "Introduction to fuzzy logic and fuzzy sets". In: Application of artificial intelligence in process control. (L. Boullart, A. Krijgsman and R.A. Vingerhoeds; editors). 1991, pp. 146-163.

[Vin+95] Rob A. Vingerhoeds et al. "Enhancing off-line and on-line condition monitoring and fault diagnosis". In: Control Engineering Practice 3.11 (1995), pp. 1515-1528. ISSN: 09670661. DOI: 10.1016/0967-0661(95)00162-N.

[VM18] David Vališ and Dariusz Mazurkiewicz. "Application of selected Levy processes for degradation modelling of long range mine belt using real-time data". In: Archives of Civil and Mechanical Engineering 18.4 (2018), pp. 1430-1440. ISSN: 16449665. DOI: 10.1016/j.acme.2018.05.006.

[Von+18] Alexander Von Birgelen et al. "Self-Organizing Maps for Anomaly Localization and Predictive Maintenance in Cyber-Physical Production Systems". In: Procedia CIRP 72 (2018), pp. 480-485. ISSN: 22128271. DOI: 10.1016/j.procir.2018.03.150.

[VWD14] Gregory W. Vogl, Brian Weiss, and Alkan Donmez. "Standards for Prognostics and Health Management ( PHM ) Techniques within Manufacturing Operations". In: Annual Conference of the Prognostics and Health Management Society. 2014. ISBN: 9781936263172.

[Wan+08] Tianyi Wang et al. "A similarity-based prognostics approach for remaining useful life estimation of engineered systems". In: 2008 International Conference on Prognostics and Health Management, PHM 2008. 2008. ISBN: 9781424419357. DOI: 10.1109/PHM.2008. 4711421.

[Wan+14] Yuanhang Wang et al. "A corrective maintenance scheme for engineering equipment". In: Engineering Failure Analysis 36 (2014), pp. 269-283. ISSN: 13506307. DOI: 10.1016/j. engfailanal.2013.10.006.

[Wan+18] Anping Wan et al. "Prognostics of gas turbine: A condition-based maintenance approach based on multi-environmental time similarity". In: Mechanical Systems and Signal Processing 109 (2018), pp. 150-165. ISSN: 10961216. DOI: 10.1016/j.ymssp.2018.02.027.

[Wel92] Gordon Wells. "An introduction to neural networks". In: Application of artificial intelligence in process control. (L. Boullart, A. Krijgsman and R.A. Vingerhoeds; editors). 1992, pp. 164- 200.

[WHF18] Zhao Qiang Wang, Chang Hua Hu, and Hong Dong Fan. "Real-Time Remaining Useful Life Prediction for a Nonlinear Degrading System in Service: Application to Bearing Data". In: IEEE/ASME Transactions on Mechatronics 23.1 (2018), pp. 211-222. ISSN: 10834435. DOI: 10.1109/TMECH.2017.2666199.

[Wor12] World Wide Web Consortium. OWL 2 Web Ontology Language. 2012. URL: http://www w3.org/TR/2012/REC-owl2-overview-20121211/ (visited on 02/01/2020).

[WTM17] Dong Wang, Kwok Leung Tsui, and Qiang Miao. "Prognostics and Health Management: A Review of Vibration Based Bearing and Gear Health Indicators". In: IEEE Access 6 (2017), pp. 665-676. ISSN: 21693536. DOI: 10.1109/ACCESS.2017.2774261.

[Wu+18] Zhenyu Wu et al. "K-PdM: KPI-Oriented Machinery Deterioration Estimation Framework for Predictive Maintenance Using Cluster-Based Hidden Markov Model". In: IEEE Access Vol 6.DOI: 10.1109/ACCESS.2018.2859922 (2018), pp. 41676-41687. ISSN: 21693536. DOI: 10.1109/ACCESS.2018.2859922.

[Yan+04] Bo Suk Yang et al. "Case-based reasoning system with Petri nets for induction motor fault diagnosis". In: Expert Systems with Applications 27.2 (2004), pp. 301-311. ISSN: 09574174. DOI: 10.1016/j.eswa.2004.02.004.

[YN18] Ali Yahyatabar and Amir Abbas Najafi. "Condition based maintenance policy for series-parallel systems through Proportional Hazards Model: A multi-stage stochastic programming approach". In: Computers and Industrial Engineering 126 (2018), pp. 30-46. ISSN: 03608352. DOI: 10.1016/j.cie.2018.09.014.

[YSJ17] Kam Chuen Yung, Bo Sun, and Xiaopeng Jiang. "Prognostics-based qualification of highpower white LEDs using Lévy process approach". In: Mechanical Systems and Signal Processing 82 (2017), pp. 206-216. ISSN: 10961216. DOI: 10.1016/j.ymssp.2016.05.019.

[ZBD16] Deyi Zhang, Andrew D. Bailey, and Dragan Djurdjanovic. "Bayesian Identification of Hidden Markov Models and Their Use for Condition-Based Monitoring". In: IEEE Transactions on Reliability (2016). ISSN: 00189529. DOI: 10.1109/TR.2016.2570561.

[Zer+17] Noureddine Zerhouni et al. "Prognostics and Health Management for Maintenance Practitioners Review, Implementation and Tools Evaluation". In: Article in International Journal of Prognostics and Health Management 8.60 (2017), p. 31. ISSN: 22129685. DOI: 10.1016/j.euprot.2015.07.015.

[Zha+17] Rui Zhao et al. "Machine Health Monitoring Using Local Feature-based Gated Recurrent Unit Networks". In: IEEE Transactions on Industrial Electronics 65.2 (2017), pp. 1539 1548. ISSN: 0278-0046. DOI: 10.1109/TIE.2017.2733438.

[Zha+18a] Zhengxin Zhang et al. "Degradation data analysis and remaining useful life estimation: A review on Wiener-process-based methods". In: European Journal of Operational Research 271.3 (2018), pp. 775-796. ISSN: 03772217. DOI: 10.1016/j.ejor.2018.02.033.

[Zha+18b] Shuai Zhao et al. "Evaluation of Reliability Function and Mean Residual Life for Degrading Systems Subject to Condition Monitoring and Random Failure". In: IEEE Transactions on Reliability 67.1 (2018), pp. 13-25. ISSN: 00189529. DOI: 10.1109/TR.2017.2779322.

[Zho+10] Zhi Jie Zhou et al. "A model for real-time failure prognosis based on hidden Markov model and belief rule base". In: European Journal of Operational Research 207.1 (2010), pp. 269- 283. ISSN: 03772217. DOI: 10.1016/j.ejor.2010.03.032.

[Zho+14] Zhi Jie Zhou et al. "A model for online failure prognosis subject to two failure modes based on belief rule base and semi-quantitative information". In: Knowledge-Based Systems (2014). ISSN: 09507051. DOI: 10.1016/j.knosys.2014.06.026.

[ZM07a] Yimin Zhan and Chris K. Mechefske. "Robust detection of gearbox deterioration using compromised autoregressive modeling and Kolmogorov-Smirnov test statistic-Part I: Compromised autoregressive modeling with the aid of hypothesis tests and simulation analysis". In: Mechanical Systems and Signal Processing 21.5 (2007), pp. 1953-1982. ISSN: 08883270. DOI: 10.1016/j.ymssp.2006.11.005.

[ZM07b] Yimin Zhan and Chris K. Mechefske. "Robust detection of gearbox deterioration using compromised autoregressive modeling and Kolmogorov-Smirnov test statistic. Part II: Experiment and application". In: Mechanical Systems and Signal Processing 21.5 (2007), pp. 1983-2011. ISSN: 08883270. DOI: 10.1016/j.ymssp.2006.11.006.

[ZYX17] Qiang Zhou, Ping Yan, and Yang Xin. "Research on a knowledge modelling methodology for fault diagnosis of machine tools based on formal semantics". In: Advanced Engineering Informatics 32 (2017), pp. 92-112. ISSN: 14740346. DOI: 10.1016/j.aei.2017.01.002.

[ZYZ15] Anmei Zhou, Dejie Yu, and Wenyi Zhang. "A research on intelligent fault diagnosis of wind turbines based on ontology and FMECA". In: Advanced Engineering Informatics 29.1 (2015), pp. 115-125. ISSN: 14740346. DOI: 10.1016/j.aei.2014.10.001.

<div align="center">

# A fault mode identification methodology based on self-organizing maps

</div>

Intentionally left blank

ORIGINAL ARTICLE


> **Figure Description:**

Brand icon



<div align="center">

# A fault mode identification methodology based on self-organizing map

</div>

Sébastien Schwartz $ ^{1,2} $ $ \textcircled{D} $ · Juan José Montero Jimenez $ ^{2,3} $ · Michel Salaun $ ^{2} $ · Rob Vingerhoeds $ ^{2} $

Received: 14 January 2019/Accepted: 18 December 2019/Published online: 1 January 2020 $ \textcircled{c} $ Springer-Verlag London Ltd., part of Springer Nature 2020

## Abstract

One of the main goals of predictive maintenance is to be able to trigger the right maintenance actions at the right moment in time building upon the monitoring of the health status of the concerned systems and their components. As such, it allows identifying incipient faults and forecasting the moment of failure at the earliest stage. Many different data-driven methods are used in such approaches (Naderi and Khorasani in 2017 IEEE 30th Canadian conference on electrical and computer engineering (CCECE), Windsor, ON, IEEE, pp 1-6, 2017. https://doi.org/10.1109/ccece.2017.7946715; Sarkar et al. in J Eng Gas Turbines Power 1338(8):081602, 2011. https://doi.org/10.1115/1.4002877; Svärd et al. in Mech Syst Signal Process 45(1):170-192, 2014. https://doi.org/10.1016/j.ymssp.2013.11.002; Pourbabaee et al. Mech Syst Signal Process 76-77:136-156, 2016. https://doi.org/10.1016/j.ymssp.2016.02.023). This work uses the self-organizing maps (SOMs) or Kohonen map, thanks to its ability to emphasize underlying behavior such as fault modes. An automatic fault mode detection is presented based on a SOM network and the kernel density estimation with as less as possible prior knowledge. The different SOM development steps are presented and the suitable solutions proposed to structure the approach are accompanied by mathematical methods. The generated maps are then used with kernel density analysis to isolate fault modes on them. Finally, a methodology is presented to identify the different fault modes. The work is illustrated with an aircraft jet engines case study.

Keywords Diagnostic · Fault identification · Predictive maintenance · Self-organizing map

## 1 Introduction

Maintenance departments are confronted with three types of maintenance: corrective maintenance (i.e., correcting systems that break down or have a deteriorated functional behavior), preventive maintenance (i.e., maintenance actions at regular intervals, to avoid break down or deterioration) and predictive maintenance (i.e., performing specific maintenance actions based on indications derived

from fine analysis on data, crew reports, etc.). Predictive maintenance has seen a huge rise over the last years, essentially due to the application of neural networks to identify incipient faults and to forecast the moment of failure through the diagnostic phase. Depending on the monitored data, there are different types of classification for diagnostic system (Fig. 1). Machine fault diagnostic approaches are grouped into model-based [1-3] and data-driven [4-7] techniques.

In this paper, a hybrid approach for a "process historybased" diagnosis with quantitative data through the combination of a neural network (NN) with a probability density function (PDF) is scoped. In particular, an unsupervised neural network (UNN) type, the self-organizing map (SOM), or Kohonen map, is used. This NN has already shown its effectiveness in the past [9] but requires substantial knowledge on the neural network type itself, making it complex to comprehend and frequently requiring "manual" rework. Therefore, the presented novel approach



<div align="center">

Fig.1 Classification of diagnostic methods based on [8]. QTA qualitative trend analysis, PDF probability density function, PCA principal component analysis

</div>


> **Figure Description:**

This diagram illustrates a hierarchical classification of diagnostic methods, starting from the root node labeled "Diagnostic Methods." This root branches into three primary categories: "Quantitative Model-Based," "Qualitative Model-Based," and "Process History Based."

The "Quantitative Model-Based" branch further divides into "Input-Output Models" and "First Principles Models." The "Qualitative Model-Based" branch splits into "Causal Models" and "Abstraction Hierarchy." The "Causal Models" node branches into "Fault Trees" and "Digraphs," while the "Abstraction Hierarchy" node branches into "Structural" and "Functional."

The "Process History Based" branch splits into "Qualitative" and "Quantitative" categories. The "Qualitative" branch further divides into "Expert Systems" and "QTA." The "Quantitative" branch splits into "Statistical" and "Non statistical." The "Statistical" node branches into "PDF" and "PCA," while the "Non statistical" node branches into "Neural Network." All relationships are represented by downward-pointing arrows indicating the hierarchical structure.



aims at automating as much as possible for the development of the SOM. The first objective is to reduce to the minimum level of the interaction between the expert knowledge and the network itself. The complete process is reviewed, and, for each step in the process, mathematical methods are proposed. It leads to a more structured and automatable procedure with an intent to make the method more accessible and autonomous. The second objective is to manage automatically the output of the SOM with PDFs to identify fault modes.

The goal of this paper is to present a fully autonomous toolchain that identifies the fault modes from input sensors by reducing as much as possible the prior knowledge and the expert intervention.

The paper is organized as follows: In the second section, predictive maintenance is introduced. In the third section, the self-organizing map is presented, as well as the different possibilities to enhance the approach and a methodology to identify the fault modes. The fourth section exposes and applies the methodology on the case study of aircraft engines. The paper concludes with some general observations and indications for future work.

## 2 Predictive maintenance

Keeping a technical system in optimal operational conditions is key for a successful and an efficient use of the system. Interruptions of operations not only have a negative impact (e.g., delayed flights, internet connections not being available, etc.), but may also have worst consequences (e.g., image of the company impacted, people will tend to privilege other suppliers, loss of income, etc.). Maintaining a system in optimal state of operation also means having timely maintenance actions to ensure the intended functionality and to avoid potential failures to occur. A good combination of corrective, preventive and

predictive maintenance is required [10]. Whereas corrective maintenance is based on alarm handling, troubleshooting for corrective actions, etc., predictive maintenance relies on offline diagnostic task analyses such as recorded data, crew reports, maintenance logs and other data recordings on the actual health state of the system. Such information is then used by operation departments to assess the health state and derive necessary maintenance actions and their planning if necessary.

Condition monitoring is used to assess the current health state of the system at hand. It uses pattern recognition in time series of monitored data and classifies those patterns as known conditions. While this is used to be done by human experts [9], requiring great skill and experience from the expert, software tools have appeared to support engineers in such activities.

As predictive maintenance aims to define the best possible moment to trigger maintenance actions [9], it gained more and more attention over the last few years. One of the solutions discussed in the literature for early detection and classification of failures during the diagnostic phase is the self-organizing map (SOM) originally proposed by Kohonen [11]. This approach allows to detect degradation patterns and the nature of the problem and to derive the remaining useful life [9, 10, 12]. This network has been widely used on various application fields for its particular abilities [13-18].

Visualization helps humans to understand diagnostic tasks. According to [19], the visualization of the data helps to gain an understanding of an unknown dataset. For limited amounts of dimensions in data, humans can do it, but the perception is limited to three dimensions. High-dimensional data visualization with more than three features is therefore unreachable. To address this issue, several visualization techniques were developed such as principal component analysis (PCA) [20], self-organized maps (SOMs) [11] or Sammon mapping [21]. Those techniques



rely on dimension reduction to visualize on 2D or 3D plots. This dimension reduction therefore generates new knowledge to be labeled for the analysis. Labeling data using prior knowledge or human reasoning become complicated on high dimensions [22], which could induce errors. Approaches relying on unsupervised learning are interesting thanks to their abilities to deal with high-dimensional data without prior knowledge. Therefore, a SOM network answers to the requirements: visualize high-dimensional data on 2D maps and obtain knowledge generated from these maps.

The successful implementation of SOM for diagnostic tasks requires an in-depth analysis of data obtained from the system at hand. It involves the assessment of data interdependency, the analysis on how many different faults/failures can be identified in the data, the distinction of eventual operational modes (if necessary) and, finally, successful training and subsequent validation of the SOM. Such analysis requires a good knowledge on the application domain itself and the measured data, in addition to strong knowledge on SOMs. In the next section, the fault mode diagnosis approach is presented. Each step of the SOM neural network is revisited and analyzed to see "whether and how" improvements may be obtained to automatize the use of SOM neural networks and to reduce the need for prior knowledge. Then, probability density function on the neural network output is used to identify faults of the supervised system.

## 3 Fault mode diagnosis using self-organizing maps

## 3.1 Overview

As presented previously, fault diagnosis requires human intervention and prior knowledge. The proposed methodology (Fig. 2) attempts to perform an automatic fault mode diagnosis with as less as possible prior knowledge. The self-organizing map neural network is the core of the methodology as a tool to emphasize the input data through a map representation. The underlying information such as faults becomes more accessible. The approach has been structured into three phases.

The first step is "input data management". Input data (raw monitored sensors) have to be formatted and used with the neural network. This sensor management involves the choice of useful variables to decrease the complexity and the size the neural network. In addition, the data are normalized to facilitate the network training.

data. During the testing phase, the network outputs a localization on the previously trained map.

The second step is "system map." The formatted input data are presented to the neural network. For the training phase, the network generates maps representing the input

The last step is the "fault mode identification". The localization on the map (output of the previous stage) enables the identification of the fault mode thanks to a mathematical procedure based on the probability density function.

In the following sections, each step (Fig. 2) will be described more in detail.

## 3.2 Input data management

As presented previously, a selection among raw monitored data is performed. This procedure is called feature selection (see [23-26]). It is used on structured data to select features that explain most of the system behaviors by eliminating inappropriate and redundant data [23]. This paper will only focus on time-series data. Some basic approaches provide good means to address the feature selection. For example, the variance is a good way to eliminate features with little or no evolution. The correlation coefficient is powerful to identify feature that have the same behavior. Visual analysis highlights features that have unusual trend.

For better analysis purpose, a normalization of the input data is performed. It provides a common scale for the features. Two main methods are used: rescaling and standardizing. The rescaling method is the simplest one and consists to scale data on the range [0,1] with the following formula:

$$
\bar {x} _ {i j} = \frac {x _ {i j} - \min _ {i} x _ {i j}}{\max _ {i} x _ {i j} - \min _ {i} x _ {i j}}
$$

where $ x_{ij} $ and $ \bar{x}_{ij} $ are, respectively, the original and normalized data values for a sample j of a feature i from the input dataset, with $ i=1\dots p $ ,where p is the number of network input.

The standardizing method uses the following formula:

$$
\bar {x} _ {i j} = \frac {x _ {i j} - \mu_ {i}}{\sigma_ {i}}
$$

where $ \mu_{i} $ and $ \sigma_{i} $ are, respectively, the mean and the standard deviation of a feature i. Even if this method provides a uniform scale, normalized inputs data do not belong to the same common scale. That is why the rescaling method will be used to have all input data on the same range [0,1].

## 3.3 System map

## 3.3.1 Overview

Self-organizing maps are neural networks using unsupervised learning inspired from human brain way [11]. They



<div align="center">

Fig.2 Fault mode diagnosis methodology

</div>


> **Figure Description:**

This diagram illustrates a process flow divided into three main sections: Input Data Management, Fault Mode Identification, and System Map. The Input Data Management section contains a Pre-processing box with a Data sub-section listing "Select feature" and "Normalize input data." An arrow flows from this section into the System Map section. The Fault Mode Identification section contains a Fault modes box listing "Quantification," "Identification," and "Association," with a feedback loop labeled "For each clusters" and an arrow pointing back from the Fault Mode Identification section to the System Map section.

The System Map section is a large container encompassing three sub-processes: Pre-processing, Training, and Labelling. The Pre-processing box lists "Map" with sub-items "Determine size," "Initialize neurons," and "Set training parameters." The Training box lists "Data" with sub-items "Present observations," "Find the BMU*," and "Update the neurons." This leads to a diamond-shaped decision node labeled "Convergence criteria." If "No," the process loops back to the start of the Training data steps; if "Yes," it proceeds to a "Map trained" box. The Labelling box contains two sections: "Map" with "Cluster identification" and "Data" with "Present observation," "Find the BMU*," and "Add information," with a feedback loop labeled "Whole dataset." A footnote at the bottom defines "*BUM: Best Matching Unit."



are suitable to produce a low-dimensional representation of the input space of training samples, called a map, to visualize high-dimensional data [27]. SOMs are therefore useful for dimensionality reduction and representation in which the similarity relations between input data are preserved [10]. Its competitive learning capability and the use of the neighborhood function preserve the topological properties of the inputs. The competitive approach aims to put output neurons in competition with each other to be activated, and the winning neuron is the only one that can be activated. As most artificial neural networks, SOMs are developed in two subsequent phases: a training phase and a testing phase. Thanks to the characteristics of this particular neural network, the testing phase can also be used as a labeling part, which is the assignment of information to specific clusters on the map, such as specific faults, or system operational conditions. The goal of the training phase is to teach the algorithm with the dataset in such a way that similar data features are clustered on specific topological regions on the map [28]. Then, the generated map provides clusters, and a health index (HI) is estimated for each node, depicting the degradation status of the studied system.

The SOM neural network building is divided into three stages: preprocessing, training and labeling. A lot of manual work done by experts is needed to perform these tasks.

## 3.3.2 Preprocessing

SOM topologies can be in one, two or even three dimensions [29-33]. The neurons are localized at lattice nodes. The original SOM [11] is a 2D hexagonal map. Then,

successively, 1D lines, 2D rectangular grids or more complex structures, such a star lattices [34] (Fig. 3), have been created. For our case study, a 2D square lattice is used to visualize it as picture.

A square lattice has $ n\times n $ neurons of m weights. The number of weights per group (i.e., m) corresponds to the number of inputs to the network. According to [35], a size of the map can be determined by calculating the number of neurons from the number of observations in the dataset such as:

$$
M \cong 5 \sqrt {N}
$$

where M is the number of neurons, and N is the number of observations. A square lattice will have n= $ \sqrt{M} $ . For example, with about 10,000 observations, Eq. (3) leads to a size M $ \cong $ 500. For a square lattice, the closest dimension would be a $ 23\times 23 $ matrix.

The next step is the map initialization. There are various ways to set initial weights, such as input vectors randomly selected [36], principal components of the input space [36], large hypercube [37] or random values. A uniform distribution in the range [0,1] with a probability density function of 1 is considered for usefulness to set neuron weight vectors $ w_{ij}=\left(w_{ij1},w_{ij2},\dots,w_{ijm}\right) $ with i,j=1...n.

## 3.3.3 Training phase

After the input data are processed and the map is initialized, the map is trained using preprocessed data. Training algorithms related to SOMs are various. Stochastic training as Algorithm 1 is one of the most classical algorithms [38]. Alternatives such as fast batch SOM [39] or growing self-



<div align="center">

Fig.3 Examples of lattice structures

</div>


> **Figure Description:**

The image displays four distinct network topologies, each represented by nodes (circles) connected by lines. From left to right, the first is labeled "Hexagonal" and consists of 19 nodes arranged in a hexagonal lattice pattern, where each interior node is connected to six neighbors. The second is labeled "Linear" and consists of four nodes connected in a single straight horizontal line. The third is labeled "Square" and consists of 16 nodes arranged in a 4x4 grid, where each interior node is connected to four neighbors. The fourth is labeled "Star" and consists of 13 nodes, featuring a central node connected to six radial arms, each containing two additional nodes, forming a six-pointed star configuration.



organizing map (GSOM) [40] can be faster but are more complex to use. They all rely on the determination of the best matching unit (BMU), which is the smallest distance between the input vector and the weight vector of the map nodes.

The learning process is iterative, until a stopping criterion is met. Examples of criteria are an error estimation such as the quantization error [36] or the so-called "rule of thumb" where the number of steps must be at least 500 times the number of neurons in the map [38]. This last

<div align="center">

Algorithm 1. Randomly input selection for self-organizing map

</div>

For t from 1 to Number_Of_Iteration do

Pick up a random input vector among the input dataset

For each node in the map do

Calculate the distance between input vector and map node weight vector

Track the node with the smallest distance (i.e. BMU)

End

Update the weight vector of the neighborhood of the BMU node and itself

End

The weight vector is updated at each iteration as follows:

$$
\left\{ \begin{array}{l l} w _ {i j} (t + 1) = w _ {i j} (t) + h _ {k l, i j} (t) \left[ x (t) - w _ {i j} (t) \right] & \forall n _ {i j} \in \mathbb {E} _ {B M U} \\ w _ {i j} (t + 1) = w _ {i j} (t) \quad \forall n _ {i j} \notin \mathbb {E} _ {B M U} \end{array} \right.
$$

where $ w_{ij} $ is the vector weight, $ t $ is the $ t^{th} $ iteration, $ h_{kl,ij} $ is the neighborhood function, $ x(t) $ is the input observed, $ n_{ij} $ is the node on the map, $ ij $ are the node coordinates on a 2D lattice, $ kl $ are the BMU node coordinates on the same 2D lattice and $ \mathbb{E}_{BMU} $ is the space of BMU neighborhood node and itself. This space is defined by the width of the neighborhood function, also called the BMU radius. A smooth Gaussian kernel is mostly used for the neighborhood function [36, 41]:

$$
h _ {k l, i j} (t) = \eta (t) \cdot e ^ {\frac {- w _ {k l} (t) - w _ {i j} (t) ^ {2}}{2 \sigma^ {2} (t)}}
$$

where $ \eta (t) $ and $ \sigma (t) $ are, respectively, the learning rate and the width of the kernel, which are the decreasing functions of time [36, 38]. This function decreases through the time to improve the neighborhood identification.

The BMU node $ n_{kl} $ is defined by:

$$
\left\{n _ {k l} | x (t) - w _ {k l 2} ^ {2} = \arg \min _ {i j} x (t) - w _ {i j} (t) _ {2} ^ {2} \right\}
$$

criterion will be used in this paper.

The SOM training speed is linked to the map size, the number of inputs and the number of samplings. The number of weights could be large, which leads to a slow convergence due to the amount of weight updates involved in each iteration. Several mechanisms have been developed to address this problem, such as optimizing the width of the neighborhood function or learning rate function. According to [36, 41], the Gaussian kernel is a good candidate. The width of the neighborhood function $ \sigma (t) $ is chosen as:

$$
\sigma (t) = \sigma_ {0} \cdot e ^ {- t / \tau_ {1}}
$$

where $ \sigma_{0} $ is an initial variance set to the map size divided by two [38], and $ \tau_{1} $ is a positive constant. The learning rate function $ \eta(t) $ is chosen as:

$$
\eta (t) = \eta_ {0} \cdot e ^ {- t / \tau_ {2}}
$$

where $ \eta_{0} $ is an initial learning rate set to 0.9 [38], and $ \tau_{2} $ is a positive constant. The function is limited to a minimum set at 0.01 [38].

For convenience, $ \tau_{1} $ and $ \tau_{2} $ are equal and follow the relation:

$$
\tau_ {i} = t _ {\max } / \ln \sigma_ {0} \quad \mathrm {w i t h} i = 1, 2
$$

where $ t_{\mathrm{max}} $ is the maximal number of iterations. Those constants lead the exponential decay function radius to 1 when t reaches it maximum value, which is the maximal number of iterations [42].



With this proposed training, the network is able to adapt automatically to the presented input data. There is no need for an objective function as in supervised learning. The main disadvantage is related to the map size. For the training phase, the computational needs increase exponentially with the map size. The inference phase has lower computational needs compared to the training phase. The output is a map that depicts the used dataset as a representation in lower dimension.

## 3.3.4 Labeling phase

The goal of the labeling phase is to attribute additional information, such as the name, the color or the number of a cluster. Additional information relies on user's needs and is linked to the application. The generated map has observable clusters. Instead of identifying them manually, an automatic cluster identification phase has been created to do so.

The cluster identification phase wants to identify nodes that make up clusters and assign an information to the cluster to which they belong. The classification of map nodes is performed with Algorithm 2. It generates automatically clusters surrounded by boundaries, and an identifier is assigned to them. For example, if the node 43 with the coordinate (4,3) is localized inside the cluster "2," then this value is attributed to the node.

$$
H _ {i j} = \frac {w _ {i j 2} - \min _ {(i , j) \in C} w _ {i j 2}}{\max _ {(i , j) \in C} w _ {i j 2} - \min _ {(i , j) \in C} w _ {i j 2}}
$$

in which scale node values of each cluster are in the range [0,1]. Those values represent the current state of the studied system. Each cluster has a degradation trend. For a node, a high HI value represents a healthy condition, whereas a low HI indicates a high degradation or a failure.

When a database with more than one fault mode is used to train the network, several subregions could appear on some clusters. Those subregions are linked to different fault modes related to part failures. To identify fault modes automatically, input data need to be labeled through the diagnostic phase.

The diagnostic phase aims at creating knowledge for the fault identification phase. The input data from the training set are again presented to the map. BMU searching provides the cluster number to which they belong and the associated HI. It leads to the input association using Algorithm 3. The building of the fault mode indication becomes possible by knowing exactly which sample appears in which clusters to localize occurring faults.

<div align="center">

Algorithm 2. Cluster identification

</div>

For each Node on the Map not seen do

While Node is not a Boundary And has NeighborhoodNodes which are not Boundary do Attribute ClusterLabel

Attribute ClusterLabel

End

Increment ClusterLabel

End

<div align="center">

Algorithm 3. Diagnostic of input data

</div>

For each Sample in Input Data do

Present the sample to the map and localize the exited BMU node

Association to the sample : the cluster number and HI of the BMU node

End

A Node is considered as seen if it has been assigned to a cluster identifier, called ClusterLabel. NeighborhoodNodes are nodes that touch it in all four directions: up, down, left and right.

In the end, a map is generated in which cluster regions appear and are defined by boundaries surrounding them. Let us recall that weight vectors are associated with each node of the map. Then, for each cluster, a health index is built for nodes $ ( i,j) $ that belong to cluster C by Eq. (10)

## 3.4 Fault modes identification

The identification of the fault modes gives an insight on the system state, such as the probability that a specific fault occurs, or its evolution through the time. Without prior knowledge about datasets, the number of faults is estimated through the fault quantification phase. Their area on the map is approximated thanks to a straightforward methodology based on probabilistic theory during the fault



subregions identification phase. Then, by presenting iteratively datasets with one associated fault to a map, that has one or more unknown fault, the fault modes association phase identifies the unknown faults.

## 3.4.1 Fault quantification

The fault quantification phase attempts to evaluate automatically the number of different system faults from a dataset (e.g., pressure drop and over-temperature are two different errors). Within a given time series of data referred to as cycles of a specific system, it can be assumed that the last cycle before non-recoverable error corresponds to the error state and can be used to identify faults [43]. At this cycle, the system is considered to be in a defect state and is taken out of service for maintenance actions. Before the stopping of the system, the advanced degradation of parts that were about to fail took place. This should be visible in the dataset. So, the last cycles of the system before breakdown are presented to the SOM and the labeling phase provides the best matching unit (BMU) (i.e., the hit node on the SOM map). The hit BMU can be the same for several instances of the system (for example, different aircraft jet engines belonging to the same family). The quantity of instances hitting this BMU indicates the hit number.

Two ways to estimate the hit number are now introduced:

- H1: using the last cycle of the system

- H2: using the last cluster hit of the system

In the first case, H1, there is only one last hit on a specific cluster for the system. For example, in a dataset with 249 systems, there are 249 last hits, shared by all map clusters, representing the final (most likely) faulty condition in which the system is found to be itself before it was stopped for maintenance. It represents a "sure" faulty condition.

In the second case, H2, the last hit for each system in each cluster is taken into consideration. Then, in the dataset with 249 systems, there are 249 last hits on each cluster. In the case of a six clusters map, this leads to 1494 last hits, representing faulty conditions for those operational conditions.

In the next section, it is shown that H2 provides more information and reliability than H1, and it is a decent approximation. H2 is used for the case study.

The frequency of those hits over each map cluster is linked to the fault number. Indeed, they tend to gather in areas that can be distinguished separately. Those hits are managed with tools from probability theory to build a representation of those subregions. A good candidate is the

probability density function (PDF). The kernel density estimator [44] provides the estimation of the PDF such as:

$$
\hat {f} _ {h} (\vec {x}) = \frac {1}{n \cdot h} \sum_ {i = 1} ^ {N} K \left(\frac {\vec {x} - \overrightarrow {x _ {i}}}{h}\right)
$$

where $ \vec{x}=\left(x^{1},x^{2},\dots,x^{p}\right) $ are real values, $ \overrightarrow{x_{i}} $ are random samples from an unknown distribution, N is the number of observation, K is the kernel smoothing function, which is a Gaussian kernel, and h is the bandwidth. In this study, the bandwidth has been selected at 1% of the SOM map size, leaving out of consideration the boundary nodes between fault clusters. For a map of $ 2 5 \times2 5 $ nodes without cluster, $ h=0.2 5 $ . According to the targeted application, the rule could evolve. Other kernel parameters are automatically estimated by the algorithm [45]. The PDF represents the probability distribution using the data samples where the kernel distribution sums the smoothing functions for each data value to produce a smooth, continuous probability curve. A 3D-PDF generation is used for each subregion, with node coordinate $ (x,y) $ and the hit number as a frequency as z coordinate. The generated function can be estimated at any $ (x,y) $ point. The number of peaks of the PDF leads to the number of faults inside each map cluster. Therefore, if a dataset has one or two fault modes, the method should lead, respectively, to one and two peaks for each cluster on the map. The goal of this approach is to be able to get an overview on the number of fault modes that are present in a dataset, without relying on a priori information.

## 3.4.2 Fault subregion identification

A cluster is surrounded by boundaries, and several small subregions can be estimated inside, related to fault modes. Fault subregions are the extracted regions from a cluster. They are generated from the separation of PDF peaks for a cluster and are used to define each fault area. Indeed, PDF uses Gaussian functions, which can be separated geometrically. However, all cluster nodes are not necessarily classified in a fault area. This is the case for nodes with weak PDF value, far away from the peak center. To address this problem, the PDF of a cluster is estimated at every cluster node. A custom threshold is applied on each estimated PDF, and fault areas are then generated with their own self-defined boundaries. The remaining nodes inside each fault area, after applying the threshold, represent the failure. So, if the node (4,3) is inside the subregion Failure 1, then this node is attributed to it.

## 3.4.3 Fault modes association

The association of fault modes (i.e., subregions of cluster) with a physical part is performed with similar data, which



present a known defect mode. Prior knowledge about fault modes, which is previously identified, is used. For example, a dataset with one fault mode is presented to a generated map that has been trained with a dataset with two fault modes. The presented dataset will excite nodes from one of the two subregions previously determined. This subregion will correspond to the known fault mode of the presented dataset.

## 4 Case study on aircraft jet engines

## 4.1 Overview

To illustrate the present work, a case study on diagnosing jet engines is used. Engine condition monitoring (ECM) allows for regular assessment of the jet engine health state, based on in-flight measured variables on the engine itself, as well as its environment (the aircraft) in its flight conditions. Specific parameter trend evolutions have shown to be early indications for engine degradations, failures and/or malfunctions [9]. Engine condition monitoring consists of a wide range of activities assessing the jet engine health, from the mounting on-wing until its removal. After every flight, performance engineers evaluate the evolution of engine critical parameters and derive from those analyses to anticipate or to avoid incidents, to evaluate the effects of incidents or to provide a clear "no problem for the next few flights" indication. Whenever an engine gets into a much deteriorated health state, no longer allowing operation within regulatory limits, the performance engineer recommends its removal and a precise planning. Actions of the performance engineer aim not only to keep the engine in its optimum operational condition, but also to correct in an


> **Figure Description:**

This diagram illustrates the cross-sectional schematic of a turbofan jet engine. The engine is depicted horizontally, with air flowing from left to right. At the front (left) is a vertical blue bar labeled "Fan." Behind the fan, the engine core consists of a series of compressor stages labeled "LPC" (Low-Pressure Compressor) in dark blue, followed by "HPC" (High-Pressure Compressor) in a lighter tan color. 

Moving further into the engine, there is a red section labeled "Combustor." Behind the combustor are two turbine sections: "HPT" (High-Pressure Turbine) in tan and "LPT" (Low-Pressure Turbine) in dark blue. The engine terminates at the rear (right) with a "Nozzle." The internal rotating shafts are labeled "N1" and "N2," with N1 connecting the fan and LPT, and N2 connecting the HPC and HPT. The entire assembly is encased within a gray engine nacelle structure.



<div align="center">

HPT: High pressure turbine.

LPT: Low pressure turbine.

HPC: High pressure compressor.

LPC: Low pressure compressor.

N1: Outer shaft.

N2: Inner shaft.

</div>

early stage any detected malfunction, allowing for staying within safe operation and also reducing fuel consumption and increasing operational punctuality. Therefore, early fault mode identification provides relevant information for the maintenance program. The use of the SOM neural network for this application is particularly interesting for its ability to map the input data without prior knowledge on fault modes. In general, the monitored system does not provide labeled data related to fault modes, whereas in the case of only one fault mode, the situation is straightforward. In the case of multiple fault modes, it becomes more complicated without a proper monitoring to identify them.

## 4.2 Input data

In this paper, datasets are generated [43] by using the C-MAPSS software [46]. C-MAPSS is a tool for the simulation of a realistic large commercial turbofan engine (Fig. 4) for the 90,000 lb thrust class. Thanks to editable input parameters, it is possible to specify operational profile, closed-loop controllers, and environmental conditions such as altitude. Furthermore, various degradations can be managed in different sections of the engine system.

Using this simulation environment, five datasets were generated by [43]. One of them was used for the prognostics challenge competition at International Conference on Prognostics and Health Management in 2008 (PHM08). In those datasets, the simulated engines have one or six operational conditions (flight phases such as Take-off, Cruise, etc.) driven by engine control settings (altitude, Mach number and Throttle Resolver Angle) and one or two fault modes. In PHM08 (Table 1), there are three datasets with one fault (i.e., #1, #2, and #5) and two with two faults (i.e., #3 and #4). The fault, corresponding to a failed system part, is, respectively, the HPC and the HPC and the fan (see Fig. 4). All dataset characteristics are summarized in Table 1.

<div align="center">

Fig. 4 Simplified diagram of the 90 K engine [46]

</div>

Each dataset (i.e., #1 to #5) consists of multivariate time series and is divided into a training set and a testing set, generated by [43]. The database provides those sets in separate files: five training files and five testing files. The training subset is only used for training of the neural network (the learning), whereas the testing subset, with

<div align="center">

Table 1 C-MAPSS dataset characteristics

</div>

<table border="1"><tr><td>Id</td><td>Name</td><td>Operational conditions</td><td>Fault modes</td><td>Failed system part</td><td>Number of engines</td></tr><tr><td>#1</td><td>FD001</td><td>1</td><td>1</td><td>HPC</td><td>100</td></tr><tr><td>#2</td><td>FD002</td><td>6</td><td>1</td><td>HPC</td><td>260</td></tr><tr><td>#3</td><td>FD003</td><td>1</td><td>2</td><td>HPC,Fan</td><td>100</td></tr><tr><td>#4</td><td>FD004</td><td>6</td><td>2</td><td>HPC,Fan</td><td>549</td></tr><tr><td>#5</td><td>FD005</td><td>6</td><td>1</td><td>HPC</td><td>218</td></tr></table>



<div align="center">

Table 2 Output variables from C-MAPSS tool

</div>

<table border="1"><tr><td>Sensor id</td><td>Symbol</td><td>Description</td><td>Units</td></tr><tr><td>1</td><td>T2</td><td>Total temperature at fan inlet</td><td>°R</td></tr><tr><td>2</td><td>T24</td><td>Total temperature at LPC outlet</td><td>°R</td></tr><tr><td>3</td><td>T30</td><td>Total temperature at HPC outlet</td><td>°R</td></tr><tr><td>4</td><td>T50</td><td>Total temperature at LPT outlet</td><td>°R</td></tr><tr><td>5</td><td>P2</td><td>Pressure at fan inlet</td><td>psia</td></tr><tr><td>6</td><td>P15</td><td>Total pressure in bypass duct</td><td>psia</td></tr><tr><td>7</td><td>P30</td><td>Total pressure at HPC outlet</td><td>psia</td></tr><tr><td>8</td><td>Nf</td><td>Physical fan speed</td><td>rpm</td></tr><tr><td>9</td><td>Nc</td><td>Physical core speed</td><td>rpm</td></tr><tr><td>10</td><td>epr</td><td>Engine pressure ration(P50/P2)</td><td>-</td></tr><tr><td>11</td><td>Ps30</td><td>Static pressure at HPC outlet</td><td>psia</td></tr><tr><td>12</td><td>Phi</td><td>Ratio of fuel flow to Ps30</td><td>pps/psi</td></tr><tr><td>13</td><td>NRf</td><td>Corrected fan speed</td><td>rpm</td></tr><tr><td>14</td><td>NRc</td><td>Corrected core speed</td><td>rpm</td></tr><tr><td>15</td><td>BPR</td><td>Bypass ration</td><td>-</td></tr><tr><td>16</td><td>farB</td><td>Burner fuel-air ratio</td><td>-</td></tr><tr><td>17</td><td>htBleed</td><td>Bleed enthalpy</td><td>-</td></tr><tr><td>18</td><td>Nf_dmd</td><td>Demanded fan speed</td><td>rpm</td></tr><tr><td>19</td><td>PCNfR_dmd</td><td>Demanded corrected fan speed</td><td>rpm</td></tr><tr><td>20</td><td>W31</td><td>HPT coolant bleed</td><td>lbm/s</td></tr><tr><td>21</td><td>W32</td><td>LPT coolant bleed</td><td>lbm/s</td></tr></table>

<div align="center">

Table 3 Extract of the dataset #4

</div>

<table border="1"><tr><td>Engine</td><td>Cycle</td><td>CS1</td><td>CS2</td><td>CS3</td><td>S1</td><td>S2</td><td>S3</td><td>S4</td><td>S5</td><td>S6</td><td>S7</td><td>S8</td><td>S9</td></tr><tr><td>1</td><td>1</td><td>42.0049</td><td>0.84</td><td>100</td><td>445</td><td>549.68</td><td>1343.43</td><td>1112.93</td><td>3.91</td><td>5.7</td><td>137.36</td><td>2211.86</td><td>8311.32</td></tr><tr><td>1</td><td>2</td><td>20.002</td><td>0.7002</td><td>100</td><td>491.19</td><td>606.07</td><td>1477.61</td><td>1237.5</td><td>9.35</td><td>13.61</td><td>332.1</td><td>2323.66</td><td>8713.6</td></tr><tr><td>1</td><td>3</td><td>42.0038</td><td>0.8409</td><td>100</td><td>445</td><td>548.95</td><td>1343.12</td><td>1117.05</td><td>3.91</td><td>5.69</td><td>138.18</td><td>2211.92</td><td>8306.69</td></tr><tr><td>1</td><td>4</td><td>42</td><td>0.84</td><td>100</td><td>445</td><td>548.7</td><td>1341.24</td><td>1118.03</td><td>3.91</td><td>5.7</td><td>137.98</td><td>2211.88</td><td>8312.35</td></tr><tr><td>1</td><td>5</td><td>25.0063</td><td>0.6207</td><td>60</td><td>462.54</td><td>536.1</td><td>1255.23</td><td>1033.59</td><td>7.05</td><td>9</td><td>174.82</td><td>1915.22</td><td>7994.94</td></tr><tr><td>1</td><td>6</td><td>34.9996</td><td>0.84</td><td>100</td><td>449.44</td><td>554.77</td><td>1352.87</td><td>1117.01</td><td>5.48</td><td>7.97</td><td>193.82</td><td>2222.77</td><td>8340</td></tr><tr><td>1</td><td>7</td><td>0.0019</td><td>0.0001</td><td>100</td><td>518.67</td><td>641.83</td><td>1583.47</td><td>1393.89</td><td>14.62</td><td>21.58</td><td>552.45</td><td>2387.92</td><td>9050.5</td></tr><tr><td>1</td><td>8</td><td>41.9981</td><td>0.84</td><td>100</td><td>445</td><td>549.05</td><td>1344.16</td><td>1110.77</td><td>3.91</td><td>5.69</td><td>137.13</td><td>2211.92</td><td>8307.28</td></tr><tr><td>1</td><td>9</td><td>42.0016</td><td>0.84</td><td>100</td><td>445</td><td>549.55</td><td>1342.85</td><td>1101.67</td><td>3.91</td><td>5.7</td><td>138.02</td><td>2211.9</td><td>8307.81</td></tr><tr><td>1</td><td>10</td><td>25.0019</td><td>0.6217</td><td>60</td><td>462.54</td><td>536.35</td><td>1251.91</td><td>1041.37</td><td>7.05</td><td>9.01</td><td>174.7</td><td>1915.23</td><td>8005.83</td></tr><tr><td>1</td><td>11</td><td>20.0016</td><td>0.7</td><td>100</td><td>491.19</td><td>606.88</td><td>1478.02</td><td>1233.07</td><td>9.35</td><td>13.61</td><td>333.22</td><td>2323.7</td><td>8709.62</td></tr><tr><td>1</td><td>12</td><td>34.9993</td><td>0.84</td><td>100</td><td>449.44</td><td>554.53</td><td>1365.99</td><td>1122.73</td><td>5.48</td><td>7.98</td><td>193.67</td><td>2222.78</td><td>8337.46</td></tr><tr><td>1</td><td>13</td><td>24.9986</td><td>0.62</td><td>60</td><td>462.54</td><td>536.32</td><td>1257.84</td><td>1040.87</td><td>7.05</td><td>9.01</td><td>174.53</td><td>1915.28</td><td>8000.07</td></tr><tr><td>1</td><td>14</td><td>20.0056</td><td>0.7008</td><td>100</td><td>491.19</td><td>607.32</td><td>1470.33</td><td>1242.41</td><td>9.35</td><td>13.61</td><td>333.71</td><td>2323.72</td><td>8714.35</td></tr><tr><td>Engine</td><td>Cycle</td><td>S10</td><td>S11</td><td>S12</td><td>S13</td><td>S14</td><td>S15</td><td>S16</td><td>S17</td><td>S18</td><td>S19</td><td>S20</td><td>S21</td></tr><tr><td>1</td><td>1</td><td>1.01</td><td>41.69</td><td>129.78</td><td>2387.99</td><td>8074.83</td><td>9.3335</td><td>0.02</td><td>330</td><td>2212</td><td>100</td><td>10.62</td><td>6.367</td></tr><tr><td>1</td><td>2</td><td>1.07</td><td>43.94</td><td>312.59</td><td>2387.73</td><td>8046.13</td><td>9.1913</td><td>0.02</td><td>361</td><td>2324</td><td>100</td><td>24.37</td><td>14.6552</td></tr><tr><td>1</td><td>3</td><td>1.01</td><td>41.66</td><td>129.62</td><td>2387.97</td><td>8066.62</td><td>9.4007</td><td>0.02</td><td>329</td><td>2212</td><td>100</td><td>10.48</td><td>6.4213</td></tr><tr><td>1</td><td>4</td><td>1.02</td><td>41.68</td><td>129.8</td><td>2388.02</td><td>8076.05</td><td>9.3369</td><td>0.02</td><td>328</td><td>2212</td><td>100</td><td>10.54</td><td>6.4176</td></tr></table>



<div align="center">

Table 3 (continued)

</div>

<table border="1"><tr><td>Engine</td><td>Cycle</td><td>S10</td><td>S11</td><td>S12</td><td>S13</td><td>S14</td><td>S15</td><td>S16</td><td>S17</td><td>S18</td><td>S19</td><td>S20</td><td>S21</td></tr><tr><td>1</td><td>5</td><td>0.93</td><td>36.48</td><td>164.11</td><td>2028.08</td><td>7865.8</td><td>10.8366</td><td>0.02</td><td>305</td><td>1915</td><td>84.93</td><td>14.03</td><td>8.6754</td></tr><tr><td>1</td><td>6</td><td>1.02</td><td>41.44</td><td>181.9</td><td>2387.87</td><td>8054.1</td><td>9.3346</td><td>0.02</td><td>330</td><td>2223</td><td>100</td><td>14.91</td><td>8.9057</td></tr><tr><td>1</td><td>7</td><td>1.3</td><td>46.94</td><td>520.48</td><td>2387.89</td><td>8127.92</td><td>8.396</td><td>0.03</td><td>391</td><td>2388</td><td>100</td><td>38.93</td><td>23.4578</td></tr><tr><td>1</td><td>8</td><td>1.01</td><td>41.6</td><td>129.65</td><td>2387.97</td><td>8075.99</td><td>9.3679</td><td>0.02</td><td>329</td><td>2212</td><td>100</td><td>10.55</td><td>6.2787</td></tr><tr><td>1</td><td>9</td><td>1.02</td><td>41.44</td><td>129.65</td><td>2388</td><td>8071.13</td><td>9.3384</td><td>0.02</td><td>328</td><td>2212</td><td>100</td><td>10.63</td><td>6.3055</td></tr><tr><td>1</td><td>10</td><td>0.94</td><td>36.24</td><td>164.08</td><td>2028.13</td><td>7869.41</td><td>10.9141</td><td>0.02</td><td>305</td><td>1915</td><td>84.93</td><td>14.34</td><td>8.6119</td></tr><tr><td>1</td><td>11</td><td>1.07</td><td>43.86</td><td>312.96</td><td>2387.83</td><td>8050.06</td><td>9.1667</td><td>0.02</td><td>363</td><td>2324</td><td>100</td><td>24.63</td><td>14.6705</td></tr><tr><td>1</td><td>12</td><td>1.02</td><td>41.45</td><td>181.71</td><td>2387.86</td><td>8056.31</td><td>9.3041</td><td>0.02</td><td>332</td><td>2223</td><td>100</td><td>14.68</td><td>8.8752</td></tr><tr><td>1</td><td>13</td><td>0.94</td><td>36.42</td><td>163.67</td><td>2028.14</td><td>7865.15</td><td>10.8388</td><td>0.02</td><td>305</td><td>1915</td><td>84.93</td><td>14.41</td><td>8.6062</td></tr><tr><td>1</td><td>14</td><td>1.07</td><td>43.92</td><td>313.3</td><td>2387.85</td><td>8051.34</td><td>9.2272</td><td>0.02</td><td>364</td><td>2324</td><td>100</td><td>24.3</td><td>14.7105</td></tr></table>


> **Figure Description:**

The image is a scatter plot titled "Sensor 9 operating regime 1 of all units." The horizontal axis is labeled "Cycle" and ranges from 0 to 400 in increments of 50. The vertical axis is labeled "Sensor reading" and ranges from 8740 to 8920 in increments of 20. The plot displays a dense cluster of blue asterisk data points representing sensor readings over time. From cycle 0 to approximately cycle 100, the data points are tightly concentrated between values of roughly 8760 and 8800. Starting around cycle 100, the data begins to show increased variance, with points spreading upward toward higher sensor readings. This upward trend in variance continues, reaching a peak dispersion between cycles 150 and 250, where individual data points reach as high as 8920 and as low as approximately 8745. Beyond cycle 250, the density of the data points decreases, with the readings gradually tapering off toward cycle 350, while still maintaining a wider range of values compared to the initial cycles.




> **Figure Description:**

The image is a scatter plot titled "Sensor 17 operating regime 1 of all units." The horizontal axis is labeled "Cycle" and ranges from 0 to 400, with tick marks every 50 units. The vertical axis is labeled "Sensor reading" and ranges from 365 to 375, with tick marks at 365, 370, and 375. The plot displays discrete horizontal bands of data points represented by blue asterisks, corresponding to specific sensor readings. These bands are located at approximately 365.2, 366.2, 367.2, 368.2, 369.2, 370.2, 371.2, 372.2, 373.2, 374.2, and 375.0. The horizontal spread of the data points varies by band, with the bands at lower sensor readings generally extending to lower cycle counts (e.g., the band at 365.2 ends near cycle 110), while bands at higher sensor readings extend to higher cycle counts (e.g., the band at 373.2 extends beyond cycle 300). The highest band at 375.0 contains a small cluster of points between cycles 200 and 260.



<div align="center">

Fig. 5 Trend of sensors in a selected regimes. (Left) Inconsistent end-life trends. (Right) Piecewise trends

</div>

different data, is only used for the network validation. In this case study, a dataset contains three input variables representing the engine operational settings, that generate one or six operational conditions and 21 output sensors (Table 2). Dataset is comparable between themselves whether they have the same operation settings, generating

<div align="center">

Table 4 SOM information for all datasets

</div>

<table border="1"><tr><td>Id</td><td>Number of observations</td><td>Features</td><td>Map size</td><td>Iterations$ ^{a}$</td></tr><tr><td>#1</td><td>20,631</td><td>3</td><td>7</td><td>24,500</td></tr><tr><td>#2</td><td>53,759</td><td>3</td><td>9</td><td>40,500</td></tr><tr><td>#3</td><td>24,720</td><td>3</td><td>7</td><td>24,500</td></tr><tr><td>#4</td><td>61,249</td><td>3</td><td>9</td><td>40,500</td></tr><tr><td>#5</td><td>45,918</td><td>3</td><td>8</td><td>32,000</td></tr></table>

$ ^{a} $Estimated following the rule of thumb

the same number of operational conditions. Thus, FD001 and FD003 are comparable as well as FD002 and FD004. However, the FD005 dataset cannot be compared with FD002 or FD004 because the values of the operational settings are not compatible, even if it has six operational conditions.

Table 3 shows an extract of available data for the dataset #4. The other datasets follow the same format.

A reduction in the number of sensors could lead to a drastic reduction in the computational time for the training of the neural network. Following the work of [10, 22, 47] for the PHM08 dataset number #5, the only relevant seven sensors were found to be: 2, 3, 4, 7, 11, 12 and 15.

In fact, among the 21 sensors, constant or binary trend is observed on several sensors that do not provide degradation behaviors. Sensors 1, 5, 6, 10, 16, 17, 18 and 19 are concerned and not considered from the selection. Others sensors provide similar information such as sensors 8 and 13



<div align="center">

Fig. 6 SOM maps from datasets #1 to #5 with three operation conditions as features

</div>


> **Figure Description:**

This image is a heatmap titled "Dataset #1" that displays a 7x7 grid of values represented by varying shades of red, where lighter shades indicate lower values and darker shades indicate higher values. The axes are labeled from 0 to 6 on both the horizontal (x-axis) and vertical (y-axis) dimensions. The grid is organized such that the lowest values are concentrated in the bottom-left corner (at coordinates 0,0) and the highest values are concentrated in the top-right corner (at coordinates 6,6). The color intensity increases progressively as one moves from the bottom-left toward the top-right, indicating a positive correlation or gradient across the dataset.




> **Figure Description:**

The image is a heatmap titled "Dataset #2" displayed on a 9x9 grid with axes labeled from 0 to 8. The grid represents a spatial distribution of values visualized through a color-coded matrix. The leftmost column (x=0) shows a gradient of red tones, transitioning from a darker red at y=0 to a lighter, pale pink at y=8. The second column (x=1) follows a similar red-to-pink gradient, though slightly darker than the first column. The third column (x=2) shows red tones at the bottom (y=0, 1, 2), black at y=3, 4, 5, a light lavender at y=6, and black at y=7, 8.

The central region of the grid features distinct clusters of color. At x=3, the values are red at y=0, black at y=1, 2, green at y=3, 4, black at y=5, 6, and dark blue at y=7, 8. At x=4, the values are black at y=0, light lavender at y=1, 2, green at y=3, 4, light green at y=5, black at y=6, and dark blue at y=7, 8. At x=5, the values are dark teal at y=0, black at y=1, light lavender at y=2, black at y=3, light green at y=4, 5, black at y=6, and black at y=7, 8.

The right side of the grid shows further variation. At x=6, the values are teal at y=0, black at y=1, 2, 3, 4, 5, 6, and dark purple at y=7, 8. At x=7, the values are light teal at y=0, 1, black at y=2, 3, 4, 5, 6, and purple at y=7, 8. Finally, at x=8, the values are light teal at y=0, 1, 2, purple at y=3, 4, 5, black at y=6, and light pink at y=7, 8. Black cells represent null or zero-value data points throughout the grid.




> **Figure Description:**

The image is a heatmap titled "Dataset #3" that displays a 7x7 grid of values represented by varying shades of red, where darker red indicates higher values and lighter pink/white indicates lower values. The axes are labeled from 0 to 6 on both the x-axis and y-axis. The grid shows a clear gradient pattern, with the highest values concentrated in the top-left corner (at coordinates [0, 6] and [1, 6]) and the lowest values concentrated in the bottom-right corner (at coordinates [6, 0] and [6, 1]). The intensity of the red color decreases progressively as one moves from the top-left toward the bottom-right of the grid.




> **Figure Description:**

The image is a heatmap titled "Dataset #4" displayed on a grid with axes ranging from 0 to 8. The grid consists of 81 cells, some of which are colored and others are black (representing null or zero values). The grid is organized as follows, starting from the bottom-left (0,0) to the top-right (8,8):

At row 0, the cells are: (0,0) dark red, (1,0) dark red, (2,0) black, (3,0) light lavender, (4,0) light lavender, (5,0) light lavender, (6,0) light purple, (7,0) light purple, (8,0) purple. At row 1: (0,1) dark red, (1,1) dark red, (2,1) medium red, (3,1) black, (4,1) black, (5,1) black, (6,1) purple, (7,1) purple, (8,1) purple. At row 2: (0,2) black, (1,2) black, (2,2) light red, (3,2) light red, (4,2) light red, (5,2) light red, (6,2) black, (7,2) black, (8,2) black. At row 3: (0,3) dark blue, (1,3) dark blue, (2,3) black, (3,3) black, (4,3) light red, (5,3) black, (6,3) teal, (7,3) teal, (8,3) dark teal. At row 4: (0,4) medium blue, (1,4) medium blue, (2,4) light blue, (3,4) light blue, (4,4) black, (5,4) light teal, (6,4) light teal, (7,4) teal, (8,4) black. At row 5: (0,5) medium blue, (1,5) medium blue, (2,5) light blue, (3,5) light blue, (4,5) black, (5,5) light teal, (6,5) light teal, (7,5) black, (8,5) light purple. At row 6: (0,6) black, (1,6) black, (2,6) black, (3,6) light blue, (4,6) black, (5,6) light blue, (6,6) black, (7,6) dark purple, (8,6) light purple. At row 7: (0,7) green, (1,7) green, (2,7) green, (3,7) black, (4,7) light green, (5,7) black, (6,7) light green, (7,7) black, (8,7) light pink. At row 8: (0,8) green, (1,8) green, (2,8) light green, (3,8) light green, (4,8) light green, (5,8) light green, (6,8) light green, (7,8) black, (8,8) light pink.




> **Figure Description:**

The image is a heatmap titled "Dataset #5" featuring an 8x8 grid of colored squares, with axes labeled from 0 to 7 on both the x and y dimensions. The grid displays a variety of colors, including black, shades of green, blue, purple, and light pink/lavender.

The grid layout is as follows, starting from the bottom-left (0,0) to the top-right (7,7):
At row 0, the colors are: (0,0) muted red, (1,0) dark red, (2,0) dark red, (3,0) black, (4,0) bright purple, (5,0) light purple, (6,0) light lavender, (7,0) light lavender.
At row 1, the colors are: (0,1) light pink, (1,1) muted red, (2,1) black, (3,1) light lavender, (4,1) black, (5,1) light purple, (6,1) black, (7,1) light lavender.
At row 2, the colors are: (0,2) light pink, (1,2) black, (2,2) light lavender, (3,2) light lavender, (4,2) light lavender, (5,2) black, (6,2) light pink, (7,2) black.
At row 3, the colors are: (0,3) black, (1,3) blue, (2,3) blue, (3,3) light lavender, (4,3) light lavender, (5,3) black, (6,3) light pink, (7,3) purple.
At row 4, the colors are: (0,4) dark blue, (1,4) blue, (2,4) blue, (3,4) light lavender, (4,4) black, (5,4) light blue, (6,4) black, (7,4) purple.
At row 5, the colors are: (0,5) black, (1,5) black, (2,5) black, (3,5) light blue, (4,5) light blue, (5,5) black, (6,5) black, (7,5) purple.
At row 6, the colors are: (0,6) green, (1,6) green, (2,6) light green, (3,6) light green, (4,6) black, (5,6) light blue, (6,6) light blue, (7,6) black.
At row 7, the colors are: (0,7) dark green, (1,7) green, (2,7) light green, (3,7) very light green, (4,7) very light green, (5,7) black, (6,7) teal, (7,7) dark teal.



with the sensor 11 by looking at the correlation coefficient with a threshold of 85%. Sensors 9 and 14 show inconsistent end-life trends among the engines (Fig. 5, left), and the sensor 17 is a piecewise constant function (Fig. 5,

right). Finally, the sensors 20 and 21 do not bring a clear trend throughout the unit's life according to [22]. Through those steps, the final seven sensors are determined. The



<div align="center">

Table 5 Training SOM information for all datasets

</div>

<table border="1"><tr><td>Id</td><td>Number of observations</td><td>Features</td><td>Map size</td><td>Iterations$ ^{a}$</td></tr><tr><td>#1</td><td>20,631</td><td>7</td><td>19</td><td>180,500</td></tr><tr><td>#2</td><td>53,759</td><td>7</td><td>24</td><td>288,000</td></tr><tr><td>#3</td><td>24,720</td><td>7</td><td>20</td><td>200,000</td></tr><tr><td>#4</td><td>61,249</td><td>7</td><td>25</td><td>312,500</td></tr><tr><td>#5</td><td>45,918</td><td>7</td><td>23</td><td>264,500</td></tr></table>

$ ^{a} $Estimated following the rule of thumb

same selected sensors have been taken into account for the datasets #1, #2, #3 and #4.

## 4.3 Operational mode labeling

The case study contains five datasets generated by [43] (see Table 1), where it is known that one or six different operational conditions are used. According to the complexity of the case study, manual operational mode labeling may not be possible by hand. To demonstrate the power of the automated SOM, they are performed following the system map process introduced in the previous section (see Fig. 2).

The three operational settings (altitude, Mach number and Throttle Resolver Angle) in the dataset are used as inputs to the SOM. Due to the number of inputs, the map size is determined with Eq. (3) and the result is divided by four, custom factors established through multiple empirical experiments. A bigger (or smaller) map leads to an increase (and decrease) in the cluster numbers and may lead to an inconsistency in the representation of information. Further development will be done to address this empirical estimation. The convergence criteria of the "rule of thumb" are used, leading to a number of iterations of 500 times the number of neurons. Table 4 summarizes SOM information used.

The training phase generates maps in Fig. 6.

The maps reveal one cluster for the datasets #1 and #3, whereas the datasets #2, #4 and #5 show six clusters. This means that there is one operational condition for #1 and #3 and six operational conditions for #2, #4 and #5, which is in line with Table 4. The diagnostic phase from the system map process provides exactly the same operational mode labeling as what was obtained manually.

## 4.4 System map generation

## 4.4.1 Preprocessing and training

The SOM will now be trained with the seven sensors identified in the previous section. The number of neurons is

determined with Eq. (3) and divided by two to reduce the computational time. Table 5 summarizes SOM information used.

The training phase generates the maps in Fig. 7.

For each dataset in Fig. 7, the number of clusters is identical to Fig. 6, corresponding to the number of operational modes. The cluster identification phase provides the same cluster information with the seven selected sensors, compared to the operational mode labeling in Sect. 4.3. It provides reliability in the unsupervised approach.

It appears that the maps for the datasets #3 and #4 show two darker colors on each cluster, which means that there are two fault modes in each cluster. This matches the information of Table 1. The color degradation corresponds to the evolution of the HI (i.e., degradation status). Lighter colors correspond to a healthy system, whereas the darker colors mean an advanced degradation. Other datasets have only one dark colors on each cluster; they have one fault mode. To confirm that, mathematical tools are now introduced.

## 4.5 Fault mode identification

## 4.5.1 Fault quantification

The kernel density estimator Eq. (11) is applied on each cluster of each map under H2. It generates a PDF to identify the number of fault modes. Thanks to the SOM map (Fig. 7), the minimum probability density function kernel bandwidth without cluster boundaries can be obtained (see Table 6).

Figure 8 presents the PDF generated for a particular cluster. On those figures, PDF values of node coordinates $ ( x,y) $ and hit numbers z are normalized. The number of fault modes is easily identifiable visually as well as automatically. This procedure is performed for each generated cluster on each map, and results are compared with the information provided by the datasets. It results that the fault number is well identified, with two fault modes for the database #3, #4 and one for the others.

In Sect. 3.4.1, two ways to evaluate the hit number were presented. Here, we would like to evaluate whether H1 is more pertinent than H2. H1 is relevant in terms of interpretation. However, the dataset used provides few engines (Table 1). Table 7 summarizes the number of samples according to hypotheses presented in Sect. 3.4.1.

Under hypothesis H1, due to a lack of samples, only one out of two fault modes is identified. For dataset #4, it has two fault modes and six operational conditions; the 249 samples of H1 represent around 21 samples per fault per operational conditions. Following the philosophy of H2, around 100 samples per fault per operational conditions are needed for proper identification.



<div align="center">

Fig.7 SOM map from datasets #1 to #5 with 7 physical sensor data as features

</div>


> **Figure Description:**

The image is a heatmap titled "Dataset #1" that displays a 10x10 grid of color-coded values. The x-axis and y-axis are both labeled with even integers ranging from 0 to 18. The heatmap uses a red-to-white color gradient, where darker red represents higher values and lighter pink/white represents lower values.

The highest intensity (darkest red) is concentrated in the upper-left corner of the grid, specifically within the cells corresponding to the x-range of 0 to 4 and the y-range of 14 to 18. From this peak, the color intensity gradually fades toward lighter shades as one moves toward the bottom and right edges of the grid. The bottom-right corner, corresponding to x-values near 18 and y-values near 0, exhibits the lightest color, indicating the lowest values in the dataset. The transition between colors is smooth, suggesting a continuous distribution of data points across the 10x10 spatial grid.




> **Figure Description:**

The image is a heatmap titled "Dataset #2" that displays a 24x24 grid divided into distinct colored regions separated by thick black borders. The axes are labeled from 0 to 21 in increments of 3, representing a coordinate system for the grid. The grid is partitioned into five primary colored segments: a green region in the top-left, a light-to-dark purple region in the center-left, a light-to-dark magenta region in the top-right, a red region in the bottom-left, and a teal-to-cyan region in the bottom-right.

The color intensity within each region follows a gradient, suggesting a continuous variable mapped across the grid cells. The black borders act as boundaries between these distinct clusters. The green region occupies the upper-left quadrant, extending from approximately x=0 to x=12 and y=18 to y=24. The purple region is located in the middle-left, spanning roughly x=0 to x=9 and y=7 to y=18. The magenta region dominates the right side, covering x=12 to x=24 and y=7 to y=24. The red region is situated in the bottom-left, covering x=0 to x=12 and y=0 to y=7. Finally, the teal/cyan region occupies the bottom-right, spanning x=12 to x=24 and y=0 to y=7. The grid cells themselves are square, and the color transitions are smooth within each bounded area.




> **Figure Description:**

This image is a heatmap titled "Dataset #3" that displays a 20x20 grid of values represented by varying shades of red. The axes are labeled from 0 to 18, with ticks appearing at intervals of 2 on both the horizontal and vertical axes. The color intensity follows a gradient where darker, deep red tones are concentrated in the bottom-left and bottom-right corners of the grid, representing higher values. The center and upper regions of the heatmap transition into lighter, paler shades of pink and white, indicating lower values. The overall distribution shows a symmetrical pattern where the intensity is highest at the bottom corners and gradually decreases toward the top center of the plot.




> **Figure Description:**

The image is a heatmap titled "Dataset #4" that displays a 25x25 grid partitioned into several distinct, color-coded regions separated by thick black borders. The x-axis and y-axis are both labeled with increments of 3, ranging from 0 to 24. The regions are filled with color gradients: a red-toned region occupies the bottom-left corner, a blue-toned region occupies the middle-left, a green-toned region occupies the top-middle and right, a teal-toned region occupies the center-right, a light purple region occupies the bottom-center, and a dark purple region occupies the bottom-right. The color intensity within each region varies, creating a gradient effect across the grid cells. The black borders delineate the boundaries between these six distinct clusters, effectively segmenting the 25x25 coordinate space.




> **Figure Description:**

The image is a data visualization titled "Dataset #5" that displays a 2D grid partitioned into six distinct colored regions separated by thick black borders. The grid axes range from 0 to 21, with tick marks at intervals of 3. The regions are color-coded with gradients: a green region occupies the top-left/center, a pink/magenta region occupies the top-right, a blue/purple region occupies the middle-left, a bright purple region occupies the center-right, a red/pink region occupies the bottom-left, and a teal/cyan region occupies the bottom-right. Each region features a color gradient that transitions from lighter shades at the edges to more saturated or darker shades toward the interior or specific corners of the partitioned segments. The black borders delineate the boundaries between these six clusters, creating a segmented map-like structure across the 22x22 grid space.



For each engine, the last flight cycle spent on each operational condition (H2) is compared to the last flight cycle before a fault occurs (H1) to quantify the reliability of H2. For example, the engine 12 (Table 8) has six operational conditions. Table 8 summarizes the flight cycle for both cases and the error of H2 compared to H1. The

<div align="center">

Table 6 PDF kernel bandwidth

</div>

<table border="1"><tr><td>Id</td><td>Map size</td><td>Bandwidth h</td></tr><tr><td>#1</td><td>19</td><td>0.19</td></tr><tr><td>#2</td><td>24</td><td>0.22</td></tr><tr><td>#3</td><td>20</td><td>0.20</td></tr><tr><td>#4</td><td>25</td><td>0.22</td></tr><tr><td>#5</td><td>23</td><td>0.21</td></tr></table>




> **Figure Description:**

The image is a 3D scatter plot titled "Dataset #1" that compares a Gaussian probability density function (pdf) with a cluster map. The vertical axis, labeled "pdf," ranges from 0 to 1. The horizontal axes, labeled "x" and "y," both range from 0 to 1, with the x-axis also showing a tick mark at -0.5. The plot contains two distinct data series identified by a legend in the top right corner: "Gaussian pdf," represented by blue open circles, and "Cluster map," represented by orange asterisks.

The "Gaussian pdf" data forms a bell-shaped surface centered in the x-y plane, with the peak reaching a value of approximately 1 on the pdf axis. The "Cluster map" data is represented by a dense, flat grid of orange asterisks covering the base of the plot at a pdf value of 0, while also overlaying the Gaussian surface at specific points, tracing the shape of the bell curve. The perspective is angled to show the 3D relationship between the flat cluster grid and the elevated Gaussian distribution.




> **Figure Description:**

This 3D scatter plot, titled "Dataset #2," displays the relationship between two variables, x and y, and a probability density function (pdf) value. The vertical axis (pdf) ranges from 0 to 1. The x-axis ranges from 0 to 1.5, and the y-axis ranges from -0.5 to 1. The plot features two distinct data series as indicated by the legend: "Gaussian pdf," represented by blue open circles, and "Cluster map," represented by red asterisks. The blue circles form a 3D bell-shaped surface (a Gaussian distribution) centered within the plot area. The red asterisks are arranged in a grid pattern on the base plane (where pdf = 0) and also appear as a subset of points following the slope of the Gaussian surface, specifically along a diagonal path leading toward the peak of the distribution.




> **Figure Description:**

The image is a 3D scatter plot titled "Dataset #3" that displays two distinct data series: "Gaussian pdf" represented by blue open circles and "Cluster map" represented by orange asterisks. The vertical axis, labeled "pdf," ranges from 0 to 1. The horizontal axes represent spatial coordinates, with the "x" axis ranging from 0 to 1.5 and the "y" axis ranging from -0.5 to 1.

The "Gaussian pdf" data forms two distinct peaks in the 3D space, representing a probability density function. The "Cluster map" data is plotted as a flat, dense grid of orange asterisks located at the base of the plot (where pdf = 0) across the x-y plane, while also appearing as a vertical projection or overlay on the peaks of the "Gaussian pdf" data, effectively mapping the cluster locations onto the probability distribution. The legend in the top right corner clearly identifies the blue circles as "Gaussian pdf" and the orange asterisks as "Cluster map."




> **Figure Description:**

The image is a 3D scatter plot titled "Dataset #4" that displays two distinct data series: a "Gaussian pdf" represented by blue open circles and a "Cluster map" represented by red asterisks. The vertical axis, labeled "pdf," ranges from 0 to 1. The horizontal axes represent spatial coordinates x and y, both ranging from -0.5 to 1.

The "Gaussian pdf" data forms a continuous, undulating surface with two prominent peaks of varying heights, suggesting a bimodal distribution. The "Cluster map" data consists of red asterisks arranged in a regular grid pattern across the base plane, with some points extending upward to align with the peaks of the Gaussian distribution. A legend in the upper right corner identifies the blue circles as "Gaussian pdf" and the red asterisks as "Cluster map." The perspective is angled to show the relationship between the grid-based cluster map and the continuous probability density function surface.




> **Figure Description:**

This is a 3D scatter and surface plot titled "Dataset #5". The vertical axis represents "pdf" with a range from 0 to 1. The horizontal axes represent "x" and "y". The x-axis ranges from 0 to 1.5, and the y-axis ranges from -0.5 to 1. The plot contains two data series identified in a legend: "Gaussian pdf" represented by blue circles, and "Cluster map" represented by orange asterisks.

The "Gaussian pdf" series forms a 3D bell-shaped surface elevated above the x-y plane, with the peak reaching a value of 1. The "Cluster map" series consists of two distinct sets of orange asterisks: one set is plotted on the base plane (z=0) in a regular grid pattern, and the second set is plotted along the surface of the Gaussian distribution, following the contour of the bell shape. The grid of asterisks on the base plane covers the area defined by x values from approximately 0 to 1 and y values from approximately 0 to 1. The asterisks following the Gaussian surface are positioned at various heights corresponding to the probability density function values at those specific x and y coordinates.



<div align="center">

Fig. 8 PDF on a cluster for datasets #1 to #5

</div>

<div align="center">

Table 7 Number of sample for datasets #1 to #5

</div>

<table border="1"><tr><td>Id</td><td>H1</td><td>H2</td></tr><tr><td>#1</td><td>100</td><td>100</td></tr><tr><td>#2</td><td>260</td><td>1560</td></tr><tr><td>#3</td><td>100</td><td>100</td></tr><tr><td>#4</td><td>249</td><td>1494</td></tr><tr><td>#5</td><td>218</td><td>1308</td></tr></table>

error is above 10% (custom threshold) for the clusters 1 and 5. That means engine 12 belongs to the group of engines, where H1 is more relevant than H2.

<div align="center">

Table 8 Example of comparison for engine 12

</div>

<table border="1"><tr><td colspan="4">Engine 12</td></tr><tr><td>Cluster</td><td>H1</td><td>H2</td><td>Error(%)</td></tr><tr><td>1</td><td>320</td><td>260</td><td>$18.75^{a}$</td></tr><tr><td>2</td><td></td><td>320</td><td>0.00</td></tr><tr><td>3</td><td></td><td>300</td><td>6.25</td></tr><tr><td>4</td><td></td><td>289</td><td>9.69</td></tr><tr><td>5</td><td></td><td>277</td><td>$13.44^{a}$</td></tr><tr><td>6</td><td></td><td>310</td><td>3.13</td></tr></table>

<div align="center">

$ ^{a} $Error above 10%

</div>



<div align="center">

Fig. 9 Failure modes for datasets #1 to #5

</div>

<table border="1"><tr><td>18</td><td></td><td>

<div align="center">

Dataset #2

</div>

<table border="1"><tr><td>25</td></tr><tr><td>20</td></tr><tr><td>15</td></tr><tr><td>10</td></tr><tr><td>5</td></tr><tr><td>0</td></tr><tr><td>0</td><td>5</td><td>10</td><td>15</td><td>20</td><td>25</td></tr></table>

Mode 1 - Health Index

Mode 2 - Health Index

Mode 3 - Health Index

Mode 4 - Health Index

Mode 5 - Health Index

Mode 6 - Health Index

Failure 1

Boundary

<table border="1"><tr><td colspan="22">Dataset #3</td></tr><tr><td>20</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>18</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>16</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>14</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>12</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>10</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>8</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>6</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>4</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>2</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

<table><tr><td>○ Mode 1 - Health Index</td></tr><tr><td>● Failure 1</td></tr><tr><td>○ Failure 2</td></tr><tr><td>★ Boundary</td></tr></table>



Fig.9 continued


> **Figure Description:**

The image displays two scatter plots, labeled "Dataset #4" and "Dataset #5," representing spatial data points on a 2D grid with X and Y axes ranging from 0 to 25. Each plot uses a color-coded legend to categorize points: Mode 1 (dark blue), Mode 2 (orange), Mode 3 (yellow), Mode 4 (purple), Mode 5 (light blue), Failure 1 (bold blue circles), Failure 2 (bold red circles), and Boundary (black stars).

In Dataset #4, the points are arranged in a grid from 0 to 24 on both axes. The "Boundary" stars form a complex, winding path that separates different clusters of health indices and failure modes. Failure 1 points are concentrated in the upper right and lower left regions, while Failure 2 points appear in smaller clusters near the center and lower right. The background is populated by a mix of Mode 1 through Mode 6 health index points, which fill the remaining grid spaces.

In Dataset #5, the grid spans X from 0 to 22 and Y from 0 to 22. The "Boundary" stars form a distinct, branching structure that separates a large central region of Failure 1 points from the surrounding health index modes. Mode 2 (orange) and Mode 3 (yellow) points dominate the upper and left portions of the plot, while Mode 5 (light blue) points occupy the right side. The Failure 1 points form a vertical, somewhat irregular column through the center of the plot, bounded by the black stars. Both plots utilize identical axis scaling and legend markers to visualize the classification of data points across the spatial domain.



This evaluation is performed for all datasets with a custom threshold of 10%. It results that there are around 3% of engines where H2 is not relevant. For a dataset of 249 engines, H1 is more relevant than H2 for only eight engines. H2 is therefore acceptable for this case study.

## 4.5.2 Fault subregions identification

For the fault subregions identification, only map nodes that are included in the PDF shape are retained. The user customizes the threshold according to the required precision. This is linked to the probability of training engines of which their last flight cycle has hit the fault mode area. A threshold of 0.40 was used, meaning that all nodes with a probability density lower than 40% are removed. The results are shown in Fig. 9.

When an engine degrades up to a point a failure mode is likely to happen, fault mode area is crossed on each operational mode. Based on this observation, the fault mode is considered to be the same on each map cluster and labeled as failure in Fig. 9.

## 4.5.3 Fault modes association

The fault modes association phase can only be performed on similar datasets as explained in Sect. 4.2. Thus, the datasets #1 and #3 are similar (similar operational settings and operation conditions) as well as the datasets #2 and #4. The use of datasets with one fault mode (i.e., the datasets #1 and #2) to identify the same failure on the maps trained with two failures (i.e., the datasets #3 and #4) results in a



<div align="center">

Fig.10 Fault modes identification for maps #3 and #4

</div>

<table border="1"><tr><td>Map #3 with Dataset #1</td><td>Mode 1 - Health Index
Mode 1 - Last Cycle Hit
Failure 1
Failure 2
Boundary</td></tr><tr><td>Map #4 with Dataset #2</td><td>Mode 1 - Health Index
Mode 1 - Last Cycle Hit
Mode 2 - Health Index
Mode 2 - Last Cycle Hit
Mode 3 - Health Index
Mode 3 - Last Cycle Hit
Mode 4 - Health Index
Mode 4 - Last Cycle Hit
Mode 5 - Health Index
Mode 5 - Last Cycle Hit
Mode 6 - Health Index
Mode 6 - Last Cycle Hit
Failure 1
Failure 2
Boundary</td></tr></table>

clear and unambiguous identification. The found fault mode is associated with the corresponding failure.

As shown in Fig. 9, the datasets #3 and #4 have both two fault modes, named, respectively, failures 1 and 2. Yet, the faulty system part is unknown. As mentioned, datasets #1 and #2 are used to identify one of the two failures on maps trend with datasets #3 and #4.

Figure 10 shows that all engines from the datasets #1 and #2 are, respectively, in the cluster failure 1 of the datasets #3 and #4, following the hit number estimation 'H2' (see Sect. 3.4.1). Knowing that #1 and #2 have HPC fault modes (Table 1), failures 1 and 2 are, respectively,

identified as HPC and fan fault mode. With this knowledge the fault modes of each engine in the datasets #3 and #4 can be determined.

However, on the map #4 (Fig. 10), some engines are out of a failure area, such as in modes 3 and 4, or misclassified, such as in mode 6. With the hit number estimation 'H2,' it represents 0.19% of error, whereas with the hit number estimation 'H1,' all engines are perfectly classified for this study. The failure identification procedure is then considered satisfactory.



## 5 Conclusion

This study addresses early detection and classification of faults through an unsupervised learning approach, without prior knowledge, based on self-organizing maps (SOMs). This neural network is at the core of the automatized approach. A complete process to comprehend the concept and to use SOM has been presented. The SOM has some advantage such as unsupervised training and is useful for dimensionality reduction and representation of complex and large datasets thanks to the map visualization. A methodology has been described to build and to configure the SOM according to the case study. The article highlights the possibility to identify the operational mode and fault modes inside generated maps with a methodology relying on the kernel density estimation. The methodology has been illustrated on a case study for diagnosing jet engine datasets. Without prior knowledge on the faults, the proposed algorithm was able to identify the number of operational modes as well as the fault mode number for the five datasets. Furthermore, the fault subregions identification estimates fault mode areas on the map, leading to failures identification on each cluster.

The unsupervised classifier used is a SOM neural network. There exist different types of unsupervised clustering techniques such as hierarchical or Bayesian clustering that could provide different results according to the case study [48]. Another candidate for future work could be a network based on restricted Boltzmann machines (RBM) [49] that will provide a probability distribution over its set of inputs.

In the current study, the automatic fault mode identification was experimented up to two fault modes. For future work, the study should be extended to more than two failure modes on the same case study. Two ways to evaluate the hit number have been explored. Other hypothesis could be examined. The used feature for #1 to #4 was supposed to be same than for #5. A generic approach to get automatically the best set of feature for different types of data will be a good solution to consider, as well as for the custom factor for the map size reduction. A study could be performed to explore the use of the presented approach with a different case study.

Acknowledgements The author affiliated to Sogeti High Tech and ISAE-SUPAERO gratefully acknowledges his colleagues who provided insight and expertise through this paper.

## Compliance with ethical standards

Conflict of interest Sébastien Schwartz, Juan José Montero Jimenez Michel Salaun and Rob Vingerhoeds declare that they have no conflict of interest.

## References

1. Simon DL, Rinehart AW (2014) A model-based anomaly detection approach for analyzing streaming aircraft engine measurement data. In: Volume 6: Ceramics; controls, diagnostics and instrumentation; education; manufacturing materials and metallurgy, Düsseldorf, Germany. ASME, p V006T06A032. https:// doi.org/10.1115/gt2014-27172

2. Naderi E, Meskin N, Khorasani K (2012) Nonlinear fault diagnosis of jet engines by using a multiple model-based approach. J Eng Gas Turbines Power 134(1):011602. https://doi.org/10.1115/1.4004152

3. Zeng D, Zhou D, Tan C, Jiang B (2018) Research on model-based fault diagnosis for a gas turbine based on transient performance. Appl Sci 8(1):148. https://doi.org/10.3390/app8010148

4. Naderi E, Khorasani K (2017) Data-driven fault detection, isolation and estimation of aircraft gas turbine engine actuator and sensors. In: 2017 IEEE 30th Canadian conference on electrical and computer engineering (CCECE), Windsor, ON. IEEE, pp 1-6. https://doi.org/10.1109/ccece.2017.7946715

5. Sarkar S, Jin X, Ray A (2011) Data-driven fault detection in aircraft engines with noisy sensor measurements. J Eng Gas Turbines Power 133(8):081602. https://doi.org/10.1115/1.4002877

6. Svärd C, Nyberg M, Frisk E, Krysander M (2014) Data-driven and adaptive statistical residual evaluation for fault detection with an automotive application. Mech Syst Signal Process 45(1):170-192. https://doi.org/10.1016/j.ymssp.2013.11.002

7. Pourbabaee B, Meskin N, Khorasani K (2016) Robust sensor fault detection and isolation of gas turbine engines subjected to time-varying parameter uncertainties. Mech Syst Signal Process 76-77:136-156. https://doi.org/10.1016/j.ymssp.2016.02.023

8. Venkatasubramanian V (2005) Prognostic and diagnostic monitoring of complex systems for product lifecycle management: challenges and opportunities. Comput Chem Eng 29(6):1253-1263. https://doi.org/10.1016/j.compchemeng.2005.02.026

9. Vingerhoeds RA, Janssens P, Netten BD, Aznar Fernández-Montesinos M (1995) Enhancing off-line and on-line condition monitoring and fault diagnosis. Control Eng Pract 3(11):1515-1528. https://doi.org/10.1016/0967-0661(95)00162-N

10. Montero Jimenez JJ, Vingerhoeds R (2018) Enhancing operational fault diagnosis by assessing multiple operational modes. In: MOSIM'18—Conférence Internationale de Modélisation, Optimisation et Simulation, Toulouse

11. Kohonen T (1982) Self-organized formation of topologically correct feature maps. Biol Cybern 43(1):59-69. https://doi.org/ 10.1007/BF00337288

12. Germen E, Başaran M, Fidan M (2014) Sound based induction motor fault diagnosis using Kohonen self-organizing map. Mech Syst Signal Process 46(1):45-58. https://doi.org/10.1016/j.ymssp.2013.12.002

13. Côme E, Cottrell M, Verleysen M, Lacaille J (2010) Aircraft engine health monitoring using self-organizing maps. In: Perner P (ed) Advances in data mining. Springer, Berlin, pp 405-417. https://doi.org/10.1007/978-3-642-14400-4_31

14. Cottrell M, Gaubert P, Eloy C, François D, Hallaux G, Lacaille J, Verleysen M (2009) Fault prediction in aircraft engines using self-organizing maps. In: Príncipe JC, Miikkulainen R (eds) Advances in self-organizing maps, vol 5629. Springer, Berlin, pp 37-44. https://doi.org/10.1007/978-3-642-02397-2_5

15. Katunin A, Amarowicz M, Chrzanowski P (2015) Faults diagnosis using self-organizing maps: a case study on the



DAMADICS benchmark problem, pp 1673-1681. https://doi.org/ 10.15439/2015f26

16. Yu H, Khan F, Garaniya V (2015) Risk-based fault detection using self-organizing map. Reliab Eng Syst Saf 139:82-96. https://doi.org/10.1016/j.ress.2015.02.011

17. Chen X, Yan X (2012) Using improved self-organizing map for fault diagnosis in chemical industry process. Chem Eng Res Des 90(12):2262-2277. https://doi.org/10.1016/j.cherd.2012.06.004

18. Dharshini R, Hemanandhini S (2016) Brain tumor segmentation based on self organising map and discrete wavelet transform. In: 2016 international conference on computer communication and informatics (ICCCI), Coimbatore, India. IEEE, pp 1-9. https:// doi.org/10.1109/iccci.2016.7479960

19. Peel L (2008) Data driven prognostics using a Kalman filter ensemble of neural network models. In: 2008 international conference on prognostics and health management. https://doi.org/ 10.1109/phm.2008.4711423

20. Jolliffe I (2011) Principal component analysis. Springer, Berlin. https://doi.org/10.1007/b98835

21. Sammon JW (1969) A nonlinear mapping for data structure analysis. IEEE Trans Comput 100(5):401-409. https://doi.org/10. 1109/t-c.1969.222678

22. Wang T, Jianbo Y, Siegel D, Lee JA (2008) Similarity-based prognostics approach for remaining useful life estimation of engineered systems. In: 2008 international conference on prognostics and health management. IEEE, pp 1-6. https://doi.org/10.1109/phm.2008.4711421

23. Guyon I, Elisseeff A (2003) An introduction to variable and feature selection. J Mach Learn Res 3:1157-1182

24. Jovic A, Brkic K, Bogunovic N (2015) A review of feature selection methods with applications. In: 2015 38th international convention on information and communication technology, electronics and microelectronics (MIPRO), Opatija, Croatia. IEEE, pp 1200-1205. https://doi.org/10.1109/mipro.2015. 7160458

25. Saeys Y, Inza I, Larranaga P (2007) A review of feature selection techniques in bioinformatics. Bioinformatics 23(19):2507-2517. https://doi.org/10.1093/bioinformatics/btm344

26. Visalakshi S, Radha V (2014) A literature review of feature selection techniques and applications: review of feature selection in data mining. In 2014 IEEE international conference on computational intelligence and computing research. IEEE, Coimbatore, India, pp 1-6. https://doi.org/10.1109/iccic.2014.7238499

27. Kohonen T (1997) Springer series in information sciences, vol 30. Springer, Berlin. https://doi.org/10.1007/978-3-642-97966-8

28. Kohonen T (2014) Unigrafia, Helsinki, Finland

29. Zin ZM (2014) Cluster and visualize data using 3D self-organizing maps. In: 2014 11th international conference on ubiquitous robots and ambient intelligence (URAI). IEEE, pp 163-168. https://doi.org/10.1109/urai.2014.7057523

30. Azcarraga A, Manalili S (2011) Design of a structured 3D SOM as a music archive, pp 188-197. https://doi.org/10.1007/978-3-642-21566-7_19

31. Gorricha J, Lobo V (2012) Improvements on the visualization of clusters in geo-referenced data using self-organizing maps. Comput Geosci 43:177-186. https://doi.org/10.1016/j.cageo.2011.10.008

32. El Tobely T, Salem A (2005) Position detection of unexploded ordnance from airborne magnetic anomaly data using 3-D self organized feature map. In: Proceedings of the fifth IEEE international symposium on signal processing and information technology, 2005. IEEE, pp 322-327. https://doi.org/10.1109/isspit.2005.1577117

33. Fujimura K, Masuda K, Fukui Y (2006) A consideration on the multi-dimensional topology in self-organizing maps. In: 2006

international symposium on intelligent signal processing and communications, IEEE, pp 825-828. https://doi.org/10.1109/ ispacs.2006.364772

34. Côme E, Cottrell M, Verleysen M, Lacaille J (2010) Self organizing star (SOS) for health monitoring. In: European conference on artificial neural networks, pp 99-104

35. Tian J, Azarian MH, Pecht M (2014) Anomaly detection using self-organizing maps-based k-nearest neighbor algorithm. In: European conference of the prognostics and health management society

36. Engelbrecht AP (2007) Computational intelligence: an introduction, 2nd edn. Wiley, Hoboken. https://doi.org/10.1002/9780470512517

37. Su M-C, Liu T-K, Chang H-T (1999) An efficient initialization scheme for the self-organizing feature map algorithm. In: IJCNN'99. International joint conference on neural networks. Proceedings (Cat. No. 99CH36339), vol 3. IEEE, pp 1906-1910. https://doi.org/10.1109/ijcnn.1999.832672

38. Kohonen T (2001) Springer series in information sciences, vol 30, 3rd edn. Springer, Berlin. https://doi.org/10.1007/978-3-642-56927-2

39. Kaski S, Venna J, Kohonen T (2000) Coloring that reveals cluster structures in multivariate data. Aust J Intell Inf Process Syst 6:82-88

40. Alahakoon D, Halgamuge SK, Srinivasan B (2000) Dynamic self-organizing maps with controlled growth for knowledge discovery. IEEE Trans Neural Netw 11(3):601-614. https://doi.org/ 10.1109/72.846732

41. Natita W, Wiboonsak W, Dusadee S (2016) Appropriate learning rate and neighborhood function of self-organizing map (SOM) for specific humidity pattern classification over Southern Thailand. Int J Model Optim 6(1):61-65. https://doi.org/10.7763/IJMO. 2016.V6.504

42. Zhang W, Wang J, Jin D, Oreopoulos L, Zhang Z (2018) A deterministic self-organizing map approach and its application on satellite data based cloud type classification. In: Conference IEEE Big Data

43. Saxena A, Goebel K, Simon D, Eklund N (2008) Damage propagation modeling for aircraft engine run-to-failure simulation. In: 2008 international conference on prognostics and health management. IEEE, pp 1-9. https://doi.org/10.1109/phm.2008. 4711414

44. Kafadar K, Bowman AW, Azzalini A (1999) Applied smoothing techniques for data analysis: the kernel approach with S-PLUS J Am Stat Assoc 94(447):982. https://doi.org/10.2307/2670015

45. Bowman AW, Azzalini A (1997) Applied smoothing techniques for data analysis: the kernel approach with S-Plus illustrations, vol 18. Oxford University Press, Oxford

46. Frederick DK, DeCastro JA, Litt JS (2007) User's guide for the commercial modular aero-propulsion system simulation (C-MAPSS)

47. Hu C, Youn BD, Wang P, Taek Yoon J (2012) Ensemble of data-driven prongostic algorithms for robust prediction of remaining useful life. Reliab Eng Syst Saf 103:120-135. https://doi.org/10.1016/j.ress.2012.03.008

48. Fusco G, Perez J (2019) Bayesian network clustering and selforganizing maps under the test of Indian Districts. A comparison. Cybergeo. https://doi.org/10.4000/cybergeo.31909

49. Zhang X, Yao L, Wang X, Monaghan J, Mcalpine D, Zhang Y (2019) Cs Eess Q-Bio. arXiv:1905.04149

Publisher's Note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.



Intentionally left blank

<div align="center">

# Ontology and CBR integration article

</div>

Intentionally left blank

<div align="center">

# INTEGRATING ONTOLOGIES AND CASE-BASED REASONING FOR THE DEVELOPMENT OF KNOWLEDGE-INTENSIVE INTELLIGENT SYSTEMS.

</div>

Hugo Muñoz-Hernandez

Rob Vingerhoeds

ISAE-SUPAERO

10 Avenue Edouard Belin 31055 Toulouse, France hugo.munoz-hernandez@student.isae-supaero.fr rob.vingerhoeds@isae-supaero.fr

Juan José Montero-Jiménez TEC-Tecnológico de Costa Rica Calle 15, Avenida 14

1 km al sur Basílica de los Ángeles

Provincia de Cartago, Cartago, 30101, Costa Rica

juan.montero@itcr.ac.cr

KEYWORDS

Ontology, Case-Based Reasoning (CBR), similarity function.

## ABSTRACT

Case-Based Reasoning (CBR) allows emulating the human inference of solutions to problems profiting from previous experience. The integration of CBR with ontologies, structured organization of semantic knowledge, has been in the attention for some time, aiming to create powerful knowledge-intensive systems capable of proposing appropriate solutions to problems. This entails having collected an appropriate number of previous cases as well as having established a suitable ontology for the application domain. This paper focuses on the integration of CBR and ontologies to support the case representation, case base storage, and semantic similarity estimation. Different alternatives for such integration are explored and the approach has been tested in the creation of a Decision-Support System for the design of predictive maintenance systems. This work opens the window to significantly improve the capabilities of a CBR system by using the knowledge materialization and the reasoning features of a specific domain ontology.

## INTRODUCTION

Since a long time ago, man has been fascinated with making a machine that had the same capabilities as human beings (think, speak, move, ...). That is the origin of the vast domain of Artificial Intelligence, which definition for this paper is considered as the following:

Artificial intelligence supplies a collection of techniques to manipulate knowledge in such a manner that new results emerge and new inferences that were not explicitly programmed.

Broadly, two areas can be distinguished in AI: symbolic AI and sub-symbolic AI. The latter comprises neural networks, data-driven techniques, that have had a lot of attention since the last 20 years. The former, symbolic AI, concerns knowledge-based systems and may involve techniques such as rule-based, fuzzy logic, Case-Based Reasoning where the knowledge is

contained in well-defined blocks of previous experience, etc (Vingerhoeds et al. 1995).

In this paper, the focus is on Case-Based Reasoning and ontologies. Case-Based Reasoning was developed under the philosophy that human beings think and reason using analogies and examples, rather than rules (Kolodner 1993). The idea is that one may recall previous similar situations when being confronted with a new problem. Starting from this previous experience (knowledge) ideas can be derived for addressing the new situation. Case-Based Reasoning is therefore an approach in which specific knowledge of previously experienced problem situations is being used to solve a new problem. This is being done by finding similar previous cases and reusing previous experiences. Allowing continuously to add new cases, new pieces of knowledge, Case-Based Reasoning supports incremental, sustained learning, where information from new situations is kept for future use.

Ontologies are formal explicit descriptions of concepts in a domain of discourse, properties of each concept describing its features, attributes and restrictions (Noy and McGuinness 2000). One of the most common goals in developing ontologies is "sharing a common understanding of the structure information among people and software agents" (Gruber 1993). However, there are also several other motivations to create ontology models such as enabling reuse and analysis of domain knowledge or making domain assumptions explicit. Ontologies are powerful tools for knowledge representation.

In this paper, the integration of ontologies with Case-Based Reasoning is being addressed. The goal of such an integration is to make use of the advantages of both approaches. For example, ontologies enable the processing and sharing of knowledge that can be used at different tasks of Case-Based Reasoning systems, such as representing the input problem, enhancing similarity assessments, case representation, case abstraction and case adaptation.

The paper is organised as follows. In the next section, the context is presented, including an overview of CBR, ontologies, and their integration. After that, an-

other section is focused on explaining the use case for which the integration of CBR and ontologies has been developed. Then, the Development section shows how the integration was carried out, followed by some results and a discussion. The paper concludes by summarizing the lessons learnt and providing indications for future work

## CONTEXT

The trigger for the work presented in this paper can be found in the development of a Decision-Support System for the design of predictive maintenance systems (Montero Jimenez et al. 2021). Ontologies have been used as formal knowledge representations that support a CBR system. This section provides the theoretical background of both technologies.

## Case-Based Reasoning (CBR)

Case-Based Reasoning consists of proposing solutions to problems within a certain domain profiting of the knowledge derived from previous cases, representing previous knowledge. Indeed, one of the characteristics of human learning is to use past experiences as a reference for the future. A complete reasoning cycle in CBR is divided into four phases(Aamodt and Plaza 1994): retrieval, reuse, revise and retain.

The development of CBR systems starts by defining the case structure, a set of variables that will be used to describe the problem and its corresponding solution from the past. The problem attributes or features are used to estimate the similarity between the target case and the cases stored in a case base. Once the features have been established, the next step is to define similarity functions. These are algorithms, with diverse levels of complexity, that when applied to a pair of values of the corresponding variable they return a similarity value number, normally between 0 and 1. Each problem attribute has its own local similarity. An aggregation function is used to consolidate all local similarities in a global similarity value. Each local similarity can receive special weights that multiply the local similarity values when calculating the global similarity. Case-based reasoning is a flexible reasoning paradigm. It is capable to compute similarities and retrieve similar cases from a case base even when only partial information is known from the target case.

In this work, the software myCBR $ ^{1} $ was used. The choice for this software was due to the availability of the Java source code, which allowed for adapting the system to the needs of the study. Different types of case attributes for similarity definition are available in myCBR, of which three have been used in the current research: String, Symbol and Integer. Both String and Symbol attributes have textual values, whereas for Symbol the values are limited to a list of allowed values and fixed similarities among them, and String similarity is based on free text. By default, the String similarity function assigns a binary similarity to each string but this function can also include further analysis by applying the Levenshtein string comparison method that can tolerate typing errors in the string and still compute a similarity value. The function applied to Integer attributes is very flexible, and the user can control the shape of the function $ \mathbb{Z}\rightarrow\mathbb{R} $ . Once the case concept is created and the attributes are defined, a case base can be stored as a list of instances of the concept with values assigned to each one of the attributes. Then, the system will be ready for querying and retrieving cases. A deeper explanation of how to model knowledge in myCBR can be found in (Bach et al. 2014).

## Ontologies

An ontology defines a set of representational primitives with which to model a domain of knowledge or discourse (Gruber 2009). In a practical sense, ontologies represent a vocabulary of concepts whose basic structure is a hierarchy of classes and subclasses. Instances can be defined as individuals belonging to classes in ontology, so as they will match the common features defining such classes. Important components of ontologies are the Object Properties which can establish links between pairs of instances or classes, and Data Properties, which can assign information tokens to particular instances. These properties are defined within a certain domain and range, which means that they are restricted, by definition, to particular classes or data types. In general, when referring to ontology entities, that includes classes, individuals and properties. The Protégé ontology editor (Stanford University 2016-2020) was used for the development of the ontology for this research.

The initiative of the Semantic Web by the World Wide Web Consortium (OWL Working Group 2012) is to gather as much knowledge as possible into the internet in a format that is readable for computers. For such purposes, the OWL2 ontology language is used. Standard ontologies like the BFO (Basic Formal Ontology) (International Organization for Standardization 2020) and CCO (Common Core Ontologies) (Rudnicki 2019) are developed and published to be the roots of all the domain-specific ontologies that may be proposed.

Other for the current study relevant aspects of ontologies concern reasoning and queries. A reasoning process can be performed on an ontology to check its logical consistency. This allows verifying, for example, if the instancing of individuals reveals no class contradictions or if the Object Properties declarations respect the restrictions of domain and range. Another important aspect of ontology reasoning is the inference of relations; some links could be established between certain entities in the ontology that was not initially explicit but logically deduced from the original ontology

structure. Various reasoners for OWL language exist, amongst which the HermiT reasoner (Glimm et al. 2014), which was used for this study. Queries allows extracting information from ontologies; they are questions that can be posed to get a specific information out of the ontology. Three different procedures or languages to query OWL ontologies exist: SPARQL, Description Logics (DL) and SQWRL. The SPARQL language allow extracting table structured information from an ontology by querying for entities that match certain conditions and have some kind of relation between them. This type of query does not need a reasoning process. A plug-in is available for Protégé to execute SPARQL queries. In this study, for the Java implementation, the Jena API has been used. Description Logics allow executing simple queries by using a reasoner and checking at first the ontology consistency. They are available by default in Protégé and also accessible with the OWL API implementation for Java. The SQWRL language is based on the SWRL rule language, and it allows to execute very accurate and specific queries using a reasoner. Again, a Protégé plug-in is available. In Java it may be used the SWRL API with a drools reasoning engine implementation available.

An ontology for the selection and assessment of predictive maintenance models was developed to support the CBR approach (Montero Jimenez et al. 2021). The OMSSA (Ontology model for Maintenance Strategy Selection and Assessment) includes all the necessary concepts of the maintenance domain to describe predictive maintenance systems architecture and application cases. The ontology was built as an extension of the standard BFO and CCO ontologies in order to be as general as possible and to possibly be re-used in the future by other ontology developers.

## Related work: integration CBR-ontologies

Ontologies and Case-Based Reasoning have been increasingly used together in the last decade. One of the most important aspects of developing CBR systems is the vocabulary framework. Ontologies have played an important role in providing this vocabulary framework for several CBR applications. For example, (Qin et al. 2018) implemented and ontology supported case-based reasoning approach for computer-aided tolerance specification. In (Amailef and Lu 2013) an ontology was integrated with a CBR system for emergency response services. (Recio-Garía and Díaz-Agudo 2007) presented a system that brought together the CBR Java framework jCOLIBRI and Description Logics (DL) to calculate a concept-based similarity values between terms according to their position in the classification structure within the ontology. The same framework was used in (Kowalski et al. 2013) for the domain of logistics adding some variables that were defined in a specific domain ontology. In (Yin et al. 2010), CBR and ontologies are used to test a criminal

investigation system. An ontology is used as a casebase and structure-based similarity values are calculated for case retrieval.

Instantiated ontologies can be used as case bases for CBR implementations as the case structure can be easily represented in the ontology. Ontologies may also help to compute semantic similarity based on ontological similarity, which can be classified into structure-based similarity and feature-based similarity. Structure-based similarity considers the ontology as a graph where concepts are linked by relations (taxonomic or others). Some methods may be proposed to measure the path distance between a pair of concepts to define their similarity value. For example, in (Avdeenko and Makarova 2018) a hierarchical ontology is used to assign similarity values between some pairs of concepts within a specific domain. Feature-based similarity is focused on comparing sets of features of two different terms, established through their property assertions. Feature-based similarity could provide a deeper and more flexible understanding of the domain vocabulary and thus better results in the semantic similarity computation. That is why in this work a feature-based similarity method is used, see also (Sánchez et al. 2012) and (Bai et al. 2008).

The actual integration of ontologies and CBR does not always receive enough attention in application articles. This paper attempts to cover such gap by providing insight on the different possibilities to integrate ontologies and CBR for the development of knowledgeintensive smart systems.

## USE CASE: PREDICTIVE MAINTENANCE SYSTEMS DESIGN

Predictive Maintenance (PdM) is a strategy that aims at triggering maintenance actions based on accurate diagnostics or prognostics before an undesired failure occurs. More specifically, predictive maintenance includes monitoring and modelling the system health, estimating the remaining useful life, and detecting and identifying the actual faults. To perform these tasks there exist several types of models that can be used for diagnostics and prognostics purposes (Montero Jiménez et al. 2020). These models analyze the physical variables measured during the operation of the system of interest. For example, in the case of a turbo-machine, some relevant operation variables to consider for predictive maintenance purposes could be the measurements of combustion temperature, pressure and axis vibrations.

A predictive maintenance approach is normally focused on the health state of the system to be maintained or on the incipient failures that may appear during its functioning, sometimes modelling the evolution of these features over time. For example, a predictive maintenance strategy conceived for health assessment may have as main objective to measure the degradation of the system compared to the optimal operation con-

dition that the system had at the beginning. Another possible task in predictive maintenance is to detect or identify automatically failures that are affecting the system and that might perturb its functioning. In addition, the power of predictive maintenance applications increases when considering the capabilities to forecast the evolution of the system health and even predict an estimation of the remaining useful life.

In order to perform all these tasks, three families of models may be considered: data-driven models, knowledge-based models and physics-based models (Montero Jiménez et al. 2020). Data-driven models have an increased popularity during the last years thanks to the current advances in computational power. Statistical models, stochastic models and machine learning are the main model types within data-driven models. In knowledge-based models, previous experiences are used to infer solutions to current problems, in form of for example rules or cases. Physics-based models are very specific for each application case, as they use a physical simulation of the system to perform predictive maintenance functions with the available data. When developing predictive maintenance systems, one of the challenges lies in the selection of the appropriate model for the knowledge representation (a large amount of options) and to position the retained model(s) for the knowledge representation within the systems architecture (Montero Jiménez and Vingerhoeds 2019).

This work is focused on providing a knowledgeintensive system to find the most adequate predictive maintenance solutions for the particular situations. For this purpose, Case-Based Reasoning appears to a suitable technique, as it allows to deal with symbolic information gathered previous predictive maintenance realisations.

## INTEGRATION OF ONTOLOGIES AND CBR FOR THE DEVELOPMENT OF A DECISION SUPPORT SYSTEM

In the current study, a domain ontology (OMSSA) (Montero Jimenez et al. 2021), developed with the ontology editor Protégé (Stanford University 2016-2020), was integrated with the myCBR engine. An instantiated version of OMSSA serves as case base and provides the knowledge for feature-based similarity measures for the myCBR engine. The methodology to estimate featurebased similarity was adopted from (Sánchez et al. 2012). The OWL API (Horridge and Bechhofer 2011) is used to develop a direct link between the myCBR data files .prj and the .owl ontologies. The HermiT reasoner was used to verify ontology database consistency, infer relations and execute "Description Logic" queries for information extracting, necessary for the feature-based similarity functions. Ontology instantiation is carried out by queries that can retrieve data from different sources, such as for example .csv files.

## Variables definition for the application case

The application case is a Predictive Maintenance Decision-Support System. In this section, some of the implementation details will be presented, so to show how CBR and ontologies can work together. As mentioned before, a first step to implement a CBR application concerns the definition of the variables describing the cases. In the current study, such cases describe previous solutions of Predictive Maintenance (PdM) that have been successfully implemented on different systems of interest. Based on (Montero Jiménez et al. 2020), the main characteristics of each case were described in a systematic set of data fields. Some of the data fields are used as case retrieval variables. Following the logic of myCBR, those variables are attributes that must be included in the concept definition:

- Task (Symbol): what is the specific function of the predictive maintenance system (e.g. health modelling).

- Case study type (Symbol): what is the type of maintainable system (e.g. a rotary machine).

- Case study (String): specific system to be maintained (e.g. jet engines).

- Input type (Symbol): list of measurable physical variables (e.g. temperature, pressure and power).

- Online/Off-line (Symbol): predictive maintenance analysis to be done online or offline?

- Input for the model (Symbol): data format type provided to the predictive maintenance module (e.g. signal data).

- Publication year (Integer): the year in which the study was published.

The attributes of type Symbol take textual values among a list of allowed values that must be specified for each of them. In addition to these data fields that are important for the case retrieval, other variables are considered as solution attributes of the case and may be exploited once the relevant cases are retrieved. Some of the solution attributes suggested by the decision support system include: study title, publication identifier, predictive maintenance model used, performance indicators, etc.

## Instancing cases in the ontology

Originally, myCBR stores the case base in .csv tabular format. This .csv tabular format was replaced by an instantiated version of OMSSA. A Java code was developed with specific methods to read all data and to make it fit in an ontology structure: classes, instances and Object Properties/Data Properties assertions. An OWL API implementation in Java was needed for such a purpose. The CCO ontologies are taken as a base, especially the Information Entity Ontology and the Artifact Ontology (Rudnicki 2019). Most of the classes

in the ontology are defined as subclasses of the already existing classes in the previously mentioned ontologies. The relations used to form the case structure are those compiled in the Table 1. Properties written in blue are included in CCO, those in green are included in OBO Relations Ontology from BFO (International Organization for Standardization 2020) and those in black have been specifically created in OMSSA. Parentheses contain the parent ontology, considering that a property can be a sub-property of a parent.

<div align="center">

Table 1: Object Properties in OMSSA.

</div>

<table border="1"><tr><td>Property</td><td>Domain</td><td>Range</td></tr><tr><td>designates</td><td>Designative Information Content Entity</td><td>No specific range</td></tr><tr><td>describes</td><td>Descriptive Information Content Entity</td><td>No specific range</td></tr><tr><td>is carrier of</td><td>Independent continuant</td><td>Generically dependent continuant</td></tr><tr><td>has part</td><td>No specific Domain</td><td>No specific range</td></tr><tr><td>has title(is carrier of)</td><td>Predictive maintenance article</td><td>Article title</td></tr><tr><td>has identifier(is carrier of)</td><td>Predictive maintenance article</td><td>Article identifier</td></tr><tr><td>has publication year(is carrier of)</td><td>Predictive maintenance article</td><td>Publication year</td></tr><tr><td>has synchronization(has quality)</td><td>Predictive maintenance system module</td><td>Module synchronization</td></tr><tr><td>has predictive maintenance function(has function)</td><td>Predictive maintenance system module</td><td>Predictive maintenance module function</td></tr></table>

The very basic structure of a case starts with an instance of a Predictive maintenance case (subclass of Designative Information Content Entity), designating an instance of a Predictive maintenance system module (subclass of Information Processing Artifact). The items to be maintained are instances of the different subclasses in Maintainable item (equivalent to Artifact). Then, the models are instances of the type subclasses in the Predictive maintenance model. The models operate over a set of variables that are recovered from the operation of the item. These variables are instances of Data variable (subclass of Descriptive Information Content Entity). As the instances of variables are physical concepts (for example, the temperature), they can be reused in more than one case of the database. For each one of the different measurable magnitudes that are mentioned in the database, there exists one single instance of Data variable. The functioning of the module and the models used for a certain case are explained in the corresponding Predictive maintenance article. The title and the identifier of those articles are assigned to instances Article title and Article identifier respectively (both are subclasses of Designative Information Content Entity). In summary, a maintenance module uses one or more models to perform a predictive maintenance diagnosis or prognostic task on a certain system Maintainable

item) based on the data of measured magnitudes recovered during the system operation. This is identified as a predictive maintenance case which is described in a specific research article (see also Figure 1, please note that some elements were omitted for clarity reasons).


> **Figure Description:**

This diagram illustrates a conceptual model using a legend that defines yellow circles as "Class," purple diamonds as "Instance," blue squares as "Object property," and blue dashed-line rectangles as "Set of entities." The diagram depicts various relationships between these elements. At the top left, a yellow circle labeled 9 connects to a purple diamond, which has a bidirectional relationship labeled A and E with another purple diamond. This second diamond connects to a vertical line that leads into a dashed-line box containing two purple diamonds. To the right, yellow circles 1 and 2 connect to purple diamonds, with a relationship labeled A between them. The diamond under 2 connects to a vertical line with four black dots, which represent connection points for relationships labeled B, B, C, D, and D.

The relationships labeled B connect the top two black dots to purple diamonds within a dashed-line box, which also contains yellow circles 3.X and 3.Y. A yellow circle labeled 3 connects to this box. Below this, yellow circles 4, 5, and 6 connect to 4.X, 5.X, and 6.X respectively, which then connect to purple diamonds. These diamonds are linked to the vertical line at the black dots corresponding to relationships C, D, and D. Finally, at the bottom, a yellow circle labeled 7 connects to a dashed-line box containing two purple diamonds followed by an ellipsis, with a relationship labeled B pointing toward this box from the diamond associated with 6.X. A vertical line segment labeled B connects the top-most purple diamond to the dashed-line box containing 3.X and 3.Y.



<div align="center">

Figure 1: Partial schema of the entities participating in the case representation in the ontology.

</div>

- Yellow nodes in Figure 1 represent OMSSA classes:

1. Predictive maintenance case

2. Predictive maintenance system module

3. Predictive maintenance model

4. Predictive maintenance function

5. Maintainable item

6. Maintainable item record

7. Data variable

8. Predictive maintenance article

9. Article title

- The labelled edges in Figure 1 represent OMSSA object properties:

A. designates

B. is carrier of

C. has predictive maintenance function

D. has part

E. has title

- The classes with a tag N.X are subclasses of the parent class N.

In order to assign the textual values to the article title, the article identifier and the reference tag of the case, which will be materialized as Designative Information Content Entities in the ontology, the property information has text value is used.

## Similarity functions

When defining a similarity function, the type of variable is a major point to consider. The similarity functions of a Symbol variable are specified in myCBR with a set of pairs of textual values with a similarity value assigned between 0 and 1. These values are estimated according to experimental and physical similarity criteria for the case variables Case study type, Input for the model and Online/offline. One of the objectives of this study is to assess feature-based semantic methods to obtain similarity values, so the procedure proposed (Sánchez et al. 2012) was adapted to the application case and the relations existing in the ontology. The basis of this method is to compare two sets of elements A and B. The following formula is used to obtain a normalized similarity of the sets:

$$
S i m i l a r i t y = 1 - \log_ {2} \left(1 + \frac {A / B + B / A}{A / B + B / A + A \cap B}\right)
$$

In the equation above, A/B means the difference between sets A and B, so the elements from A that do not belong to B. A $ \cap $ B is the intersection of A and B.

The case feature Input type is a list of variables that are monitored during the operation of the system to be maintained. These variables are represented in the ontology with instances of the class Data variable. The above-mentioned method is used to compare the set of values in the query case with all cases in the case base. The attribute Input type in myCBR will store the list of variables as a textual value separated by commas. When executing a query, a list of variables names is proposed, so the algorithm first has to add this list to the allowed values of the attribute. Then, the similarity values are assigned to all the pairs formed by the query string and all the textual values existing in the database. The variable names are separated for each of them and the formula in Equation (1) is applied. Also, a Levenshtein method function was implemented to manage slight misspelling in the query string.

Whilst the mathematical method to calculate the ontological similarities for the attribute Task is the same as before, the sets of elements to be compared are obtained in a different way. The relation function uses model is defined as an inference resulting of the property chain is predictive maintenance function of and is a carrier of to link instances of functions with instances of models (ontology class Predictive maintenance model). This means that the database will be queried automatically for information on the types of models that were used for each type of task concerning predictive maintenance. That allows estimating a semantic similarity between the different subclasses of functions.

The types considered in the ontology are: Fault detection, Fault feature extraction, Fault identification, Future state forecast, Health assessment, Health

modelling, and Remaining useful life estimation. The algorithm will query for each of the mentioned subclasses all the instances of models that are linked to their individuals through the inferred relation function uses the model. Each of the instances of models belongs to one of the several subclasses of the Predictive maintenance model that were defined in the ontology. The purpose is to list all the model types that have instances linked to any instances of each of the function types.

This is how sets of model types related to functions are compared using the method of Equation (1) to get similarity values. An implementation of the HermiT reasoner in Java has been used to check the ontology consistency, infer the relations and extract the required information through Description Logics queries.

From a similarity point of view, using the variable Publication year, referring to the year when a case study was published, the more recent an article is, the more accurate and relevant is supposed to be. A simple Integer similarity function has been tested with a similarity of 1 for cases published 5 years ago or less and a constant slope descending to a similarity of 0 at 40 years.

Finally, the default myCBR string comparison function with Levenshtein method has been used for the String attribute Case study. To obtain the global similarity value of a case from the similarities of the variables, myCBR allows using a simple weighted sum or a euclidean average. The weights may be adjusted, but for this study, they have been set to 1 for all the variables.

## Procedure to link ontologies and myCBR

The default method for importing databases into myCBR is via .csv files. As one of the main goals of this project was to create a direct link between ontologies and myCBR and use ontologies as database holders, SPARQL queries were used to extract the information as organized tabular data and load it automatically into a myCBR project file. Using the Jena API tool, single string queries with multiple statements were formulated to obtain a query results table with entities names or Data Properties content in which the rows correspond to cases and the columns to the variables defining those cases. This table is then stored inside a myCBR project file. The procedure may require dividing the query pieces to be executed sequentially when the volume of data is too large, so in that case, the partial results would be simply merged in one data table. The developed application allows loading a case base ready to be used by myCBR directly from an ontology .owl file following data translation rules specified in SPARQL language.

## RESULTS AND DISCUSSION

Keeping in mind the objective to propose an integration procedure between myCBR and ontologies,

different kinds of queries were tested in Java for OWL ontologies. SPARQL queries seem to be best placed for such integration, having as major advantages to having a fast execution without the using of a reasoner and that the outputs obtained are immediately organized in tabular data. This makes it easy to introduce the data in the myCBR project files.

For the information extraction for semantic similarity values definition, SQWRL queries were tested, but the obtained performance was low in terms of calculation speed and memory consumption. For the reasoner implementation tested for SQWRL queries, it was found that again a slow process resulted, potentially due to the complexity of the case base. In the end, in this study, Description Logics queries were used, only requiring to run the reasoner once for the execution of series of queries.

A feature-based similarity method has been tested in two of the variables describing the study case: Input type and Task. For the case retrieval variable Input type, the feature-based method seemed to be suitable criteria to compare sets of elements, suggested in (Qin et al. 2018). The in this way obtained results have been shown to be relevant and useful, demonstrating that the integration procedure is practical for defining accurate similarity values automatically. As to the similarity values between pairs of predictive maintenance tasks or functions, the corresponding similarity values matrix is shown in Table 2, of which the letters should be read considering:

A) Fault detection

B) Fault feature extraction

C) Fault identification

D) One step future state forecast

E) Multiple steps future state forecast

F) Health assessment

G) Health modelling

H) Remaining useful life estimation

<div align="center">

Table 2: Similarity values matrix for predictive maintenance functions.

</div>

<table border="1"><tr><td></td><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td><td>F</td><td>G</td><td>H</td></tr><tr><td>A</td><td>1</td><td>0.033</td><td>0.225</td><td>0.02</td><td>0.03</td><td>0.093</td><td>0.079</td><td>0.063</td></tr><tr><td>B</td><td>0.033</td><td>1</td><td>0.018</td><td>0</td><td>0</td><td>0.02</td><td>0.033</td><td>0.023</td></tr><tr><td>C</td><td>0.225</td><td>0.018</td><td>1</td><td>0</td><td>0</td><td>0.082</td><td>0.07</td><td>0.073</td></tr><tr><td>D</td><td>0.02</td><td>0</td><td>0</td><td>1</td><td>0.061</td><td>0.025</td><td>0</td><td>0.034</td></tr><tr><td>E</td><td>0.03</td><td>0</td><td>0</td><td>0.061</td><td>1</td><td>0.037</td><td>0.015</td><td>0.03</td></tr><tr><td>F</td><td>0.093</td><td>0.02</td><td>0.082</td><td>0.025</td><td>0.037</td><td>1</td><td>0.13</td><td>0.076</td></tr><tr><td>G</td><td>0.079</td><td>0.033</td><td>0.07</td><td>0</td><td>0.015</td><td>0.13</td><td>1</td><td>0.078</td></tr><tr><td>H</td><td>0.063</td><td>0.023</td><td>0.073</td><td>0.034</td><td>0.03</td><td>0.076</td><td>0.078</td><td>1</td></tr></table>

As can be seen, the similarity values for non-identical concepts are overall very low meaning that the instances in OMSSA seldom show a model that has been used

for two different tasks. Note the existence of one pair (Fault detection-Fault identification) that is much higher (over 10% similarity) in comparison to the rest; this is expected as classification models can be used for fault detection and also for fault identification purposes. Another interesting result concerns the pair One step future step forecast-Multiple steps future state forecast, basically the latter being an extension of the former, where the similarity could be expected to be close to 1. Both concepts are subclasses of the same predictive maintenance function in the ontology Future state forecast. Hence, from a global point of view, the analysis of the results suggest that there is possibly some aspect about the data or the similarity definition that makes it difficult to obtain really meaningful values. A first explanation hypothesis concerns the high degree of specialization of predictive maintenance models in the ontology. The class Predictive maintenance models have been automatically filled up with as many subclasses as specific types of models were reported in the literature and therewith declared in the database. Grouping all those types of models into less specific types could have changed the outcome. Another option would be to use a bigger case base, which in itself goes against the generally assumed guidelines for Case-Based Reasoning to work with relatively small case bases. This needs to be investigated in the next steps of the study.

So, the results suggest that some modifications could be needed, specifically in what concerns the similarity between the types of predictive maintenance models considered. However, the value of what has been obtained is not limited to the results in themselves, but also the fact that the integration procedure for ontologies and CBR has been validated so as to be exploited and improved to achieve a superior level of performance for the decision support system.

## CONCLUSION AND FUTURE WORK

This paper presents an approach to integrate ontologies and Case-Based Reasoning for a practical application case base for the development of predictive maintenance systems. The automatic transmission of the data in tabular format to ontologies has shown satisfactory results. The implementation of an ontology reasoner and some semantic feature-based similarity methods using Description Logics was possible thanks to the OWL API. It helped to improve the performances and accuracy of the system for this application and others to be tested in the future. The integration of myCBR and .owl ontologies through SPARQL queries using the Jena API is functional and reusable for other applications

This study has especially focused on the retrieval of cases, but the use of ontological knowledge could also be powerful to improve the rest of CBR functions as well. There may be good potential for future work to consider the complete CBR cycle and to automatize all CBR tasks (as suggested in (Mantaras et al. 2005)).

In addition, the study to improve ontological similarity is interesting; more complex and accurate semantic similarity functions could be implemented. In particular, exploiting the ontological reasoner inference could help to make deeper use of the knowledge in the ontology. Another potential improvement may come from taxonomic similarity functions that take better advantage of the hierarchical structure of an ontology. Additional validation work should aim for testing the validity of the recommendations given by the system within the application domain at hand (the design of predictive maintenance system) and to extend with developments on other application domains.

## REFERENCES

Aamodt A. and Plaza E., 1994. Case-Based Reasoning: Foundational Issues, Methodological Variations, and System Approaches. AI Communications IOS Press, Vol. 7: 1, pp. 39-59.

Amailef K. and Lu J., 2013. Ontology-supported case-based reasoning approach for intelligent m-Government emergency response services. Decision Support Systems, 55, 79-97. ISSN 01679236. doi:10.1016/j.dss.2012.12.034.

Avdeenko T.V. and Makarova E.S., 2018. Knowledge Representation Model Based on Case-Based Reasoning and the Domain Ontology: Application to the IT Consultation. IFAC-PapersOnLine, 51, no. 11, 1218-1223. ISSN 2405-8963. doi:https://doi.org/10.1016/j.ifacol.2018.08.424. URL https://www.sciencedirect.com/science/article/pii/S2405896318315519. 16th IFAC Symposium on Information Control Problems in Manufacturing INCOM 2018.

Bach K.; Sauer C.; Althoff K.D.; and Roth-Berghofer T., 2014. Knowledge Modeling with the Open Source Tool myCBR. vol. 1289.

Bai Y.; Yang J.; and Qiu Y., 2008. OntoCBR: Ontology-based CBR in context-aware applications. ISBN 978-0-7695-3134-2, 164-169. doi:10.1109/MUE.2008.56.

Glimm B.; Horrocks I.; Motik B.; Stoilos G.; and Wang Z., 2014. Hermit: An Owl 2 Reasoner. Journal of Automated Reasoning, 53. doi:10.1007/s10817-014-9305-1.

Gruber T., 2009. Ontology, Springer US, Boston, MA. ISBN 978-0-387-39940-9, 1963-1965. doi:10.1007/ 978-0-387-39940-9_1318.

Gruber T.R., 1993. A translation approach to portable ontology specifications. Knowledge Acquisition, 5, no. 2, 199220. ISSN 10428143. doi:10.1006/knac.1993.1008.

Horridge M. and Bechhofer S., 2011. The owl api: A java api for owl ontologies. Semantic Web, 2, 11-21. doi:10. 3233/SW-2011-0025.

International Organization for Standardization, 2020. ISO/IEC FDIS 21838-2.2 Information technology Top-level ontologies (TLO) Part 2: Basic Formal Ontology (BFO). Available online. URL: https://www.iso.org/standard/74572.html.

Kolodner J., 1993. Case based reasoning. Morgan Kaufmann. ISBN 978-1558602373.

Kowalski M.; Klüpfel H.; Zelewski S.; and Bergenrodt D., 2013. Integration of Case-Based and Ontology-Based Reasoning for the Intelligent Reuse of Project-Related Knowledge. ISBN 978-3642328374, 289-299. doi:10.1007/978-3-642-32838-1_31.

Montero Jimenez J.J.; Vingerhoeds R.; and Grabot B., 2021. Enhancing predictive maintenance architecture process by using ontology-enabled Case-Based Reasoning. IEEE ISSE 2021.

Montero Jiménez J.J.; Sebastien S.; Vingerhoeds R.; Grabot B.; and Salaün M., 2020. Towards multi-model approaches to predictive maintenance: A systematic literature survey on diagnostics and prognostics. Journal of Manufacturing Systems, 56, 539-557. doi:10.1016/j.jmsy.2020.07.008.

Montero Jiménez J.J. and Vingerhoeds R., 2019. A System Engineering Approach to Predictive Maintenance Systems: from needs and desires to logical architecture. 1-8. doi: 10.1109/ISSE46696.2019.8984559.

Mántaras R.; Mcsherry D.; Bridge D.; Leake D.; Smyth B.; Craw S.; Faltings B.; Maher M.; Cox M.; Keane M.; Aamodt A.; and Watson I., 2005. Retrieval, reuse, revision and retention in case-based reasoning. Knowledge Eng Review, 20, 215-240. doi:10.1017/S0269888906000646.

Noy N.F. and McGuinness D.L., 2000. Ontology Development 101: A Guide to Creating Your First Ontology. Stanford University. Available online. URL: https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html Accessed June 2021.

OWL Working Group, 2012. OWL 2 Web Ontology Language. World Wide Web Consortium. Available online. URL: http://www.w3.org/TR/2012/REC-owl2-overview- 20121211/. Accessed March 2021.

Qin Y.; Lu W.; Qi Q.; Liu X.; Huang M.; Scott P.; and Jiang X., 2018. Towards an ontology-supported case-based reasoning approach for computer-aided tolerance specification. Knowledge-Based Systems, 141, 129-147. doi: 10.1016/j.knosys.2017.11.013.

Recio-Garía J. and Díaz-Agudo B., 2007. Ontology based CBR with jCOLIBRI. ISBN 978-1-84628-665-0, 149-162. doi:10.1007/978-1-84628-666-7_12.

Rudnicki R., 2019. An Overview of the Common Core Ontologies. CUBRC Inc, Buffalo, NY. Available online. URL: https://www.nist.gov/system/files/documents/2019/ 05/30/nist-ai-rfi-cubrc_inc_004.pdf.

Stanford University, 2016-2020. Protégé official website. Available online. URL: https://protege.stanford.edu/. Last visited June 2021.

Sánchez D.; Batet M.; Isern D.; and Valls A., 2012. Ontology-based semantic similarity: A new feature-based approach. Expert Systems with Applications, 39, no. 9, 7718-7728. ISSN 0957-4174. doi:https://doi.org/10.1016/j.eswa.2012.01.082.

Vingerhoeds R.A.; Janssens P.; Netten B.D.; and Aznar Fernández-Montesinos M., 1995. Enhancing off-line and on-line condition monitoring and fault diagnosis. Control Engineering Practice, 3, no.11, 1515-1528. ISSN 09670661. doi:10.1016/0967-0661(95)00162-N.

Yin Z.; Gao Y.; and Chen B., 2010. On development of supplementary Criminal analysis system based on CBR and Ontology. In 2010 International Conference on Computer Application and System Modeling (ICCASM 2010). vol. 14, V14-653-V14-655. doi:10.1109/ICCASM.2010. 5622227.

<div align="center">

# DSS code Guide

</div>

The content in this appendix corresponds to a user guide developed in ISAE-SUPAERO for the ontology enabled CBR engine for predictive maintenance component selection. Hugo Munoz Hernandez, Juan José Montero Jimenez, Rob Vingerhoeds. "Decision Support System Code Guide: Application to Predictive Maintenance Systems Design".

Intentionally left blank

Decision Support System Code Guide

Application to Predictive Maintenance Systems Design

Isae


> **Figure Description:**

Decorative icon



Institut Supérieur de l'Aéronautique et de l'Espace


> **Figure Description:**

Organization logo



Hugo MUNOZ HERNANDEZ

Juan Jose MONTERO JIMENEZ Rob VINGERHOEDS

July, 2021

## Contents

1 Installation and configuration 3

2 Basic usage 4

2.1 SPARQL queries 4

2.2 SQWRL queries 4

2.3 Load data in a table format (.csv) to an ontology file (.owl) using CSVtoOntologyExec 5

2.4 Load data from an ontology file (.owl) to a table format .csv file using OntologytoCSVExec 6

2.5 Preparing project case base and similarity values for myCBR with myCBRSetting 11

2.6 Query and retrieval using the GUI’s 12

2.6.1 GUI2 13

2.6.2 GUI3 14

2.7 The javadoc 15

2.8 Management of the data folder 16

3 Dependencies 17

## 1 Installation and configuration

For the installation procedure described here it is assumed that the user has installed a version of Eclipse that supports at least Java 8. Under the previous condition, the following steps may be followed to ensure the correct installation:

1. Download the .zip compressed folder of the project and save it in a selected local address in your computer.

2. Make right click over the compressed folder and use Extract Here, a decompressed folder with the same denomination has been created. Inside this folder, another folder named InternshipProject may be found.

3. Open Eclipse and browse to select InternshipProject as the working folder.

4. Once Eclipse has been initialized, go to File $ \rightarrow $ Import $ \rightarrow $ General $ \rightarrow $ Existing Projects into Workspace $ \rightarrow $ Browse and select the folder InternshipProject. The project will be built in the current workspace of Eclipse. The recognition of the folder as an Eclipse project is possible because of the file .project in the same folder.

5. In the case that some referenced libraries (.jar) seem to be missed, right click on InternshipProject at the workspace menu on the left $ \rightarrow $ Build Path $ \rightarrow $ Configure Build Path $ \rightarrow $ Libraries $ \rightarrow $ click on Classpath in the list below and now the option buttons on the right are available. Delete the paths that are indicated as erroneous and click Add JARs on the left to reintroduce the libraries that are missed. Browse to the external-libs folder and select the .jar files that have to be restored, then just click OK and Apply and Close. However, this problem is not likely to occur as the .classpath file store the path to all the dependencies of the project. Another possible solution to the problem if this existed would be to open the .classpath file with a plain text editor and change the paths that are referencing a local folder in another user computer to a general path starting at the folder external-libs of the project.

Now that the code is installed, some configurations are needed to star execution. There is a class named AppConfiguration in the User package which only contains public static attributes and a couple of methods to build variables. These attributes are read and used by other classes of the project, so they are stored together in the accessory class AppConfiguration to be accessed (not modified) by other pieces of code in the application. The very first change that the user must make in the mentioned class before executing the code is setting the data path attribute to the actual local path of the data folder of the project. From that point, the attributes on AppConfiguration should be updated to the file names that are wanted to be used inside the data folder (.csv, .owl,.prj, etc). See the javadoc of the project and the comments in the source code of AppConfiguration to get known about the meaning of the attributes.

## 2 Basic usage

The usage of this application will be performed simply by the execution of java classes from Eclipse (or any other IDE). It may also require the manipulation of files (ontology files, .csv, myCBR project files, etc) in the designated file folders. Unless a modification of the source code is needed for some reason, there are 5 executable classes in the project that concern to the user at this moment: CSVtoOntologyExec, myCBRSetting, SPARQL, GUI2, GUI3, OntologytoCSVExec and SWRLAPIexec.

## 2.1 SPARQL queries

A simple executable class has been added to the project to execute SPARQL queries on the working ontology in the same way that they are available in Protégé. The Jena tool (see Section 3 for more information) is used for that purpose. The SPARQL queries allows the user to obtain an accurate required information from the ontology. A general reference for the SPARQL language can be found at [11]. The user just needs to write the query in a correct syntactical form and execute the class file to get the results of the query on the console. These queries are very quick in their execution as they do not need to run a reasoner and check the ontology consistency. Even if the current implementation in the project is accessory, the SPARQL queries could be potentially used to extract information from an ontology for the definition of ontological similarity values.

## 2.2 SQWRL queries

The implementation of the SWRL API together with the reasoning engine drools allows to add SWRL rules to the working ontology execute SQWRL queries. See Section 3 for more information. The SQWRL language, which is based on the Semantic Web Rule Language (SWRL), opens the possibility to accurate queries with a relatively simple syntax. There is a paper [21] where the creator of this language give an introduction to the main rules and basic syntax of the queries. An inconvenient has been found for the use the SQWRL queries for the application case in the current research project: the reasoner must be run once for each query, so, when working with ontologies having a big number of individuals declared, this process can require an important amount of RAM memory in the computer and it can last long if many queries are wanted to be executed. That is why, at this moment, the direct querying through the OWL API is used for extracting information from an ontology, as it only requires to run the reasoner (HermiT) once before executing as many queries as desired. Indeed, the example class in the project SWRLAPIexec allowing to execute SQWRL queries may not work correctly due to the compatibility problems of SWRL API with the latest version of OWL API. See Section 3. However, as it is


## Continued from pages 201-262

potentially useful for the development of the project, the SWRL API implementation is still included in the project.

## 2.3 Load data in a table format (.csv) to an ontology file (.owl) using CSVtoOntologyExec

When executed, the class CSVtoOntologyExec will read the content in the specified data base in a .csv file and load the information into an ontology file (.owl). An important consideration is that the .owl files should be written in RDF/XML syntax (choose that option when using Save as in Protégé). In what concerns to myCBR retrieval, this class may only be executed when the case base information and similarity values contained in the .prj file should be changed or updated to perform CBR queries using new data. The path for working file folder should have been set in the AppConfiguration class, together with the corresponding files denominations. In this folder, it is recommended to locate a clean version of the ontology that is wanted to be used (without instances or individual or property assertions) and another copy (of course with a different name) where the data base will be stored. So, when updating the data base the procedure should be as follows:

- Delete the data base ontology file.

- Make a copy of the clean ontology file and change the name as desired . Of course, the same name should be specified in the AppConfiguration class (ont_file_name).

- Execute CSVtoOntologyExec, which will read the clean ontology file (specified in AppConfiguration as base_ont_file_name) and the data base of the .csv file (specified in AppConfiguration as csv) to merge the information in the ontology data base file.

The translation of the information stored in the table to ontological entities is stated with the appropriate using of the methods of the class CSVtoOntology in the package OntologyTools. See the javadoc of the project for details. By this way, the code is flexible to adapt to the ontological meaning of the content in the different columns and cells forming the table tabular data base.

In this particular case, the executable code in the CSVtoOntologyExec class is configured for the Predictive Maintenance data base and the OPMAD ontology. Nevertheless, the class could be modified if needed to suit to another different case or to adapt to a restructuring of the current data base and ontology.

## 2.4 Load data from an ontology file (.owl) to a table format .csv file using OntologytoCSVExec

The class OntologytoCSVExec is an executable class allowing to extract data from an ontology file and rewrite it in an organized table format into a .csv file. The class OntologytoTabular is used to get the data and organize it in a structured tabular List object. In the mentioned class, a Jena API implementation is used to be able to execute a series of SPARQL queries on the working ontology and get a tabular data as a result. The advantages of this type of queries for this application are their execution time (fast execution as they do not need reasoning) and the retrieval results obtained on the shape of organized tables. Now, one important issue should be underlined: the SPARQL queries have to be adapted to the particular ontology of the user, as well as the organization criteria for the data when stored as a .csv table. Even if it is possible to use one single query for the data extraction, it is recommended to divide the query in various of them when the size of the database is remarkable, as it would be much faster to execute. The list of queries is automatically built by a method in the AppConfiguration file. It is required to specify the static String parameter queryHead in the mentioned class to set the first part of the SPARQL queries, that will be common to all the queries in the list. This part of the query aims to define the variables that are going to be retrieved and to initialize the selection block. The closing of the query is also common to all the queries in the list, so it can be specified with the parameter queryEnd. The body commands of the queries, which will use the relations existing in the ontology to extract the data, are listed in the parameter queryBodyList in the AppConfiguration file. Then, the method queryList will build the strings with the full queries adding one head and one closing to each one of the body commands blocks. A reference to the SPARQL syntax can be found at [11]. The general procedure to determine the query structure is to choose the variables defining the cases, establish which entities in the ontology contain that information and look for properties or ontological relations that build links between the different pieces of data.

The output data of a SPARQL query is organized in columns, one for each requested variable. Cells in the table can store one single data value. If a variable value in one of the columns matches more than one value of other variable, then there will be one row in the query results table for each combination of values. That comes to say, using a simplified example, that having a table with only two columns in which each one of the n values of the first variable matches two values of the second variable, then the table will have 2n rows, where the values of the first variable variable will appear twice in the column. The same logic extends to several variables with multiple values, that would imply to add as many rows as necessary to include all the combinations of values. An example for the application case of Predictive Maintenance Decision-Support System is shown in Figure 1, where it is observed that there are as many rows concerning the reference index '1' as values of the field Input type existing for such case. Note that the indices are ordered using the ontological Protégé criteria instead of mathematical order.

<table border="1"><tr><td>Reference</td><td>Publication_Year</td><td>Task</td><td>Case_study</td><td>Case_study_type</td><td>Input_for_the_model</td><td>Input_type</td></tr><tr><td>“1”</td><td>2019</td><td>Health modelling</td><td>Simulated_jet-engines_data</td><td>Rotary_machines</td><td>Time_series</td><td>Baypass_ratio</td></tr><tr><td>“1”</td><td>2019</td><td>Health modelling</td><td>Simulated_jet-engines_data</td><td>Rotary_machines</td><td>Time_series</td><td>Temperature</td></tr><tr><td>“1”</td><td>2019</td><td>Health modelling</td><td>Simulated_jet-engines_data</td><td>Rotary_machines</td><td>Time_series</td><td>Fluid_Pressure</td></tr><tr><td>“1”</td><td>2019</td><td>Health modelling</td><td>Simulated_jet-engines_data</td><td>Rotary_machines</td><td>Time_series</td><td>Spinning_speed</td></tr><tr><td>“10”</td><td>2016</td><td>One_step_future_state_forecast</td><td>Proton_exchange_membrane_fuel_cell</td><td>Energy_cells_and_batteries</td><td>Time_series</td><td>Voltage</td></tr><tr><td>“100”</td><td>2013</td><td>Multiple_steps_future_state_forecast</td><td>Lithium-ion_battery</td><td>Energy_cells_and_batteries</td><td>Time_series</td><td>Impedance</td></tr><tr><td>“100”</td><td>2013</td><td>Multiple_steps_future_state_forecast</td><td>Lithium-ion_battery</td><td>Energy_cells_and_batteries</td><td>Time_series</td><td>Temperature</td></tr><tr><td>“100”</td><td>2013</td><td>Multiple_steps_future_state_forecast</td><td>Lithium-ion_battery</td><td>Energy_cells_and_batteries</td><td>Time_series</td><td>Voltage</td></tr><tr><td>“100”</td><td>2013</td><td>Multiple_steps_future_state_forecast</td><td>Lithium-ion_battery</td><td>Energy_cells_and_batteries</td><td>Time_series</td><td>Current</td></tr></table>

<div align="center">

Figure 1: Example of SPARQL query results table for the application Predictive Maintenance Decision-Support System.

</div>

Additionally, a complete SPARQL query for the previously mentioned application case is included in Figure 2 as example to be modified by the user. There is an important detail that must be clarified in what concerns to the variable designations in the SPARQL query: as the characters blank space, '-' and '/' are not allowed, they are substituted respectively by '-', double '-' and triple '-'. When rewriting data in a tabular shape using the class OntologytoTabular, the headers of the table containing the variables designations are automatically recovered following the inverse transformation rule.

To optimize the execution time of the queries, they can be divided. Individual queries can be executed to obtain partial data tables in which the reference indices column will be extracted together with one or more of the other columns. It is necessary that all the partial queries get the reference indices column as the first column of their results table, so as later all the partial tables can be merged in one. Hence, in most of the cases the columns can be extracted individually, but sometimes it could be required that some columns are extracted through the same query. When two or more columns that store multiple elements in their cells have an order dependency between them, they must be associated to the same query. The order dependency means that the elements listed in the cells of one of the columns are linked to another corresponding element among the ones listed in the cell of another columns. So, the elements in both columns must be listed in the same order to preserve the relation between the elements of data.

Once defined the queries, the results coming from their execution will be rewritten to tables where each row should match only one case, merging the rows coming from the SPARQL result to gather in the correspondent cells the set of values for those fields that are multiple-valued. A reference column is chosen (first column) with integer reference indices so as the content of the cells of all the rows with the same index is merged. The general criteria to do so is that no value is repeated in the multiple values cells. However, a set of variables names can be listed using the parameter Repetition_allowed for those columns in which repeated values in the same cell should be allowed. As blank spaces are forbidden in the SPARQL syntax, when the text values are recovered they are rewritten substituting ' ' characters by blank spaces, unless the user specifies no to do so via the parameter Not_Spaced. At the end, all the tables will be put together according to the reference indices column, so as the data coming from the list of queries is gathered into one single data table.

Then, here are the features that must be set up in order to define the data transference from the ontology to a .csv file:

- SPARQL queries list that will determine what information is requested to the ontology and how it is organized. To be set up in the AppConfiguration file.

- Parameter list Not_Spaced to be specified in the class AppConfiguration. In this list it must be included the designation tags of those variables or fields in the table where blank spaces are not desired or expected. For those columns of the table, the text value will be written as it is in origin in the query results, without replacing characters ' _ ' by blank spaces.

- Parameter list Repetition allowed to be specified in the class AppConfiguration. In this list the user must include, among those variables (columns) that could contain multiple elements in the same cell, in which of them it is allowed that elements are repeated more than once in the same cell.

For the example below, concerning the Predictive Maintenance Decision-Support System application, it is illustrated the structure of the SPARQL query (Figure 2), the results for a case with multiple values (Figure 3) and the final format in the .csv table. So, when the results are retrieved from the SPARQL query, more than one row may be obtained for each case to get all the values combinations of all the fields that are multiple-valued. In the Figure 3 it is observed how the case with reference index '8' has multiple values for the fields Input type and Models, while the description tags of the field Model Type are matched to particular values of Models. In this example, a single query has been used in order to clarify the explanation, but in the real application case the query was divided in parts. Indeed, a query was used for each of the columns in the table except the pair Model Type and Models and the pair Performance indicator and Performance, which were respectively included in the same query. The reason for that is that they must keep an order relation for the elements that are listed in the cells. The Model Type values must be stored in the same order that the corresponding elements in the column Models that they are describing. Same condition is needed for the elements listed in Performance indicator and the their value in the column Performance. The column Model Type is declared in the list Repetition allowed, so as more than one of the Models concerning one case could be described with the same type if they belong to the same family of models.


> **Figure Description:**

The image displays a SPARQL query script used for querying an ontology. The script begins with a series of namespace prefixes: PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>, PREFIX owl: <http://www.w3.org/2002/07/owl#>, PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>, PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>, PREFIX def: <http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD#>, PREFIX obo: <http://purl.obolibrary.org/obo/>, and PREFIX cco: <http://www.ontologyrepository.com/CommonCoreOntologies/>.

The SELECT clause specifies the variables to be retrieved: ?Reference, ?Publication_Year, ?Task, ?Case_study, ?Case_study_type, ?Input_for_the_model, ?Input_type, ?Model_Type, ?Models, ?Online_Off__line, ?Performance_indicator, ?Performance, ?Complementary_notes, ?Study_title, and ?Publication_identifier.

The WHERE clause contains a series of triple patterns defining the relationships between these variables. These include: ?a rdf:type def:Predictive_maintenance_system_module; ?a obo:RO_0010002 ?d; ?b obo:RO_0010002 ?d; ?b rdf:type def:Predictive_Maintenance_Article; ?Models rdfs:subClassOf def:Predictive_maintenance_model; ?d rdf:type ?Models; ?e rdf:type def:Predictive_maintenance_case; ?e cco:designates ?a; ?def:has_text_value ?Reference; ?b def:has_publication_year ?Publication_Year; ?Task rdfs:subClassOf def:Predictive_maintenance_module_function; ?h rdf:type ?Task; ?a def:has_predictive_maintenance_function ?h; ?a obo:BFO_0000051 ?j; ?j rdf:type ?Case_study; ?Case_study rdfs:subClassOf def:Maintainable_item; ?Case_study_type rdf:type def:item_type; ?b obo:RO_0010002 ?Case_study_type; ?Input_for_the_model rdfs:subClassOf def:maintainable_item_record; ?n rdf:type ?Input_for_the_model; ?a obo:BFO_0000051 ?n; ?Input_type rdf:type def:Data_variable; ?n obo:RO_0010002 ?Input_type; ?Model_Type rdf:type def:Model_type; ?Model_Type cco:describes ?d; ?a def:has_synchronization ?Online_Off__line; ?Online_Off__line rdf:type def:Module_synchronization; ?b def:has_title ?r; ?r def:has_text_value ?Study_title; ?b def:has_identifier ?s; ?s def:has_text_value ?Publication_identifier; ?Performance_indicator rdfs:subClassOf def:Performance_value; ?t rdf:type ?Performance_indicator; ?t cco:describes ?a; ?t def:has_text_value ?Performance; ?u rdf:type def:Complementary_notes; ?u cco:describes ?b; and ?u def:has_text_value ?Complementary_notes. The query concludes with a closing brace.



<div align="center">

}ORDER BY (?Reference)

</div>

<div align="center">

Figure 2: Example of complete SPARQL for the application Predictive Maintenance Decision-Support System.

</div>


> **Figure Description:**

This image displays two parts of a table, labeled (a) and (b), which detail research data regarding remaining useful life estimation. The top section (a) contains the following columns: Reference, Publication_Year, Task, Case_study, Case_study_category (labeled "Case_stud..."), Input_for_the_model (labeled "Input_for_the_..."), Input_type, Model_Type, and Models. Every row in this section has "8" as the Reference, "2019" as the Publication_Year, "Remaining useful life estimation" as the Task, "Railway_track_geometry" as the Case_study, "Structures" as the Case_study_category, and "Time_series" as the Input_for_the_model. The Input_type values are "Plastic_strains", "Mechanical_Pressure", "Life_cycles", "Mechanical_stresses", and "Elastic_strains", repeating in that order for different model groups. The Model_Type values are "Data-driven" (for Bayes_model), "Physics-based" (for Particle_Filter), and "Physics-based" (for Physics-based_model_for_track_settlement).

The bottom section (b) contains the following columns: Online__Off__line, Performance_indicator, Performance, Complementary_notes, Study_title, and Publication_identifier. Every row in this section has "Online" as the Online__Off__line value, "Mean_absolute_percentage_error" as the Performance_indicator, and "(<5%)" as the Performance. The Complementary_notes column contains "No_info_about_operationa" for every row. The Study_title for every row is "A_knowledge-based_prognostics_framework_." and the Publication_identifier for every row is "doi.org/10.1016/j.ress.2018.07.004". There are 13 rows of data in each section, corresponding to the same set of entries across both parts of the table.



<div align="center">

(b)

</div>

<div align="center">

Figure 3: SPARQL query results table for one particular case for the application Predictive Maintenance Decision-Support System.

</div>


> **Figure Description:**

This image contains two tables, labeled as (a), which summarize research studies. The first table has columns for Reference, Publication Year, Task, Case study, Case study type, Input for the model, Input type, Data Pre-proc, Model Approach, Model Type, and Models. The rows are as follows: 1, 2019, Health modeling, Simulated jet-engines data, Rotary machine, Time series, Temperature, yes, Single model, Data-driven, Logistic regression. 2, 2019, Health assessment, Simulated jet-engines data, Rotary machine, Time series, Temperature, yes, Single model, Data-driven, Logistic regression. 3, 2019, Remaining useful life, Simulated jet-engines data, Rotary machine, Time series, Health index, yes, Single model, Data-driven, OS-ELM (Online-sequential ELM). 4, 2019, Remaining useful life, Simulated jet-engines data, Rotary machine, Time series, Health index, yes, Multi model, Data-driven, KFOS-ELM (Kalman filter-based). 5, 2019, Remaining useful life, Simulated jet-engines data, Rotary machine, Time series, Health index, yes, Multi model, Data-driven, EOS-ELM (Ensemble of OS-ELM). 6, 2019, Remaining useful life, Simulated jet-engines data, Rotary machine, Time series, Health index, yes, Multi model, Data-driven, AEKFOS-ELM (adaptive-weighted). 7, 2019, Health assessment, Railway track geometry, Structures, Time series, Mechanical stress, No, Multi model, Physics-based, Data-driven, Physics-based model for track. 8, 2019, Remaining useful life, Railway track geometry, Structures, Time series, Mechanical stress, No, Multi model, Physics-based, Data-driven, Physics-based model for track.

The second table, which continues the data for the same references, has columns for Online/Off-line, Performance indicator, Performance, Complementary notes, Study title, and Publication identifier. The rows are as follows: Off-line, Mean absolute percentage error, (<0.05), 1 operational mode, 100, Aircraft engine, doi.org/10.1016/j.ast.2018.09.044. Off-line, Mean absolute percentage error, (<0.05), 1 operational mode, 100, Aircraft engine, doi.org/10.1016/j.ast.2018.09.044. Off-line, Score function (the smaller the better), Mean accuracy, Error range, (58.96), (93.26), ([21,33]), 1 operational mode, 100, Aircraft engine, doi.org/10.1016/j.ast.2018.09.044. Off-line, Score function (the smaller the better), Mean accuracy, Error range, (35.78), (95.78), ([15,22]), 1 operational mode, 100, Aircraft engine, doi.org/10.1016/j.ast.2018.09.044. Off-line, Score function (the smaller the better), Mean accuracy, Error range, (34.56), (96.54), ([13,19]), 1 operational mode, 100, Aircraft engine, doi.org/10.1016/j.ast.2018.09.044. Off-line, Score function (the smaller the better), Mean accuracy, Error range, (33.13), (96.76), ([11,18]), 1 operational mode, 100, Aircraft engine, doi.org/10.1016/j.ast.2018.09.044. Off-line, N/A, N/A, No info about operation, A knowledge-based, doi.org/10.1016/j.ress.2018.07.004. Online, Mean absolute percentage error, (<5%), No info about operation, A knowledge-based, doi.org/10.1016/j.ress.2018.07.004.



<div align="center">

(b)

</div>

<div align="center">

Figure 4: Final results table as it is loaded in the .csv file for the application Predictive Maintenance Decision-Support System.

</div>

## 2.5 Preparing project case base and similarity values for myCBR with myCBRSetting

The class myCBRSetting may be executed when the data base in the .csv (file name specified as csv in the class AppConfiguration) file or the ontology .owl file have been changed (normally their modifications are coordinated). In order to perform myCBR queries on a new case base, or a case base that has been updated, the information must be written in the .prj (file name specified as projectName in the class AppConfiguration) file, which is the one that contains the project data for myCBR. Moreover, the class will run an OWL reasoner (more precisely the HermiT reasoner, see Section 3) on the ontology that will check its consistency and infer relations for the knowledge contained in the ontology. In consequence, the execution of the class can take a bit of minutes, depending on the ontology size. The main reason to use the reasoner is to be able to perform queries on the ontology to extract information that can be used to calculate ontological similarity values. Moreover, the HermiT reasoner allows to make queries about relations that are not initially explicit in the ontology but inferred during the reasoning process. Obviously, if the ontology is not consistent the execution will stop, so to work with an ontological data base it must be consistent. Furthermore, even if the data base can be loaded to the project file either from a .csv data file or from an .owl ontology, the ontology file is always necessary to obtain the similarity values. The class myCBRSetting may be modified to adapt the code to a new application other than the Predictive Maintenance Decision-Support System. This is because the ontology relations and the method for semantic similarity calculation depend obviously on the application.

When executing, at first, the class uses an instance of CBREngine to load the current .prj file, delete all the existing instances in the case base and introduce the new ones, with their corresponding attribute values, by importing the chosen .csv file or the .owl ontology file. If the .owl database is chosen, the procedure to extract the data is exactly the same as the one followed when executing OntologytoCSVExec, see the Subsection 2.4 for more details. The class OntologytoTabular will get the data from the ontology following the structure of the SPARQL queries list. Then, once the data has been tabulated, it is loaded directly into the myCBR project file instead of creating a .csv file. So, using the direct importing from the .owl file has the same result that creating the .csv file form the ontology and loading it with the default myCBR importer.

After that, the similarity functions are established with the appropriate values. In particular for the Predictive Maintenance Decision-Support System application, for the field Task associated to each one of the cases, the similarity values are calculated using an ontological method. The querying of the ontology uses the classes DLQueryEngineIRI and DLQueryParserIRI of the package OnotlogyTools. See the javadoc of the project for more details.

<table border="1"><tr><td>Case variable</td><td>Variable type(myCBR)</td><td>Values</td></tr><tr><td>Task</td><td>Symbol</td><td>Fault feature extraction,Fault detection,Fault identification,Health modelling,Health assessment,Remaining useful life estimation,One step future state forecast,Multiple steps future state forecast.</td></tr><tr><td>Case study type</td><td>Symbol</td><td>Rotary machines,Reciprocating machines,Electrical components,Structures,Energy cells and batteries,Production lines,Others.</td></tr><tr><td>Case study</td><td>String</td><td>The myCBR Levenshtein function is used.Similarity is calculated with the quotientnumber of characters reference String-Levenshtein distancenumber of characters reference String</td></tr><tr><td>Input type</td><td>Symbol</td><td>A list of variables must be provided separated by’,’and where all the words should begin with capital letters as it is established in the case base.An additional Levenshtein method in Java allows to support misspelling up to 3 erroneous characters.</td></tr><tr><td>Online/Off-line</td><td>Symbol</td><td>Online,Off-line,Both,Unknown synchronization.</td></tr><tr><td>Input for the model</td><td>Symbol</td><td>Signals,Structured text-based,Text based maintenance/operations logs,Time series.</td></tr><tr><td>Publication Year</td><td>Integer</td><td>This field is not provided by the user,the application will used the current date automatically.The most recent cases in the case base will be prioritized over the older ones.</td></tr></table>

<div align="center">

Table 1: Case variables for querying and retrieval

</div>

## 2.6 Query and retrieval using the GUI's

Once executed CSVtoOntologyExec to load the data base into the ontology and myCBRSetting to configure the .prj file for myCBR, only the executable GUI's are required to query and retrieve until the case base is wanted to be modified. The tool myCBR uses the case base, the attributes and the similarity functions specified in the .prj file to search the most suitable case for the given query. To visualize or to modify manually the project file the myCBR Workbench application may be used.

When executing any one of the GUI's, the class Recommender is used. Most of the similarity functions are defined during the execution of the class myCBRSetting, but there is one particular field in the Predictive Maintenance Decision-Support System which similarity values are defined by comparing the current query to all the cases in the data base individually, and that is Input type. An analog method is used, which is analog to the one applied to establish the similarity values between the different Predictive Maintenance functions (field Task).

Two executable Graphical User Interfaces are provided for querying: GUI2 and GUI3.

## 2.6.1 GUI2

The GUI2 allows the user to perform one query at a time by specifying the following parameters:

- Values of the case fields for the retrieval. Some of them must be typed (Case Study and Input type) and for the rest of the fields the values are selected form the ones available in a drop down menu.

- Value of the weights assigned to each field.

- Type of amalgamation function that is used to get the global similarity value of each case.

- Number of cases to be retrieved. The resulting list of cases (ordered from higher to lower similarity value) will be shown in the screen after submitting the query.


> **Figure Description:**

Software interface screenshot.

The image displays a graphical user interface titled "Predictive maintenance with CBR method GUI 2." The interface is organized into three main sections: Input variables, Additional Inputs, and a User dialog box, with a "SUBMIT QUERY" button at the bottom. The Input variables section contains a table with two columns: the left column lists labels, and the right column contains dropdown menus and text fields, each paired with a "Variable weights" column on the far right containing the value "1.0" for every row. The rows are as follows: "Task" is set to "Feature extraction," "Case study type" is set to "Rotary machines," "Case study" is set to "Simulated jet-engines data," "Input type" is set to "Temperature, Fluid Pressure, Spinning speed, Baypass," "Online/Off-line" is set to "Online," and "Input for the model" is set to "Signals."

Below this, the "Additional Inputs" section contains two fields: "Number of cases to retrieve," which is set to "3," and "Amalgamation function to use," which is set to "euclidean." The "User dialog" box at the bottom provides instructions: "Welcome to the myCBR Graphical User Interface! * Input Variables : variables used in the query to retrieve and calculate similarites. - Task, Publication year, Case Study Type, Online/Off-line, Input for the model, Input type : Drop down list - Case Study : Free text * Additional inputs : inputs to complement the retrieval method. - Number of cases to retrieve : Integer number. - Amalgamation function to use : Drop down list." The entire interface concludes with a large "SUBMIT QUERY" button centered at the bottom.



<div align="center">

Figure 5: Window of the GUI2

</div>

If one of the fields is left blank, then its weight in the global similarity value is automatically set to 0. The value of the field Case study is expected to be equal to one already existing in the data base, otherwise the similarity value will be 0 for all the cases.

The field Input type contains a list of variables (most of them physical variables) that are considered in the Predictive Maintenance model of each case. This list must be typed with the terms separated by ', ' and all the words starting by capital letters, as they appear in the case base. Nevertheless, both fields can manage with possible misspelling errors using the Levenshtein distance method. In particular, the Case study field is defined as string type in myCBR, and it uses the default Levenshtein comparison function. But, for the Input type field, the Levenshtein method is not available in myCBR as it is declared as symbolic value. So, an additional method (class LevenshteinDistanceDP) to allow up to a distance of three erroneous characters in the spelling is implemented in the similarity function definition (Recommender). See the javadoc for more details.

## 2.6.2 GUI3

Using this GUI, the user is able to execute a list of consecutive queries provided in an input file in .csv format and to save their results in separate files (one for each query in the list). It is necessary to prepare an input file with the appropriate structure (see Figure 6). An example of input file is also provided in the actual project folder of the application. For the fields that are stated as symbolic in myCBR and for the string variable Case study, the user must type in the input file a value which is included among the possible values for each field (see Table 1), otherwise the similarity will be just 0. Symbolic fields, with the exception of Input type, do not support misspelling. The field Input type contains a list of variables separated by ',' where the words should begin by capital letters (as they are in the data base). As soon as one of the variables of the list exist in one of the cases in the data base the similarity value will not be 0 for that case.


> **Figure Description:**

This table presents data across several columns, with each column header followed by a weight column labeled w1 through w6. The headers are Task, Case study type, Case study, Online/Offline, Input for the model, Input type, Number of ca, and Amalgamation function. The weight columns (w1, w2, w3, w4, w5, w6) all contain the value 1 for every row.

The first row of data contains the following values: Task is "Fault detectio", Case study type is "Rotary machi", Case study is "Simulated jet-", Online/Offline is "Online", Input for the model is "Time series", Input type is "Temperature", Number of ca is "20", and Amalgamation function is "euclidean".

The second row of data contains the following values: Task is "Feature extra", Case study type is "Rotary machi", Case study is "Simulated jet-", Online/Offline is "Offline", Input for the model is "Time series", Input type is "Temperature", Number of ca is "1", and Amalgamation function is "euclidean".

The third row of data contains the following values: Task is "Fault detectio", Case study type is "Rotary machi", Case study is "Simulated jet-", Online/Offline is "Offline", Input for the model is "Time series", Input type is "Temperature", Number of ca is "5", and Amalgamation function is "euclidean".



<div align="center">

Figure 6: Example .csv input file for the GUI3

</div>

After having prepared the input file, the GUI window will just require to the user to provide the name of the input file and also that of the result files, as shown in Figure 7. For each one of the queries in the list, a result file will be generated with the denomination specified by the user and an index added to the name indicating its position in the list of queries. An example result file is shown in the Figure 8. The content of the result files is another list containing the information about the cases that have been retrieved (as many as demanded by each query).


> **Figure Description:**

Software user interface screenshot.



<div align="center">

Figure 7: Window of the GUI3

</div>


> **Figure Description:**

The image is a table presenting a comparative analysis of various research studies, organized by columns labeled Reference, Sim, Task, Case study type, Case study, Online/Offline, Input for the model, Model Approach, Models, Input type, Number of inputs, Performance, Performance, Complementary, and Publication identifier. The rows contain the following data: 209, 0,919, Fault detection, Rotary machinery, Simulated jet-engine, Online, Time series, Single model, Voting method, Spinning speed, 3, N/A, N/A, No info about, 10.12700/APH.15.1.2018.2.10; 191, 0,901, Fault detection, Rotary machinery, Simulated jet-engine, Online, Time series, Multi model, Bayes model, Measurement, 2, Robustness, N/A, 10 operational, 10.1109/TCST.2011.2177981; 166, 0,845, Fault detection, Rotary machinery, Wind turbines, Off-line, Time series, Single model, Gaussian process, Wind power, 22, Accuracy, <0.945, one case of study, 10.1016/j.renene.2018.10.088; 167, 0,845, Fault detection, Rotary machinery, Wind turbines, Off-line, Time series, Single model, Gaussian process, Wind power, 22, N/A, N/A, one case of study, 10.1016/j.renene.2018.10.088; 210, 0,837, Fault identification, Rotary machinery, Simulated jet-engine, Online, Time series, Single model, Expert system, Results of a fault, 1, N/A, N/A, No info about, 10.12700/APH.15.1.2018.2.10; 211, 0,818, Fault detection, Rotary machinery, Simulated jet-engine, Off-line, Time series, Multi model, Hybrid Kalman, Compressor Temp, 8, Visual indicator, N/A, 6 operational modes, 10.1109/ACC.2013.6580567; 192, 0,818, Fault identification, Rotary machinery, Simulated jet-engine, Online, Time series, Multi model, Bayes model, Measurement, 2, Robustness, N/A, 10 operational, 10.1109/TCST.2011.2177981; 195, 0,786, Fault detection, Rotary machinery, Rotor shafts, Online, Time series, Multi model, Gauss-Markov, Imbalance source, 2, N/A, N/A, No info about, 10.1117/12.475502; 72, 0,772, Fault detection, Structures, Tank reactor, Online, Time series, Multi model, Updated Rule, Temperature, 3, Probability, From graphics, 2 operational, 10.1016/j.ejor.2010.03.032; 98, 0,760, Fault detection, Rotary machinery, Steam Turbine, Online, Signals, Single model, Extreme Gradient, Condenser vacuum, 7, N/A, N/A, No info about, 10.1016/j.microrel.2013.03.010; 59, 0,758, Remaining useful life, Rotary machinery, Aircraft bearing, Online, Time series, Single model, Relevance vector, Health index, 1, Score function, 19,66, No info about, 10.1016/j.ress.2017.12.016; 58, 0,758, Remaining useful life, Rotary machinery, Aircraft bearing, Online, Time series, Single model, Ensemble learning, Health index, 1, Score function, 7,8, No info about, 10.1016/j.ress.2017.12.016; 60, 0,758, Remaining useful life, Rotary machinery, Aircraft bearing, Online, Time series, Single model, Particle filter, Health index, 1, Score function, 301,8, No info about, 10.1016/j.ress.2017.12.016; 204, 0,756, Remaining useful life, Rotary machinery, Wind turbines, Online, Time series, Single model, Geolocation point, Distance, Deg, 2, Prognostic horizon, (65),(0.7), No info about, 10.1016/j.renene.2017.05.020; 2, 0,755, Health assessment, Rotary machinery, Simulated jet-engine, Off-line, Time series, Single model, Logistic regression, Temperature, 5, Mean absolute, <0.05, 1 operational, 10.1016/j.ast.2018.09.044; 1, 0,755, Health modelling, Rotary machinery, Simulated jet-engine, Off-line, Time series, Single model, Logistic regression, Temperature, 5, Mean absolute, <0.05, 1 operational, 10.1016/j.ast.2018.09.044; 51, 0,754, Remaining useful life, Rotary machinery, Simulated jet-engine, Off-line, Time series, Single model, LSTM (Long-Short), Temperature, 14, Root mean square, 6,9±4,7, 6 CMPASS dataset, 10.1016/j.ast.2019.105423; 53, 0,754, Remaining useful life, Rotary machinery, Simulated jet-engine, Off-line, Time series, Single model, Recurrent Neural, Temperature, 14, Root mean square, 10,2±5,8, 6 CMPASS dataset, 10.1016/j.ast.2019.105423; 52, 0,754, Remaining useful life, Rotary machinery, Simulated jet-engine, Off-line, Time series, Single model, LSTM (Long-Short), Temperature, 14, Root mean square, 8,2±5,7, 6 CMPASS dataset, 10.1016/j.ast.2019.105423; 54, 0,754, Remaining useful life, Rotary machinery, Simulated jet-engine, Off-line, Time series, Single model, Gated recurrent, Temperature, 14, Root mean square, 10,0±6,0, 6 CMPASS dataset, 10.1016/j.ast.2019.105423.



<div align="center">

Figure 8: Example .csv result file for the GUI3

</div>

## 2.7 The javadoc

A complete javadoc has been generated for this project. It is available in the folder javadoc of the project. The easiest way to access to the documentation is opening the index file in the mentioned folder. It is an HTML file in the standard format for javadoc resources available in the web, and it may be opened with a web browser. The documentation contains a detailed descriptions of all the classes and methods organized in linked pages, allowing to navigate through the structure of the code. To update the documentation using Eclipse, go to Project $ \rightarrow $ Generate Javadoc. When the window is open, the user must select the folder where the javadoc will be saved. It is recommended to use the folder javadoc, after having deleted the previous content to avoid problems. Of course, the generation of javadoc depends on the javadoc format comments that have been added to the code. See [12] for more details on the javadoc comments format.

## 2.8 Management of the data folder

The purpose of the data folder in the project is to store all the files that are needed for the execution tasks of the application. It is very important to remember that the denomination of the files that are wanted to be used inside this folder must be in coordination with the names introduced in AppConfiguration, so as the code is able to find such files. Some of the main types of files and their function are listed:

- Files .owl : the ontology files. One important consideration is that these files must be written in the RDF/XML syntax (choose that option when using Save as in Protégé). They can be opened with Protégé to visualize and edit the ontology or with a simple plain text editor, which allows to modify manually the statements. Two files may be used, one file should contain a clean ontology (without the declaration of the individuals in the data base) and the other one with all the data base loaded (and a different name, of course). An ontological data base could be directly used for the myCBR project build-up by selecting the appropriate option (user text input) when executing the class myCBRSetting. In any case, an ontology structure is required, either formed from a .csv table or directly provided by the user.

- Files .csv : files with a table format. A data base in .csv format may be needed to be loaded in the working ontology. The input and result files used by the GUI3 are also .csv format. These files can be opened with Excel. Using a plane text editor to open .csv files may be recommended to ensure that no weird characters have been introduced by Excel at the beginning of the data (an unusual bug in Excel that may alter the name of the first column of data).

- Files .prj : the project files of myCBR, where all the information concerning the query and retrieval must be stored. This type of file can be opened with the myCBR Workbench application.

- Files .ttl : these files contain the ontology dependencies (BFO, CCO ontologies, etc). They are necessary to read the ontologies when working with local imports, so as the ontology is independent of the online servers. They are available at the GitHub repository [22], and may be updated with newer versions from time to time. For the execution of the code, some mappers are set using OWL API to link the .ttl files with the URI that are used by the ontologies to invoke the corresponding dependencies. For the OPMAD ontology, the following files are required: ArtifactOntology.ttl, EventOntology.ttl, ExtendedRelationalOntology.ttl, GeospatialOntology.ttl, InformationEntityOntology.ttl, ro-import.ttl, TimeOntology.ttl.

- File catalog-v001.xml : this file stores the paths to allow Protégé to import the local ontology dependencies in .ttl format when opening an ontology file that needs those dependencies.

## 3 Dependencies

Here are listed the main APIs and libraries which are needed for the application, which are included in the external-libs folder of the project:

- OWL API : it is an API that allows to read, modify, manipulate and create .owl ontologies. The version currently used in the application is 5.1.9, but future updates could be possible. The API is implemented by including the necessary .jar files in the external-libs folder of the application. The last version of OWL API is available at the Maven repository [2] (artifact owlapi-distribution), but it has been directly obtained as .jar files from [1] with all dependencies. Previous versions are also available. A complete documentation can be accessed at [3] and there is an introduction tutorial written by the creators at [6]. The licenses concerning the API are the Apache License [4] and the GNU license [5].

- HermiT reasoner: it is a reasoner that works in Protégé, the most used software for ontology manipulation. There is and implementation for Java based on the OWL API. The version used is the latest one (1.4.5.519), and it can be found at the Maven repository [7] or downloaded from [8] with all dependencies. The reasoner is needed to perform queries on ontologies through Java. The documentation for a previous equivalent version (1.3.8.4) is available at [9]. The GNU license es applicable [5].

- myCBR: it is an open source tool for case-based reasoning applications. The Software Development Kit of myCBR project has been implemented in the application with the appropriate .jar file. The myCBR Workbench application may be very useful for visualizing .prj files. All the information concerning myCBR project (source code, installation guide, tutorials, javdoc, etc) is available at the website [10].

- Jena: it is a tool for ontology manipulation. In paritcular, it is used in this application for adding the capability to perform SPARQL queries on ontologies through Java with the SPARQL executable class in the project, that uses the Jena methods. The latest version is used (4.0.0), and it can be found at the Maven repository [13] (artifact jena-arq) or downloaded from [14] with all dependencies. A complete documentation of the Jena Core is available at [15]. The Apache license [4] is applicable.

- SWRL API with drools rule engine: the SWRL API may be used to implement SWRL rules in an ontology through a Java application. Moreover, if the drools reasoner is added, the application is able to execute SQWRL queries on the working ontology. In this case, the latest version of SWRL API (2.0.9) is used, which is available at the Maven repository [16]and at [17] for direct .jar download with all dependencies. A javadoc is available at [18]. Nevertheless, the compatibility of the SWRL API with OWL API is only guaranteed up to version 4.5.9, even if some later versions could be supported. Moreover, to query an ontology with the SWRL API and SQWRL language, an additional implementation of a reasoner is necessary: the implementation of drools engine is available for this purpose. Once again, it may be

found at the Maven repository [19] or for direct .jar download with all dependencies at [20].

## References

[1] JAR download (April 2021): https://jar-download.com/artifacts/net.sourceforge.owlapi/owlapi-distribution

[2] MVN repository (April 2021): https://mvnrepository.com/artifact/net.sourceforge.owlapi/owlapi-distribution/5.1.17

[3] OWL API javadoc (April 2021): https://javadoc.io/doc/net.sourceforge.owlapi/owlapi-distribution/latest/index.html

[4] Apache License version 2.0: https://www.apache.org/licenses/LICENSE-2.0

[5] GNU LESSER GENERAL PUBLIC LICENSE: http://www.gnu.org/licenses/lgpl- 3.0.txt

[6] MATENTZOGLU Nicolas., PALMISANO Ignazio. An introduction to OWL API. University of Manchester, 2016. http://syllabus.cs.manchester.ac.uk/pgt/2020/COMP62342/introduction-owl-api msc.pdf

[7] MVN repository (April 2021): https://mvnrepository.com/artifact/net.sourceforge.owlapi/org.semantic

[8] JAR download (April 2021): https://jar-download.com/?search`box=org.semanticweb.hermit

[9] HermiT 1.3.8.4 javadoc (April 2021): http://javadox.com/com.hermitreasoner/org.semanticweb.hermit/1.3.8.4/overview-summary.html

[10] myCBR website (April 2021): http://mycbr-project.org/index.

[11] SPARQL syntax reference (April 2021): https://www.w3.org/TR/sparql11-query/

[12] Javadoc reference (April 2021): https://www.oracle.com/technical- resources/articles/java/javadoc-tool.html

[13] MVN repository (April 2021): https://mvnrepository.com/artifact/org.apache.jena/jena-arq/4.0.0

[14] JAR download (April 2021): https://jar-download.com/artifacts/org.apache.jena/jena- arq

[15] Jena Core 4.0.0 (April 2021): https://jena.apache.org/documentation/javadoc/jena/

[16] MVN repository (April 2021): https://mvnrepository.com/artifact/edu.stanford.swrl/swrlapi/2.0.9

[17] JAR download (April 2021): https://jar-download.com/artifacts/edu.stanford.swrl/swrlapi

[18] SWRL API Javadoc (April 2021): http://soft.vub.ac.be/svnpub/PlatformKit/platformkit-kb-owlapi3-doc/doc/owlapi3/javadoc/overview-summary.html

[19] MVN repository (April 2021): https://mvnrepository.com/artifact/org.apache.jena/jena- arq/4.0.0

[20] JAR download (April 2021): https://jar-download.com/artifacts/org.apache.jena/jena-arq

[21] O'CONNOR Martin Joseph, DAS Amar. SQWRL: A Query Language for OWL. Stanford Center for Biomedical Informatics Research, 2009.

[22] GitHub repository (April 2021): https://github.com/CommonCoreOntology/CommonCoreOntologies

## Summary in French / Résumé en français

## Sommaire

maire

D.1 Introduction . . . . .

## D.1 Introduction

## D.1.1 Maintenance Prédictive

La maintenance prédictive est une stratégie de maintenance qui vise à déterminer le moment précis pour effectuer des actions de maintenance. Pas trop tôt, car les actions de maintenance peuvent entraîner le changement de pièces qui ont encore une durée de vie restante significative ce qui représente un coût pour les entreprises ; mais pas trop tard non plus, car une panne inattendue peut à son tour donner lieu à une série de conséquences négatives. La maintenance prédictive est une alternative aux autres stratégies de maintenance traditionnelles, telles que la maintenance corrective et la maintenance préventive. Au lieu d'attendre qu'une panne se produise ou d'effectuer une maintenance basée sur des intervalles de fonctionnement fixes, la maintenance prédictive est basée sur le diagnostic de l'état actuel de l'équipement et sur la prédiction du moment où une éventuelle panne pourrait survenir.

La maintenance prédictive est fortement liée à la maintenance basée sur l'état (Condition-Based Monitoring, CBM) et à la gestion de la santé basée sur les prévisions (Prognostics and Health Management, PHM). La maintenance prédictive et ces deux disciplines englobent le diagnostic et le pronostic de maintenance ; parfois ces termes sont même utilisés comme synonymes. Les deux termes maintenance prédictive et CBM sont apparus dans les années 1940 et font référence à la stratégie de maintenance qui vise à anticiper les pannes des machines en fonction de leur état. Cependant, ce n'est qu'au début des années 1990 que cette stratégie prend de l'importance grâce à la mise en place de systèmes de surveillance et d'outils de calcul capables de surveiller les tâches de diagnostic. Quant au pronostic de durée de vie restante, faisant partie de la maintenance prédictive et de la CBM, cela restait une discipline imprécise. Dès le début des années 2000, la discipline PHM a émergé avec l'objectif de couvrir des problèmes de pronostic. Depuis lors, les diagnostics de maintenance et la recherche de pronostics ont suscité beaucoup d'attention de la part des universités et de l'industrie ; grâce à l'augmentation continue de la puissance de calcul et compte tenu des avantages de sa mise en œuvre. Au cours de la dernière décennie, différentes contributions ont été apportées sous des termes différents (maintenance prédictive, CBM et PHM) ; elles se référent au même domaine de recherche.

## D.1.2 Idée conceptuelle et architecture d'un système

Selon le manuel INCOSE [INC15], le cycle de vie d'un système peut être divisé en six étapes génériques (voir Figure D.1). Le cycle de vie d'un système commence par l'étape conceptuelle, qui vise à explorer des solutions possibles pour répondre aux besoins et souhaits initiaux des parties prenantes. La phase conceptuelle est suivie de la phase de développement, au cours de laquelle une conception détaillée des composants du système et de leurs interfaces est réalisée. Après la conception détaillée, commence l'étape de production qui est dédiée à la mise en œuvre du système, c'est-à-dire la fabrication, le codage, la création des différents composants et leur intégration finale dans le système. La vérification et la validation du système font partie de la phase de production. Une fois le système validé, il est livré au client pour sa phase d'utilisation. Au stade de l'utilisation, le système remplit la fonction pour laquelle il a été créé. La phase de maintenance se déroule parallèlement à la phase d'utilisation pendant le fonctionnement du système. Cette étape de maintenance est destinée à assurer l'état de fonctionnement optimal du système. En fin de cycle de vie du système, la phase de retrait vise à bien gérer le retrait du système, sa mise hors service, et son démantèlement.

Le processus d'architecture du système se positionne au cœur de la phase conceptuelle. Cette phase commence par rassembler tous les besoins et souhaits des parties prenantes et les formaliser dans les exigences des different acteurs. Ces exigences sont ensuite utilisées pour créer l'architecture du système

<table border="1"><tr><td rowspan="2">Concept stage</td><td rowspan="2">Development stage</td><td rowspan="2">Production stage</td><td>Utilization stage</td><td rowspan="2">Retirement State</td></tr><tr><td>Support stage</td></tr></table>

<div align="center">

Figure. D.1: Étapes génériques du cycle de vie d'un système (traduit de l'anglais) [INC15]

</div>

qui servira de base à la conception détaillée et à la mise en œuvre du système. Le développement de l'architecture peut être divisé en trois niveaux [Roq18]; [INC15] : architecture fonctionnelle, architecture logique et architecture physique. L'architecture fonctionnelle décrit comment les différentes (sous-)fonctions d'un système interagissent les unes avec les autres pour atteindre un objectif spécifique, mais ne fournit aucun détail sur les composants qui remplissent chaque (sous-)fonction. L'architecture logique fournit autant de détails que possible sur les composants de l'architecture et leurs interfaces, mais n'implique pas à ce stade les choix quant aux réalisations et/ou aux technologies spécifiques, ce qui signifie que l'architecture logique montre des composants génériques. L'architecture physique fournit les détails des technologies à affecter à chaque composant logique. L'union de ces trois niveaux d'architecture peut être appelée l'architecture du système et peut alors être définie comme les « concepts ou propriétés fondamentaux d'un système dans son environnement incorporés dans ses éléments, ses relations et dans les principes de sa conception et évolution » [ISO11]. En termes simples, l'architecture traite de la manière dont un ensemble d'éléments, qui peuvent être physiques ou informationnels, sont organisés pour répondre à un objectif spécifique.

## D.1.3 Questions à la base de ce projet de recherche

La maintenance prédictive est réalisée à l'aide d'approches spécialisées pour effectuer des tâches de diagnostic et de pronostic, afin de déterminer le bon moment pour déclencher les actions de maintenance. En ce moment, la conception et le développement de ces systèmes spécialisés continuent d'être basés sur des essais et des erreurs. Il existe plusieurs architectures génériques dans les normes et standards, comme [MIM01], mais en réalité la conception d'un nouveau système de maintenance prédictive commence beaucoup plus tôt, au stade conceptuel, moment auquel ces architecture génériques n'aident pas encore l'architecte. En effet, une architecture générique ne fournit pas de liens avec les besoins et souhaits initiaux d'un nouveau système de maintenance prédictive, et ces besoins et souhaits peuvent bien ne pas être couverts par une architecture générique. De plus, une architecture générique ne fournit aucune indication pour sélectionner les technologies appropriées pouvant réaliser les composants génériques [MV19], par exemple pour la détction d'un défaut ou pour l'estimation d'une durée de vie restante à partir d'une série de mesures.

Même si la maintenance prédictive traite en général des tâches de diagnostic et de pronostic, tous les systèmes prédictifs ne couvrent pas exactement les mêmes fonctions. Par exemple, un nouveau système de maintenance prédictive peut être destiné à effectuer des diagnostics sur différents composants d'un système ; plusieurs modules de diagnostic du même type seront nécessaires et les modules de prédiction ne seront pas inclus. Les architectures génériques ne fournissent pas une approche systématique pour les conceptions qui n'ont besoin que d'un sous-ensemble des composants génériques proposés ou lorsque plusieurs composants du même type sont nécessaires.

Il existe un nombre important d'options pour réaliser les fonctions de diagnostic et de pronostic dans un système de maintenance prédictive, et il n'y a pas de directives pour aider l'architecte à sélectionner les modèles, techniques ou algorithmes appropriés qui peuvent exécuter ces fonctions. L'exploration de l'espace de solution pour déterminer les composants appropriés peut alors être complexe et prendre du temps. Cette thèse vise à faciliter le processus architectural des systèmes de maintenance prédictive en permettant une manière plus efficace d'explorer l'espace des solutions et de proposer les composants les plus adaptés à l'architecture du système.

Avant d'aborder la conception de systèmes de maintenance prédictive, il est important de comprendre le domaine de la recherche en maintenance prédictive lui-même et les différentes options disponibles pour effectuer des diagnostics et des pronostics. Les questions de recherche suivantes sont proposées pour guider l'étude de l'état de l'art dans ce domaine :

1. Quelles sont les tendances actuelles du diagnostic et du pronostic en maintenance prédictive ?

2. Quels types de modèles, techniques ou méthodes sont utilisés pour traiter le diagnostic et le pronostic en maintenance prédictive ?

3. Quels sont les principaux défis rencontrés par la maintenance prédictive dans le diagnostic et le pronostic ?

Après l'étude de l'état de l'art, les questions de recherche sont adaptées en fonction des résultats de l'étude et de la motivation initiale de cette recherche liée à la conception de systèmes de maintenance prédictive (voir section D.2).

## D.1.4 Organisation du résumé

La section D.2 aborde l'état de l'art de la maintenance prédictive sur la base des questions de recherche initiales introduites ci-dessus. Cette section est liée au chapitre 2 de la thèse, qui est composé d'un article publié qui comprend les tendances actuelles des modèles de diagnostic et de pronostic dans le domaine de la maintenance. La section se termine en affinant les questions de recherche qui ont motivé le reste de la recherche.

La section D.3 propose une approche d'ingénierie des systèmes pour la conception de systèmes de maintenance prédictive, en particulier au stade conceptuel de l'analyse des besoins et souhaits initiaux des parties prenantes jusqu'à la proposition d'une architecture logique. Cette section est liée au chapitre 3 de la thèse qui est composé d'un article publié et présenté lors d'une conférence et se termine en présentant la sélection de la composante maintenance prédictive comme le défi principal qui sera abordé dans les chapitres suivants. Un système d'aide à la décision (Decision Support System, DSS) qui combine des ontologies et un raisonnement basé aux cas est proposé comme une solution possible pour aborder la sélection de composants dans l'approche systématique.

La section D.4 explique l'un des éléments de base d'aide à la décision : les ontologies. Des recherches complémentaires ont été spécifiquement menées sur les ontologies qui ont abouti à un article de revue, accepté pour publication au moment de la rédaction de ce manuscrit, et qui présente un modèle ontologique pour la sélection et l'évaluation des stratégies de maintenance (Ontology for Maintenance Strategy Selection and Architecture, OMSSA). Le contexte théorique des ontologies est présenté en soulignant leur importance dans la communauté des chercheurs en raison de leurs capacités à modéliser formellement le vocabulaire d'un domaine spécifique et à le raisonner. La section D.4 explique le développement de l'ontologie qui sera ensuite utilisée dans le DSS pour la sélection des composants.

La section D.5 présente le deuxième pilier du DSS : le raisonnement basé aux cas (Case-Based Reasoning, CBR). Les principes du paradigme de la CBR ont été présentés, y compris les phases de son cycle générique. Dans une première approche pour adresser les questions à la base de cette thèse, le DSS se concentre sur la phase de récupération de la CBR. Une explication de la mise en œuvre du moteur de récupération CBR est fournie à l'aide de code source logicielle.

La section D.6 explique le cadre général d'intégration des composants de base du DSS et comment il s'intègre dans l'approche systématique de la conception des systèmes de maintenance prédictive. Cette

section est liée au chapitre 6 de la thèse qui est composé d'un article de conférence publié et qui est la suite de l'article présenté dans la section D.2. Une validation croisée est effectuée pour démontrer les capacités du DSS.

La section D.7 est destinée à étendre la validation du DSS. Une étude de cas est présentée pour développer l'approche complète proposée dans la recherche actuelle et un exemple de modèle de maintenance prédictive est mis en œuvre pour l'étude de cas sur la base des suggestions du DSS. Les résultats de cette mise en œuvre sont expliqués et analysés.

La section D.8 tire des conclusions de travaux présentés et propose des perspectives pour une suite dans ces activités de recherche.

## D.2 Vers une approche multimodèle de la maintenance prédictive : une revue littéraire systématique sur le diagnostic et le pronostic

Une revue systématique de la littérature montre que la maintenance prédictive gagne de plus en plus en importance dans la communauté universitaire, en particulier au cours des 25 dernières années. La Figure D.2 montre le nombre de publications mentionnant les termes « maintenance prédictive », « maintenance conditionnelle » et « pronostic et prise en charge de l'état de la santé » au cours des 25 dernières années dans les sources de recherche consultées.


> **Figure Description:**

This bar chart displays the number of publications on three specific terms—Predictive Maintenance, Prognostics and health management, and Condition-based maintenance—from 1995 to 2019. The vertical axis represents the "Number of publications on which therms are found" (sic) ranging from 0 to 300 in increments of 50, while the horizontal axis lists each year from 1995 to 2019. The legend identifies the three categories by color: blue for Predictive Maintenance, red for Prognostics and health management, and green for Condition-based maintenance.

The data shows a general upward trend for all three categories over the 25-year period. Predictive Maintenance (blue) shows consistent growth, starting at 8 in 1995 and reaching 245 by 2019, with a peak of 265 in 2018. Prognostics and health management (red) remains at or near zero until 2000, then grows steadily to reach 130 in 2019. Condition-based maintenance (green) shows the highest overall volume in many years, starting at 0 in 1995, reaching 52 in 2001, and peaking at 267 in 2017 before declining to 218 in 2019. 

Specific data points for each year are as follows: 1995 (8, 0, 0), 1996 (8, 0, 0), 1997 (16, 0, 12), 1998 (38, 0, 12), 1999 (39, 0, 30), 2000 (43, 5, 43), 2001 (40, 8, 52), 2002 (44, 5, 44), 2003 (46, 0, 39), 2004 (38, 5, 46), 2005 (44, 2, 44), 2006 (62, 18, 94), 2007 (52, 13, 76), 2008 (63, 24, 90), 2009 (67, 26, 117), 2010 (68, 38, 119), 2011 (58, 33, 119), 2012 (99, 50, 195), 2013 (110, 73, 162), 2014 (87, 58, 182), 2015 (133, 76, 219), 2016 (156, 96, 222), 2017 (227, 113, 267), 2018 (265, 110, 244), and 2019 (245, 130, 218).



<div align="center">

Figure. D.2: Nombre de publications liées à la maintenance prédictive au cours des 25 dernières années

</div>

La revue de la littérature se compose de deux parties. La première portait sur les précédentes revues bibliographiques sur la maintenance prédictive, qui ont permis d'identifier les modèles utilisés pour la maintenance prédictive et l'évolution des tendances au cours des années. Les taxonomies utilisées pour classer les différents modèles prédictifs monrent de légères variations terminologiques d'une étude à l'autre dans les études diagnostiques et pronostiques en maintenance. On peut distinguer deux approches principales : les approches mono-modèles et les approches multi-modèles. Pour les approches mono-modèles, on peut identifier trois familles de modèles : modèles basés sur la connaissance, modèles basés sur des données et modèles basés sur la physique. Les approches multi-modèles combinent au moins deux modèles des trois familles de modèles mentionnées. Les approches multi-modèles peuvent avoir différentes configurations et sont parfois appelées modèles hybrides.

La seconde partie de la revue de la littérature a été consacrée à l'étude des tendances actuelles des différentes approches des modèles. La revue a démontré l'existance d'une tendance à la mise en œuvre d'approches multi-modèles puisqu'un seul modèle souvent ne satisfait pas à toutes les fonctions d'un système de maintenance prédictive. La figure D.3 montre toutes les possibilités de combinaison de modèles dans des approches multi-modèles.


> **Figure Description:**

This diagram illustrates potential combinations of three modeling approaches: Knowledge-based, Data-driven, and Physics-based. The three primary approaches are represented as rounded rectangles positioned at the vertices of a triangle: Knowledge-based at the top, Data-driven at the bottom left, and Physics-based at the bottom right. A large dashed-line oval encompasses the entire structure, labeled "Potential combinations" at the bottom center.

The diagram displays various interaction types through labeled boxes connected by lines or curved arrows. A central box labeled "KB+DD+PB" is connected to each of the three primary approach boxes by straight lines, representing the integration of all three. Additionally, there are direct connections between the primary approaches: a line labeled "KB+DD" connects Knowledge-based and Data-driven, a line labeled "KB+PB" connects Knowledge-based and Physics-based, and a line labeled "DD-PB" connects Data-driven and Physics-based.

Self-referential or internal interactions are represented by curved arrows and boxes: a "KB-KB" box is connected to the Knowledge-based box, a "DD-DD" box is connected to the Data-driven box, and a "PB-PB" box is connected to the Physics-based box. All text labels are oriented horizontally within their respective boxes or along the connecting lines.



KB: Knowledge-based model. DD: Data-driven model. PB: Physics-based model.

## Figure. D.3: Combinaisons possibles de modèles de maintenance prédictive

La revue bibliographique a permis d'identifier les enjeux actuels de la maintenance prédictive :

- Extrapolation des solutions de maintenance prédictive existantes dans des applications complexes, incluant plusieurs composants et leurs défaillances associées. La plupart des applications identifiées se concentraient sur un seul composant avec un nombre limité de défauts possibles. Cependant, les applications réelles sont souvent des systèmes complexes constitués de nombreux composants et de nombreux défauts associés à chaque composant et au système lui-même. Les approches multi-modèles offrent une solution potentielle pour surmonter la complexité des systèmes de maintenance prédictive.

- L'absence d'une approche systématique pour concevoir et développer des systèmes de maintenance prédictive. Il existe des standards, des normes et des architectures génériques pour développer de nouveaux systèmes de maintenance prédictive, tels que OSA-CBM. Cependant, ils se concentrent uniquement sur les composants fonctionnels de base du système et ne couvrent pas les aspects importants des indicateurs de performance ou des contraintes du contexte du système. De plus, ils n'offrent pas d'explication cohérente sur les modèles à utiliser en fonction des besoins initiaux du système de maintenance prédictive. L'absence d'approche systématique limite la mise en œuvre de systèmes de maintenance prédictive dans les applications industrielles à grande échelle.

- La fusion de diverses sources de données de contrôle de l'état des systèmes. Ce défi est lié à l'extrapolation des modèles actuels de maintenance prédictive aux systèmes complexes. Les systèmes techniques peuvent avoir différents types de sources de données, par exemple des mesures de capteurs, des enregistrements de maintenance, des enregistrements opérationnels, des documents de conception, etc. Des informations importantes pourraient être recueillies auprès de toutes ces sources pour mettre en œuvre de nouveaux systèmes de maintenance prédictive.

- Intégration des données d'influence externe à l'exploitation des systèmes. Le fonctionnement des systèmes peut varier en fonction du contexte d'exploitation. Des changements dans ce contexte opérationnel peuvent affecter directement les performances du système et, par conséquent, les analyses de surveillance de l'état de santé du système. Il peut ainsi déclencher de fausses alarmes suggérant l'existence de défauts, ou il peut à l'inverse empêcher l'identification de défauts existants. Des modèles complémentaires capables d'intégrer une influence externe à des fins de maintenance prédictive pourraient contribuer à une solution.

- Gestion de l'incertitude numérique des mesures. L'incertitude de mesures et de calculs affecte directement l'exactitude du diagnostic et du pronostic. Cela peut être dû aux données collectées ou aux imperfections du modèle utilisé pour l'analyse. Cela peut affecter la fiabilité des résultats. La gestion de l'incertitude est vitale pour les systèmes critiques soumis à la réglementation des autorités. C'est le cas des systèmes critiques tels que les centrales nucléaires et les avions où les réglementations sont restrictives pour maintenir les normes de sécurité et éviter les événements catastrophiques.

L'étude de l'état de l'art a motivé l'amélioration des questions de recherche. Le reste de la recherche a été motivé par les questions suivantes :

1. Comment aborder l'architecture et la conception des systèmes de maintenance prédictive?

2. Comment sélectionner un modèle ou une combinaison de modèles appropriés compte tenu d'un nouveau problème de maintenance prédictive à résoudre?

3. Comment proposer une approche adaptée pour une solution de maintenance prédictive?

4. Comment un concepteur peut-il bénéficier de l'expérience des systèmes existants pour développer de nouvelles solutions de maintenance prédictive?

## D.3 Des besoins et souhaits pour une architecture logique de systèmes de maintenance prédictive

La question de recherche No. 1 obtenue à l'issue de l'étude de l'état de l'art porte sur la conception de nouveaux systèmes de maintenance prédictive. Dans l'énoncé de recherche présenté dans la section D.1, il a été expliqué que la conception et le développement de systèmes de maintenance prédictive sont toujours basés sur des essais et des erreurs. Malgré l'existence de plusieurs architectures génériques dans les normes et standards, telles que [MIM01], l'étape conceptuelle de tels systèmes n'est pas entièrement couverte. Il existe un écart dans le développement de tels systèmes, depuis la collecte des besoins et des souhaits pour le nouveau système jusqu'à la création de l'architecture qui répond aux besoins et souhaits initiaux.

La création d'un nouveau système doit toujours commencer par une analyse des besoins et souhaits exprimés (ou pas) par les parties prenantes. Ces besoins et souhaits permettent d'établir une liste des exigences des parties prenantes pour le nouveau système. Les recherches actuelles proposent une approche d'ingénierie des systèmes pour couvrir l'étape conceptuelle des systèmes de maintenance prédictive.

La Figure D.4 montre les différentes étapes abordées dans l'approche d'ingénierie des systèmes proposée dans cette thèse. Il commence par recueillir les besoins et les souhaits initiaux des parties prenantes, qui sont par la suite traduits dans une liste formelle des exigences des parties prenantes. Les exigences sont hiérarchisées et classées en exigences fonctionnelles, de performance, structurelles et expérientielles. Cette classification aidera à la création de l'architecture du système. Les exigences fonctionnelles sont utilisées

pour démarrer le processus d'architecture, en particulier pour effectuer l'analyse fonctionnelle et créer le fonctionnel. L'architecture fonctionnelle est ensuite utilisée pour développer l'architecture logique qui reste générique. Les exigences de performance, structureles et expérientielles sont utilisées pour faire la sélection des composants pour répondre à l'architecture logique et créer l'architecture physique.


> **Figure Description:**

This diagram is a flowchart illustrating a sequential process for developing a predictive maintenance system, consisting of six primary steps represented by yellow rounded rectangles, each marked with an "OR" icon. The process begins at the top with "Gather needs and desires for a new predictive maintenance system," which flows downward to "Formalize stakeholder requirements," then to "Classify and prioritize requirements," followed by "Perform Functional Analysis," "Develop Logical Architecture," and finally "Develop physical architecture" at the bottom.

Each transition between these steps is marked by a small orange icon and a label indicating the output of the preceding step. Specifically, the transition from the first to the second step is labeled "Needs and desires for the new predictive maintenance system," the second to the third is "Formal stakeholder requirements," the third to the fourth is "Functional requirements," the fourth to the fifth is "Functional Architecture," and the fifth to the sixth is "Logical Architecture." Additionally, a side branch originates from the "Classify and prioritize requirements" step, looping around to the right and connecting to the final "Develop physical architecture" step; this branch is labeled with the text "Behavioral, structural and experiential requirements" accompanied by the same orange icon used for the other transitions.



<div align="center">

Figure. D.4: Étapes abordées dans l'approche d'ingénierie des systèmes pour la conception de systèmes de maintenance prédictive

</div>

Cette section est liée au chapitre 3 de la thèse dans lequel une approche systématique a été proposée pour aborder l'étape conceptuelle des systèmes de maintenance prédictive afin de répondre à la première question de recherche affinée. Les différentes étapes depuis la satisfaction des besoins et souhaits initiaux des parties prenantes jusqu'à la définition de l'architecture logique ont été couvertes et différentes méthodes ont été proposées pour y répondre. Cependant, le reste des questions de recherche affinées n'a pas encore trouvé de réponse. En maintenance prédictive, l'espace des solutions est vaste et complexe comme le montre le chapitre 2 de la thèse. Il n'y a pas de règles spécifiques qu'un architecte peut suivre pour sélectionner les bons modèles et approches pour résoudre de nouveaux problèmes de maintenance prédictive. Dans cette recherche, une hypothèse est proposée pour surmonter ce problème : la mise en œuvre d'un système d'aide à la décision (DSS) basé sur le raisonnement basé au cas (CBR) et soutenu par des ontologies pourrait aider l'architecte à sélectionner des composants appropriés sur la base d'expériences passées à partir d'expériences réussies.

## D.4 Développement d'une ontologie pour le système de raisonnement par cas

Le DSS est composé de deux blocs principaux : le raisonnement basé aux cas (CBR) et les ontologies. La CBR est un paradigme de raisonnement qui cherche à résoudre de nouveaux problèmes sur la base des expériences de problèmes similaires résolus dans le passé. La CBR est abordée dans le chapitre 5 de la thèse et dans la section D.5 de ce résumé, mais une brève introduction est nécessaire pour comprendre le rôle que jouent les ontologies dans le DSS développé dans les recherches actuelles. Les systèmes CBR sont développés sur un vocabulaire de base [Alt+12]; [Sán+12]. Ce vocabulaire est nécessaire pour structurer les cas de problèmes résolus stockés dans un « case base », pour les mesures de similarité qui comparent le nouveau problème avec ceux du « case base », et pour les connaissances nécessaires pour adapter la solution récupérée au nouveau problème (voir Figure D.5). Pour les besoins de cette thèse, une ontologie est choisie pour servir de cadre terminologique (vocabulaire de base). Un modèle d'ontologie fournit les termes, les définitions et les relations entre les termes qui sont utilisés pour construire la structure de cas, les similitudes et les connaissances adaptatives dans le DSS. Ce chapitre est consacré au contexte théorique et au développement du modèle d'ontologie pour le DSS proposé.


> **Figure Description:**

The image is a diagram illustrating the components of a case-based reasoning system. It consists of a large outer circle containing a smaller, concentric dashed circle. The space between the two circles is labeled "Vocabulary" in three locations, oriented to follow the curvature of the outer circle at the top, bottom-left, and bottom-right. The inner dashed circle is divided into three equal sectors by dashed lines radiating from the center. The top sector contains the text "Case base," the bottom-left sector contains "Similarity measures," and the bottom-right sector contains "Adaptation knowledge." Double-headed arrows indicate relationships between these components: one arrow connects "Case base" to "Similarity measures," one connects "Case base" to "Adaptation knowledge," and one connects "Similarity measures" to "Adaptation knowledge."



<div align="center">

Figure. D.5: Raisonnement basé aux cas, développé sur un cadre de vocabulaire [Alt+12]

</div>

En sciences de l'information, une ontologie est une description explicite formelle de concepts dans un domaine de discours, propriétés de chaque concept qui décrivent ses caractéristiques, attributs et restrictions [NM01]. L'un des objectifs les plus courants dans le développement d'ontologies est de « partager une compréhension commune de la structure des informations entre les personnes et les agents logiciels » [Gru93]; [Mus92]. Cela signifie que le vocabulaire utilisé par les personnes dans un domaine de connaissance spécifique peut être « lisible par machine ». Tous les concepts d'une ontologie sont représentés par des classes liées par des propriétés (également appelées relations). Les ontologies sont développées avec des langages formels. L'un des plus reconnus est le langage d'ontologie Web dans sa deuxième version (OWL2) qui est pris en charge par le World Wide Web Consortium (W3C) [Wor12].

## D.4.1 Ontologie pour la sélection et l'évaluation des stratégies de maintenance (OMSSA)

Une enquête complémentaire de fil conducteur de cette thèse a permis la création d'un modèle ontologique pour la sélection et l'évaluation des stratégies de maintenance (OMSSA). La création d'OMSSA suit les normes les plus elevées et les dernières tendances en matière de création d'ontologies à l'aide d'ontologies de référence de haut et de moyen niveau. Cela facilitera la réutilisation et l'intégration d'OMSSA avec d'autres ontologies connexes. La contribution de l'OMSSA a été consolidée dans un article scientifique qui

a été accepté pour publication au moment où cette thèse a été écrite. OMSSA sert de base à la création du modèle ontologique utilisé pour le système d'aide à la décision (DSS) proposé dans cette thèse.

## D.4.2 Ontologie pour la conception de maintenance prédictive (OPMAD)

OPMAD est une extension de l'OMSSA et les mêmes normes et méthodologies ont été suivies pour son développement. Dans ce qui suit dans ce résumé, les noms de classe d'OPMAD seront conversés en anglais afin de maintenir la cohérence avec le modèle et les graphiques. La Figure D.6 présente les classes et relations les plus importantes dans OPMAD. En raison des limitations d'espace, les sous-classes ne sont pas représentées sur la figure. Comme l'objectif d'OPMAD est d'aider le DSS à identifier des modèles appropriés pour les systèmes de maintenance prédictive, l'explication des classes d'ontologies et de leurs relations commence à partir de la classe Modèle de maintenance prédictive (Predictive Maintenance Model) et est basée sur les termes présentés dans la Figure D.6. Un modèle de maintenance prédictive est transporté dans un module de maintenance prédictive (Predictive Maintenance Module) qui est un composant d'un système de maintenance prédictive (Predictive Maintenance System). Chaque module de maintenance prédictive a une fonction de maintenance prédictive (Predictive Maintenance Function), cette recherche se concentre sur les fonctions de diagnostic et de pronostic.

Le modèle de maintenance prédictive intégré dans le module est directement lié à un élément maintainable (Maintainable item), qui est la classe qui décrit le système maintainable pour lequel le système de maintenance prédictive est développé. L'élément maintainable est classé par la classe de type d'élément maintainable (Maintainable item type) qui a été ajoutée à des fins de calcul de similarité dans le DSS ; ces types de classes aident à comparer le nouveau problème à traiter avec le problème résolu dans un « case base » d'un système CBR. Les éléments maintainables appartenant au même type partagent des caractéristiques de dégradation importantes et donc les mêmes modèles de maintenance prédictive peuvent être proposés pour résoudre les mêmes fonctions de maintenance prédictive. L'élément maintainable a sa propre fonction (Function) qui est affectée par une défaillance (Failure) se manifestant par un mode de défaillance (Failure Mode). Un élément maintainable a un ou plusieurs modes de défaillance qui font également l'objet du modèle de maintenance prédictive. Dans le modèle de maintenance prédictive sont entrées les données d'état (Condition) qui sont utilisées pour effectuer des diagnostics et des pronostics. Les deux qualités importantes pour la mise en œuvre d'un modèle de maintenance prédictive sont son type et sa configuration. Le type de modèle de maintenance prédictive (Predictive Maintenance Model Type) classe le modèle en familles de modèles basés sur les connaissances, sur les données et sur la physique. Ce type de classification est utile aux fins de la similitude et des préférences dans le DSS.

La configuration du modèle de maintenance prédictive (Predictive Maintenance Model Configuration) indique si un modèle doit être complété par d'autres modèles pour remplir sa fonction ; il peut améliorer les performances, mais augmente la complexité du développement. Le module de maintenance prédictive est noté par indicateur de synchronisation (Module Synchronization) et de performance (Performance indicator). Ces deux qualités fournissent des informations utiles sur la façon dont les modèles de maintenance prédictive intégrés dans les modules doivent être testés et synchronisés avec l'élément maintainable. Toutes ces informations sur les modèles de maintenance prédictive, les éléments maintainables, leurs modèles de défaillance, entre autres, sont collectées dans le cas de la maintenance prédictive (Predictive Maintenance Case) qui est documentée et publiée via un article de maintenance prédictive (Predictive Maintenance Article), un type spécial de l'article qui se concentre sur la maintenance prédictive. A partir de ces articles de maintenance prédictive, certains indicateurs bibliométriques sont également inclus dans l'ontologie qui sera utilisée dans le système CBR. Ces indicateurs bibliométriques sont fournis en tant qu'attributs de solution afin que l'ingénieur puisse facilement trouver la source d'information pour un cas spécifique. Le titre, l'identifiant et l'année de publication de l'article peuvent être utilisés à des fins de similarité et/ou comme source d'information pour plus de détails sur les modèles de maintenance

prédictive et leur mise en œuvre.


> **Figure Description:**

This diagram is a conceptual ontology or entity-relationship model illustrating the components and relationships within a Predictive Maintenance (PdM) system. The central node is the "PdM Module," which is a part of the "PdM System" (connected via *hasPart*). The "PdM Module" has relationships with several entities: it *hasQuality* links to both "Synchronization" and "Sychronization," it *isCarrierOf* a "PdM Model," and it *hasFunction* links to "PdM Module function."

The "PdM Model" is connected to "PdM Model configuration" (*hasConfiguration*), "PdM Model type" (*hasType*), "Condition Data" (*hasInput*), and "Maintainable item" (*IsAbout*). "Condition Data" is further linked to "Condition Data Type" via *hasType*. The "Maintainable item" serves as a central hub, connecting to "Maintainable item type" (*hasType*), "Function" (*hasFunction*), "Failure Mode" (*hasFailureMode*), and "PdM Case" (*hasCaseStudy*).

The "Function" entity is linked to "PdM Module function" via *is a* and is *isAffectedBy* "Failure." The "Failure" entity is linked to "Failure Mode" via *describes*. At the bottom of the diagram, "PdM Article" is linked to "PdM Case" via *isCarrierOf*. "PdM Article" is also the target of *IsAbout* relationships originating from "PdM Article title," "PdM Article identifier," and "PdM Article Publication year." All relationships are represented by directed arrows with italicized labels indicating the nature of the connection between the rectangular entity boxes.



<div align="center">

Figure. D.6: Classes et relations dans OPMAD

</div>

## D.5 Développement de systèmes de raisonnement par cas

Le raisonnement basé sur les cas (CBR) est une méthodologie de résolution de problèmes basée sur la récupération de solutions précédentes pour des problèmes similaires [De +05]. Le raisonnement basé sur les cas a été développé sous la philosophie selon laquelle les êtes humains pensent et raisonnent en utilisant des analogies et des exemples, plutôt que des structures SI-ALORS, ces dernières formant la base du raisonnement basé sur des règles. La résolution du problème s'effectue dans un processus cyclique de plusieurs étapes : le cycle CBR [AP94]. Ce cycle est composé de quatre phases : récupération, réutilisation, révision et conservation (voir Figure D.7).

Le cycle CBR démarre lorsqu'un nouveau problème est présenté. La première phase vise à récupérer les cas les plus similaires à partir d'une base de connaissances qui stocke tous les cas précédents. Le cas cible (nouveau) est comparé aux cas existants dans la base de connaissances à l'aide de différentes mesures de similarité. Le cas récupéré le plus proche est proposé comme solution possible en phase de réutilisation. Une certaine adaptation peut être nécessaire pour appliquer la solution dans le cas prévu. Une fois la solution suggérée et mise en œuvre, la phase d'examen est effectuée. Si la solution suggérée parvient à résoudre le problème, elle est confirmée et dans la dernière phase, elle est conservée dans la base de connaissances afin qu'elle puisse être réutilisée dans de futurs problèmes similaires. Plus de détails sur chaque phase de la


> **Figure Description:**

This diagram illustrates the Case-Based Reasoning cycle, organized as a circular process with a central knowledge base. At the center is a box labeled "General Knowledge" containing a stack of documents labeled "Previous cases." Surrounding this center are four distinct phases arranged in a clockwise circle, each represented by a shaded arc and specific process steps.

The cycle begins at the top with a "Problem" input leading to a "New case" box. This feeds into the "RETRIEVE" phase, which connects to a "Retrieved case" box positioned next to another "New case" box. The process continues to the "REUSE" phase, which leads to a "Solved case" box that points outward to a "Suggested Solution." This then moves into the "REVISE" phase, leading to a "Tested/Repeated case" box. From this box, an arrow points outward to a "Confirmed Solution," and the process continues to the "RETAIN" phase. This phase connects to a "Learned case" box, which feeds back into the central "Previous cases" stack.

Double-headed arrows indicate bidirectional interaction between the central "General Knowledge" base and each of the four phases (RETRIEVE, REUSE, REVISE, and RETAIN). The flow of the cycle is sequential, moving from the retrieval of previous cases to the reuse of information, the revision of solutions, and the retention of new knowledge, all while maintaining a constant link to the central repository of previous cases.



<div align="center">

Figure. D.7: Cycle de raisonnement basé aux cas, image inspirée par [AP94]

</div>

CBR sont fournis dans les sous-sections suivantes.

## D.5.1 Plateforme MyCBR

Le module CBR du DSS dans ce projet de recherche a été créé à l'aide de myCBR, un outil de recherche pour le raisonnement basé aux cas « open source » [Alt+12]. Lors du développement d'un système de récupération CBR à l'aide de myCBR, la première étape consiste à déterminer les attributs des cas. Les cas sont représentés par un vecteur d'attributs charactérisant les problèmes et les solutions :

$$
\mathrm {C a s e} = [ \mathrm {A t t r i b u t s d e p r o b l e m e}, \mathrm {A t t r i b u t s d e s o l u t i o n} ]
$$

Les attributs de problème sont utilisés pour mesurer la similarité d'un cas cible et des cas d'un « case base »". Les attributs de la solution, comme son nom l'indique, fournissent des informations pertinentes relatives à la solution du problème dans chaque cas stocké dans la base de cas.

La deuxième étape consiste à attribuer une similarité locale à chaque attribut du problème. MyCBR fournit plusieurs options pour calculer la similarité pour chaque attribut du problème. Parmi les options disponibles, trois fonctions de similarité ont été utilisées pour les recherches actuelles :

1. Similarité nombre entier/flottant : cette fonction de similarité est utilisée pour les attributs numériques. La similarité est obtenue par une différence entre une valeur de référence et les valeurs d'entrée de la fonction. Une fonction mathématique est nécessaire pour définir comment la similarité diminue à mesure que les valeurs d'entrée s'éloignent de la valeur de référence. Cette fonction mathématique peut être linéaire, exponentielle ou déterminée par des points discrets sur le plan cartésien.

2. Similitude de symbole : Cette mesure de similarité est recommandée pour les variables avec un ensemble fixe d'options. Ces options sont organisées dans une matrice de similarité et certaines valeurs numériques sont données pour établir la similarité entre les options. Cette fonction de similarité a été modifiée afin que certains attributs de la recherche actuelle interagissent avec le modèle ontologique. Les valeurs de la matrice de similarité sont obtenues automatiquement à partir des classes et relations d'une ontologie en utilisant l'approche de similarité basée sur les caractéristiques proposées par [Sán+12].

3. Similitude de chaîne de caractères : la similarité d'attribut est obtenue sur la base de chaînes de texte ouvertes. Contrairement à la similarité de symboles qui a un nombre limité d'options pour définir la similarité, la similarité de chaîne n'a que la restriction d'avoir des phrases ou des mots en entrée. MyCBR propose trois options pour calculer la similarité basée sur les chaînes : Equality, Ngram et Levenshtein. Pour l'étude de cas actuelle, la fonction Levenshtein a été sélectionnée pour calculer les attributs en fonction des chaînes de similarité. La fonction Levenshtein offre un moyen flexible de calculer la similarité en fonction de chaque caractère de la chaîne [Lev66]. Ceci est particulièrement utile lorsqu'il existe un grand nombre d'options inconnues lors de la création de similitudes, et il tolère également les fautes d'orthographe mineures.

Après le calcul de similitude pour chacun des attributs du problème, ces similitudes individuelles sont combinées pour en dériver une similitude globale. Chaque attribut a un poids et à travers une fonction d'agrégation la similarité globale est calculée. L'objectif des poids est de donner une importance particulière aux attributs du problème. Aux fins de cette recherche, tous les attributs reçoivent un poids de 1, ce qui signifie qu'ils sont d'égale importance. MyCBR propose deux options différentes pour calculer la similarité globale : somme pondérée et distance euclidienne.

- Somme pondérée : comme son nom l'indique, c'est la somme des similitudes compte tenu du poids de chacun.

- Distance euclidienne : la distance euclidienne entre deux points dans l'espace euclidien est un nombre, la longueur d'un segment de droite entre les deux points.

Dans cette thèse, les deux fonctions de fusion peuvent être choisies par l'utilisateur. Il est important de noter que seuls les attributs retenus dans la description du problème sont pris en compte pour calculer la similarité globale. Cela signifie que si l'architecte n'a que deux ou trois attributs sur les sept qui décrivent le problème, la similarité globale sera calculée en fonction de ces deux ou trois attributs.

## D.5.2 Représentation des cas

« Un cas est une connaissance dans un contexte particulier qui représente une expérience qui enseigne une leçon essentielle pour atteindre le but du raisonneur » [Kol93]. Les cas sont souvent représentés sous une forme couplée [problème, solution], dans laquelle les similitudes sont appliquées à la partie "problème" afin que la partie "solution" soit récupérée. La représentation du cas est composée de trois parties principales [BKP05] :

1. Définissez les attributs du cas.

2. Définissez la structure du contenu du cas.

3. Organisez le « case base » .

La représentation et la structure du cas se font à l'aide d'OPMAD. La Figure D.6 montre les différents attributs (classes en ontologie) d'un cas représenté dans OPMAD. Ces classes d'ontologies peuvent être divisées en deux groupes différents : les attributs de problème et les attributs de solution :

- Attributes du problème = [PdM Function, Maintainable Item, Maintainable Item Type, Condition Data Type, Module synchronization, PdM Article Publication year]

- Attributes du problème = [PdM Model,PdM Model Configuration,PdM Model Type,Module Performance Indicator,PdM Article Identifier,PdM Article Title]

## D.5.3 Développement du moteur de récupération de composants pour les systèmes de maintenance prédictive

Le « case base » dans le DSS est une version instanciée de l'ontologie OPMAD qui a été renseignée de cas réussis d'implementations de maintenance prédictive à partir d'une revue bibliographique approfondie. Le processus d'instanciation d'OPMAD comprend la définition des différentes variables de recherche et les options possibles pour chaque variable ; cela permet une meilleure structure du « case base » et facilite la récupération des cas pendant le raisonnement. Pour chaque attribut de problème, une similarité locale est sélectionnée parmi les options possibles : entier, symbole, basé sur une ontologie, texte ouvert. Le Tableau D.1 montre les fonctions de similarité attribuées à chacun des attributs du problème. Deux fonctions d'agrégation différentes ont été ajoutées pour calculer la similarité globale entre un cas cible et les cas stockés dans le « case base ». Une interface graphique a été développée pour faciliter la vérification et la validation du moteur de récupération. Le moteur de récupération développé est le cœur du DSS pour la sélection des composants de maintenance prédictive. Le chapitre suivant est orienté pour montrer le cadre complet du système CBR avec une ontologie pour la sélection des composants de maintenance prédictive. Les détails du développement du moteur de récupération sont fournis dans le guide de code à l'annexe C.

<div align="center">

Tableau D.1: Affectation des fonctions de similarité

</div>

<table border="1"><tr><td>Attribute</td><td>Similarity function</td></tr><tr><td>PdM Function</td><td>Symbole(Ontologie)</td></tr><tr><td>Maintainable item</td><td>Chaîne(Levenshtein)</td></tr><tr><td>Maintainable item type</td><td>Symbole(égalité)</td></tr><tr><td>Condition Data</td><td>Symbole(Ontologie)</td></tr><tr><td>Condition Data Type</td><td>Symbole(égalité)</td></tr><tr><td>Module synchronization</td><td>Symbole(égalité)</td></tr><tr><td>PdM Article Publication Year</td><td>Entier(fonction définie par des points)</td></tr></table>

## D.6 Développer un cadre pour la sélection de modèles de maintenance predictive

Une étape commune dans le développement de l'architecture des systèmes concerne l'architecture logique. L'architecture logique fournit autant de détails que possible tout en conservant les composants génériques. Ces composants génériques doivent être remplacés par des composants spécifiques créant ainsi l'architecture physique du système. Pour la sélection des composants, il est possible d'appliquer la créativité structurée. La créativité structurée dans l'architecture logique est basée sur l'analyse des combinaisons possibles des différents composants physiques/informatifs qui peuvent être sélectionnés pour répondre à chaque

composante logique. Cela permet d'explorer l'espace des solutions et peut aider l'architecte à identifier des solutions innovantes pour un nouveau système. Si plusieurs solutions possibles sont identifiées, une analyse de compromis peut être nécessaire pour sélectionner la plus appropriée. L'architecture choisie sert de base à la conception détaillée des systèmes. Les connaissances acquises grâce au nouveau système mis en œuvre peuvent être utilisées par l'architecte pour développer de futurs systèmes. Il existe une analogie entre le travail de créativité structuré effectué par l'architecte pour sélectionner les composants appropriés pour répondre à l'architecture logique et les quatre phases du raisonnement basé aux cas : récupérer, réutiliser, réviser et conserver. Une représentation graphique de cette analogie est présentée à la Figure D.8 (en notation Capella [Roq18]). L'analogie proposée relie la phase de récupération CBR à la recherche de l'architecte dans les systèmes précédents connexes qui peuvent servir d'inspiration pour le développement du nouveau système.

- La phase de réutilisation du CBR serait l'affectation des composants identifiés pour se conformer à la nouvelle architecture du système.

- La phase d'examen CBR commencerait par l'analyse de compensation effectuée par l'architecte pour identifier les composants les plus appropriés. Cette phase se poursuit jusqu'à la vérification et la validation du système mis en œuvre, qui sont généralement réalisées par des acteurs autres que l'architecte.

- Après la validation du nouveau système, l'architecte peut conserver les enregistrements qui seront utilisés à l'avenir ; ce serait la phase de rétention CBR.

Cette analogie est générique en termes du système que l'architecte va développer. Toutes les activités sont effectuées « manuellement » par l'architecte et les enregistrements des expériences précédentes peuvent ne pas être structurés pour faciliter leur réutilisation. Cette approche manuelle peut fonctionner lorsque le nombre d'expériences précédentes est limité afin que l'espace de solution à explorer par l'architecte reste gérable. Lorsque le nombre d'expériences précédentes est élevé ou que les exigences sont complexes, la sélection des composants les plus adaptés peut ne pas être facile. Reprendre connaissance d'un nombre important d'architectures plus anciennes peut prendre du temps et des options importantes peuvent être perdues.

Compte tenu de cette analogie entre la CBR et le travail de créativité structure, différents algorithmes peuvent être proposés pour accompagner l'architecte dans les différentes phases du travail architectural. Dans une première étape, la recherche actuelle s'est concentrée sur le développement d'un système d'aide à la décision (DSS) capable de rechercher et de recommander des composants physiques / informationnels appropriés. Cela peut aider l'architecte à gagner du temps dans la phase de conception, et permet une analyse plus large effectuée par des machines, analyses qui peuvent difficilement être approchées par l'homme.

La Figure D.9 présente un concept de DSS et comment il s'intègre dans l'analogie présentée à la Figure D.8. Ce concept est composé de trois parties principales : la base de données «le case base », le moteur de recherche et l'ontologie spécifique au domaine. La base de données de cas stocke les cas passés dans un format structuré pour une réutilisation facile. L'architecte présentera les informations du nouveau système en cours de développement au moteur de récupération et récupérerra, dans le case base, un ensemble de cas les plus similaires qui servira d'inspiration lors de la sélection des composants appropriés pour l'architecture logique.

Au sein de cette structure, l'ontologie joue un rôle essentiel. Les cas, les attributs de ces cas et les similitudes entre les différentes variables textuelles sont souvent décrits en langage naturel. Modéliser ce langage naturel et le rendre lisible par machine est nécessaire pour automatiser la recherche de cas. L'intégration de l'ontologie proposée et du module de récupération CBR est expliquée plus en détail dans


> **Figure Description:**

This diagram illustrates a software or systems engineering process involving an Architect and a team of Design, implementation, verification, and validation engineers, centered around the reuse of historical knowledge. The process begins at the top with the Architect, who performs the task "Develop concept phase until a generic logical architecture." An arrow labeled "Generic logical architecture (New Problem)" leads to the next step, "Search posible components from previous experiences (Retrieval Phase)." This step receives input from a box on the left labeled "Historical records of previous experiences," which contains the task "Store knowledge from previous experiences." The retrieval step outputs "Logical components" and leads to the "Allocate posible components to logical architecture (Reuse phase)" step, which also receives "Identified suitable components" from the historical records box.

From the allocation step, an arrow labeled "Possible physical architectures" leads to "Trade-off analysis on the architecture possibilities (start of the revise phase)." This step outputs a "Selected architecture" arrow that points downward to the second swimlane, labeled "Design, implementation, verification and validation engineers." Within this lower section, the process flows to "Design and implement the system," which then outputs an "Implemented system" arrow leading to "Verify and validate system (end of revise phase)." 

The verification and validation step sends "Information from implemented system" back to the "Keep records from the validated system (retain phase)" task, which is located within the Architect's swimlane. This task then sends a "New record from the validated system" back to the "Store knowledge from previous experiences" box, completing the feedback loop. Each process step is represented by a yellow rectangular box containing a small circular icon with the letters "DR," and the flow between steps is marked with small arrow icons labeled with the nature of the data or artifacts being transferred.



<div align="center">

Figure. D.8: Analogie entre le raisonnement basé au cas et les tâches effectuées par un concepteur de systèmes, en notation Capella [Roq18]

</div>

une enquête complémentaire présentée à l'annexe B. La section suivante traite de la validation du DSS proposé et de la discussion des résultats obtenus.


> **Figure Description:**

This diagram illustrates a Case-Based Reasoning (CBR) retrieval system and its interaction with an architect and engineering team. On the left, a "Retrieval System Manager" maintains the case base, including the retain phase of CBR, and sends a "New case" to the "CBR Retrieval System." The CBR Retrieval System contains a "Casebase" (which stores cases), a "Retrieve engine" (which retrieves suitable models from previous experiences), and an "Ontology Model" (which provides a terminology framework). The "Retrieve engine" receives "Previous cases" from the "Casebase" and "Terms, definitions, similarities" from the "Ontology Model," while the "Ontology Model" provides "Terms, definitions, relations" back to the "Casebase."

On the right, an "Architec" provides "attributes of the current problem" to the "Retrieve engine" and receives "Suitable Models" in return. The architect then follows a workflow: "Develop concept phase until logical architecture," which leads to "Allocate models to logical components (Reuse Phase of CBR)," and finally "Architecture trade-off (start of the revise phase of CBR)." These steps are connected by arrows labeled "Logical architecture" and "Architecture posibilites."

At the bottom, "Design, implementation, verification and validation engineers" receive the "Selected system architecture" to "Design and implement system." This leads to "Verification and validation (end of the revise phase of CBR)," which then sends a "Verified and validated architecture (revised solution)" back to the "Retrieval System Manager." The "Design and implement system" and "Verification and validation" steps are connected by an arrow labeled "Implemented system." All major functional blocks are represented as rectangles containing specific tasks, with arrows indicating the flow of information and system components between the actors and the CBR system.



<div align="center">

Figure. D.9: Idée conceptuelle d'incorporation de DSS pour la sélection des composants du système

</div>

## D.7 Validation et discussion des résultats

La validation du DSS est divisée en deux parties : une validation croisée pour confirmer la cohérence du DSS et une mise en œuvre d'un modèle suggéré dans une étude de cas pour tester les recommandations du DSS dans un exemple pratique.

## D.7.1 Validation croisée

La validation croisée est une technique qui peut être utilisée pour tester l'efficacité de modèles d'intelligence artificielle entraînés. Pour l'approche actuelle, une approche fractionnée de données de test et d'apprentissage est retenue pour effectuer une validation croisée. Pour l'ensemble de données, 63 des 263 cas dans le « case base » ont été tirés au sort pour les tests, laissant le reste comme ensemble d'apprentissage. Pour chacun des 63 cas tiré au sort, les attributs du problème ont été présentés au DSS à l'aide de l'interface graphique. Puis, l'attention s'est portée sur les 10 cas les plus similaires lors de la récupération. La Figure D.10 montre l'exemple d'un test de récupération dans lequel tous les attributs de problème dans le cas cible correspondent aux mêmes attributs dans le cas 35. Cette correspondance complète entre les attributs entraîne une similarité globale de 1.


> **Figure Description:**

Software interface screenshot.

The image displays a graphical user interface titled "Predictive maintenance with CBR method - GUI 2." The interface is divided into sections for "Input variables" and "Additional inputs," with a corresponding "Variable weights" column. Under "Input variables," the following fields are set with a weight of 1.0: "PdM function" is set to "Remaining useful life estimation," "Maintainable item type" is set to "Rotary machines," "Maintainable item" is set to "Rolling bearings," "Condition data type" is set to "Vibrations," "Module sychonization" is set to "Off-line," and "Condition data" is set to "Time series." The "Additional inputs" section specifies "Number of cases to retrieve" as 10 and "Aggregation function to use" as "euclidean."

Below these inputs, a "User dialog" box displays the message: "I found Case35 with a similarity of 1.000 as the best match. The 10 best cases shown in a table:". The table contains two columns, "Case" and "Description." The first row of the table shows "Case35" with "Sim = 1.000" in the first column. The second column contains the following details: "Reference, Similarity and Input variables," "Reference: 35," "Task: Remaining useful life estimation," "Case study type: Rotary machines," "Case study: Rolling bearings," "Online/Off-line: Off-line," "Input for the model: Time series," "Models: Convolutional Neural Network," "Input type: Vibrations," "Publication Year: 2018," and "Publication identifier: DOI: 10.1109/ACCESS.2018.2804930." At the bottom of the interface, there is a button labeled "SUBMIT QUERY."



<div align="center">

Figure. D.10: Exemple de reprise de dossier à l'aide de l'interface DSS

</div>

L'espace de solution des modèles de maintenance prédictive peut être divisé en deux groupes comme expliqué dans [Mon+20]. Le premier groupe est composé d'approches à modèle unique, divisées en trois catégories principales : les modèles basés sur la connaissance, les modèles basés sur les données et les modèles basés sur la physique. Le deuxième groupe est constitué d'approches multi-modèles, dans lesquelles au moins deux modèles de l'une des trois catégories mentionnées sont combinés pour réaliser une fonction spécifique du système de maintenance prédictive. La maintenance prédictive est composée de tâches de diagnostic et de pronostic. Selon la revue de la littérature [Mon+20], les tâches de diagnostic telles que la détection des défauts, l'identification des défauts et la modélisation de l'état de santé peuvent être abordées par des modèles des trois catégories d'approches à modèle unique ou d'approches multi-modèles. En revanche, pour les tâches de prédiction, il est difficile de trouver des modèles basés sur les connaissances. Par exemple, les fonctions de prédiction, telles que l'estimation de la durée de vie utile restante et les fonctions de prévision de l'état suivant, sont généralement réalisées par des modèles basés sur la physique, des modèles basés sur les données et des approches multi-modèles qui combinent des modèles basés sur la physique et des données. La validation croisée du DSS a confirmé ce comportement. Les récupérations pour les tâches de diagnostic ont proposé des solutions à modèle unique et multi-modèles en tenant compte des modèles des trois catégories. Les récupérations pour les prévisions proposaient également des solutions à un ou plusieurs modèles, mais les modèles proposés ne provenient que de catégories physiques et axées sur les données. Cela permet de confirmer que l'espace de solution est bien couvert.

Pour chaque cas de test, les cas récupérés sont classés en fonction de la similitude des attributs du problème. Pour certains des tests, plusieurs cas récupérés avaient la même valeur de similarité maximale et/ou proposaient le même modèle pour réaliser une fonction PdM spécifique. Du point de vue de l'ingénierie des systèmes, cela représente deux limitations. La première fait référence à au moins deux cas avec la même similarité maximale car aucune information supplémentaire n'est fournie pour effectuer l'analyse de compromis pour sélectionné le composant le plus approprié. La seconde limitation est liée à la diversité des cas récupérés, en particulier lorsque deux cas ou plus suggèrent que le même modèle réalise une fonction spécifique. Un architecte en quête d'inspiration pour développer des solutions innovantes aura besoin que le DSS propose un ensemble diversifié de modèles. Ce sont des points d'amélioration à considérer à l'avenir pour le DSS. Une analyse plus détaillée peut également être effectuée qui inclut l'effort d'adapter la solution d'un cas récupéré au cas cible. Cela peut aider à effectuer une analyse de compromis sur les options rappelées et par conséquent à améliorer les performances du DSS.

## D.7.2 Implementation d'un cas d'étude pratique

Dans le cadre de la validation, un exemple de mise en œuvre a été développé à partir des suggestions DSS dans l'étude de cas. L'étude de cas consiste en un ensemble de données de moteurs d'avion [Cha+21]. L'ensemble de données contient les enregistrements de dysfonctionnements de 128 moteurs d'avion dans des conditions de vol réelles et a été généré avec le modèle Commercial Modular Aero-Propulsion System Simulation (CMAPSS) développé par la NASA. Ces données sont appelées l'ensemble de données N-CMAPSS. Le but n'est pas seulement de tester les capacités du système CBR activé par l'ontologie (le DSS), mais aussi d'identifier les points d'amélioration pour le DSS. L'objectif de cette validation est de mettre en œuvre l'un des modèles proposés par le DSS pour remplir une fonction de maintenance prédictive pour la base de données N-CMAPSS. Cette implémentation permet de démontrer que DSS est capable de suggérer des composants appropriés pour les systèmes de maintenance prédictive, en complément de la validation croisée.

Afin de mieux valider les recommandations du DSS, l'un des modèles proposés a été pris en exemple et appliqué pour remplir la fonction de maintenance prédictive correspondante. Le DSS recommande la SOM et la régression logistique pour la modélisation de la santé comme les modèles les plus appropriés (similarité égale à 0,879) pour l'étude de cas N-CMAPSS. Construisant sur l'expérience de l'équipe de recherche en cartes d'auto-organisation (SOM), une implémentation du volet modélisation de la santé des moteurs est réalisée à l'aide d'un SOM. La section suivante fournit des explications supplémentaires sur l'implication de l'échantillon SOM et ses résultats préliminaires.

La méthodologie pour mettre en œuvre les cartes d'auto-organisation (SOM) pour la modélisation de la santé a été adoptée à partir de [Sch+20], (voir également l'annexe A). Les cartes auto-organisées sont des réseaux de neurones artificiels avec un entraînement non-supervisé qui sont capables de regrouper des instances de données en fonction des attributs d'instance. Un SOM est normalement constitué d'une couche carrée de neurones et les différents groupes après l'entraînement SOM peuvent être représentés graphiquement sur des cartes comme des régions bien définies. Il a été utilisé avec succès pour modéliser le processus de dégradation de différentes machines telles que les moteurs à réaction [MV18]. Dans ces cas, les neurones représentent la santé ou la dégradation de la machine dans un mode de fonctionnement spécifique. Le SOM entraîné aura une seule région, mais une transition du blanc (état optimal) au noir (état d'échec). Lors de l'évaluation de la santé ou de la dégradation d'une machine à l'aide du SOM entraîné, un neurone s'affichera sur la carte indiquant à quel point la dégradation est avancée ou à quel point la santé a diminué. C'est le véritable objectif de l'implémentation actuelle : obtenir un SOM entraîné capable de montrer une transition de l'état optimal à l'état défaillant. La Figure D.11 montre la carte auto-organisatrice entraînée avec le N-CMAPSS. Le résultat correspond au comportement attendu. Les différents modèles de dégradation ont été disposés sur la carte.


> **Figure Description:**

The image is a heatmap titled "Dataset" that displays a 5x5 grid of values represented by varying shades of red, where lighter shades indicate lower values and darker shades indicate higher values. The x-axis and y-axis are both labeled with integers from 0 to 4. The grid is organized such that the values generally increase as both the x and y coordinates increase, with the highest values concentrated in the upper-right corner (at coordinates (4,4)) and the lowest values concentrated in the lower-left corner (at coordinates (0,0)). The color intensity transitions smoothly from a very pale pink at the bottom-left to a deep, dark red at the top-right.



<div align="center">

Figure. D.11: Carte auto-organisatrice formée avec l'étude de cas N-CMAPSS

</div>

Il est important de se rappeler que la validation d'un système d'aide à la décision (DSS) est une tâche difficile. La validation du SOM pour modéliser la santé du N-CMAPSS peut être utilisée pour valider indirectement le DSS ; cependant, il est important de souligner que d'autres implémentations seraient nécessaires pour confirmer les capacités et la précision du DSS proposé pour la sélection des modèles de maintenance prédictive. Dans l'implémentation actuelle, le N-CMPASS représente le cas cible pour lequel un nouveau système de maintenance prédictive doit être développé. Le système de recommandation CBR avec ontologie (également appelé DSS dans ce manuscrit) a proposé différents modèles pour remplir chaque fonction de maintenance prédictive. L'un des modèles proposés par le DSS pour modéliser la fonction de santé était la carte d'auto-organisation (SOM). La mise en œuvre du SOM a montré avec succès la tendance à la dégradation des moteurs à réaction, du fonctionnement nominal à l'état de défaillance en utilisant un sous-ensemble du N-CMPASS. Le SOM entraîné peut également être utilisé pour évaluer la santé/la dégradation d'un autre moteur du même type et dans les mêmes conditions de fonctionnement. Il est important de préciser que cette validation vise à démontrer la pertinence du modèle proposé par le DSS, mais davantage de comparaisons entre les modèles proposés sont nécessaires pour déterminer le meilleur modèle.

## D.8 Conclusion et perspectives de travaux futurs

## D.8.1 Résumé des contributions

Cette thèse comprend quatre articles qui ont été publiés ou acceptés pour publication dans des 2 revues scientifiques avec comité de relecture et 2 conférences internationales avec comité de relecture. Les principales contributions ont été regroupées dans les articles comme suit :

1. L'article de revue bibliographique résumait l'état de l'art en matière de diagnostics et de pronostics. Une proposition a été avancée pour différencier les modèles hybrides des approches multi-modèles.

Des tendances vers des approches multi-modèles ont été notées. Au moment de la rédaction de ce manuscrit, l'article de synthèse a été cité plus de vingt fois.

2. L'approche d'ingénierie des systèmes pour la conception de systèmes de maintenance prédictive propose, contrairement aux architectures génériques existantes, une approche systématique passant par une étape conceptuelle des systèmes de maintenance prédictive à partir des besoins et souhaits initiaux et ceci jusqu'à l'architecture logique. Cela permet d'aider l'architecte à déterminer les composants du système et à maintenir la traçabilité des besoins et souhaits initiaux des parties prenantes. Ces résultats ont été publiés dans une contribution de conférence à une conférence internationale.

3. Même si les ontologies n'étaient pas le domaine initial de ce projet de recherche, leur étude s'avérait nécessaire et ce travail de recherche a produit ses propres résultats. La création d'OMSSA, un modèle d'ontologie pour la sélection et l'évaluation des stratégies de maintenance, fournit un cadre terminologique qui peut être utilisé par des agents intelligents pour automatiser des tâches complexes de gestion de stratégies de maintenance. Une extension à OMSSA (OPMAD) est l'ontologie utilisée pour créer le « case base » et les mesures de similarité DSS pour la sélection des composants de maintenance prédictive. Le travail de recherche effectué dans la création de l'OMSSA a été consolidé dans un article de revue, actuellement accepté pour publication.

4. Un système d'aide à la décision (DSS) capable de consulter des cas réussis de mise en œuvre d'un système de maintenance prédictive peut aider un architecte système à sélectionner des modèles de maintenance prédictive appropriés pour effectuer des tâches de diagnostic et de prévision. Les premiers résultats de cette recherche ont été publiés dans une contribution de conférence à une conférence internationale.

## D.8.2 Perspectives de travaux futurs

Pendant ce projet de recherche, il n'a pas été possible d'expliquer et de prouver tout. Il est donc important de mettre les choses en perspective pour repérer les axes d'amélioration et les lister comme perspectives de travaux futurs. Les perspectives de travaux futurs sont organisées en trois grands groupes :

1. Perspectives liées à l'approche d'ingénierie systèmes pour la conception de systèmes de maintenance prédictive

2. Perspectives pour OMSSA et OPMAD

3. Perspectives pour le DSS basé sur le raisonnement à base des cas

## D.8.2.1 Perspectives liées à l'approche d'ingénierie systèmes pour la conception de systèmes de maintenance prédictive

- Affiner la liste des besoins, des souhaits et des exigences du système de maintenance prédictive : après la publication de l'article relatif à l'étape conceptuelle des systèmes de maintenance prédictive, plusieurs besoins, souhaits et exigences ont été identifiés qui n'avaient pas été initialement pris en compte. La liste des besoins, des souhaits et des exigences possibles pour les nouveaux systèmes de maintenance prédictive peut être améliorée. Ces listes peuvent être stockées dans des bases de données qui peuvent être utilisées par des agents intelligents automatisés pour aider les ingénieurs à évaluer les besoins et les souhaits initiaux d'un système de maintenance prédictive et à suggérer les exigences correspondantes des parties intéressées. Un DSS pourrait être mis au point pour définir les besoins des parties prénantes en fonction des besoins initiaux et des souhaits du nouveau système de maintenance prédictive.

- Inclure la technique phase des « trade-offs » dans le cadre systématique proposé : Les analyses de trade-off sont présentes à divers moments de la phase conceptuelle. L'intégration d'un outil d'analyse de trade-off (compromis) peut aider à améliorer le DSS et faciliter la sélection des composants de l'architecture.

- Inclure la formalisation des exigences système : un aspect important d'une approche d'ingénierie système consiste à obtenir les exigences système. Même lorsque la création de ces exigences est en théorie avant le processus d'architecture, en pratique, ces exigences sont généralement établies en parallèle avec le développement de l'architecture du système ou même à la fin, lorsque toutes les capacités des différents composants logiques sont connues. Ces exigences sont importantes pour la phase de conception détaillée. L'obtention de ces exigences sortait du cadre de la recherche actuelle, mais constitue un sujet complémentaire intéressant pour les recherches futures.

## D.8.2.2 Perspectives pour OMSSA et OPMAD

- Affiner les classes et les relations : le développement d'ontologies est un sujet en constante évolution. Il existe plusieurs initiatives pour fournir des ontologies de niveau supérieur et intermédiaire dans différents domaines. Le domaine industriel ne fait pas exception. Des travaux supplémentaires seront nécessaires pour aligner OMSSA et OPMAD sur ces ontologies normalisées afin de favoriser leur intégration et leur réutilisation dans d'autres applications. Ce travail comprend l'affinement des classes et les relations entre elles.

- Extension du raisonnement en ontologie : OMSSA et OPMAD ont été utiles dans la recherche actuelle, mais en tant qu'ontologies, ils ont été sous-utilisés. Les ontologies ont diverses capacités qui n'ont pas été exploitées. L'une d'elles est la mise en œuvre de règles sémantiques. Cela élargit les options de raisonnement et peut être utilisé comme moyen complémentaire au système CBR.

## D.8.2.3 Perspectives pour le DSS basé sur le raisonnement à base des cas

- Étendre l'utilisation de l'ontologie pour des fonctions de similarité plus locales : l'ontologie a été utile mais sous-utilisée. Certaines autres mesures de similarité qui ont été attribuées à une mesure de similarité de symboles binaires peuvent être réorganisées pour utiliser des similarités basées sur des ontologies.

- Utiliser l'ontologie pour estimer les poids pour le calcul de similarité globale : l'ontologie peut également être utilisée pour calculer les poids de chaque similarité locale lors du calcul de la similarité globale. Dans la première tentative de calcul de similitude globale effectuée dans cette enquête, toutes les similitudes locales ont reçu le même poids. Une amélioration du calcul de la similarité globale pourrait être de donner un rang d'importance à chaque similarité locale. Les poids peuvent être calculés à l'aide de l'ontologie peuplée.

- Étendre le système d'aide à la décision en développement d'autres phases du cycle de CBR, telles que la phase d'adaptation : la portée du DSS était dans la phase de reprise du cycle de CBR. Le système peut être étendu pour faciliter la phase d'adaptation des composants proposés pour le nouveau système de maintenance prédictive. Cette extension peut également inclure l'analyse de la compensation des différentes composantes suggérées par le DSS. Les résultats de la recherche actuelle ont montré plusieurs opportunités d'amélioration qui devraient être abordées à l'avenir avant la mise en œuvre éventuelle du DSS.

- Affiner le processus d'instanciation pour éviter les problèmes de diversité mais en gardant tout l'espace de solution couvert : l'instanciation du "case base" doit être affinée. Une opportunité d'amélioration

peut être de diviser l'espace de solution par les différentes fonctions de maintenance prédictive et de s'assurer que l'espace de solution est entièrement couvert par chacune d'entre elles. Des cas généralisés pour chaque fonction de maintenance prédictive peuvent résoudre le problème de diversité dans les cas de récupération.

- Analyse de compromis pour mieux sélectionner la technique parmi les propositions : comme pour le DSS, l'analyse des trade-offs peut aider l'architecte à discriminer entre les composants proposés par le DSS. Lors de la validation, il a été mentionné que parfois le DSS suggérait deux composants différents avec la même similitude. L'ajout d'attributs supplémentaires en tant qu'indicateurs de performance peut aider l'architecte à prendre la bonne décision pour son problème.

## Summary in Spanish / Resumen en Español

## Contenido

Intenido

E.1 Introducción . . . . .

## E.1 Introducción

## E.1.1 Mantenimiento predictivo

Mantenimiento predictivo es una estrategia de mantenimiento que tiene como objetivo determinar el momento preciso para realizar las acciones de mantenimiento. No muy antes porque las acciones de mantenimiento podrían provocar el cambio de piezas que aún tienen una vida útil importante, lo que representa costos para las compañías; pero no muy tarde porque una falla inesperada puede ocurrir trayendo consigo una serie de consecuencias negativas. Mantenimiento predictivo es una alternativa a otras estrategias tradicionales de mantenimiento, como lo son mantenimiento correctivo y preventivo. En lugar de esperar a que una falla ocurra o realizar mantenimientos basados en intervalos fijos de operación, mantenimiento predictivo se basa en el diagnóstico del estado actual de los equipos y en el pronóstico de cuando una eventual falla podría ocurrir.

Mantenimiento predictivo está fuertemente relacionado con Mantenimiento Basado en Condición (CBM por sus siglas en inglés) y Administración de la Salud basado en Pronósticos (PHM por sus siglas en inglés). Tanto mantenimiento predictivo como estas dos disciplinas abarcan los diagnósticos y pronósticos para mantenimiento; en algunas ocasiones estos términos son incluso utilizados como sinónimos. Aparentemente, los términos de mantenimiento predictivo y CBM aparecieron en la década de 1940. Ambos términos se refieren a la estrategia de mantenimiento que pretende anticipar los fallos de las máquinas en función de su condición. Sin embargo, no es hasta principios de los años noventa cuando esta estrategia adquiere importancia gracias a la implantación de sistemas de monitorización y herramientas computacionales capaces de continuar con las tareas de diagnóstico. En cuanto al pronóstico, incluso cuando se menciona en el mantenimiento predictivo y CBM, siempre fue una disciplina inexacta. A principios de la década del 2000, la disciplina de PHM surgió con el objetivo de cubrir la brecha en investigación en pronósticos para mantenimiento predictivo. Desde entonces, la investigación en diagnóstico y pronóstico para el mantenimiento ha ganado mucha atención de la academia y la industria; gracias a los continuos incrementos en poder computacional y dados los beneficios de su implementación. En la última década, se han hecho diferentes contribuciones bajo los diferentes términos (mantenimiento predictivo, CBM y PHM) y se refieren al mismo campo de investigación.

## E.1.2 Idea conceptual y arquitectura de un sistema

Según el manual de INCOSE [INC15], el ciclo de vida de un sistema puede dividirse en seis etapas genéricas (véase la Figura E.1). El ciclo de vida del sistema comienza con la etapa conceptual, cuyo objetivo es explorar posibles soluciones para satisfacer las necesidades iniciales de las partes interesadas. La fase conceptual va seguida de la fase de desarrollo, en la que se realiza un diseño detallado de los componentes del sistema y sus interfaces. Después del diseño detallado, comienza la etapa de producción que está dedicada a la implementación del sistema, lo que significa la fabricación, codificación, creación de los diferentes componentes y su integración final en el sistema. La verificación y validación del sistema forman parte de la fase de producción. Una vez validated el sistema, se entrega al cliente para su etapa de utilización. En la etapa de utilización, el sistema cumple la función para la que fue creado. La etapa de mantenimiento va en paralelo a la etapa de utilización durante el funcionamiento del sistema. Esta etapa de mantenimiento tiene como objetivo asegurar el estado de funcionamiento óptimo del sistema. Al final del ciclo de vida del sistema, la fase de eliminación tiene como objetivo gestionar adecuadamente los residuos del sistema cuando se retira de la operación.

El proceso de arquitectura del sistema tiene lugar dentro de la etapa conceptual. La etapa conceptual comienza por reunir todas las necesidades y deseos de las partes interesadas y formalizarlos en los requisitos

<table border="1"><tr><td rowspan="2">Concept stage</td><td rowspan="2">Development stage</td><td rowspan="2">Production stage</td><td>Utilization stage</td><td rowspan="2">Retirement State</td></tr><tr><td>Support stage</td></tr></table>

<div align="center">

Figura. E.1: Etapas genéricas del ciclo de vida de un Sistema (en inglés) [INC15]

</div>

de las partes interesadas. Estos requisitos se utilizan luego para la creación de la arquitectura del sistema que servirá de base para el diseño detallado y la implementación del sistema. El desarrollo de la arquitectura se puede dividir en tres niveles [Roq18]; [INC15]: arquitectura funcional, arquitectura lógica y arquitectura física. La arquitectura funcional describe cómo las diferentes subfunciones de un sistema interactúan entre sí para cumplir un objetivo específico, pero no proporciona ningún detalle sobre los componentes que cumplen cada subfunción. La arquitectura lógica proporciona tanto detalle como sea posible de los componentes de la arquitectura y sus interfaces, pero no involucra a ninguna tecnología específica, lo que significa que la arquitectura lógica muestra componentes genéricos. La arquitectura física proporciona los detalles de las tecnologías que se asignarán para cada componente lógico. La unión de estos tres niveles de la arquitectura puede ser llamada como la arquitectura del sistema y puede entonces ser definida como los "conceptos fundamentales o propiedades de un sistema en su entorno encarnado en sus elementos, relaciones, y en los principios de su diseño y evolución" [ISO11]. En palabras simples, la arquitectura de un sistema muestra el cómo un conjunto de elementos, que podrían ser físicos o informativos, se organizan para cumplir un objetivo específico.

## E.1.3 Declaración de investigación

El mantenimiento predictivo se lleva a cabo mediante sistemas especializados para realizar tareas de diagnóstico y pronóstico, para determinar el momento adecuado para desencadenar acciones de mantenimiento. El diseño y desarrollo de estos sistemas especializados sigue basándose en prueba y error. Existen varias arquitecturas genéricas en normas y estándares, como por ejemplo [MIM01], pero el diseño de un nuevo sistema de mantenimiento predictivo comienza mucho antes, en la etapa conceptual. Una arquitectura genérica no proporciona un vínculo con las necesidades y deseos iniciales de un nuevo sistema de mantenimiento predictivo y, a menudo, estas necesidades y deseos no se satisfacen con una arquitectura genérica. Además, una arquitectura genérica no proporciona ninguna guía para seleccionar las tecnologías adecuadas que puedan cumplir los componentes genéricos que propone [MV19].

El mantenimiento predictivo aborda tareas de diagnóstico y pronóstico, pero no todos los sistemas predictivos cubren las mismas funciones. Por ejemplo, un nuevo sistema de mantenimiento predictivo puede estar destinado a realizar diagnósticos en diferentes componentes de un sistema y se necesitarán varios módulos de diagnóstico del mismo tipo y no se incluirán módulos de pronóstico. Las arquitecturas genéricas no proporcionan un enfoque sistemático para diseños que sólo necesitan un subconjunto de los componentes genéricos propuestos o cuando se necesitan varios componentes del mismo tipo.

Existe un número importante de opciones para cumplir con las funciones de diagnóstico y pronóstico en un sistema de mantenimiento predictivo, y no hay directrices para ayudar al arquitecto a seleccionar los modelos, técnicas o algoritmos adecuados que pueden llevar a cabo estas funciones. La exploración del espacio de solución para determinar los componentes adecuados puede entonces ser compleja y de larga duración. Esta tesis tiene como objetivo facilitar el proceso de arquitectura de los sistemas de mantenimiento predictivo al permitir una manera más eficiente de explorar el espacio de solución y proponer los componentes más adecuados para la arquitectura del sistema. Antes de profundizar en el diseño de sistemas de mantenimiento predictivo, es importante entender el campo de investigación del mantenimiento predictivo en sí y las diferentes opciones disponibles para realizar diagnósticos y pronósticos. Se proponen

las siguientes preguntas de investigación para orientar el estudio del estado del arte en este tema:

1. ¿Cuáles son las tendencias actuales en diagnóstico y pronóstico en mantenimiento predictivo?

2. ¿Qué tipo de modelos, técnicas o métodos se utilizan para abordar el diagnóstico y el pronóstico en el mantenimiento predictivo?

3. ¿Cuáles son los principales desafíos que enfrenta el mantenimiento predictivo en el diagnóstico y el pronóstico?

Después del estudio de vanguardia, las preguntas de investigación se adaptan de acuerdo con los resultados del estudio y la motivación inicial de esta investigación relacionada con el diseño de sistemas de mantenimiento predictivo (ver sección E.2)

## E.1.4 Organización del resumen

La sección E.2 aborda el estado del arte del mantenimiento predictivo basado en las preguntas iniciales de investigación introducidas en este capítulo. Esta sección está relacionada con el capítulo 2 de la tesis que se compone de un artículo publicado que incluye las tendencias actuales en modelos para diagnósticos y pronósticos en el campo del mantenimiento. La sección termina refinando las preguntas de investigación que motivaron el resto de la investigación.

La sección E.3 propone enfoque de ingeniería de sistemas para el diseño de mantenimiento predictivo, específicamente en la etapa conceptual desde la reunión de las necesidades y deseos iniciales de las partes interesadas hasta la propuesta de una arquitectura lógica. Esta sección está relacionada con el capítulo 3 de la tesis que se compone de un artículo publicado en la conferencia y termina presentando la selección del componente de mantenimiento predictivo como el principal desafío que se abordará en los siguientes capítulos. Se propone un Sistema de Apoyo a las Decisiones (DSS por sus siglas en inglés) que combina ontologías y razonamiento basado en casos como posible solución para abordar la selección de componentes en el enfoque sistemático.

La sección E.4 explica uno de los elementos básicos del Sistema de Apoyo a las Decisiones: las ontologías. La investigación complementaria se ha realizado específicamente en ontologías que han resultado en un artículo de una revista, aceptado para su publicación en el momento en que este manuscrito fue escrito. El fondo teórico de las ontologías se presenta destacando su importancia en la comunidad de investigación debido a sus capacidades para modelar formalmente el vocabulario de un dominio en específico y realizar razonamiento con él. La sección E.4 explica el desarrollo de la ontología que más tarde se utiliza en el DSS para la selección de componentes. . Esta sección está relacionada con el capítulo 4 de la tesis que incluye un artículo aceptado para publicación que trata de un modelo ontológico para la selección y evaluación de estrategias de mantenimiento (OMSSA por sus siglas en inglés).

La sección E.5 explica el segundo pilar del DSS: Razonamiento basado en casos (CBR). Los principios del paradigma CBR se introdujeron incluyendo las fases del ciclo CBR. En un primer intento, el DSS se centra en la fase de recuperación de CBR. Se proporciona una explicación de la implementación del motor de recuperación de CBR utilizando código de fuente abierta.

La sección E.6 explica el marco general de la integración de los componentes básicos del DSS y cómo encaja en el enfoque sistemático para diseñar sistemas de mantenimiento predictivo. Esta sección está relacionada con el capítulo 6 de la tesis que se compone de un artículo de conferencia publicado que es la continuación del artículo presentado en la sección E.2. La validación cruzada se realiza para demostrar las capacidades del DSS.

La sección E.7 tiene por objeto extender la validación del DSS. Se selecciona un caso de estudio para desarrollar el enfoque completo propuesto en la investigación actual y se implementa un ejemplo de modelo de mantenimiento predictivo para el caso de estudio basado en las sugerencias del DSS. Se explican y analizan los resultados de esta implementación.

En la sección E.8 se presentan las conclusiones de los trabajos realizados y se proponen perspectivas para una continuación de esas actividades de investigación en el futuro.

## E.2 Hacia un enfoque multimodelo en mantenimiento predictivo: una revisión literaria sistemática en diagnósticos y pronósticos.

La revisión sistemática de la literatura muestra que el mantenimiento predictivo está ganando importancia en la comunidad académica, especialmente en los últimos 25 años. La Figura E.2 muestra el número de publicaciones que mencionan los términos "mantenimiento predictivo", "mantenimiento basado en condición" y "pronóstico y gestión de la salud" en los últimos 25 años en las fuentes de búsqueda consultadas.


> **Figure Description:**

This bar chart displays the number of publications on three specific terms—Predictive Maintenance, Prognostics and health management, and Condition-based maintenance—from 1995 to 2019. The vertical axis represents the "Number of publications on which therms are found" (sic) ranging from 0 to 300 in increments of 50. The horizontal axis lists each year from 1995 to 2019. The legend identifies the three categories by color: blue for Predictive Maintenance, red for Prognostics and health management, and green for Condition-based maintenance.

For each year, the data is represented as follows: 1995 (Blue: ~8, Red: 0, Green: 0), 1996 (Blue: ~8, Red: 0, Green: 0), 1997 (Blue: ~16, Red: 0, Green: ~12), 1998 (Blue: ~38, Red: 0, Green: ~12), 1999 (Blue: ~40, Red: 0, Green: ~30), 2000 (Blue: ~44, Red: ~5, Green: ~44), 2001 (Blue: ~40, Red: ~8, Green: ~52), 2002 (Blue: ~44, Red: ~5, Green: ~45), 2003 (Blue: ~47, Red: 0, Green: ~40), 2004 (Blue: ~38, Red: ~5, Green: ~47), 2005 (Blue: ~45, Red: ~2, Green: ~44), 2006 (Blue: ~62, Red: ~18, Green: ~95), 2007 (Blue: ~52, Red: ~14, Green: ~76), 2008 (Blue: ~64, Red: ~25, Green: ~90), 2009 (Blue: ~67, Red: ~26, Green: ~118), 2010 (Blue: ~69, Red: ~38, Green: ~120), 2011 (Blue: ~59, Red: ~33, Green: ~120), 2012 (Blue: ~99, Red: ~51, Green: ~195), 2013 (Blue: ~110, Red: ~73, Green: ~163), 2014 (Blue: ~87, Red: ~59, Green: ~182), 2015 (Blue: ~134, Red: ~77, Green: ~218), 2016 (Blue: ~156, Red: ~95, Green: ~222), 2017 (Blue: ~227, Red: ~113, Green: ~267), 2018 (Blue: ~266, Red: ~110, Green: ~243), and 2019 (Blue: ~245, Red: ~130, Green: ~218).



<div align="center">

Figura. E.2: Número de publicaciones relacionadas con mantenimiento predictivo en los últimos 25 años.

</div>

La revisión bibliográfica se dividió en dos partes. En la primera se abordaron revisiones bibliográficas previas sobre el mantenimiento predictivo lo que ayudó a identificar los modelos utilizados para el mantenimiento predictivo y la evolución de las tendencias a lo largo de los años. Las taxonomías utilizadas para clasificar los diferentes modelos de diagnóstico y pronóstico en mantenimiento predictivo muestran ligeras variaciones en la terminología de un estudio a otro. Pueden extraerse dos enfoques principales: los enfoques de un solo modelo y los enfoques de varios modelos. Para los enfoques de un solo modelo se pueden identificar tres familias de modelos; para este estudio estas familias de modelos se denominarán de la siguiente manera: modelos basados en el conocimiento, modelos basados en datos y modelos basados en la física. Los enfoques multimodelo combinan al menos dos modelos de las tres familias de modelos mencionadas. Los enfoques multimodelo pueden tener diferentes configuraciones y a veces son nombrados como modelos híbridos.

La segunda parte de la revisión literaria se dedicó al estudio de las tendencias actuales en los diferentes enfoques de los modelos. La revisión literaria ha mostrado que existe una tendencia en la implementación de enfoques multimodelo ya que un solo modelo difícilmente satisface todas las funciones en un sistema de

mantenimiento predictivo. La Figura E.3 muestra todas las posibilidades de combinar modelos en enfoques multimodelo.


> **Figure Description:**

This diagram illustrates the potential combinations of three primary modeling approaches: Knowledge-based, Data-driven, and Physics-based. The three main categories are represented as rounded rectangles positioned at the vertices of an equilateral triangle. A dashed oval encompasses the entire structure, labeled at the bottom center as "Potential combinations."

At the center of the triangle is a box labeled "KB+DD+PB," which is connected by lines to each of the three main categories. The relationships between the categories are represented by connecting lines and labeled boxes. A line connects "Knowledge-based" to "Data-driven" with a box labeled "KB+DD" on the line. A line connects "Knowledge-based" to "Physics-Based" with a box labeled "KB+PB" on the line. A line connects "Data-driven" to "Physics-Based" with a box labeled "DD-PB" on the line.

Additionally, there are self-referential loops for each category, indicated by curved arrows pointing back to the source box, each accompanied by a label box: "DD-DD" for Data-driven, "KB-KB" for Knowledge-based, and "PB-PB" for Physics-Based. The layout suggests a framework for integrating these three distinct methodologies into various hybrid or singular modeling approaches.



<div align="center">

KB: Knowledge-based model. DD: Data-driven model. PB: Physics-based model.

</div>

<div align="center">

Figura. E.3: Posibles combinaciones de modelos de mantenimiento predictivo.

</div>

La revisión bibliográfica permitió identificar los desafíos actuales para el mantenimiento predictivo:

- La extrapolación de soluciones existentes de mantenimiento predictivo en aplicaciones complejas, incluyendo múltiples componentes y sus fallas asociadas. La mayoría de las aplicaciones identificadas se centraron en un solo componente con un número limitado de fallos. Sin embargo, las aplicaciones de la vida real son frecuentemente sistemas complejos compuestos de muchos componentes y muchas fallas asociadas a cada componente y al propio sistema.

- La falta de un enfoque sistemático para diseñar y desarrollar sistemas de mantenimiento predictivo. Existen estándares, normas y arquitecturas genéricas para desarrollar nuevos sistemas de mante nimiento predictivo, como OSA-CBM. Sin embargo, sólo se centran en los componentes funcionales básicos del sistema y no abarcan aspectos importantes relativos a los indicadores de rendimiento o las limitaciones de contexto del sistema. Además, todavía no ofrecen una explicación consistente sobre qué modelos utilizar en función de las necesidades iniciales del sistema de mantenimiento predictivo. La falta de un enfoque sistemático limita la implementación de sistemas de mantenimiento predictivo en aplicaciones industriales a escala real.

- La fusión de diversas fuentes de datos de monitoreo de condición. Este desafío está relacionado con la extrapolación de los modelos actuales en mantenimiento predictivo a sistemas complejos. Los sistemas técnicos pueden tener diferentes tipos de fuentes de datos, por ejemplo mediciones de sensores, registros de mantenimiento, registros operacionales, documentos de diseño, etc. Se podrían reunir información importante de todas estas fuentes para implementar nuevos sistemas de mantenimiento predictivo.

- La incorporación de datos de influencia externa. El funcionamiento de los sistemas puede variar dependiendo de su contexto operativo. Los cambios en el contexto operativo pueden afectar directamente al rendimiento del sistema y, por consiguiente, a las lecturas del seguimiento sanitario. Puede activar

falsas alarmas sugiriendo la existencia de fallas, o puede impedir la identificacion de fallas existentes. Esto podría abordarse mediante modelos complementarios capaces de incorporar la influencia externa con fines de mantenimiento predictivo.

- Manejo de la incertidumbre. La incertidumbre afecta directamente la precision del diagnóstico y el pronóstico. Puede deberse a los datos recopilados o a las imperfecciones del modelo utilizado para el análisis. Puede afectar la fiabilidad de los resultados. La gestión de la incertidumbre es vital para los sistemas críticos sujetos a las regulaciones de las autoridades. Este es el caso de sistemas críticos como las centrales nucleares y las aeronaves en las que las regulaciones son restrictivas para mantener los estándares de seguridad y evitar eventos catastróficos.

El estudio del estado del arte motivó la mejora de las preguntas de investigación. El resto de la investigación fue impulsado por las siguientes preguntas:

1. ¿Cómo abordar la arquitectura y diseño de sistemas de mantenimiento predictivo?

2. ¿Cómo seleccionar un modelo adecuado o combinación de modelos dado un nuevo problema de mantenimiento predictivo para resolver?

3. ¿Cómo sugerir un enfoque adecuado para una solución de mantenimiento predictivo?

4. ¿Cómo puede un diseñador beneficiarse de la experiencia de los sistemas existentes para desarrollar nuevas soluciones de mantenimiento predictivo?

## E.3 De necesidades y deseos hasta una arquitectura lógica de sistemas de mantenimiento predictivo

La primera pregunta de investigación obtenida al final del estudio del estado del arte es sobre el diseño de nuevos sistemas de mantenimiento predictivo. En la declaración de investigación presentada en la sección D.1 se explicó que el diseño y desarrollo de sistemas de mantenimiento predictivo todavía se basa en prueba y error. A pesar de la existencia de varias arquitecturas genéricas en normas y estándares, como por ejemplo [MIM01], la etapa conceptual de tales sistemas no está totalmente cubierta. Hay una brecha en el desarrollo de tales sistemas desde la recolección de necesidades y deseos para el nuevo sistema hasta la creación de la arquitectura que satisfaga las necesidades y deseos iniciales.

La creación de un nuevo sistema debe comenzar siempre escuchando a aquellos que están relacionados o interesados en el proyecto, conocidos como partes interesadas. Ellos proveen todas las necesidades y deseos para ser cumplidos por un nuevo sistema. Estas necesidades y deseos son la fuente de información para establecer la lista de requisitos de las partes interesadas del nuevo sistema. La investigación actual propone un enfoque de ingeniería de sistemas para cubrir la etapa conceptual de los sistemas de mantenimiento predictivo.

En el gráfico D.4 se muestran las diferentes etapas abordadas en el enfoque propuesto de ingeniería de sistemas. Comienza por reunir las necesidades y deseos iniciales de las partes interesadas. Estas necesidades y deseos se traducen en una lista formal de requisitos de las partes interesadas. Los requerimientos son prioritizados y clasificados en requerimientos funcionales, de desempeño, estructurales y experienciales. Esta clasificación ayudará en la creación de la arquitectura del sistema. Los requisitos funcionales se utilizan para iniciar el proceso de arquitectura, específicamente para realizar el análisis funcional y crear el funcional. La arquitectura funcional se utiliza entonces para desarrollar la arquitectura lógica que sigue


> **Figure Description:**

This diagram illustrates a sequential process for developing a predictive maintenance system, represented by a series of yellow rounded-rectangular process blocks connected by downward-pointing arrows. The process begins with the block "Gather needs and desires for a new predictive maintenance system," which produces an output labeled "Needs and desires for the new predictive maintenance system." This leads to the second block, "Formalize stakeholder requirements," which outputs "Formal stakeholder requirements." The third block is "Classify and prioritize requirements," which produces "Functional requirements" leading to the next step, and also has a side-branch arrow leading directly to the final block.

Following the main path, the "Functional requirements" lead to the block "Perform Functional Analysis," which outputs "Functional Architecture." This is followed by the block "Develop Logical Architecture," which outputs "Logical Architecture." The final block in the sequence is "Develop physical architecture." A separate branch originating from the right side of the "Classify and prioritize requirements" block connects to the final "Develop physical architecture" block, with an associated label "Behavioral, structural and experiential requirements" positioned to the right of the connection. Each process block is marked with a small circular icon containing the letters "OR."



<div align="center">

Figura. E.4: Pasos abordados en el enfoque de ingeniería de sistemas para el diseño de sistemas de mantenimiento predictivo

</div>

siendo genérica. Los requisitos de desempeño, estructurales y experienciales se utilizan para realizar la selección de componentes para cumplir con la arquitectura lógica y crear la arquitectura física.

Esta sección está relacionada con capítulo 3 de la tesis en el que se propuso un enfoque sistemático para abordar la etapa conceptual de los sistemas de mantenimiento predictivo a fin de dar respuesta a la primera pregunta de investigación perfeccionada. Los diferentes pasos desde la reunión de las necesidades y deseos iniciales de las partes interesadas hasta la definición de la arquitectura lógica se han cubierto y diferentes métodos se han propuesto para abordarlos. Sin embargo, el resto de las preguntas de investigación refinadas están aún por responder. En el mantenimiento predictivo, el espacio de solución es vasto y complejo como se muestra en el Capítulo 2 de la tesis. No hay reglas específicas que un arquitecto pueda seguir para seleccionar los modelos y enfoques adecuados para resolver nuevos problemas de mantenimiento predictivo. En esta investigación se propone una hipótesis para superar este problema: la implementación de un Sistema de Apoyo a la Decisión (DSS, por sus siglas en inglés) basado en el Razonamiento Basado en Casos (CBR, por sus siglas en inglés) y apoyado por ontologías podría ayudar al arquitecto a seleccionar componentes adecuados basados en experiencias pasadas extraídas de implementaciones exitosas de sistemas de mantenimiento predictivo.

## E.4 Desarrollo de una ontología para el sistema de razonamiento basado en casos

El DSS se compone de dos bloques de construcción principales: Razonamiento basado en casos (CBR) y ontologías. CBR es un paradigma de razonamiento que busca resolver nuevos problemas basados en las experiencias de problemas similares resueltos en el pasado. CBR se aborda en el capítulo 5 de la tesis y en la sección D.5 del presente resumen, pero es necesaria una breve introducción para comprender el papel que desempeñan las ontologías en el DSS desarrollado en la investigación actual. Los sistemas CBR se desarrollan sobre un vocabulario base [Alt+12]; [Sán+12]. Este vocabulario es necesario para dar estructura a los casos almacenados de problemas resueltos en un caso basado, a las medidas de similitud que comparan el nuevo problema con los de la base de casos, y a los conocimientos necesarios para adaptar la solución recuperada para el nuevo problema (véase Figura E.5). Para efectos de esta tesis se elige una ontología para que sirva de marco terminológico (vocabulario base). Un modelo de ontología proporciona los términos, definiciones y relaciones entre los términos que se utilizan para construir la estructura de casos, las similitudes y el conocimiento de adaptación en el DSS. Este capítulo está dedicado a los antecedentes teóricos y el desarrollo del modelo de ontología para el DSS propuesto.


> **Figure Description:**

The image is a diagram illustrating the components of a case-based reasoning system. It consists of a large outer circle containing a smaller, dashed-line inner circle. The space between the two circles is labeled "Vocabulary" in three locations, oriented along the top, bottom-left, and bottom-right arcs of the outer circle. The inner circle is divided into three equal triangular sectors by dashed lines radiating from the center. The top sector is labeled "Case base," the bottom-left sector is labeled "Similarity measures," and the bottom-right sector is labeled "Adaptation knowledge." Double-headed arrows indicate relationships between these components: one arrow connects "Case base" to "Similarity measures," one arrow connects "Case base" to "Adaptation knowledge," and one arrow connects "Similarity measures" to "Adaptation knowledge."



<div align="center">

Figura. E.5: Razonamiento basado en casos desarrollado sobre un marco de vocabulario [Alt+12]

</div>

En ciencias de la información, una ontología es una descripción explícita formal de conceptos en un dominio del discurso, propiedades de cada concepto que describen sus características, atributos y restricciones [NM01]. Uno de los objetivos más comunes en el desarrollo de ontologías es "compartir un entendimiento común de la información de la estructura entre personas y agentes de software" [Gru93]; [Mus92]. Esto significa que el vocabulario utilizado por las personas en un dominio específico de conocimiento está habilitado para ser "legible por máquinas". Todos los conceptos en una ontología están representados por clases que están vinculadas por propiedades (también llamadas relaciones). Las ontologías se desarrollan con lenguajes formales. Uno de los más reconocidos es el Lenguaje de Ontología Web en su segunda versión (OWL2) que es apoyado por el World Wide Web Consortium (W3C) [Wor12].

## E.4.1 Ontología para la selección y evaluación de estrategias de mantenimiento (OMSSA por sus siglas en inglés)

Una investigación complementaria al hilo principal de esta tesis permitió la creación de un modelo ontológico para la selección y evaluación de estrategias de mantenimiento (OMSSA por sus siglas en inglés). La creación de OMSSA sigue los mayores estándares y últimas tendencias en la creación de ontologías utilizando ontologías de alto nivel y medio nivel de referencia. Esto facilitará la reutilización e integración de OMSSA con otras ontologías relacionadas. La contribución de OMSSA fue consolidada en un artículo

científico que fue aceptado para su publicación en el momento que esta tesis fue escrita. OMSSA sirve de base para la creación del modelo ontológico que se usa para el sistema de ayuda a la decisión (DSS) propuesto en esta investigación.

## E.4.2 Ontología para la concepción de mantenimiento predictivo (OPMAD por sus siglas en inglés)

Para esta sección se mantendrán los nombres de las clases de OPMAD en inglés para mantener congruencia con el modelo y los gráficos. OPMAD es una extensión de OMSSA y se han seguido los mismos estándares y metodologías para su desarrollo. La Figura E.6 presenta las clases y relaciones más importantes en OPMAD. Por limitación de espacio, las subclases no se muestran en la figura. Como el objetivo de OPMAD es apoyar el DSS para identificar modelos adecuados para los sistemas de mantenimiento predictivo, la explicación de las clases de ontología y sus relaciones comienza a partir de la clase Modelo de Mantenimiento Predictivo (Predictive Maintenance Model), y se basa en los términos presentados en la Figura E.6. Un modelo de mantenimiento predictivo se lleva en un módulo de mantenimiento predictivo (Predictive Maintenance Module) que es un componente de un sistema de mantenimiento predictivo (Predictive Maintenance System). Cada módulo de mantenimiento predictivo tiene una Función de Mantenimiento Predictivo (Predictive Maintenance Function), esta investigación se centra en funciones de diagnóstico y pronóstico.

El modelo de mantenimiento predictivo integrado en el módulo está directamente vinculado a un elemento mantenible (Maintainable item), que es la clase que describe el sistema mantenible para el que se desarrolla el sistema de mantenimiento predictivo. El elemento mantenible se clasifica por la clase tipo de elemento mantenible (Maintainable item Type) que se agregó con fines de cálculo de similitud en el DSS; este tipo de clases ayudan a comparar el nuevo problema a tratar con el problema resuelto en una base de casos de un sistema CBR. Los elementos mantenibles pertenecientes al mismo tipo comparten importantes características de degradación y por lo tanto se pueden proponer los mismos modelos de mantenimiento predictivo para resolver las mismas funciones de mantenimiento predictivo.

El elemento mantenible tiene su propia función (Function) que se ve afectada por una falla (Failure) que se manifiesta a través de un modo de falla (Failure Mode). Un elemento mantenible tiene uno o varios modos de fallo que también son objeto del modelo de mantenimiento predictivo. El modelo de mantenimiento predictivo tiene como entrada los datos de condición (Condition) que se utilizan para realizar diagnósticos y pronósticos. Dos cualidades importantes para la implementación de un modelo de mantenimiento predictivo es su tipo y configuración. El tipo de modelo de mantenimiento predictivo (Predictive Maintenance Model Type) clasifica el modelo dentro de las familias de modelos basados en conocimiento, basados en datos y basados en la física. Este tipo de clasificación ayuda a efectos de similitud y preferencias en el DSS. La configuración del modelo de mantenimiento predictivo (Predictive Maintenance Model Configuration) muestra si un modelo debe complementarse con otros modelos para cumplir su función; puede mejorar el rendimiento, pero aumenta la complejidad del desarrollo. El módulo de mantenimiento predictivo está calificado por la sincronización (Module Synchronization) y el indicador de rendimiento (Module Performance Indicator). Estas dos cualidades proporcionan información útil sobre cómo se deben probar y sincronizar los modelos de mantenimiento predictivos incorporados en los módulos con el elemento mantenible.

Toda esta información de los modelos de mantenimiento predictivo, elementos mantenibles, sus modelos de fallo, entre otras, se colecta en el caso de mantenimiento predictivo (Predictive Maintenance Case) que se documenta y publica a través de un artículo de mantenimiento predictivo (Predictive Maintenance Article), un tipo especial de artículo que se centra en el mantenimiento predictivo. A partir de estos artículos de mantenimiento predictivo también se incluyen algunos indicadores bibliométricos en la ontología que se utilizará en el sistema CBR. Estos indicadores bibliométricos se proporcionan como atributos de

solución para que el ingeniero pueda encontrar fácilmente la fuente de información de un caso específico. El título, el identificador y el año de publicación del artículo pueden utilizarse con fines de similitud y/o como fuente de información para más detalles de los modelos de mantenimiento predictivo y su implementación.


> **Figure Description:**

This diagram illustrates a conceptual ontology or relationship map centered on Predictive Maintenance (PdM) systems. At the top, a "PdM System" has a "hasPart" relationship with a "PdM Module." The "PdM Module" is connected to "Synchronization" and "Sychronization" via "hasQuality" relationships, and it connects to "PdM Module function" via "hasFunction." The "PdM Module" also "isCarrierOf" a "PdM Model." The "PdM Model" has a "hasConfiguration" relationship with "PdM Model configuration," a "hasType" relationship with "PdM Model type," and an "IsAbout" relationship with "Maintainable item."

The "Maintainable item" serves as a central node, connected to "Condition Data" via a "hasInput" relationship, and to "Maintainable item type" via a "hasType" relationship. The "Maintainable item" also has a "hasFunction" relationship with "Function," a "hasCaseStudy" relationship with "PdM Case," and a "hasFailureMode" relationship with "Failure Mode." "Condition Data" has a "hasType" relationship with "Condition Data Type."

The "Function" node is connected to "Failure" via an "isAffectedBy" relationship, and "Failure Mode" "describes" "Failure." At the bottom, "PdM Case" is linked to "PdM Article" via an "isCarrierOf" relationship. "PdM Article" is the subject of "IsAbout" relationships originating from "PdM Article title," "PdM Article identifier," and "PdM Article Publication year." Finally, "PdM Module function" has an "is a" relationship with "Function." All relationships are represented by directed arrows labeled with the specific relationship type.



<div align="center">

Figura. E.6: Clases and relaciones en OPMAD

</div>

## E.5 Desarrollo de sistemas de razonamiento basado en casos

El razonamiento basado en casos (CBR) es una metodología de resolución de problemas basada en recuperación de soluciones previas para problemas similares [De +05]. El razonamiento basado en el caso se desarrolló bajo la filosofía de que los seres humanos piensan y razonan usando analogías y ejemplos, en lugar de estructuras SI-ENTONCES, estas últimas formando la base para el razonamiento basado en reglas. La solución del problema se realiza en un proceso cíclico de varios pasos: el ciclo CBR [AP94]. Este ciclo se compone de cuatro fases: recuperar, reutilizar, revisar y retener (ver Figura E.7).

El ciclo CBR se activa cuando se encuentra un nuevo problema. Esta primera fase tiene como objetivo recuperar los casos más similares de una base de conocimientos que almacena todos los casos anteriores. El caso objetivo (nuevo) se compara con los casos existentes en la base de conocimientos utilizando diferentes mediciones de similitud. El caso más cercano recuperado se propone como una posible solución en la fase de reutilización. Tal vez se necesite alguna adaptación para aplicar la solución en el caso previsto. Después de sugerir e implementar la solución se lleva a cabo la fase de revisión. Si la solución sugerida logra resolver el problema, se confirma y en la última fase, se retiene en la base de conocimiento para que pueda ser reutilizada en futuros problemas similares. En las subsecciones siguientes se proporcionan más detalles sobre cada fase de la RBC.


> **Figure Description:**

This diagram illustrates the Case-Based Reasoning cycle, organized around a central box labeled "General Knowledge" containing a stack of documents labeled "Previous cases." The cycle consists of four main stages arranged in a circular flow, each represented by a shaded arc: RETRIEVE, REUSE, REVISE, and RETAIN.

The process begins at the top with a "Problem" arrow pointing to a "New case" box. This "New case" box connects to the "Previous cases" central repository. From the "Previous cases," an arrow points to a "Retrieved case" box, which is paired with a "New case" box. This pair transitions into the "REUSE" stage, leading to a "Solved case" box, which has an outgoing arrow labeled "Suggested Solution."

The "Solved case" box connects to the "REVISE" stage, which leads to a "Tested/Repeated case" box. An arrow pointing away from this box is labeled "Confirmed Solution." This "Tested/Repeated case" box then connects to the "RETAIN" stage, which leads to a "Learned case" box. Finally, an arrow points from the "Learned case" box back into the central "Previous cases" repository. Double-headed arrows connect the central "General Knowledge" box to each of the four shaded stage arcs (RETRIEVE, REUSE, REVISE, and RETAIN), indicating a continuous interaction between the stages and the knowledge base.



<div align="center">

Figura. E.7: Ciclo de razonamiento basado en casos, ilustración inspirada en [AP94]

</div>

## E.5.1 Plataforma MyCBR

El módulo CBR del DSS para la investigación actual se ha creado utilizando myCBR, una herramienta de búsqueda basada en similitudes de código abierto para el razonamiento basado en casos (CBR) [Alt+12]. Al desarrollar un sistema de recuperación de CBR usando myCBR el primer paso es determinar los atributos del caso. Los casos están representados por un vector acoplado de atributos:

$$
\mathrm {C a s o} = [ \mathrm {A t r i b u t o s d e l p r o b l e m a}, \mathrm {A t r i b u t o s d e l s o l u c i c i o n} ].
$$

Los atributos de problema se utilizan para medir la similitud de un caso objetivo y los casos en una base de casos. Los atributos de la solución, como su nombre lo dice proveen información relevante relacionada con la solución del problema en cada caso almacenado en la base de casos.

Una vez los atributos han sido determinados, el segundo paso es la asignación de una medida de similitud local a cada atributo del problema. MyCBR proporciona varias opciones para calcular la similitud para cada atributo del problema. Dentro de las opciones disponibles, se han utilizado tres funciones de similitud para la investigación actual:

1. Similitud entero/flotante: esta función de similitud se utiliza para los atributos numéricos. La similitud se obtiene por una diferencia entre un valor de referencia y los valores de entrada de la función. Se necesita una función matemática para definir cómo disminuye la similitud a medida que los valores de entrada se alejan del valor de referencia. Esta función matemática puede ser lineal, exponencial o determinada por puntos discretos en el plano cartesiano.

2. Similitud de símbolo: esta medida de similitud es aconsejable para variables con un conjunto fijo de opciones. Estas opciones se organizan en una matriz de similitud y se dan algunos valores numéricos

para establecer la similitud entre las opciones. Esta función de similitud ha sido modificada para que algunos atributos de la investigación actual interactuen con el modelo ontológico. Los valores de la matriz de similitud se obtienen automáticamente a partir de las clases y relaciones de una ontología utilizando el enfoque de similitud basado en características propuesto por [Sán+12].

3. Similitud de cadena de caracteres: la similitud de atributos se obtiene con base en cadenas de texto abiertas. A diferencia de la similitud de símbolo que tiene un número limitado de opciones para definir la similitud, la similitud de cadena de caracteres solo tiene la restricción de tener oraciones o palabras como entrada. MyCBR ofrece tres opciones para calcular la similitud basada en cadenas: Igualdad, Ngram y Levenshtein. Para el estudio de caso actual, se seleccionó la función Levenshtein para calcular los atributos basados en cadenas de caracteres de similitud. La función Levenshtein ofrece un medio flexible para calcular la similitud basada en cada carácter de la cadena [Lev66]. Esto es especialmente útil cuando hay un amplio conjunto de opciones que son desconocidas al crear similitudes y también tolera pequeños errores ortográficos.

Después del cálculo de similitud para cada uno de los atributos del problema, se combinan estas similitudes individuales en una similitud global. Por medio de una función de agregación se calcula la similitud global en la que cada atributo tiene un peso spécífico. El objetivo de los pesos es dar especial importancia a los atributos de problemas. Para efectos de esta investigación, todos los atributos reciben el peso de 1, lo que significa que tienen la misma importancia. MyCBR ofrece dos opciones diferentes para calcular la similitud global: suma ponderada y distancia euclidiana.

- Suma ponderada: como dice el nombre, es la suma de similitudes considerando el peso de cada una.

- Distancia euclidiana: la distancia euclidiana entre dos puntos en el espacio euclidiano es un número, la longitud de un segmento de línea entre los dos puntos.

En esta tesis, ambas funciones de amalgamación pueden ser utilizadas por el usuario. Es importante señalar que para calcular la similitud global sólo se consideran los atributos disponibles. Esto significa que, si el arquitecto cuenta sólo con dos o tres atributos de los siete que describen el problema, la similitud global se calculará sobre la base de esos dos o tres atributos.

## E.5.2 Representación de los casos

"Un caso es una pieza de conocimiento en un contexto particular que representa una experiencia que enseña una lección esencial para alcanzar la meta del razonador" [Kol93]. Los casos se representan a menudo en una forma acoplada [problema, solución], en la que se aplican similitudes en la parte del "problema" para que la parte de la "solución" se recupera. La representación del caso se compone de tres partes principales [BKP05]:

1. Definir los atributos del caso.

2. Definir la estructura del contenido del caso.

3. Organizar la base de casos.

La representación y estructura del caso se hace usando OPMAD. La Figura E.6 mostró los diferentes atributos (clases en ontología) del caso representado en OPMAD. Estas clases de ontología se pueden dividir en dos grupos diferentes: los atributos del problema y los atributos de la solución (mantienen sus nombres originales en inglés):

- Atributos del problema = [PdM Function,Maintainable Item,Maintainable Item Type, Condition Data Type,Module synchronization,PdM Article Publication year]

• Atributos de 1 solución = [PdM Model,PdM Model Configuration,PdM Model Type, Module Performance Indicator,PdM Article Identifier,PdM Article Title]

## E.5.3 Desarrollo del motor de recuperación de componentes para sistemas de mantenimiento predictivo

La base de casos del DSS es una versión instanciada de OPMAD que ha sido poblada con casos exitosos de implementaciones de mantenimiento predictivo. El proceso para instanciar OPMAD a partir de una extensa revisión bibliográfica incluye la definición de las diferentes variables a buscar y las posibles opciones para cada variable; esto permite una mejor estructura de base de casos y facilita la recuperación. Para cada atributo de problema, se selecciona una similitud local entre las opciones posibles: entero, símbolo, basado en ontología, texto abierto. Tabla E.1 muestra las funciones de similitud asignadas a cada uno de los atributos del problema. Se han añadido dos funciones de agregación diferentes para calcular la similitud global entre un caso objetivo y los casos almacenados en la base de casos. Se ha desarrollado un GUI para facilitar la verificación y validación del motor de recuperación. El motor de recuperación desarrollado es el núcleo del DSS para la selección de componentes de mantenimiento predictivo. El siguiente capítulo está orientado a mostrar el marco completo del sistema CBR con ontología para la selección de componentes de mantenimiento predictivo. Los detalles de desarrollo del motor de recuperación se proporcionan en la guía de códigos del apéndice C.

<div align="center">

Tabla E.1: Asignación de funciones de similitud

</div>

<table border="1"><tr><td>Attribute</td><td>Similarity function</td></tr><tr><td>PdM Function</td><td>Símbolo(Ontología)</td></tr><tr><td>Maintainable item</td><td>Cadena(Levenshtein)</td></tr><tr><td>Maintainable item type</td><td>Símbolo(igualdad)</td></tr><tr><td>Condition Data</td><td>Símbolo(Ontología)</td></tr><tr><td>Condition Data Type</td><td>Símbolo(igualdad)</td></tr><tr><td>Module synchronization</td><td>Símbolo(igualdad)</td></tr><tr><td>PdM Article Publication Year</td><td>Entero(función definida por puntos)</td></tr></table>

## E.6 Desarrollando un marco de trabajo para la selección de modelos de mantenimiento predictivo

Un hito común en el desarrollo de la arquitectura de sistemas es la arquitectura lógica. En la arquitectura lógica se provee la mayor cantidad de detalle posible manteniendo los componentes genéricos. Estos componentes genéricos deben ser sustituidos por componentes específicos creando así la arquitectura física del sistema. Para la selección de los componentes se puede aplicar la creatividad estructurada. La creatividad estructurada en la arquitectura lógica se basa en analizar las posibles combinaciones de los diferentes componentes físicos/informativos que pueden ser seleccionados para satisfacer cada componente lógico. Esto permite la exploración del espacio de solución y puede ayudar al arquitecto a identificar soluciones innovadoras para un nuevo sistema. Si se identifican varias soluciones posibles, puede ser necesario un análisis de compensación para seleccionar la más adecuada. La arquitectura seleccionada sirve de base para el diseño detallado de los sistemas. Los conocimientos obtenidos del nuevo sistema implementado pueden ser utilizados por el arquitecto para desarrollar futuros sistemas. Existe una analogía entre el trabajo de


> **Figure Description:**

This diagram illustrates a software or systems engineering process involving an Architect and a team of Design, implementation, verification, and validation engineers. The process is divided into two main swimlanes. The top lane, labeled "Architect," contains a vertical sequence of yellow process boxes: "Develop concept phase until a generic logical architecture," "Search posible components from previous experiences (Retrieval Phase)," "Allocate posible components to logical architecture (Reuse phase)," and "Trade-off analysis on the architecture possibilities (start of the revise phase)." These steps are connected by downward arrows labeled "Generic logical architecture (New Problem)," "Logical architecture," and "Possible physical architectures."

To the left, a separate box labeled "Historical records of previous experiences" contains the process "Store knowledge from previous experiences." This box interacts with the Architect's lane: an arrow labeled "Logical components" points from the historical records to the retrieval phase, and an arrow labeled "Identified suitable components" points from the historical records to the allocation phase.

The bottom swimlane, labeled "Design, implementation, verification and validation engineers," contains two process boxes: "Design and implement the system" and "Verify and valdiate system (end of revise phase)." An arrow labeled "Selected architecture" flows from the Architect's trade-off analysis box down to the "Design and implement the system" box. An arrow labeled "Implemented system" connects the design box to the verification box. The verification box then sends an arrow labeled "Information from implemented system" to a process box labeled "Keep records from the validated system (retain phase)," which is located within the Architect's lane. Finally, an arrow labeled "New record from the validated system" flows from the "Keep records" box back to the "Store knowledge from previous experiences" box, completing the feedback loop. Each process box is marked with a small circular icon containing the letters "OR."



<div align="center">

Figura. E.8: Analogía entre razonamiento basado en casos y las tareas que realiza un diseñoador de sistemas, en notación Capella [Roq18]

</div>

creatividad estructurada realizado por el arquitecto para seleccionar componentes adecuados para cumplir con la arquitectura lógica y las cuatro fases del Razonamiento Basado en Casos: recuperar, reutilizar, revisar y retener. Una representación gráfica de esta analogía se presenta en Figura E.8 (en notación de Capella [Roq18]).

La analogía propuesta relaciona la fase de recuperación de CBR con la búsqueda realizada por el arquitecto en sistemas anteriores relacionados que pueden servir de inspiración para el desarrollo del nuevo sistema.

- La fase de reutilización de CBR sería la asignación de los componentes identificados para cumplir con la nueva arquitectura del sistema.

- La fase de revisión del CBR comenzaría por el análisis de compensación realizado por el arquitecto para identificar los componentes más adecuados. Esta fase continua hasta la verificación y validación del sistema implementado que generalmente son realizados por otros actores distintos del arquitecto.

- Después de la validación del nuevo sistema, el arquitecto puede mantener los registros que se utilizarán en el futuro; esta sería la fase de retención de CBR.

Esta analogía sigue siendo genérica en cuanto al sistema que el arquitecto va a desarrollar. Todas las actividades son realizadas "manualmente" por el arquitecto y los registros de experiencias previas pueden no estar estructurados para facilitar su reutilización. Este enfoque manual puede funcionar cuando la cantidad de experiencias previas es limitada para que el espacio de solución a ser explorado por el arquitecto siga siendo manejable. Cuando el número de experiencias previas es alto o los requisitos complejos, la selección de los componentes más adecuados puede no ser fácil. Recuperar conocimiento de un número importante de arquitecturas anteriores puede consumir demasiado tiempo y se pueden perder opciones importantes.

Considerando esta analogía entre CBR y el trabajo de creatividad estructurada, se pueden proponer diferentes algoritmos para apoyar al arquitecto en las diferentes fases del trabajo de arquitectura. En un

primer paso, la investigación actual se centro en el desarrollo de un Sistema de Apoyo a la Decisión (DSS) capaz de realizar la búsqueda y recomendación de componentes físicos/informativos adecuados. Esto puede ayudar al arquitecto a ahorrar tiempo en la fase de concepto, y permite un análisis más amplio realizado por máquinas, análisis que difícilmente pueden ser abordados por los seres humanos.

La Figura E.9 presenta un concepto del DSS y cómo encaja en la analogía presentada en la Figura E.8. Este concepto se compone de tres partes principales: la base de casos, el motor de recuperación y la ontología específica del dominio. La base de casos almacena los casos del pasado en un formato estructurado para facilitar su reutilización. El arquitecto presentará al motor de recuperación la información del nuevo sistema en desarrollo y obtendrá un conjunto de los casos más similares recuperados de la base de casos que servirá de inspiración al seleccionar componentes adecuados para la arquitectura lógica.

Dentro de esta estructura la ontología juega un papel vital. Los casos, los atributos de estos casos y las similitudes entre las diferentes variables basadas en texto se describen a menudo en lenguaje natural. Modelar este lenguaje natural y hacerlo legible por máquina es necesario para automatizar la recuperación del caso. La integración de la ontología propuesta y el módulo de recuperación de CBR se explica con más detalle en una investigación complementaria presentada en el Apéndice B. La siguiente sección aborda la validación del DSS propuesto y la discusión de los resultados obtenidos.


> **Figure Description:**

This diagram illustrates a Case-Based Reasoning (CBR) workflow involving three primary entities: a Retrieval System Manager, a CBR Retrieval System, and an Architect, alongside a bottom section for Design, implementation, verification, and validation engineers. The Retrieval System Manager contains a process to "Maintain case base (including the retain phase of CBR)," which sends a "New case" to the "Casebase" component within the CBR Retrieval System. The "Casebase" stores cases and interacts with the "Retrieve engine," which retrieves "suitable models from previous experiences" based on "Previous cases." The "Retrieve engine" also utilizes an "Ontology Model" to "Provide terminology framework," which supplies "Terms, definitions, similarities" to the engine and "Terms, definitions, relations" back to the "Casebase."

The Architect entity receives "attributes of the current problem" and proceeds to "Develop concept phase until logical architecture." This leads to a "Logical architecture" output, which informs the "Allocate models to logical components (Reuse Phase of CBR)" process. This process receives "Suitable Models" from the "Retrieve engine" and outputs "Architecture posibilites," which then feed into the "Architecture trade-off (start of the revise phase of CBR)." 

The final output from the Architect, labeled "Selected system architecture," is sent to the "Design, implementation, verification and validation engineers" section. This section contains a process to "Design and implement system," which produces an "Implemented system" that is then subjected to "Verification and validation (end of the revise phase of CBR)." Finally, a "Verified and validated architecture (revised solution)" is sent back to the Retrieval System Manager to complete the cycle. Each process block is marked with an orange circular icon, and data flows are represented by arrows labeled with the specific information being transferred.



<div align="center">

Figura. E.9: Idea conceptual de la incorporación del DSS para la selección de componentes de sistemas

</div>

## E.7 Validación y discusión de resultados

La validación del DSS se divide en dos partes: una validación cruzada para confirmar la coherencia del DSS y una implementación de un modelo sugerido en un estudio de caso para probar las recomendaciones del DSS en un ejemplo práctico.

## E.7.1 Validación cruzada

La validación cruzada es una técnica que se puede utilizar para probar la eficacia de los modelos de inteligencia artificial entrenados. Para el abordaje actual, se selecciona un enfoque de división de la prueba de tren para realizar la validación cruzada. Para el conjunto de pruebas, 63 de los 263 casos de la base de casos se extrajeron al azar y el resto se ha dejado en la base de casos como conjunto de entrenamiento. Para cada uno de los 63 casos extraídos, los atributos del problema fueron presentados al DSS usando GUI.

La atención se centró en los 10 casos más similares al realizar la recuperación. La Figura E.10 muestra un ejemplo de una prueba de recuperación en la que todos los atributos de problema del caso objetivo se corresponden con los atributos de solución correspondientes del caso 35. Esta coincidencia completa entre los atributos resulta en una similitud global de 1.

El espacio de solución de los modelos de mantenimiento predictivo se puede dividir en dos grupos como se explica en [Mon+20]. El primer grupo está compuesto por enfoques de modelo único, divididos en tres categorías principales: modelos basados en el conocimiento, modelos basados en datos y modelos basados en la física. El segundo grupo está compuesto por enfoques multimodelo, en los que al menos dos modelos de cualquiera de las tres categorías mencionadas se combinan para cumplir una función específica del sistema de mantenimiento predictivo. El mantenimiento predictivo está compuesto por tareas de diagnóstico y pronóstico. Según la revisión de la literatura [Mon+20], las tareas de diagnóstico como la detección de fallas, la identificación de fallas y la modelización del estado de salud pueden ser abordadas por modelos de las tres categorías de enfoques de modelo único o enfoques multimodelo. En cambio, para las tareas de pronóstico es difícil encontrar modelos basados en el conocimiento. Por ejemplo, las funciones de pronóstico, como la estimación de la vida útil restante y las funciones de previsión del estado siguiente, se cumplen normalmente mediante modelos basados en la física, modelos basados en datos y enfoques multimodelo que combinan modelos basados en la física y en datos. La validación cruzada del DSS permitió confirmar este comportamiento. Las recuperaciones para tareas de diagnóstico propusieron soluciones de modelo único y multimodelo considerando modelos de las tres categorías de modelos. Las recuperaciones para pronósticos también propusieron soluciones de modelo único y multimodelo, pero los modelos propuestos fueron sólo de categorías basadas en datos y en la física. Esto ayuda a confirmar que el espacio de solución está bien cubierto.


> **Figure Description:**

Software user interface screenshot.

The image displays a software interface titled "Predictive maintenance with CBR method - GUI 2." The top section, labeled "Input variables" in red, contains a table with six rows of parameters, each paired with a dropdown menu and a "Variable weights" column set to 1.0. The parameters are: "PdM function" (set to "Remaining useful life estimation"), "Maintainable item type" (set to "Rotary machines"), "Maintainable item" (set to "Rolling bearings"), "Condition data type" (set to "Vibrations"), "Module sychonization" (set to "Off-line"), and "Condition data" (set to "Time series"). Below this, an "Additional inputs" section (also in red) includes a field for "Number of cases to retrieve" set to 10, and an "Aggregation function to use" dropdown set to "euclidean."

The "User dialog" section displays the text: "I found Case35 with a similarity of 1.000 as the best match. The 10 best cases shown in a table:". Below this is a table with two columns: "Case" and "Description." The first row of the table contains "Case35 Sim = 1.000" in the left column and a detailed description in the right column: "Reference, Similarity and Input variables," "Reference: 35," "Task: Remaining useful life estimation," "Case study type: Rotary machines," "Case study: Rolling bearings," "Online/Off-line: Off-line," "Input for the model: Time series," "Models: Convolutional Neural Network," "Input type: Vibrations," "Publication Year: 2018," and "Publication identifier: DOI: 10.1109/ACCESS.2018.2804930." At the very bottom of the window is a button labeled "SUBMIT QUERY."



<div align="center">

Figura. E.10: Ejemplo de recuperación de caso usando la interfaz del DSS

</div>

Para cada caso de prueba, los casos recuperados se clasifican en función de la similitud de los atributos del problema. Para algunas de las pruebas, el remolque o más casos recuperados tenían el mismo valor de similitud máximo y/o proponían el mismo modelo para cumplir una función PdM específica. Desde una perspectiva de Ingeniería de Sistemas, esto representa dos limitaciones. El primero se refiere a dos o más casos recuperados con la misma similitud máxima porque no se proporciona más información para realizar el análisis de compensación y se selecciona el más adecuado. La segunda limitación está relacionada con la diversidad en los casos recuperados, especialmente cuando dos o más casos recuperados sugieren

que el mismo modelo cumple una función específica. Un arquitecto que busca inspiración para desarrollar soluciones innovadoras necesitará del DSS para proponer un conjunto diverso de modelos. Estos son puntos de mejora para que el DSS sea considerado en el futuro. También se puede realizar un análisis más detallado que incluya el esfuerzo de adaptar la solución de un caso recuperado para el caso objetivo. Esto puede ayudar a realizar el análisis de compensación en las opciones recuperadas y, en consecuencia, mejorar el rendimiento del DSS.

## E.7.2 Implementación del caso de estudio práctico

Como parte de la validación, se ha desarrollado un ejemplo de implementación a partir de las sugerencias del DSS en caso de estudio. El caso de estudio consiste en un conjunto de datos de motor de avión [Cha+21]. El conjunto de datos contiene los registros de fallos de funcionamiento de 128 motores de avión en condiciones reales de vuelo y se ha generado con el modelo Commercial Modular Aero-Propulsion System Simulation (CMAPSS) desarrollado por la NASA. Estos datos se llaman el conjunto de datos N-CMAPSS. El propósito no es sólo comprobar las capacidades del sistema CBR habilitado por ontología (el DSS) sino también identificar los puntos de mejora para el DSS. El objetivo de esta validación es implementar uno de los modelos propuestos por el DSS para cumplir una función de mantenimiento predictivo para la base de datos N-CMAPSS. Esta implementación ayuda a demostrar que el DSS es capaz de sugerir componentes adecuados para sistemas de mantenimiento predictivo, complementando la validación cruzada.

A fin de validar mejor las recomendaciones del Departamento de Seguridad, se ha tomado como ejemplo uno de los modelos propuestos y se ha aplicado para cumplir la función de mantenimiento predictivo correspondiente. Aprovechando la experiencia del equipo de investigación en Mapas de Auto Organización (SOM), se realiza una implementación del componente de modelado de salud utilizando el SOM. El DSS recomienda el SOM y la regresión logística para el modelado de salud como los modelos más adecuados (similitud igual a 0.879) para el estudio de caso N-CMAPSS. La siguiente sección proporciona explicaciones adicionales sobre la implementación del ejemplo SOM y sus resultados preliminares.

La metodología para implementar los Mapas de Auto-Organización (SOM) para la modelización de la salud ha sido adoptada de [Sch+20], (véase también el Apéndice A). Los mapas auto-organizados son redes neuronales artificiales con entrenamiento no supervisado que son capaces de agrupar instancias de datos dependiendo de los atributos de instancia. SOM se compone normalmente de una capa cuadrada de neuronas y los diferentes grupos después de la formación SOM se puede representar gráficamente en los mapas como regiones bien definidas. Se ha utilizado con éxito para modelar el proceso de degradación de diferentes máquinas como los motores a reacción [MV18]. En estos casos, las neuronas representan la salud o la degradación de la máquina en un modo operativo específico. El SOM entrenado tendrá una sola región, pero una transición de blanco (estado óptimo) a negro (estado fallido). Al evaluar la salud o la degradación de una máquina usando el SOM entrenado, una neurona saldrá en el mapa mostrando qué tan avanzada está la degradación o cuánto ha disminuido la salud. Este es el verdadero objetivo de la implementación actual: obtener un SOM capacitado capaz de mostrar una transición del estado óptimo al estado fallido. La figura E.11 muestra el mapa auto-organizativo entrenado con el N-CMAPSS. El resultado corresponde con el comportamiento esperado. Los diferentes modelos de degradación han sido ordenados en el mapa.

Es importante recordar que la validación de un Sistema de Apoyo a las Decisiones (DSS) es una tarea difícil. La validación del SOM para modelar la salud del N-CMAPSS puede utilizarse para validar indirectamente el DSS; sin embargo, es importante resaltar que se requerirían otras implementaciones que confirmen las capacidades y la precision del DSS propuesto para la selección de modelos de mantenimiento predictivo. En la implementación actual, el N-CMPASS representa el caso objetivo para el que se tiene que desarrollar un nuevo sistema de mantenimiento predictivo. El sistema de recomendación CBR con ontología (también llamado DSS en este manuscrito) propuso diferentes modelos para cumplir cada función


> **Figure Description:**

The image is a heatmap titled "Dataset" with a 5x5 grid of cells, plotted against x and y axes that both range from 0 to 4. The color intensity, representing the data values, increases from light pink to dark red as both the x and y coordinates increase. The grid is organized such that the lowest values are at the bottom-left (0,0) and the highest values are at the top-right (4,4). Specifically, the intensity gradient shows a clear progression where the cells at (0,0), (0,1), (1,0), and (1,1) are the lightest, while the cells at (3,4), (4,3), and (4,4) are the darkest red. The axes are labeled with integers 0, 1, 2, 3, and 4 at equal intervals.



<div align="center">

Figura. E.11: Mapa auto-organizativo entrenado con el caso de estudio N-CMAPSS

</div>

de mantenimiento predictivo. Uno de los modelos propuestos por el DSS para el modelo de la función de salud fue el Mapa de Auto-Organización (SOM). La implementación de SOM mostró con éxito la tendencia de degradación de los motores a reacción desde la operación nominal a la condición fallida utilizando un subconjunto del N-CMPASS. El SOM entrenado también se puede utilizar para evaluar la salud/ degradación de otro motor del mismo tipo y bajo las mismas condiciones de operación. Es importante aclarar que esta validación tiene por objeto demostrar la idoneidad del modelo propuesto por el DSS, pero se necesitan más comparaciones entre los modelos propuestos para determinar el mejor modelo.

## E.8 Conclusión y perspectivas de trabajo futuro

## E.8.1 Resumen de contribuciones

La tesis está compuesta por cuatro artículos que han sido publicados o aceptados para su publicación en revistas o conferencias internacionales. Las principales contribuciones de la investigación doctoral se han consolidado en los artículos de la siguiente manera:

1. El artículo de revisión bibliográfica resumió el estado del arte en diagnósticos y pronósticos. Se ha presentado una propuesta para diferenciar los modelos híbridos de los enfoques multimodelo. Se han señalado las tendencias hacia la aplicación de enfoques multimodelo. En el momento en que este manuscrito fue terminado, el artículo de revisión fue citado más de veinte veces. La revisión de la literatura puede ser vista como una contribución científica ya que proporciona un punto de partida para aquellos investigadores interesados en el mantenimiento predictivo.

2. El enfoque de ingeniería de sistemas para el diseño de sistemas de mantenimiento predictivo ha sido la primera contribución científica publicada en una conferencia internacional durante el desarrollo del doctorado. A diferencia de las arquitecturas genéricas existentes para el diseño de sistemas de

mantenimiento predictivo, el enfoque sistemático propuesto aborda la etapa conceptual de los sistemas de mantenimiento predictivo desde las necesidades y deseos iniciales hasta la arquitectura lógica. Ayuda al arquitecto a determinar con precision los componentes del sistema y mantener la trazabilidad con las necesidades y deseos iniciales obtenidos de las partes interesadas.

3. Incluso cuando las ontologías no eran el ámbito principal de la investigación actual, una buena cantidad de trabajo de investigación se ha realizado en el dominio y ha producido sus propios resultados de investigación. La creación de OMSSA, un modelo de ontología para la selección y evaluación de estrategias de mantenimiento, proporciona un marco terminológico que puede ser utilizado por agentes inteligentes para automatizar las complejas tareas de gestión de estrategias de mantenimiento. Una extensión a OMSSA (OPMAD) es la ontología utilizada para crear la base de casos y las medidas de similitud del DSS para la selección de componentes de mantenimiento predictivo. El trabajo de investigación realizado en la creación de OMSSA se ha consolidado en un artículo de la revista que estaba bajo una segunda revisión después de una revisión importante en el momento en que este documento fue escrito.

4. El alcance principal de la investigación actual ha producido una contribución. Un sistema de apoyo a la toma de decisiones (DSS) capaz de consultar casos exitosos de implementación de sistemas de mantenimiento predictivo puede ayudar a un arquitecto de sistemas a seleccionar modelos de mantenimiento predictivo adecuados para realizar tareas de diagnóstico y pronóstico. Los primeros resultados de esta investigación se han publicado en un documento de conferencia que se ha publicado en una conferencia internacional.

## E.8.2 Perspectivas de trabajo futuro

Mientras se trabaja en la investigación no es factible explicar y probar todo. Para lograr los objetivos de la investigación en un plazo fijo, algunos de los pasos intermedios de la investigación tienen que ser simplificados y a veces se toman decisiones pragmáticas. Al lograr los resultados, es importante poner las cosas en perspectiva para detectar los puntos de mejora y enumerarlos como perspectivas de trabajo futuro. La investigación nunca termina, y una de las partes principales de cualquier manuscrito de doctorado es indicar lo que faltaba y se espera que se haga con el fin de continuar la línea de investigación. Las perspectivas de la labor futura se organizan en tres grupos principales:

1. Perspectivas relacionadas con el enfoque de ingeniería de sistemas para el diseño de sistemas de mantenimiento predictivo.

2. Perspectivas relacionadas con las ontologías desarrolladas en la investigación actual.

3. Perspectiva relacionada con el sistema de recomendación basado en casos, habilitado para la ontología, para la selección predictiva de componentes.

## E.8.2.1 Perspectivas relacionadas con el enfoque de ingeniería de sistemas para el diseño de sistemas de mantenimiento predictivo.

- Mejorar la lista de necesidades, deseos y requerimientos del sistema de mantenimiento predictivo: después de publicar el artículo relacionado con la etapa conceptual de los requerimientos que no fueron considerados originalmente. Se puede actualizar y refinar la lista de posibles necesidades, deseos y requisitos para nuevos sistemas de mantenimiento predictivo. Estas listas pueden almacenarse en bases de datos que pueden ser utilizadas por agentes inteligentes automatizados para ayudar a los ingenieros a evaluar las necesidades y deseos iniciales de un sistema de mantenimiento predictivo y

sugerir los requisitos correspondientes de las partes interesadas. Se podría desarrollar un DSS para definir los requisitos correctos de las partes interesadas basados en las necesidades iniciales y los deseos para el nuevo sistema de mantenimiento predictivo.

- Incluir la técnica de análisis de compensación en el marco sistemático: Los análisis de compensación están presentes en varios puntos durante la etapa conceptual. Por falta de tiempo, aún no se ha abordado. La integración de una herramienta de análisis de compensación puede ayudar a mejorar el DSS y facilitar la selección de los componentes de la arquitectura.

- Incluir la formalización de los requisitos del sistema: un aspecto importante de un enfoque de ingeniería de sistemas es la obtención de los requisitos del sistema. Incluso cuando la creación de estos requisitos es en teoría antes del proceso de arquitectura, en la práctica, estos requisitos se establecen normalmente paralelamente al desarrollo de la arquitectura del sistema o incluso al final, cuando se conocen todas las prestaciones de los diferentes componentes lógicos. Estos requisitos son importantes para la fase de diseño detallado. La obtención de estos requisitos estaba fuera del alcance de la investigación actual, pero es un tema complementario interesante para futuras investigaciones.

## E.8.2.2 Perspectivas relacionadas con las ontologías desarrolladas en la presente investigación.

- Refinar clases y relaciones: el desarrollo de ontologías es un tema en rápida evolución. Hay varias iniciativas para proporcionar ontologías de nivel superior y medio en diferentes dominios. El dominio industrial no es la excepción. Será necesario seguir trabajando para alinear OMSSA y OPMAD a estas ontologías estandarizadas, para impulsar su integración y reutilización en otras aplicaciones industriales. Este trabajo incluye el refinamiento de las clases y las relaciones entre ellas.

- Extender el razonamiento en la ontología: OMSSA y OPMAD han sido útiles en la investigación actual, pero como ontologías, han sido infrautilizados. Las ontologías tienen varias capacidades que no fueron explotadas. Una de ellas es la implementación de reglas semánticas. Esto amplía las opciones de razonamiento y se puede utilizar como un medio complementario al sistema CBR.

## E.8.2.3 Perspectiva relacionada con el sistema de recomendación basado en casos, habilitado para la ontología, para la selección predictiva de componentes.

- Ampliar el uso de la ontología para funciones de similitud más locales: como ya se ha mencionado, la ontología ha sido útil pero infrautilizada. Algunas otras medidas de similitud que han sido asignadas a una medida de similitud de símbolos binarios pueden ser reorganizadas para usar similitudes basadas en ontología.

- Utilizar la ontología para estimar los pesos para el cálculo de similitud global: relacionado con la observación anterior. la ontología también se puede utilizar para calcular los pesos de cada similitud local al calcular la similitud global. En el primer intento de cálculo de similitud global realizado en esta investigación, todas las similitudes locales recibieron el mismo peso. Una mejora en el cálculo de la similitud global podría ser dando un rango de importancia a cada similitud local. Los pesos se pueden calcular usando la ontología poblada.

- Ampliar el Sistema de Apoyo a las Decisiones desarrollando otras fases del ciclo CBR, como la fase de adaptación: El alcance del DSS estaba en la fase de recuperación del ciclo CBR. El sistema puede ampliarse para facilitar la fase de adaptación de los componentes propuestos para el nuevo sistema de mantenimiento predictivo. Esta ampliación también puede incluir el análisis de compensación de los diferentes componentes sugerido por el DSS. Los resultados de la investigación actual mostraron varias oportunidades de mejora que deberían abordarse en el futuro antes de la eventual implantación del DSS.

- Refinar el proceso de instanciación para evitar problemas de diversidad pero manteniendo todo el espacio de solución cubierto: Como se mencionó en el capítulo de validación, la instanciación de la base de casos debe ser refinada. Una oportunidad de mejora puede ser dividir el espacio de solución por las diferentes funciones de mantenimiento predictivo y asegurarse de que el espacio de solución está completamente cubierto para cada uno de ellos. Casos generalizados para cada función de mantenimiento predictivo pueden resolver el problema de la diversidad en los casos de recuperación.

- Análisis de compensación para seleccionar mejor la técnica entre las propuestas: ya se mencionó como la perspectiva de trabajo futuro para el enfoque sistemático para el diseño de sistemas de mantenimiento predictivo. En cuanto al DSS, el análisis de compensación puede ayudar al arquitecto a discriminar entre los componentes sugeridos por el DSS. En la validación se mencionó que a veces el DSS sugería dos componentes diferentes con la misma similitud. Agregar algunos atributos adicionales como indicadores de rendimiento puede ayudar al arquitecto a tomar la decisión correcta para su problema.

Résumé — La maintenance prédictive vise à déterminer le bon moment pour déclencher des actions de maintenance en fonction de l'état de santé d'un système. La maintenance prédictive est effectuée par des systèmes spécialisés dont la conception est encore basée sur des essais et des erreurs. Deux des principaux défis dans le développement des systèmes de maintenance prédictive sont l'absence d'une approche systématique pour aborder leur état conceptuel, et la sélection des composants appropriés pour traiter les tâches de diagnostic et de pronostic. Cette recherche vise à proposer des solutions possibles pour relever ces défis. Une approche d'ingénierie des systèmes est proposée pour aborder l'étape du concept, et un système d'aide à la décision (DSS) est proposé pour aider l'architecte à sélectionner les composants appropriés en fonction des mises en œuvre de maintenance prédictives réussies précédentes. Pour le développement du DSS deux technologies sont intégrées : Case-Based Reasoning et ontologies. La validation du DSS comprend la mise en œuvre de l'un des composants suggérés par le DSS pour accomplir une tâche de diagnostic dans une étude de cas de données de moteur à réaction simulée.

Mots clés : maintenance prédictive, architecture des systèmes

Abstract Predictive maintenance aims at determining the right moment to trigger maintenance actions based on the health state of a system. Predictive maintenance is carried out by specialized systems whose design is still based on trial and error. Two of the main challenges in the development of predictive maintenance systems is the lack of a systematic approach to address their concept state, and the selection of suitable components to address the diagnostics and prognostics tasks. This research aims at proposing possible solutions to address these challenges. A systems engineering approach is proposed to address the concept stage, and a Decision Support System (DSS) is proposed to help the architect select suitable components based on previous successful predictive maintenance implementations. For the development of the DSS two technologies are integrated: Case-Based Reasoning and ontologies. The validation of the DSS includes the implementation of one of the suggested components by the DSS to fulfil a diagnostics tasks in a simulated jet-engine data case study.

Keywords: Predictive maintenance, systems architecture, knowledge reuse

ISAE-SUPAERO, 10 Avenue Edouard Belin Toulouse
