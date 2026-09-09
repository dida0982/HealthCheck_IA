function capturarResultados() {
  const resultados = document.querySelectorAll("div.MjjYud");

  resultados.forEach((resultado, index) => {
    const tituloElemento = resultado.querySelector("h3");
    const linkElemento = tituloElemento?.closest("a");

    const descricaoElemento =
      resultado.querySelector(".VwiC3b") ||
      resultado.querySelector("[data-sncf]");

    if (!tituloElemento || !linkElemento) {
      return;
    }

    // Evita inserir o componente duas vezes
    if (resultado.querySelector(".healthcheck-card")) {
      return;
    }

    const item = {
      titulo: tituloElemento.innerText.trim(),
      url: linkElemento.href,
      descricao: descricaoElemento
        ? descricaoElemento.innerText.trim()
        : "Descrição não encontrada"
    };

    criarComponenteHealthCheck(resultado, item, index);
  });
}


function criarComponenteHealthCheck(resultado, item, index) {
  const card = document.createElement("div");

  card.className = "healthcheck-card";

  /*
    Por enquanto os resultados são SIMULADOS.

    Alternamos entre verde e vermelho apenas para
    visualizar os dois tipos de componente.
  */

  const favoravel = index % 2 === 0;

  const status = favoravel
    ? "Evidências favoráveis"
    : "Evidências contraditórias";

  const classeStatus = favoravel
    ? "healthcheck-favoravel"
    : "healthcheck-contraditorio";

  const icone = favoravel ? "🟢" : "🔴";

  const confianca = favoravel ? 85 : 82;

  card.innerHTML = `
    <div class="healthcheck-header">

      <div class="healthcheck-status ${classeStatus}">
        <span>${icone}</span>
        <strong>${status}</strong>
      </div>

      <div class="healthcheck-confidence">
        Confiança: ${confianca}%
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
        Esta análise é apenas uma simulação visual.
        A Inteligência Artificial ainda não está conectada.
      </p>

      <p>
        <strong>Título analisado:</strong>
        ${item.titulo}
      </p>

      <p>
        <strong>Fonte:</strong>
        ${new URL(item.url).hostname}
      </p>

    </div>
  `;

  resultado.appendChild(card);

  const botao = card.querySelector(".healthcheck-button");
  const detalhes = card.querySelector(".healthcheck-details");

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


function iniciarHealthCheck() {
  capturarResultados();
}


iniciarHealthCheck();


const observer = new MutationObserver(() => {
  capturarResultados();
});


observer.observe(document.body, {
  childList: true,
  subtree: true
});