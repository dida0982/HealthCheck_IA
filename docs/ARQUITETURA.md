# 🏗️ Arquitetura do HealthCheck IA

## 1. Visão geral

O **HealthCheck IA** utiliza uma arquitetura composta por uma extensão para Google Chrome, uma API local desenvolvida com FastAPI, um mecanismo de recuperação de evidências, um pipeline RAG e um modelo de linguagem executado localmente.

O objetivo da arquitetura é permitir que uma alegação relacionada à saúde seja analisada utilizando evidências previamente armazenadas em uma base de conhecimento.

Fluxo geral:

```text
┌──────────────────────────────┐
│          Usuário             │
│     Pesquisa no Google       │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│      Extensão Chrome         │
│   HTML + CSS + JavaScript    │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│        API FastAPI           │
│         main.py              │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│     Busca de evidências      │
│    busca_semantica.py        │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│     Base de conhecimento     │
│      documentos + chunks     │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│             RAG              │
│           rag.py             │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│          Ollama              │
│        qwen2.5:7b            │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Classificação + explicação   │
│    + evidências utilizadas   │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│      Extensão Chrome         │
│     Card exibido ao usuário  │
└──────────────────────────────┘
```

---

# 2. Componentes da arquitetura

## 2.1 Extensão Chrome

A interface do HealthCheck IA é implementada como uma extensão para Google Chrome.

Os principais arquivos estão em:

```text
extension/
├── content.js
├── manifest.json
├── styles.css
└── teste-visual.html
```

### `manifest.json`

Define a configuração da extensão, permissões e scripts utilizados pelo navegador.

### `content.js`

É responsável pela integração do HealthCheck IA com a página de resultados do Google.

Entre suas responsabilidades estão:

- detectar resultados da pesquisa;
- capturar título, descrição e URL;
- enviar os dados ao backend;
- receber a resposta da API;
- construir o card do HealthCheck IA;
- exibir classificação;
- apresentar explicação;
- apresentar evidências;
- permitir acesso às fontes originais;
- apresentar mensagens de pensamento crítico e transparência sobre IA.

### `styles.css`

Responsável pela apresentação visual dos componentes inseridos pela extensão.

### `teste-visual.html`

Página local utilizada para validar visualmente os cinco estados de classificação sem executar o modelo de linguagem.

Isso permite testar a interface sem realizar chamadas ao backend ou ao Ollama.

---

# 3. Backend

O backend está localizado em:

```text
backend/
```

Os principais componentes são:

```text
backend/
├── main.py
├── rag.py
├── busca_semantica.py
└── carregar_documentos.py
```

O backend é desenvolvido em **Python** utilizando **FastAPI**.

---

# 4. API — `main.py`

O arquivo:

```text
backend/main.py
```

funciona como ponto central da API.

A principal operação disponibilizada pelo backend é:

```text
POST /analisar
```

A extensão envia uma alegação para esse endpoint.

De forma simplificada, a requisição contém informações como:

```json
{
  "titulo": "Título da informação",
  "descricao": "Alegação que será analisada"
}
```

O backend então executa o pipeline de análise.

Fluxo:

```text
Receber alegação
       ↓
Buscar evidências
       ↓
Montar contexto RAG
       ↓
Enviar contexto ao LLM
       ↓
Interpretar resposta
       ↓
Selecionar evidências utilizadas
       ↓
Retornar JSON para a extensão
```

A resposta contém informações como:

```text
classificação
explicação
evidências utilizadas
evidências recuperadas
metadados das fontes
```

---

# 5. Base de conhecimento

A base está localizada em:

```text
data/
```

e atualmente está organizada em seis temas:

```text
data/
├── cancer/
├── dengue/
├── diabetes/
├── hipertensao/
├── medicamentos/
└── vacinas/
```

A versão atual possui **18 documentos**.

Cada documento possui metadados como:

```text
Título
Fonte
URL
Tema
Subtema
Data de acesso
```

Os documentos são baseados em fontes institucionais relacionadas à saúde.

