import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Cargar tu archivo maestro de 4MB
loader = TextLoader("corpus_maestro_rag.txt", encoding="utf-8")
documentos = loader.load()

# 2. Fragmentar el texto (Splitting)
# Usamos un chunk_size grande para mantener el contexto filosófico
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
    add_start_index=True
)
fragmentos = text_splitter.split_documents(documentos)

print(f"Texto dividido en {len(fragmentos)} fragmentos.")

# 3. Configurar el modelo de Embeddings (Multilingüe es mejor)
embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

# 4. Crear la base de datos de vectores y guardarla en disco
vector_db = Chroma.from_documents(
    documents=fragmentos,
    embedding=embeddings_model,
    persist_directory="./db_proyecto_genz" # Carpeta donde se guardarán los vectores
)

print("¡Vectores generados y guardados exitosamente!")