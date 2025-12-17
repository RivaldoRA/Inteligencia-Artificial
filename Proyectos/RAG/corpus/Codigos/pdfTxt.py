import fitz  # PyMuPDF
import os
import glob

def pdf_a_texto(carpeta_entrada, carpeta_salida):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    for ruta_pdf in glob.glob(os.path.join(carpeta_entrada, "*.pdf")):
        nombre_archivo = os.path.basename(ruta_pdf).replace(".pdf", ".txt")
        doc = fitz.open(ruta_pdf)
        texto = ""
        
        for pagina in doc:
            texto += pagina.get_text()
        
        with open(os.path.join(carpeta_salida, nombre_archivo), "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"Convertido: {nombre_archivo}")

# Uso
pdf_a_texto(r"C:\Users\rival\Downloads\Proyecto3", "./")