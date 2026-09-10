const buttons = document.querySelectorAll("[data-lang]");
const header = document.querySelector(".site-header");
const menuToggle = header?.querySelector(".menu-toggle");
const menu = header?.querySelector(".burger-menu");
const menuBackdrop = header?.querySelector("[data-menu-close]");

function setMenuOpen(open) {
  if (!header || !menuToggle || !menu) return;
  const isEnglish = document.documentElement.lang === "en";
  header.classList.toggle("is-menu-open", open);
  document.body.classList.toggle("menu-open", open);
  menuToggle.setAttribute("aria-expanded", String(open));
  menuToggle.setAttribute("aria-label", open
    ? (isEnglish ? "Close menu" : "Закрыть меню")
    : (isEnglish ? "Open menu" : "Открыть меню"));
  menu.setAttribute("aria-hidden", String(!open));
}

function setLanguage(language) {
  const lang = language === "en" ? "en" : "ru";
  const rootPrefix = window.location.pathname.includes("/en/") ? "../" : "";
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-cv-link]").forEach(link => {
    link.href = rootPrefix + "cv/Roman_Mironichev_Product_Marketing_Operations_" + lang.toUpperCase() + "_2026.pdf";
  });
  document.querySelectorAll("[data-media-link]").forEach(link => {
    link.href = rootPrefix + (lang === "en" ? "media/en/" : "media/");
  });
  document.title = lang === "ru"
    ? (document.body.classList.contains("projects-page") ? "Проекты — MironLab" : "Miron Lab — Product & Operations")
    : (document.body.classList.contains("projects-page") ? "Projects — MironLab" : "Miron Lab — Product & Operations");

  document.querySelectorAll("[data-ru][data-en]").forEach((element) => {
    element.textContent = element.dataset[lang];
  });
  document.querySelectorAll("[data-alt-ru][data-alt-en]").forEach((element) => {
    element.alt = element.dataset[`alt${lang[0].toUpperCase()}${lang.slice(1)}`];
  });
  buttons.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.lang === lang)));
  try { localStorage.setItem("mironlab-jump-language", lang); } catch {}
  setMenuOpen(false);
}

buttons.forEach((button) => button.addEventListener("click", () => setLanguage(button.dataset.lang)));
let savedLanguage = window.location.pathname.includes("/en/") ? "en" : "ru";
try { savedLanguage = localStorage.getItem("mironlab-jump-language") || "ru"; } catch {}
if (window.location.pathname.includes("/en/")) savedLanguage = "en";
setLanguage(savedLanguage);

menuToggle?.addEventListener("click", () => {
  setMenuOpen(!header.classList.contains("is-menu-open"));
});
menuBackdrop?.addEventListener("click", () => setMenuOpen(false));
menu?.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => setMenuOpen(false)));
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") setMenuOpen(false);
});

const observer = "IntersectionObserver" in window
  ? new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 })
  : null;

document.querySelectorAll(".reveal").forEach((element) => {
  if (observer) observer.observe(element);
  else element.classList.add("is-visible");
});
