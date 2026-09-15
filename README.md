# 🩺 HealthCheck IA

## Inteligência Artificial + Evidências + Pensamento Crítico

O **HealthCheck IA** é um sistema de apoio à verificação de alegações relacionadas à saúde.

O projeto utiliza **Inteligência Artificial, recuperação de evidências e RAG (Retrieval-Augmented Generation)** para analisar informações encontradas em pesquisas do Google e apresentar ao usuário:

- classificação da alegação;
- explicação da análise;
- evidências utilizadas;
- fontes originais;
- similaridade semântica das evidências;
- orientações de pensamento crítico.

O objetivo não é criar uma IA que determine simplesmente se uma informação é "verdadeira" ou "falsa", mas fornecer evidências que ajudem o usuário a avaliar criticamente aquilo que está lendo.

> **A IA deve auxiliar o pensamento humano, e não substituí-lo.**

---

# 🎯 Problema

A facilidade de publicação e compartilhamento de conteúdo na internet também favorece a circulação de informações falsas, enganosas, incompletas ou sem comprovação.

Na área da saúde, esse problema pode influenciar decisões relacionadas a:

- medicamentos;
- vacinas;
- doenças;
- tratamentos;
- prevenção;
- automedicação;
- saúde pública.

Sistemas baseados em IA também apresentam um risco adicional: o usuário pode interpretar a resposta produzida pelo modelo como uma autoridade absoluta.

O HealthCheck IA foi desenvolvido considerando esse problema.

Em vez de apresentar apenas:

```text
❌ FAKE
```

o sistema procura apresentar:

```text
🔴 Evidências contraditórias

Por que o sistema classificou assim?
[explicação]

Evidências utilizadas
[trechos recuperados]

Consultar fonte original

💭 Antes de compartilhar
Compare a alegação com as evidências apresentadas.
```

---

# 🌐 MVP — Extensão para Google Chrome

O MVP atual funciona como uma **extensão para Google Chrome** integrada a um backend local desenvolvido em Python.

Quando o usuário realiza uma pesquisa relacionada à saúde no Google, a extensão:

1. identifica os resultados da pesquisa;
2. captura título, descrição e URL;
3. envia a informação para o backend;
4. recupera evidências semanticamente relacionadas;
5. utiliza um LLM para comparar a alegação com as evidências;
6. recebe uma classificação e uma explicação;
7. apresenta o resultado diretamente na página do Google.

Fluxo simplificado:

```text
Pesquisa no Google
        ↓
Extensão Chrome
        ↓
Captura do resultado
        ↓
API FastAPI
        ↓
Busca semântica
        ↓
Recuperação de evidências
        ↓
RAG
        ↓
LLM local
        ↓
Classificação + explicação
        ↓
Evidências + fontes
        ↓
Card exibido no Google
```

---

# 🏷️ Classificações

O HealthCheck IA trabalha com cinco categorias.

### 🟢 Sustentada pelas evidências

As evidências recuperadas são compatíveis com a alegação analisada.

### 🟡 Parcialmente sustentada

Parte da alegação possui suporte nas evidências, mas outra parte não pôde ser confirmada ou apresenta limitações.

### 🟠 Enganosa

A alegação utiliza informações verdadeiras ou plausíveis para sustentar uma conclusão exagerada, distorcida ou inadequada.

### 🔴 Contradita pelas evidências

As evidências recuperadas apresentam informações incompatíveis com a alegação.

### ⚪ Não foi possível verificar

As evidências disponíveis na base não são suficientes para confirmar ou contradizer a alegação com segurança.

> **Ausência de evidência não é tratada como evidência de falsidade.**

---

# 🧠 Pensamento crítico

O HealthCheck IA não apresenta apenas uma classificação.

Cada análise procura oferecer elementos que permitam ao usuário compreender o resultado e verificar as evidências por conta própria.

O card apresentado pela extensão contém:

- classificação;
- mensagem educativa;
- explicação produzida a partir das evidências;
- evidências utilizadas;
- instituição responsável pela fonte;
- título do documento;
- similaridade semântica;
- link para a fonte original;
- orientação antes do compartilhamento;
- aviso de que a análise foi assistida por IA.

