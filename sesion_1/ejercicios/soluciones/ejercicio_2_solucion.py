"""
Sesión 1 - Ejercicio 2 (SOLUCIÓN): Traductor con personalidad (dos pasos)
"""

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

FRASE_ES = "La inteligencia artificial cambiará muchos trabajos en la próxima década."

SYSTEM_TRADUCTOR = (
    "Eres un traductor profesional inglés-español. Traduce el texto del usuario "
    "al inglés de forma fiel, natural y sin añadir comentarios ni explicaciones. "
    "Devuelve únicamente la traducción."
)

SYSTEM_ESTILO = (
    "Eres un pirata del Caribe del siglo XVIII. Reescribe el texto en inglés que "
    "te da el usuario manteniendo el significado pero usando jerga de barco, "
    "'arr', metáforas náuticas y tono teatral. Una sola respuesta, sin preámbulos."
)


def main() -> None:
    print("=" * 60)
    print("EJERCICIO 2 - Traductor con personalidad [SOLUCIÓN]")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0.7)

    print(f'\nFrase original (ES): "{FRASE_ES}"\n')

    mensajes_paso1 = [
        SystemMessage(content=SYSTEM_TRADUCTOR),
        HumanMessage(content=FRASE_ES),
    ]
    resp1 = llm.invoke(mensajes_paso1)
    traduccion = (resp1.content or "").strip()

    print("-" * 60)
    print("Paso 1 - Traducción al inglés:")
    print(traduccion)
    print()

    mensajes_paso2 = [
        SystemMessage(content=SYSTEM_ESTILO),
        HumanMessage(content=traduccion),
    ]
    resp2 = llm.invoke(mensajes_paso2)
    final_texto = (resp2.content or "").strip()

    print("-" * 60)
    print("Paso 2 - Mismo contenido, estilo pirata (EN):")
    print(final_texto)


if __name__ == "__main__":
    main()
