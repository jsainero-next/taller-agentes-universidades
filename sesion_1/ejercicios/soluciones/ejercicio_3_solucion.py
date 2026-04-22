"""
Sesión 1 - Ejercicio 3 (SOLUCIÓN): Calculadora inteligente (Function Calling)
"""

import json

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()


@tool
def sumar(a: float, b: float) -> float:
    """Suma dos números y devuelve el resultado."""
    return float(a) + float(b)


@tool
def multiplicar(a: float, b: float) -> float:
    """Multiplica dos números y devuelve el resultado."""
    return float(a) * float(b)


PREGUNTA_USUARIO = "¿Cuánto es (5 + 7) multiplicado por 10?"

MAX_VUELTAS = 5


def main() -> None:
    print("=" * 60)
    print("EJERCICIO 3 - Calculadora inteligente [SOLUCIÓN]")
    print("=" * 60)
    print(f"\nPregunta: {PREGUNTA_USUARIO}\n")

    herramientas = [sumar, multiplicar]
    herramientas_por_nombre = {t.name: t for t in herramientas}

    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
    model_with_tools = llm.bind_tools(herramientas)

    messages: list = [HumanMessage(content=PREGUNTA_USUARIO)]

    for vuelta in range(MAX_VUELTAS):
        ai_msg = model_with_tools.invoke(messages)
        messages.append(ai_msg)

        if not ai_msg.tool_calls:
            print("-" * 60)
            print("Respuesta final del modelo:")
            print(ai_msg.content or "(sin contenido de texto)")
            break

        print(f"\n--- Vuelta {vuelta + 1}: el modelo pide herramientas ---")
        for tool_call in ai_msg.tool_calls:
            nombre = tool_call["name"]
            args = tool_call["args"]
            tool_call_id = tool_call.get("id") or ""

            print(f"  Llamada: {nombre}({json.dumps(args, ensure_ascii=False)})")

            fn = herramientas_por_nombre.get(nombre)
            if fn is None:
                resultado = f"Error: herramienta desconocida {nombre}"
            else:
                resultado = fn.invoke(args)

            print(f"  Resultado: {resultado}")
            messages.append(
                ToolMessage(content=str(resultado), tool_call_id=tool_call_id)
            )
    else:
        print("\nSe alcanzó el máximo de vueltas sin respuesta final en texto.")


if __name__ == "__main__":
    main()
