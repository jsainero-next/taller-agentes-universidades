"""Genera el PDF de ejemplo para los ejercicios de RAG."""

from pathlib import Path

from fpdf import FPDF

RUTA_SALIDA = Path(__file__).resolve().parent.parent / "datos" / "documento.pdf"

CONTENIDO = """
INTELIGENCIA ARTIFICIAL: UNA INTRODUCCIÓN

La inteligencia artificial (IA) es la rama de la informática que se dedica a crear sistemas capaces de realizar tareas que normalmente requieren inteligencia humana. Estos sistemas pueden aprender de datos, reconocer patrones, tomar decisiones y mejorar con la experiencia.

La IA se divide en varios subcampos. El machine learning permite que las máquinas aprendan automáticamente a partir de ejemplos sin ser programadas explícitamente para cada tarea. El deep learning utiliza redes neuronales con muchas capas para procesar grandes cantidades de datos y extraer representaciones complejas.

Las aplicaciones de la IA son muy diversas: asistentes virtuales, vehículos autónomos, diagnóstico médico, traducción automática, recomendación de contenidos y muchos más. La IA está transformando industrias enteras y cambiando la forma en que interactuamos con la tecnología.

Los grandes modelos de lenguaje (LLM), como GPT o Claude, son un ejemplo reciente de IA. Estos modelos se entrenan con enormes cantidades de texto y pueden generar respuestas coherentes, traducir idiomas, resumir documentos y mantener conversaciones naturales.

El futuro de la IA plantea tanto oportunidades como desafíos. Es importante desarrollar la IA de forma responsable, considerando aspectos éticos, de privacidad y de impacto en el empleo.
""".strip()


def main() -> None:
    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=14)
    pdf.multi_cell(0, 8, CONTENIDO)
    pdf.output(str(RUTA_SALIDA))
    print(f"PDF generado: {RUTA_SALIDA}")


if __name__ == "__main__":
    main()
