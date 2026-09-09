function capturarResultados() {
  const resultados = document.querySelectorAll("div.MjjYud");

  const dados = [];

  resultados.forEach((resultado, index) => {
    const tituloElemento = resultado.querySelector("h3");
    const linkElemento = tituloElemento?.closest("a");

    // Alguns resultados podem não ter descrição
    const descricaoElemento =
      resultado.querySelector(".VwiC3b") ||
      resultado.querySelector("[data-sncf]");

    if (!tituloElemento || !linkElemento) {
      return;
    }

    const item = {
      titulo: tituloElemento.innerText.trim(),
      url: linkElemento.href,
      descricao: descricaoElemento
        ? descricaoElemento.innerText.trim()
        : "Descrição não encontrada"
    };

    dados.push(item);

    console.log(`Resultado ${dados.length}`);
    console.log("Título:", item.titulo);
    console.log("URL:", item.url);
    console.log("Descrição:", item.descricao);
    console.log("-----------------------------");
  });

  console.log("Todos os resultados capturados:");
  console.log(dados);

  return dados;
}

capturarResultados();