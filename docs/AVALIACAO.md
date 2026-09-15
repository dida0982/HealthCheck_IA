# 📊 Avaliação Científica — HealthCheck IA

## 1. Objetivo da avaliação

O HealthCheck IA foi submetido a uma avaliação quantitativa para medir sua capacidade de classificar alegações de saúde nas cinco categorias utilizadas pelo sistema.

As métricas utilizadas foram:

- Accuracy;
- Precision;
- Recall;
- F1-score;
- Matriz de confusão;
- Análise de erros por categoria.

O objetivo não foi apenas medir quantos casos o sistema acertou, mas identificar em quais categorias ele apresenta maior dificuldade.

---

# 2. Classes avaliadas

O sistema trabalha com cinco classes:

```text
SUSTENTADA PELAS EVIDÊNCIAS
PARCIALMENTE SUSTENTADA
ENGANOSA
CONTRADITA PELAS EVIDÊNCIAS
NÃO FOI POSSÍVEL VERIFICAR
```

Cada classificação representa a relação entre a alegação e as evidências recuperadas pelo sistema.

---

# 3. Conjunto piloto

Antes da avaliação final foi utilizado um conjunto piloto contendo:

```text
25 alegações
```

O conjunto foi balanceado:

```text
5 — Sustentadas
5 — Parcialmente sustentadas
5 — Enganosas
5 — Contraditas
5 — Não foi possível verificar
```

Esse conjunto foi utilizado durante o desenvolvimento e ajuste do sistema.

O resultado obtido na configuração congelada foi:

```text
22 / 25
88%
```

Como esse conjunto participou do processo de desenvolvimento, ele não foi utilizado como resultado científico final do projeto.

---

# 4. Congelamento da configuração

Antes da execução da avaliação final, foi definida a configuração utilizada pelo sistema.

```text
Modelo: qwen2.5:7b
Execução: Ollama
Temperature: 0
Seed: 42
Evidências recuperadas: Top 5
```

Após essa definição, o conjunto final não deveria ser utilizado para continuar ajustando o prompt e posteriormente reportar os resultados no mesmo conjunto como se fossem uma nova avaliação independente.

---

# 5. Dataset de avaliação final

O conjunto final está localizado em:

```text
tests/dataset_avaliacao_final.csv
```

Ele contém:

```text
200 alegações
```

distribuídas igualmente entre as cinco classes.

| Classe | Quantidade |
|---|---:|
| Sustentada pelas evidências | 40 |
| Parcialmente sustentada | 40 |
| Enganosa | 40 |
| Contradita pelas evidências | 40 |
| Não foi possível verificar | 40 |
| **Total** | **200** |

O conjunto final é separado do conjunto piloto/de desenvolvimento.

Isso permite avaliar a configuração congelada em alegações diferentes das utilizadas durante os ajustes iniciais.

---

# 6. Execução automatizada

A execução da avaliação final é realizada por:

```text
tests/executar_avaliacao_final.py
```

O script envia as alegações para o sistema e registra:

```text
classe esperada
classe produzida
resultado da comparação
```

Os resultados são armazenados em:

```text
tests/resultados_avaliacao_final.csv
```

---

# 7. Resultado geral

Das 200 alegações avaliadas:

```text
151 foram classificadas corretamente
49 foram classificadas incorretamente
```

Portanto:

```text
Accuracy = 151 / 200
Accuracy = 0,755
Accuracy = 75,50%
```

Resultado:

> **O HealthCheck IA atingiu 75,50% de acurácia no conjunto final de 200 alegações.**

---

# 8. Métricas gerais

As métricas finais foram:

| Métrica | Resultado |
|---|---:|
| Accuracy | 75,50% |
| Precision macro | 79,72% |
| Recall macro | 75,50% |
| F1-score macro | 72,87% |
| F1-score weighted | 72,87% |

O F1-score macro é particularmente relevante porque calcula o desempenho de cada classe e depois realiza a média entre elas.

Como o conjunto possui 40 exemplos por classe, todas possuem o mesmo peso no cálculo macro.

---

# 9. Resultados por classe

| Classe | Precision | Recall | F1-score | Casos |
|---|---:|---:|---:|---:|
| Sustentada pelas evidências | 68,97% | 100,00% | 81,63% | 40 |
| Parcialmente sustentada | 92,31% | 30,00% | 45,28% | 40 |
| Enganosa | 71,74% | 82,50% | 76,74% | 40 |
| Contradita pelas evidências | 92,86% | 65,00% | 76,47% | 40 |
| Não foi possível verificar | 72,73% | 100,00% | 84,21% | 40 |

Os resultados mostram diferenças importantes entre as categorias.

---

# 10. Matriz de confusão

A matriz de confusão está armazenada em:

```text
tests/matriz_confusao.csv
```

Linhas representam a classificação esperada.

Colunas representam a classificação produzida.

