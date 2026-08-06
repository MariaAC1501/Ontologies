# Enfoque de validación y discusión

</div>

"Cuando quieras saber cómo funcionan realmente las cosas, estúdialas cuando se están desmoronando."

William Gibson

Contenido

7.1 Validación del Sistema de Soporte a la Decisión propuesto mediante un ejemplo práctico 109

7.2 Ejemplo de caso de uso: Diseño de un sistema de mantenimiento predictivo para un conjunto de datos de motores aeronáuticos con corrida hasta falla bajo condiciones reales de vuelo 109

7.3 La fase conceptual de un sistema de mantenimiento predictivo para la base de datos N-CMAPSS 111

7.4 Selección de componentes usando un sistema de recomendación basado en casos habilitado por ontologías 113

7.5 Discusión 117

7.6 Lecciones aprendidas de la validación del DSS usando N-CMAPSS 119

## 7.1 Validación del Sistema de Soporte a la Decisión propuesto mediante un ejemplo práctico

Como parte de la validación del marco de trabajo, se desarrolló un ejemplo de caso de uso. Este ejemplo utiliza un conjunto de datos de motores aeronáuticos [Cha+21]. El conjunto de datos contiene los registros de corrida hasta falla de 128 motores a reacción de aeronaves bajo condiciones reales de vuelo y fue generado con el modelo Commercial Modular Aero-Propulsion System Simulation (CMAPSS) desarrollado por la NASA. Este conjunto de datos se denomina N-CMAPSS. El propósito no es solo comprobar las capacidades del sistema CBR habilitado por ontologías propuesto, sino también identificar puntos de mejora para el DSS. El objetivo de esta validación es implementar uno de los modelos propuestos por el DSS para cumplir una función de mantenimiento predictivo para la base de datos N-CMAPSS. Esta implementación ayuda a demostrar que el DSS es capaz de sugerir componentes adecuados para sistemas de mantenimiento predictivo, complementando la validación cruzada presentada en el Capítulo 6.

## 7.2 Ejemplo de caso de uso: Diseño de un sistema de mantenimiento predictivo para un conjunto de datos de motores aeronáuticos con corrida hasta falla bajo condiciones reales de vuelo

El conjunto de datos N-CMAPSS fue publicado en enero de 2021 y tiene como objetivo facilitar el desarrollo de algoritmos especializados para aplicaciones de mantenimiento predictivo, proporcionando un conjunto completo de datos de corrida hasta falla con diferentes modos de falla. CMAPSS ha sido utilizado para simular otros conjuntos de datos conocidos con fines de pronóstico, como los datos PHM08 [Sax+08]. El conjunto de datos N-CMAPSS supone una mejora en el nivel de fidelidad entre los datos simulados y los datos de la vida real. Cada vuelo en el conjunto de datos N-CMAPSS se registra completamente desde el despegue hasta el aterrizaje. Las versiones anteriores de los conjuntos de datos CMAPSS ofrecían un enfoque más simple que solo proporcionaba una única medición discreta por cada vuelo del motor. Otra mejora puede observarse en la cantidad de modos de falla. Los conjuntos de datos CMAPSS anteriores solo tenían uno o dos modos de falla impuestos y, para aquellos con dos modos de falla, no existían registros explícitos que permitieran discriminar el modo de falla que afectaba a cada motor a reacción. El conjunto de datos N-CMAPSS tiene hasta siete modos de falla distintos y existe un registro explícito del modo de falla que afectó a cada motor. Cada modo de falla tiene su propio conjunto de síntomas que pueden identificarse por la pérdida de flujo (F) o eficiencia (E) en los componentes rotativos del motor, como el ventilador, el compresor de baja presión (LPC), el compresor de alta presión (HPC), la turbina de baja presión (LPT) y la turbina de alta presión (HPT). Esta mejora amplía el uso del conjunto de datos N-CMAPSS no solo para pronóstico, como los conjuntos de datos CMAPSS anteriores, sino también para diagnóstico.

Según [Cha+21], se siguieron cinco pasos principales para generar el conjunto de datos (véase la Figura 7.1):

1. Los datos de vuelo se definen según lo registrado a bordo de aviones comerciales reales.

2. La degradación de los componentes del motor se impone en la simulación para que sea posible rastrear el componente fallado en cada motor con corrida hasta falla.

3. El vuelo degradado resultante se simula usando CMAPSS.

4. Se evalúa la condición de salud y la unidad continúa volando con una degradación creciente hasta que el índice de salud del motor alcanza cero.

5. Se añade ruido de sensor a la respuesta simulada del motor para acercar los datos simulados a los de la vida real.

