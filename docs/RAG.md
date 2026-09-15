# 🧠 RAG — HealthCheck IA

## 1. Visão geral

O HealthCheck IA utiliza **RAG (Retrieval-Augmented Generation)** para analisar alegações relacionadas à saúde.

A ideia central é evitar que o modelo de linguagem produza uma classificação utilizando apenas o conhecimento adquirido durante seu treinamento.

Antes da geração da resposta, o sistema recupera evidências da base de conhecimento do projeto e fornece esses trechos ao modelo.

O fluxo principal é:

```text
Alegação
   ↓
Embedding
   ↓
Busca de evidências
   ↓
Top 5 chunks
   ↓
Construção do contexto
   ↓
Prompt
   ↓
Qwen 2.5 7B
   ↓
Classificação
   ↓
Explicação
   ↓
Evidências utilizadas
```

---

# 2. Por que utilizar RAG?

Um modelo de linguagem pode produzir respostas plausíveis mesmo quando não possui evidências suficientes para sustentá-las.

Na área da saúde, esse comportamento representa um risco importante.

O RAG permite colocar uma camada de recuperação de informação antes da geração.

No HealthCheck IA, o objetivo é fazer com que o modelo responda à seguinte questão:

> **Qual é a relação entre esta alegação e as evidências recuperadas da base de conhecimento?**

Assim, o LLM funciona principalmente como um componente de interpretação das evidências.

---

# 3. Base documental

A recuperação começa na base localizada em:

```text
data/
```

A versão atual contém **18 documentos** distribuídos entre seis temas:

```text
cancer
dengue
diabetes
hipertensao
medicamentos
vacinas
```

Os documentos incluem metadados como:

```text
Título
Fonte
URL
Tema
Subtema
Data de acesso
```

Esses metadados permitem rastrear a origem das evidências apresentadas ao usuário.

---

# 4. Carregamento dos documentos

O processamento dos documentos é realizado por:

```text
backend/carregar_documentos.py
```

Durante essa etapa, o sistema:

```text
Lê os documentos
      ↓
Extrai os metadados
      ↓
Limpa seções auxiliares
      ↓
Divide o conteúdo em chunks
      ↓
Disponibiliza os chunks para indexação
```

Seções auxiliares utilizadas durante a construção da base, como:

```text
## Alegações relacionadas
## Palavras-chave
```

são removidas antes do chunking.

Após essa limpeza, a versão utilizada na avaliação possui:

```text
73 chunks
```

---

# 5. Embeddings

Para comparar semanticamente uma alegação com os chunks, o sistema utiliza embeddings.

Modelo:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

O embedding transforma um texto em uma representação vetorial.

De forma simplificada:

```text
"A vacina ajuda a prevenir casos graves."
                  ↓
             EMBEDDING
                  ↓
       [representação vetorial]
```

O mesmo processo é realizado com os chunks da base.

Isso permite comparar semanticamente a alegação com as evidências disponíveis.

---

# 6. Busca semântica

A busca está implementada em:

```text
backend/busca_semantica.py
```

Quando uma alegação é recebida, o sistema gera seu embedding e o compara com os embeddings dos chunks.

A comparação utiliza:

```text
similaridade de cosseno
```

Além da similaridade semântica, a ordenação atual utiliza um pequeno componente de sobreposição lexical.

De forma simplificada:

```text
score de ordenação
=
similaridade semântica
+
componente lexical
```

Esse mecanismo auxilia a priorização de chunks que possuem proximidade semântica e também termos relevantes em comum com a alegação.

---

# 7. Similaridade semântica

O valor de similaridade apresentado pelo sistema corresponde à **similaridade de cosseno** entre a alegação e o chunk.

Esse valor deve ser interpretado apenas como uma medida de proximidade entre os textos.

Portanto:

```text
Similaridade semântica ≠ probabilidade de verdade
Similaridade semântica ≠ confiança da IA
Similaridade semântica ≠ confiança da classificação
```

Um trecho pode possuir alta similaridade com uma alegação e, ainda assim, contradizê-la.

Por exemplo:

```text
Alegação:
"A vacina aumenta o risco de casos graves."

Evidência:
"A vacinação reduz o risco de casos graves."
```

