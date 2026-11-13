import { createZip, readTextureCatalog, readTextureImage } from "./texture-archive.js";

const studio = document.querySelector("[data-texture-studio]");
const dialog = studio.querySelector("[data-texture-dialog]");
const canvas = dialog.querySelector("[data-texture-canvas]");
const context = canvas.getContext("2d", { willReadFrequently: true });
const search = studio.querySelector("[data-portal-search]");
const editing = studio.dataset.textureStudio === "resourcepacks";
const cards = new Map([...studio.querySelectorAll("[data-texture]")].map((card) => [card.dataset.texture, card]));
const grid = studio.querySelector(".studio-grid");
const categories = [...studio.querySelectorAll("[data-texture-category]")];
const status = studio.querySelector("[data-studio-status]");
const empty = studio.querySelector("[data-studio-empty]");
const format = studio.querySelector("[data-texture-format]");
const size = studio.querySelector("[data-texture-size]");
const packName = studio.querySelector("[data-pack-name]");
const packCount = studio.querySelector("[data-pack-count]");
const selected = new Set();
const imported = new Map();
const folderFor = { block: "block", item: "item", hud: "gui/sprites/hud", entity: "entity", particle: "particle" };
const es = document.documentElement.lang === "es";
const say = (en, translation) => es ? translation : en;
const storageKey = "skell-resource-pack";
let pack = { name: "My resource pack", entries: {} };
let active;
let category = "all";
let multi = false;
let packOnly = false;
let brush = "draw";
let previousPixel;
let statusTimer;
let opening = false;
let textureBaseline;
const locale = document.documentElement.lang;

try {
  const saved = JSON.parse(localStorage.getItem(storageKey));
  if (saved && typeof saved.name === "string" && saved.entries && typeof saved.entries === "object") {
    pack.name = saved.name;
    for (const [key, entry] of Object.entries(saved.entries)) {
      if (!entry || !Object.hasOwn(folderFor, entry.group) || typeof entry.data !== "string" || !entry.data.startsWith("data:image/png;")) continue;
      pack.entries[key] = { ...entry, path: entry.path || folderFor[entry.group] + "/" + key + ".png" };
    }
  }
  format.value = localStorage.getItem("skell-texture-format") || "png";
  size.value = localStorage.getItem("skell-texture-size") || "512";
} catch {}

const PALETTES = {
  acacia: [154, 75, 43], oak: [163, 129, 76], spruce: [104, 72, 43], cherry: [196, 131, 140],
  grass: [89, 134, 52], moss: [79, 101, 33], stone: [117, 116, 113], cobblestone: [107, 106, 107],
  deepslate: [63, 62, 68], sand: [214, 197, 133], amethyst: [148, 106, 206], diamond: [74, 199, 195],
  emerald: [67, 175, 107], redstone: [188, 45, 42], gold: [224, 177, 53], golden: [224, 177, 53],
  bricks: [151, 76, 62], obsidian: [43, 32, 59], glass: [169, 213, 221], dirt: [120, 83, 55],
  water: [49, 100, 177], snow: [220, 233, 246], netherrack: [124, 46, 48], iron: [161, 164, 164],
  heart: [228, 49, 63], apple: [185, 36, 40], ender: [60, 136, 114], creeper: [80, 139, 59],
  slime: [90, 169, 70], enderman: [44, 35, 53], zombie: [67, 128, 85], flame: [244, 151, 49],
};

function seededRandom(key) {
  let hash = 2166136261;
  for (const character of key) hash = Math.imul(hash ^ character.charCodeAt(0), 16777619);
  return () => {
    hash ^= hash << 13;
    hash ^= hash >>> 17;
    hash ^= hash << 5;
    return (hash >>> 0) / 4294967296;
  };
}

function insideShape(key, group, x, y) {
  if (group === "block") return true;
  if (key.includes("sword")) return (Math.abs(x + y - 15) <= 1 && y < 12 && x > 3) || (Math.abs(x - y + 5) < 2 && y > 7 && y < 13);
  if (key === "crosshair") return (x === 7 && y > 3 && y < 12) || (y === 7 && x > 3 && x < 12);
  if (group === "entity") return x > 1 && x < 14 && y > 1 && y < 14;
  if (group === "particle") return Math.abs(x - 7.5) + Math.abs(y - 7.5) < 6 - Math.abs(x - y) / 4;
  if (key === "heart") return y > 2 && y < 14 && Math.abs(x - 7.5) < (y < 7 ? 6 : 12 - y / 1.25) && (y > 6 || x !== 7);
  if (key === "hotbar") return x > 0 && x < 15 && y > 5 && y < 10;
  return ((x - 7.5) / 5.7) ** 2 + ((y - 7.5) / 6.3) ** 2 < 1;
}

