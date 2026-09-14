import requests


URL_API = "http://127.0.0.1:8000/analisar"


casos = [
    {
        "id": 13,
        "titulo": "Eliminar água parada garante proteção total contra dengue",
        "descricao": "Como eliminar locais com água parada ajuda a combater os criadouros do Aedes aegypti, quem elimina água parada em casa fica totalmente protegido contra dengue.",
        "esperado": "ENGANOSA"
    }
]


for caso in casos:

    print("=" * 70)
    print(f"ID: {caso['id']}")
    print(f"Título: {caso['titulo']}")
    print(f"Esperado: {caso['esperado']}")

    resposta = requests.post(
        URL_API,
        json={
            "titulo": caso["titulo"],
            "descricao": caso["descricao"]
        },
        timeout=300
    )

    resposta.raise_for_status()

    resultado = resposta.json()

    produzido = resultado["classificacao"]

    print(f"Produzido: {produzido}")

    if produzido == caso["esperado"]:
        print("Resultado: ✅ ACERTO")
    else:
        print("Resultado: ❌ ERRO")

    print()