Las condiciones de vuelo se han dividido en tres clases según la duración del vuelo. La clase 1 incluye todos los vuelos que duran de una a tres horas. La clase 2 incluye todos los vuelos de entre tres y cinco horas de duración. La clase 3 incluye todos los vuelos que duran más de 5 horas. El conjunto de datos está dividido en 8 subconjuntos con distintos modos de falla y diferente número de unidades de motor. La Tabla 7.1 muestra una visión general del conjunto de datos N-CMAPSS. Cada subconjunto tiene su propio modo de falla, excepto el subconjunto DS02, que tiene 2 modos de falla, correspondientes a los subconjuntos SD01 y DS03, respectivamente. La visión general muestra los síntomas que describen cada modo de falla. Por ejemplo, el modo de falla del subconjunto DS01 puede detectarse por una disminución de la eficiencia en el HPC, mientras que el modo de falla del subconjunto DS04 puede detectarse por una disminución de la eficiencia y del flujo del ventilador del motor.

Cada unidad del conjunto de datos N-CMAPSS tiene una degradación inicial desconocida, lo que significa que los registros no comenzaron en el mismo punto para todas ellas. Los registros de cada motor en N-CMAPSS finalizan cuando el motor alcanza el estado de falla. Cada motor atraviesa una etapa de degradación normal en la que los síntomas de falla no son evidentes. Si aparece una falla en el motor, habrá una transición de la degradación normal a una degradación anormal, más rápida que la degradación normal hacia el estado de falla. Los datos están compuestos por 46 variables divididas en 5 grupos diferentes:

1. Descriptores de escenario: variables independientes de la operación del motor que se usan para describir los modos operativos del motor.

2. Mediciones: sensores que describen la operación del motor.

3. Sensores virtuales: mediciones complementarias ofrecidas por CMAPSS para evaluar la operación del motor.

4. Parámetros de salud del modelo: variables complementarias que muestran los síntomas de los diferentes modos de falla.

5. Variables auxiliares: variables para la consistencia del conjunto de datos.

Puede encontrarse una explicación adicional sobre el conjunto de datos N-CMAPSS en [Cha+21] y [FDL07].

> **Descripción de la figura:**
>
> Este diagrama ilustra un proceso cíclico de cinco pasos para simular la degradación de motores aeronáuticos, centrado en una flecha circular que indica el flujo de operaciones. El paso 1, "Definir condiciones de vuelo", muestra el logotipo de NASA DASHlink y la imagen de un avión. El paso 2, "Imponer degradación", incluye una gráfica de líneas que representa "HPT Eff. - θ [-]" en el eje y (de 0.000 a -0.015) frente a "Time [cycle]" en el eje x (de 0 a 100). La gráfica muestra diez líneas de colores que representan las unidades 1 a 10, todas con tendencia descendente a medida que aumenta el tiempo.
>
> El paso 3, "Simular vuelo degradado", muestra un esquema etiquetado como "CMAPSS Aircraft Engine Simulator", que representa los componentes internos de un motor a reacción, incluyendo el compresor de baja presión (LPC), el compresor de alta presión (HPC), la turbina de alta presión (HPT) y la turbina de baja presión (LPT), conectados por varios flujos y sensores. El paso 4, "Volar hasta la falla", presenta una gráfica de líneas que representa "Health Index H [-]" en el eje y (de 0.0 a 1.0) frente a "Time [cycle]" en el eje x (de 0 a 100). Esta gráfica también muestra diez líneas de colores para las unidades 1 a 10, todas mostrando una disminución del índice de salud con el tiempo. El paso 5, "Agregar ruido de sensor y almacenar", está representado por un ícono de documento con una cuadrícula de tabla, indicando la etapa final de procesamiento de datos antes de que el ciclo potencialmente se repita.

<div align="center">

Figura 7.1: Proceso de creación de datos N-CMAPSS [Cha+21]

</div>

## 7.3 La fase conceptual de un sistema de mantenimiento predictivo para la base de datos N-CMAPSS

Dado que N-CMAPSS está orientado a fines de investigación, corresponde a los investigadores definir la lista de necesidades y deseos para el nuevo sistema de mantenimiento predictivo. Para el marco de investigación actual, se propone la siguiente lista de necesidades y deseos:

1. Leer el formato de datos N-CMAPSS.

2. Identificar las variables necesarias para realizar diagnóstico y pronóstico.

<div align="center">

Tabla 7.1: Visión general del conjunto de datos N-CMAPSS [Cha+21]

</div>

