"""
Sesión 1 - Ejercicio 1 (SOLUCIÓN): Clasificador de tickets (JSON)
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

PROMPT_INSTRUCCIONES = f"""Analiza el siguiente correo de soporte y responde SOLO con un objeto JSON válido (sin markdown ni texto adicional) con estas claves exactas:
- "categoria": debe ser exactamente una de estas cadenas: "Facturacion", "ErrorTecnico", "ConsultaGeneral".
  Usa "Facturacion" si habla de facturas, pagos o pedidos comerciales.
  Usa "ErrorTecnico" si describe fallos de software, errores o incidencias técnicas.
  Usa "ConsultaGeneral" en cualquier otro caso.
- "prioridad": número entero del 1 al 5. Usa 5 si el tono es muy urgente o enfadado, 4 si hay urgencia clara, 3 normal, 2 baja, 1 muy tranquila.
- "id_pedido": el identificador del pedido si aparece (ej. #A-88421 o similar), como string; si no hay ninguno, usa null.

Correo:
---
{CORREO_EJEMPLO.strip()}
---
"""


def main() -> None:
    print("=" * 60)
    print("EJERCICIO 1 - Clasificador de tickets (JSON) [SOLUCIÓN]")
    print("=" * 60)

    llm = ChatOpenAI(
        model="gpt-5.4-nano",
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}},
    )
    response = llm.invoke(PROMPT_INSTRUCCIONES)

    print("\nRespuesta raw:")
    print(response.content)
    print()

    datos = json.loads(response.content)
    print("-" * 60)
    print("Campos parseados:")
    print(f"  categoria:   {datos.get('categoria')}")
    print(f"  prioridad:   {datos.get('prioridad')}")
    print(f"  id_pedido:   {datos.get('id_pedido')}")


if __name__ == "__main__":
    main()
