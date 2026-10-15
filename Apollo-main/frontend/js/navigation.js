export function initNavigation() {
  const links = document.querySelectorAll(".nav-link");
  const screens = document.querySelectorAll(".screen");
  if (!links.length) return;

  links.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      links.forEach((l) => l.classList.remove("active"));
      screens.forEach((s) => s.classList.remove("active"));
      link.classList.add("active");

      const alvo = document.getElementById(link.dataset.screen);
      if (alvo) alvo.classList.add("active");
    });
  });
}
