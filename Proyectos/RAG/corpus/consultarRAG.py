from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import sys
import os

# 1. Configuración de Modelos
embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = OllamaLLM(model="llama3.2")

# 2. Conexión a la Base de Datos
if not os.path.exists("./db_proyecto_genz"):
    print("Error: No se encontró la base de datos de vectores.")
    sys.exit()

vector_db = Chroma(persist_directory="./db_proyecto_genz", embedding_function=embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 5})

# 3. Traductor de Consulta (Mejora la búsqueda en Reddit)
query_transform_prompt = ChatPromptTemplate.from_template(
    "Genera 3 términos cortos en inglés para buscar en Reddit sobre: {question}. Solo términos, sin texto adicional."
)
query_translator = query_transform_prompt | llm | StrOutputParser()

# 4. Prompt de Análisis Estricto
prompt = ChatPromptTemplate.from_template("""
Eres un analista experto en sociología y filosofía. Responde en ESPAÑOL.
Usa el contexto proporcionado (incluyendo datos en inglés de Reddit si es necesario).
No inventes información fuera del contexto. Sé directo y profundo.

Contexto:
{context}

Pregunta: {question}
""")

# 5. Función de recuperación bilingüe
def bilingual_retrieval(inputs):
    question = inputs["question"]
    # Intentamos obtener términos en inglés para enriquecer la búsqueda
    try:
        english_terms = query_translator.invoke({"question": question})
        search_query = f"{question} {english_terms}"
    except:
        search_query = question
    return retriever.invoke(search_query)

# 6. Construcción de la Cadena (LCEL)
rag_chain = (
    {"context": bilingual_retrieval, "question": lambda x: x["question"]}
    | prompt
    | llm
    | StrOutputParser()
)

# 7. Bucle de Interacción en Consola
def iniciar_chat():
    print("\n" + "="*50)
    print("SISTEMA RAG: ANÁLISIS FILOSÓFICO GEN Z")
    print("Escribe 'salir' o 'exit' para cerrar el programa.")
    print("="*50 + "\n")

    while True:
        usuario_input = input("Tú: ")
        
        if usuario_input.lower() in ["salir", "exit", "quit"]:
            print("Cerrando sistema de análisis. Hasta pronto.")
            break
        
        if not usuario_input.strip():
            continue
        
        try:
            # Ejecución de la cadena
            respuesta = rag_chain.invoke({"question": usuario_input})
            print(f"\nIA: {respuesta}\n")
            print("-" * 30)
        except Exception as e:
            print(f"\nError al procesar la consulta: {e}")

if __name__ == "__main__":
    iniciar_chat()