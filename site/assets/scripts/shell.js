const SCROLL_THRESHOLD = 12;
const FOCUSABLE = "a[href], button:not([disabled]), input, select, [tabindex]:not([tabindex='-1'])";

function trackScroll(header) {
  const update = () => header.classList.toggle("is-scrolled", scrollY > SCROLL_THRESHOLD);
  update();
  addEventListener("scroll", update, { passive: true });
}

function setupMobileMenu(header) {
  const button = header.querySelector("[data-menu-button]");
  const menu = document.querySelector("[data-mobile-menu]");
  if (!button || !menu) return;
  const inertTargets = [document.querySelector("main"), document.querySelector(".site-footer")];

  const toggle = (open) => {
    header.classList.toggle("is-open", open);
    menu.classList.toggle("is-open", open);
    document.body.classList.toggle("is-locked", open);
    button.setAttribute("aria-expanded", String(open));
    button.setAttribute("aria-label", open ? button.dataset.closeLabel : button.dataset.openLabel);
    inertTargets.forEach((target) => target && (target.inert = open));
    if (open) menu.querySelector("a")?.focus({ preventScroll: true });
  };

  button.addEventListener("click", () => toggle(!menu.classList.contains("is-open")));
  menu.addEventListener("click", (event) => event.target.closest("a") && toggle(false));
  matchMedia("(min-width: 900px)").addEventListener("change", (event) => event.matches && toggle(false));

  addEventListener("keydown", (event) => {
    if (!menu.classList.contains("is-open")) return;
    if (event.key === "Escape") {
      toggle(false);
      button.focus();
      return;
    }
    if (event.key !== "Tab") return;
    const items = [button, ...menu.querySelectorAll(FOCUSABLE)];
    const first = items[0];
    const last = items.at(-1);
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
}

function revealOnScroll() {
  const items = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window)) {
    items.forEach((item) => item.classList.add("is-visible"));
    return;
  }
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    },
    { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
  );
  items.forEach((item) => observer.observe(item));
}

function followPointerOnButtons() {
  document.addEventListener("pointermove", (event) => {
    const button = event.target.closest?.(".btn");
    if (!button) return;
    const box = button.getBoundingClientRect();
    button.style.setProperty("--mx", `${event.clientX - box.left}px`);
    button.style.setProperty("--my", `${event.clientY - box.top}px`);
  });
}

function rememberLanguageChoice() {
  document.addEventListener("click", (event) => {
    const choice = event.target.closest?.("[data-language-choice]");
    if (!choice) return;
    try {
      localStorage.setItem("skell-language", choice.dataset.languageChoice);
    } catch {
      return;
    }
  });
}

export function initShell() {
  const header = document.querySelector("[data-header]");
  if (header) {
    trackScroll(header);
    setupMobileMenu(header);
  }
  revealOnScroll();
  followPointerOnButtons();
  rememberLanguageChoice();
}
