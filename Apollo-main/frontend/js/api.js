const CHAVE_TOKEN = "apollo_token";

export function salvarToken(token) {
  sessionStorage.setItem(CHAVE_TOKEN, token);
}

export function limparToken() {
  sessionStorage.removeItem(CHAVE_TOKEN);
}

export function getToken() {
  return sessionStorage.getItem(CHAVE_TOKEN);
}

async function apiFetch(caminho, opcoes = {}) {
  const token = getToken();
  const resposta = await fetch(caminho, {
    ...opcoes,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(opcoes.headers || {}),
    },
  });

  const ehLogin = caminho.startsWith("/api/auth/");
  if (resposta.status === 401 && !ehLogin) {
    limparToken();
    window.location.href = "login.html";
    throw new Error("Sessão expirada ou inválida");
  }
  return resposta;
}

export async function apiGet(caminho) {
  const resposta = await apiFetch(caminho);
  if (!resposta.ok) throw new Error(`GET ${caminho} falhou (${resposta.status})`);
  return resposta.json();
}

export async function apiPost(caminho, corpo) {
  const resposta = await apiFetch(caminho, { method: "POST", body: JSON.stringify(corpo) });
  if (!resposta.ok) throw new Error(`POST ${caminho} falhou (${resposta.status})`);
  return resposta.json();
}

export async function apiPatch(caminho, corpo) {
  const resposta = await apiFetch(caminho, { method: "PATCH", body: JSON.stringify(corpo) });
  if (!resposta.ok) throw new Error(`PATCH ${caminho} falhou (${resposta.status})`);
  return resposta;
}
