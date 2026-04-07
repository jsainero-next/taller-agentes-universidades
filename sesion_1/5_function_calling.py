"""
Sesión 1 - Ejemplo 5: Introducción al Function Calling

El modelo, en lugar de responder con texto, indica: "Necesito llamar a
enviar_correo() con estos argumentos". El código detecta esta intención.
"""

import json

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()


@tool
def enviar_correo(destinatario: str, asunto: str, cuerpo: str) -> str:
    """Envía un correo electrónico a un destinatario con el asunto y cuerpo indicados."""
    return f"[SIMULADO] Correo enviado a {destinatario}: '{asunto}' - {cuerpo[:50]}..."


def main() -> None:
    prompt = "Envía un correo a juan@empresa.com con asunto 'Reunión mañana' y cuerpo 'Hola Juan, confirmamos la reunión a las 10:00.'"

    print("=" * 60)
    print("FUNCTION CALLING")
    print("=" * 60)
    print(f"\nPrompt del usuario: \"{prompt}\"\n")

    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
    model_with_tools = llm.bind_tools([enviar_correo])

    response = model_with_tools.invoke(prompt)

    print("-" * 60)
    print("Respuesta del modelo:")
    if response.content:
        print(f"Texto: {response.content}")
    if response.tool_calls:
        print("\nEl modelo decidió llamar a herramientas:")
        for tool_call in response.tool_calls:
            print(f"  - Función: {tool_call['name']}")
            print(f"    Argumentos: {json.dumps(tool_call['args'], indent=4, ensure_ascii=False)}")

            # Ejecutar la herramienta (simulado)
            if tool_call["name"] == "enviar_correo":
                args = tool_call["args"]
                resultado = enviar_correo.invoke(args)
                print(f"    Resultado: {resultado}")

    print("\n" + "=" * 60)
    print("El modelo no respondió con texto libre, sino con una intención de")
    print("llamar a enviar_correo(). El programa puede ejecutar la función.")


if __name__ == "__main__":
    main()
