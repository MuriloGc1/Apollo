function escapeHTML(texto) {
  const div = document.createElement("div");
  div.textContent = texto ?? "";
  return div.innerHTML;
}

function criarElemento(html) {
  const template = document.createElement("template");
  template.innerHTML = html.trim();
  return template.content.firstElementChild;
}

function renderVazio(container, mensagem, icone = "fa-solid fa-inbox") {
  container.appendChild(
    criarElemento(`
      <div class="empty-state">
        <i class="${icone}"></i>
        <p>${escapeHTML(mensagem)}</p>
      </div>
    `)
  );
}

export function renderAvisos(dados, container) {
  container.innerHTML = "";
  if (!dados || dados.length === 0) {
    renderVazio(container, "Nenhum aviso no momento", "fa-solid fa-bell-slash");
    return;
  }
  dados.forEach((aviso) => {
    container.appendChild(
      criarElemento(`
        <div class="card aviso-card">
          <div class="aviso-icon"><i class="${aviso.icone}"></i></div>
          <div class="aviso-date">${escapeHTML(aviso.data)}</div>
          <div class="aviso-title">${escapeHTML(aviso.titulo)}</div>
        </div>
      `)
    );
  });
}

export function renderDisciplinas(dados, container) {
  container.innerHTML = "";
  if (!dados || dados.length === 0) {
    renderVazio(container, "Nenhuma disciplina cadastrada ainda", "fa-solid fa-graduation-cap");
    return;
  }
  dados.forEach((d) => {
    const avatarStyle = d.corAvatar ? ` style="background:${d.corAvatar}"` : "";
    const fillStyle = d.corProgresso ? ` background:${d.corProgresso};` : "";
    container.appendChild(
      criarElemento(`
        <div class="card disc-card">
          <div class="disc-header">
            <div class="disc-name">${escapeHTML(d.nome)}</div>
            <div class="disc-prof">
              <div class="prof-avatar"${avatarStyle}>${escapeHTML(d.iniciais)}</div>
              ${escapeHTML(d.professor)}
            </div>
          </div>
          <div class="disc-stats">
            <div class="stat-item stat-${d.statusMedia}"><div class="stat-val">${escapeHTML(d.media)}</div><div class="stat-lbl">Média</div></div>
            <div class="stat-item stat-${d.statusFaltas}"><div class="stat-val">${d.faltas}</div><div class="stat-lbl">Faltas</div></div>
            <div class="stat-item stat-${d.statusFrequencia}"><div class="stat-val">${escapeHTML(d.frequencia)}</div><div class="stat-lbl">Frequência</div></div>
          </div>
          <div class="disc-progress">
            <div class="prog-label"><span>Progresso</span><span>${d.progresso}%</span></div>
            <div class="prog-bar"><div class="prog-fill" style="width:${d.progresso}%;${fillStyle}"></div></div>
          </div>
          <button class="btn-acessar">Acessar</button>
        </div>
      `)
    );
  });
}

const STATUS_TAREFA = {
  expirado: { label: "Expirado", icone: "fa-solid fa-triangle-exclamation", classe: "s-red", dataClasse: "vencida", dataIcone: "fa-regular fa-calendar-xmark", botaoTexto: "Visualizar", botaoClasse: "btn-entregar btn-entregar--disabled" },
  pendente: { label: "Pendente", icone: "fa-solid fa-clock", classe: "s-yellow", dataClasse: "pend", dataIcone: "fa-regular fa-calendar", botaoTexto: "Entregar", botaoClasse: "btn-entregar" },
  entregue: { label: "Entregue", icone: "fa-solid fa-circle-check", classe: "s-green", dataClasse: "ok", dataIcone: "fa-solid fa-circle-check", botaoTexto: "Visualizar", botaoClasse: "btn-vis" },
};

export function renderTarefas(dados, container) {
  container.innerHTML = "";
  if (!dados || dados.length === 0) {
    renderVazio(container, "Nenhuma tarefa por aqui", "fa-solid fa-list-check");
    return;
  }
  dados.forEach((t) => {
    const cfg = STATUS_TAREFA[t.status];
    container.appendChild(
      criarElemento(`
        <div class="card tarefa-card" data-tarefa-id="${t.id}">
          <div class="tarefa-top">
            <div class="tarefa-disc">${escapeHTML(t.disciplina)}</div>
            <div class="tarefa-status ${cfg.classe}"><i class="${cfg.icone}"></i> ${cfg.label}</div>
          </div>
          <div class="tarefa-desc">${escapeHTML(t.descricao)}</div>
          <div class="tarefa-footer">
            <div class="tarefa-data ${cfg.dataClasse}"><i class="${cfg.dataIcone}"></i> ${escapeHTML(t.dataLabel)}</div>
            <button class="${cfg.botaoClasse}">${cfg.botaoTexto}</button>
          </div>
        </div>
      `)
    );
  });
}

