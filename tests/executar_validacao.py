import csv
import requests
from pathlib import Path


PASTA_TESTES = Path(__file__).parent

ARQUIVO_DATASET = PASTA_TESTES / "dataset_validacao.csv"
ARQUIVO_RESULTADOS = PASTA_TESTES / "resultados_validacao.csv"

URL_API = "http://127.0.0.1:8000/analisar"


def executar_validacao():

    with open(
        ARQUIVO_DATASET,
        "r",
        encoding="utf-8-sig"
    ) as arquivo:

        leitor = csv.DictReader(arquivo)

        casos = list(leitor)

    print()
    print("=" * 70)
    print("HEALTHCHECK IA — VALIDAÇÃO")
    print("=" * 70)

    print(f"\nTotal de alegações: {len(casos)}\n")

    resultados = []

    total_acertos = 0

    for caso in casos:

        payload = {
            "titulo": caso["titulo"],
            "descricao": caso["descricao"]
        }

        print("-" * 70)
        print(f"ID: {caso['id']}")
        print(f"Título: {caso['titulo']}")
        print(f"Esperado: {caso['classe_esperada']}")

        try:

            resposta = requests.post(
                URL_API,
                json=payload,
                timeout=300
            )

            resposta.raise_for_status()

            resultado_api = resposta.json()

            classe_produzida = resultado_api["classificacao"]

            acertou = (
                classe_produzida
                == caso["classe_esperada"]
            )

            if acertou:
                total_acertos += 1
                status = "ACERTO"
            else:
                status = "ERRO"

            print(f"Produzido: {classe_produzida}")

            if acertou:
                print("Resultado: ✅ ACERTO")
            else:
                print("Resultado: ❌ ERRO")

            resultados.append({
                "id": caso["id"],
                "titulo": caso["titulo"],
                "descricao": caso["descricao"],
                "tema": caso["tema"],
                "classe_esperada": caso["classe_esperada"],
                "classe_produzida": classe_produzida,
                "status": status
            })

        except requests.RequestException as erro:

            print(f"Erro ao consultar a API: {erro}")

            resultados.append({
                "id": caso["id"],
                "titulo": caso["titulo"],
                "descricao": caso["descricao"],
                "tema": caso["tema"],
                "classe_esperada": caso["classe_esperada"],
                "classe_produzida": "ERRO NA API",
                "status": "ERRO"
            })

    with open(
        ARQUIVO_RESULTADOS,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as arquivo:

        campos = [
            "id",
            "titulo",
            "descricao",
            "tema",
            "classe_esperada",
            "classe_produzida",
            "status"
        ]

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        escritor.writeheader()
        escritor.writerows(resultados)

    total_casos = len(resultados)

    acuracia = (
        total_acertos / total_casos * 100
        if total_casos > 0
        else 0
    )

    print()
    print("=" * 70)
    print("RESUMO")
    print("=" * 70)

    print(f"Total: {total_casos}")
    print(f"Acertos: {total_acertos}")
    print(f"Erros: {total_casos - total_acertos}")
    print(f"Acurácia preliminar: {acuracia:.2f}%")

    print()
    print(
        f"Resultados salvos em: "
        f"{ARQUIVO_RESULTADOS}"
    )

    print()
    print("=" * 70)
    print("VALIDAÇÃO FINALIZADA")
    print("=" * 70)


if __name__ == "__main__":
    executar_validacao()