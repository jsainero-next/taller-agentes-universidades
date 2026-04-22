"""
Sesión 2 - Ejemplo 4: El "Loop" del Agente

Un agente que combina RAG (documentos) y herramientas (búsqueda web).
Muestra cómo "razona" en la consola antes de dar la respuesta final.
"""

import os

import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

@tool
def internet_search(query: str) -> str:
    """Busca información actual en internet. Úsala para noticias o datos recientes."""
    from googlesearch import search
    
    try:
        results = []
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

# Ruta relativa al directorio del script
RUTA_PDF = os.path.join(os.path.dirname(__file__), "..", "datos", "documento.pdf")


def crear_retriever_tool():
    """Crea una herramienta que busca en el PDF."""
    loader = PyPDFLoader(RUTA_PDF)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma.from_documents(chunks, embeddings, collection_name="doc_agente")
    retriever = vector_store.as_retriever(k=2)

    @tool
    def buscar_en_documento(consulta: str) -> str:
        """Busca información en el documento PDF sobre inteligencia artificial.
        Usa esta herramienta cuando la pregunta sea sobre el contenido del documento."""
        docs = retriever.invoke(consulta)
        return "\n\n".join(d.page_content for d in docs)

    return buscar_en_documento


def main() -> None:
    # busqueda_web = DuckDuckGoSearchRun()
    buscar_doc = crear_retriever_tool()

    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
    agent = create_react_agent(
        llm,
        tools=[buscar_doc, internet_search],
        prompt="Eres un asistente experto. Tienes dos herramientas:\n"
        "1. buscar_en_documento: para consultar el PDF sobre IA.\n"
        "2. internet_search: para buscar noticias o información actual en internet.\n"
        "Usa la herramienta apropiada según la pregunta. Puedes usar varias si es necesario.",
    )

    pregunta = "¿Qué dice el documento sobre la IA? Y ¿hay noticias recientes sobre ChatGPT?"

    print("=" * 60)
    print("LOOP DEL AGENTE (RAG + Tools)")
    print("=" * 60)
    print(f"\nPregunta: \"{pregunta}\"")
    print("\nEl agente razonará paso a paso, usando RAG y/o búsqueda web...\n")

    inputs = {"messages": [{"role": "user", "content": pregunta}]}

    for chunk in agent.stream(inputs, stream_mode="updates"):
        for node_name, node_output in chunk.items():
            if "messages" in node_output:
                for msg in node_output["messages"]:
                    if hasattr(msg, "content") and msg.content:
                        print(f"[{node_name}] {msg.content[:300]}")
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tc in msg.tool_calls:
                            args = tc.get("args", {})
                            print(f"  -> Tool: {tc.get('name')} | args: {args}")

    result = agent.invoke(inputs)
    print("\n" + "=" * 60)
    print("RESPUESTA FINAL:")
    print("=" * 60)
    last_msg = result["messages"][-1]
    print(last_msg.content if hasattr(last_msg, "content") else last_msg)


if __name__ == "__main__":
    main()
