"""
Sesión 2 - Ejercicio 1: Evaluador de relevancia (RAG con filtro)

Objetivo
--------
Tras recuperar fragmentos del vector store, un segundo paso con el LLM
decide si el contexto es realmente útil para la pregunta. Solo si es así
se genera la respuesta RAG; si no, se informa al usuario de que no hay
información suficiente en los documentos.

Instrucciones
-------------
1. Reutiliza el patrón de carga de PDF, chunking y Chroma de
   sesion_2/2_conexion_documentos.py (ajusta la ruta al PDF: desde esta
   carpeta son dos niveles arriba hasta la raíz del proyecto, luego datos/).
2. Recupera k fragmentos con el retriever para una PREGUNTA fija.
3. Construye un prompt que pida al modelo un JSON con:
   - es_relevante (booleano)
   - razon (breve texto)
   Usa response_format json_object como en sesion_1/4_extraccion_json.py.
4. Si es_relevante es True, invoca una cadena RAG (prompt + contexto + pregunta)
   para la respuesta final. Si es False, imprime un mensaje claro sin inventar.

Pista: formatea los fragmentos recuperados en un solo string para el
prompt del evaluador y para el generador.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Raíz del repo: sesion_2/ejercicios/ -> ../../
RUTA_PDF = os.path.join(os.path.dirname(__file__), "..", "..", "datos", "documento.pdf")

PREGUNTA = "¿Qué es la inteligencia artificial según el documento?"


def main() -> None:
    print("=" * 60)
    print("EJERCICIO 1 - Evaluador de relevancia (RAG)")
    print("=" * 60)

    # TODO: cargar PDF, trocear, vector store, retriever
    # TODO: recuperar documentos para PREGUNTA
    # TODO: paso evaluador (JSON) y decisión
    # TODO: respuesta RAG o mensaje de falta de contexto

    raise NotImplementedError("Completa este ejercicio antes de ejecutar.")


if __name__ == "__main__":
    main()
