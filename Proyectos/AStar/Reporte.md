## Descripción general

Este código implementa el **algoritmo de búsqueda A*** (A Star) utilizando **Pygame** para mostrar de forma **gráfica e interactiva** cómo se calcula el camino más corto entre dos puntos dentro de una cuadrícula, considerando **obstáculos** y **movimientos diagonales**.

El objetivo principal es **visualizar paso a paso** el recorrido que sigue A* desde el nodo inicial hasta el nodo final.

## Estructura del programa

### 1. Configuración de la ventana y colores

Se crea una ventana cuadrada de 800×800 píxeles usando Pygame.
Los colores representan el estado de cada nodo:

* **Inicio** (naranja)
* **Fin** (púrpura)
* **Paredes** (negro)
* **Nodos abiertos** (verde)
* **Nodos cerrados** (rojo)
* **Camino final** (turquesa)

Esto permite entender visualmente el funcionamiento del algoritmo.

### 2. Clase `Nodo`

Cada celda del grid es un objeto `Nodo`.
Esta clase se encarga de:

* Guardar su **posición** (fila y columna).
* Saber si es **pared, inicio o fin**.
* Dibujarse en la ventana.
* Calcular y almacenar sus **vecinos válidos**.

Incluye movimientos:

* **Horizontales y verticales**
* **Diagonales**, evitando el “corte de esquinas” (no permite pasar en diagonal si dos paredes bloquean el paso).

### 3. Función heurística

Se utiliza una **heurística basada en la distancia euclidiana**, que estima qué tan lejos está un nodo del nodo final.
Esta estimación ayuda al algoritmo A* a decidir qué camino es más prometedor.

### 4. Implementación del algoritmo A*

La función `algoritmo_a_estrella` es el núcleo del programa:

* Usa una **cola de prioridad** para elegir siempre el nodo con menor costo estimado.
* Calcula:

  * **g(n)**: costo desde el inicio hasta el nodo actual.
  * **f(n)**: g(n) + heurística.
* Marca los nodos como:

  * **Abiertos** (explorados pero no finalizados).
  * **Cerrados** (ya evaluados).
* Guarda el recorrido para poder **reconstruir el camino final** cuando se llega al destino.

Todo el proceso se dibuja en tiempo real.

### 5. Reconstrucción del camino

Una vez que se alcanza el nodo final, se recorre el diccionario `vino_de` para marcar el **camino óptimo** desde el inicio hasta el fin, coloreándolo de turquesa.

### 6. Creación y dibujo del grid

Se genera una cuadrícula de 13×13 nodos:

* Cada nodo se dibuja como un cuadrado.
* Se dibujan líneas para separar visualmente las celdas.

### 7. Interacción con el usuario

El usuario puede interactuar con el algoritmo:

* **Click izquierdo**:

  * Primer click: nodo inicio
  * Segundo click: nodo fin
  * Clicks siguientes: paredes
* **Click derecho**: borra un nodo
* **Barra espaciadora**: ejecuta el algoritmo A*
* **Tecla R**: reinicia todo
* **Tecla C**: limpia solo el rastro del algoritmo

## Conclusión

En este código se implementó el **algoritmo A*** de forma completa y visual, permitiendo observar cómo:

* Se exploran nodos,
* Se evalúan costos,
* Se evitan obstáculos,
* Y se construye el camino más corto.

La integración con **Pygame** facilita la comprensión del algoritmo al mostrar gráficamente cada paso del proceso, lo que lo convierte en una herramienta ideal para **aprender y analizar** cómo funciona A* en la práctica.
