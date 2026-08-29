const translations = {
  ru: {
    title: "Роман Мироничев — персональная веб-страница",
    description: "Персональная веб-страница Романа Мироничева: управление IT-проектами, портфолио, услуги и контакты.",
    skip: "Перейти к содержанию",
    navExperience: "Услуги",
    navContact: "Контакты",
    heroTitle: "Miron Lab.",
    heroText: "Персональный сайт Романа Мироничева.",
    continue: "Продолжить знакомство ↓",
    photoAlt: "Роман Мироничев",
    aboutTitle: "Проекты и услуги",
    aboutText: "Мой опыт работы с IT-проектами начинается с 2008 года. Основные направления — разработка веб-сайтов и мобильных приложений, а также управление IT-командами. Я сопровождаю проекты от идеи и планирования до запуска.",
    portfolioLabel: "Проектирование и запуск",
    studioLabel: "Процессы и delivery",
    serviceBuildTitle: "Разработка веб-сайтов и мобильных приложений",
    serviceTeamsTitle: "Управление IT-командами",
    contactTitle: "Контакты",
    formName: "Ваше имя",
    formNamePlaceholder: "Как к вам обращаться?",
    formMessage: "Сообщение",
    formMessagePlaceholder: "Расскажите кратко о задаче",
    formSubmit: "Отправить сообщение",
    formNote: "Форма откроет письмо в вашем почтовом приложении. Данные не сохраняются на сайте.",
    mailSubject: "Сообщение с mironlab.ru",
    mailName: "Имя",
    mailEmail: "Email",
    mailMessage: "Сообщение"
  },
  en: {
    title: "Roman Mironichev — Personal Website",
    description: "Roman Mironichev's personal website: IT project management, portfolio, services and contacts.",
    skip: "Skip to content",
    navExperience: "Services",
    navContact: "Contact",
    heroTitle: "Miron Lab.",
    heroText: "Personal website of Roman Mironichev.",
    continue: "Continue ↓",
    photoAlt: "Roman Mironichev",
    aboutTitle: "Projects & Services",
    aboutText: "I have worked with IT projects since 2008. My core areas are website and mobile application development, as well as IT team management. I support projects from idea and planning through launch.",
    portfolioLabel: "Design and launch",
    studioLabel: "Processes and delivery",
    serviceBuildTitle: "Website & Mobile App Development",
    serviceTeamsTitle: "IT Team Management",
    contactTitle: "Contact",
    formName: "Your name",
    formNamePlaceholder: "How should I address you?",
    formMessage: "Message",
    formMessagePlaceholder: "Tell me briefly about your project",
    formSubmit: "Send message",
    formNote: "The form opens an email in your mail application. No data is stored on this website.",
    mailSubject: "Message from mironlab.ru",
    mailName: "Name",
    mailEmail: "Email",
    mailMessage: "Message"
  }
};

const languageButtons = document.querySelectorAll("[data-lang]");

function setLanguage(language, updateUrl = true) {
  const lang = translations[language] ? language : "ru";
  const dictionary = translations[lang];

  document.documentElement.lang = lang;
  document.title = dictionary.title;
  document.querySelector('meta[name="description"]').setAttribute("content", dictionary.description);

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const value = dictionary[element.dataset.i18n];
    if (value !== undefined) element.innerHTML = value;
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    const value = dictionary[element.dataset.i18nPlaceholder];
    if (value !== undefined) element.placeholder = value;
  });

  document.querySelectorAll("[data-i18n-alt]").forEach((element) => {
    const value = dictionary[element.dataset.i18nAlt];
    if (value !== undefined) element.alt = value;
  });

  languageButtons.forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.lang === lang));
  });

  if (updateUrl) {
    const url = new URL(window.location.href);
    if (lang === "ru") url.searchParams.delete("lang");
    else url.searchParams.set("lang", lang);
    history.replaceState({}, "", url);
  }

  localStorage.setItem("mironlab-language", lang);
}

languageButtons.forEach((button) => {
  button.addEventListener("click", () => setLanguage(button.dataset.lang));
});

const queryLanguage = new URLSearchParams(window.location.search).get("lang");
const savedLanguage = localStorage.getItem("mironlab-language");
setLanguage(queryLanguage || savedLanguage || "ru", false);

const revealObserver = "IntersectionObserver" in window
  ? new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 })
  : null;

document.querySelectorAll(".reveal").forEach((element) => {
  if (revealObserver) revealObserver.observe(element);
  else element.classList.add("is-visible");
});
