class ShulkerDemo {
  constructor(root) {
    this.box = root.querySelector("[data-shulker-box]");
    this.tooltip = root.querySelector("[data-shulker-tooltip]");
    this.box.addEventListener("pointerdown", (event) => {
      this.box.setPointerCapture(event.pointerId);
      this.show(true);
    });
    for (const type of ["pointerup", "pointercancel"]) this.box.addEventListener(type, () => this.show(false));
    this.box.addEventListener("click", (event) => {
      if (event.detail === 0) this.show(this.box.getAttribute("aria-pressed") !== "true");
    });
    this.box.addEventListener("blur", () => this.show(false));
    this.box.addEventListener("contextmenu", (event) => event.preventDefault());
  }

  show(visible) {
    this.box.setAttribute("aria-pressed", String(visible));
    this.tooltip.classList.toggle("is-visible", visible);
    this.tooltip.setAttribute("aria-hidden", String(!visible));
  }
}

export function init(root) {
  new ShulkerDemo(root);
}
