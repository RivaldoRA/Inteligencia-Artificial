## Descripción general

Este código implementa el **fine-tuning de un modelo de lenguaje LLaMA 3.2** utilizando **LoRA (Low-Rank Adaptation)** mediante la librería **Unsloth**, con el objetivo de crear un **modelo tutor especializado** a partir de ejemplos de código en Python.

El entrenamiento se realiza de forma eficiente usando **cuantización en 4 bits**, adaptadores LoRA y **GPUs rentadas en Vast.ai**, lo que permite acelerar el proceso y reducir el consumo de memoria.

---

## Estructura del programa

### 1. Importación de librerías

Se utilizan librerías especializadas en **entrenamiento de modelos de lenguaje**:

* `unsloth`: carga optimizada de modelos LLaMA y soporte para LoRA
* `transformers` y `trl`: entrenamiento supervisado (SFT)
* `datasets`: carga y procesamiento del dataset
* `torch`: manejo de GPU y precisión numérica

Estas herramientas permiten entrenar modelos grandes de manera eficiente.

---

### 2. Carga del modelo base

Se carga el modelo **LLaMA 3.2** en versión **cuantizada a 4 bits**, lo que reduce el uso de memoria sin sacrificar demasiado rendimiento.

Parámetros importantes:

* `max_seq_length = 2048`: longitud máxima de contexto
* `load_in_4bit = True`: optimización para GPUs con memoria limitada

Esto hace posible entrenar el modelo incluso en entornos alquilados.

---

### 3. Configuración de LoRA

Se agregan **adaptadores LoRA** al modelo base para ajustar su comportamiento sin modificar todos los pesos originales.

Características clave:

* Se aplica LoRA a capas internas críticas (`q_proj`, `k_proj`, `v_proj`, etc.)
* Se utiliza un valor de `r` y `lora_alpha` que permiten un aprendizaje significativo
* Se activa **gradient checkpointing** para reducir el uso de memoria

Gracias a LoRA, el entrenamiento es más rápido y ligero que un fine-tuning completo.

---

### 4. Formato tipo chat

El tokenizer se configura con un **template de conversación estilo LLaMA**, lo que permite entrenar el modelo en formato **pregunta–respuesta**.

La función `formatting_prompts_func`:

* Convierte los mensajes del dataset al formato esperado por el modelo
* Genera texto listo para entrenamiento supervisado

Esto es clave para que el modelo se comporte como un tutor conversacional.

---

## Obtención del dataset

El dataset utilizado para el entrenamiento fue obtenido de **Kaggle**, a partir de conjuntos de datos que contienen **ejemplos de código en Python**, diseñados para tareas de explicación, corrección y generación de código.

Debido a que **la mayoría del contenido original se encontraba en inglés**, se utilizó una **IA de lenguaje** para **traducir automáticamente los ejemplos al español**, asegurando coherencia técnica y manteniendo la estructura del código original. Este paso permitió adaptar el dataset al contexto del proyecto sin perder calidad en los ejemplos.

Posteriormente, los datos se organizaron en formato **JSONL**, estructurados como conversaciones (mensajes), compatibles con el entrenamiento tipo chat.

Para acelerar el proceso de entrenamiento y manejar modelos de gran tamaño, se **rentaron GPUs en la plataforma Vast.ai**, lo que permitió:

* Reducir significativamente los tiempos de entrenamiento
* Utilizar mayor capacidad de cómputo bajo demanda
* Experimentar con diferentes configuraciones sin depender de hardware local

---

### 5. Carga y preparación del dataset

El dataset se carga desde un archivo `dataset_tutor_final.jsonl` y se procesa para:

* Aplicar el formato de chat
* Convertir cada ejemplo en texto listo para el entrenamiento

Esto asegura que los datos estén alineados con el comportamiento esperado del modelo.

---

### 6. Configuración del entrenador

Se utiliza `SFTTrainer` para entrenamiento supervisado, con parámetros optimizados:

* Batch size pequeño con **gradient accumulation**
* Learning rate ajustado para mayor estabilidad
* Optimizador `adamw_8bit` para eficiencia
* Precisión automática `fp16` o `bf16` según soporte de GPU

Esta configuración permite entrenar de manera estable incluso con recursos limitados.

---

### 7. Entrenamiento del modelo

El modelo se entrena durante una época completa sobre el dataset, ajustando únicamente los parámetros LoRA.

Durante este proceso:

* Se optimiza la respuesta del modelo a preguntas técnicas
* Se refuerza su capacidad para explicar código en Python

---

### 8. Guardado del modelo

Finalmente, el modelo entrenado se guarda en formato **GGUF**, con cuantización `q8_0`, lo que permite:

* Reutilizar el modelo sin volver a entrenar
* Ejecutarlo en entornos locales o con frameworks como Ollama
* Mantener un tamaño de archivo reducido

---

## Conclusión

En este código se desarrolló un **modelo de lenguaje especializado** mediante fine-tuning eficiente, combinando:

* Modelos LLaMA cuantizados
* Adaptadores LoRA
* Dataset personalizado traducido con IA
* Entrenamiento acelerado con GPUs rentadas en Vast.ai

El resultado es un modelo tutor capaz de **comprender y explicar código en Python**, optimizado tanto en rendimiento como en consumo de recursos, y listo para ser utilizado en aplicaciones educativas o de asistencia técnica.
