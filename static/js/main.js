fetch("roteiros.json")
  .then(res => res.json())
  .then(data => {
    const container = document.querySelector("#listaRoteiros");
    Object.values(data).forEach(r => {
      container.innerHTML += `
        <div class="card">
          <img src="assets/img/${r.img}" alt="${r.title}">
          <h3>${r.title}</h3>
          <p>${r.start} a ${r.end}</p>
          <a href="roteiro.html?id=${r.id}">Ver roteiro</a>
        </div>
      `;
    });
  });
