from pathlib import Path

pasta_data = Path("../data")

documentos = []

for arquivo in pasta_data.rglob("*.md"):

    conteudo = arquivo.read_text(
        encoding="utf-8"
    )

    documentos.append({
        "arquivo": arquivo.name,
        "conteudo": conteudo
    })


print(
    f"Documentos carregados: {len(documentos)}"
)


for documento in documentos:

    print(documento["arquivo"])