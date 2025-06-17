import streamlit as st  
import groq as gq
# LISTA DE MODELOS DISPONIBLES
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192']
# CONFIGURAR LA PÁGINA
def configurar_pagina():
    st.set_page_config(page_title="Mi primer chat bot con streamlit", page_icon="🔥")
    st.title("Mi primera app con streamlit")
# CREAR CLIENTE GROQ
def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groq_api_key)
# MOSTRAR BARRA LATERAL Y DEVOLVER MODELO ELEGIDO
def mostrar_sidebar():
    st.sidebar.title("Elegí tu modelo de IA preferido")
    modelo = st.sidebar.selectbox("Elija", MODELOS, index=0)
    st.write(f'Elegiste el modelo: {modelo}')
    return modelo

# INICIALIZAR EL ESTADO DEL CHAT

def inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

# MOSTRAR MENSAJES PREVIOS
def mostrar_historial_chat():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

# OBTENER INPUT DEL USUARIO
def obtener_mensaje_usuario():
    return st.chat_input("Hazle una pregunta a la IA")

# AGREGAR MENSAJE AL HISTORIAL
def agregar_mensaje_al_historial(role, content):
    st.session_state.mensajes.append({"role": role, "content": content})

# MOSTRAR MENSAJE EN PANTALLA
def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

# LLAMAR AL MODELO Y OBTENER RESPUESTA
def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensajes,
        stream=False
    )
    return respuesta.choices[0].message.content
# FLUJO PRINCIPAL DEL CHAT
def ejecutar_chat():
    configurar_pagina()
    cliente = crear_cliente_groq()
    modelo = mostrar_sidebar()
    print(modelo)
    # modelo = sider_con_for()
    inicializar_estado_chat()
    mostrar_historial_chat()

    mensaje_usuario = obtener_mensaje_usuario()
    print(mensaje_usuario)
    if mensaje_usuario:
        agregar_mensaje_al_historial("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)

        respuesta_contenido = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)

        agregar_mensaje_al_historial("assistant", respuesta_contenido)
        mostrar_mensaje("assistant", respuesta_contenido)
# EJECUTAR LA APP
if __name__ == "__main__":
    ejecutar_chat()
