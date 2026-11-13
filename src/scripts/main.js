import { initShell } from "./shell.js";
import { whenNearViewport } from "./lazy.js";

const FEATURES = [
  ["[data-demo]", "./tabs.js"],
  ["[data-gui]", "./gui-demo.js"],
  ["[data-hud-editor]", "./hud-editor.js"],
  ["[data-kill-demo], [data-kill-mini]", "./kill-demo.js"],
  ["[data-recordings-demo]", "./recordings-demo.js"],
  ["[data-shulker]", "./shulker-demo.js"],
  ["[data-layout-viz]", "./layout-viz.js"],
  ["[data-faq]", "./faq.js"],
  ["[data-docs]", "./docs.js"],
];

initShell();

const initialized = new WeakSet();

export function initFeatures(root = document) {
  for (const [selector, path] of FEATURES) {
    for (const element of root.querySelectorAll(selector)) {
      if (initialized.has(element)) continue;
      initialized.add(element);
      whenNearViewport(element, () => import(path).then((module) => module.init(element)));
    }
  }
}

initFeatures();