<table border="1"><tr><td rowspan="2">Nombre</td><td rowspan="2">#Unidades</td><td rowspan="2">Clases de vuelo</td><td rowspan="2">Modos de falla</td><td colspan="2">Fan</td><td colspan="2">LPC</td><td colspan="2">HPC</td><td colspan="2">HPT</td><td colspan="2">LPT</td><td rowspan="2">Tamaño(medidas)</td></tr><tr><td>E</td><td>F</td><td>E</td><td>F</td><td>E</td><td>F</td><td>E</td><td>F</td><td>E</td><td>F</td></tr><tr><td>DS01</td><td>10</td><td>1,2,3</td><td>1</td><td></td><td></td><td></td><td></td><td></td><td></td><td>√</td><td></td><td></td><td></td><td>7.6M</td></tr><tr><td>DS02</td><td>9</td><td>1,2,3</td><td>2</td><td></td><td></td><td></td><td></td><td></td><td></td><td>√</td><td></td><td>√</td><td>√</td><td>6.5M</td></tr><tr><td>DS03</td><td>15</td><td>1,2,3</td><td>1</td><td></td><td></td><td></td><td></td><td></td><td></td><td>√</td><td></td><td>√</td><td>√</td><td>9.8M</td></tr><tr><td>DS04</td><td>10</td><td>2,3</td><td>1</td><td>√</td><td>√</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>10.0M</td></tr><tr><td>DS05</td><td>10</td><td>1,2,3</td><td>1</td><td></td><td></td><td></td><td></td><td>√</td><td>√</td><td></td><td></td><td></td><td></td><td>6.9M</td></tr><tr><td>DS06</td><td>10</td><td>1,2,3</td><td>1</td><td></td><td></td><td>√</td><td>√</td><td>√</td><td>√</td><td></td><td></td><td></td><td></td><td>6.8M</td></tr><tr><td>DS07</td><td>10</td><td>1,2,3</td><td>1</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>√</td><td>√</td><td>7.2M</td></tr><tr><td>DS08</td><td>54</td><td>1,2,3</td><td>1</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>35.6M</td></tr></table>

3. Preprocesar y reducir el conjunto de datos N-CMAPSS.

4. Detectar la transición de degradación normal a degradación anormal.

5. Identificar el modo de falla que conduce al motor a fallar.

6. Determinar el estado actual de un motor a reacción.

7. Estimar la vida útil remanente de un motor a reacción.

8. Proporcionar un informe de resultados.

La lista anterior de necesidades y deseos se traduce en la siguiente lista de requisitos funcionales:

1. El sistema deberá leer el conjunto de datos N-CMAPSS.

2. El sistema deberá modelar la salud del motor a reacción.

4. El sistema deberá evaluar el estado de salud del motor.

3. El sistema deberá detectar fallas incipientes en el motor.

5. El sistema deberá estimar la vida útil remanente del motor.

6. El sistema deberá proporcionar un informe de los resultados del mantenimiento predictivo.

En el primer concepto del sistema de mantenimiento predictivo, el preprocesamiento y la reducción de datos no están incluidos y se realizaron manualmente. Como puede verse, solo se determinaron requisitos funcionales. N-CMAPSS no proporciona necesidades de desempeño, restricciones estructurales ni necesidades experienciales, lo que significa que no se añadieron requisitos conductuales, estructurales o experienciales. Como el conjunto de datos proviene de un caso de estudio académico, no se agregaron necesidades o deseos experienciales. Es importante notar que, en aplicaciones prácticas, estos tres tipos de requisitos son importantes, ya que proporcionan los requisitos relacionados con el desempeño esperado del sistema, las interfaces con otros sistemas relacionados y la interfaz con el usuario del sistema.

Dados los requisitos funcionales, se siguió el proceso de arquitectura presentado en el Capítulo 3 hasta obtener una arquitectura lógica del nuevo sistema de mantenimiento predictivo. La Figura 7.2 presenta la arquitectura lógica desarrollada a partir de los requisitos funcionales previamente listados. Un primer componente recogerá los datos procesados de los registros del motor a reacción. Estos datos se utilizarán para desarrollar el modelo de salud del motor. Posteriormente, los datos del motor y el modelo de salud son utilizados por los componentes encargados de evaluar el estado de salud, detectar fallas incipientes e identificar dichas fallas. Las salidas de estos tres componentes son la entrada para el componente del sistema encargado de la estimación de la vida útil remanente. La evaluación de salud, la detección de fallas, la identificación de fallas y el cálculo de la vida útil remanente proporcionarán la información necesaria para elaborar el informe de mantenimiento predictivo mediante el último componente del sistema. Las funciones de cada componente del sistema de mantenimiento predictivo se asignaron de forma que coincidieran con las definiciones establecidas en la ontología y en el Sistema de Soporte a la Decisión (DSS), para que fuera posible recuperar las recomendaciones correspondientes.

> **Descripción de la figura:**
>
> Este diagrama ilustra la arquitectura de un sistema de mantenimiento predictivo, organizado en cinco módulos principales. En el nivel superior, el "Sistema de mantenimiento predictivo" contiene el "Módulo de recolección de datos", el "Módulo de detección de fallas", el "Módulo de modelado/evaluación de salud", el "Módulo de identificación de fallas", el "Módulo de vida útil remanente" y el "Módulo de reporte".
>
> El "Módulo de recolección de datos" contiene una función de "Recolectar datos" que envía "Datos del motor" al "Módulo de detección de fallas", al "Módulo de modelado/evaluación de salud" y al "Módulo de identificación de fallas". El "Módulo de detección de fallas" contiene una función de "Detectar falla" que produce una "falla detectada" para el "Módulo de vida útil remanente" y el "Módulo de reporte". El "Módulo de modelado/evaluación de salud" contiene dos funciones: "Modelar la evolución de la salud del motor", que produce un "Índice de salud" para el "Módulo de identificación de fallas" y el "Módulo de vida útil remanente", y "Evaluar estado de salud", que produce un "Estado de salud" para el "Módulo de reporte". La función "Modelar la evolución de la salud del motor" también produce "Modelo de salud e índice de salud" para la función "Evaluar estado de salud".
>
> El "Módulo de identificación de fallas" contiene una función "Identificar falla (modo de falla)" que recibe "Datos del motor" e "Índice de salud" como entradas y produce una "falla identificada" para el "Módulo de vida útil remanente" y el "Módulo de reporte". El "Módulo de vida útil remanente" contiene una función "Estimar la RUL del motor" que recibe "falla detectada", "falla identificada" e "Índice de salud" como entradas, y produce "RUL". Finalmente, el "Módulo de reporte" contiene una función "Generar informe" que recibe "falla detectada", "falla identificada", "estado de salud" y "RUL" como entradas. Las conexiones están representadas por líneas con flechas que indican el flujo de datos entre las funciones específicas de cada módulo.

