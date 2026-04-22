"""
Sesión 1 - Ejercicio 2: Traductor con personalidad (dos pasos)

Objetivo
--------
1. Traducir una frase en español al inglés (rol: traductor profesional).
2. Tomar esa traducción en inglés y reescribirla con otra personalidad
   (ej.: pirata del Caribe, robot de los 80, poeta barroco).

Instrucciones
-------------
1. Define dos system prompts distintos (constantes o diccionario).
2. Primera llamada: SystemMessage(traductor) + HumanMessage(frase_es).
3. Segunda llamada: SystemMessage(estilo) + HumanMessage(resultado del paso 1).
4. Imprime la frase original, la traducción y el texto final con estilo.

Pista: usa HumanMessage y SystemMessage como en sesion_1/3_roles_system_prompt.py
"""

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

FRASE_ES = "La inteligencia artificial cambiará muchos trabajos en la próxima década."

# TODO: system prompt para traducción fiel al inglés.
SYSTEM_TRADUCTOR = ""

# TODO: system prompt para reescribir en el estilo elegido.
SYSTEM_ESTILO = ""


def main() -> None:
    print("=" * 60)
    print("EJERCICIO 2 - Traductor con personalidad")
    print("=" * 60)

    # TODO: llm = ChatOpenAI(model=..., temperature=...)
    # TODO: mensajes paso 1 → respuesta traducción
    # TODO: mensajes paso 2 → respuesta final

    raise NotImplementedError("Completa este ejercicio antes de ejecutar.")


if __name__ == "__main__":
    main()
