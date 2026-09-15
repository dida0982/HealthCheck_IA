# 📚 Base de Conhecimento — HealthCheck IA

## 1. Objetivo

A base de conhecimento do **HealthCheck IA** contém os documentos utilizados como fonte de evidências pelo sistema RAG.

O objetivo é permitir que as classificações sejam fundamentadas em conteúdos previamente selecionados e rastreáveis, em vez de depender exclusivamente do conhecimento interno do modelo de linguagem.

Na versão atual, a base contém:

```text
18 documentos
6 temas de saúde
73 chunks após processamento
```

---

# 2. Estrutura

Os documentos estão armazenados em:

```text
data/
```

e organizados por tema:

```text
data/
├── cancer/
├── dengue/
├── diabetes/
├── hipertensao/
├── medicamentos/
└── vacinas/
```

Cada diretório contém três documentos.

Total:

```text
6 temas × 3 documentos = 18 documentos
```

---

# 3. Temas cobertos

A versão atual cobre:

### Câncer

Informações relacionadas à prevenção, fatores de risco e características gerais do câncer.

### Dengue

Informações relacionadas à doença, transmissão, prevenção, sintomas e aspectos relevantes para saúde pública.

### Diabetes

Informações relacionadas ao diabetes, prevenção, fatores de risco e cuidados gerais.

### Hipertensão

Informações relacionadas à hipertensão arterial, fatores de risco, prevenção e controle.

### Medicamentos

Informações relacionadas ao uso de medicamentos e princípios gerais de segurança.

### Vacinas

Informações relacionadas à vacinação, segurança, prevenção e imunização.

A presença desses temas não significa que o sistema possua cobertura completa de todas as alegações possíveis dentro dessas áreas.

---

# 4. Instituições utilizadas

A base atual utiliza documentos associados a instituições reconhecidas na área da saúde:

```text
Ministério da Saúde
Anvisa
Fiocruz
INCA
Organização Mundial da Saúde — OMS
Organização Pan-Americana da Saúde — OPAS
```

A utilização dessas instituições busca aumentar a rastreabilidade das evidências e priorizar fontes institucionais.

Isso não significa que outras fontes científicas ou institucionais não possam ser incorporadas em versões futuras.

---

# 5. Documentos

A estrutura atual possui os seguintes arquivos:

## Câncer

```text
inca_cancer.md
oms_cancer.md
opas_cancer.md
```

## Dengue

```text
ministerio_saude_dengue.md
fiocruz_dengue.md
oms_dengue.md
```

## Diabetes

```text
ministerio_saude_diabetes.md
oms_diabetes.md
opas_diabetes.md
```

## Hipertensão

```text
ministerio_saude_hipertensao.md
oms_hipertensao.md
opas_hipertensao.md
```

## Medicamentos

```text
ministerio_saude_medicamentos.md
oms_medicamentos.md
opas_medicamentos.md
```

## Vacinas

```text
ministerio_saude_gripe.md
anvisa_vacinas.md
fiocruz_vacinas.md
```

Total:

```text
18 documentos
```

---

# 6. Metadados

Cada documento possui metadados para permitir rastreabilidade.

Estrutura utilizada:

```text
# Título do documento

Fonte: instituição responsável
URL: endereço da fonte original
Tema: tema principal
Subtema: assunto específico
Data de acesso: data em que a fonte foi consultada

## Resumo

Conteúdo utilizado como evidência
```

Os principais campos são:

### Título

Identifica o documento.

### Fonte

Identifica a instituição associada ao conteúdo.

### URL

Permite consultar a fonte original.

### Tema

Indica a categoria principal do documento.

### Subtema

Permite uma descrição mais específica do conteúdo.

### Data de acesso

Registra quando a fonte foi consultada durante a construção ou revisão da base.

> A data de acesso não deve ser interpretada automaticamente como data de publicação ou de atualização do conteúdo original.

---

# 7. Fontes originais

## Câncer

### INCA

```text
https://www.inca.gov.br/tipos-de-cancer
```

### Organização Mundial da Saúde

```text
https://www.who.int/news-room/fact-sheets/detail/cancer
```

### Organização Pan-Americana da Saúde

```text
https://www.paho.org/pt/topics/cancer
```

---

## Dengue

### Ministério da Saúde

```text
https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/d/dengue
```

### Fiocruz

```text
https://portal.fiocruz.br/dengue
```

### Organização Mundial da Saúde

```text
https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue
```

---

## Diabetes

### Ministério da Saúde / Conitec

```text
https://www.gov.br/conitec/pt-br
```

