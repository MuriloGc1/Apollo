const NOMES_MES = [
  "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
];
const NOMES_DIA_SEMANA = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"];

export function initCalendar(cardEl, eventos = []) {
  if (!cardEl) return;

  const mesEl = cardEl.querySelector(".cal-month");
  const gridEl = cardEl.querySelector(".cal-grid");
  const btnPrev = cardEl.querySelector('[data-cal-nav="prev"]');
  const btnNext = cardEl.querySelector('[data-cal-nav="next"]');

  const hoje = new Date();
  let mesAtual = hoje.getMonth();
  let anoAtual = hoje.getFullYear();

  function temEvento(dia, mes, ano) {
    return eventos.some((e) => e.dia === dia && e.mes === mes && e.ano === ano);
  }

  function render() {
    mesEl.textContent = `${NOMES_MES[mesAtual]} ${anoAtual}`;
    gridEl.innerHTML = "";

    NOMES_DIA_SEMANA.forEach((nome) => {
      const el = document.createElement("div");
      el.className = "cal-day-name";
      el.textContent = nome;
      gridEl.appendChild(el);
    });

    const primeiroDiaSemana = new Date(anoAtual, mesAtual, 1).getDay();
    const totalDias = new Date(anoAtual, mesAtual + 1, 0).getDate();

    for (let i = 0; i < primeiroDiaSemana; i++) {
      const el = document.createElement("div");
      el.className = "cal-day empty";
      gridEl.appendChild(el);
    }

    for (let dia = 1; dia <= totalDias; dia++) {
      const el = document.createElement("div");
      el.className = "cal-day";
      el.textContent = dia;

      const ehHoje = dia === hoje.getDate() && mesAtual === hoje.getMonth() && anoAtual === hoje.getFullYear();
      if (ehHoje) el.classList.add("today");
      if (temEvento(dia, mesAtual, anoAtual)) el.classList.add("has-event");

      gridEl.appendChild(el);
    }
  }

  btnPrev?.addEventListener("click", () => {
    mesAtual--;
    if (mesAtual < 0) {
      mesAtual = 11;
      anoAtual--;
    }
    render();
  });

  btnNext?.addEventListener("click", () => {
    mesAtual++;
    if (mesAtual > 11) {
      mesAtual = 0;
      anoAtual++;
    }
    render();
  });

  render();
}
