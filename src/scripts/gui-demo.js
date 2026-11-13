import { readStrings } from "./strings.js";

const WIDE_PANEL_MIN_WIDTH = 780;
const PANEL_WIDTH = "340px";
const HUD_STYLE_VARIABLES = {
  Scale: (control) => ["--pv-scale", control.value],
  "Corner radius": (control) => ["--pv-radius", `${control.value}px`],
  "Text color": (control) => ["--pv-color", control.value],
};
const PREVIEW_VALUES = {
  fps: ["FPS", "144"],
  coordinates: ["XYZ", "128 · 72 · −340"],
  clock: ["", "21:47"],
  ping: ["PING", "32 ms"],
  cps: ["CPS", "8 | 6"],
  speed: ["SPEED", "5.6 b/s"],
  infobar: ["", "144 FPS · 32 ms"],
  radar: ["N", "12 m"],
};

let settingsRequest;

function loadSettings() {
  settingsRequest ??= fetch(`/assets/data/settings.${document.documentElement.lang}.json`).then((response) => response.json());
  return settingsRequest;
}

function template(name) {
  return document.getElementById(`template-${name}`).content.firstElementChild.cloneNode(true);
}

function percentage(control) {
  const span = control.max - control.min || 1;
  return `${((control.value - control.min) / span) * 100}%`;
}

function formatNumber(value, step) {
  const decimals = step && step < 1 ? String(step).split(".")[1]?.length ?? 1 : 0;
  return Number(value).toFixed(decimals);
}

class GuiDemo {
  constructor(root) {
    this.root = root;
    this.text = readStrings().gui;
    this.body = root.querySelector(".skui__body");
    this.main = root.querySelector("[data-main]");
    this.surface = root.querySelector("[data-settings]");
    this.search = root.querySelector("[data-search]");
    this.results = root.querySelector('[data-page="results"]');
    this.resultsGrid = root.querySelector("[data-results]");
    this.empty = root.querySelector("[data-empty]");
    this.page = "HUD";
    this.wantedLayout = "sheet";
    this.enabled = new Map();
    this.openModule = null;
    this.openOrigin = null;
    this.defaults = new Map();
    root.querySelectorAll(".skcard").forEach((card) => this.enabled.set(card.dataset.module, card.classList.contains("is-on")));
    this.initialEnabled = new Map(this.enabled);
    this.bind();
    this.updateCounts();
  }

  bind() {
    this.root.addEventListener("click", (event) => this.handleClick(event));
    this.root.addEventListener("contextmenu", (event) => {
      const card = event.target.closest(".skcard");
      if (!card) return;
      event.preventDefault();
      this.setEnabled(card.dataset.module, !this.enabled.get(card.dataset.module));
    });
    this.root.addEventListener("keydown", (event) => this.handleKey(event));
    this.search.addEventListener("input", () => this.runSearch());
    this.root.closest("[data-panel]").addEventListener("demo-reset", () => this.reset());
    new ResizeObserver(() => this.applyLayout()).observe(this.root);
    this.root.querySelectorAll("[data-layout-choice]").forEach((button) =>
      button.addEventListener("click", () => this.chooseLayout(button.dataset.layoutChoice, button))
    );
    this.root.querySelectorAll("[data-animation-choice]").forEach((button) =>
      button.addEventListener("click", () => this.chooseMotion(button.dataset.animationChoice, button))
    );
    this.root.querySelectorAll("[data-accent]").forEach((swatch) =>
      swatch.addEventListener("click", () => this.chooseAccent(swatch))
    );
    this.root.querySelector("[data-close-settings]").addEventListener("click", () => this.closeSettings());
    this.root.querySelector("[data-reset-settings]").addEventListener("click", () => this.resetSettings());
  }

  handleClick(event) {
    const nav = event.target.closest("[data-page-target]");
    if (nav) return this.showPage(nav.dataset.pageTarget);
    const chip = event.target.closest("[data-group-filter]");
    if (chip) return this.filterGroup(chip);
    const toggle = event.target.closest(".skcard .skswitch");
    if (toggle) {
      const card = toggle.closest(".skcard");
      return this.setEnabled(card.dataset.module, !this.enabled.get(card.dataset.module));
    }
    const card = event.target.closest(".skcard");
    if (card) this.openSettings(card, event.target.closest("[data-open-settings]"));
  }

