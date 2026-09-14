async function analisarResultado(item) {
  try {
    const resposta = await fetch("http://127.0.0.1:8000/analisar", {
      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        titulo: item.titulo,
        descricao: item.descricao
      })
    });

if (!resposta.ok) {
  const erroBackend = await resposta.text();

  throw new Error(
    `Erro HTTP ${resposta.status}: ${erroBackend}`
  );
}

    const dados = await resposta.json();

    console.log("Resposta do backend:", dados);

    return dados;

  } catch (erro) {
    console.error("Erro ao conectar com o backend:", erro);

    return null;
  }
}


function escaparHTML(texto) {
  const elemento = document.createElement("div");

  elemento.textContent = texto ?? "";

  return elemento.innerHTML;
}


function obterConfiguracaoClassificacao(classificacao) {

  switch (classificacao) {

    case "SUSTENTADA PELAS EVIDÊNCIAS":
      return {
        status: "Evidências favoráveis",
        icone: "🟢",
        classe: "healthcheck-sustentada",
        mensagem:
          "As fontes consultadas são compatíveis com a afirmação, mas isso não dispensa a verificação do contexto.",
        compartilhar:
          "Leia as evidências e consulte as fontes originais antes de compartilhar."
      };


    case "PARCIALMENTE SUSTENTADA":
      return {
        status: "Evidências parcialmente favoráveis",
        icone: "🟡",
        classe: "healthcheck-parcial",
        mensagem:
          "Parte da afirmação possui suporte nas evidências, mas outra parte não pôde ser confirmada.",
        compartilhar:
          "Verifique separadamente cada informação antes de compartilhar a afirmação completa."
      };


    case "ENGANOSA":
      return {
        status: "Informação potencialmente enganosa",
        icone: "🟠",
        classe: "healthcheck-enganosa",
        mensagem:
          "Uma informação verdadeira ou plausível pode estar sendo usada para sustentar uma conclusão exagerada ou distorcida.",
        compartilhar:
          "Compare a afirmação completa com aquilo que as fontes realmente dizem antes de compartilhar."
      };


    case "CONTRADITA PELAS EVIDÊNCIAS":
      return {
        status: "Evidências contraditórias",
        icone: "🔴",
        classe: "healthcheck-contraditoria",
        mensagem:
          "As evidências encontradas apresentam informações incompatíveis com a afirmação.",
        compartilhar:
          "Leia a explicação e confira as fontes originais antes de compartilhar essa informação."
      };


    case "NÃO FOI POSSÍVEL VERIFICAR":
      return {
        status: "Evidências insuficientes",
        icone: "⚪",
        classe: "healthcheck-nao-verificada",
        mensagem:
          "O HealthCheck IA não encontrou evidências suficientes na base consultada para confirmar ou contradizer esta afirmação. Isso não significa que a informação seja verdadeira ou falsa.",
        compartilhar:
          "Procure outras fontes confiáveis e atualizadas antes de compartilhar."
      };


    default:
      return {
        status: "Resultado recebido",
        icone: "🔎",
        classe: "",
        mensagem:
          "Analise as evidências apresentadas antes de tirar uma conclusão.",
        compartilhar:
          "Consulte as fontes originais antes de compartilhar."
      };
  }
}


async function capturarResultados() {

  const resultados =
    document.querySelectorAll("div.MjjYud");


  for (const resultado of resultados) {

    const tituloElemento =
      resultado.querySelector("h3");

    const linkElemento =
      tituloElemento?.closest("a");


    const descricaoElemento =
      resultado.querySelector(".VwiC3b") ||
      resultado.querySelector("[data-sncf]");


    if (!tituloElemento || !linkElemento) {
      continue;
    }


    if (resultado.querySelector(".healthcheck-card")) {
      continue;
    }


    const item = {

      titulo:
        tituloElemento.innerText.trim(),

      url:
        linkElemento.href,

      descricao:
        descricaoElemento
          ? descricaoElemento.innerText.trim()
          : "Descrição não encontrada"

    };


    criarComponenteHealthCheck(
      resultado,
      item
    );
  }
}


