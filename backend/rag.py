from busca_semantica import buscar_evidencias


def montar_contexto_rag(alegacao, evidencias):

    contexto = f"""
ALEGAÇÃO:

{alegacao}

EVIDÊNCIAS RECUPERADAS:
"""

    for posicao, evidencia in enumerate(evidencias, start=1):

        contexto += f"""

EVIDÊNCIA {posicao}

Arquivo:
{evidencia["arquivo"]}

Chunk:
{evidencia["chunk_id"]}

Similaridade:
{evidencia["similaridade"]:.4f}

Conteúdo:
{evidencia["conteudo"]}
"""

    return contexto


def montar_prompt_rag(alegacao, evidencias):

    contexto = montar_contexto_rag(
        alegacao,
        evidencias
    )

    prompt = f"""
Você é o componente de análise do HealthCheck IA.

Sua tarefa é avaliar uma alegação relacionada à saúde utilizando SOMENTE
as evidências fornecidas abaixo.

REGRAS OBRIGATÓRIAS:

1. Utilize somente as evidências fornecidas neste contexto.
2. Não utilize conhecimento externo.
3. Não invente fatos, dados, estudos ou fontes.
4. Não presuma informações que não estejam presentes nas evidências.
5. Diferencie ausência de evidência de evidência de ausência.
6. Se as evidências forem insuficientes, conflitantes ou não permitirem
   uma conclusão segura, classifique como "NÃO FOI POSSÍVEL VERIFICAR".
7. A similaridade semântica não representa verdade e não deve ser usada,
   sozinha, para decidir a classificação.
8. Explique de forma objetiva quais evidências sustentam sua conclusão.

CLASSIFIQUE A ALEGAÇÃO EM APENAS UMA DAS CATEGORIAS:

- SUSTENTADA PELAS EVIDÊNCIAS
- PARCIALMENTE SUSTENTADA
- ENGANOSA
- CONTRADITA PELAS EVIDÊNCIAS
- NÃO FOI POSSÍVEL VERIFICAR

{contexto}

FORMATO OBRIGATÓRIO DA RESPOSTA:

Responda SOMENTE com um JSON válido.

Não escreva nenhum texto antes ou depois do JSON.

Use exatamente esta estrutura:

{{
    "classificacao": "SUSTENTADA PELAS EVIDÊNCIAS",
    "explicacao": "Explique de forma curta e objetiva a conclusão.",
    "evidencias_utilizadas": [1, 2, 3]
}}

O campo "classificacao" deve conter exatamente uma destas opções:

- SUSTENTADA PELAS EVIDÊNCIAS
- PARCIALMENTE SUSTENTADA
- ENGANOSA
- CONTRADITA PELAS EVIDÊNCIAS
- NÃO FOI POSSÍVEL VERIFICAR

O campo "explicacao" deve conter uma explicação curta baseada somente nas evidências recuperadas.

O campo "evidencias_utilizadas" deve conter somente os números das evidências realmente utilizadas na conclusão.

Se nenhuma evidência for suficiente, utilize uma lista vazia:

"evidencias_utilizadas": []
"""

    return prompt


if __name__ == "__main__":

    alegacao = "A vacina contra gripe ajuda a evitar casos graves?"

    evidencias = buscar_evidencias(
        alegacao,
        top_k=3
    )

    prompt = montar_prompt_rag(
        alegacao,
        evidencias
    )

    print("\n=== PROMPT RAG ===")
    print(prompt)