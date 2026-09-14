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

    const evidenciaExtra =
      indice >= 3;

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

    const conteudoLimpo =
  (evidencia.conteudo || "")
    .split("\n")
    .filter((linha) => {

      const texto =
        linha.trim();

      if (texto.startsWith("# ")) {
        return false;
      }

      if (texto.startsWith("## ")) {
        return false;
      }

      if (texto.startsWith("Fonte:")) {
        return false;
      }

      if (texto.startsWith("URL:")) {
        return false;
      }

      if (texto.startsWith("Tema:")) {
        return false;
      }

      if (texto.startsWith("Subtema:")) {
        return false;
      }

      if (texto.startsWith("Data de acesso:")) {
        return false;
      }

      return true;
    })
    .join("\n")
    .trim();


    htmlEvidencias += `
      <div
        class="healthcheck-evidence ${evidenciaExtra ? "healthcheck-evidence-extra" : ""}"
        ${evidenciaExtra ? "hidden" : ""}
      >

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
          ${escaparHTML(conteudoLimpo)}
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

if (evidencias.length > 3) {
  htmlEvidencias += `
    <button
      class="healthcheck-show-evidences"
      type="button"
      aria-expanded="false"
    >
      Ver todas as evidências (${evidencias.length})
    </button>
  `;
}

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


      <div class="healthcheck-critical-intro">

        <p>
          ${escaparHTML(configuracao.mensagem)}
        </p>

      </div>


      <hr>


      <section class="healthcheck-section">

        <h4>
          🔍 POR QUE O SISTEMA CLASSIFICOU ASSIM?
        </h4>

        <p>
          ${escaparHTML(explicacao)}
        </p>

      </section>


      <hr>


      <section class="healthcheck-section">

        <h4>
          📚 EVIDÊNCIAS UTILIZADAS
        </h4>

        ${htmlEvidencias}

        <p>
          <small>
            ℹ Similaridade representa o quanto o trecho
            recuperado está relacionado semanticamente
            à afirmação analisada. Não representa
            probabilidade de a informação ser verdadeira.
          </small>
        </p>

      </section>


      <hr>


      <section class="healthcheck-section healthcheck-share">

        <h4>
          💭 ANTES DE COMPARTILHAR
        </h4>

        <p>
          ${escaparHTML(configuracao.compartilhar)}
        </p>

      </section>


      <hr>


      <section class="healthcheck-section healthcheck-ai-notice">

        <h4>
          🤖 ANÁLISE ASSISTIDA POR IA
        </h4>

        <p>
          Esta análise foi gerada com auxílio de
          Inteligência Artificial a partir das evidências
          disponíveis na base do HealthCheck IA.
        </p>

        <p>
          A IA pode cometer erros. Confira as evidências
          e consulte as fontes originais antes de tomar
          uma decisão.
        </p>

      </section>

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

const botaoEvidencias =
  card.querySelector(
    ".healthcheck-show-evidences"
  );


if (botaoEvidencias) {

  botaoEvidencias.addEventListener(
    "click",
    () => {

      const extras =
        card.querySelectorAll(
          ".healthcheck-evidence-extra"
        );

      const estaAberto =
        botaoEvidencias.getAttribute(
          "aria-expanded"
        ) === "true";


      extras.forEach(
        (evidencia) => {

          evidencia.hidden =
            estaAberto;

        }
      );


      botaoEvidencias.setAttribute(
        "aria-expanded",
        String(!estaAberto)
      );


      botaoEvidencias.innerText =
        estaAberto
          ? `Ver todas as evidências (${evidencias.length})`
          : "Mostrar menos evidências";

    }
  );
}

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