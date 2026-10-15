import { apiPost } from "./api.js";

export function initPasswordRecovery() {
  const form = document.getElementById("recover-form");
  if (!form) return;

  const stepForm = document.getElementById("step-form");
  const stepSuccess = document.getElementById("step-success");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email-recover").value.trim();
    const botao = form.querySelector("button[type=submit]");

    botao.disabled = true;
    try {
      await apiPost("/api/auth/recuperar-senha", { email });
    } catch {}
    stepForm.style.display = "none";
    stepSuccess.style.display = "block";
  });
}
