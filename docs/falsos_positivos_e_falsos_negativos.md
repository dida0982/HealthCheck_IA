Como temos **cinco classes**, “falso positivo” e “falso negativo” dependem de qual classe estamos analisando. Por isso, para o nosso projeto, a **matriz de confusão é mais informativa** do que falar apenas em FP/FN.

A matriz obtida nas 200 alegações foi:

```text
ESPERADO ↓              SUST.   PARC.   ENGAN.   CONTR.   NÃO VERIF.
SUSTENTADA                40      0        0        0          0
PARCIAL                    16     12        1        1         10
ENGANOSA                    0      1       33        1          5
CONTRADITA                  2      0       12       26          0
NÃO VERIFICÁVEL             0      0        0        0         40
```

Dos **200 casos**, tivemos **151 acertos e 49 erros**. Isso corresponde à acurácia de **75,5%**.

Os erros ficaram bastante concentrados. Os três principais foram:

```text
PARCIAL → SUSTENTADA
16 casos

CONTRADITA → ENGANOSA
12 casos

PARCIAL → NÃO FOI POSSÍVEL VERIFICAR
10 casos
```

Só esses três tipos representam **38 dos 49 erros**, aproximadamente **77,6%**.

Isso nos mostra uma limitação específica do sistema: a maior dificuldade está em alegações que exigem distinguir **uma afirmação parcialmente sustentada de uma totalmente sustentada**, e em separar **contradição direta de informação enganosa**.

Para a documentação da Etapa 15, podemos registrar:

> **Falsos positivos e falsos negativos:** por utilizar cinco categorias, os erros do HealthCheck IA foram analisados por meio de uma matriz de confusão multiclasse. Na avaliação com 200 alegações, o sistema classificou corretamente 151 casos (75,5%). Os erros mais frequentes ocorreram entre categorias semanticamente próximas, principalmente em alegações parcialmente sustentadas classificadas como sustentadas e alegações contraditas classificadas como enganosas. Esses resultados demonstram que a saída do sistema não deve ser interpretada como uma determinação infalível da veracidade de uma informação.

Há ainda um ponto de segurança importante. No teste final, as classes tiveram comportamentos bem diferentes:

```text
SUSTENTADA              recall = 100%
PARCIALMENTE SUSTENTADA recall = 30%
ENGANOSA                recall = 82,5%
CONTRADITA              recall = 65%
NÃO VERIFICÁVEL         recall = 100%
```

O **30% de recall da classe PARCIALMENTE SUSTENTADA** é uma limitação relevante e deve ser documentada, não escondida. O sistema teve dificuldade considerável justamente nessa categoria.

Isso fortalece nossa decisão anterior de mostrar **explicação + evidências + fontes**, em vez de entregar apenas um rótulo colorido ao usuário.
