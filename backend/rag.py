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

11. Antes de classificar, identifique qual é a afirmação central
    da alegação.

12. Compare especificamente essa afirmação central com as evidências.

13. A presença de informações verdadeiras sobre o mesmo tema não
    significa que a alegação está sustentada.

14. Para classificar como "SUSTENTADA PELAS EVIDÊNCIAS", as evidências
    devem confirmar diretamente a afirmação central da alegação.

15. Se a alegação afirmar algo e as evidências afirmarem explicitamente
    o contrário, classifique como:
    "CONTRADITA PELAS EVIDÊNCIAS".
    
16. Classifique como "PARCIALMENTE SUSTENTADA" quando a alegação
    possuir duas ou mais afirmações relevantes e pelo menos uma delas
    for sustentada pelas evidências, enquanto outra não for sustentada
    ou não puder ser confirmada.

17. Classifique como "ENGANOSA" quando a alegação utilizar informação
    verdadeira ou parcialmente verdadeira de maneira distorcida,
    fora de contexto ou que leve diretamente a uma conclusão incorreta.

18. Não classifique automaticamente como "ENGANOSA" apenas porque
    uma parte da alegação não está sustentada.

19. Se uma parte da alegação estiver claramente sustentada e outra
    parte apenas não estiver sustentada pelas evidências, prefira:
    "PARCIALMENTE SUSTENTADA".

20. Use "ENGANOSA" quando houver distorção do significado das
    evidências, e não apenas uma combinação de uma afirmação sustentada
    com outra não confirmada.
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