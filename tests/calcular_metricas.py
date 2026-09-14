import pandas as pd
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)

BASE_DIR = Path(__file__).parent
ARQUIVO = BASE_DIR / "resultados_avaliacao_final.csv"

CLASSES = [
    "SUSTENTADA PELAS EVIDÊNCIAS",
    "PARCIALMENTE SUSTENTADA",
    "ENGANOSA",
    "CONTRADITA PELAS EVIDÊNCIAS",
    "NÃO FOI POSSÍVEL VERIFICAR",
]

df = pd.read_csv(ARQUIVO)

y_true = df["classe_esperada"]
y_pred = df["classe_produzida"]

print("=" * 70)
print("AVALIAÇÃO CIENTÍFICA — HEALTHCHECK IA")
print("=" * 70)

print(f"\nTotal de alegações: {len(df)}")
print(f"Acertos: {(y_true == y_pred).sum()}")
print(f"Erros: {(y_true != y_pred).sum()}")

# Accuracy
accuracy = accuracy_score(y_true, y_pred)

print(f"\nACCURACY: {accuracy:.4f} ({accuracy * 100:.2f}%)")

# Precision, Recall e F1 Macro
precision_macro, recall_macro, f1_macro, _ = (
    precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=CLASSES,
        average="macro",
        zero_division=0
    )
)

print("\nMÉTRICAS MACRO")
print(f"Precision: {precision_macro:.4f}")
print(f"Recall:    {recall_macro:.4f}")
print(f"F1-score:  {f1_macro:.4f}")

# Weighted F1
_, _, f1_weighted, _ = precision_recall_fscore_support(
    y_true,
    y_pred,
    labels=CLASSES,
    average="weighted",
    zero_division=0
)

print(f"\nF1 weighted: {f1_weighted:.4f}")

# Métricas por classe
print("\n" + "=" * 70)
print("MÉTRICAS POR CLASSE")
print("=" * 70)

print(
    classification_report(
        y_true,
        y_pred,
        labels=CLASSES,
        digits=4,
        zero_division=0
    )
)

# Matriz de confusão
matriz = confusion_matrix(
    y_true,
    y_pred,
    labels=CLASSES
)

matriz_df = pd.DataFrame(
    matriz,
    index=CLASSES,
    columns=CLASSES
)

print("\n" + "=" * 70)
print("MATRIZ DE CONFUSÃO")
print("Linhas = classe esperada")
print("Colunas = classe produzida")
print("=" * 70)

print(matriz_df.to_string())

# Salvar matriz
matriz_df.to_csv(
    BASE_DIR / "matriz_confusao.csv",
    encoding="utf-8-sig"
)

print("\nMatriz salva em:")
print(BASE_DIR / "matriz_confusao.csv")

print("=" * 70)