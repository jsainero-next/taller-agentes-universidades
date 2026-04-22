"""
Sesión 1 - Ejercicio 3: Calculadora inteligente (Function Calling)

Objetivo
--------
Definir dos herramientas `sumar` y `multiplicar` y conseguir que el modelo
resuelva preguntas que requieran varias llamadas, por ejemplo:
  "¿Cuánto es (5 + 7) multiplicado por 10?"

Instrucciones
-------------
1. Completa las funciones decoradas con @tool (sumar y multiplicar).
2. Implementa un bucle:
   - Invoca el modelo con bind_tools([sumar, multiplicar]).
   - Si hay tool_calls, ejecuta cada herramienta con los argumentos
     indicados y vuelve a invocar el modelo con el historial (mensaje
     del asistente + mensajes de herramienta con los resultados).
   - Repite hasta que no haya más tool_calls o hasta un máximo de vueltas
     (ej. 5) para evitar bucles infinitos.
3. Al final, imprime la respuesta en texto del modelo.

Pista: revisa sesion_1/5_function_calling.py y la documentación de LangChain
sobre ToolMessage y AIMessage para el historial.
"""

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()


@tool
def sumar(a: float, b: float) -> float:
    """TODO: docstring que describa la herramienta para el modelo."""
    raise NotImplementedError


@tool
def multiplicar(a: float, b: float) -> float:
    """TODO: docstring que describa la herramienta para el modelo."""
    raise NotImplementedError


PREGUNTA_USUARIO = "¿Cuánto es (5 + 7) multiplicado por 10?"


def main() -> None:
    print("=" * 60)
    print("EJERCICIO 3 - Calculadora inteligente")
    print("=" * 60)
    print(f"\nPregunta: {PREGUNTA_USUARIO}\n")

    # TODO: arranca el historial con un solo mensaje de usuario (HumanMessage).
    # TODO: crea el modelo con bind_tools([sumar, multiplicar]) y un bucle:
    #       invoke(historial) → añade la respuesta del asistente al historial;
    #       si trae tool_calls, ejecuta cada una, añade ToolMessage por resultado
    #       (no olvides el id de la llamada) y vuelve al principio del bucle;
    #       si ya no pide herramientas, imprime el texto y termina (límite de vueltas).
    #       Importa HumanMessage y ToolMessage desde langchain_core.messages.

    raise NotImplementedError("Completa este ejercicio antes de ejecutar.")


if __name__ == "__main__":
    main()
