"""
Sesión 2 - Ejercicio 3: Chat mínimo con Streamlit

Objetivo
--------
Crear una interfaz web sencilla de chat que conserve la conversación usando
st.session_state y permita ajustar la temperatura del modelo desde la barra
lateral.

Cómo ejecutarlo
---------------
Desde la raíz del proyecto (con el entorno activado):

  streamlit run sesion_2/ejercicios/ejercicio_3_enunciado.py

Instrucciones
-------------
1. Inicializa st.session_state["messages"] como lista vacía la primera vez
   (patrón: comprobar si la clave no está en session_state).
2. Muestra el historial con st.chat_message("user") / st.chat_message("assistant").
3. Lee nuevos mensajes con st.chat_input("Escribe un mensaje...").
4. Al enviar un mensaje: añádelo al historial, construye la lista de mensajes
   para LangChain (HumanMessage / AIMessage) y obtén la respuesta del
   ChatOpenAI usando la temperature del sidebar (st.sidebar.slider).
5. Añade la respuesta del asistente al historial y vuelve a mostrar.

Pista: Streamlit re-ejecuta todo el script en cada interacción; por eso
session_state es obligatorio para no perder el chat.
"""

from dotenv import load_dotenv

load_dotenv()

# TODO: import streamlit as st
# TODO: import ChatOpenAI y tipos de mensaje desde langchain


def main() -> None:
    # TODO: st.set_page_config y título
    # TODO: slider de temperatura en st.sidebar
    # TODO: bucle de visualización de st.session_state["messages"]
    # TODO: st.chat_input y lógica del LLM

    raise NotImplementedError(
        "Implementa la app con Streamlit (este archivo no usa main() típico: "
        "coloca la lógica a nivel de módulo o llama a main() al final)."
    )


if __name__ == "__main__":
    main()
