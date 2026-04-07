"""
Sesión 1 - Ejemplo 2: Control de la creatividad

Prueba el mismo prompt con temperatura 0 vs temperatura 1.5 para ver
la degradación del lenguaje con temperatura alta.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def main() -> None:
    prompt = "Explica en una frase qué es la inteligencia artificial."

    print("=" * 60)
    print("CONTROL DE LA CREATIVIDAD (Temperature)")
    print("=" * 60)
    print(f"\nPrompt: \"{prompt}\"\n")

    # Temperatura 0: respuestas deterministas y coherentes
    print("-" * 60)
    print("TEMPERATURA 0 (determinista)")
    print("-" * 60)
    llm_t0 = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
    resp_t0 = llm_t0.invoke(prompt)
    print(resp_t0.content)
    print()

    # Temperatura 1.5: respuestas más creativas pero pueden degradarse
    print("-" * 60)
    print("TEMPERATURA 1.5 (alta creatividad)")
    print("-" * 60)
    llm_t15 = ChatOpenAI(model="gpt-5.4-nano", temperature=1.5)
    resp_t15 = llm_t15.invoke(prompt)
    print(resp_t15.content)
    print()

    print("=" * 60)
    print("Conclusión: Temperatura 0 = coherente. Temperatura alta = más variado.")
    print("Para tareas de extracción o razonamiento, usa temperatura baja.")


if __name__ == "__main__":
    main()