export function renderOpcoesDisciplina(dadosTarefas, selectEl) {
  if (!selectEl) return;
  const valorSelecionado = selectEl.value;
  const nomes = [...new Set(dadosTarefas.map((t) => t.disciplina))].sort((a, b) => a.localeCompare(b, "pt-BR"));

  selectEl.innerHTML = `<option value="">Todas as disciplinas</option>`;
  nomes.forEach((nome) => {
    selectEl.appendChild(criarElemento(`<option value="${escapeHTML(nome)}">${escapeHTML(nome)}</option>`));
  });

  if (nomes.includes(valorSelecionado)) selectEl.value = valorSelecionado;
}

export function renderStatusTarefas(dados, container) {
  container.innerHTML = "";
  const contagem = { expirado: 0, pendente: 0, entregue: 0 };
  dados.forEach((t) => contagem[t.status]++);
  const corPorStatus = { expirado: "red", pendente: "yellow", entregue: "green" };

  Object.keys(STATUS_TAREFA).forEach((status) => {
    const cfg = STATUS_TAREFA[status];
    const cor = corPorStatus[status];
    container.appendChild(
      criarElemento(`
        <div class="status-row">
          <div class="status-left f-${cor}"><i class="${cfg.icone}"></i> ${cfg.label}</div>
          <div class="status-count ${cor}-val">${contagem[status]}</div>
        </div>
      `)
    );
  });
}

export function renderEventos(dados, container) {
  container.innerHTML = "";
  if (!dados || dados.length === 0) {
    renderVazio(container, "Nenhum evento por aqui", "fa-regular fa-calendar");
    return;
  }
  dados.forEach((ev) => {
    container.appendChild(
      criarElemento(`
        <div class="event-item">
          <div class="event-dot" style="background:${ev.cor}"></div>
          <div>
            <div class="event-time">${escapeHTML(ev.hora)}</div>
            <div class="event-name">${escapeHTML(ev.nome)}</div>
          </div>
        </div>
      `)
    );
  });
}

export function renderNotas(dados, container) {
  container.innerHTML = "";
  if (!dados || dados.length === 0) {
    renderVazio(container, "Nenhuma nota lançada ainda", "fa-solid fa-chart-bar");
    return;
  }
  dados.forEach((n) => {
    const statusAv1 = n.statusAv1 || n.statusValores;
    const statusAv2 = n.statusAv2 || n.statusValores;
    const statusAv3 = n.statusAv3 || n.statusValores;
    container.appendChild(
      criarElemento(`
        <div class="nt-row">
          <div class="nt-disc"><div class="disc-dot" style="background:${n.corDot}"></div>${escapeHTML(n.disciplina)}</div>
          <div class="nt-prof">${escapeHTML(n.professor)}</div>
          <div class="nt-val ${n.statusFaltas}-val">${n.faltas}</div>
          <div class="nt-val ${statusAv1}-val">${n.av1}</div>
          <div class="nt-val ${statusAv2}-val">${n.av2}</div>
          <div class="nt-val ${statusAv3}-val">${n.av3}</div>
          <div class="nt-total ${n.statusTotal}-val">${n.total}</div>
        </div>
      `)
    );
  });
}

export function renderProgressList(dados, container, { fina = false } = {}) {
  container.innerHTML = "";
  if (!dados || dados.length === 0) {
    renderVazio(container, "Sem dados para exibir ainda", "fa-solid fa-chart-simple");
    return;
  }
  dados.forEach((item) => {
    const classeBarra = fina ? "prog-bar prog-bar--thin" : "prog-bar";
    const fillStyle = item.cor ? ` style="width:${item.pct}%;background:${item.cor}"` : ` style="width:${item.pct}%"`;
    container.appendChild(
      criarElemento(`
        <div class="prog-item">
          <div class="prog-item-label"><span class="prog-item-name">${escapeHTML(item.nome)}</span><span class="prog-item-pct">${item.pct}%</span></div>
          <div class="${classeBarra}"><div class="prog-fill"${fillStyle}></div></div>
        </div>
      `)
    );
  });
}

