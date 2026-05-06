"""
Sesión 2 - Ejercicio 2 (SOLUCIÓN): Memoria por resumen (compactar historial)
"""

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

LIMITE_MENSAJES = 8
MENSAJES_A_MANTENER = 4


def formatear_turnos_para_resumen(mensajes: list) -> str:
    """Convierte una lista de BaseMessage en texto plano para el prompt de resumen."""
    lineas: list[str] = []
    for m in mensajes:
        if isinstance(m, HumanMessage):
            lineas.append(f"Usuario: {m.content}")
        elif isinstance(m, AIMessage):
            lineas.append(f"Asistente: {m.content}")
        elif isinstance(m, SystemMessage):
            lineas.append(f"Sistema/Resumen previo: {m.content}")
    return "\n".join(lineas)


def compactar_historial(
    historial: list,
    llm: ChatOpenAI,
    limite: int = LIMITE_MENSAJES,
    mantener: int = MENSAJES_A_MANTENER,
) -> list:
    """
    Si el historial supera `limite`, resume los mensajes antiguos y deja
    solo un SystemMessage con el resumen + los `mantener` últimos mensajes.
    """
    if len(historial) <= limite:
        return historial

    recientes = historial[-mantener:]
    viejos = historial[:-mantener]

    prompt_resumen = (
        "Resume la siguiente conversación en un solo párrafo en español, "
        "conservando hechos, nombres y decisiones importantes. "
        "No inventes información que no aparezca en el texto.\n\n"
        f"{formatear_turnos_para_resumen(viejos)}"
    )
    res = llm.invoke(prompt_resumen)
    texto_resumen = (res.content or "").strip()

    nuevo = [
        SystemMessage(
            content=(
                "A continuación un resumen de la conversación anterior "
                f"(mensajes antiguos compactados):\n\n{texto_resumen}"
            )
        )
    ]
    nuevo.extend(recientes)
    return nuevo


def imprimir_historial_etiquetado(historial: list, titulo: str) -> None:
    print(f"\n{titulo} ({len(historial)} mensajes)")
    print("-" * 60)
    for i, m in enumerate(historial, 1):
        tipo = type(m).__name__
        contenido = (m.content or "")[:200]
        if len(m.content or "") > 200:
            contenido += "..."
        print(f"  {i}. [{tipo}] {contenido}")


def main() -> None:
    print("=" * 60)
    print("EJERCICIO 2 - Memoria por resumen [SOLUCIÓN]")
    print("=" * 60)

    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)

    # Simulación de varios turnos (sin UI)
    turnos_usuario = [
        "Me llamo Ana y estoy aprendiendo LangChain.",
        "¿Recuerdas cómo me llamo?",
        "Quiero usar RAG con PDFs.",
        "¿Qué librería de troceado mencioné en mi última frase? (trampa: no lo dije)",
        "Responde solo con OK si entiendes.",
        "Vuelve a decirme mi nombre.",
    ]

    historial: list = []

    for i, texto_usuario in enumerate(turnos_usuario, 1):
        historial.append(HumanMessage(content=texto_usuario))
        # Respuesta simulada del asistente (podría ser llm.invoke(historial))
        historial.append(
            AIMessage(
                content=llm.invoke(
                    historial
                ).content
                or ""
            )
        )
        print(f"\n--- Tras turno simulado {i} ---")
        print(f"Usuario: {texto_usuario}")
        print(f"Historial: {len(historial)} mensajes")

        if len(historial) > LIMITE_MENSAJES:
            print("\n>>> Umbral superado: compactando...")
            imprimir_historial_etiquetado(historial, "ANTES")
            historial = compactar_historial(historial, llm)
            imprimir_historial_etiquetado(historial, "DESPUÉS")

    print("\n" + "=" * 60)
    print("Historial final completo:")
    imprimir_historial_etiquetado(historial, "FINAL")


if __name__ == "__main__":
    main()
