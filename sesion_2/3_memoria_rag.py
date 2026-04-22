"""
Sesión 2 - Ejemplo 2b: Memoria en Sistemas RAG

Problema: un RAG básico no recuerda conversaciones anteriores.
Si el usuario pregunta "¿Y las aplicaciones?" tras haber preguntado
sobre IA, el retriever no sabe a qué se refiere "las aplicaciones"
y recupera contexto irrelevante.

Solución: añadir un paso de reformulación (history-aware retriever)
que convierte la pregunta de seguimiento en una pregunta autónoma
antes de buscar en el vector store.

  Turno 1: "¿Qué es la inteligencia artificial?"
             → retriever busca eso directamente ✔

  Turno 2: "¿Y cuáles son sus aplicaciones?"
    SIN memoria → retriever busca "¿Y cuáles son sus aplicaciones?"  ✗
    CON memoria → se reformula a "¿Cuáles son las aplicaciones de
                  la inteligencia artificial?" y luego se busca     ✔
"""

import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

RUTA_PDF = os.path.join(os.path.dirname(__file__), "..", "datos", "documento.pdf")

# Almacén en memoria de historiales por sesión
_store: dict[str, BaseChatMessageHistory] = {}


def obtener_historial(session_id: str) -> BaseChatMessageHistory:
    if session_id not in _store:
        _store[session_id] = ChatMessageHistory()
    return _store[session_id]


def construir_rag_con_memoria(retriever, llm: ChatOpenAI):
    """
    Devuelve una cadena RAG que mantiene historial de conversación.

    Dos pasos clave:
      1. history_aware_retriever  → reformula la pregunta usando el historial
                                    para que sea autónoma antes de buscar.
      2. cadena de respuesta      → genera la respuesta con el contexto
                                    recuperado y el historial completo.
    """
    # Prompt para reformular preguntas de seguimiento
    prompt_reformulacion = ChatPromptTemplate.from_messages([
        ("system",
         "Dado el historial de conversación y la última pregunta del usuario, "
         "reformúlala como una pregunta autónoma que se entienda sin el historial. "
         "Si ya es autónoma, devuélvela tal cual. NO respondas la pregunta."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, prompt_reformulacion
    )

    # Prompt para generar la respuesta final
    prompt_respuesta = ChatPromptTemplate.from_messages([
        ("system",
         "Responde la pregunta basándote solo en el siguiente contexto:\n\n{context}"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    cadena_respuesta = create_stuff_documents_chain(llm, prompt_respuesta)

    # Cadena completa: recuperar + responder
    cadena_rag = create_retrieval_chain(history_aware_retriever, cadena_respuesta)

    # Envolver con gestión automática de historial por sesión
    return RunnableWithMessageHistory(
        cadena_rag,
        obtener_historial,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )


def demo_sin_memoria(chain_sin_memoria, preguntas: list[str]) -> None:
    print("\n" + "─" * 60)
    print("❌  RAG SIN MEMORIA")
    print("─" * 60)
    print("   Cada pregunta se trata de forma aislada.")
    for i, pregunta in enumerate(preguntas, 1):
        print(f"\n  Turno {i}: \"{pregunta}\"")
        resultado = chain_sin_memoria.invoke({"input": pregunta})
        respuesta = resultado.get("answer") or resultado
        print(f"  Respuesta: {str(respuesta)[:300]}")


def demo_con_memoria(chain_con_memoria, preguntas: list[str], session_id: str) -> None:
    print("\n" + "─" * 60)
    print("✅  RAG CON MEMORIA")
    print("─" * 60)
    print("   Las preguntas de seguimiento se reformulan automáticamente.")
    config = {"configurable": {"session_id": session_id}}
    for i, pregunta in enumerate(preguntas, 1):
        print(f"\n  Turno {i}: \"{pregunta}\"")
        resultado = chain_con_memoria.invoke({"input": pregunta}, config=config)
        print(f"  Respuesta: {resultado['answer'][:300]}")

    # Mostrar el historial acumulado al final
    historial = obtener_historial(session_id).messages
    print(f"\n  Historial guardado: {len(historial)} mensajes en total")


def main() -> None:
    print("=" * 60)
    print("MEMORIA EN SISTEMAS RAG")
    print("=" * 60)

    # ── Preparar vector store (idéntico al ejemplo 2) ──────────
    print("\n1. Cargando y troceando el PDF...")
    loader = PyPDFLoader(RUTA_PDF)
    documentos = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    )
    chunks = splitter.split_documents(documentos)
    print(f"   {len(chunks)} chunks generados a partir de {len(documentos)} páginas")

    print("\n2. Generando embeddings...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="doc_memoria",
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)

    # ── Cadena sin memoria (del ejemplo 2) ─────────────────────
    def formatear_contexto(docs):
        return "\n\n".join(d.page_content for d in docs)

    prompt_simple = ChatPromptTemplate.from_template(
        "Responde la pregunta basándote solo en el siguiente contexto:\n\n{context}\n\n"
        "Pregunta: {input}"
    )
    chain_sin_memoria = (
        RunnablePassthrough.assign(
            context=lambda x: formatear_contexto(retriever.invoke(x["input"]))
        )
        | prompt_simple
        | llm
        | StrOutputParser()
    ).with_config({"output_key": "answer"})

    # Envolver para tener la misma interfaz que la cadena con memoria
    class ChainWrapper:
        def __init__(self, chain):
            self._chain = chain

        def invoke(self, inputs):
            return {"answer": self._chain.invoke(inputs)}

    chain_sin_memoria = ChainWrapper(chain_sin_memoria)

    # ── Cadena con memoria ──────────────────────────────────────
    chain_con_memoria = construir_rag_con_memoria(retriever, llm)

    # ── Conversación de prueba ──────────────────────────────────
    preguntas = [
        "¿Qué es la inteligencia artificial según el documento?",
        "¿Y cuáles son sus principales aplicaciones?",   # pregunta de seguimiento
    ]

    print("\n3. Comparativa: mismas dos preguntas con y sin memoria")

    demo_sin_memoria(chain_sin_memoria, preguntas)
    demo_con_memoria(chain_con_memoria, preguntas, session_id="usuario_demo")

    print("\n" + "=" * 60)
    print("CONCLUSIÓN")
    print("=" * 60)
    print("""
  Sin memoria: "¿Y cuáles son sus principales aplicaciones?"
               llega al retriever tal cual → contexto pobre.

  Con memoria: el LLM primero reformula la pregunta a algo como
               "¿Cuáles son las principales aplicaciones de la
               inteligencia artificial?" y LUEGO busca en el
               vector store → contexto relevante.

  Patrón clave:
    historia  ──►  reformulación  ──►  retriever  ──►  LLM  ──►  respuesta
                   (pregunta                           (con
                    autónoma)                           contexto
                                                        + historial)
""")


if __name__ == "__main__":
    main()
