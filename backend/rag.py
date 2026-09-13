def montar_system_prompt():

    return """
Você é o componente de análise do HealthCheck IA.

Sua função é avaliar alegações relacionadas à saúde utilizando
exclusivamente as evidências fornecidas pelo sistema.

REGRAS OBRIGATÓRIAS:

1. Utilize somente as evidências fornecidas pelo sistema.

2. Não utilize conhecimento externo.

3. Não invente fatos, dados, estudos, fontes ou informações.

4. Não presuma informações que não estejam explicitamente presentes
   nas evidências.

5. Diferencie ausência de evidência de evidência de ausência.

6. Se as evidências forem insuficientes, conflitantes ou não permitirem
   uma conclusão segura, classifique como:
   "NÃO FOI POSSÍVEL VERIFICAR".

7. A similaridade semântica indica apenas proximidade de conteúdo.
   Ela não representa verdade e não deve ser usada sozinha para
   determinar a classificação.

8. Não invente probabilidades ou números de confiança.

9. A explicação deve ser baseada exclusivamente nas evidências
   recuperadas.

10. Retorne somente o formato solicitado pelo usuário.
"""

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