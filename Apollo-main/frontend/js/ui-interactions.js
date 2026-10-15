function initTabGroup(tabSelector, groupSelector) {
  document.querySelectorAll(tabSelector).forEach((tab) => {
    tab.addEventListener("click", () => {
      tab
        .closest(groupSelector)
        .querySelectorAll(tabSelector)
        .forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
    });
  });
}

export function initTabs() {
  initTabGroup(".tab", ".tabs");
  initTabGroup(".ctab", ".contacts-tabs");
}

export function initContactSelection(listContainer, onSelecionar) {
  if (!listContainer) return;
  listContainer.addEventListener("click", (e) => {
    const item = e.target.closest(".contact-item");
    if (!item) return;
    listContainer.querySelectorAll(".contact-item").forEach((i) => i.classList.remove("active"));
    item.classList.add("active");
    onSelecionar?.(item.dataset.contatoId);
  });
}

export function initFavoriteToggle(gridContainer, onAlternar) {
  if (!gridContainer) return;
  gridContainer.addEventListener("click", (e) => {
    const btn = e.target.closest(".btn-fav");
    if (!btn) return;
    const card = btn.closest("[data-material-id]");
    const jaFavoritado = btn.textContent.trim() === "★";
    const novoFavorito = !jaFavoritado;
    btn.textContent = novoFavorito ? "★" : "☆";
    btn.classList.toggle("active", novoFavorito);
    if (card) onAlternar?.(card.dataset.materialId, novoFavorito);
  });
}

export function initEntregarTarefa(container, onEntregar) {
  if (!container) return;
  container.addEventListener("click", (e) => {
    const btn = e.target.closest(".btn-entregar:not(.btn-entregar--disabled)");
    if (!btn) return;
    const card = btn.closest("[data-tarefa-id]");
    if (card) onEntregar?.(card.dataset.tarefaId);
  });
}

export function initEnviarMensagem(formEl, inputEl, onEnviar) {
  if (!formEl || !inputEl) return;
  formEl.addEventListener("submit", async (e) => {
    e.preventDefault();
    const texto = inputEl.value.trim();
    if (!texto) return;
    await onEnviar?.(texto);
    inputEl.value = "";
    inputEl.focus();
  });
}

export function initLogout(chipEl, onLogout) {
  if (!chipEl) return;
  chipEl.addEventListener("click", () => onLogout?.());
}

export function initViewToggle(btnGrade, btnLista, container) {
  if (!btnGrade || !btnLista || !container) return;

  function setView(visualizacaoGrade) {
    container.classList.toggle("tarefas-grid", visualizacaoGrade);
    btnGrade.classList.toggle("hbtn--active", visualizacaoGrade);
    btnGrade.classList.toggle("hbtn--muted", !visualizacaoGrade);
    btnLista.classList.toggle("hbtn--active", !visualizacaoGrade);
    btnLista.classList.toggle("hbtn--muted", visualizacaoGrade);
  }

  btnGrade.addEventListener("click", () => setView(true));
  btnLista.addEventListener("click", () => setView(false));
}
