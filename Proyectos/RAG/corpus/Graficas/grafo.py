import networkx as nx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import os

# 1. Cargar el texto del corpus (si la variable 'fragmentos' no existe)
def cargar_corpus(ruta_archivo):
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            # Dividimos por el separador que usaste en tu script de scraping
            return f.read().split("--- FIN ---")
    else:
        print(f"Error: No se encontró {ruta_archivo}")
        return []

# 2. Definir los nodos (Conceptos Filosóficos y de la Gen Z)
# Estos conceptos responden a tus ejes de Han, Foucault y Bauman
conceptos = [
     'algorithm', 'ansiedad', 'anxiety', 'burnout', 
    'identidad', 'identity',  'void', 'tiktok', 
    'autonomy', 'vigilancia', 'surveillance', 
    'sentido', 'meaning', 'rendimiento', 'performance', 
     'purpose', 'soledad', 'loneliness', 'work', 'life'
]

# 3. Procesamiento
textos = cargar_corpus("../corpus_maestro_rag.txt")

if textos:
    # Creamos una matriz de co-ocurrencia: ¿qué palabras aparecen juntas?
    cv = CountVectorizer(vocabulary=conceptos, binary=True)
    matrix = cv.fit_transform(textos)
    
    # El producto de la matriz nos da las conexiones entre palabras
    co_occurrence = (matrix.T * matrix)
    co_occurrence.setdiag(0) # Quitamos la relación de una palabra consigo misma

    # 4. Construcción del Grafo
    G = nx.from_scipy_sparse_array(co_occurrence)
    labels = {i: concepto for i, concepto in enumerate(conceptos)}
    G = nx.relabel_nodes(G, labels)

    # Eliminar nodos que no tengan ninguna conexión para limpiar la gráfica
    nodos_aislados = [node for node, degree in dict(G.degree()).items() if degree == 0]
    G.remove_nodes_from(nodos_aislados)

    # 5. Visualización Estética
    plt.figure(figsize=(12, 10))
    # Layout de "resorte" para que los nodos relacionados se atraigan
    pos = nx.spring_layout(G, k=0.8, iterations=100)

    # Dibujar la red
    nx.draw_networkx_nodes(G, pos, node_size=2500, node_color='#40E0D0', alpha=0.9)
    nx.draw_networkx_edges(G, pos, width=1.5, edge_color='gray', alpha=0.3)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    plt.title("Grafo de Red: Interconexión de Crisis y Autonomía en la Gen Z")
    plt.axis('off')
    plt.savefig("grafo_red_conceptos.png")
    plt.show()