<div align="center">

Figura 7.2: La arquitectura lógica de un sistema de mantenimiento predictivo para el conjunto de datos N-CMAPSS

</div>

## 7.4 Selección de componentes usando un sistema de recomendación basado en casos habilitado por ontologías

Considerando la arquitectura lógica presentada en la Figura 7.2, existen cuatro componentes lógicos diferentes para los cuales el Sistema de Soporte a la Decisión puede proporcionar sugerencias:

- Módulo de modelado/evaluación de salud

- Módulo de detección de fallas

- Módulo de identificación de fallas

- Módulo de estimación de vida útil remanente

Para cada uno de estos cuatro componentes lógicos, se realizó una recuperación de posibles soluciones usando el DSS propuesto. Los resultados de las recuperaciones se resumen en la Tabla 7.2. El DSS es capaz de proporcionar la similitud de cada uno de los casos de la base de casos, pero los casos más similares tendrán mayor relevancia. Para los fines de análisis y presentación de la Tabla 7.2, solo se consideran las cinco similitudes más altas para cada función de mantenimiento predictivo.

Los resultados de la Tabla 7.2 demuestran las capacidades del DSS para recuperar soluciones adecuadas para cada uno de los componentes lógicos. Todos los modelos propuestos pueden adaptarse para cumplir la función prevista. Todas las similitudes entre el caso objetivo y los casos recuperados fueron superiores a 0.776, lo que significa que la similitud global entre los modelos propuestos y el caso objetivo fue al menos de 77.6 %. Una oportunidad de mejora para investigaciones futuras puede verse en aquellos casos recuperados con exactamente la misma similitud; se necesitaría información adicional para seleccionar el más adecuado. Por ejemplo, para el módulo de estimación de vida útil remanente, el DSS propuso cinco modelos posibles con el mismo valor de similitud; ningún modelo quedó clasificado por encima de otro. Un arquitecto necesitará información adicional para realizar el análisis de compromiso y seleccionar el modelo más adecuado para implementar. Pueden añadirse medidas de similitud adicionales para refinar el proceso de recuperación. Es importante no olvidar que, en un primer intento, el DSS está destinado a proporcionar soluciones adecuadas, pero aún queda una cantidad considerable de trabajo para que el DSS sea capaz de sugerir la más adecuada entre las demás.

Es importante notar que la similitud ontológica permitió proponer algunos modelos utilizados originalmente para identificación de fallas a fin de cumplir funciones de detección de fallas y viceversa. Esta similitud inferida es precisa, ya que ambas funciones están relacionadas con tareas de clasificación. Al añadir más casos a la base de casos, pueden encontrarse más similitudes semánticas como esta. Los valores actuales de similitud son bajos, ya que la diversidad en la base de casos es alta en comparación con el tamaño de la base. Puede encontrarse una explicación adicional sobre la similitud semántica en [MHMJV21], una publicación de conferencia realizada en el marco de la presente investigación e incluida en el Apéndice B.

Con el fin de validar aún más las recomendaciones del DSS, se tomó como ejemplo uno de los modelos sugeridos y se implementó para cumplir la función de mantenimiento predictivo correspondiente. Aprovechando la experiencia del equipo de investigación en mapas autoorganizados (SOM), se realizó una implementación del componente de modelado de salud usando SOM. El DSS recomienda SOM y regresión logística para el modelado de salud como los modelos más adecuados (similitud igual a 0.897) para el caso de estudio N-CMAPSS. La siguiente sección proporciona explicaciones adicionales sobre el ejemplo de implementación con SOM y sus resultados preliminares.

