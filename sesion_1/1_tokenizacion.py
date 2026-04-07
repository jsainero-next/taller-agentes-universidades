"""
Sesión 1 - Ejemplo 1: Tokenización en vivo

Muestra cómo una frase se convierte en IDs de tokens y cómo esto afecta
al coste y al límite de contexto.
"""

import tiktoken


def imprimir_tabla_tokens(encoding: tiktoken.Encoding, tokens: list[int]) -> None:
    col_id = 10
    col_texto = 20
    separador = f"  {'─' * col_id}┼{'─' * col_texto}"
    cabecera = f"  {'Token ID':^{col_id}}│{'Texto':^{col_texto}}"
    print(separador.replace("┼", "┬").replace("─", "─"))
    print(cabecera)
    print(separador)
    for token_id in tokens:
        raw = encoding.decode_single_token_bytes(token_id)
        try:
            texto = raw.decode("utf-8")
        except UnicodeDecodeError:
            texto = repr(raw)
        texto_display = repr(texto) if texto.strip() == "" else texto
        print(f"  {token_id:^{col_id}}│{texto_display:^{col_texto}}")
    print(separador.replace("┼", "┴").replace("─", "─"))


def main() -> None:
    # Usamos el encoding de GPT-5.4-nano (o200k_base)
    encoding = tiktoken.get_encoding("o200k_base")

    frases = [
        "Hola, ¿cómo estás?",
        "La inteligencia artificial está transformando el mundo.",
        "Python es un lenguaje de programación muy popular para machine learning.",
    ]

    print("=" * 60)
    print("TOKENIZACIÓN EN VIVO")
    print("=" * 60)
    print(f"\nEncoding usado: o200k_base (GPT-5.4-nano)\n")

    for frase in frases:
        tokens = encoding.encode(frase)
        print(f"Frase: \"{frase}\"")
        print(f"  Tokens IDs: {tokens}")
        print(f"  Número de tokens: {len(tokens)}")
        imprimir_tabla_tokens(encoding, tokens)

        # Coste aproximado (GPT-5.4-nano: ~$0.15/1M input, ~$0.60/1M output)
        coste_estimado_input = (len(tokens) / 1_000_000) * 0.15
        coste_estimado_output = (len(tokens) / 1_000_000) * 0.60
        print(f"  Coste estimado (input): ~${coste_estimado_input:.6f}")
        print(f"  Coste estimado (output): ~${coste_estimado_output:.6f}")
        print()

    # Decodificar: mostrar que los IDs vuelven al texto original
    print("-" * 60)
    print("DECODIFICACIÓN: tokens -> texto")
    ejemplo = "Hola mundo"
    tokens_ejemplo = encoding.encode(ejemplo)
    texto_decodificado = encoding.decode(tokens_ejemplo)
    print(f"Original:  \"{ejemplo}\"")
    print(f"Tokens:    {tokens_ejemplo}")
    imprimir_tabla_tokens(encoding, tokens_ejemplo)
    print(f"Decodificado: \"{texto_decodificado}\"")

    # Límite de contexto
    print("\n" + "=" * 60)
    print("LÍMITE DE CONTEXTO")
    print("=" * 60)
    print("GPT-5.4-nano: ~128K tokens de contexto")
    print("GPT-5.4-nano: ~128K tokens de contexto")
    print("Un texto de ~1000 palabras ≈ 1300 tokens aprox")


if __name__ == "__main__":
    main()
