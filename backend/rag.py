from busca_semantica import buscar_evidencias


def montar_contexto_rag(alegacao, top_k=3):

    evidencias = buscar_evidencias(
        alegacao,
        top_k=top_k
    )

    contexto = f"""
ALEGAÇÃO:

{alegacao}

EVIDÊNCIAS RECUPERADAS:
"""

    for posicao, evidencia in enumerate(evidencias, start=1):

        contexto += f"""

EVIDÊNCIA {posicao}

Arquivo:
{evidencia["arquivo"]}

Chunk:
{evidencia["chunk_id"]}

Similaridade:
{evidencia["similaridade"]:.4f}

Conteúdo:
{evidencia["conteudo"]}
"""

    return contexto


if __name__ == "__main__":

    alegacao = "A vacina contra gripe ajuda a evitar casos graves?"

    contexto = montar_contexto_rag(
        alegacao,
        top_k=3
    )

    print("\n=== CONTEXTO RAG ===")
    print(contexto)