La metodología para implementar los mapas autoorganizados (SOM) para modelado de salud fue adoptada de [Sch+20] (véase el Apéndice A). Los mapas autoorganizados son redes neuronales artificiales con entrenamiento no supervisado que son capaces de agrupar instancias de datos según los atributos de dichas instancias. Un SOM normalmente está compuesto por una capa cuadrada de neuronas y los diferentes clústeres después del entrenamiento pueden representarse gráficamente en los mapas como regiones bien definidas. Se ha utilizado con éxito para modelar el proceso de degradación de distintas máquinas, como motores a reacción [MV18]. En estos casos, las neuronas representan la salud o degradación de la máquina en un modo operativo específico. El SOM entrenado tendrá una sola región, pero con una transición del blanco (estado óptimo) al negro (estado fallido). Al evaluar la salud o degradación de una máquina usando el SOM entrenado, se activará una neurona en el mapa que mostrará qué tan avanzada está la degradación o cuánto ha disminuido la salud. Ese es el objetivo real de la implementación actual: obtener un SOM entrenado capaz de mostrar una transición desde el estado óptimo hasta el estado fallido.

En un primer intento, se seleccionó una implementación simplificada. Para entrenar el SOM, solo se utiliza un subconjunto de los datos N-CMAPSS. Se seleccionó el DS01 porque tiene un solo modo de falla. El primer reto en la adaptación de la solución SOM a la base de datos N-CMAPSS está relacionado con los modos operativos. Para entrenar el SOM, los diferentes modos operativos deben poder distinguirse entre sí; desafortunadamente, N-CMAPSS no está enfocado en los diferentes modos operativos del motor, sino en toda la envolvente de vuelo. Para resolver este reto, se definió un modo operativo cuando el motor alcanza los 10000 pies de altitud mientras la aeronave está ascendiendo. En ese modo operativo, el ángulo del resolver de aceleración siempre será mayor al 70 % y el número Mach del vuelo siempre estará en el mismo intervalo. Estas tres variables se presentan en N-CMAPSS como descriptores de escenario y son independientes de la operación del motor.

Un segundo reto en la adaptación del SOM para N-CMAPSS estuvo relacionado con las variables seleccionadas para el entrenamiento. N-CMAPSS está compuesto por 45 variables diferentes de distinta naturaleza: descriptores de escenario, mediciones operativas del motor, sensores virtuales y parámetros de salud del modelo. Para la implementación actual, solo se han seleccionado los descriptores de escenario y las mediciones operativas del motor (véase la Tabla 7.3), ya que representan las variables que pueden obtenerse de motores aeronáuticos reales. Los sensores virtuales y los parámetros de salud del modelo forman parte de la simulación y de la consistencia del modelo, pero no estarían disponibles en motores a reacción reales.

<div align="center">

Tabla 7.2: Recuperación de modelos para los ejemplos N-CMAPSS

</div>

<table border="1"><tr><td>Función del caso objetivo</td><td>Caso</td><td>Función PdM</td><td>Modelo</td><td>Similitud</td></tr><tr><td rowspan="5">Detección de fallas</td><td>166</td><td>Detección de fallas</td><td>Clasificador de proceso gaussiano</td><td>0.859</td></tr><tr><td>211</td><td>Detección de fallas</td><td>Modelo lineal por tramos (PWL), filtro de Kalman híbrido, modelo OBEM</td><td>0.834</td></tr><tr><td>49</td><td>Identificación de fallas</td><td>Máquinas de vectores de soporte</td><td>0.776</td></tr><tr><td>48</td><td>Identificación de fallas</td><td>Red de creencias profundas</td><td>0.776</td></tr><tr><td>50</td><td>Identificación de fallas</td><td>Red neuronal perceptrón multicapa</td><td>0.776</td></tr><tr><td rowspan="5">Identificación de fallas</td><td>48</td><td>Identificación de fallas</td><td>Red de creencias profundas</td><td>0.859</td></tr><tr><td>50</td><td>Identificación de fallas</td><td>Red neuronal perceptrón multicapa</td><td>0.859</td></tr><tr><td>49</td><td>Identificación de fallas</td><td>Máquinas de vectores de soporte</td><td>0.859</td></tr><tr><td>212</td><td>Detección de fallas</td><td>Modelo lineal por tramos (PWL), filtro de Kalman híbrido, modelo OBEM</td><td>0.834</td></tr><tr><td>166</td><td>Detección de fallas</td><td>Clasificador de proceso gaussiano</td><td>0.794</td></tr><tr><td rowspan="5">Modelado/evaluación de salud</td><td>12</td><td>Modelado de salud</td><td>Mapas autoorganizados</td><td>0.897</td></tr><tr><td>1</td><td>Modelado de salud</td><td>Regresión logística</td><td>0.897</td></tr><tr><td>57</td><td>Modelado de salud</td><td>Modelo de regresión estadística</td><td>0.854</td></tr><tr><td>159</td><td>Modelado de salud</td><td>Cadenas ocultas de Markov</td><td>0.852</td></tr><tr><td>168</td><td>Modelado de salud</td><td>Muestreo basado en cópulas</td><td>0.838</td></tr><tr><td rowspan="5">Estimación de vida útil remanente</td><td>51</td><td>Estimación de vida útil remanente</td><td>LSTM (red neuronal Long-Short Term Memory)</td><td>0.895</td></tr><tr><td>53</td><td>Estimación de vida útil remanente</td><td>Red neuronal recurrente</td><td>0.895</td></tr><tr><td>54</td><td>Estimación de vida útil remanente</td><td>Red de unidades recurrentes con compuertas</td><td>0.895</td></tr><tr><td>62</td><td>Estimación de vida útil remanente</td><td>Máquina de vectores de relevancia</td><td>0.895</td></tr><tr><td>64</td><td>Estimación de vida útil remanente</td><td>Regresión lineal bayesiana</td><td>0.895</td></tr></table>

