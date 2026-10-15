import { apiPost, salvarToken } from "./api.js";
import { initTheme } from "./theme.js";

document.addEventListener("DOMContentLoaded", () => {
  initTheme(null);

  const form = document.getElementById("login-form");
  const erroEl = document.getElementById("login-erro");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    erroEl.style.display = "none";

    const email = document.getElementById("login-email").value.trim();
    const senha = document.getElementById("login-senha").value;
    const botao = form.querySelector("button[type=submit]");

    botao.disabled = true;
    botao.textContent = "Entrando...";
    try {
      const resultado = await apiPost("/api/auth/login", { email, senha });
      salvarToken(resultado.access_token);
      window.location.href = "painel.html";
    } catch (erro) {
      erroEl.textContent = "E-mail ou senha incorretos. Confira e tente novamente.";
      erroEl.style.display = "block";
      botao.disabled = false;
      botao.textContent = "Entrar";
    }
  });
});
