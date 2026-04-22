"""
Sesión 2 - Ejemplo 2: Conexión a Documentos

Carga un PDF, lo trocea (chunking) y realiza una consulta simple sobre él.
"""

import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Ruta relativa al directorio raíz del proyecto
RUTA_PDF = os.path.join(os.path.dirname(__file__), "..", "datos", "documento.pdf")


def formatear_contexto(docs: list) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def main() -> None:
    print("=" * 60)
    print("CONEXIÓN A DOCUMENTOS (RAG)")
    print("=" * 60)

    # 1. Cargar el PDF
    print("\n1. Cargando PDF...")
    loader = PyPDFLoader(RUTA_PDF)
    documentos = loader.load()
    print(f"   Páginas cargadas: {len(documentos)}")

    # 2. Trocear (chunking)
    print("\n2. Troceando documento...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documentos)
    print(f"   Chunks generados: {len(chunks)}")

    # 3. Crear vector store
    print("\n3. Generando embeddings y almacenando en Chroma...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="documento_pdf",
    )
    retriever = vector_store.as_retriever(k=3)

    # 4. Crear cadena RAG con LCEL
    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "Responde la pregunta basándote solo en el siguiente contexto:\n\n{context}\n\n"
        "Pregunta: {input}"
    )
    chain = (
        RunnablePassthrough.assign(
            context=lambda x: formatear_contexto(retriever.invoke(x["input"]))
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    # 5. Consulta
    pregunta = "¿Qué es la inteligencia artificial según el documento?"
    print(f"\n4. Consulta: \"{pregunta}\"")
    print("\nRespuesta:")
    resultado = chain.invoke({"input": pregunta})
    print(resultado)


if __name__ == "__main__":
    main()
