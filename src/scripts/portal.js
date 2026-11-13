const spanish = document.documentElement.lang === "es";
const prefix = spanish ? "/es/" : "/";
const say = (english, translation) => spanish ? translation : english;

function stored(key, fallback) {
  try {
    return JSON.parse(localStorage.getItem(key)) ?? fallback;
  } catch {
    return fallback;
  }
}

function save(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    return false;
  }
}

function download(blob, name) {
  const url = URL.createObjectURL(blob);
  const anchor = Object.assign(document.createElement("a"), { href: url, download: name });
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function setupDialog() {
  const dialog = document.querySelector(".portal-dialog");
  if (!dialog) return;
  for (const target of document.querySelectorAll(".reference-header, .site-footer")) target.inert = true;
  const close = dialog.querySelector(".portal-close");
  close.focus({ preventScroll: true });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") close.click();
    if (event.key !== "Tab") return;
    const controls = [...dialog.querySelectorAll("a[href], button:not(:disabled), input:not(:disabled), select")].filter((control) => control.getClientRects().length);
    const first = controls[0], last = controls.at(-1);
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  const search = dialog.querySelector("[data-portal-search]");
  if (!search) return;
  const content = [...dialog.querySelectorAll("[data-search-item]")];
  const links = [...dialog.querySelectorAll("[data-sidebar-link]")];
  search.addEventListener("input", () => {
    const query = search.value.trim().toLowerCase();
    for (const entry of content.length ? content : links) entry.hidden = !entry.textContent.toLowerCase().includes(query);
    for (const group of dialog.querySelectorAll("[data-faq-group]")) group.hidden = !group.querySelector("[data-search-item]:not([hidden])");
  });
  for (const link of links) {
    if (!link.hash || link.pathname !== location.pathname) continue;
    link.addEventListener("click", () => {
      for (const item of links) item.removeAttribute("aria-current");
      link.setAttribute("aria-current", "true");
    });
  }
}

function renderConfigs() {
  const list = document.querySelector("[data-config-list]");
  if (!list) return;
  list.replaceChildren();
  for (const name of stored("skell-configs", [])) {
    const row = document.createElement("p");
    row.textContent = name;
    list.append(row);
  }
}

function setupForms() {
  const signedIn = sessionStorage.getItem("skell-demo-session") === "active";
  for (const node of document.querySelectorAll("[data-account-signed-out]")) node.hidden = signedIn;
  for (const node of document.querySelectorAll("[data-account-signed-in]")) node.hidden = !signedIn;
  renderConfigs();
  for (const form of document.querySelectorAll("[data-portal-form]")) {
    const submit = form.querySelector("[data-portal-submit]");
    const status = form.querySelector("[role=status]");
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const kind = form.dataset.portalForm;
      if (kind === "register" && form.elements.password.value !== form.elements.confirmation.value) {
        status.textContent = say("Passwords do not match.", "Las contraseñas no coinciden.");
        return;
      }
      if (kind === "login" || kind === "register") {
        form.reset();
        sessionStorage.setItem("skell-demo-session", "active");
        location.assign(prefix + "account/");
        return;
      }
      if (kind === "reset") {
        form.reset();
        status.textContent = say("Reset preview complete. No email was sent.", "Vista previa completada. No se envió un correo.");
        return;
      }
      const data = Object.fromEntries(new FormData(form));
      const key = kind === "config" ? "skell-configs" : "skell-drafts-" + kind;
      const previous = stored(key, []);
      const value = kind === "config" ? String(data.name).trim() : data;
      if (!value) {
        status.textContent = say("Enter a name.", "Introduce un nombre.");
        return;
      }
      const saved = save(key, [...previous, value]);
      if (saved) form.reset();
      status.textContent = saved ? say("Saved in this browser.", "Guardado en este navegador.") : say("Browser storage is unavailable.", "El almacenamiento del navegador no está disponible.");
      renderConfigs();
    });
    submit.disabled = false;
  }
}

function pressed(group, active) {
  for (const option of group) option.setAttribute("aria-pressed", String(option === active));
}

function setupCheckout() {
  const dialog = document.querySelector("[data-checkout-dialog]");
  if (!dialog) return;
  const releases = document.querySelectorAll("[data-release]");
  const plans = document.querySelectorAll("[data-plan]");
  let release = "stable";
  const total = (card) => Number(card.dataset.basePrice) + (release === "beta" ? 4 : 0);
  for (const option of releases) {
    option.addEventListener("click", () => {
      release = option.dataset.release;
      pressed(releases, option);
      for (const plan of plans) {
        plan.querySelector("[data-price]").textContent = "$" + total(plan);
        plan.querySelector("[data-checkout]").textContent = say("Pay", "Pagar") + " $" + total(plan) + " →";
      }
    });
  }
  for (const plan of plans) {
    const methods = plan.querySelectorAll("[data-payment-method]");
    for (const method of methods) method.addEventListener("click", () => pressed(methods, method));
    plan.querySelector("[data-checkout]").addEventListener("click", () => {
      const method = plan.querySelector("[data-payment-method][aria-pressed=true]");
      dialog.querySelector("[data-checkout-summary]").textContent = [plan.dataset.plan, "$" + total(plan), method.dataset.paymentMethod].join(" · ");
      dialog.showModal();
    });
  }
  dialog.querySelector("[data-portal-action=close-checkout]").addEventListener("click", () => dialog.close());
}

