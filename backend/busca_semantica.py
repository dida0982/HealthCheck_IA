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


pergunta = "A vacina contra gripe ajuda a evitar casos graves?"

embedding_pergunta = modelo.encode([pergunta])


similaridades = cosine_similarity(
    embedding_pergunta,
    embeddings
)[0]


top_k = 3

indices_ordenados = similaridades.argsort()[::-1]

top_indices = indices_ordenados[:top_k]


print("\n=== BUSCA SEMÂNTICA ===")

print("\nPergunta:")
print(pergunta)

print(f"\nTOP {top_k} resultados mais relevantes:\n")


for posicao, indice in enumerate(top_indices, start=1):

    chunk = chunks[indice]
    similaridade = similaridades[indice]

    print("=" * 60)

    print(f"POSIÇÃO: {posicao}")
    print(f"SIMILARIDADE: {similaridade:.4f}")
    print(f"ARQUIVO: {chunk['arquivo']}")
    print(f"CHUNK ID: {chunk['chunk_id']}")

    print("\nCONTEÚDO:")
    print(chunk["conteudo"])

    print()