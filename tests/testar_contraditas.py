import requests


URL_API = "http://127.0.0.1:8000/analisar"

casos = [
    {
        "id": 18,
        "titulo": "Não existem formas de prevenção contra o câncer",
        "descricao": "Hábitos saudáveis, vacinação, rastreamento e diagnóstico precoce não possuem nenhuma relação com a prevenção do câncer.",
        "esperado": "CONTRADITA PELAS EVIDÊNCIAS"
    },
    {
        "id": 20,
        "titulo": "Atividade física não ajuda na prevenção do diabetes tipo 2",
        "descricao": "A prática regular de atividade física não possui relação com a prevenção do diabetes tipo 2.",
        "esperado": "CONTRADITA PELAS EVIDÊNCIAS"
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