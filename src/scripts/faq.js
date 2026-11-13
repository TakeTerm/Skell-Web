const TRANSITION_MS = 360;

class Faq {
  constructor(root) {
    this.items = [...root.querySelectorAll(".faq__item")];
    for (const item of this.items) {
      this.set(item, false);
      item.querySelector(".faq__question").addEventListener("click", () => this.toggle(item));
    }
    addEventListener("hashchange", () => this.openFromHash());
    this.openFromHash();
  }

  set(item, open) {
    const question = item.querySelector(".faq__question");
    const panel = item.querySelector(".faq__panel");
    item.classList.toggle("is-open", open);
    question.setAttribute("aria-expanded", String(open));
    panel.inert = !open;
  }

  toggle(item) {
    const willOpen = !item.classList.contains("is-open");
    for (const other of this.items) if (other !== item) this.set(other, false);
    this.set(item, willOpen);
  }

  openFromHash() {
    const target = this.items.find((item) => item.querySelector(".faq__panel").id === location.hash.slice(1));
    if (!target) return;
    for (const other of this.items) if (other !== target) this.set(other, false);
    this.set(target, true);
    setTimeout(() => target.scrollIntoView({ block: "center" }), TRANSITION_MS / 2);
  }
}

export function init(root) {
  new Faq(root);
}
