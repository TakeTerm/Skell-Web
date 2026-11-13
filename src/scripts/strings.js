let cache;

export function readStrings() {
  cache ??= JSON.parse(document.getElementById("demo-strings").textContent);
  return cache;
}

export function format(template, values) {
  return template.replace(/\{(\w+)\}/g, (_, key) => values[key]);
}

export const prefersReducedMotion = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
