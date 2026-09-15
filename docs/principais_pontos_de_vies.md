POSSÍVEIS VIESES DO HEALTHCHECK IA

1. VIÉS DA BASE DOCUMENTAL

O sistema depende das fontes incluídas na base de conhecimento.

A versão atual utiliza principalmente documentos de organizações
oficiais e instituições de saúde, como Ministério da Saúde, Anvisa,
Fiocruz, INCA, OMS e OPAS.

Isso aumenta a rastreabilidade das evidências, mas também significa
que a análise reflete principalmente o conteúdo e a cobertura dessas
instituições.

Temas pouco documentados na base podem resultar com maior frequência
em "NÃO FOI POSSÍVEL VERIFICAR".


2. VIÉS DA RECUPERAÇÃO SEMÂNTICA

O sistema não envia toda a base documental ao modelo.

O mecanismo de busca seleciona os trechos considerados mais
relacionados semanticamente à alegação.

Portanto, uma evidência relevante pode existir na base e não aparecer
entre os trechos recuperados.

Além disso, trechos semanticamente semelhantes podem ser recuperados
mesmo quando não são os melhores para decidir a alegação.


3. VIÉS DO MODELO DE LINGUAGEM

O Qwen 2.5 7B é responsável por interpretar a alegação e comparar
as evidências recuperadas.

Como qualquer modelo de linguagem, ele pode interpretar de maneira
incorreta relações de negação, causalidade, intensidade, condições
e afirmações compostas.

O prompt estabelece regras para reduzir esse comportamento, mas não
garante que o modelo as seguirá corretamente em todos os casos.


4. VIÉS DO CONJUNTO DE AVALIAÇÃO

O conjunto final possui 200 alegações balanceadas entre as cinco
classes.

Esse balanceamento facilita a comparação entre categorias, mas não
representa necessariamente a distribuição real das informações de
saúde encontradas na internet.

Além disso, o conjunto de avaliação foi construído no próprio contexto
do projeto. Portanto, os resultados medem o desempenho nesse conjunto
específico e não constituem uma validação externa independente.


Os resultados do HealthCheck IA podem ser influenciados pela composição da base documental, pelo mecanismo de recuperação semântica, pelo comportamento do modelo de linguagem e pelas características do conjunto utilizado na avaliação.