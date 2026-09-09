function adicionarHealthCheck() {
  const resultados = document.querySelectorAll("div.MjjYud");

  resultados.forEach((resultado) => {
    if (resultado.querySelector(".healthcheck-box")) {
      return;
    }

    const titulo = resultado.querySelector("h3");

    if (!titulo) {
      return;
    }

    const caixa = document.createElement("div");

    caixa.className = "healthcheck-box";
    caixa.innerHTML = `
      <strong>🔎 HealthCheck IA</strong>
      <span>Aguardando análise</span>
    `;

    resultado.appendChild(caixa);
  });
}

adicionarHealthCheck();

const observer = new MutationObserver(() => {
  adicionarHealthCheck();
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});