  handleKey(event) {
    if (event.key === "Escape") {
      if (this.openModule) this.closeSettings();
      else if (this.search.value) {
        this.search.value = "";
        this.runSearch();
      }
      return;
    }
    const typing = event.target.matches("input, select, textarea, [data-keybind-listening]");
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "f") {
      event.preventDefault();
      this.search.focus();
    } else if (!typing && event.key.length === 1 && !event.ctrlKey && !event.metaKey && !event.altKey && event.target.closest(".skui__main, .skui__side")) {
      this.search.focus();
    }
    if (event.key === "Tab" && !typing && event.target.closest(".skui__side") && event.target.matches(".skui__nav")) {
      const buttons = [...this.root.querySelectorAll(".skui__nav")];
      const next = buttons[(buttons.indexOf(event.target) + (event.shiftKey ? -1 : 1) + buttons.length) % buttons.length];
      if (event.altKey) {
        event.preventDefault();
        next.focus();
      }
    }
  }

  setEnabled(id, on) {
    this.enabled.set(id, on);
    this.root.querySelectorAll(`.skcard[data-module="${id}"]`).forEach((card) => {
      card.classList.toggle("is-on", on);
      card.querySelector(".skswitch").setAttribute("aria-checked", String(on));
    });
    this.root.querySelectorAll(".skset .skswitch[data-enabled-switch]").forEach((control) => {
      if (this.openModule === id) control.setAttribute("aria-checked", String(on));
    });
    this.updateCounts();
  }

  updateCounts() {
    for (const nav of this.root.querySelectorAll(".skui__nav-count")) {
      const category = nav.closest("[data-page-target]").dataset.pageTarget;
      const cards = this.main.querySelectorAll(`.skui__page[data-page="${category}"] .skcard`);
      const active = [...cards].filter((card) => this.enabled.get(card.dataset.module)).length;
      nav.textContent = `${active}/${cards.length}`;
    }
  }

  showPage(category) {
    this.closeSettings(true);
    this.search.value = "";
    this.runSearch(false);
    this.page = category;
    this.root.querySelectorAll(".skui__nav").forEach((nav) => {
      const active = nav.dataset.pageTarget === category;
      nav.classList.toggle("is-active", active);
      nav.toggleAttribute("aria-current", active);
    });
    this.main.querySelectorAll(".skui__page").forEach((page) => {
      const active = page.dataset.page === category;
      page.hidden = !active;
      page.classList.toggle("is-entering", active);
    });
    this.main.scrollTo({ top: 0 });
  }

  filterGroup(chip) {
    const page = chip.closest(".skui__page");
    page.querySelectorAll("[data-group-filter]").forEach((other) => other.classList.toggle("is-active", other === chip));
    const group = chip.dataset.groupFilter;
    page.querySelectorAll(".skcard").forEach((card) => (card.hidden = Boolean(group) && card.dataset.group !== group));
  }

  runSearch(showResults = true) {
    const query = this.search.value.trim().toLowerCase();
    this.resultsGrid.replaceChildren();
    if (!query) {
      this.results.hidden = true;
      this.main.querySelector(`.skui__page[data-page="${this.page}"]`).hidden = false;
      this.empty.hidden = true;
      return;
    }
    if (!showResults) return;
    const matches = [...this.main.querySelectorAll(".skui__page:not(.skui__page--results) .skcard")].filter((card) =>
      card.textContent.toLowerCase().includes(query)
    );
    this.main.querySelectorAll(".skui__page:not(.skui__page--results)").forEach((page) => (page.hidden = true));
    this.results.hidden = false;
    this.empty.hidden = matches.length > 0;
    for (const card of matches) {
      const clone = card.cloneNode(true);
      clone.hidden = false;
      this.resultsGrid.append(clone);
    }
  }

  effectiveLayout() {
    return this.wantedLayout === "panel" && this.root.clientWidth >= WIDE_PANEL_MIN_WIDTH ? "panel" : "sheet";
  }

  applyLayout() {
    const layout = this.effectiveLayout();
    this.root.dataset.layout = layout;
    this.body.style.setProperty("--panel-width", layout === "panel" && this.openModule ? PANEL_WIDTH : "0px");
  }

  chooseLayout(layout, button) {
    this.wantedLayout = layout;
    button.parentElement.querySelectorAll("button").forEach((other) => other.setAttribute("aria-pressed", String(other === button)));
    this.applyLayout();
  }

  chooseMotion(motion, button) {
    this.root.dataset.motion = motion;
    button.parentElement.querySelectorAll("button").forEach((other) => other.setAttribute("aria-pressed", String(other === button)));
  }

  chooseAccent(swatch) {
    const color = swatch.dataset.accent;
    this.root.style.setProperty("--accent", color);
    this.root.style.setProperty("--accent-glow", `${color}66`);
    swatch.parentElement.querySelectorAll("button").forEach((other) => other.setAttribute("aria-pressed", String(other === swatch)));
  }

  async openSettings(card, trigger) {
    const id = card.dataset.module;
    const data = (await loadSettings())[id];
    if (!data) return;
    if (this.openModule === id && this.effectiveLayout() === "sheet") return;
    this.openModule = id;
    this.openOrigin = trigger ?? card;
    const bodyBox = this.body.getBoundingClientRect();
    const cardBox = card.getBoundingClientRect();
    this.surface.style.setProperty("--origin-x", `${cardBox.left + cardBox.width / 2 - bodyBox.left - (this.surface.offsetLeft || 0)}px`);
    this.surface.style.setProperty("--origin-y", `${cardBox.top + cardBox.height / 2 - bodyBox.top}px`);
    this.fillSettings(id, data);
    this.surface.classList.remove("is-leaving");
    this.surface.hidden = false;
    this.surface.style.animation = "none";
    void this.surface.offsetWidth;
    this.surface.style.animation = "";
    this.applyLayout();
    this.surface.querySelector("[data-close-settings]").focus({ preventScroll: true });
  }

  closeSettings(immediate = false) {
    if (!this.openModule) return;
    const origin = this.openOrigin;
    this.openModule = null;
    this.body.style.setProperty("--panel-width", "0px");
    const finish = () => {
      this.surface.hidden = true;
      this.surface.classList.remove("is-leaving");
    };
    if (immediate || this.root.dataset.motion === "off") finish();
    else {
      this.surface.classList.add("is-leaving");
      setTimeout(finish, 240);
    }
    if (!immediate) origin?.focus({ preventScroll: true });
  }

  fillSettings(id, data) {
    const card = this.root.querySelector(`.skcard[data-module="${id}"]`);
    this.surface.querySelector("[data-settings-title]").textContent = data.name;
    const body = this.surface.querySelector("[data-settings-body]");
    body.replaceChildren();
    const preview = this.surface.querySelector("[data-preview]");
    this.buildPreview(preview, id, data, card);
    this.defaults.set(id, []);
    body.append(this.enabledRow(id), this.keybindRow());
    for (const group of data.groups) {
      if (group.name) {
        const heading = template("group");
        heading.textContent = group.name;
        body.append(heading);
      }
      for (const setting of group.settings) {
        const row = this.settingRow(setting, preview, id);
        if (row) body.append(row);
      }
    }
  }

  enabledRow(id) {
    const row = template("bool");
    row.querySelector(".skrow__label").textContent = this.text.enabled;
    const toggle = row.querySelector(".skswitch");
    toggle.dataset.enabledSwitch = "";
    toggle.setAttribute("aria-checked", String(this.enabled.get(id)));
    toggle.setAttribute("aria-label", this.text.enabled);
    toggle.addEventListener("click", () => this.setEnabled(id, !this.enabled.get(id)));
    return row;
  }

  keybindRow() {
    const row = template("keybind");
    row.querySelector(".skrow__label").textContent = this.text.keybind;
    const button = row.querySelector(".skkey");
    button.textContent = this.text.unbound;
    const stop = () => {
      button.classList.remove("is-listening");
      button.removeAttribute("data-keybind-listening");
    };
    button.addEventListener("click", () => {
      button.classList.add("is-listening");
      button.dataset.keybindListening = "";
      button.textContent = this.text.pressKey;
    });
    button.addEventListener("keydown", (event) => {
      if (!button.classList.contains("is-listening")) return;
      event.preventDefault();
      event.stopPropagation();
      button.textContent = event.key === "Escape" ? this.text.unbound : event.key.length === 1 ? event.key.toUpperCase() : event.key;
      stop();
    });
    button.addEventListener("blur", () => button.classList.contains("is-listening") && ((button.textContent = this.text.unbound), stop()));
    button.addEventListener("contextmenu", (event) => {
      event.preventDefault();
      button.textContent = this.text.unbound;
      stop();
    });
    return row;
  }

  buildPreview(container, id, data, card) {
    container.replaceChildren();
    container.removeAttribute("style");
    const values = PREVIEW_VALUES[id];
    if (!values) {
      const tile = document.createElement("div");
      tile.className = "hudw";
      tile.dataset.previewWidget = "";
      tile.innerHTML = `<span class="hudw__value"></span>`;
      tile.querySelector(".hudw__value").textContent = data.name;
      container.append(tile);
      return;
    }
    const widget = document.createElement("div");
    widget.className = "hudw";
    widget.dataset.previewWidget = "";
    if (values[0]) widget.insertAdjacentHTML("beforeend", `<span class="hudw__label"></span>`);
    widget.insertAdjacentHTML("beforeend", `<span class="hudw__value"></span>`);
    widget.querySelector(".hudw__label") && (widget.querySelector(".hudw__label").textContent = values[0]);
    widget.querySelector(".hudw__value").textContent = values[1];
    container.append(widget);
  }

  settingRow(setting, preview, moduleId) {
    const widget = preview.querySelector("[data-preview-widget]");
    const apply = (control) => {
      const mapped = HUD_STYLE_VARIABLES[setting.key];
      if (mapped && widget) widget.style.setProperty(...mapped(control));
      if (setting.key === "Background" && widget) widget.style.setProperty("--pv-bg", control.checked ? "" : "transparent");
      if (setting.key === "Chroma text" && widget) widget.style.setProperty("--pv-color", control.checked ? "var(--accent)" : "#fff");
    };
    let row;
    if (setting.type === "bool") {
      row = template("bool");
      const toggle = row.querySelector(".skswitch");
      const state = { checked: Boolean(setting.default) };
      toggle.setAttribute("aria-checked", String(state.checked));
      toggle.setAttribute("aria-label", setting.name);
      toggle.addEventListener("click", () => {
        state.checked = !state.checked;
        toggle.setAttribute("aria-checked", String(state.checked));
        apply(state);
      });
      this.defaults.get(moduleId).push(() => {
        state.checked = Boolean(setting.default);
        toggle.setAttribute("aria-checked", String(state.checked));
        apply(state);
      });
    } else if (setting.type === "number" && setting.min != null) {
      row = template("number");
      const input = row.querySelector("input");
      const output = row.querySelector("output");
      input.min = setting.min;
      input.max = setting.max;
      input.step = setting.step || (setting.max - setting.min) / 100;
      input.value = setting.default;
      input.setAttribute("aria-label", setting.name);
      const update = () => {
        output.textContent = formatNumber(input.value, setting.step);
        input.style.setProperty("--fill", percentage(input));
        apply(input);
      };
      input.addEventListener("input", update);
      update();
      this.defaults.get(moduleId).push(() => {
        input.value = setting.default;
        update();
      });
    } else if (setting.type === "mode" && setting.options.length) {
      row = setting.options.length <= 3 ? this.segmentedRow(setting, moduleId) : this.selectRow(setting, moduleId);
    } else if (setting.type === "color") {
      row = template("color");
      const input = row.querySelector("input");
      input.value = "#ffffff";
      input.setAttribute("aria-label", setting.name);
      input.addEventListener("input", () => apply(input));
      this.defaults.get(moduleId).push(() => {
        input.value = "#ffffff";
        apply(input);
      });
    } else if (setting.type === "string") {
      row = template("text");
      const input = row.querySelector("input");
      input.value = setting.default ?? "";
      input.setAttribute("aria-label", setting.name);
      this.defaults.get(moduleId).push(() => (input.value = setting.default ?? ""));
    }
    row?.querySelector(".skrow__label").replaceChildren(setting.name);
    return row;
  }

  segmentedRow(setting, moduleId) {
    const row = template("mode");
    const group = row.querySelector(".segmented");
    group.setAttribute("aria-label", setting.name);
    const buttons = setting.options.map((option) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "segmented__option";
      button.textContent = option.label;
      button.addEventListener("click", () => select(option.value));
      group.append(button);
      return [option.value, button];
    });
    const select = (value) => buttons.forEach(([optionValue, button]) => button.setAttribute("aria-pressed", String(optionValue === value)));
    const initial = setting.default ?? setting.options[0].value;
    select(initial);
    this.defaults.get(moduleId).push(() => select(initial));
    return row;
  }

  selectRow(setting, moduleId) {
    const row = template("select");
    const select = row.querySelector("select");
    select.setAttribute("aria-label", setting.name);
    for (const option of setting.options) select.add(new Option(option.label, option.value));
    const initial = setting.default ?? setting.options[0].value;
    select.value = initial;
    this.defaults.get(moduleId).push(() => (select.value = initial));
    return row;
  }

  resetSettings() {
    this.defaults.get(this.openModule)?.forEach((restore) => restore());
  }

  reset() {
    this.closeSettings(true);
    for (const [id, on] of this.initialEnabled) this.setEnabled(id, on);
    this.showPage("HUD");
    this.root.querySelectorAll(".skui__chips").forEach((chips) => chips.querySelector("[data-group-filter]")?.click());
  }
}

export function init(root) {
  new GuiDemo(root);
}
