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