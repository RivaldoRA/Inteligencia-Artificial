## Descripción general

Este código implementa una **Red Neuronal Convolucional (CNN)** utilizando **TensorFlow/Keras** para realizar **reconocimiento y clasificación de imágenes**.
El modelo se entrena con un conjunto de imágenes organizadas por carpetas (una carpeta por clase) y aprende a identificar animales a partir de imágenes de **85×85 píxeles**.

El flujo completo incluye:

* Carga y etiquetado de imágenes
* Preprocesamiento de datos
* Entrenamiento del modelo CNN
* Evaluación del desempeño
* Predicción de nuevas imágenes

Perfecto, aquí tienes la **sección adicional** integrada y redactada con un estilo claro, formal y acorde a un **reporte académico o técnico**, manteniendo el mismo nivel de detalle que el resto de la explicación.

---

## Obtención del dataset

Para el entrenamiento de la Red Neuronal Convolucional se construyó un **dataset personalizado** a partir de diferentes fuentes, priorizando imágenes reales y variadas para mejorar la capacidad de generalización del modelo.

La **mayoría de las imágenes** fueron obtenidas de la plataforma **iNaturalist**, utilizando el dataset disponible a través de la página **IGIB**, de donde se recopilaron **alrededor de 100 000 imágenes** por categoría:

* Gatos
* Tortugas
* Mariquitas

La clase de **perros** no se obtuvo de iNaturalist, sino que fue tomada de un dataset público disponible en **Kaggle**, específicamente del conjunto conocido como **“Perros vs Gatos”**, del cual se extrajeron únicamente las imágenes correspondientes a perros.

Para el procesamiento de las imágenes, se utilizó un modelo de **detección de objetos YOLOv11**, proporcionado por la plataforma **Roboflow**. Este modelo permitió realizar de forma **automática** el recorte de los objetos de interés (gatos, perros, tortugas y mariquitas), ajustando todas las imágenes a una **resolución uniforme de 85×85 píxeles**, compatible con la arquitectura de la CNN.

En el caso de la clase **hormigas**, debido a la complejidad de las imágenes y a la baja precisión de detección automática, se realizó un **recorte manual** de aproximadamente **5 000 imágenes**, asegurando que el objeto de interés estuviera correctamente centrado y visible.

Este proceso de obtención y preprocesamiento del dataset permitió contar con un conjunto de datos **balanceado, limpio y consistente**, adecuado para el entrenamiento y evaluación del modelo de clasificación de imágenes.

---

## Estructura del programa

### 1. Importación de librerías

Se utilizan librerías para:

* **Procesamiento numérico**: NumPy
* **Manejo de archivos**: `os`, `re`
* **Visualización**: Matplotlib
* **Machine Learning**: TensorFlow y Keras
* **Evaluación**: métricas de clasificación de Scikit-learn

Esto permite manejar imágenes, construir el modelo y analizar resultados.

---

### 2. Carga del conjunto de imágenes

Las imágenes se leen desde una carpeta raíz que contiene **subcarpetas**, donde cada subcarpeta representa una **clase**.

El proceso:

* Se recorren las carpetas con `os.walk`
* Se filtran archivos con extensiones válidas de imagen
* Cada imagen se carga en memoria y se guarda en una lista
* Se registra cuántas imágenes hay por categoría

Al final se obtiene:

* Un arreglo `X` con las imágenes
* Una lista de etiquetas `y` asociadas a cada imagen

---

### 3. Creación de etiquetas

Las etiquetas se generan automáticamente:

* A cada carpeta se le asigna un índice numérico
* Todas las imágenes de esa carpeta reciben la misma etiqueta
* Se guarda el nombre de cada clase para interpretarlas después

Esto permite entrenar la red usando **clasificación multiclase**.

---

### 4. División del dataset

El conjunto de datos se divide en:

* **Entrenamiento (80%)**
* **Prueba (20%)**

Posteriormente, el conjunto de entrenamiento se divide nuevamente para crear:

* **Entrenamiento**
* **Validación**

Esto permite evaluar el modelo durante el entrenamiento y evitar sobreajuste.

---

### 5. Preprocesamiento de imágenes

Antes de entrenar:

* Las imágenes se convierten a tipo `float32`
* Se normalizan dividiendo entre 255 (valores entre 0 y 1)

Este paso mejora la estabilidad y velocidad del aprendizaje.

---

### 6. Construcción del modelo CNN

Se define una red convolucional profunda con **Keras Sequential**, compuesta por:

#### Bloques convolucionales

Cada bloque incluye:

* **Conv2D** para extraer características
* **LeakyReLU** como función de activación
* **BatchNormalization** para estabilizar el entrenamiento
* **MaxPooling2D** para reducir dimensiones
* **Dropout** para evitar sobreajuste

Se utilizan tres bloques con 32, 64 y 128 filtros respectivamente.

#### Capa de clasificación

* Se aplana la salida (`Flatten`)
* Capa densa intermedia
* Capa final con **Softmax**, que devuelve la probabilidad de cada clase

---

### 7. Compilación del modelo

El modelo se compila usando:

* **Función de pérdida**: `sparse_categorical_crossentropy`
* **Optimizador**: Adagrad
* **Métrica**: accuracy

Esto define cómo aprende la red y cómo se mide su rendimiento.

---

### 8. Entrenamiento del modelo

Durante el entrenamiento:

* Se usa **EarlyStopping** para detener el proceso si no hay mejora
* **ReduceLROnPlateau** ajusta el learning rate automáticamente
* **ModelCheckpoint** guarda el mejor modelo encontrado

El modelo aprende a reconocer patrones en las imágenes a lo largo de múltiples épocas.

---

### 9. Evaluación del modelo

Una vez entrenado:

* Se evalúa con el conjunto de prueba
* Se muestran métricas de **pérdida y precisión**
* Se grafican curvas de:

  * Accuracy (entrenamiento vs validación)
  * Loss (entrenamiento vs validación)

Esto permite analizar si el modelo aprendió correctamente.

---

### 10. Análisis de aciertos y errores

El código:

* Identifica imágenes correctamente clasificadas
* Muestra ejemplos visuales
* Analiza errores de clasificación
* Genera un **classification report** con precisión, recall y F1-score

Esto ayuda a entender en qué clases falla más el modelo.

---

### 11. Predicción de nuevas imágenes

El modelo entrenado se guarda y luego se reutiliza para:

* Clasificar una imagen individual
* Clasificar múltiples imágenes desde una carpeta

Cada imagen:

* Se redimensiona a 85×85
* Se convierte a RGB si es necesario
* Se normaliza
* Se pasa al modelo para obtener la clase y su nivel de confianza

---

## Conclusión

En este código se desarrolló un **sistema completo de clasificación de imágenes usando CNN**, cubriendo todo el flujo de trabajo de **Deep Learning**:

* Preparación del dataset
* Diseño y entrenamiento de una red convolucional
* Evaluación del desempeño
* Uso del modelo para predicciones reales

La implementación permite comprender de forma práctica cómo una CNN **aprende características visuales** y las utiliza para reconocer diferentes clases de imágenes, siendo una base sólida para proyectos más avanzados de **visión por computadora**.
