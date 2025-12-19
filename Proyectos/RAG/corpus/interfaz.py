import streamlit as st
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import sys

# --- CONFIGURACIÓN DE STREAMLIT ---
st.set_page_config(page_title="Analista Gen Z", page_icon="🧬", layout="wide")
st.title("🧬 Sistema RAG: Análisis Filosófico Gen Z")

# --- CARGA DE RECURSOS (CACHED) ---
@st.cache_resource
def init_rag_system():
    # 1. Configuración de Modelos
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    llm = OllamaLLM(model="llama3.2")

    # 2. Conexión a la Base de Datos
    db_path = "./db_proyecto_genz"
    if not os.path.exists(db_path):
        return None, None, None

    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k": 5})
    
    return llm, retriever, embeddings

llm, retriever, embeddings = init_rag_system()

if llm is None:
    st.error("Error: No se encontró la base de datos de vectores en './db_proyecto_genz'")
    st.stop()

# --- LÓGICA DE PROMPTS Y CADENAS ---
query_transform_prompt = ChatPromptTemplate.from_template(
    "Genera 3 términos cortos en inglés para buscar en Reddit sobre: {question}. Solo términos, sin texto adicional."
)
query_translator = query_transform_prompt | llm | StrOutputParser()

analysis_prompt = ChatPromptTemplate.from_template("""
Eres un analista experto en sociología y filosofía. Responde en ESPAÑOL.
Usa el contexto proporcionado (incluyendo datos en inglés de Reddit si es necesario).
No inventes información fuera del contexto. Sé directo y profundo.

Contexto:
{context}

Pregunta: {question}
""")

def bilingual_retrieval(question):
    try:
        # Esto se imprime en la consola para monitoreo
        print(f"--- Traducción de consulta para: {question} ---")
        english_terms = query_translator.invoke({"question": question})
        search_query = f"{question} {english_terms}"
        print(f"Buscando en DB con: {search_query}")
    except Exception as e:
        print(f"Error en traducción: {e}")
        search_query = question
    return retriever.invoke(search_query)

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("Escribe tu análisis filosófico..."):
    # 1. Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Log en consola
    print(f"\n[USUARIO]: {prompt}")

    # 2. Generar respuesta
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Recuperación de documentos
            with st.spinner("Consultando base de datos de vectores..."):
                docs = bilingual_retrieval(prompt)
                context_text = "\n\n".join([d.page_content for d in docs])
            
            # Ejecución de la cadena de análisis
            print("IA Generando respuesta...", end="", flush=True)
            
            # Nota: OllamaLLM no soporta stream nativo de la misma forma que el chat directo 
            # de ollama-python sin configurar callbacks, así que lo manejamos directo:
            chain = analysis_prompt | llm | StrOutputParser()
            
            # Si prefieres ver el progreso en consola:
            respuesta_final = chain.invoke({"context": context_text, "question": prompt})
            
            full_response = respuesta_final
            response_placeholder.markdown(full_response)
            
            # Log final en consola
            print(f"\n[IA]: {full_response[:100]}...") 
            print("-" * 30)

        except Exception as e:
            error_msg = f"Error al procesar la consulta: {e}"
            st.error(error_msg)
            print(error_msg)

    st.session_state.messages.append({"role": "assistant", "content": full_response})