function getQueryParam(name) {
  const url = new URL(window.location.href);
  return url.searchParams.get(name);
}

const id = getQueryParam("id");

fetch("roteiros.json")
  .then(res => res.json())
  .then(data => {
    const r = data[id];
    if (!r) {
      document.body.innerHTML = "<h1>Roteiro não encontrado</h1>";
      return;
    }

    document.querySelector("#imgRoteiro").src = `assets/img/${r.img}`;
    document.querySelector("#titulo").innerText = r.title;
    document.querySelector("#empresa").innerText = r.empresa;
    document.querySelector("#diretor").innerText = r.director;
    document.querySelector("#periodo").innerText = `${r.start} a ${r.end}`;
    document.querySelector("#preco").innerText = r.preco;

    // Itinerário
    document.querySelector("#itinerario").innerHTML =
      Array.isArray(r.itinerario)
        ? r.itinerario.map(i => `<li>${i}</li>`).join("")
        : Object.values(r.itinerario).map(i => `<li>${i}</li>`).join("");

    // Incluso
    document.querySelector("#incluso").innerHTML =
      r.incluso.map(i => `<li>${i}</li>`).join("");

    // Não incluso
    document.querySelector("#naoIncluso").innerHTML =
      r.nao_incluso.map(i => `<li>${i}</li>`).join("");
  });
