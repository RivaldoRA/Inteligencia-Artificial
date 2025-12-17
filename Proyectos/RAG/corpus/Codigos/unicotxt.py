import os
import glob

# Configuración
carpeta_entrada = './'  # Cambia esto al nombre de tu carpeta
archivo_salida = 'corpus_maestro_rag.txt'

def consolidar_carpeta_a_uno(input_path, output_file):
    # Verificar si la carpeta existe
    if not os.path.exists(input_path):
        print(f"Error: La carpeta '{input_path}' no existe.")
        return

    # Buscar todos los archivos .txt
    archivos = glob.glob(os.path.join(input_path, "*.txt"))
    
    if not archivos:
        print("No se encontraron archivos .txt en la carpeta.")
        return

    print(f"Se encontraron {len(archivos)} archivos. Iniciando consolidación...")

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for ruta in archivos:
            nombre_archivo = os.path.basename(ruta)
            
            with open(ruta, 'r', encoding='utf-8', errors='ignore') as infile:
                contenido = infile.read().strip()
                
                if contenido:
                    # Escribimos el delimitador para ayudar al RAG a saber de dónde viene el texto
                    outfile.write(f"\n\n--- DOCUMENTO: {nombre_archivo} ---\n")
                    outfile.write(contenido)
                    outfile.write(f"\n--- FIN DE: {nombre_archivo} ---\n")
            
            print(f"Procesado: {nombre_archivo}")

    print(f"\n¡Éxito! Todo el texto está en: {output_file}")

# Ejecutar
consolidar_carpeta_a_uno(carpeta_entrada, archivo_salida)