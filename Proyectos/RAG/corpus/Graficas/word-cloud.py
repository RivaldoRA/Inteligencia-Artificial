import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords

def generar_nube_limpia(ruta_corpus, nombre_salida="nube_filosofica.png"):
    # 1. Cargar el texto del corpus
    with open(ruta_corpus, "r", encoding="utf-8") as f:
        texto = f.read().lower()

    # 2. Configurar Stop Words bilingües
    nltk.download('stopwords')
    stops_es = set(stopwords.words('spanish'))
    stops_en = set(stopwords.words('english'))
    
    # 3. Ruido detectado en tus imágenes actuales (filtros personalizados)
    ruido_reddit = {
        'like', 'people', 'think', 'get', 'one', 'year', 'make', 'even', 
        'deleted', 'removed', 'thing', 'know', 'say', 'would', 'really',
        'also', 'time', 'way', 'go', 'going', 'well', 'want', 'see',
        'documento', 'archivo', 'título', 'post', 'comentario', 'comentarios'
    }
    
    filtro_final = stops_es.union(stops_en).union(ruido_reddit)

    # 4. Configuración visual de la nube
    wc = WordCloud(
        width=1600, 
        height=800,
        background_color='white',
        colormap='magma',  # Colores más oscuros para temas existenciales
        stopwords=filtro_final,
        max_words=100,
        collocations=False
    ).generate(texto)

    # 5. Guardar y mostrar
    plt.figure(figsize=(20, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(nombre_salida, bbox_inches='tight')
    print(f"Nube guardada exitosamente en {nombre_salida}")
    plt.show()

if __name__ == "__main__":
    # Asegúrate de que el nombre del archivo coincida con tu corpus
    generar_nube_limpia("../corpus_maestro_rag.txt")