"""
Sesión 2 - Ejemplo 1: Búsqueda Semántica

Genera embeddings de 3 frases y encuentra cuál es la más parecida a una
pregunta del usuario (sin usar palabras exactas).
"""

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from numpy import dot
from numpy.linalg import norm

load_dotenv()


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Calcula la similitud coseno entre dos vectores."""
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))


def main() -> None:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    frases = [
        "Python es un lenguaje de programación interpretado y de alto nivel.",
        "La inteligencia artificial permite que las máquinas aprendan de datos.",
        "El café se prepara moliendo granos y filtrando con agua caliente.",
    ]

    pregunta = "¿Cómo funcionan los sistemas que aprenden automáticamente?"

    print("=" * 60)
    print("BÚSQUEDA SEMÁNTICA")
    print("=" * 60)
    print(f"\nFrases de referencia:")
    for i, f in enumerate(frases, 1):
        print(f"  {i}. {f}")
    print(f"\nPregunta del usuario: \"{pregunta}\"")
    print("\n(La pregunta no usa las mismas palabras que las frases.)\n")

    # Generar embeddings
    embeddings_frases = embeddings.embed_documents(frases)
    embedding_pregunta = embeddings.embed_query(pregunta)

    # Calcular similitud
    print("-" * 60)
    print("Similitud coseno (pregunta vs cada frase):")
    similitudes = []
    for i, (frase, emb) in enumerate(zip(frases, embeddings_frases)):
        sim = cosine_similarity(emb, embedding_pregunta)
        similitudes.append((i, sim))
        print(f"  Frase {i + 1}: {sim:.4f}")

    mejor_idx = max(similitudes, key=lambda x: x[1])[0]
    print(f"\nLa frase más similar es la #{mejor_idx + 1}: \"{frases[mejor_idx]}\"")
    print("\nLa búsqueda semántica encuentra significado, no palabras.")


if __name__ == "__main__":
    main()
