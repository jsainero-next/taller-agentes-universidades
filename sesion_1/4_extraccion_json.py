"""
Sesión 1 - Ejemplo 4: Extracción de datos (JSON Mode)

Obliga al modelo a responder con JSON válido en lugar de texto libre.
Esto es vital para que un proceso pueda leer y procesar la respuesta del LLM.
"""

import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def main() -> None:
    prompt = """Extrae la siguiente información del texto en formato JSON:
- nombre: nombre de la persona
- edad: edad en años (número)
- ciudad: ciudad de residencia

Texto: "María García tiene 28 años y vive en Madrid."
"""

    print("=" * 60)
    print("EXTRACCIÓN DE DATOS (JSON Mode)")
    print("=" * 60)
    print(f"\nPrompt:\n{prompt}\n")

    # JSON Mode: el modelo responde con JSON válido
    llm = ChatOpenAI(
        model="gpt-5.4-nano",
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}},
    )
    response = llm.invoke(prompt)

    print("-" * 60)
    print("Respuesta del modelo (raw):")
    print(response.content)
    print()

    # Parsear y usar el JSON en el programa
    datos = json.loads(response.content)
    print("-" * 60)
    print("Datos parseados (accesibles en el código):")
    for clave, valor in datos.items():
        print(f"  {clave}: {valor}")
    print()

    # Ejemplo de uso programático
    print("Ejemplo de uso: generar un saludo")
    saludo = f"Hola {datos.get('nombre', '')}, tienes {datos.get('edad', '')} años."
    print(f"  {saludo}")


if __name__ == "__main__":
    main()
