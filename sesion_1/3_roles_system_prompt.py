"""
Sesión 1 - Ejemplo 3: Roles y System Prompt

Los LLMs reciben los mensajes organizados en tres roles:
  - system:    instrucciones de comportamiento que el usuario nunca ve
  - user:      el mensaje del usuario
  - assistant: la respuesta del modelo (se usa para construir historial)

Este ejemplo envía el MISMO mensaje de usuario con tres system prompts
distintos para mostrar cómo el rol system controla completamente el
tono, el idioma y la personalidad del modelo.
"""

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()


PREGUNTA = "¿Qué es la inteligencia artificial?"

PERSONAJES = [
    {
        "nombre": "Profesor universitario",
        "system": (
            "Eres un catedrático de informática. Explica los conceptos con rigor "
            "académico y precisión técnica, usando terminología del área."
        ),
    },
    {
        "nombre": "Explicador para niños de 8 años",
        "system": (
            "Eres un maestro de primaria. Explica todo de forma muy sencilla, "
            "con analogías del mundo cotidiano y frases cortas."
        ),
    },
    {
        "nombre": "Escéptico sarcástico",
        "system": (
            "Eres un periodista tecnológico muy escéptico. Responde con ironía "
            "y señala siempre los límites y exageraciones del marketing tecnológico."
        ),
    },
]


def main() -> None:
    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0.7)

    print("=" * 60)
    print("ROLES Y SYSTEM PROMPT")
    print("=" * 60)
    print(f'\nPregunta del usuario (siempre la misma): "{PREGUNTA}"\n')
    print("Observa cómo cambia la respuesta según el system prompt.\n")

    for personaje in PERSONAJES:
        print("-" * 60)
        print(f"SYSTEM PROMPT → {personaje['nombre']}")
        print(f'  "{personaje["system"]}"')
        print()

        messages = [
            SystemMessage(content=personaje["system"]),
            HumanMessage(content=PREGUNTA),
        ]
        response = llm.invoke(messages)
        print(response.content)
        print()

    print("=" * 60)
    print("Conclusión: el system prompt actúa como las instrucciones ocultas")
    print("que moldean el comportamiento del modelo antes de que hable el usuario.")
    print("Es la herramienta principal para personalizar un LLM en una aplicación.")


if __name__ == "__main__":
    main()