A proposta é utilizar IA como **ferramenta de apoio ao raciocínio**, e não como autoridade definitiva.

---

# 📚 Base de conhecimento

A versão atual possui uma base de conhecimento local composta por **18 documentos** organizados em seis temas:

```text
data/
├── cancer/
├── dengue/
├── diabetes/
├── hipertensao/
├── medicamentos/
└── vacinas/
```

As evidências foram organizadas a partir de instituições reconhecidas na área da saúde, incluindo:

- Ministério da Saúde;
- Anvisa;
- Fiocruz;
- INCA;
- Organização Mundial da Saúde (OMS);
- Organização Pan-Americana da Saúde (OPAS).

Os documentos armazenam metadados como:

```text
Título
Fonte
URL
Tema
Subtema
Data de acesso
```

A base não é atualizada em tempo real e deve ser revisada periodicamente.

---

# 🔎 Embeddings e busca semântica

Os documentos são divididos em trechos menores (**chunks**) que podem ser recuperados durante uma análise.

Para representação semântica é utilizado o modelo:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

A busca utiliza similaridade de cosseno combinada com um pequeno componente de sobreposição lexical para ordenar as evidências.

O sistema recupera os trechos mais relacionados à alegação e os envia ao processo de RAG.

> **Importante:** similaridade semântica não representa probabilidade de uma informação ser verdadeira e não deve ser interpretada como confiança da classificação.

---

# 🤖 RAG e modelo de linguagem

O HealthCheck IA utiliza **RAG — Retrieval-Augmented Generation**.

Antes de solicitar uma classificação ao modelo de linguagem, o sistema recupera evidências da base de conhecimento.

Fluxo:

```text
Alegação
   ↓
Embedding
   ↓
Busca semântica
   ↓
Top 5 evidências
   ↓
Prompt + evidências
   ↓
LLM
   ↓
Classificação
   ↓
Explicação
   ↓
Evidências utilizadas
```

O modelo utilizado atualmente é:

```text
qwen2.5:7b
```

executado localmente por meio do **Ollama**.

A configuração utilizada na avaliação final foi:

```text
temperature = 0
seed = 42
top_k de evidências = 5
```

O prompt determina que o modelo deve utilizar somente as evidências fornecidas e evitar completar lacunas utilizando conhecimento externo.

---

# 🛡️ Política de abstenção

Um princípio importante do HealthCheck IA é permitir que o modelo **não produza uma conclusão quando as evidências forem insuficientes**.

Quando a base recuperada não fornece suporte adequado para confirmar ou contradizer uma alegação, o sistema deve utilizar:

```text
⚪ NÃO FOI POSSÍVEL VERIFICAR
```

O modelo é orientado a:

- utilizar somente as evidências fornecidas;
- não inventar fontes;
- não inventar estudos;
- não presumir informações ausentes;
- não transformar ausência de evidência em falsidade;
- evitar conclusões sem suporte;
- não selecionar arbitrariamente uma fonte quando evidências relevantes forem conflitantes.

---

# 🧪 Avaliação científica

O sistema passou por uma etapa específica de avaliação.

Inicialmente foi utilizado um conjunto piloto de desenvolvimento com **25 alegações**, utilizado durante os ajustes do sistema.

Após o congelamento da configuração, foi criado um conjunto de teste separado contendo:

```text
200 alegações
```

distribuídas igualmente entre as cinco classes:

```text
40 — Sustentada pelas evidências
40 — Parcialmente sustentada
40 — Enganosa
40 — Contradita pelas evidências
40 — Não foi possível verificar
```

## Resultados

O HealthCheck IA classificou corretamente:

```text
151 / 200 alegações
```

Resultados gerais:

| Métrica | Resultado |
|---|---:|
| Accuracy | 75,50% |
| Precision macro | 79,72% |
| Recall macro | 75,50% |
| F1-score macro | 72,87% |

### Desempenho por classe

