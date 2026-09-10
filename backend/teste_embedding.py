from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

frase = "A vacina contra gripe ajuda a reduzir casos graves."

embedding = modelo.encode(frase)

print("Frase:")
print(frase)

print("\nEmbedding:")
print(embedding)

print("\nQuantidade de dimensões:")
print(len(embedding))