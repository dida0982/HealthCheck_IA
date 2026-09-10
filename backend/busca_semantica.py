from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from carregar_documentos import chunks


modelo = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


textos = []

for chunk in chunks:
    textos.append(chunk["conteudo"])


embeddings = modelo.encode(
    textos,
    show_progress_bar=True
)


def buscar_evidencias(pergunta, top_k=3):

    embedding_pergunta = modelo.encode([pergunta])

    similaridades = cosine_similarity(
        embedding_pergunta,
        embeddings
    )[0]

    indices_ordenados = similaridades.argsort()[::-1]

    top_indices = indices_ordenados[:top_k]

    resultados = []

    for indice in top_indices:

        chunk = chunks[indice]

        resultados.append({
            "arquivo": chunk["arquivo"],
            "chunk_id": chunk["chunk_id"],
            "conteudo": chunk["conteudo"],
            "similaridade": float(similaridades[indice])
        })

    return resultados


if __name__ == "__main__":

    pergunta = "A vacina contra gripe ajuda a evitar casos graves?"

    resultados = buscar_evidencias(
        pergunta,
        top_k=3
    )

    print("\n=== BUSCA SEMÂNTICA ===")

    print("\nPergunta:")
    print(pergunta)

    print("\nTOP 3 resultados mais relevantes:\n")

    for posicao, resultado in enumerate(resultados, start=1):

        print("=" * 60)

        print(f"POSIÇÃO: {posicao}")
        print(f"SIMILARIDADE: {resultado['similaridade']:.4f}")
        print(f"ARQUIVO: {resultado['arquivo']}")
        print(f"CHUNK ID: {resultado['chunk_id']}")

        print("\nCONTEÚDO:")
        print(resultado["conteudo"])

        print()