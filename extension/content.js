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
      throw new Error(`Erro HTTP: ${resposta.status}`);
    }

    const dados = await resposta.json();

    console.log("Resposta do backend:", dados);

    return dados;

  } catch (erro) {
    console.error("Erro ao conectar com o backend:", erro);

    return null;
  }
}


async function capturarResultados() {
  const resultados = document.querySelectorAll("div.MjjYud");

  for (const resultado of resultados) {

    const tituloElemento = resultado.querySelector("h3");
    const linkElemento = tituloElemento?.closest("a");

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
      titulo: tituloElemento.innerText.trim(),

      url: linkElemento.href,

      descricao: descricaoElemento
        ? descricaoElemento.innerText.trim()
        : "Descrição não encontrada"
    };

    criarComponenteHealthCheck(resultado, item);
  }
}


async function criarComponenteHealthCheck(resultado, item) {

  const card = document.createElement("div");

  card.className = "healthcheck-card";

  /*
    Primeiro mostramos o estado de carregamento.
  */

  card.innerHTML = `
    <div class="healthcheck-header">

      <div class="healthcheck-status">
        <span>🔎</span>

        <strong>
          HealthCheck IA
        </strong>
      </div>

      <div class="healthcheck-confidence">
        Analisando...
      </div>

    </div>

    <div class="healthcheck-loading">
      Consultando o backend...
    </div>
  `;

  resultado.appendChild(card);


  /*
    Agora enviamos o conteúdo para o FastAPI.
  */

  const analise = await analisarResultado(item);


  /*
    Caso não seja possível conectar ao backend.
  */

  if (!analise) {

    card.innerHTML = `
      <div class="healthcheck-header">

        <div class="healthcheck-status healthcheck-erro">
          <span>⚠️</span>

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
    Por enquanto nosso backend sempre retorna:

    {
      classificacao: "enganosa",
      confianca: 0.82
    }

    Portanto ainda é uma resposta simulada.
  */


  const classificacao = analise.classificacao;

  const confianca = Math.round(
    analise.confianca * 100
  );


  let status;
  let icone;
  let classeStatus;


  if (classificacao === "enganosa") {

    status = "Evidências contraditórias";

    icone = "🔴";

    classeStatus = "healthcheck-contraditorio";

  } else {

    status = "Resultado recebido";

    icone = "🟡";

    classeStatus = "";
  }


  card.innerHTML = `
    <div class="healthcheck-header">

      <div class="healthcheck-status ${classeStatus}">

        <span>
          ${icone}
        </span>

        <strong>
          ${status}
        </strong>

      </div>

      <div class="healthcheck-confidence">

        Confiança:
        ${confianca}%

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
          Classificação recebida do backend:
        </strong>

        ${classificacao}

      </p>


      <p>

        <strong>
          Título analisado:
        </strong>

        ${item.titulo}

      </p>


      <p>

        <strong>
          Fonte:
        </strong>

        ${new URL(item.url).hostname}

      </p>


      <p class="healthcheck-warning">

        Esta classificação ainda é simulada.
        A Inteligência Artificial ainda não foi implementada.

      </p>

    </div>
  `;


  const botao =
    card.querySelector(".healthcheck-button");

  const detalhes =
    card.querySelector(".healthcheck-details");


  botao.addEventListener("click", () => {

    const estaAberto =
      botao.getAttribute("aria-expanded") === "true";


    botao.setAttribute(
      "aria-expanded",
      String(!estaAberto)
    );


    detalhes.hidden = estaAberto;


    botao.innerText = estaAberto
      ? "Ver análise"
      : "Ocultar análise";

  });
}



capturarResultados();


const observer = new MutationObserver(() => {

  capturarResultados();

});


observer.observe(
  document.body,
  {
    childList: true,
    subtree: true
  }
);