---

# 6. Carregamento dos documentos

O arquivo:

```text
backend/carregar_documentos.py
```

é responsável pelo processamento inicial da base.

Durante o carregamento são recuperados:

- conteúdo do documento;
- título;
- instituição responsável;
- URL original;
- tema;
- subtema;
- data de acesso.

Os documentos são divididos em unidades menores chamadas **chunks**.

Esses chunks são utilizados posteriormente pela busca semântica.

A versão atual da base gera **73 chunks** após a remoção das seções auxiliares utilizadas na organização dos documentos.

---

# 7. Embeddings

Para permitir a comparação semântica entre uma alegação e os documentos, o sistema utiliza embeddings.

Modelo:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Cada chunk é transformado em uma representação vetorial.

A alegação analisada também é transformada em embedding.

Isso permite comparar matematicamente a proximidade semântica entre:

```text
embedding da alegação
        ↕
embedding dos chunks
```

---

# 8. Busca semântica

A lógica de recuperação está localizada em:

```text
backend/busca_semantica.py
```

A busca utiliza similaridade de cosseno para comparar a alegação com os chunks.

Além da similaridade semântica, a ordenação atual utiliza um pequeno componente de sobreposição lexical.

Fluxo:

```text
Alegação
   ↓
Embedding da alegação
   ↓
Comparação com embeddings dos chunks
   ↓
Similaridade de cosseno
   ↓
Componente lexical
   ↓
Ordenação
   ↓
Top 5 evidências
```

O valor apresentado como similaridade corresponde à **similaridade de cosseno**.

> Similaridade semântica representa proximidade entre conteúdos. Ela não representa probabilidade de verdade nem nível de confiança da classificação.

---

# 9. RAG

O HealthCheck IA utiliza:

```text
Retrieval-Augmented Generation
```

ou:

```text
RAG
```

A implementação relacionada à construção dos prompts está concentrada em:

```text
backend/rag.py
```

O RAG conecta dois componentes:

```text
Recuperação de evidências
           +
Modelo de linguagem
```

Em vez de solicitar ao modelo uma resposta baseada apenas no conhecimento aprendido durante seu treinamento, o HealthCheck IA fornece explicitamente as evidências recuperadas da base.

Fluxo:

```text
Alegação
   ↓
Busca semântica
   ↓
5 evidências recuperadas
   ↓
Construção do prompt
   ↓
LLM
   ↓
Classificação fundamentada nas evidências
```

---

# 10. Modelo de linguagem

O modelo utilizado atualmente é:

```text
qwen2.5:7b
```

executado localmente utilizando:

```text
Ollama
```

Configuração utilizada na avaliação final:

```text
model = qwen2.5:7b
temperature = 0
seed = 42
top_k de evidências = 5
```

A execução local permite que o backend se comunique diretamente com o servidor do Ollama instalado na máquina.

---

# 11. Prompt e controle da resposta

O prompt utilizado pelo HealthCheck IA contém regras destinadas a restringir a análise às evidências recuperadas.

Entre as principais regras estão:

- utilizar somente as evidências fornecidas;
- não utilizar conhecimento externo para completar lacunas;
- não inventar fatos;
- não inventar fontes;
- não inventar estudos;
- não presumir informações ausentes;
- diferenciar ausência de evidência de evidência de ausência;
- utilizar abstenção quando não houver suporte suficiente;
- fundamentar a explicação nas evidências recuperadas.

Essas regras reduzem o risco de respostas sem suporte, embora não garantam matematicamente que um modelo de linguagem nunca cometerá erros.

---

# 12. Sistema de classificação

O modelo pode produzir cinco classificações:

```text
SUSTENTADA PELAS EVIDÊNCIAS
PARCIALMENTE SUSTENTADA
ENGANOSA
CONTRADITA PELAS EVIDÊNCIAS
NÃO FOI POSSÍVEL VERIFICAR
```

Essas categorias representam a relação entre a alegação analisada e as evidências recuperadas.

