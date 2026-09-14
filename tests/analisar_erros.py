import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent

ARQUIVO = BASE_DIR / "resultados_avaliacao_final.csv"
SAIDA_ERROS = BASE_DIR / "erros_avaliacao_final.csv"
SAIDA_RESUMO = BASE_DIR / "resumo_erros.csv"

df = pd.read_csv(ARQUIVO)

# ---------------------------------------------------------
# 1. Separar somente os erros
# ---------------------------------------------------------

erros = df[
    df["classe_esperada"] != df["classe_produzida"]
].copy()

print("=" * 80)
print("ANÁLISE DE ERROS — HEALTHCHECK IA")
print("=" * 80)

print(f"\nTotal avaliado: {len(df)}")
print(f"Total de erros: {len(erros)}")
print(f"Taxa de erro: {(len(erros) / len(df)) * 100:.2f}%")

# ---------------------------------------------------------
# 2. Agrupar esperado -> produzido
# ---------------------------------------------------------

resumo = (
    erros
    .groupby(
        ["classe_esperada", "classe_produzida"]
    )
    .size()
    .reset_index(name="quantidade")
    .sort_values(
        "quantidade",
        ascending=False
    )
)

print("\n" + "=" * 80)
print("ERROS AGRUPADOS: ESPERADO -> PRODUZIDO")
print("=" * 80)

for _, linha in resumo.iterrows():

    print(
        f'\n{linha["classe_esperada"]}'
        f'\n    ↓'
        f'\n{linha["classe_produzida"]}'
        f'\nQuantidade: {linha["quantidade"]}'
    )

# ---------------------------------------------------------
# 3. Erros por classe esperada
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("ERROS POR CLASSE ESPERADA")
print("=" * 80)

erros_por_classe = (
    erros["classe_esperada"]
    .value_counts()
)

for classe, quantidade in erros_por_classe.items():

    total_classe = (
        df["classe_esperada"] == classe
    ).sum()

    percentual = (
        quantidade / total_classe
    ) * 100

    print(
        f"\n{classe}"
        f"\nErros: {quantidade}/{total_classe}"
        f"\nTaxa de erro: {percentual:.2f}%"
    )

# ---------------------------------------------------------
# 4. Erros por tema
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("ERROS POR TEMA")
print("=" * 80)

erros_tema = (
    erros["tema"]
    .value_counts()
)

for tema, quantidade in erros_tema.items():

    total_tema = (
        df["tema"] == tema
    ).sum()

    percentual = (
        quantidade / total_tema
    ) * 100

    print(
        f"\n{tema}"
        f"\nErros: {quantidade}/{total_tema}"
        f"\nTaxa de erro: {percentual:.2f}%"
    )

# ---------------------------------------------------------
# 5. Mostrar cada erro
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("DETALHAMENTO DOS 49 ERROS")
print("=" * 80)

for _, linha in erros.iterrows():

    print(f'\nID: {linha["id"]}')
    print(f'Tema: {linha["tema"]}')
    print(f'Título: {linha["titulo"]}')

    print(
        f'Esperado:  '
        f'{linha["classe_esperada"]}'
    )

    print(
        f'Produzido: '
        f'{linha["classe_produzida"]}'
    )

    print("-" * 80)

# ---------------------------------------------------------
# 6. Salvar arquivos
# ---------------------------------------------------------

erros.to_csv(
    SAIDA_ERROS,
    index=False,
    encoding="utf-8-sig"
)

resumo.to_csv(
    SAIDA_RESUMO,
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 80)
print("ARQUIVOS GERADOS")
print("=" * 80)

print(f"\nErros detalhados:")
print(SAIDA_ERROS)

print(f"\nResumo das confusões:")
print(SAIDA_RESUMO)

print("\nAnálise concluída.")