import csv
import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent

ARQUIVO_ENTRADA = BASE_DIR / "dataset_avaliacao_final.csv"
ARQUIVO_SAIDA = BASE_DIR / "resultados_avaliacao_final.csv"

URL_API = "http://127.0.0.1:8000/analisar"

resultados = []

with open(ARQUIVO_ENTRADA, "r", encoding="utf-8-sig") as arquivo:
    leitor = csv.DictReader(arquivo)

    for linha in leitor:
        id_ = linha["id"]
        titulo = linha["titulo"]
        descricao = linha["descricao"]
        classe_esperada = linha["classe_esperada"]
        tema = linha["tema"]

        print(f"\nAnalisando ID {id_}...")

        payload = {
            "titulo": titulo,
            "descricao": descricao
        }

        try:
            resposta = requests.post(
                URL_API,
                json=payload,
                timeout=180
            )

            resposta.raise_for_status()

            dados = resposta.json()

            classe_produzida = dados.get(
                "classificacao",
                "ERRO_SEM_CLASSIFICACAO"
            )

            status = (
                "ACERTO"
                if classe_produzida == classe_esperada
                else "ERRO"
            )

            print(f"Esperado:  {classe_esperada}")
            print(f"Produzido: {classe_produzida}")
            print(f"Status:    {status}")

        except Exception as erro:
            classe_produzida = "ERRO_EXECUCAO"
            status = "ERRO"

            print(f"ERRO na execução do ID {id_}: {erro}")

        resultados.append({
            "id": id_,
            "titulo": titulo,
            "descricao": descricao,
            "tema": tema,
            "classe_esperada": classe_esperada,
            "classe_produzida": classe_produzida,
            "status": status
        })

        # salva continuamente para não perder progresso
        with open(
            ARQUIVO_SAIDA,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as saida:

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
                saida,
                fieldnames=campos
            )

            escritor.writeheader()
            escritor.writerows(resultados)

print("\n" + "=" * 60)
print("AVALIAÇÃO FINAL CONCLUÍDA")
print("=" * 60)
print(f"Total processado: {len(resultados)}")
print(f"Arquivo salvo em:")
print(ARQUIVO_SAIDA)