export function renderBiblioteca(dados, container) {
  container.innerHTML = "";
  if (!dados || dados.length === 0) {
    renderVazio(container, "Nenhum material disponível ainda", "fa-solid fa-book-open");
    return;
  }
  dados.forEach((item) => {
    const tipos = item.tipos.map((t) => `<div class="bib-type"><i class="${t.icone}"></i>${escapeHTML(t.label)}</div>`).join("");
    container.appendChild(
      criarElemento(`
        <div class="card bib-card" data-material-id="${item.id}">
          <div class="bib-cover" style="background:linear-gradient(135deg, ${item.gradiente[0]}, ${item.gradiente[1]})"><span>${escapeHTML(item.sigla)}</span></div>
          <div class="bib-body">
            <div class="bib-sub">${escapeHTML(item.subtitulo)}</div>
            <div class="bib-name">${escapeHTML(item.nome)}</div>
            <div class="bib-prof">${escapeHTML(item.professor)}</div>
            <div class="bib-badge" style="background:${item.badge.bg};color:${item.badge.cor}">${escapeHTML(item.badge.texto)}</div>
            <div class="bib-types">${tipos}</div>
            <div class="bib-footer">
              <button class="btn-fav${item.favorito ? " active" : ""}">${item.favorito ? "★" : "☆"}</button>
              <button class="btn-ac">Acessar</button>
            </div>
          </div>
        </div>
      `)
    );
  });
}

export function renderContatos(dados, container) {
  container.innerHTML = "";
  if (!dados || dados.length === 0) {
    renderVazio(container, "Nenhuma conversa ainda", "fa-regular fa-comments");
    return;
  }
  dados.forEach((c) => {
    const avatarStyle = c.corBg ? ` style="background:${c.corBg};color:${c.corTexto}"` : "";
    container.appendChild(
      criarElemento(`
        <div class="contact-item${c.ativo ? " active" : ""}" data-contato-id="${escapeHTML(c.id)}">
          <div class="c-avatar"${avatarStyle}>${escapeHTML(c.iniciais)}</div>
          <div class="c-info">
            <div class="c-name">${escapeHTML(c.nome)}</div>
            <div class="c-date">${escapeHTML(c.info)}</div>
          </div>
          <div class="c-time">${escapeHTML(c.hora)}</div>
        </div>
      `)
    );
  });
}

export function renderMensagens(dados, container) {
  container.innerHTML = "";
  if (!dados || dados.length === 0) {
    renderVazio(container, "Nenhuma mensagem ainda. Diga oi!", "fa-regular fa-comment-dots");
    return;
  }
  dados.forEach((m) => {
    container.appendChild(
      criarElemento(`
        <div class="msg ${m.direcao === "sent" ? "sent" : "recv"}">
          <div class="bubble">${escapeHTML(m.texto)}</div>
          <div class="msg-time">${escapeHTML(m.hora)}</div>
        </div>
      `)
    );
  });
  container.scrollTop = container.scrollHeight;
}

export function renderCabecalhoChat(contato, elementos) {
  const { avatarEl, nomeEl, statusEl } = elementos;
  if (!contato) {
    avatarEl.textContent = "";
    avatarEl.removeAttribute("style");
    nomeEl.textContent = "Selecione uma conversa";
    statusEl.innerHTML = "";
    return;
  }
  avatarEl.textContent = contato.iniciais;
  avatarEl.style.background = contato.corBg || "";
  avatarEl.style.color = contato.corTexto || "";
  nomeEl.textContent = contato.nome;
  statusEl.innerHTML = `<div class="online-dot"></div>${escapeHTML(contato.info)}`;
}

const PAPEL_LABEL = { aluno: "Estudante", professor: "Professor", responsavel: "Responsável" };

export function renderUsuario(usuario, elementos) {
  const { avatarEl, nomeEl, papelEl } = elementos;
  if (!usuario) return;
  avatarEl.textContent = usuario.iniciais;
  nomeEl.textContent = `Olá! ${usuario.nome}`;
  papelEl.textContent = PAPEL_LABEL[usuario.papel] || usuario.papel;
}
