import pandas as pd
import mlflow

from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support
)

BASE_DIR = Path(__file__).parent

ARQUIVO_RESULTADOS = BASE_DIR / "resultados_avaliacao_final.csv"
ARQUIVO_MATRIZ = BASE_DIR / "matriz_confusao.csv"
ARQUIVO_ERROS = BASE_DIR / "erros_avaliacao_final.csv"
ARQUIVO_RESUMO_ERROS = BASE_DIR / "resumo_erros.csv"

# ---------------------------------------------------------
# Configuração do experimento
# ---------------------------------------------------------

mlflow.set_experiment("HealthCheck_IA_Avaliacao_Final")

# ---------------------------------------------------------
# Carregar resultados
# ---------------------------------------------------------

df = pd.read_csv(ARQUIVO_RESULTADOS)

y_true = df["classe_esperada"]
y_pred = df["classe_produzida"]

CLASSES = [
    "SUSTENTADA PELAS EVIDÊNCIAS",
    "PARCIALMENTE SUSTENTADA",
    "ENGANOSA",
    "CONTRADITA PELAS EVIDÊNCIAS",
    "NÃO FOI POSSÍVEL VERIFICAR",
]

# ---------------------------------------------------------
# Métricas
# ---------------------------------------------------------

accuracy = accuracy_score(y_true, y_pred)

precision_macro, recall_macro, f1_macro, _ = (
    precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=CLASSES,
        average="macro",
        zero_division=0
    )
)

precision_weighted, recall_weighted, f1_weighted, _ = (
    precision_recall_fscore_support(
        y_true,
        y_pred,
        labels=CLASSES,
        average="weighted",
        zero_division=0
    )
)

total = len(df)
acertos = int((y_true == y_pred).sum())
erros = int((y_true != y_pred).sum())

# ---------------------------------------------------------
# Registrar experimento
# ---------------------------------------------------------

with mlflow.start_run(
    run_name="qwen2.5_7b_avaliacao_final_200"
):

    # Parâmetros
    mlflow.log_param("modelo", "qwen2.5:7b")
    mlflow.log_param("temperature", 0)
    mlflow.log_param("seed", 42)
    mlflow.log_param("top_k", 5)

    mlflow.log_param("dataset", "dataset_avaliacao_final.csv")
    mlflow.log_param("dataset_size", total)
    mlflow.log_param("numero_classes", 5)

    mlflow.log_param(
        "tipo_avaliacao",
        "multiclasse_balanceada"
    )

    # Métricas gerais
    mlflow.log_metric("accuracy", accuracy)

    mlflow.log_metric(
        "precision_macro",
        precision_macro
    )

    mlflow.log_metric(
        "recall_macro",
        recall_macro
    )

    mlflow.log_metric(
        "f1_macro",
        f1_macro
    )

    mlflow.log_metric(
        "precision_weighted",
        precision_weighted
    )

    mlflow.log_metric(
        "recall_weighted",
        recall_weighted
    )

    mlflow.log_metric(
        "f1_weighted",
        f1_weighted
    )

    mlflow.log_metric(
        "total_acertos",
        acertos
    )

    mlflow.log_metric(
        "total_erros",
        erros
    )

    mlflow.log_metric(
        "taxa_erro",
        erros / total
    )

    # -----------------------------------------------------
    # Métricas por classe
    # -----------------------------------------------------

    precision_cls, recall_cls, f1_cls, suporte_cls = (
        precision_recall_fscore_support(
            y_true,
            y_pred,
            labels=CLASSES,
            average=None,
            zero_division=0
        )
    )

    nomes_mlflow = [
        "sustentada",
        "parcialmente_sustentada",
        "enganosa",
        "contradita",
        "nao_verificavel",
    ]

    for i, nome in enumerate(nomes_mlflow):

        mlflow.log_metric(
            f"precision_{nome}",
            precision_cls[i]
        )

        mlflow.log_metric(
            f"recall_{nome}",
            recall_cls[i]
        )

        mlflow.log_metric(
            f"f1_{nome}",
            f1_cls[i]
        )

        mlflow.log_metric(
            f"support_{nome}",
            int(suporte_cls[i])
        )

    # -----------------------------------------------------
    # Artefatos
    # -----------------------------------------------------

    arquivos = [
        ARQUIVO_RESULTADOS,
        ARQUIVO_MATRIZ,
        ARQUIVO_ERROS,
        ARQUIVO_RESUMO_ERROS,
    ]

    for arquivo in arquivos:

        if arquivo.exists():

            mlflow.log_artifact(
                str(arquivo),
                artifact_path="avaliacao"
            )

    # Também registrar o próprio script
    mlflow.log_artifact(
        str(Path(__file__)),
        artifact_path="codigo"
    )

    # -----------------------------------------------------
    # Tags
    # -----------------------------------------------------

    mlflow.set_tag(
        "projeto",
        "HealthCheck IA"
    )

    mlflow.set_tag(
        "etapa",
        "12.12 - Avaliacao cientifica"
    )

    mlflow.set_tag(
        "tipo_modelo",
        "LLM local via Ollama"
    )

    mlflow.set_tag(
        "observacao",
        "Dataset final independente do conjunto piloto"
    )

    print("=" * 70)
    print("EXPERIMENTO REGISTRADO NO MLFLOW")
    print("=" * 70)

    print(f"Accuracy:        {accuracy:.4f}")
    print(f"Precision macro: {precision_macro:.4f}")
    print(f"Recall macro:    {recall_macro:.4f}")
    print(f"F1 macro:        {f1_macro:.4f}")
    print(f"F1 weighted:     {f1_weighted:.4f}")

    print(f"\nAcertos: {acertos}/{total}")
    print(f"Erros:   {erros}/{total}")

    print("\nArtefatos registrados:")
    for arquivo in arquivos:
        if arquivo.exists():
            print(f"- {arquivo.name}")

    print("\nExperimento:")
    print("HealthCheck_IA_Avaliacao_Final")

    print("=" * 70)