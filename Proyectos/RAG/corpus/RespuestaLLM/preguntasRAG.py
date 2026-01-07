from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

# 1. Configuración de Modelos
embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = OllamaLLM(model="llama3.2")

# 2. Base de Datos
vector_db = Chroma(persist_directory="./db_proyecto_genz", embedding_function=embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 5})

# 3. Traductor de Consulta (para captar Reddit)
query_transform_prompt = ChatPromptTemplate.from_template(
    "Genera 3 términos cortos en inglés para buscar en Reddit sobre: {question}. Solo términos, sin texto adicional."
)
query_translator = query_transform_prompt | llm | StrOutputParser()

# 4. Prompt de Análisis (Sin referencias externas)
prompt = ChatPromptTemplate.from_template("""
Eres un analista experto en sociología y filosofía. Responde en ESPAÑOL basándote en el contexto proporcionado.
NO utilices frases como "según el texto" o "el fragmento menciona". 
NO incluyas bibliografía ni referencias al final. 
Responde de forma directa, analítica y fluida.

Contexto:
{context}

Pregunta: {question}
""")

# 5. Función de recuperación
def bilingual_retrieval(inputs):
    question = inputs["question"]
    english_terms = query_translator.invoke({"question": question})
    search_query = f"{question} {english_terms}"
    return retriever.invoke(search_query)

# 6. Cadena RAG
rag_chain = (
    {"context": bilingual_retrieval, "question": lambda x: x["question"]}
    | prompt
    | llm
    | StrOutputParser()
)

# 7. Lista de preguntas
preguntas = [
    "¿Qué expresiones o términos utiliza la Gen Z para describir el vacío existencial en redes sociales?",
    "¿Cómo influyen los algoritmos de recomendación en la construcción de su identidad?",
    "¿Qué emociones aparecen con mayor frecuencia cuando se habla de burnout o presión digital?",
    "¿La Gen Z percibe la autonomía como algo propio o como algo condicionado por la tecnología?",
    "¿Qué diferencias hay entre discursos auténticos vs discursos performativos en plataformas como TikTok?",
    "¿Existen patrones de lenguaje que indiquen crisis de sentido o desorientación vital?",
    "¿Cómo se refleja la idea de 'identidad líquida' en los datos recuperados?",
    "¿Qué menciones aparecen sobre libertad, control o manipulación algorítmica?",
    "¿Se observan señales de que los algoritmos crean deseos o hábitos?",
    "¿Qué temas o preocupaciones predominan en la conversación digital sobre propósito de vida?",
    "¿Hay evidencia de rechazo a los metarrelatos o valores tradicionales?",
    "¿Cómo aparece la figura del 'yo digital' en los textos analizados?",
    "¿Qué ejemplos concretos muestran pérdida del pensamiento crítico por efecto de la burbuja de filtros?",
    "¿Existen contrastes entre la visión que la Gen Z tiene de sí misma y lo que los datos sugieren?",
    "¿Qué rol juega la hiperconectividad en la ansiedad o depresión mencionada?",
    "¿Se observan patrones que apoyen las ideas de Byung-Chul Han sobre rendimiento y autoexplotación?",
    "¿Cómo interpretaría Foucault el régimen de vigilancia algorítmica detectado?",
    "¿Qué evidencias hay de que la tecnología 'desoculta' y transforma la vida según Heidegger?",
    "¿El espacio público digital está debilitado como afirma Habermas? ¿Qué muestran los datos?",
    "¿Cuáles son los principales miedos, frustraciones y esperanzas de la Gen Z frente al futuro?"
]

# 8. Ejecución y escritura del archivo
archivo_salida = "Analisis_GenZ_RAG.md"

with open(archivo_salida, "w", encoding="utf-8") as f:
    f.write("# Informe de Análisis Sociológico y Filosófico: Generación Z\n\n")
    
    for i, p in enumerate(preguntas):
        print(f"Procesando pregunta {i+1}/20...")
        respuesta = rag_chain.invoke({"question": p})
        f.write(f"## {p}\n\n")
        f.write(f"{respuesta}\n\n")
        f.write("---\n\n")

print(f"Informe completado: {archivo_salida}")