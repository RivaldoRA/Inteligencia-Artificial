import streamlit as st
import ollama
import sys

st.set_page_config(page_title="Tutor IA con Ollama", page_icon="🎓")
st.title("Tutor de Programación (Ollama)")

# Configuración: Nombre del modelo que tienes en Ollama
# Puedes ver tus modelos con el comando 'ollama list' en la terminal
MODEL_NAME = "llama3.2" 

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Log en consola
    print(f"\n--- USUARIO: {prompt} ---")

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # System prompt para mantener la identidad de tutor
        system_instruction = (
            "Eres un tutor de programación experto. "
            "Si te preguntan quién eres, responde siempre: 'Soy un tutor de programación'."
        )

        # Llamada a Ollama con streaming
        stream = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {'role': 'system', 'content': system_instruction},
                {'role': 'user', 'content': prompt},
            ],
            stream=True,
        )

        print("ASISTENTE: ", end="", flush=True)

        for chunk in stream:
            text = chunk['message']['content']
            full_response += text
            
            # Actualizar la web
            response_placeholder.markdown(full_response + "▌")
            
            # Actualizar la consola
            print(text, end="", flush=True)

        response_placeholder.markdown(full_response)
        print("\n" + "-"*30)

    st.session_state.messages.append({"role": "assistant", "content": full_response})