<div align="center">

Tabla 7.3: Mediciones operativas N-CMAPSS

</div>

<table border="1"><tr><td>Símbolo</td><td>Descripción</td><td>Unidades</td></tr><tr><td>Wf</td><td>Flujo de combustible</td><td>pps</td></tr><tr><td>Nf</td><td>Velocidad física del ventilador</td><td>rpm</td></tr><tr><td>Nc</td><td>Velocidad física del núcleo</td><td>rpm</td></tr><tr><td>T24</td><td>Temperatura total a la salida del LPC</td><td>°R</td></tr><tr><td>T30</td><td>Temperatura total a la salida del HPC</td><td>°R</td></tr><tr><td>T48</td><td>Temperatura total a la salida del HPT</td><td>°R</td></tr><tr><td>T50</td><td>Temperatura total a la salida del LPT</td><td>°R</td></tr><tr><td>P2</td><td>Presión total a la entrada del ventilador</td><td>psia</td></tr><tr><td>P15</td><td>Presión total en el conducto de derivación</td><td>psia</td></tr><tr><td>P21</td><td>Presión total a la salida del ventilador</td><td>psia</td></tr><tr><td>P24</td><td>Presión total a la salida del LPC</td><td>psia</td></tr><tr><td>Ps30</td><td>Presión estática a la salida del HPC</td><td>psia</td></tr><tr><td>P40</td><td>Presión total a la salida del quemador</td><td>psia</td></tr><tr><td>P50</td><td>Presión total a la salida del LPT</td><td>psia</td></tr></table>

LPC: compresor de baja presión

HPC: compresor de alta presión

LPT: turbina de baja presión

HPT: turbina de alta presión

Para aumentar las posibilidades de convergencia en el entrenamiento del SOM, es aconsejable añadir las entradas más representativas. Una buena práctica consiste en eliminar todas las variables que presentan un comportamiento binario o constante, ya que no aportan información útil sobre la degradación. También se recomienda una prueba de correlación entre variables para evitar añadir variables redundantes al entrenamiento del SOM. Ambas pruebas se realizaron sobre las mediciones operativas. Ninguna variable presentó registros constantes o binarios. La Figura 7.3 muestra una matriz de correlación para las mediciones operativas en la que las mismas variables aparecen en los ejes horizontal y vertical; el valor de correlación se muestra en la intersección de ambos ejes. Se estableció un umbral de correlación en 0.9. Si dos o más variables tienen una correlación mayor que el umbral, solo una de ellas se seleccionará al azar, ya que proporcionarán casi la misma información. Es importante señalar que antes de la prueba de correlación, todas las variables fueron normalizadas entre 0 y 1, lo cual también es un requisito para el entrenamiento del SOM [Sch+20]. Después de realizar la evaluación de variables, solo cuatro de ellas fueron seleccionadas para entrenar el mapa, lo que representa una reducción en el número de variables en comparación con el estudio del Apéndice A:

1. Temperatura total a la salida del compresor de baja presión (LPC).

2. Temperatura total a la salida de la turbina de alta presión (HPT).

3. Presión total a la entrada del ventilador.

4. Presión total a la salida de la turbina de baja presión (LPT).

Una vez seleccionadas y normalizadas las variables, puede comenzar el entrenamiento del SOM. Dado el tamaño de los datos, se seleccionó un mapa de 5x5 neuronas con arquitectura cuadrada. Se entrenaron varios SOM y su convergencia y comportamiento fueron confirmados en los resultados. La Figura 7.4 muestra un ejemplo de un mapa entrenado usando los datos extraídos de la base de datos N-CMAPSS. La neurona más clara representa la condición óptima de operación del motor y la neurona roja más oscura representa la condición del motor justo antes de su falla. Un motor evaluado con este SOM activará una neurona entre estos dos límites y su degradación podrá estimarse usando los pesos de la neurona. En la representación gráfica del SOM puede observarse una transición de tonos claros a oscuros. Esto representa la degradación del motor en el modo operativo seleccionado. Para más explicaciones sobre el entrenamiento e interpretación del SOM, véase el artículo del Apéndice A.

