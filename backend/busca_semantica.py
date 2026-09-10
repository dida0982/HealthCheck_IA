from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
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
)


indice_mais_similar = similaridades[0].argmax()

maior_similaridade = similaridades[0][indice_mais_similar]

print("\n=== RESULTADO ===")

print(f"Quantidade de chunks: {len(chunks)}")
print(f"Quantidade de textos: {len(textos)}")

print(f"Formato dos embeddings: {embeddings.shape}")

print("\nPrimeiro chunk:")
print(chunks[0]["conteudo"][:300])

print("\nArquivo de origem:")
print(chunks[0]["arquivo"])

print("\nID do chunk:")
print(chunks[0]["chunk_id"])

print("\nPrimeiros 10 números do embedding:")
print(embeddings[0][:10])