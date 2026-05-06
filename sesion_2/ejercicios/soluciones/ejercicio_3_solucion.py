"""
Sesión 2 - Ejercicio 3 (SOLUCIÓN): Chat mínimo con Streamlit

Ejecutar desde la raíz del proyecto:

  streamlit run sesion_2/ejercicios/soluciones/ejercicio_3_solucion.py
"""

from dotenv import load_dotenv
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()


def construir_mensajes_lc() -> list:
    mensajes: list = [
        SystemMessage(
            content="Eres un asistente útil. Responde en español de forma concisa."
        )
    ]
    for entry in st.session_state.messages:
        role = entry["role"]
        content = entry["content"]
        if role == "user":
            mensajes.append(HumanMessage(content=content))
        elif role == "assistant":
            mensajes.append(AIMessage(content=content))
    return mensajes


def main() -> None:
    st.set_page_config(page_title="Chat Sesión 2", page_icon="💬")
    st.title("Chat mínimo (ejercicio 3)")
    st.caption("Sesión 2 · Streamlit + LangChain")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    temperatura = st.sidebar.slider(
        "Temperatura del modelo",
        min_value=0.0,
        max_value=1.5,
        value=0.7,
        step=0.05,
        help="Valores bajos: más determinista. Valores altos: más variación.",
    )

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Escribe un mensaje..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        llm = ChatOpenAI(model="gpt-5.4-nano", temperature=temperatura)
        respuesta = llm.invoke(construir_mensajes_lc())
        texto = (respuesta.content or "").strip()

        st.session_state.messages.append({"role": "assistant", "content": texto})
        with st.chat_message("assistant"):
            st.markdown(texto)


if __name__ == "__main__":
    main()