function setupLogo() {
  const stage = document.querySelector(".portal-logo-preview");
  if (!stage) return;
  const color = document.querySelector("[data-logo-color]");
  const wordmark = document.querySelector("[data-logo-wordmark]");
  const animation = document.querySelector("[data-logo-animate]");
  const format = document.querySelector("[data-logo-format]");
  const size = document.querySelector("[data-logo-size]");
  color.addEventListener("input", () => { stage.style.color = color.value; });
  wordmark.addEventListener("change", () => { stage.querySelector("strong").hidden = !wordmark.checked; });
  animation.addEventListener("change", () => { stage.classList.toggle("is-animated", animation.checked); });
  document.querySelector("[data-portal-action=download-logo]").addEventListener("click", async () => {
    const response = await fetch("/assets/brand/skell-mark.svg");
    if (!response.ok) return;
    const mark = new DOMParser().parseFromString(await response.text(), "image/svg+xml").documentElement;
    const namespace = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(namespace, "svg");
    svg.setAttribute("xmlns", namespace);
    svg.setAttribute("viewBox", wordmark.checked ? "0 0 340 150" : "0 0 150 150");
    svg.setAttribute("width", wordmark.checked ? "340" : "150");
    svg.setAttribute("height", "150");
    mark.setAttribute("x", "12");
    mark.setAttribute("y", "15");
    mark.setAttribute("width", "120");
    mark.setAttribute("height", "120");
    for (const path of mark.querySelectorAll("path")) path.setAttribute("fill", color.value);
    svg.append(mark);
    if (wordmark.checked) {
      const word = document.createElementNS(namespace, "text");
      for (const [key, value] of Object.entries({ x: 141, y: 96, "font-family": "sans-serif", "font-size": 64, fill: color.value })) word.setAttribute(key, value);
      word.textContent = "Skell";
      svg.append(word);
    }
    const image = new Blob([new XMLSerializer().serializeToString(svg)], { type: "image/svg+xml" });
    if (format.value === "svg") {
      download(image, "skell-logo.svg");
      return;
    }
    const canvas = document.createElement("canvas");
    canvas.width = Number(size.value);
    canvas.height = wordmark.checked ? Math.round(canvas.width * 150 / 340) : canvas.width;
    const context = canvas.getContext("2d");
    if (format.value === "jpg") {
      context.fillStyle = "#101010";
      context.fillRect(0, 0, canvas.width, canvas.height);
    }
    const url = URL.createObjectURL(image);
    try {
      const source = new Image();
      source.src = url;
      await source.decode();
      context.drawImage(source, 0, 0, canvas.width, canvas.height);
      canvas.toBlob((blob) => blob && download(blob, "skell-logo." + format.value), format.value === "jpg" ? "image/jpeg" : "image/png");
    } finally {
      URL.revokeObjectURL(url);
    }
  });
}

document.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-portal-action]");
  if (!button) return;
  const action = button.dataset.portalAction;
  if (action === "signout") {
    sessionStorage.removeItem("skell-demo-session");
    location.assign(prefix + "login/");
  } else if (action === "passkey" || action === "qr") {
    document.querySelector(".portal-auth [role=status]").textContent = say("This sign-in method needs a live account service.", "Este método de inicio requiere un servicio de cuentas.");
  } else if (action === "copy") {
    const target = document.querySelector("[data-portal-copy]");
    try {
      await navigator.clipboard.writeText(target.dataset.portalCopy);
      button.textContent = say("Copied", "Copiado");
    } catch {
      button.textContent = say("Copy unavailable", "No se pudo copiar");
    }
  }
});

setupDialog();
setupForms();
setupCheckout();
setupLogo();

const cookies = document.querySelector("[data-cookie-panel]");
if (cookies) {
  cookies.hidden = Boolean(stored("skell-storage-notice", false));
  document.querySelector("[data-cookie-open]").addEventListener("click", () => { cookies.hidden = false; });
  cookies.querySelector("[data-cookie-close]").addEventListener("click", () => {
    save("skell-storage-notice", true);
    cookies.hidden = true;
  });
}
