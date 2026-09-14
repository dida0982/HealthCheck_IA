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

15. Antes de avaliar "PARCIALMENTE SUSTENTADA" ou "ENGANOSA",
    verifique obrigatoriamente se existe contradição direta entre
    a afirmação central da alegação e as evidências.

16. Se a alegação afirmar algo e pelo menos uma evidência diretamente
    relevante afirmar explicitamente o contrário, classifique como:
    "CONTRADITA PELAS EVIDÊNCIAS".

17. Quando houver contradição direta da afirmação central,
    "CONTRADITA PELAS EVIDÊNCIAS" tem prioridade sobre:
    "PARCIALMENTE SUSTENTADA" e "ENGANOSA".

18. Não classifique como "PARCIALMENTE SUSTENTADA" quando a afirmação
    central estiver explicitamente contradita pelas evidências.

19. Não classifique como "ENGANOSA" quando a afirmação central estiver
    explicitamente contradita pelas evidências. Nesse caso use:
    "CONTRADITA PELAS EVIDÊNCIAS".

20. Classifique como "CONTRADITA PELAS EVIDÊNCIAS" quando a evidência
    fornecer uma resposta incompatível com a afirmação central da alegação.

21. A contradição não exige uma negação literal. Também existe contradição
    quando a alegação atribui uma propriedade, causa, forma principal,
    característica ou resultado a X, mas a evidência atribui essa mesma
    propriedade ou papel a Y de forma incompatível com X.

22. Use "NÃO FOI POSSÍVEL VERIFICAR" somente quando as evidências não
    confirmarem nem contradisserem a afirmação central da alegação.
    Não use essa classe quando as evidências fornecerem uma resposta
    incompatível para o mesmo fato central.

23. Não classifique automaticamente como "ENGANOSA" apenas porque uma
    parte da alegação não está sustentada.

24. Se uma parte estiver claramente sustentada e outra apenas não puder
    ser confirmada, sem distorção e sem contradição direta, classifique:
    "PARCIALMENTE SUSTENTADA".

25. Use "ENGANOSA" quando houver uma relação de raciocínio distorcida,
    como utilizar uma informação verdadeira para justificar uma
    conclusão exagerada ou incorreta.
    
26. Utilize na conclusão apenas evidências que estejam diretamente
    relacionadas à afirmação central da alegação.

27. Não utilize uma evidência apenas porque ela pertence ao mesmo tema.
    A evidência precisa fornecer informação diretamente útil para
    confirmar, contradizer ou qualificar a alegação analisada.

28. Não faça inferências que não estejam explicitamente apoiadas pelas
    evidências. Não transforme informações genéricas em conclusões que
    elas não sustentam.

29. O campo "evidencias_utilizadas" deve conter somente evidências que
    tenham sido realmente necessárias para chegar à conclusão.

30. Quando houver evidências diretamente relacionadas à alegação e
    outras apenas genericamente relacionadas ao tema, priorize as
    evidências diretamente relacionadas.

31. Não utilize uma evidência irrelevante para justificar uma
    classificação que foi obtida a partir de outra evidência.
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

IMPORTANTE SOBRE AS EVIDÊNCIAS:

- Os números em "evidencias_utilizadas" devem corresponder exatamente
  aos números das evidências apresentadas acima.

- Antes de responder, confira se cada afirmação da explicação está
  explicitamente presente nas evidências indicadas.

- Não atribua a uma evidência uma informação que pertença a outra.

- Não reformule uma evidência de maneira que acrescente informação
  que não esteja escrita nela.

- Se a conclusão exigir mais de uma evidência, inclua todas as
  evidências necessárias em "evidencias_utilizadas".
"""