Os textos tratam do mesmo assunto e podem possuir alta similaridade semântica, embora apresentem sentidos opostos.

---

# 8. Recuperação das evidências

Após calcular os scores, os chunks são ordenados.

A configuração utilizada atualmente recupera:

```text
Top 5 evidências
```

Esses cinco trechos formam o contexto disponibilizado ao modelo de linguagem.

O fato de um chunk ter sido recuperado não significa automaticamente que ele será considerado evidência utilizada na classificação.

Existe uma diferença entre:

```text
EVIDÊNCIA RECUPERADA
```

e:

```text
EVIDÊNCIA UTILIZADA
```

A primeira foi considerada semanticamente relevante pelo mecanismo de recuperação.

A segunda foi indicada como efetivamente relevante para fundamentar a classificação produzida.

---

# 9. Construção do RAG

O arquivo:

```text
backend/rag.py
```

é responsável pela construção das instruções utilizadas durante a análise.

O processo pode ser representado como:

```text
Alegação
   +
Evidência 1
   +
Evidência 2
   +
Evidência 3
   +
Evidência 4
   +
Evidência 5
   ↓
System Prompt
   +
User Prompt
   ↓
LLM
```

O modelo recebe explicitamente as evidências recuperadas e deve realizar a classificação considerando esse contexto.

---

# 10. System Prompt

O `system prompt` estabelece as regras gerais que devem orientar o comportamento do modelo.

Entre elas estão:

```text
Utilizar somente as evidências fornecidas
Não utilizar conhecimento externo
Não inventar fatos
Não inventar fontes
Não inventar estudos
Não presumir informações ausentes
Não interpretar ausência de evidência como falsidade
Utilizar abstenção quando não houver suporte suficiente
```

Também existem regras destinadas a diferenciar as cinco categorias de classificação.

---

# 11. User Prompt

O `user prompt` contém os dados específicos da análise.

De forma conceitual:

```text
ALEGAÇÃO

[texto que será analisado]

EVIDÊNCIAS

[1] evidência recuperada
[2] evidência recuperada
[3] evidência recuperada
[4] evidência recuperada
[5] evidência recuperada
```

O modelo deve responder considerando a relação entre a alegação e esses trechos.

---

# 12. Modelo de linguagem

O modelo utilizado atualmente é:

```text
qwen2.5:7b
```

executado localmente utilizando:

```text
Ollama
```

Na configuração congelada utilizada durante a avaliação:

```text
temperature = 0
seed = 42
top_k de evidências = 5
```

A temperatura igual a zero reduz a variabilidade da geração.

A utilização de uma seed também contribui para maior reprodutibilidade dos experimentos, embora a execução de modelos de linguagem não deva ser considerada absolutamente determinística em todos os ambientes.

---

# 13. Resposta estruturada

O HealthCheck IA solicita uma resposta estruturada contendo informações como:

```text
classificacao
explicacao
evidencias_utilizadas
```

As classificações permitidas são:

```text
SUSTENTADA PELAS EVIDÊNCIAS

PARCIALMENTE SUSTENTADA

ENGANOSA

CONTRADITA PELAS EVIDÊNCIAS

NÃO FOI POSSÍVEL VERIFICAR
```

---

# 14. Evidências utilizadas

O modelo indica quais evidências recuperadas foram efetivamente utilizadas para fundamentar sua análise.

Por exemplo:

```json
{
  "classificacao": "CONTRADITA PELAS EVIDÊNCIAS",
  "explicacao": "As evidências recuperadas apresentam informações incompatíveis com a alegação.",
  "evidencias_utilizadas": [1, 3]
}
```

O backend associa esses índices aos chunks recuperados.

Dessa forma, a interface pode apresentar ao usuário os trechos utilizados e seus respectivos metadados.

---

# 15. Política de abstenção

Um componente central do RAG do HealthCheck IA é a política de abstenção.

Quando as evidências recuperadas não permitem confirmar nem contradizer adequadamente uma alegação, o modelo deve retornar:

```text
NÃO FOI POSSÍVEL VERIFICAR
```

Nesses casos, a resposta deve evitar transformar ausência de informação em conclusão.

Princípio:

> **Ausência de evidência não significa evidência de falsidade.**

Quando nenhuma evidência fornece suporte adequado, o modelo também pode retornar:

```json
{
  "evidencias_utilizadas": []
}
```

Isso evita que trechos sejam apresentados como suporte apenas porque tratam do mesmo assunto.

---

# 16. Evidências contraditórias entre si

Existe uma diferença importante entre:

```text
As evidências contradizem a alegação
```

e:

```text
As evidências recuperadas contradizem umas às outras
```

No primeiro caso, quando as fontes relevantes concordam entre si e apresentam informações incompatíveis com a alegação, a classificação pode ser:

```text
CONTRADITA PELAS EVIDÊNCIAS
```

No segundo caso, quando fontes relevantes apresentam informações conflitantes e o conflito impede uma conclusão segura, a política definida para o sistema é a abstenção:

```text
NÃO FOI POSSÍVEL VERIFICAR
```

O modelo não deve escolher arbitrariamente uma das fontes conflitantes.

---

# 17. Exemplo de fluxo

Considere a alegação:

```text
"A vacina contra gripe aumenta o risco de formas graves da doença."
```

O sistema executa:

```text
1. Recebe a alegação

2. Gera o embedding

3. Compara com os 73 chunks

4. Recupera os 5 chunks mais relevantes

5. Insere as evidências no contexto

6. Envia o prompt ao Qwen

7. O modelo compara a alegação com as evidências

8. Identifica que as evidências indicam redução do risco de formas graves

9. Produz:
   CONTRADITA PELAS EVIDÊNCIAS

10. Indica quais evidências foram utilizadas

11. O backend retorna a resposta

12. A extensão apresenta classificação,
    explicação e fontes ao usuário
```

---

# 18. Limitações do RAG

O uso de RAG reduz alguns riscos, mas não elimina erros.

Existem diferentes pontos de falha possíveis:

```text
Alegação
   ↓
[1] Embedding pode representar imperfeitamente o texto
   ↓
[2] Retrieval pode não recuperar o melhor chunk
   ↓
[3] Evidência pode ser insuficiente
   ↓
[4] LLM pode interpretar incorretamente a evidência
   ↓
[5] Classificação pode ser incorreta
```

Portanto, possuir uma arquitetura RAG não significa que todas as respostas estarão corretas.

---

# 19. Retrieval e geração são avaliados em conjunto

O resultado final depende de duas grandes etapas:

```text
RETRIEVAL
Encontrar evidências relevantes

+

GENERATION
Interpretar corretamente essas evidências
```

Um erro na recuperação pode fornecer contexto inadequado ao modelo.

Mesmo com retrieval correto, o LLM ainda pode interpretar incorretamente uma relação de:

- negação;
- causalidade;
- intensidade;
- condição;
- generalização;
- composição de múltiplas afirmações.

Essas limitações foram consideradas durante a avaliação do projeto.

---

# 20. Relação com o pensamento crítico

O RAG também permite que o usuário tenha acesso aos trechos utilizados na análise.

Isso é importante porque a resposta não termina na classificação.

O usuário pode verificar:

```text
Qual evidência foi utilizada?

Quem publicou?

Qual é o documento?

Qual é a fonte original?

O trecho realmente sustenta a explicação?
```

Assim, a arquitetura permite que a IA funcione como ferramenta de apoio à consulta das evidências.

---

# 21. Resumo técnico

```text
Documentos oficiais
       ↓
Chunking
       ↓
73 chunks
       ↓
Sentence Transformers
       ↓
Embeddings
       ↓
Busca semântica + componente lexical
       ↓
Top 5
       ↓
RAG
       ↓
System Prompt + User Prompt
       ↓
Ollama
       ↓
Qwen 2.5 7B
       ↓
Classificação
       ↓
Explicação
       ↓
Evidências utilizadas
       ↓
FastAPI
       ↓
Chrome Extension
       ↓
Usuário
```

---

## HealthCheck IA

**Inteligência Artificial + Evidências + Pensamento Crítico**

O RAG do HealthCheck IA foi desenvolvido para manter as evidências no centro da análise, reduzindo a dependência do conhecimento interno do modelo e permitindo que o usuário consulte as fontes utilizadas.