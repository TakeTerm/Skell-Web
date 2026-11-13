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

export async function createZip(files) {
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

export function readTextureCatalog(bytes) {
  const view = new DataView(bytes);
  let tail = bytes.byteLength - 22;
  const lower = Math.max(0, tail - 65535);
  while (tail >= lower && view.getUint32(tail, true) !== 0x06054b50) tail -= 1;
  if (tail < lower) throw new Error("ZIP directory missing");
  if (view.getUint16(tail + 4, true) || view.getUint16(tail + 6, true)) throw new Error("Multi-volume archive");
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
    const encrypted = (view.getUint16(cursor + 8, true) & 1) !== 0;
    cursor += 46 + nameLength + view.getUint16(cursor + 30, true) + view.getUint16(cursor + 32, true);
    const match = /^assets\/minecraft\/textures\/(block|item|gui|entity|particle)\/([a-z0-9_/-]+)\.png$/.exec(path);
    if (!match || encrypted || ![0, 8].includes(method) || uncompressed > 4_000_000 || length > 4_000_000) continue;
    if (view.getUint32(start, true) !== 0x04034b50) continue;
    const dataOffset = start + 30 + view.getUint16(start + 26, true) + view.getUint16(start + 28, true);
    const group = match[1] === "gui" ? "hud" : match[1];
    const label = match[2].split("/").at(-1).replaceAll("_", " ");
    entries.push({ key: group + "/" + match[2], label, group, path: path.slice("assets/minecraft/textures/".length), method, uncompressed, bytes: new Uint8Array(bytes, dataOffset, length) });
  }
  return entries;
}

export async function readTextureImage(entry) {
  if (entry.method === 0) return new Blob([entry.bytes], { type: "image/png" });
  const reader = new Blob([entry.bytes]).stream().pipeThrough(new DecompressionStream("deflate-raw")).getReader();
  const chunks = [];
  let total = 0;
  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      total += value.byteLength;
      if (total > entry.uncompressed) throw new Error("Texture exceeds declared size");
      chunks.push(value);
    }
    if (total !== entry.uncompressed) throw new Error("Incomplete texture data");
    return new Blob(chunks, { type: "image/png" });
  } finally {
    await reader.cancel();
  }
}
