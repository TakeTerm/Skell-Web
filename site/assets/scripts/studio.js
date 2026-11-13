const studio = document.querySelector("[data-texture-studio]");
const dialog = studio.querySelector("[data-texture-dialog]");
const canvas = dialog.querySelector("[data-texture-canvas]");
const context = canvas.getContext("2d", { willReadFrequently: true });
const search = studio.querySelector("[data-portal-search]");
const editing = studio.dataset.textureStudio === "resourcepacks";
const cards = [...studio.querySelectorAll("[data-texture]")];
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

try {
  pack = JSON.parse(localStorage.getItem(storageKey)) ?? pack;
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
  const term = search.value.toLowerCase().trim();
  for (const card of cards) {
    const sameCategory = category === "all" || card.dataset.textureGroup === category;
    const inPack = Object.hasOwn(pack.entries, card.dataset.texture);
    card.hidden = !sameCategory || (packOnly && !inPack) || !card.textContent.toLowerCase().includes(term);
  }
  empty.hidden = cards.some((card) => !card.hidden);
}

function readImage(src, target) {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => {
      target.clearRect(0, 0, 16, 16);
      target.imageSmoothingEnabled = false;
      target.drawImage(image, 0, 0, 16, 16);
      resolve();
    };
    image.onerror = reject;
    image.src = src;
  });
}

async function showTexture(card) {
  active = { name: card.dataset.texture, group: card.dataset.textureGroup };
  dialog.querySelector("[data-texture-title]").textContent = card.querySelector("b").textContent;
  context.clearRect(0, 0, 16, 16);
  const saved = pack.entries[active.name];
  if (saved && editing) await readImage(saved.data, context);
  else if (imported.has(active.name)) await readImported(imported.get(active.name), context);
  else paintSample(context, active.name, active.group);
  brush = "draw";
  previousPixel = undefined;
  dialog.showModal();
}

function setPack() {
  try {
    localStorage.setItem(storageKey, JSON.stringify(pack));
    if (packCount) packCount.textContent = say("Textures", "Texturas") + ": " + Object.keys(pack.entries).length;
    return true;
  } catch {
    notify(say("Browser storage is full or unavailable.", "El almacenamiento está lleno o no está disponible."));
    return false;
  }
}

function textureCard(key, group, label) {
    const existing = cards.find((card) => card.dataset.texture === key);
    if (existing) return existing;
    const node = document.createElement("button");
    node.type = "button";
    node.className = "studio-texture";
    node.dataset.texture = key;
    node.dataset.textureGroup = group;
    node.setAttribute("aria-pressed", "false");
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
    studio.querySelector(".studio-grid").append(node);
    cards.push(node);
    bindCard(node);
    return node;
}

function updatePackList() {
  for (const [key, entry] of Object.entries(pack.entries)) {
    const card = textureCard(key, entry.group, key.split("/").at(-1).replaceAll("_", " "));
    const target = card.querySelector("canvas").getContext("2d");
    readImage(entry.data, target).catch(() => paintSample(target, key, entry.group));
  }
}

function bindCard(card) {
  card.addEventListener("click", () => {
    if (!multi) {
      showTexture(card).catch(() => notify(say("Unable to open texture.", "No se pudo abrir la textura.")));
      return;
    }
    const key = card.dataset.texture;
    if (selected.has(key)) selected.delete(key);
    else selected.add(key);
    card.setAttribute("aria-pressed", String(selected.has(key)));
  });
}

function pixel(event) {
  const box = canvas.getBoundingClientRect();
  return [Math.floor((event.clientX - box.left) * 16 / box.width), Math.floor((event.clientY - box.top) * 16 / box.height)]
    .map((value) => Math.min(15, Math.max(0, value)));
}

function drawPixel(x, y) {
  if (brush === "erase") context.clearRect(x, y, 1, 1);
  else context.fillRect(x, y, 1, 1);
}

