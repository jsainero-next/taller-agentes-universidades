"""
Sesión 2 - Ejemplo 4: Uso de Herramientas (Tools)

Un agente calculadora que usa herramientas matemáticas básicas.
El LLM decide qué operación usar según la pregunta del usuario.
"""

import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()


@tool
def sumar(a: float, b: float) -> float:
    """Suma dos números."""
    return a + b


@tool
def restar(a: float, b: float) -> float:
    """Resta b de a."""
    return a - b


@tool
def multiplicar(a: float, b: float) -> float:
    """Multiplica dos números."""
    return a * b


@tool
def dividir(a: float, b: float) -> float:
    """Divide a entre b."""
    if b == 0:
        return "Error: no se puede dividir entre cero."
    return a / b


def main() -> None:
    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
    agent = create_react_agent(
        llm,
        tools=[sumar, restar, multiplicar, dividir],
        prompt="Eres una calculadora. Usa las herramientas disponibles para resolver operaciones matemáticas.",
    )

    pregunta = "¿Cuánto es (25 + 17) * 3?"

    print("=" * 50)
    print("AGENTE CALCULADORA")
    print("=" * 50)
    print(f"\nPregunta: {pregunta}\n")

    for chunk in agent.stream({"messages": [{"role": "user", "content": pregunta}]}, stream_mode="updates"):
        for node, output in chunk.items():
            for msg in output.get("messages", []):
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        args = ", ".join(f"{k}={v}" for k, v in tc["args"].items())
                        print(f"  -> Herramienta: {tc['name']}({args})")
                elif hasattr(msg, "content") and msg.content:
                    print(f"  [{node}] {msg.content}")


if __name__ == "__main__":
    main()
