import os

# Lista de tus archivos recolectados
archivos_input = [
    'dataset_reddit_genz_algorithm.txt', 
    'dataset_reddit_genz_burnout.txt', 
    'dataset_reddit_genz_depression.txt', 
    'dataset_reddit_genz_narcissism.txt', 
]

archivo_final = 'corpus_consolidado_rag.txt'

def combinar_txt(lista_archivos, salida):
    with open(salida, 'w', encoding='utf-8') as outfile:
        for nombre_archivo in lista_archivos:
            if os.path.exists(nombre_archivo):
                with open(nombre_archivo, 'r', encoding='utf-8') as infile:
                    # Escribimos un encabezado para separar las fuentes
                    outfile.write(f"\n--- INICIO DE FUENTE: {nombre_archivo} ---\n")
                    
                    # Escribimos el contenido del archivo
                    outfile.write(infile.read())
                    
                    # Aseguramos un salto de línea al final de cada archivo
                    outfile.write(f"\n--- FIN DE FUENTE: {nombre_archivo} ---\n")
                print(f"Procesado: {nombre_archivo}")
            else:
                print(f"Advertencia: El archivo {nombre_archivo} no se encontró.")

# Ejecutar la función
combinar_txt(archivos_input, archivo_final)
print(f"\nÉxito. Tu corpus para el RAG está listo en: {archivo_final}")