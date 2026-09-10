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
)


indice_mais_similar = similaridades[0].argmax()

maior_similaridade = similaridades[0][indice_mais_similar]


print("\n=== BUSCA POR SIMILARIDADE ===")

print("\nPergunta:")
print(pergunta)

print("\nMaior similaridade:")
print(maior_similaridade)

print("\nChunk mais parecido:")
print(chunks[indice_mais_similar]["conteudo"])

print("\nArquivo de origem:")
print(chunks[indice_mais_similar]["arquivo"])

print("\nID do chunk:")
print(chunks[indice_mais_similar]["chunk_id"])