function paintSample(target, key, group) {
  target.clearRect(0, 0, 16, 16);
  const random = seededRandom(key);
  const base = PALETTES[key.split("_")[0]] || [136, 138, 150];
  const striped = key.includes("planks") || key.includes("log") || key === "bricks";
  for (let y = 0; y < 16; y += 1) {
    for (let x = 0; x < 16; x += 1) {
      if (!insideShape(key, group, x, y)) continue;
      let shade = Math.floor(random() * 39) - 19;
      if (striped && (y % 4 === 0 || (x + Math.floor(y / 4) * 5) % 12 === 0)) shade -= 27;
      if (key.includes("_ore") && random() > .21) {
        target.fillStyle = "rgb(" + [104 + shade, 104 + shade, 109 + shade].join(",") + ")";
      } else if (group === "entity" && ((x > 3 && x < 7 || x > 9 && x < 13) && y > 5 && y < 9)) {
        target.fillStyle = "#242424";
      } else {
        target.fillStyle = "rgb(" + base.map((channel) => Math.max(0, Math.min(255, channel + shade))).join(",") + ")";
      }
      target.fillRect(x, y, 1, 1);
    }
  }
}

function notify(message) {
  status.textContent = message;
  status.hidden = false;
  clearTimeout(statusTimer);
  statusTimer = setTimeout(() => { status.hidden = true; }, 4200);
}

function filterCards() {
  const term = search.value.toLocaleLowerCase(locale).trim();
  let visible = 0;
  for (const [key, card] of cards) {
    const inCategory = category === "all" || card.dataset.textureGroup === category;
    card.hidden = !inCategory || (packOnly && !Object.hasOwn(pack.entries, key)) || !card.dataset.search.includes(term);
    if (!card.hidden) visible += 1;
  }
  empty.hidden = visible > 0;
}

async function drawSource(source, target, thumbnail = false) {
  const image = new Image();
  image.src = source;
  await image.decode();
  const limit = thumbnail ? 48 : 1024;
  const scale = Math.min(1, limit / Math.max(image.naturalWidth, image.naturalHeight));
  target.canvas.width = Math.max(1, Math.round(image.naturalWidth * scale));
  target.canvas.height = Math.max(1, Math.round(image.naturalHeight * scale));
  target.imageSmoothingEnabled = false;
  target.drawImage(image, 0, 0, target.canvas.width, target.canvas.height);
}

async function drawBlob(blob, target, thumbnail = false) {
  const url = URL.createObjectURL(blob);
  try {
    await drawSource(url, target, thumbnail);
  } finally {
    URL.revokeObjectURL(url);
  }
}

function paintOriginal(key, group, target) {
  target.canvas.width = 16;
  target.canvas.height = 16;
  paintSample(target, key, group);
}

async function drawTexture(key, group, target, thumbnail = false) {
  const saved = editing && pack.entries[key];
  const original = imported.get(key);
  if (saved) await drawSource(saved.data, target, thumbnail);
  else if (original) await drawBlob(await readTextureImage(original), target, thumbnail);
  else paintOriginal(key, group, target);
}

function setBrush(value) {
  brush = value;
  for (const button of dialog.querySelectorAll("[data-brush]")) {
    button.setAttribute("aria-pressed", String(button.dataset.brush === value));
  }
}

function openEditor(key, group, label) {
  active = { name: key, group };
  textureBaseline = context.getImageData(0, 0, canvas.width, canvas.height);
  dialog.querySelector("[data-texture-title]").textContent = label;
  updateViewer();
  setBrush("draw");
  previousPixel = undefined;
  if (!dialog.open) dialog.showModal();
}

async function showTexture(card) {
  if (opening) return;
  const key = card.dataset.texture;
  const group = card.dataset.textureGroup;
  opening = true;
  try {
    await drawTexture(key, group, context);
    openEditor(key, group, card.querySelector("b").textContent);
  } finally {
    opening = false;
  }
}

function storePack(nextPack) {
  try {
    localStorage.setItem(storageKey, JSON.stringify(nextPack));
    pack = nextPack;
    if (packCount) packCount.textContent = say("Textures", "Texturas") + ": " + Object.keys(pack.entries).length;
    return true;
  } catch {
    notify(say("Browser storage is full or unavailable.", "El almacenamiento está lleno o no está disponible."));
    return false;
  }
}