> **Descripción de la figura:**
>
> Esta imagen es un mapa de calor de correlación que muestra las relaciones entre 14 variables: T24, T30, T48, T50, P15, P2, P21, P24, Ps30, P40, P50, Nf, Nc y Wf. Las variables están listadas tanto en el eje vertical y como en el eje horizontal x. El mapa de calor utiliza una escala de color que va de beige claro (cerca de 0.0) a marrón oscuro (cerca de 1.0), con una barra de color a la derecha que indica valores en 0.2, 0.4, 0.6 y 0.8. Cada celda contiene el coeficiente numérico de correlación entre la variable de la fila y la de la columna correspondiente.
>
> La matriz es simétrica con una diagonal de 1. Los valores son los siguientes: Fila T24: 1, 0.94, 0.85, 0.68, 0.94, 0.48, 0.94, 0.99, 0.95, 0.94, 0.84, 0.93, 0.91, 0.95. Fila T30: 0.94, 1, 0.8, 0.61, 0.86, 0.26, 0.86, 0.93, 0.99, 0.99, 0.88, 0.99, 0.99, 0.96. Fila T48: 0.85, 0.8, 1, 0.95, 0.7, 0.15, 0.7, 0.81, 0.81, 0.8, 0.74, 0.85, 0.73, 0.93. Fila T50: 0.68, 0.61, 0.95, 1, 0.55, 0.11, 0.55, 0.65, 0.63, 0.62, 0.63, 0.67, 0.52, 0.8. Fila P15: 0.94, 0.86, 0.7, 0.55, 1, 0.71, 1, 0.98, 0.89, 0.89, 0.88, 0.8, 0.84, 0.85. Fila P2: 0.48, 0.26, 0.15, 0.11, 0.71, 1, 0.71, 0.57, 0.33, 0.33, 0.44, 0.16, 0.26, 0.26. Fila P21: 0.94, 0.86, 0.7, 0.55, 1, 0.71, 1, 0.98, 0.89, 0.89, 0.88, 0.8, 0.84, 0.85. Fila P24: 0.99, 0.93, 0.81, 0.65, 0.98, 0.57, 0.98, 1, 0.95, 0.95, 0.9, 0.9, 0.9, 0.93. Fila Ps30: 0.95, 0.99, 0.81, 0.63, 0.89, 0.33, 0.89, 0.95, 1, 1, 0.92, 0.97, 0.99, 0.97. Fila P40: 0.94, 0.99, 0.8, 0.62, 0.89, 0.33, 0.89, 0.95, 1, 1, 0.92, 0.97, 0.99, 0.97. Fila P50: 0.84, 0.88, 0.74, 0.63, 0.88, 0.44, 0.88, 0.9, 0.92, 0.92, 1, 0.84, 0.86, 0.9. Fila Nf: 0.93, 0.99, 0.85, 0.67, 0.8, 0.16, 0.8, 0.9, 0.97, 0.97, 0.84, 1, 0.97, 0.97. Fila Nc: 0.91, 0.99, 0.73, 0.52, 0.84, 0.26, 0.84, 0.9, 0.99, 0.99, 0.86, 0.97, 1, 0.93. Fila Wf: 0.95, 0.96, 0.93, 0.8, 0.85, 0.26, 0.85, 0.93, 0.97, 0.97, 0.9, 0.97, 0.93, 1.

<div align="center">

Figura 7.3: Matriz de correlación de los sensores del conjunto de datos N-CMAPSS que se usarán como entrada para el SOM

</div>

## 7.5 Discusión

Es importante recordar que la validación de un Sistema de Soporte a la Decisión (DSS) no es una tarea trivial. La validación del modelo implementado sugerido por el DSS puede utilizarse para validar indirectamente el DSS, pero se requerirían implementaciones adicionales para confirmar las capacidades y la precisión del DSS propuesto para la selección de modelos de mantenimiento predictivo. En la implementación actual, N-CMPASS representa el caso objetivo para el cual debe desarrollarse un nuevo sistema de mantenimiento predictivo. El sistema de recomendación CBR habilitado por ontologías (también llamado DSS en este manuscrito) propuso diferentes modelos para cumplir cada función de mantenimiento predictivo. Uno de los modelos propuestos por el DSS para la función de modelado de salud fue el mapa autoorganizado (SOM). La implementación del SOM mostró exitosamente la tendencia de degradación de los motores a reacción desde la operación nominal hasta la condición de falla usando un subconjunto de N-CMPASS. El SOM entrenado también puede utilizarse para evaluar la salud/degradación de otros motores del mismo tipo y bajo las mismas condiciones de operación. Es importante aclarar que esta validación busca demostrar la idoneidad del modelo propuesto por el DSS, pero se necesitan comparaciones adicionales entre los modelos sugeridos para determinar cuál es el mejor. Durante la validación cruzada presentada en el Capítulo 6 y la validación actual basada en la implementación del SOM, se identificaron varios puntos de mejora:

> **Descripción de la figura:**
>
> La imagen es un mapa de calor titulado "Dataset" que muestra una cuadrícula de 5x5 valores representados por distintos tonos de rojo, donde los tonos más claros indican valores más bajos y los más oscuros indican valores más altos. Tanto el eje x como el eje y están etiquetados con enteros del 0 al 4. La cuadrícula está organizada de modo que los valores aumentan al moverse desde la esquina inferior izquierda hacia la esquina superior derecha. Específicamente, la celda inferior izquierda (0,0) es la de color más claro, mientras que la celda superior derecha (4,4) es la más oscura. La intensidad del color rojo aumenta progresivamente tanto a lo largo de las filas como de las columnas, creando un efecto de gradiente en el que los valores más altos se concentran en el cuadrante superior derecho de la matriz.