### Organização Mundial da Saúde

```text
https://www.who.int/news-room/fact-sheets/detail/diabetes
```

### Organização Pan-Americana da Saúde

```text
https://www.paho.org/pt/topics/diabetes
```

---

## Hipertensão

### Ministério da Saúde

```text
https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/h/hipertensao
```

### Organização Mundial da Saúde

```text
https://www.who.int/news-room/fact-sheets/detail/hypertension
```

### Organização Pan-Americana da Saúde

```text
https://www.paho.org/pt/topics/hypertension
```

---

## Medicamentos

### Ministério da Saúde

```text
https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/m/medicamentos
```

### Organização Mundial da Saúde

```text
https://www.who.int/news-room/fact-sheets/detail/essential-medicines
```

### Organização Pan-Americana da Saúde

```text
https://www.paho.org/pt/topics/medicines
```

---

## Vacinas

### Ministério da Saúde — Gripe/Influenza

```text
https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/g/gripe-influenza
```

### Anvisa

```text
https://www.gov.br/anvisa/pt-br/assuntos/fiscalizacao-e-monitoramento/farmacovigilancia/vacinas
```

### Fiocruz

```text
https://www.ioc.fiocruz.br/noticias/por-que-se-vacinar-contra-gripe-todo-ano-entenda-o-papel-do-ioc-na-definicao-da-formulacao
```

---

# 8. Carregamento

O processamento da base é realizado por:

```text
backend/carregar_documentos.py
```

O carregador percorre os arquivos Markdown e extrai:

```text
conteúdo
título
fonte
URL
tema
subtema
data de acesso
```

Essas informações são propagadas para os chunks e posteriormente podem ser apresentadas junto às evidências recuperadas.

---

# 9. Limpeza dos documentos

Durante o desenvolvimento, alguns documentos possuíam seções auxiliares como:

```text
## Alegações relacionadas
## Palavras-chave
```

Essas seções eram úteis para organização manual da base, mas poderiam influenciar artificialmente a recuperação semântica.

Por isso, o carregamento remove essas seções antes do chunking.

O conteúdo destinado à recuperação fica concentrado nas informações documentais relevantes.

---

# 10. Chunking

Os documentos são divididos em unidades menores chamadas:

```text
chunks
```

A divisão permite que o sistema recupere trechos específicos em vez de enviar documentos completos ao modelo de linguagem.

Durante o desenvolvimento foram observadas diferentes quantidades de chunks.

Após a limpeza das seções auxiliares, a configuração utilizada na avaliação final possui:

```text
73 chunks
```

Esses chunks formam o conjunto consultado pelo mecanismo de busca semântica.

---

# 11. Embeddings

Cada chunk é convertido em uma representação vetorial utilizando:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Os embeddings permitem comparar semanticamente a alegação analisada com os trechos existentes na base.

O processo pode ser representado como:

```text
18 documentos
      ↓
Limpeza
      ↓
Chunking
      ↓
73 chunks
      ↓
Embeddings
      ↓
Busca semântica
```

---

# 12. Recuperação

Quando uma alegação é analisada, o sistema compara seu embedding com os chunks da base.

A implementação atual utiliza:

```text
similaridade de cosseno
+
pequeno componente de sobreposição lexical
```

A ordenação seleciona os trechos mais relacionados à alegação.

Atualmente são recuperados:

```text
Top 5 chunks
```

Esses trechos são fornecidos ao RAG.

---

# 13. Evidência recuperada x evidência utilizada

É importante distinguir dois conceitos.

## Evidência recuperada

É um chunk selecionado pelo mecanismo de busca por apresentar relação semântica ou lexical com a alegação.

## Evidência utilizada

É uma evidência que foi considerada relevante para fundamentar a classificação produzida.

Portanto:

```text
Recuperação ≠ utilização como suporte
```

Um trecho pode ser semanticamente parecido com a alegação sem fornecer evidência suficiente para confirmá-la ou contradizê-la.

---

# 14. Similaridade semântica

A similaridade exibida pelo HealthCheck IA corresponde à proximidade semântica entre a alegação e o chunk.

Ela não representa:

```text
probabilidade de verdade
confiança da classificação
confiança da IA
qualidade científica da fonte
```

Uma evidência pode apresentar alta similaridade justamente porque contradiz diretamente a alegação.

---

# 15. Critérios para inclusão de fontes

Na versão atual do projeto, foram priorizados documentos que permitissem:

```text
identificar a instituição responsável;
registrar uma URL original;
organizar o conteúdo por tema;
manter rastreabilidade;
utilizar conteúdo relacionado aos temas do MVP.
```

