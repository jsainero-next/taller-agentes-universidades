"""
Sesión 2 - Ejercicio 1 (SOLUCIÓN): Evaluador de relevancia (RAG con filtro)
"""

import json
import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

RUTA_PDF = os.path.join(os.path.dirname(__file__), "..", "..", "..", "datos", "documento.pdf")


def formatear_contexto(docs: list) -> str:
    partes = []
    for i, d in enumerate(docs, 1):
        partes.append(f"--- Fragmento {i} ---\n{d.page_content}")
    return "\n\n".join(partes)


def evaluar_relevancia(
    pregunta: str, contexto: str, llm: ChatOpenAI
) -> tuple[bool, str]:
    prompt = f"""Eres un evaluador estricto. Dada la pregunta del usuario y los fragmentos
recuperados de un documento, decide si es razonable responder la pregunta usando SOLO
esa información (es decir, los fragmentos contienen datos suficientes y relacionados).

Responde únicamente con un objeto JSON válido con estas claves:
- "es_relevante": true o false
- "razon": una frase breve en español

Pregunta del usuario:
{pregunta}

Fragmentos recuperados:
{contexto}
"""
    resp = llm.invoke(prompt)
    data = json.loads(resp.content)
    return bool(data.get("es_relevante")), str(data.get("razon", ""))


def responder_con_contexto(pregunta: str, contexto: str, llm: ChatOpenAI) -> str:
    plantilla = ChatPromptTemplate.from_template(
        "Responde la pregunta basándote solo en el siguiente contexto. "
        "Si algo no está en el contexto, dilo explícitamente.\n\n"
        "Contexto:\n{context}\n\nPregunta: {input}"
    )
    cadena = plantilla | llm | StrOutputParser()
    return cadena.invoke({"context": contexto, "input": pregunta})


def pipeline_pregunta(pregunta: str, retriever, llm_eval: ChatOpenAI, llm_gen: ChatOpenAI) -> None:
    print(f"\nPregunta: {pregunta!r}")
    docs = retriever.invoke(pregunta)
    contexto = formatear_contexto(docs)
    print("-" * 60)
    print("Fragmentos recuperados (resumen):")
    print(contexto[:500] + ("..." if len(contexto) > 500 else ""))

    relevante, razon = evaluar_relevancia(pregunta, contexto, llm_eval)
    print("-" * 60)
    print(f"Evaluador: es_relevante={relevante}")
    print(f"Razón: {razon}")

    if relevante:
        print("-" * 60)
        print("Respuesta RAG:")
        print(responder_con_contexto(pregunta, contexto, llm_gen))
    else:
        print("-" * 60)
        print(
            "No se genera respuesta a partir de los documentos: "
            "el contexto recuperado no es suficiente o no está alineado con la pregunta."
        )


def main() -> None:
    print("=" * 60)
    print("EJERCICIO 1 - Evaluador de relevancia [SOLUCIÓN]")
    print("=" * 60)

    print("\n1. Cargando PDF y construyendo vector store...")
    loader = PyPDFLoader(RUTA_PDF)
    documentos = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documentos)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="ej_s2_ej1",
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    llm_eval = ChatOpenAI(
        model="gpt-5.4-nano",
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}},
    )
    llm_gen = ChatOpenAI(model="gpt-5.4-nano", temperature=0)

    print("\n2. Caso alineado con el documento (típicamente relevante):")
    pipeline_pregunta(
        "¿Qué es la inteligencia artificial según el documento?",
        retriever,
        llm_eval,
        llm_gen,
    )

    print("\n\n3. Caso probablemente fuera de tema (típicamente no relevante):")
    pipeline_pregunta(
        "¿Cuál es la receta exacta del gazpacho andaluz tradicional?",
        retriever,
        llm_eval,
        llm_gen,
    )


if __name__ == "__main__":
    main()