| Classe | Precision | Recall | F1-score |
|---|---:|---:|---:|
| Sustentada | 68,97% | 100,00% | 81,63% |
| Parcialmente sustentada | 92,31% | 30,00% | 45,28% |
| Enganosa | 71,74% | 82,50% | 76,74% |
| Contradita | 92,86% | 65,00% | 76,47% |
| Não foi possível verificar | 72,73% | 100,00% | 84,21% |

Os resultados mostram que as principais dificuldades estão nas categorias semanticamente próximas.

O maior desafio observado foi identificar corretamente alegações **parcialmente sustentadas**, que apresentaram recall de 30%.

Entre os erros mais frequentes estavam:

```text
Parcialmente sustentada → Sustentada
Contradita → Enganosa
Parcialmente sustentada → Não foi possível verificar
```

Esses resultados reforçam que a classificação produzida pelo sistema **não deve ser interpretada como infalível**.

---

# 📊 MLflow

Os experimentos da avaliação foram registrados utilizando **MLflow**.

Experimento:

```text
HealthCheck_IA_Avaliacao_Final
```

Run:

```text
qwen2.5_7b_avaliacao_final_200
```

Foram registrados dados relacionados às métricas e aos artefatos produzidos durante a avaliação.

O armazenamento utilizado atualmente é SQLite:

```text
mlflow.db
```

---

# 🔐 Segurança

O projeto possui regras específicas para reduzir respostas sem suporte nas evidências.

Entre elas:

- política de abstenção;
- proibição de inventar fontes;
- proibição de utilizar evidências apenas por serem do mesmo tema;
- separação entre similaridade semântica e confiança;
- transparência sobre uso de Inteligência Artificial;
- acesso às fontes originais;
- mensagens de pensamento crítico;
- tratamento específico para evidências insuficientes;
- cuidados com alegações relacionadas a decisões médicas.

Durante a validação de segurança foram realizados testes envolvendo:

```text
✓ evidência insuficiente
✓ contradição direta
✓ informação enganosa
✓ alegação parcialmente sustentada
✓ interpretação da similaridade semântica
✓ decisão relacionada a medicamentos
```

Os **6 casos de segurança testados foram aprovados**.

---

# ⚠️ Limitações

O HealthCheck IA possui limitações que devem ser consideradas.

### Base limitada

O sistema analisa apenas as evidências existentes na base de conhecimento.

Uma evidência relevante pode existir fora da base.

### Atualização

A base não é atualizada em tempo real.

Informações e recomendações de saúde podem mudar.

### Recuperação de evidências

Mesmo quando uma informação existe na base, o mecanismo de busca pode não recuperá-la entre os primeiros resultados.

### Modelo de linguagem

O LLM pode interpretar incorretamente alegações ou evidências.

### Erros de classificação

O sistema pode produzir falsos positivos, falsos negativos e confusões entre categorias semanticamente próximas.

### Cobertura temática

A versão atual está concentrada nos temas presentes na base de conhecimento e não funciona como verificador universal de informações de saúde.

### Uso médico

O HealthCheck IA:

```text
NÃO realiza diagnóstico.
NÃO prescreve medicamentos.
NÃO recomenda tratamentos.
NÃO substitui profissionais de saúde.
```

> **O HealthCheck IA deve ser utilizado como ferramenta de apoio ao pensamento crítico e à consulta de evidências, e não como autoridade definitiva sobre a veracidade de informações ou como substituto de orientação profissional.**

---

# 🛠️ Tecnologias utilizadas

### Extensão

- HTML
- CSS
- JavaScript
- Chrome Extensions
- Manifest V3

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### Inteligência Artificial

- Ollama
- Qwen 2.5 7B
- Sentence Transformers
- Embeddings
- RAG

### Dados e avaliação

- Pandas
- NumPy
- Scikit-learn

### Experimentação

- MLflow
- SQLite

### Desenvolvimento

- Git
- GitHub
- VS Code

---

# 📁 Estrutura do projeto