function indexCard(card) {
  card.dataset.search = card.textContent.toLocaleLowerCase(locale) + " " + card.dataset.texture;
}

function textureCard(key, group, label, target = grid) {
  if (cards.has(key)) return cards.get(key);
  const node = document.createElement("button");
  node.type = "button";
  node.className = "studio-texture";
  node.dataset.texture = key;
  node.dataset.textureGroup = group;
  const preview = document.createElement("canvas");
  preview.width = 16;
  preview.height = 16;
  const image = document.createElement("span");
  image.className = "studio-texture__image";
  image.append(preview);
  const name = document.createElement("b");
  name.textContent = label;
  const badge = document.createElement("small");
  badge.textContent = group;
  node.append(image, name, badge);
  target.append(node);
  cards.set(key, node);
  indexCard(node);
  return node;
}

function observeSavedTextures() {
  for (const [key, entry] of Object.entries(pack.entries)) {
    observeCard(textureCard(key, entry.group, key.split("/").at(-1).replaceAll("_", " ")));
  }
}

grid.addEventListener("click", (event) => {
    const card = event.target.closest("[data-texture]");
    if (!card) return;
    if (!multi) {
      showTexture(card).catch(() => notify(say("Unable to open texture.", "No se pudo abrir la textura.")));
      return;
    }
    const key = card.dataset.texture;
    if (selected.has(key)) selected.delete(key);
    else selected.add(key);
    card.setAttribute("aria-pressed", String(selected.has(key)));
});

function pixel(event) {
  const box = canvas.getBoundingClientRect();
  const x = Math.floor((event.clientX - box.left) * canvas.width / box.width);
  const y = Math.floor((event.clientY - box.top) * canvas.height / box.height);
  return [Math.min(canvas.width - 1, Math.max(0, x)), Math.min(canvas.height - 1, Math.max(0, y))];
}

function drawPixel(x, y) {
  if (brush === "erase") context.clearRect(x, y, 1, 1);
  else context.fillRect(x, y, 1, 1);
}

function fillRegion(x, y) {
  const { width, height } = canvas;
  const pixels = context.getImageData(0, 0, width, height);
  const values = new Uint32Array(pixels.data.buffer);
  const start = y * width + x;
  const original = values[start];
  context.fillRect(x, y, 1, 1);
  const replacement = new Uint32Array(context.getImageData(x, y, 1, 1).data.buffer)[0];
  if (original === replacement) return;
  const pending = [start];
  values[start] = replacement;
  while (pending.length) {
    const index = pending.pop();
    const column = index % width;
    for (const next of [
      column > 0 ? index - 1 : -1,
      column < width - 1 ? index + 1 : -1,
      index >= width ? index - width : -1,
      index < width * (height - 1) ? index + width : -1,
    ]) {
      if (values[next] !== original) continue;
      values[next] = replacement;
      pending.push(next);
    }
  }
  context.putImageData(pixels, 0, 0);
}

function draw(event) {
  const [x, y] = pixel(event);
  context.fillStyle = dialog.querySelector("[data-texture-color]").value;
  if (brush === "fill") {
    if (!previousPixel) fillRegion(x, y);
    previousPixel = [x, y];
    return;
  }
  const [fromX, fromY] = previousPixel || [x, y];
  const steps = Math.max(Math.abs(fromX - x), Math.abs(fromY - y), 1);
  for (let step = 0; step <= steps; step += 1) {
    drawPixel(Math.round(fromX + (x - fromX) * step / steps), Math.round(fromY + (y - fromY) * step / steps));
  }
  previousPixel = [x, y];
}

function blobFor(input, outputSize, type) {
  const output = document.createElement("canvas");
  const scale = outputSize ? outputSize / Math.max(input.width, input.height) : 1;
  output.width = Math.max(1, Math.round(input.width * scale));
  output.height = Math.max(1, Math.round(input.height * scale));
  const target = output.getContext("2d");
  target.imageSmoothingEnabled = false;
  if (type === "jpg") {
    target.fillStyle = "#000";
    target.fillRect(0, 0, output.width, output.height);
  }
  target.drawImage(input, 0, 0, output.width, output.height);
  return new Promise((resolve) => output.toBlob(resolve, type === "jpg" ? "image/jpeg" : "image/" + type));
}

