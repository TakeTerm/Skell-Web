const preview = document.querySelector("[data-client-preview]");

function choose(buttons, selected) {
  for (const button of buttons) button.setAttribute("aria-pressed", String(button === selected));
}

function bindChoices(root, selector, onSelect) {
  const buttons = [...root.querySelectorAll(selector)];
  for (const button of buttons) {
    button.addEventListener("click", () => {
      choose(buttons, button);
      onSelect(button);
    });
  }
}

function toggleButton(button, active) {
  button.setAttribute("aria-pressed", String(active));
}

function setupPreview(panel) {
  const cards = [...panel.querySelectorAll("[data-preview-card]")];
  const search = panel.querySelector("[data-preview-search]");
  const favorites = panel.querySelector("[data-preview-favorites]");
  const empty = panel.querySelector("[data-preview-empty]");
  let category = "0";

  function filter() {
    const term = search.value.trim().toLowerCase();
    const onlyFavorites = favorites.getAttribute("aria-pressed") === "true";
    let visible = 0;
    for (const card of cards) {
      const inCategory = category === "0" || card.dataset.previewCard.split(" ").includes(category);
      const favorite = card.querySelector(".preview-favorite").getAttribute("aria-pressed") === "true";
      card.hidden = !inCategory || !card.textContent.toLowerCase().includes(term) || (onlyFavorites && !favorite);
      if (!card.hidden) visible += 1;
    }
    empty.hidden = visible !== 0;
  }

  bindChoices(panel, "[data-preview-category]", (button) => {
    category = button.dataset.previewCategory;
    panel.querySelector("[data-preview-title]").textContent = button.textContent;
    filter();
  });
  bindChoices(panel, "[data-preview-theme]", (button) => {
    panel.dataset.theme = button.dataset.previewTheme;
  });
  bindChoices(panel, "[data-preview-mode]", (button) => {
    panel.dataset.mode = button.dataset.previewMode;
  });
  bindChoices(panel, "[data-preview-accent]", (button) => {
    panel.style.setProperty("--preview-accent", button.dataset.previewAccent);
  });

  panel.addEventListener("submit", (event) => event.preventDefault());
  search.addEventListener("input", filter);
  favorites.addEventListener("click", () => {
    const active = favorites.getAttribute("aria-pressed") !== "true";
    toggleButton(favorites, active);
    favorites.textContent = active ? "★" : "☆";
    filter();
  });

  for (const button of panel.querySelectorAll(".preview-favorite")) {
    button.addEventListener("click", () => {
      const active = button.getAttribute("aria-pressed") !== "true";
      toggleButton(button, active);
      button.textContent = active ? "★" : "☆";
      filter();
    });
  }

  const expand = panel.querySelector("[data-preview-expand]");
  expand.addEventListener("click", () => toggleButton(expand, panel.classList.toggle("is-expanded")));

  for (const input of panel.querySelectorAll('input[type="range"]')) {
    const output = input.closest("label").querySelector("output");
    input.addEventListener("input", () => { output.value = input.value; });
  }

  addEventListener("keydown", (event) => {
    if (!(event.ctrlKey || event.metaKey) || event.key.toLowerCase() !== "k") return;
    event.preventDefault();
    search.focus();
  });
}

function setupNavigation() {
  const nav = document.querySelector(".reference-nav");
  if (!nav) return;
  const button = document.querySelector("[data-reference-menu]");
  const dropdowns = [...nav.querySelectorAll("details")];

  function closeMenu() {
    nav.classList.remove("is-open");
    button.setAttribute("aria-expanded", "false");
  }

  button.addEventListener("click", () => {
    button.setAttribute("aria-expanded", String(nav.classList.toggle("is-open")));
  });
  nav.addEventListener("click", (event) => {
    if (!event.target.closest("a")) return;
    for (const item of dropdowns) item.open = false;
    closeMenu();
  });
  document.addEventListener("click", (event) => {
    if (event.target.closest(".reference-header")) return;
    for (const item of dropdowns) item.open = false;
    closeMenu();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    const open = dropdowns.find((item) => item.open);
    if (open) {
      open.open = false;
      open.querySelector("summary").focus();
    } else if (nav.classList.contains("is-open")) {
      closeMenu();
      button.focus();
    }
  });
  for (const dropdown of dropdowns) {
    dropdown.addEventListener("toggle", () => {
      if (!dropdown.open) return;
      for (const other of dropdowns) if (other !== dropdown) other.open = false;
    });
  }
}

function openStudioFromHash() {
  if (!["#studio", "#studio-demo"].includes(location.hash)) return;
  const studio = document.querySelector("#studio");
  if (studio) studio.open = true;
}

if (preview && !preview.closest(".portal-scene")) setupPreview(preview);
setupNavigation();
openStudioFromHash();
addEventListener("hashchange", openStudioFromHash);
