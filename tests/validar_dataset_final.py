import pandas as pd
from pathlib import Path

ARQUIVO = Path(__file__).parent / "dataset_avaliacao_final.csv"

CLASSES_ESPERADAS = [
    "SUSTENTADA PELAS EVIDÊNCIAS",
    "PARCIALMENTE SUSTENTADA",
    "ENGANOSA",
    "CONTRADITA PELAS EVIDÊNCIAS",
    "NÃO FOI POSSÍVEL VERIFICAR",
]

COLUNAS_ESPERADAS = [
    "id",
    "titulo",
    "descricao",
    "classe_esperada",
    "tema",
]

print("=" * 60)
print("VALIDAÇÃO DO DATASET FINAL — HEALTHCHECK IA")
print("=" * 60)

try:
    df = pd.read_csv(ARQUIVO)
except Exception as erro:
    print("\n❌ ERRO AO LER O CSV")
    print(erro)
    raise SystemExit(1)

erros = []

# 1. Verificar colunas
if list(df.columns) != COLUNAS_ESPERADAS:
    erros.append(
        f"Colunas incorretas.\n"
        f"Esperado: {COLUNAS_ESPERADAS}\n"
        f"Encontrado: {list(df.columns)}"
    )

# 2. Verificar quantidade
if len(df) != 200:
    erros.append(f"O dataset possui {len(df)} registros. Esperado: 200.")

# 3. Verificar IDs
ids_esperados = set(range(1, 201))
ids_encontrados = set(df["id"].dropna().tolist())

faltando = ids_esperados - ids_encontrados
extras = ids_encontrados - ids_esperados

if faltando:
    erros.append(f"IDs faltando: {sorted(faltando)}")

if extras:
    erros.append(f"IDs fora do intervalo 1–200: {sorted(extras)}")

# 4. IDs duplicados
duplicados = df[df["id"].duplicated(keep=False)]["id"].tolist()

if duplicados:
    erros.append(f"IDs duplicados: {sorted(set(duplicados))}")

# 5. Campos vazios
if df.isnull().any().any():
    linhas_vazias = df[df.isnull().any(axis=1)]["id"].tolist()
    erros.append(f"Existem campos vazios nos IDs: {linhas_vazias}")

# 6. Classes
classes_encontradas = set(df["classe_esperada"].dropna().unique())

classes_invalidas = classes_encontradas - set(CLASSES_ESPERADAS)

if classes_invalidas:
    erros.append(
        f"Classes inválidas encontradas: {sorted(classes_invalidas)}"
    )

# 7. Contagem por classe
print("\nCONTAGEM POR CLASSE:")
contagem = df["classe_esperada"].value_counts()

for classe in CLASSES_ESPERADAS:
    quantidade = contagem.get(classe, 0)
    simbolo = "✅" if quantidade == 40 else "❌"
    print(f"{simbolo} {classe}: {quantidade}")

    if quantidade != 40:
        erros.append(
            f'A classe "{classe}" possui {quantidade} registros. Esperado: 40.'
        )

# Resultado final
print("\n" + "=" * 60)

if erros:
    print("❌ DATASET COM PROBLEMAS\n")

    for numero, erro in enumerate(erros, start=1):
        print(f"{numero}. {erro}")

    print("\nCorrija os problemas antes de executar a avaliação.")

else:
    print("✅ DATASET VÁLIDO")
    print(f"Total de registros: {len(df)}")
    print("IDs: 1–200")
    print("Classes: 5")
    print("Registros por classe: 40")
    print("IDs duplicados: 0")
    print("Campos vazios: 0")
    print("\nO dataset está pronto para a avaliação final.")

print("=" * 60)