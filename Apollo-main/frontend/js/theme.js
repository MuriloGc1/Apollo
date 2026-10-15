const CHAVE_STORAGE = "apollo-tema";

export function initTheme(botao) {
  const salvo = localStorage.getItem(CHAVE_STORAGE);
  aplicar(salvo === "escuro");
  atualizarIcone(botao, salvo === "escuro");

  botao?.addEventListener("click", () => {
    const estaEscuro = document.documentElement.dataset.theme === "dark";
    aplicar(!estaEscuro);
    localStorage.setItem(CHAVE_STORAGE, !estaEscuro ? "escuro" : "claro");
    atualizarIcone(botao, !estaEscuro);
  });
}

function aplicar(escuro) {
  document.documentElement.dataset.theme = escuro ? "dark" : "light";
}

function atualizarIcone(botao, escuro) {
  const icone = botao?.querySelector("i");
  if (!icone) return;
  icone.className = escuro ? "fa-solid fa-sun" : "fa-solid fa-moon";
}
