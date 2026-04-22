"""
Sesión 1 - Ejercicio 1: Clasificador de tickets (JSON)

Objetivo
--------
Dado un correo de soporte en texto libre, el modelo debe devolver un JSON
válido con:
  - categoria: una de "Facturacion", "ErrorTecnico", "ConsultaGeneral"
  - prioridad: entero del 1 al 5 (5 = urgente)
  - id_pedido: string con el número de pedido si aparece en el texto,
    o null si no hay ninguno

Instrucciones
-------------
1. Completa la variable PROMPT_INSTRUCCIONES con instrucciones claras y
   el texto del correo (usa CORREO_EJEMPLO o pide uno por input).
2. Crea el ChatOpenAI con response_format json_object (igual que en
   sesion_1/4_extraccion_json.py).
3. Parsea la respuesta con json.loads y muestra los campos.

Pista: enumera en el prompt las categorías permitidas y cómo inferir la
prioridad (tono del usuario, palabras como "urgente", etc.).
"""

import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

CORREO_EJEMPLO = """
Hola, soy cliente desde hace años. El pedido #A-88421 sigue sin llegar
y necesito la factura YA. Esto es inaceptable.
Saludos,
Laura
"""

# TODO: redacta el prompt completo (instrucciones + correo a analizar).
PROMPT_INSTRUCCIONES = """
"""


def main() -> None:
    print("=" * 60)
    print("EJERCICIO 1 - Clasificador de tickets (JSON)")
    print("=" * 60)

    # TODO: instancia el modelo con JSON mode y temperature=0
    # llm = ChatOpenAI(...)

    # TODO: invoca el modelo y parsea el JSON
    # response = llm.invoke(PROMPT_INSTRUCCIONES)
    # datos = json.loads(response.content)

    raise NotImplementedError("Completa este ejercicio antes de ejecutar.")


if __name__ == "__main__":
    main()