Elas não devem ser interpretadas como uma determinação absoluta da verdade.

---

# 13. Política de abstenção

Quando as evidências recuperadas não permitem uma conclusão segura, o sistema deve utilizar:

```text
NÃO FOI POSSÍVEL VERIFICAR
```

Princípio:

```text
Ausência de evidência ≠ evidência de falsidade
```

Quando o sistema se abstém por falta de evidência suficiente, ele não deve selecionar evidências apenas por possuírem o mesmo tema da alegação.

---

# 14. Resposta da API

Após o processamento pelo LLM, o backend interpreta a resposta e associa os índices indicados pelo modelo às evidências recuperadas.

A extensão recebe informações que permitem apresentar:

```text
classificação
explicação
evidências utilizadas
fonte
título
URL
tema
subtema
data de acesso
similaridade semântica
```

---

# 15. Interface apresentada ao usuário

A extensão transforma a resposta técnica da API em um card voltado ao usuário.

A interface procura seguir esta organização:

```text
STATUS DA CLASSIFICAÇÃO

Mensagem educativa

🔍 POR QUE O SISTEMA CLASSIFICOU ASSIM?

Explicação

📚 EVIDÊNCIAS UTILIZADAS

Evidência 1
Fonte
Título
Similaridade semântica
Trecho
Consultar fonte original

...

💭 ANTES DE COMPARTILHAR

Orientação de pensamento crítico

🤖 ANÁLISE ASSISTIDA POR IA

Aviso de transparência
```

A interface evita apresentar o modelo como autoridade absoluta.

---

# 16. Comunicação entre os componentes

A arquitetura pode ser resumida em quatro camadas principais:

```text
CAMADA 1 — INTERFACE
Chrome Extension
        ↓
CAMADA 2 — API
FastAPI
        ↓
CAMADA 3 — RECUPERAÇÃO
Documentos + chunks + embeddings + busca semântica
        ↓
CAMADA 4 — GERAÇÃO
RAG + Ollama + Qwen 2.5 7B
```

A resposta percorre o caminho inverso:

```text
Qwen
 ↓
FastAPI
 ↓
JSON
 ↓
Chrome Extension
 ↓
Card
 ↓
Usuário
```

---

# 17. Princípios arquiteturais

A arquitetura do HealthCheck IA foi construída considerando os seguintes princípios:

### Evidência antes da geração

O modelo recebe evidências recuperadas antes de produzir sua análise.

### Rastreabilidade

As evidências possuem metadados e links para as fontes originais.

### Transparência

O usuário é informado de que a análise utiliza Inteligência Artificial.

### Abstenção

O sistema pode reconhecer quando não possui evidências suficientes.

### Pensamento crítico

A interface incentiva o usuário a consultar as fontes antes de compartilhar uma informação.

### Separação de responsabilidades

A extensão cuida da interação com o navegador.

O FastAPI coordena o processamento.

A busca semântica recupera as evidências.

O RAG organiza o contexto.

O LLM realiza a análise textual baseada nas evidências.

---

# 18. Arquitetura atual

A implementação atual pode ser representada de forma resumida como:

```text
Google
  │
  ▼
Chrome Extension
  │
  │ HTTP
  ▼
FastAPI
  │
  ├──────────────► Base de conhecimento
  │                     │
  │                     ▼
  │              Chunks + Embeddings
  │                     │
  │                     ▼
  │              Busca semântica
  │                     │
  ◄─────────────────────┘
  │
  ▼
RAG
  │
  ▼
Ollama
  │
  ▼
Qwen 2.5 7B
  │
  ▼
Resposta estruturada
  │
  ▼
FastAPI
  │
  ▼
Chrome Extension
  │
  ▼
Card HealthCheck IA
  │
  ▼
Usuário
```

---

## HealthCheck IA

**Inteligência Artificial + Evidências + Pensamento Crítico**

A arquitetura foi projetada para manter as evidências no centro do processo de análise, utilizando o modelo de linguagem como componente de interpretação e não como fonte única de conhecimento.