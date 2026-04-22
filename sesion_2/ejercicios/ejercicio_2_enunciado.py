"""
Sesión 2 - Ejercicio 2: Memoria por resumen (compactar historial)

Objetivo
--------
Simular un chat cuya lista de mensajes crece. Cuando supere un umbral,
los mensajes más antiguos se resumen en un solo bloque (p. ej. un
SystemMessage con el resumen) y se conservan solo los últimos turnos.
Así se evita crecer sin límite y se mantiene contexto aproximado del pasado.

Instrucciones
-------------
1. Representa el historial como lista de mensajes LangChain:
   HumanMessage / AIMessage (y opcionalmente un SystemMessage inicial).
2. Tras cada turno simulado (o al final de una secuencia de turnos),
   si len(historial) > LIMITE, llama al LLM para resumir los mensajes
   "viejos" y reemplázalos por un único SystemMessage (o HumanMessage
   fijo) que contenga solo el resumen, seguido de los mensajes recientes
   que decidas conservar (p. ej. los últimos 4 mensajes).
3. Imprime o muestra el historial antes y después de compactar para
   comprobar que el tamaño baja y el resumen aparece.

Pista: no hace falta interfaz gráfica; un bucle for con preguntas de
ejemplo en main() es suficiente. Revisa sesion_2/3_memoria_rag.py para
el estilo de mensajes, aunque aquí implementas tú la lógica de resumen.
"""

from dotenv import load_dotenv

load_dotenv()

LIMITE_MENSAJES = 8  # al superarlo, compactar
MENSAJES_A_MANTENER = 4  # cuántos mensajes recientes conservar tras compactar


def main() -> None:
    print("=" * 60)
    print("EJERCICIO 2 - Memoria por resumen")
    print("=" * 60)

    # TODO: ChatOpenAI + construir historial de ejemplo (varios turnos)
    # TODO: función compactar_historial(historial, llm) -> nuevo historial
    # TODO: invocar compactar cuando len(historial) > LIMITE_MENSAJES
    # TODO: imprimir estado antes/después

    raise NotImplementedError("Completa este ejercicio antes de ejecutar.")


if __name__ == "__main__":
    main()
