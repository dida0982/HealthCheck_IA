````markdown
# 🩺 HealthCheck IA

## Inteligência Artificial no combate à desinformação em saúde.

O **HealthCheck IA** é um projeto que tem como objetivo desenvolver uma solução baseada em Inteligência Artificial para auxiliar na identificação e verificação de desinformação relacionada à saúde.

A proposta é permitir que usuários tenham acesso a **evidências, fontes confiáveis e informações complementares antes de confiar ou compartilhar determinado conteúdo**, utilizando a Inteligência Artificial como ferramenta de apoio à análise.

> **Objetivo principal:**  
> Desenvolver uma solução baseada em Inteligência Artificial para auxiliar na identificação e verificação de desinformação relacionada à saúde, apresentando evidências e fontes confiáveis sem substituir o pensamento crítico do usuário.

---

## 🎯 Problema

A internet tornou o acesso à informação extremamente rápido. Entretanto, essa facilidade também contribuiu para a disseminação de conteúdos falsos, enganosos ou sem comprovação.

Na área da saúde, esse problema pode ter consequências especialmente graves.

Uma informação incorreta pode influenciar decisões relacionadas a:

- medicamentos;
- vacinas;
- tratamentos;
- doenças;
- alimentação;
- prevenção;
- saúde pública;
- automedicação.

Além disso, existe outro problema: utilizar Inteligência Artificial simplesmente para responder se determinada informação é **"verdadeira" ou "falsa"** pode fazer com que o usuário transfira seu processo de julgamento para a própria IA.

Por isso, o HealthCheck IA busca uma abordagem diferente.

---

## 💡 Nossa proposta

Em vez de simplesmente apresentar:

> ❌ **"Essa informação é falsa."**

o sistema deverá apresentar ao usuário **evidências que permitam compreender por que determinada alegação pode ou não ser sustentada**.

Exemplo:

> 🔴 **Contradita pelas evidências**
>
> **Confiança da análise:** 87%
>
> Foram encontradas evidências que contradizem a alegação apresentada.
>
> **Fontes consultadas:**
> - Ministério da Saúde
> - Fiocruz
> - PubMed
>
> **Ver evidências**

Dessa forma, a IA funciona como uma ferramenta de **apoio ao pensamento crítico**, e não como uma autoridade responsável por decidir o que o usuário deve acreditar.

---

# 🌐 MVP — Extensão para Google Chrome

O primeiro MVP do HealthCheck IA será uma **extensão para Google Chrome**.

A extensão deverá analisar resultados de pesquisas relacionadas à saúde diretamente na página de resultados do Google.

O objetivo é fornecer informações adicionais **antes mesmo de o usuário clicar no resultado**.

### Fluxo esperado

```text
Usuário realiza uma pesquisa no Google
                ↓
A extensão identifica os resultados
                ↓
Captura título, descrição e URL
                ↓
Identifica conteúdos relacionados à saúde
                ↓
Consulta uma base de evidências confiáveis
                ↓
A Inteligência Artificial analisa a alegação
                ↓
Compara a alegação com as evidências encontradas
                ↓
Apresenta classificação, explicação e fontes
````

---

## 🔎 Exemplo de utilização

O usuário pesquisa:

```text
chá de boldo cura diabetes
```

Um resultado aparece normalmente no Google.

O HealthCheck IA poderá adicionar abaixo dele:

```text
🔴 CONTRADITA PELAS EVIDÊNCIAS

Confiança da análise: 91%

As evidências encontradas não sustentam
a alegação apresentada.

3 evidências encontradas.

