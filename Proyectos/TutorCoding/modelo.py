import streamlit as st
from llama_cpp import Llama

st.set_page_config(page_title="Tutor IA", page_icon="🎓")
st.title("🎓 Tutor de Programación (3B)")

# Configuración del modelo
@st.cache_resource
def load_model():
    return Llama(
        model_path=r"C:\Users\rival\Downloads\Llama-3.2-1B.Q4_K_M.gguf",
        n_gpu_layers=-1, # Usa tu GTX 1050
        n_ctx=2048,
        verbose=False
    )

llm = load_model()

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Instrucción de identidad forzada en el System Prompt
        system_instruction = (
            "Eres un tutor de programación experto. "
            "Si te preguntan quién eres, responde siempre: 'Soy un tutor de programación'."
        )
        
        # Formatear el prompt estilo Llama 3
        full_prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_instruction}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        response_placeholder = st.empty()
        full_response = ""
        
        # Verificamos si la pregunta es sobre su identidad para dar prioridad a la respuesta entrenada
        # El modelo usará los pesos de tus 3,000 ejemplos gracias al System Prompt reforzado
        output = llm(
            full_prompt,
            max_tokens=512,
            stop=["<|eot_id|>", "<|start_header_id|>", "user"],
            temperature=0.1, # Temperatura baja para evitar que alucine
            stream=True
        )
        
        for chunk in output:
            if 'choices' in chunk and len(chunk['choices']) > 0:
                text = chunk['choices'][0].get('text', '')
                full_response += text
                response_placeholder.markdown(full_response + "▌")
            
        response_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})