| Esperado ↓ / Produzido → | Sustentada | Parcial | Enganosa | Contradita | Não verificável |
|---|---:|---:|---:|---:|---:|
| Sustentada | 40 | 0 | 0 | 0 | 0 |
| Parcial | 16 | 12 | 1 | 1 | 10 |
| Enganosa | 0 | 1 | 33 | 1 | 5 |
| Contradita | 2 | 0 | 12 | 26 | 0 |
| Não verificável | 0 | 0 | 0 | 0 | 40 |

A diagonal principal representa os acertos.

---

# 11. Sustentada pelas evidências

Resultado:

```text
Precision = 68,97%
Recall = 100%
F1 = 81,63%
```

Todas as 40 alegações esperadas como sustentadas foram identificadas corretamente.

```text
40 / 40
```

Entretanto, a precision é menor porque alegações de outras categorias também foram classificadas como sustentadas.

O principal caso foi:

```text
PARCIALMENTE SUSTENTADA
        ↓
SUSTENTADA
16 casos
```

---

# 12. Parcialmente sustentada

Resultado:

```text
Precision = 92,31%
Recall = 30%
F1 = 45,28%
```

Essa foi a categoria de maior dificuldade.

Das 40 alegações parcialmente sustentadas, apenas:

```text
12 / 40
```

foram corretamente classificadas.

Os principais erros foram:

```text
16 → Sustentada
10 → Não foi possível verificar
1  → Enganosa
1  → Contradita
```

Isso indica dificuldade do sistema em decompor alegações compostas nas quais uma parte possui suporte e outra não.

---

# 13. Enganosa

Resultado:

```text
Precision = 71,74%
Recall = 82,50%
F1 = 76,74%
```

Das 40 alegações enganosas:

```text
33 / 40
```

foram identificadas corretamente.

Os demais casos foram classificados como:

```text
1 → Parcialmente sustentada
1 → Contradita
5 → Não foi possível verificar
```

---

# 14. Contradita pelas evidências

Resultado:

```text
Precision = 92,86%
Recall = 65%
F1 = 76,47%
```

Das 40 alegações contraditas:

```text
26 / 40
```

foram identificadas corretamente.

O principal erro foi:

```text
CONTRADITA
    ↓
ENGANOSA
12 casos
```

Isso mostra que o sistema possui dificuldade em alguns casos para distinguir uma alegação diretamente incompatível com as evidências de uma alegação que utiliza informação de forma distorcida.

---

# 15. Não foi possível verificar

Resultado:

```text
Precision = 72,73%
Recall = 100%
F1 = 84,21%
```

Todas as 40 alegações esperadas nessa categoria foram identificadas corretamente:

```text
40 / 40
```

A precision é menor porque algumas alegações pertencentes a outras classes também foram classificadas como não verificáveis.

---

# 16. Taxa de erro por classe esperada

A análise por classe mostra:

| Classe esperada | Erros | Total | Taxa de erro |
|---|---:|---:|---:|
| Sustentada | 0 | 40 | 0% |
| Parcialmente sustentada | 28 | 40 | 70% |
| Enganosa | 7 | 40 | 17,5% |
| Contradita | 14 | 40 | 35% |
| Não foi possível verificar | 0 | 40 | 0% |

A categoria parcialmente sustentada concentra a maior dificuldade.

---

# 17. Principais padrões de erro

Os três erros mais frequentes foram:

```text
PARCIAL → SUSTENTADA
16 casos

CONTRADITA → ENGANOSA
12 casos

PARCIAL → NÃO FOI POSSÍVEL VERIFICAR
10 casos
```

Somados:

```text
16 + 12 + 10 = 38 erros
```

Como ocorreram 49 erros no total:

```text
38 / 49 ≈ 77,6%
```

Portanto, aproximadamente:

> **77,6% dos erros observados estão concentrados nesses três padrões de confusão.**

---

# 18. Interpretação dos erros

Os resultados indicam dois desafios principais.

## Alegações compostas

A categoria parcialmente sustentada exige identificar que diferentes partes de uma mesma alegação possuem níveis diferentes de suporte.

Exemplo conceitual:

```text
Parte A → possui evidência
+
Parte B → não possui evidência
```

O sistema precisa considerar as duas partes antes de classificar a afirmação completa.

Esse comportamento mostrou-se difícil para o modelo.

## Contradição x informação enganosa

Outra dificuldade está na separação entre:

```text
CONTRADITA
```

e:

```text
ENGANOSA
```

Em alguns casos, o modelo interpreta uma afirmação incompatível com as evidências como uma distorção ou exagero, em vez de classificá-la como contradição direta.

---

# 19. Precision

Precision responde aproximadamente à pergunta:

> Entre os casos que o sistema classificou em determinada categoria, quantos realmente pertenciam àquela categoria no conjunto de avaliação?

A média macro obtida foi:

