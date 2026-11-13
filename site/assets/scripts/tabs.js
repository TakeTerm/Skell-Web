const ARROWS = { ArrowLeft: -1, ArrowRight: 1 };

export function init(section) {
  const list = section.querySelector("[role=tablist]");
  const indicator = list.querySelector("[data-indicator]");
  const tabs = [...list.querySelectorAll("[role=tab]")];
  const panels = new Map(tabs.map((tab) => [tab, section.querySelector(`#${tab.getAttribute("aria-controls")}`)]));

  const moveIndicator = (tab) => {
    indicator.style.width = `${tab.offsetWidth}px`;
    indicator.style.transform = `translateX(${tab.offsetLeft}px)`;
  };

  const centerTab = (tab) => {
    const target = tab.offsetLeft - (list.clientWidth - tab.offsetWidth) / 2;
    list.scrollTo({ left: Math.max(0, target), behavior: "smooth" });
  };

  const select = (tab, focus = false) => {
    for (const [other, panel] of panels) {
      const active = other === tab;
      other.setAttribute("aria-selected", String(active));
      other.tabIndex = active ? 0 : -1;
      panel.classList.toggle("is-active", active);
      panel.inert = !active;
    }
    moveIndicator(tab);
    if (focus) tab.focus({ preventScroll: true });
  };

  tabs.forEach((tab) =>
    tab.addEventListener("click", () => {
      select(tab);
      centerTab(tab);
    })
  );
  list.addEventListener("keydown", (event) => {
    const current = tabs.indexOf(document.activeElement);
    if (current < 0) return;
    if (event.key in ARROWS) {
      event.preventDefault();
      const next = tabs[(current + ARROWS[event.key] + tabs.length) % tabs.length];
      select(next, true);
      centerTab(next);
    } else if (event.key === "Home" || event.key === "End") {
      event.preventDefault();
      select(event.key === "Home" ? tabs[0] : tabs.at(-1), true);
    }
  });

  section.querySelector("[data-demo-reset]")?.addEventListener("click", () => {
    const active = [...panels.values()].find((panel) => panel.classList.contains("is-active"));
    active.dispatchEvent(new CustomEvent("demo-reset"));
  });

  const selectedTab = tabs.find((tab) => tab.getAttribute("aria-selected") === "true");
  select(selectedTab);
  addEventListener("resize", () => moveIndicator(tabs.find((tab) => tab.tabIndex === 0)));
  document.fonts?.ready.then(() => moveIndicator(tabs.find((tab) => tab.tabIndex === 0)));
}