A base prioriza instituições oficiais ou reconhecidas na área da saúde.

---

# 16. Atualização da base

A base de conhecimento do HealthCheck IA **não é atualizada em tempo real**.

Por isso, foi definida uma política de atualização.

Cada documento deve manter, sempre que possível:

```text
Título
Fonte
URL
Tema
Subtema
Data de acesso
```

As fontes devem ser revisadas periodicamente.

Durante a revisão devem ser observados aspectos como:

```text
A página ainda está disponível?

O conteúdo foi atualizado?

A recomendação continua válida?

A URL mudou?

Existe nova orientação institucional?
```

---

# 17. Temas que exigem maior atenção

Alguns assuntos de saúde podem mudar mais rapidamente e devem receber prioridade durante revisões da base.

Exemplos:

```text
vacinação
surtos e epidemias
medicamentos
recomendações clínicas
alertas de saúde pública
```

Quando uma fonte institucional modificar uma orientação relevante, a versão utilizada pela base deve ser revisada.

---

# 18. Atualização de chunks e embeddings

Uma alteração documental não termina na edição do arquivo Markdown.

Quando o conteúdo relevante de um documento é atualizado, os dados derivados também precisam refletir essa alteração.

Fluxo:

```text
Fonte atualizada
      ↓
Documento atualizado
      ↓
Novo processamento
      ↓
Chunks atualizados
      ↓
Embeddings correspondentes
      ↓
Nova recuperação
```

Isso evita que o sistema continue utilizando representações derivadas de conteúdo antigo.

---

# 19. Limitações da base

A base atual possui limitações importantes.

## Cobertura limitada

Os 18 documentos não representam todo o conhecimento disponível sobre saúde.

## Temas limitados

A versão atual está concentrada em seis áreas.

## Atualização não automática

Novas recomendações podem existir antes de serem incorporadas ao projeto.

## Dependência das fontes selecionadas

A composição da base influencia diretamente quais evidências podem ser recuperadas.

## Ausência de evidência

Uma informação não encontrada na base não deve ser considerada automaticamente falsa.

---

# 20. Viés documental

A seleção de documentos institucionais melhora a rastreabilidade, mas também influencia o tipo de informação disponível ao sistema.

Isso pode produzir um:

```text
viés da base documental
```

Temas com maior cobertura possuem mais oportunidades de recuperação de evidências.

Temas pouco representados podem produzir mais casos de:

```text
NÃO FOI POSSÍVEL VERIFICAR
```

---

# 21. Política de abstenção e base de conhecimento

Quando a base não fornece evidências suficientes para avaliar uma alegação, o sistema deve evitar produzir uma conclusão sem suporte.

A classificação prevista é:

```text
NÃO FOI POSSÍVEL VERIFICAR
```

Princípio fundamental:

> **Ausência de evidência na base não prova que uma alegação seja falsa.**

O usuário deve ser informado de que podem existir informações relevantes fora da base consultada.

---

# 22. Transparência

A interface do HealthCheck IA permite apresentar os metadados associados às evidências.

O usuário pode verificar:

```text
Fonte
Título
Trecho recuperado
Similaridade semântica
URL original
```

Essa rastreabilidade é importante para que o usuário possa consultar diretamente a origem da informação.

---

# 23. Papel da base no HealthCheck IA

A base de conhecimento é uma das partes centrais da arquitetura.

```text
BASE DE CONHECIMENTO
        ↓
EVIDÊNCIAS
        ↓
RAG
        ↓
LLM
        ↓
CLASSIFICAÇÃO
        ↓
EXPLICAÇÃO
```

A qualidade da resposta depende não apenas do modelo de linguagem, mas também da:

```text
qualidade
cobertura
atualização
organização
recuperação
```

das evidências disponíveis.

---

# 24. Resumo

A versão atual da base possui:

```text
18 documentos
6 temas
73 chunks
6 instituições principais
metadados rastreáveis
links para fontes originais
```

Temas:

```text
Câncer
Dengue
Diabetes
Hipertensão
Medicamentos
Vacinas
```

Instituições:

```text
Ministério da Saúde
Anvisa
Fiocruz
INCA
OMS
OPAS
```

A base não pretende representar todo o conhecimento médico disponível.

Ela constitui o conjunto de evidências utilizado pelo MVP atual do HealthCheck IA.

---

## HealthCheck IA

**Inteligência Artificial + Evidências + Pensamento Crítico**

A base de conhecimento foi estruturada para manter as evidências rastreáveis e permitir que o usuário consulte as fontes originais utilizadas durante a análise.