function download(blob, name) {
  const url = URL.createObjectURL(blob);
  Object.assign(document.createElement("a"), { href: url, download: name }).click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

async function exportSelection() {
  if (!selected.size) {
    notify(say("Select at least one texture.", "Selecciona al menos una textura."));
    return;
  }
  const files = [];
  const source = document.createElement("canvas").getContext("2d");
  for (const key of selected) {
    const card = cards.get(key);
    await drawTexture(key, card.dataset.textureGroup, source);
    const blob = await blobFor(source.canvas, Number(size.value), format.value);
    if (blob) files.push([key.replaceAll("/", "-") + "." + format.value, blob]);
  }
  if (files.length) download(await createZip(files), "skell-textures.zip");
}

async function exportPack() {
  const metadata = { pack: { description: pack.name, min_format: [75, 0], max_format: [75, 0] } };
  const files = [["pack.mcmeta", new Blob([JSON.stringify(metadata, null, 2)], { type: "application/json" })]];
  for (const entry of Object.values(pack.entries)) {
    const response = await fetch(entry.data);
    files.push(["assets/minecraft/textures/" + entry.path, await response.blob()]);
  }
  download(await createZip(files), (pack.name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "skell-pack") + ".zip");
}

function visibleCards() {
  return [...cards.values()].filter((card) => !card.hidden);
}

function viewerFilename() {
  const target = Number(size.value);
  const scale = target ? target / Math.max(canvas.width, canvas.height) : 1;
  const dimensions = [canvas.width, canvas.height].map((value) => Math.max(1, Math.round(value * scale))).join("x");
  return active.name.replaceAll("/", "-") + "_" + dimensions + "." + format.value;
}

function updateViewer() {
  if (!active) return;
  const cardList = visibleCards();
  const index = cardList.indexOf(cards.get(active.name));
  const path = imported.get(active.name)?.path || pack.entries[active.name]?.path || folderFor[active.group] + "/" + active.name + ".png";
  dialog.querySelector("[data-texture-path]").textContent = "assets/minecraft/textures/" + path;
  dialog.querySelector("[data-texture-dimensions]").textContent = say("Original", "Original") + " " + canvas.width + "×" + canvas.height;
  dialog.querySelector("[data-texture-filename]").textContent = viewerFilename();
  dialog.querySelector("[data-texture-position]").textContent = index < 0 ? "—" : index + 1 + " / " + cardList.length;
  dialog.querySelector("[data-portal-action=previous-texture]").disabled = index <= 0;
  dialog.querySelector("[data-portal-action=next-texture]").disabled = index < 0 || index >= cardList.length - 1;
  for (const button of dialog.querySelectorAll("[data-viewer-size]")) button.setAttribute("aria-pressed", String(button.dataset.viewerSize === size.value));
  for (const button of dialog.querySelectorAll("[data-viewer-format]")) button.setAttribute("aria-pressed", String(button.dataset.viewerFormat === format.value));
}

function pageTexture(direction) {
  const visible = visibleCards();
  const next = visible.indexOf(cards.get(active.name)) + direction;
  if (visible[next]) return showTexture(visible[next]);
}

dialog.addEventListener("click", (event) => {
  const option = event.target.closest("[data-viewer-size], [data-viewer-format]");
  if (!option) return;
  const control = option.hasAttribute("data-viewer-size") ? size : format;
  control.value = option.dataset.viewerSize ?? option.dataset.viewerFormat;
  control.dispatchEvent(new Event("change"));
  updateViewer();
});

const actions = {
  multi: (button) => {
    multi = !multi;
    button.setAttribute("aria-pressed", String(multi));
    if (multi) {
      for (const card of cards.values()) card.setAttribute("aria-pressed", "false");
      return;
    }
    selected.clear();
    for (const card of cards.values()) card.removeAttribute("aria-pressed");
  },
  "close-texture": () => dialog.close(),
  "download-texture": async () => {
    const blob = await blobFor(canvas, Number(size.value), format.value);
    if (blob) download(blob, viewerFilename());
  },
  "previous-texture": () => pageTexture(-1),
  "next-texture": () => pageTexture(1),
  draw: () => setBrush("draw"),
  fill: () => setBrush("fill"),
  erase: () => setBrush("erase"),
  "reset-texture": () => context.putImageData(textureBaseline, 0, 0),
  "save-texture": () => {
    const { name, group } = active;
    const path = imported.get(name)?.path || pack.entries[name]?.path || folderFor[group] + "/" + name + ".png";
    const entries = Object.fromEntries(Object.entries(pack.entries).filter(([, entry]) => entry.path !== path));
    entries[name] = { data: canvas.toDataURL("image/png"), group, path };
    if (!storePack({ ...pack, entries })) return;
    observeSavedTextures();
    filterCards();
    notify(say("Texture saved to pack.", "Textura guardada en el paquete."));
  },
  "export-selection": exportSelection,
  "export-pack": exportPack,
  "hide-guide": () => { studio.querySelector("[data-studio-guide]").hidden = true; },
  "show-textures": () => showPack(false),
  "show-pack": () => showPack(true),
};

studio.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-portal-action]");
  const action = button && actions[button.dataset.portalAction];
  if (!action) return;
  try {
    await action(button);
  } catch {
    notify(say("Unable to complete the export or edit.", "No se pudo completar la exportación o edición."));
  }
});
for (const button of categories) {
  button.addEventListener("click", () => {
    category = button.dataset.textureCategory;
    for (const option of categories) option.setAttribute("aria-pressed", String(option === button));
    filterCards();
  });
}
let searchFrame;
search.addEventListener("input", () => {
  cancelAnimationFrame(searchFrame);
  searchFrame = requestAnimationFrame(filterCards);
});

