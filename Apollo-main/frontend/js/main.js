import {
  renderAvisos,
  renderDisciplinas,
  renderTarefas,
  renderOpcoesDisciplina,
  renderStatusTarefas,
  renderEventos,
  renderNotas,
  renderProgressList,
  renderBiblioteca,
  renderContatos,
  renderMensagens,
  renderCabecalhoChat,
  renderUsuario,
} from "./render-cards.js";
import { initNavigation } from "./navigation.js";
import { initCalendar } from "./calendar.js";
import {
  initTabs,
  initContactSelection,
  initFavoriteToggle,
  initViewToggle,
  initEntregarTarefa,
  initEnviarMensagem,
  initLogout,
} from "./ui-interactions.js";
import { initPasswordRecovery } from "./auth.js";
import { initTheme } from "./theme.js";
import { apiGet, apiPatch, apiPost, getToken, limparToken } from "./api.js";

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("avisos-container")) {
    if (!getToken()) {
      window.location.href = "login.html";
    } else {
      renderPainel();
    }
  }
  initNavigation();
  initTabs();
  initPasswordRecovery();
  initTheme(document.getElementById("theme-toggle"));
  initLogout(document.getElementById("user-chip"), () => {
    limparToken();
    window.location.href = "login.html";
  });
});

async function renderPainel() {
  const tarefasEl = document.getElementById("tarefas-container");
  const statusTarefasEl = document.getElementById("status-tarefas-container");
  const filtroDisciplinaEl = document.getElementById("filtro-disciplina");
  const contatosEl = document.getElementById("contatos-container");
  const mensagensEl = document.getElementById("chat-messages-container");
  const chatElementos = {
    avatarEl: document.getElementById("chat-avatar"),
    nomeEl: document.getElementById("chat-name"),
    statusEl: document.getElementById("chat-status"),
  };

  renderCabecalhoChat(null, chatElementos);
  renderMensagens([], mensagensEl);

  let conversaAtualId = null;

  const [usuario, avisos, disciplinas, tarefasIniciais, eventosHoje, eventosProximos, eventosCalendario, notas, progresso, frequencia, biblioteca, contatos] =
    await Promise.all([
      apiGet("/api/usuario/atual"),
      apiGet("/api/avisos"),
      apiGet("/api/disciplinas"),
      apiGet("/api/tarefas"),
      apiGet("/api/eventos/hoje"),
      apiGet("/api/eventos/proximos"),
      apiGet("/api/eventos/calendario"),
      apiGet("/api/notas"),
      apiGet("/api/progresso-disciplinas"),
      apiGet("/api/frequencia-disciplinas"),
      apiGet("/api/biblioteca"),
      apiGet("/api/contatos"),
    ]);

  renderUsuario(usuario, {
    avatarEl: document.getElementById("user-avatar"),
    nomeEl: document.getElementById("user-name"),
    papelEl: document.getElementById("user-role"),
  });
  renderAvisos(avisos, document.getElementById("avisos-container"));
  renderDisciplinas(disciplinas, document.getElementById("disciplinas-container"));
  renderEventos(eventosHoje, document.getElementById("eventos-hoje-container"));
  renderEventos(eventosProximos, document.getElementById("eventos-proximos-container"));
  renderNotas(notas, document.getElementById("notas-container"));
  renderProgressList(progresso, document.getElementById("progresso-disciplinas-container"));
  renderProgressList(frequencia, document.getElementById("frequencia-disciplinas-container"), { fina: true });
  renderBiblioteca(biblioteca, document.getElementById("biblioteca-container"));
  renderContatos(contatos, contatosEl);
  initCalendar(document.querySelector(".cal-card"), eventosCalendario);

  let tarefas = tarefasIniciais;
  function renderTarefasFiltradas() {
    const disciplina = filtroDisciplinaEl.value;
    const filtradas = disciplina ? tarefas.filter((t) => t.disciplina === disciplina) : tarefas;
    renderTarefas(filtradas, tarefasEl);
    renderStatusTarefas(filtradas, statusTarefasEl);
  }
  renderOpcoesDisciplina(tarefas, filtroDisciplinaEl);
  renderTarefasFiltradas();
  filtroDisciplinaEl?.addEventListener("change", renderTarefasFiltradas);
  initViewToggle(document.getElementById("tarefas-view-grid"), document.getElementById("tarefas-view-list"), tarefasEl);
  initEntregarTarefa(tarefasEl, async (tarefaId) => {
    await apiPatch(`/api/tarefas/${tarefaId}/status`, { status: "entregue" });
    tarefas = await apiGet("/api/tarefas");
    renderOpcoesDisciplina(tarefas, filtroDisciplinaEl);
    renderTarefasFiltradas();
  });

  initContactSelection(contatosEl, async (contatoId) => {
    conversaAtualId = contatoId;
    const contato = contatos.find((c) => c.id === contatoId);
    renderCabecalhoChat(contato, chatElementos);
    renderMensagens(await apiGet(`/api/mensagens/${contatoId}`), mensagensEl);
  });
  initEnviarMensagem(document.getElementById("chat-input-form"), document.getElementById("chat-input-field"), async (texto) => {
    if (!conversaAtualId) return;
    await apiPost(`/api/mensagens/${conversaAtualId}`, { texto });
    renderMensagens(await apiGet(`/api/mensagens/${conversaAtualId}`), mensagensEl);
  });

  initFavoriteToggle(document.getElementById("biblioteca-container"), (materialId, novoFavorito) => {
    apiPatch(`/api/biblioteca/${materialId}/favorito`, { favorito: novoFavorito });
  });
}
