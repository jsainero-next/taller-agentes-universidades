"""
Sesión 2 - Ejemplo 3: Uso de Herramientas (Tools)

El LLM decide usar una herramienta de búsqueda web (DuckDuckGo) para
responder sobre una noticia reciente.
"""

import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

@tool
def internet_search(query: str) -> str:
    """Busca información actual en internet. Úsala para noticias o datos recientes."""
    from googlesearch import search
    
    try:
        # Realizamos la búsqueda en Google (gratuito, sin API Key)
        # En la versión 1.3.0 de googlesearch-python, los parámetros son 'term' y 'num_results'
        # search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0, timeout=5)
        results = []
        # Obtenemos un iterador de URLs
        search_results = search(query, num_results=5, lang="es")
        
        for url in search_results:
            results.append(f"Enlace encontrado: {url}")
            if len(results) >= 5:
                break
        
        if not results:
            return "No se encontraron resultados para esta búsqueda."
            
        return "He encontrado los siguientes enlaces relevantes:\n\n" + "\n".join(results)
    except Exception as e:
        return f"Error al buscar en internet: {str(e)}"


load_dotenv()


def main() -> None:
    # Herramienta de búsqueda web
    # busqueda_web = DuckDuckGoSearchRun()

    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
    agent = create_react_agent(
        llm,
        tools=[internet_search],
        prompt="Eres un asistente que puede buscar información en internet. "
        "Usa la búsqueda web cuando necesites información actual o reciente.",
    )

    pregunta = "¿Cuáles son las últimas noticias sobre inteligencia artificial hoy?"

    print("=" * 60)
    print("USO DE HERRAMIENTAS (Tools)")
    print("=" * 60)
    print(f"\nPregunta: \"{pregunta}\"")
    print("\nEl agente decidirá si necesita buscar en la web...\n")

    inputs = {"messages": [{"role": "user", "content": pregunta}]}

    for chunk in agent.stream(inputs, stream_mode="updates"):
        for node_name, node_output in chunk.items():
            if "messages" in node_output:
                for msg in node_output["messages"]:
                    if hasattr(msg, "content") and msg.content:
                        print(f"[{node_name}] {msg.content[:200]}...")
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tc in msg.tool_calls:
                            print(f"  -> Llamando herramienta: {tc.get('name', '?')}")

    result = agent.invoke(inputs)
    print("\n" + "=" * 60)
    print("RESPUESTA FINAL:")
    print("=" * 60)
    last_msg = result["messages"][-1]
    print(last_msg.content if hasattr(last_msg, "content") else last_msg)


if __name__ == "__main__":
    main()
