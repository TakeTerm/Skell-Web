class LayoutViz {
  constructor(root) {
    this.root = root;
    root.querySelectorAll("[data-viz-layout]").forEach((button) =>
      button.addEventListener("click", () => this.choose(root.querySelectorAll("[data-viz-layout]"), button, () => (root.dataset.layout = button.dataset.vizLayout)))
    );
    root.querySelectorAll("[data-viz-accent]").forEach((swatch) =>
      swatch.addEventListener("click", () => this.choose(root.querySelectorAll("[data-viz-accent]"), swatch, () => root.style.setProperty("--viz-accent", swatch.dataset.vizAccent)))
    );
  }

  choose(group, selected, apply) {
    group.forEach((item) => item.setAttribute("aria-pressed", String(item === selected)));
    apply();
  }
}

export function init(root) {
  new LayoutViz(root);
}