function draw(event) {
  const [x, y] = pixel(event);
  context.fillStyle = dialog.querySelector("[data-texture-color]").value;
  if (brush === "fill") {
    context.fillRect(0, 0, 16, 16);
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
  output.width = outputSize;
  output.height = outputSize;
  const target = output.getContext("2d");
  target.imageSmoothingEnabled = false;
  if (type === "jpg") {
    target.fillStyle = "#000";
    target.fillRect(0, 0, outputSize, outputSize);
  }
  target.drawImage(input, 0, 0, outputSize, outputSize);
  return new Promise((resolve) => output.toBlob(resolve, type === "jpg" ? "image/jpeg" : "image/" + type));
}

function download(blob, name) {
  const url = URL.createObjectURL(blob);
  Object.assign(document.createElement("a"), { href: url, download: name }).click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function checksum(bytes) {
  let crc = 0xffffffff;
  for (const byte of bytes) {
    crc ^= byte;
    for (let bit = 0; bit < 8; bit += 1) crc = (crc >>> 1) ^ ((crc & 1) ? 0xedb88320 : 0);
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function zipHeader(length, fields) {
  const view = new DataView(new ArrayBuffer(length));
  for (const [offset, value, bytes] of fields) {
    if (bytes === 4) view.setUint32(offset, value, true);
    else view.setUint16(offset, value, true);
  }
  return view.buffer;
}

async function zip(files) {
  const encoder = new TextEncoder();
  const entries = [];
  const central = [];
  let offset = 0;
  let centralSize = 0;
  for (const [name, content] of files) {
    const path = encoder.encode(name);
    const bytes = new Uint8Array(await content.arrayBuffer());
    const crc = checksum(bytes);
    const local = zipHeader(30, [[0, 0x04034b50, 4], [4, 20, 2], [6, 0x800, 2], [14, crc, 4], [18, bytes.length, 4], [22, bytes.length, 4], [26, path.length, 2]]);
    const directory = zipHeader(46, [[0, 0x02014b50, 4], [4, 20, 2], [6, 20, 2], [8, 0x800, 2], [16, crc, 4], [20, bytes.length, 4], [24, bytes.length, 4], [28, path.length, 2], [42, offset, 4]]);
    entries.push(local, path, bytes);
    central.push(directory, path);
    offset += local.byteLength + path.length + bytes.length;
    centralSize += directory.byteLength + path.length;
  }
  const end = zipHeader(22, [[0, 0x06054b50, 4], [8, files.length, 2], [10, files.length, 2], [12, centralSize, 4], [16, offset, 4]]);
  return new Blob([...entries, ...central, end], { type: "application/zip" });
}

async function exportSelection() {
  if (!selected.size) {
    notify(say("Select at least one texture.", "Selecciona al menos una textura."));
    return;
  }
  const files = [];
  for (const card of cards.filter((entry) => selected.has(entry.dataset.texture))) {
    const preview = card.querySelector("canvas");
    const source = imported.get(card.dataset.texture);
    if (source) await readImported(source, preview.getContext("2d"));
    const blob = await blobFor(preview, Number(size.value), format.value);
    if (blob) files.push([card.dataset.texture.replaceAll("/", "-") + "." + format.value, blob]);
  }
  if (files.length) download(await zip(files), "skell-textures.zip");
}

async function exportPack() {
  const metadata = { pack: { description: pack.name, min_format: [75, 0], max_format: [75, 0] } };
  const files = [["pack.mcmeta", new Blob([JSON.stringify(metadata, null, 2)], { type: "application/json" })]];
  for (const [key, entry] of Object.entries(pack.entries)) {
    const response = await fetch(entry.data);
    files.push(["assets/minecraft/textures/" + (entry.path || folderFor[entry.group] + "/" + key + ".png"), await response.blob()]);
  }
  download(await zip(files), (pack.name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "skell-pack") + ".zip");
}

const actions = {
  multi: (button) => {
    multi = !multi;
    button.setAttribute("aria-pressed", String(multi));
    if (multi) return;
    selected.clear();
    for (const card of cards) card.setAttribute("aria-pressed", "false");
  },
  "close-texture": () => dialog.close(),
  "download-texture": async () => {
    const blob = await blobFor(canvas, Number(size.value), format.value);
    if (blob) download(blob, active.name.replaceAll("/", "-") + "." + format.value);
  },
  draw: () => { brush = "draw"; },
  fill: () => { brush = "fill"; },
  erase: () => { brush = "erase"; },
  "reset-texture": () => imported.has(active.name) ? readImported(imported.get(active.name), context) : paintSample(context, active.name, active.group),
  "save-texture": () => {
    pack.entries[active.name] = { data: canvas.toDataURL("image/png"), group: active.group, path: imported.get(active.name)?.path || pack.entries[active.name]?.path };
    if (setPack()) notify(say("Texture saved to pack.", "Textura guardada en el paquete."));
    updatePackList();
  },
  "export-selection": exportSelection,
  "export-pack": exportPack,
  "show-pack": (button) => {
    packOnly = !packOnly;
    button.setAttribute("aria-pressed", String(packOnly));
    filterCards();
  },
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
for (const card of cards) {
  const target = card.querySelector("canvas").getContext("2d");
  paintSample(target, card.dataset.texture, card.dataset.textureGroup);
  bindCard(card);
}
search.addEventListener("input", filterCards);
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
    pack.name = packName.value.trim() || "My resource pack";
    packName.value = pack.name;
    setPack();
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
    const url = URL.createObjectURL(file);
    try {
      await readImage(url, context);
      active = { name: file.name.replace(/\.[^.]+$/, "").toLowerCase().replace(/[^a-z0-9_-]/g, "_") || "custom", group: "block" };
      dialog.querySelector("[data-texture-title]").textContent = active.name;
      dialog.showModal();
    } catch {
      notify(say("Unable to read this image.", "No se pudo leer la imagen."));
    } finally {
      URL.revokeObjectURL(url);
      event.target.value = "";
    }
  });
  setPack();
  updatePackList();
}

function catalogDirectory(bytes) {
  const view = new DataView(bytes);
  let tail = bytes.byteLength - 22;
  const lower = Math.max(0, tail - 65535);
  while (tail >= lower && view.getUint32(tail, true) !== 0x06054b50) tail -= 1;
  if (tail < lower) throw new Error("ZIP directory missing");
  const count = view.getUint16(tail + 10, true);
  let cursor = view.getUint32(tail + 16, true);
  const decode = new TextDecoder();
  const entries = [];
  for (let i = 0; i < count; i += 1) {
    if (view.getUint32(cursor, true) !== 0x02014b50) throw new Error("Invalid ZIP entry");
    const nameLength = view.getUint16(cursor + 28, true);
    const path = decode.decode(new Uint8Array(bytes, cursor + 46, nameLength));
    const start = view.getUint32(cursor + 42, true);
    const method = view.getUint16(cursor + 10, true);
    const length = view.getUint32(cursor + 20, true);
    const uncompressed = view.getUint32(cursor + 24, true);
    cursor += 46 + nameLength + view.getUint16(cursor + 30, true) + view.getUint16(cursor + 32, true);
    const match = /^assets\/minecraft\/textures\/(block|item|gui|entity|particle)\/([a-z0-9_/-]+)\.png$/.exec(path);
    if (!match || ![0, 8].includes(method) || uncompressed > 4_000_000 || length > 4_000_000) continue;
    if (view.getUint32(start, true) !== 0x04034b50) continue;
    const dataOffset = start + 30 + view.getUint16(start + 26, true) + view.getUint16(start + 28, true);
    const group = match[1] === "gui" ? "hud" : match[1];
    const label = match[2].split("/").at(-1).replaceAll("_", " ");
    entries.push({ key: group + "/" + match[2], label, group, path: path.slice("assets/minecraft/textures/".length), method, bytes: new Uint8Array(bytes, dataOffset, length) });
  }
  return entries;
}

async function readImported(entry, target) {
  let image = new Blob([entry.bytes], { type: "image/png" });
  if (entry.method === 8) {
    const stream = image.stream().pipeThrough(new DecompressionStream("deflate-raw"));
    image = await new Response(stream, { headers: { "Content-Type": "image/png" } }).blob();
  }
  const url = URL.createObjectURL(image);
  try {
    await readImage(url, target);
  } finally {
    URL.revokeObjectURL(url);
  }
}

const observer = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    if (!entry.isIntersecting) continue;
    const card = entry.target;
    observer.unobserve(card);
    readImported(imported.get(card.dataset.texture), card.querySelector("canvas").getContext("2d")).catch(() => {});
  }
}, { rootMargin: "120px" });

studio.querySelector("[data-archive-import]").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  try {
    if (file.size > 160_000_000) throw new Error("Archive too large");
    const entries = catalogDirectory(await file.arrayBuffer());
    if (!entries.length) throw new Error("No textures found");
    for (const entry of entries) {
      imported.set(entry.key, entry);
      const card = textureCard(entry.key, entry.group, entry.label);
      observer.observe(card);
    }
    for (const button of categories) {
      const key = button.dataset.textureCategory;
      button.querySelector("small").textContent = String(cards.filter((card) => key === "all" || card.dataset.textureGroup === key).length);
    }
    filterCards();
    notify(say("Textures imported for this tab.", "Texturas importadas para esta pestaña."));
  } catch {
    notify(say("This archive could not be read or contains no supported textures.", "No se pudo leer el archivo o no contiene texturas compatibles."));
  } finally {
    event.target.value = "";
  }
});