```text
HealthCheck_IA/
│
├── backend/
│   ├── main.py
│   ├── rag.py
│   ├── busca_semantica.py
│   └── carregar_documentos.py
│
├── data/
│   ├── cancer/
│   ├── dengue/
│   ├── diabetes/
│   ├── hipertensao/
│   ├── medicamentos/
│   └── vacinas/
│
├── extension/
│   ├── content.js
│   ├── manifest.json
│   ├── styles.css
│   └── teste-visual.html
│
├── tests/
│   ├── dataset_avaliacao_final.csv
│   ├── dataset_validacao.csv
│   ├── resultados_avaliacao_final.csv
│   ├── matriz_confusao.csv
│   └── calcular_metricas.py
│
├── docs/
│
├── MVP/
│
├── README.md
├── requirements.txt
└── mlflow.db
```

---

# 💻 Instalação

Clone o repositório:

```bash
git clone https://github.com/dida0982/HealthCheck_IA.git
```

Entre na pasta:

```bash
cd HealthCheck_IA
```

Crie um ambiente virtual:

```bash
python -m venv backend/.venv
```

Ative o ambiente no Windows PowerShell:

```powershell
.\backend\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

O projeto também necessita do **Ollama** instalado no computador.

Baixe o modelo utilizado:

```bash
ollama pull qwen2.5:7b
```

Inicie o backend:

```bash
python -m uvicorn backend.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

E a documentação Swagger em:

```text
http://127.0.0.1:8000/docs
```

A instalação da extensão Chrome e o processo completo de execução serão detalhados na documentação do projeto.

---

# 📦 Escopo do MVP

## ✅ Implementado

- extensão Chrome;
- captura dos resultados do Google;
- backend FastAPI;
- comunicação extensão ↔ backend;
- base local de evidências;
- embeddings;
- busca semântica;
- RAG;
- integração com LLM local;
- cinco categorias de classificação;
- explicação da classificação;
- exibição das evidências;
- links para fontes originais;
- mensagens de pensamento crítico;
- política de abstenção;
- testes de segurança;
- dataset de avaliação;
- métricas de desempenho;
- matriz de confusão;
- registro de experimentos com MLflow.

## ❌ Fora do MVP atual

- análise de imagens;
- análise de vídeos;
- análise de áudio;
- WhatsApp;
- Instagram;
- outros idiomas além do português;
- análise universal de qualquer assunto;
- diagnóstico médico;
- prescrição ou recomendação de tratamento.

---

# 📌 Status do projeto

```text
[x] Definição do MVP
[x] Extensão Chrome
[x] Captura dos resultados do Google
[x] Backend FastAPI
[x] Integração Chrome + Python
[x] Base de conhecimento
[x] Embeddings e busca semântica
[x] RAG
[x] Integração com LLM
[x] Sistema de classificação
[x] Avaliação científica
[x] Pensamento crítico
[x] Segurança e limitações
[ ] Documentação final
[ ] Apresentação
```

O projeto encontra-se atualmente na fase de **documentação e preparação da apresentação final**.

---

# 🚀 Trabalhos futuros

Possíveis evoluções incluem:

- ampliação da base de conhecimento;
- inclusão de novos temas de saúde;
- atualização automatizada ou assistida das fontes;
- análise do conteúdo completo das páginas;
- avaliação com conjuntos externos;
- comparação entre diferentes modelos;
- melhoria da classificação de alegações compostas;
- análise multimodal;
- integração com outras plataformas.

---

# 🎓 Propósito

O HealthCheck IA não busca apenas detectar desinformação.

O projeto investiga como Inteligência Artificial, recuperação de evidências e design orientado ao pensamento crítico podem auxiliar pessoas a avaliar informações relacionadas à saúde.

> **Não queremos uma IA que diga às pessoas no que acreditar.**
>
> **Queremos uma IA que apresente evidências para ajudá-las a avaliar aquilo que estão lendo.**

---

# 👤 Autor

**Guilherme Barros**

<img src="https://github.com/dida0982.png" width="150" alt="Foto de perfil">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/guilherme-barros-6a0369209/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dida0982)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/guilherme_barros_jr/)

Projeto **HealthCheck IA**

GitHub: **dida0982**

---

**HealthCheck IA — Inteligência Artificial + Evidências + Pensamento Crítico**