```text
79,72%
```

---

# 20. Recall

Recall responde aproximadamente à pergunta:

> Entre todos os casos que pertenciam a determinada categoria no conjunto de avaliação, quantos o sistema conseguiu identificar?

A média macro foi:

```text
75,50%
```

O menor recall ocorreu em:

```text
PARCIALMENTE SUSTENTADA
30%
```

Esse resultado é uma limitação importante do sistema atual.

---

# 21. F1-score

O F1-score combina precision e recall por meio da média harmônica.

De forma simplificada:

```text
F1 = 2 × (Precision × Recall)
         ────────────────────
          Precision + Recall
```

O resultado macro foi:

```text
72,87%
```

Isso resume o equilíbrio médio entre precision e recall nas cinco categorias.

---

# 22. Accuracy

Accuracy representa a proporção total de classificações corretas:

```text
Accuracy =
classificações corretas
────────────────────────
total de classificações
```

No HealthCheck IA:

```text
151
─── = 0,755
200
```

Portanto:

```text
75,50%
```

---

# 23. MLflow

Os resultados da avaliação final também foram registrados utilizando:

```text
MLflow
```

Experimento:

```text
HealthCheck_IA_Avaliacao_Final
```

Run:

```text
qwen2.5_7b_avaliacao_final_200
```

O armazenamento oficial atual utiliza:

```text
mlflow.db
```

SQLite permite manter os dados do experimento registrados localmente.

---

# 24. Reprodução das métricas

O cálculo das métricas é realizado por:

```text
tests/calcular_metricas.py
```

Entre os artefatos relacionados à avaliação estão:

```text
tests/
├── dataset_validacao.csv
├── resultados_validacao.csv
├── dataset_avaliacao_final.csv
├── resultados_avaliacao_final.csv
├── calcular_metricas.py
├── matriz_confusao.csv
├── analisar_erros.py
├── erros_avaliacao_final.csv
├── resumo_erros.csv
└── registrar_mlflow.py
```

---

# 25. Limitações da avaliação

Os resultados devem ser interpretados considerando as características do experimento.

### Dataset balanceado

O conjunto possui exatamente 40 exemplos por categoria.

Essa distribuição não representa necessariamente a frequência das categorias encontradas no uso real.

### Dataset construído dentro do projeto

O conjunto final foi separado do conjunto piloto/de desenvolvimento, mas foi elaborado no contexto do próprio projeto.

Portanto, os resultados não devem ser apresentados como uma validação externa independente.

### Base de conhecimento limitada

O desempenho depende dos documentos disponíveis na base.

### Retrieval

O modelo só pode interpretar adequadamente as evidências que chegam ao contexto.

Um erro de recuperação pode influenciar a classificação final.

### LLM

Mesmo quando as evidências corretas são recuperadas, o modelo pode interpretar incorretamente relações de negação, causalidade, intensidade, condição ou composição.

---

# 26. Uso correto dos resultados

Uma forma adequada de apresentar os resultados é:

> **O HealthCheck IA foi avaliado em um conjunto de teste separado do conjunto piloto/de desenvolvimento, contendo 200 alegações balanceadas entre cinco classes. O sistema classificou corretamente 151 casos, alcançando 75,5% de acurácia e F1-score macro de 72,87%.**

Não é adequado concluir apenas com essas métricas que o sistema possui 75,5% de probabilidade de estar correto em qualquer situação real.

As métricas descrevem o desempenho observado no conjunto avaliado.

---

# 27. Próximos experimentos

Trabalhos futuros podem incluir:

```text
avaliação com datasets externos;
avaliação por especialistas;
ampliação do número de alegações;
datasets com distribuição próxima do uso real;
comparação entre diferentes LLMs;
comparação entre estratégias de retrieval;
avaliação separada do retrieval;
avaliação de diferentes valores de top_k;
análise específica de alegações compostas.
```

Uma nova configuração ajustada a partir dos erros do conjunto final deverá ser avaliada em um novo conjunto de teste para evitar reutilizar o mesmo conjunto como desenvolvimento e avaliação final.

---

# 28. Resultado final

Resumo da avaliação:

```text
Dataset final: 200 alegações

Acertos: 151
Erros: 49

Accuracy: 75,50%
Precision macro: 79,72%
Recall macro: 75,50%
F1-score macro: 72,87%

Maior dificuldade:
PARCIALMENTE SUSTENTADA

Recall da classe:
30%

Principais confusões:
PARCIAL → SUSTENTADA
CONTRADITA → ENGANOSA
PARCIAL → NÃO FOI POSSÍVEL VERIFICAR
```

---

## HealthCheck IA

**Inteligência Artificial + Evidências + Pensamento Crítico**

A avaliação demonstra que o sistema possui capacidade relevante de classificação no conjunto testado, mas também evidencia limitações importantes que devem ser comunicadas de forma transparente.