function showPack(open) {
  packOnly = open;
  category = "all";
  for (const option of categories) option.setAttribute("aria-pressed", String(option.dataset.textureCategory === "all"));
  studio.querySelector("[data-portal-action=show-pack]").setAttribute("aria-pressed", String(open));
  studio.querySelector("[data-portal-action=show-textures]").setAttribute("aria-pressed", String(!open));
  filterCards();
}

for (const [control, key] of [[format, "format"], [size, "size"]]) {
  control.addEventListener("change", () => {
    try {
      localStorage.setItem("skell-texture-" + key, control.value);
    } catch {}
  });
}
if (editing) {
  packName.value = pack.name;
  packName.addEventListener("change", () => {
    storePack({ ...pack, name: packName.value.trim() || "My resource pack" });
    packName.value = pack.name;
  });
  canvas.addEventListener("pointerdown", (event) => {
    previousPixel = undefined;
    canvas.setPointerCapture(event.pointerId);
    draw(event);
  });
  canvas.addEventListener("pointermove", (event) => {
    if (canvas.hasPointerCapture(event.pointerId)) draw(event);
  });
  studio.querySelector("[data-texture-import]").addEventListener("change", async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    try {
      await drawBlob(file, context);
      const name = file.name.replace(/\.[^.]+$/, "").toLowerCase().replace(/[^a-z0-9_-]/g, "_") || "custom";
      openEditor(name, "block", name);
    } catch {
      notify(say("Unable to read this image.", "No se pudo leer la imagen."));
    } finally {
      event.target.value = "";
    }
  });
  packCount.textContent = say("Textures", "Texturas") + ": " + Object.keys(pack.entries).length;
}

function paintThumbnail(card) {
  const key = card.dataset.texture;
  drawTexture(key, card.dataset.textureGroup, card.querySelector("canvas").getContext("2d"), true).catch(() => {});
}

const observer = "IntersectionObserver" in window ? new IntersectionObserver((entries) => {
  for (const entry of entries) {
    if (!entry.isIntersecting) continue;
    observer.unobserve(entry.target);
    paintThumbnail(entry.target);
  }
}, { rootMargin: "120px" }) : null;

function observeCard(card) {
  if (observer) observer.observe(card);
  else paintThumbnail(card);
}

for (const card of cards.values()) {
  indexCard(card);
  observeCard(card);
}
if (editing) observeSavedTextures();

studio.querySelector("[data-archive-import]").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  try {
    if (file.size > 160_000_000) throw new Error("Archive too large");
    const entries = readTextureCatalog(await file.arrayBuffer());
    if (!entries.length) throw new Error("No textures found");
    const fragment = document.createDocumentFragment();
    for (const entry of entries) {
      imported.set(entry.key, entry);
      observeCard(textureCard(entry.key, entry.group, entry.label, fragment));
    }
    grid.append(fragment);
    const counts = new Map();
    for (const card of cards.values()) counts.set(card.dataset.textureGroup, (counts.get(card.dataset.textureGroup) || 0) + 1);
    for (const button of categories) {
      const key = button.dataset.textureCategory;
      button.querySelector("small").textContent = String(key === "all" ? cards.size : counts.get(key) || 0);
    }
    filterCards();
    notify(say("Textures imported for this tab.", "Texturas importadas para esta pestaña."));
  } catch {
    notify(say("This archive could not be read or contains no supported textures.", "No se pudo leer el archivo o no contiene texturas compatibles."));
  } finally {
    event.target.value = "";
  }
});

if (editing) showPack(false);