[Ver evidências]
```

O usuário poderá então consultar as evidências antes de decidir se confia no conteúdo.

---

# 🧠 Pensamento crítico

Um dos princípios fundamentais do projeto é:

> **A IA deve auxiliar o pensamento humano, e não substituí-lo.**

Por isso, o HealthCheck IA não pretende funcionar simplesmente como uma máquina de classificação de **"FAKE" ou "VERDADEIRO"**.

O sistema deverá:

* apresentar evidências;
* mostrar as fontes utilizadas;
* explicar os motivos da classificação;
* indicar o nível de confiança da análise;
* apresentar diferentes perspectivas quando necessário;
* reconhecer quando não existem evidências suficientes;
* permitir que o usuário consulte as fontes;
* estimular a análise crítica da informação.

---

# 🏷️ Classificação das informações

Inicialmente, o sistema poderá utilizar cinco categorias:

### 🟢 Sustentada pelas evidências

As evidências encontradas sustentam a alegação apresentada.

### 🟡 Parcialmente sustentada

Existem evidências favoráveis, mas a afirmação apresenta limitações, generalizações ou informações incompletas.

### 🟠 Enganosa

A informação utiliza elementos verdadeiros, mas os apresenta de maneira que pode levar a uma interpretação incorreta.

### 🔴 Contradita pelas evidências

As evidências encontradas contradizem a alegação apresentada.

### ⚪ Não foi possível verificar

Não existem evidências suficientes para que o sistema produza uma conclusão confiável.

---

# 📊 Confiança da análise

Além da classificação, o sistema poderá apresentar um indicador como:

```text
Confiança da análise: 87%
```

É importante destacar que esse valor **não representa "87% de chance de a notícia ser verdadeira"**.

Ele representa o nível de confiança do sistema na classificação realizada a partir das evidências disponíveis.

---

# 📚 Fontes de evidências

O projeto deverá priorizar informações provenientes de instituições reconhecidas e fontes científicas.

Entre as fontes que poderão compor a base de conhecimento estão:

* Ministério da Saúde;
* Anvisa;
* Fiocruz;
* SUS;
* Biblioteca Virtual em Saúde (BVS);
* PubMed;
* universidades públicas;
* sociedades médicas;
* artigos científicos;
* outras instituições reconhecidas na área da saúde.

A seleção, avaliação e hierarquia dessas fontes também fazem parte da pesquisa do projeto.

---

# 🤖 Arquitetura proposta

A arquitetura inicial poderá seguir o seguinte fluxo:

```text
┌──────────────────────────┐
│      Google Chrome       │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│     Chrome Extension     │
│       JavaScript         │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│        Backend API       │
│    Python + FastAPI      │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│   Busca de Evidências    │
│   Embeddings + RAG       │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│            LLM           │
│   Análise da alegação    │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│ Classificação + Evidência│
│   Explicação + Fontes    │
└──────────────────────────┘
```

---

# 🛠️ Tecnologias previstas

O projeto poderá utilizar ferramentas gratuitas e open source, como:

### Front-end / Extensão

* HTML
* CSS
* JavaScript
* Chrome Extensions API
* Manifest V3

### Backend

* Python
* FastAPI
* Pydantic

### Inteligência Artificial

* NLP
* LLM
* Ollama
* Sentence Transformers
* Embeddings
* RAG

### Dados

* Pandas
* Scikit-learn
* FAISS
* SQLite

### Experimentação

* MLflow
* Jupyter Notebook

### Desenvolvimento

* Git
* GitHub
* VS Code

---

# 📦 Escopo do MVP 1.0

Para manter o projeto tecnicamente viável, a primeira versão terá um escopo limitado.

## ✅ Faz parte do MVP

* pesquisas realizadas no Google;
* análise dos resultados da pesquisa;
* captura de título, descrição e URL;
* conteúdo textual;
* idioma português;
* informações relacionadas à saúde;
* recuperação de evidências;
* classificação da alegação;
* apresentação das fontes;
* explicação do resultado.

## ❌ Não faz parte inicialmente

* análise de imagens;
* análise de vídeos;
* análise de áudio;
* WhatsApp;
* Instagram;
* política;
* esportes;
* outros idiomas;
* análise universal de qualquer conteúdo da internet.

Essas funcionalidades poderão ser estudadas posteriormente.

---

# 🧪 Avaliação

O sistema deverá ser avaliado utilizando exemplos previamente verificados.

Entre as métricas que poderão ser utilizadas estão:

* Accuracy;
* Precision;
* Recall;
* F1-score;
* Matriz de Confusão.

Também poderão ser realizados experimentos para comparar diferentes modelos, estratégias de recuperação de evidências e prompts.

---

# ⚠️ Limitações

O HealthCheck IA **não substitui profissionais de saúde, instituições oficiais ou avaliação científica especializada**.

A Inteligência Artificial também pode cometer erros.

Por esse motivo, o projeto prioriza:

* transparência;
* explicabilidade;
* apresentação das fontes;
* rastreabilidade das evidências;
* indicação de incerteza;
* possibilidade de abstenção da IA.

Quando não houver evidências suficientes, o sistema deverá preferir:

> ⚪ **Não foi possível verificar**

em vez de produzir uma conclusão sem sustentação.

---

# 🚀 Visão futura

Após a validação do MVP, poderão ser estudadas funcionalidades como:

* análise do conteúdo completo das páginas;
* análise de imagens;
* análise de vídeos;
* reconhecimento de conteúdo multimodal;
* integração com outras plataformas;
* atualização automática da base científica;
* personalização das explicações;
* ferramentas educacionais de alfabetização midiática.

---

# 🎓 Propósito do projeto

O HealthCheck IA não busca apenas detectar desinformação.

A proposta é investigar como a Inteligência Artificial pode contribuir para uma sociedade mais preparada para **questionar, verificar e interpretar informações**.

> **Não queremos uma IA que diga às pessoas no que acreditar.**
>
> **Queremos uma IA que forneça evidências para ajudá-las a decidir no que acreditar.**

---

## 📌 Status

🚧 **Projeto em desenvolvimento — MVP 1.0**

### Roadmap inicial

* [x] Definição da ideia
* [x] Definição do MVP
* [ ] Desenvolvimento da extensão Chrome
* [ ] Captura dos resultados do Google
* [ ] Desenvolvimento da API
* [ ] Construção da base de evidências
* [ ] Implementação da busca semântica
* [ ] Implementação do RAG
* [ ] Integração com LLM
* [ ] Sistema de classificação
* [ ] Exibição das evidências
* [ ] Testes e avaliação
* [ ] Documentação final
* [ ] Demonstração do MVP

---

## HealthCheck IA

**Inteligência Artificial + Evidências + Pensamento Crítico**

> Tecnologia para ajudar pessoas a verificar informações de saúde antes de confiar ou compartilhar.

---

## 👤 Autor

**Guilherme Barros**

<img src="https://github.com/dida0982.png" width="150" alt="Foto de perfil">

Desenvolvedor Front-end | Brasília, DF - Brasil

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/guilherme-barros-6a0369209/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/dida0982)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/guilherme_barros_jr/)

----