<div align="center">

Figura 7.4: SOM entrenado para el subconjunto DS01

</div>

- Problemas con la diversidad de los casos recuperados: aunque no fue el caso para este estudio N-CMAPSS, en algunas recuperaciones de la validación cruzada el DSS propuso el mismo modelo varias veces con diferentes referencias en la base de casos. Esto constituye un problema desde el punto de vista de la ingeniería de sistemas. Un arquitecto que busque soluciones innovadoras necesita una lista diversa de posibles soluciones por parte del DSS. Puede realizarse trabajo adicional para evitar este problema de diversidad. La generalización de casos y otras técnicas de diversidad de casos pueden aplicarse para superar este problema [De +05]. Tal situación también podría atribuirse a un problema potencial de cobertura del espacio de soluciones. Si los casos almacenados corresponden solo a una pequeña porción del espacio de soluciones, los modelos sugeridos por el DSS pueden ser muy similares. Para el estudio actual, este no es el caso; se han considerado modelos de todo el espacio de soluciones. El estudio del estado del arte del Capítulo 2 permitió determinar que el espacio de soluciones para sistemas de mantenimiento predictivo está compuesto por modelos basados en datos, modelos basados en conocimiento, modelos basados en física y enfoques multimodelo que combinan al menos dos modelos de cualquiera de las tres familias mencionadas. La base de casos del DSS se construyó considerando todo el espacio de soluciones, pero la validación mostró que esto puede mejorarse. Puede realizarse un refinamiento del espacio de soluciones con respecto a cada función de mantenimiento predictivo. Para funciones de diagnóstico como, por ejemplo, "extracción de características", solo se identificaron modelos basados en datos al crear la base de casos. Otro ejemplo puede verse en la función "estimación de vida útil remanente", donde solo se identificaron modelos basados en datos y en física. Un refinamiento del espacio de soluciones considerando cada función de mantenimiento predictivo por separado puede ayudar a mejorar la base de casos y la diversidad de los modelos recuperados con el DSS.

- Información adicional para realizar el análisis de compromiso: varios modelos recuperados para la misma función de mantenimiento predictivo tienen la misma similitud. Implementar varias soluciones usando distintos modelos que tienen la misma similitud no siempre será factible por limitaciones de tiempo y recursos. Esto plantea un desafío para el arquitecto al seleccionar el más adecuado. Podrían añadirse otros atributos al caso para que la información recuperada pueda usarse para realizar un análisis de compromiso, de modo que el DSS ayude al arquitecto a tomar una decisión precisa respecto a la selección del modelo. Indicadores de desempeño, potencia computacional requerida, complejidad de implementación y costo de implementación son algunos ejemplos de variables complementarias que pueden ayudar a evaluar los modelos propuestos por el DSS. Los atributos adicionales también pueden utilizarse para incluir las preferencias o restricciones iniciales establecidas por el usuario del DSS desde el comienzo. Algunos usuarios pueden estar interesados solo en modelos basados en datos; entonces la solución podría limitarse antes de la recuperación de modelos.

- Información sobre la adaptación del modelo propuesto: la versión actual del DSS puede mejorarse incluyendo información adicional para la adaptación del modelo sugerido al caso objetivo. Esto no solo es útil para el análisis de compromiso, sino también para la etapa de diseño detallado e implementación del sistema de mantenimiento predictivo. La implementación del SOM para modelado de salud ha mostrado que algunos hiperparámetros de los modelos deben cambiarse. Puede añadirse una guía complementaria para la adaptación de los modelos sugeridos con el fin de facilitar su implementación en el caso objetivo. Un sistema experto podría guiar al arquitecto con los pasos de adaptación para cada modelo. Por limitaciones de tiempo, esto no fue posible en la presente investigación.

## 7.6 Lecciones aprendidas de la validación del DSS usando N-CMAPSS

La validación del DSS propuesto para la selección de componentes de mantenimiento predictivo se presentó en este capítulo. Las capacidades del DSS fueron probadas mediante la implementación de uno de los modelos sugeridos para modelado de salud en el caso de estudio N-CMAPSS. Esta validación ayudó a demostrar no solo que el DSS propuesto es capaz de sugerir componentes adecuados para sistemas de mantenimiento predictivo, sino que también permitió identificar puntos de mejora del DSS. Un DSS es difícil de validar con una cantidad limitada de datos y con un número limitado de implementaciones de los modelos sugeridos, pero el éxito en la implementación del SOM para el modelado de salud del caso de estudio N-CMAPSS valida indirectamente las capacidades del DSS. En el siguiente y último capítulo, las lecciones aprendidas de la investigación se resumen en las conclusiones y en las perspectivas de trabajo futuro propuestas.

Intencionalmente dejado en blanco

<div align="center">
