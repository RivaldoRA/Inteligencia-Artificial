# Analisis preeliminar del dataset
A primera estancia el dataset esta dividio en dos partes, Generación Z y la nueva película de Guillermo del Toro "Frankenstein". El dataset cuenta con las siguientes columnas: ID, Categoria, Tituo, Medio, Fecha, Resumen, Comentario_Reaccion.

Analizando el dataset al ordenar las columnas y los medios de la A a la Z nos permite ver las columnas de manera ordenada 

El dataset cuenta con un error donde dos registros tienen una coma en el título, provocando que se cree una columna de más y los datos estén desalineados

La única conexión notoria entre los dos temas es un comentario que dice "La Gen Z se identifica mucho con el Monstruo, un marginado incomprendido.",

# Procesamiento de Lenguaje Natural (PLN)
Las columnas de texto (Titulo, Resumen, Comentario_Reaccion) requieren técnicas específicas para extraer información significativa:

**Limpieza de Texto:** Eliminar caracteres especiales, signos de puntuación, convertir a minúsculas, y eliminar palabras vacías (stop words).

**Vectorización:** Convertir el texto en un formato numérico que los algoritmos puedan entender, utilizando técnicas como:

- Bag-of-Words (BoW) o TF-IDF (Frecuencia de Término - Frecuencia Inversa de Documento).
- Word Embeddings (como Word2Vec o GloVe) para capturar el contexto semántico de las palabras. 