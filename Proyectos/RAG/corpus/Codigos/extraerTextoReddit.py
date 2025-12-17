from bs4 import BeautifulSoup
import os
import glob

def extraer_datos_limpios(ruta_html):
    """Extrae título, post y comentarios filtrando bots y palabras clave."""
    with open(ruta_html, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

    # 1. Título
    titulo = soup.find('title').get_text(strip=True) if soup.find('title') else "Sin título"
    
    # 2. Post Principal
    post_elem = soup.find('shreddit-post')
    texto_post = "\n".join([p.get_text(strip=True) for p in post_elem.find_all('p')]) if post_elem else ""

    # 3. Comentarios
    bots_identificados = ['AutoModerator', 'VisualMod', 'Bot']
    comentarios_finales = []
    comentarios_raw = soup.find_all('shreddit-comment')
    
    for comment in comentarios_raw:
        autor = comment.get('author', 'Desconocido')
        
        # Filtro A: Nombre del autor (si es un bot conocido)
        if any(bot.lower() in autor.lower() for bot in bots_identificados):
            continue
            
        # Extraer el texto del comentario
        c_text = "\n".join([p.get_text(strip=True) for p in comment.find_all('p')])
        
        # Filtro B: Si el texto está vacío o contiene la palabra "bot"
        if not c_text or "bot" in c_text.lower():
            continue

        comentarios_finales.append(f"[{autor}]: {c_text}")

    return {
        "archivo": os.path.basename(ruta_html),
        "titulo": titulo,
        "post": texto_post,
        "comentarios": comentarios_finales
    }

# --- PROCESAMIENTO ---

carpeta_origen = r"C:\Users\rival\Downloads\Proyecto3" 
archivos = glob.glob(os.path.join(carpeta_origen, "*.htm*"))

print(f"Archivos encontrados: {len(archivos)}")

with open("dataset_final_rag.txt", "w", encoding="utf-8") as out:
    for ruta in archivos:
        doc = extraer_datos_limpios(ruta)
        out.write(f"--- DOCUMENTO: {doc['archivo']} ---\n")
        out.write(f"TÍTULO: {doc['titulo']}\n")
        out.write(f"POST: {doc['post']}\n")
        out.write("COMENTARIOS FILTRADOS:\n")
        for c in doc['comentarios']:
            out.write(f"{c}\n")
        out.write(f"--- FIN ---\n\n")

print("Proceso completado.")