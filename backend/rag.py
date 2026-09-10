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


def montar_user_prompt(alegacao, evidencias):

    contexto = montar_contexto_rag(
        alegacao,
        evidencias
    )

    return f"""
{contexto}

CLASSIFIQUE A ALEGAÇÃO EM APENAS UMA DAS CATEGORIAS:

- SUSTENTADA PELAS EVIDÊNCIAS
- PARCIALMENTE SUSTENTADA
- ENGANOSA
- CONTRADITA PELAS EVIDÊNCIAS
- NÃO FOI POSSÍVEL VERIFICAR

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

Se nenhuma evidência for suficiente, utilize:

"evidencias_utilizadas": []
"""