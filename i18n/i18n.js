(function () {
  const STORAGE_KEY = "portfolio-lang";
  const DEFAULT_LANG = "en";

  let currentLang = localStorage.getItem(STORAGE_KEY) || DEFAULT_LANG;
  let strings = {};

  function get(obj, path) {
    return path.split(".").reduce((acc, part) => (acc && acc[part] !== undefined ? acc[part] : null), obj);
  }

  function applyTranslations() {
    document.documentElement.lang = currentLang;

    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      const value = get(strings, key);
      if (value != null) el.textContent = value;
    });

    document.querySelectorAll("[data-i18n-html]").forEach((el) => {
      const key = el.getAttribute("data-i18n-html");
      const value = get(strings, key);
      if (value != null) el.innerHTML = value;
    });

    const title = get(strings, "meta.title");
    const desc = get(strings, "meta.description");
    if (title) document.title = title;
    if (desc) {
      const meta = document.querySelector('meta[name="description"]');
      if (meta) meta.setAttribute("content", desc);
    }
    document.querySelectorAll("[data-i18n-meta]").forEach((el) => {
      const key = el.getAttribute("data-i18n-meta");
      const value = get(strings, key);
      if (value != null) el.setAttribute("content", value);
    });

    document.querySelectorAll(".lang-btn").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.lang === currentLang);
    });

    const cvLink = document.getElementById('cv-link');
    if (cvLink) {
      cvLink.href = currentLang === 'tr' ? 'ECE-DALPOLAT-cv-TR.pdf' : 'ECE-DALPOLAT-resume.pdf';
    }
  }

  function i18nJsonUrl(lang) {
    const script = document.querySelector('script[src*="i18n.js"]');
    if (script && script.src) {
      return new URL(`${lang}.json`, script.src).href;
    }
    return `i18n/${lang}.json`;
  }

  async function loadLanguage(lang) {
    const res = await fetch(i18nJsonUrl(lang));
    if (!res.ok) throw new Error(`Failed to load ${lang}.json`);
    strings = await res.json();
    currentLang = lang;
    localStorage.setItem(STORAGE_KEY, lang);
    applyTranslations();
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".lang-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const lang = btn.dataset.lang;
        if (lang && lang !== currentLang) loadLanguage(lang);
      });
    });
    loadLanguage(currentLang).catch(() => {
      currentLang = DEFAULT_LANG;
    });
  });
})();