async function criarComponenteHealthCheck(
  resultado,
  item
) {

  const card =
    document.createElement("div");


  card.className =
    "healthcheck-card";


  /*
    Estado inicial enquanto
    o backend realiza a análise.
  */

  card.innerHTML = `
    <div class="healthcheck-header">

      <div class="healthcheck-status">

        <span>
          🔎
        </span>

        <strong>
          HealthCheck IA
        </strong>

      </div>

      <div class="healthcheck-confidence">
        Analisando...
      </div>

    </div>

    <div class="healthcheck-loading">
      Buscando evidências e consultando a IA...
    </div>
  `;


  resultado.appendChild(card);


  /*
    Envia título e descrição
    para o FastAPI.
  */

  const analise =
    await analisarResultado(item);


  /*
    Caso o backend não responda.
  */

  if (!analise) {

    card.innerHTML = `
      <div class="healthcheck-header">

        <div class="healthcheck-status healthcheck-erro">

          <span>
            ⚠️
          </span>

          <strong>
            Não foi possível analisar
          </strong>

        </div>

      </div>

      <p>
        O servidor HealthCheck IA não respondeu.
      </p>
    `;

    return;
  }


  /*
    Resultado REAL vindo
    do RAG + Llama.
  */

  const classificacao =
    analise.classificacao;

  const explicacao =
    analise.explicacao;

  const evidencias =
    analise.evidencias || [];

  const evidenciasUtilizadas =
    analise.evidencias_utilizadas || [];


  const configuracao =
    obterConfiguracaoClassificacao(
      classificacao
    );


  /*
    Monta a lista das evidências
    recuperadas pelo RAG.
  */

let htmlEvidencias = "";


evidencias.forEach(
  (evidencia, indice) => {

    const numero =
      indice + 1;

    const foiUtilizada =
      evidenciasUtilizadas.includes(numero);

    const similaridade =
      typeof evidencia.similaridade === "number"
        ? (evidencia.similaridade * 100).toFixed(1)
        : null;

    const fonte =
      evidencia.fonte ||
      evidencia.arquivo ||
      "Fonte não identificada";

    const tituloFonte =
      evidencia.titulo ||
      "Documento consultado";

    const urlFonte =
      evidencia.url || "";


    htmlEvidencias += `
      <div class="healthcheck-evidence">

        <p>
          <strong>
            Evidência ${numero}
            ${foiUtilizada ? "✓" : ""}
          </strong>
        </p>

        <p>
          <strong>
            ${escaparHTML(fonte)}
          </strong>
        </p>

        <p>
          ${escaparHTML(tituloFonte)}
        </p>

        ${
          similaridade
            ? `
              <p>
                <small>
                  Similaridade semântica:
                  ${similaridade}%
                </small>
              </p>
            `
            : ""
        }

        <p>
          ${escaparHTML(evidencia.conteudo)}
        </p>

        ${
          urlFonte
            ? `
              <p>
                <a
                  href="${escaparHTML(urlFonte)}"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="healthcheck-source-link"
                >
                  🔗 Consultar fonte original
                </a>
              </p>
            `
            : `
              <p>
                <small>
                  ⚠ Link original não cadastrado na base.
                </small>
              </p>
            `
        }

      </div>
    `;
  }
);


  /*
    Atualiza o card com
    a análise real.
  */

  card.innerHTML = `
    <div class="healthcheck-header">

      <div
        class="
          healthcheck-status
          ${configuracao.classe}
        "
      >

        <span>
          ${configuracao.icone}
        </span>

        <strong>
          ${configuracao.status}
        </strong>

      </div>

    </div>


    <button
      class="healthcheck-button"
      aria-expanded="false"
      type="button"
    >

      Ver análise

    </button>


    <div
      class="healthcheck-details"
      hidden
    >


      <p>

        <strong>
          Classificação:
        </strong>

        ${escaparHTML(classificacao)}

      </p>


      <p>

        <strong>
          Explicação:
        </strong>

        ${escaparHTML(explicacao)}

      </p>


      <p>

        <strong>
          Resultado analisado:
        </strong>

        ${escaparHTML(item.titulo)}

      </p>


      <p>

        <strong>
          Site:
        </strong>

        ${escaparHTML(
          new URL(item.url).hostname
        )}

      </p>


      <hr>


      <h4>
        Evidências encontradas
      </h4>


      ${htmlEvidencias}


      <p class="healthcheck-warning">

        O HealthCheck IA apresenta
        evidências para auxiliar na
        avaliação da informação.
        A análise não substitui
        orientação profissional.

      </p>

    </div>
  `;


  const botao =
    card.querySelector(
      ".healthcheck-button"
    );


  const detalhes =
    card.querySelector(
      ".healthcheck-details"
    );


  botao.addEventListener(
    "click",
    () => {

      const estaAberto =
        botao.getAttribute(
          "aria-expanded"
        ) === "true";


      botao.setAttribute(
        "aria-expanded",
        String(!estaAberto)
      );


      detalhes.hidden =
        estaAberto;


      botao.innerText =
        estaAberto
          ? "Ver análise"
          : "Ocultar análise";

    }
  );
}



capturarResultados();



const observer =
  new MutationObserver(() => {

    capturarResultados();

  });



observer.observe(
  document.body,
  {
    childList: true,
    subtree: true
  }
);