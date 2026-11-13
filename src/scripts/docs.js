const HEADING_OFFSET = "-96px 0px -70% 0px";

function setupMobileMenu(root) {
  const button = root.querySelector("[data-docs-menu-button]");
  const bar = root.querySelector("[data-docs-bar]");
  if (!button) return;
  const toggle = (open) => button.setAttribute("aria-expanded", String(open));
  button.addEventListener("click", () => toggle(button.getAttribute("aria-expanded") !== "true"));
  bar.addEventListener("click", (event) => event.target.closest("a") && toggle(false));
  document.addEventListener("click", (event) => !bar.contains(event.target) && toggle(false));
  bar.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    toggle(false);
    button.focus();
  });
}

function trackHeadings(root) {
  const toc = root.querySelector("[data-toc]");
  if (!toc || !("IntersectionObserver" in window)) return;
  const links = new Map([...toc.querySelectorAll("[data-toc-link]")].map((link) => [link.dataset.tocLink, link]));
  const headings = [...links.keys()].map((id) => document.getElementById(id)).filter(Boolean);
  const activate = (id) => {
    links.forEach((link, key) => {
      const active = key === id;
      link.classList.toggle("is-active", active);
      if (active) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  };
  const visible = new Set();
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) visible.add(entry.target.id);
        else visible.delete(entry.target.id);
      }
      const current = headings.find((heading) => visible.has(heading.id));
      if (current) activate(current.id);
    },
    { rootMargin: HEADING_OFFSET }
  );
  headings.forEach((heading) => observer.observe(heading));
}

class ModuleReference {
  constructor(root) {
    this.root = root;
    this.input = root.querySelector("[data-module-search]");
    this.sections = [...root.querySelectorAll(".modref-section")];
    this.empty = root.querySelector("[data-module-empty]");
    this.category = "";
    this.input.addEventListener("input", () => this.apply());
    root.querySelectorAll("[data-category-filter]").forEach((chip) => chip.addEventListener("click", () => this.chooseCategory(chip)));
    addEventListener("hashchange", () => this.revealHash());
    this.revealHash();
  }

  chooseCategory(chip) {
    this.category = chip.dataset.categoryFilter;
    this.root.querySelectorAll("[data-category-filter]").forEach((other) => other.setAttribute("aria-pressed", String(other === chip)));
    this.apply();
  }

  apply() {
    const query = this.input.value.trim().toLowerCase();
    let shown = 0;
    for (const section of this.sections) {
      const inCategory = !this.category || section.dataset.category === this.category;
      let matches = 0;
      for (const entry of section.querySelectorAll(".modref")) {
        const visible = inCategory && entry.dataset.search.includes(query);
        entry.hidden = !visible;
        if (visible) matches++;
      }
      section.hidden = matches === 0;
      shown += matches;
    }
    this.empty.hidden = shown > 0;
  }

  revealHash() {
    const target = location.hash.length > 1 ? document.getElementById(decodeURIComponent(location.hash.slice(1))) : null;
    if (!target || !this.root.contains(target)) return;
    this.input.value = "";
    this.chooseCategory(this.root.querySelector('[data-category-filter=""]'));
    target.scrollIntoView({ block: "center" });
    target.querySelector("details")?.setAttribute("open", "");
  }
}

export function init(root) {
  setupMobileMenu(root);
  trackHeadings(root);
  const reference = root.querySelector("[data-module-reference]");
  if (reference) new ModuleReference(reference);
}
