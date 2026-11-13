import { readStrings } from "./strings.js";

const CONFIRM_MS = 3000;
const NOTE_MS = 1800;
const TOAST_MS = 3400;
const REMOVE_MS = 420;
const WARMUP_STEP_MS = 200;
const WARMUP_STEPS = 20;
const CLIP_DURATION = "0:30";
const CLIP_SIZE = "13.9 MB";
const RECORDING_SIZE_PER_SECOND = 0.82;

const pad = (value) => String(value).padStart(2, "0");
const clock = (seconds) => `${Math.floor(seconds / 60)}:${pad(seconds % 60)}`;

class RecordingsDemo {
  constructor(root) {
    this.root = root;
    this.text = readStrings().recordings;
    this.list = root.querySelector("[data-rec-list]");
    this.empty = root.querySelector("[data-rec-empty]");
    this.toast = root.querySelector("[data-clip-toast]");
    this.timer = root.querySelector("[data-rec-timer]");
    this.recorderButton = root.querySelector("[data-recorder-toggle]");
    this.recorderLabel = root.querySelector("[data-rec-label]");
    this.replayToggle = root.querySelector("[data-replay-toggle]");
    this.replayStatus = root.querySelector("[data-replay-status]");
    this.replayBar = root.querySelector("[data-replay-bar] i");
    this.templates = Object.fromEntries([...this.list.children].reverse().map((row) => [row.dataset.kind, row.cloneNode(true)]));
    this.initialRows = [...this.list.children].map((row) => row.cloneNode(true));
    this.noteTimers = new Map();
    this.filter = "all";
    this.recordedSeconds = 0;
    this.recording = false;
    this.replayProgress = 0;
    this.bind();
  }

  bind() {
    this.root.querySelectorAll("[data-rec-filter]").forEach((chip) => chip.addEventListener("click", () => this.setFilter(chip)));
    this.list.addEventListener("click", (event) => {
      const button = event.target.closest("[data-rec-action]");
      if (button) this.handleAction(button);
    });
    this.recorderButton.addEventListener("click", () => this.toggleRecording());
    this.replayToggle.addEventListener("click", () => this.toggleReplay());
    this.root.querySelector("[data-save-clip]").addEventListener("click", () => this.saveClip());
    this.root.addEventListener("keydown", (event) => {
      if (event.key === "F8") {
        event.preventDefault();
        this.saveClip();
      }
    });
    this.root.closest("[data-panel]")?.addEventListener("demo-reset", () => this.reset());
  }

  rows() {
    return [...this.list.children];
  }

  setFilter(chip) {
    this.filter = chip.dataset.recFilter;
    this.root.querySelectorAll("[data-rec-filter]").forEach((other) => other.setAttribute("aria-pressed", String(other === chip)));
    this.applyFilter();
  }

  applyFilter() {
    const rows = this.rows();
    rows.forEach((row) => (row.hidden = this.filter !== "all" && row.dataset.kind !== this.filter));
    this.empty.hidden = rows.some((row) => !row.hidden);
  }

  handleAction(button) {
    const row = button.closest(".rec__item");
    const action = button.dataset.recAction;
    if (action === "delete") this.confirmDelete(button, row);
    else this.showNote(row, action === "play" ? this.text.playNote : this.text.showNote);
  }

  showNote(row, note) {
    const meta = row.querySelector(".rec__meta");
    if (!meta.dataset.original) meta.dataset.original = meta.textContent;
    meta.textContent = note;
    clearTimeout(this.noteTimers.get(row));
    this.noteTimers.set(row, setTimeout(() => (meta.textContent = meta.dataset.original), NOTE_MS));
  }

  confirmDelete(button, row) {
    if (!button.classList.contains("is-confirming")) {
      button.classList.add("is-confirming");
      button.dataset.icon = button.innerHTML;
      button.textContent = button.dataset.confirmLabel;
      button.timer = setTimeout(() => this.cancelConfirm(button), CONFIRM_MS);
      return;
    }
    clearTimeout(button.timer);
    this.removeRow(row);
  }

  cancelConfirm(button) {
    button.classList.remove("is-confirming");
    button.innerHTML = button.dataset.icon;
  }

  removeRow(row) {
    row.classList.add("is-removing");
    setTimeout(() => {
      row.remove();
      this.applyFilter();
    }, REMOVE_MS);
  }

  nextNumber(kind) {
    const pattern = kind === "clip" ? /Clip-(\d+)/ : /Recording-(\d+)/;
    const numbers = this.rows().map((row) => Number(row.querySelector("strong").textContent.match(pattern)?.[1] ?? 0));
    return Math.max(0, ...numbers) + 1;
  }

  addRow(kind, name, duration, size) {
    const row = this.templates[kind].cloneNode(true);
    const oldName = row.querySelector("strong").textContent;
    row.classList.remove("is-removing");
    row.hidden = false;
    row.querySelector("strong").textContent = name;
    row.querySelector(".rec__meta").textContent = `${duration} · ${size} · ${this.text.today}`;
    row.querySelector(".rec__thumb").style.setProperty("--seed", [...name].reduce((sum, character) => sum + character.charCodeAt(0), 0) % 360);
    row.querySelectorAll("[aria-label]").forEach((element) => element.setAttribute("aria-label", element.getAttribute("aria-label").replace(oldName, name)));
    row.classList.add("is-new");
    this.list.prepend(row);
    this.applyFilter();
    return row;
  }

  toggleRecording() {
    this.recording = !this.recording;
    const card = this.recorderButton.closest(".rec__card");
    card.classList.toggle("is-recording", this.recording);
    this.recorderLabel.textContent = this.recording ? this.recorderButton.dataset.stop : this.recorderButton.dataset.start;
    if (this.recording) {
      this.recordedSeconds = 0;
      this.timer.textContent = "00:00";
      this.recordingTimer = setInterval(() => {
        this.recordedSeconds += 1;
        this.timer.textContent = `${pad(Math.floor(this.recordedSeconds / 60))}:${pad(this.recordedSeconds % 60)}`;
      }, 1000);
      return;
    }
    clearInterval(this.recordingTimer);
    const seconds = Math.max(this.recordedSeconds, 1);
    const name = `Recording-${this.nextNumber("recording")}.mp4`;
    this.addRow("recording", name, clock(seconds), `${Math.max(1, Math.round(seconds * RECORDING_SIZE_PER_SECOND))} MB`);
    this.timer.textContent = "00:00";
  }

  toggleReplay() {
    const on = this.replayToggle.getAttribute("aria-checked") !== "true";
    this.replayToggle.setAttribute("aria-checked", String(on));
    clearInterval(this.warmup);
    this.replayProgress = 0;
    this.replayBar.style.width = "0";
    if (!on) {
      this.replayStatus.textContent = this.text.warmup;
      return;
    }
    this.replayStatus.textContent = this.text.warmup;
    this.warmup = setInterval(() => {
      this.replayProgress += 1;
      this.replayBar.style.width = `${(this.replayProgress / WARMUP_STEPS) * 100}%`;
      if (this.replayProgress >= WARMUP_STEPS) {
        clearInterval(this.warmup);
        this.replayStatus.textContent = this.text.ready;
      }
    }, WARMUP_STEP_MS);
  }

  saveClip() {
    const ready = this.replayProgress >= WARMUP_STEPS;
    if (!ready) {
      this.replayStatus.textContent = this.text.notReady;
      return;
    }
    const name = this.text.newName.replace("{n}", this.nextNumber("clip"));
    this.addRow("clip", name, CLIP_DURATION, CLIP_SIZE);
    this.toast.querySelector(":scope > div > span").textContent = name;
    this.toast.classList.remove("is-visible");
    void this.toast.offsetWidth;
    this.toast.classList.add("is-visible");
    this.toast.setAttribute("aria-hidden", "false");
    clearTimeout(this.toastTimer);
    this.toastTimer = setTimeout(() => {
      this.toast.classList.remove("is-visible");
      this.toast.setAttribute("aria-hidden", "true");
    }, TOAST_MS);
  }

  reset() {
    if (this.recording) this.toggleRecording();
    if (this.replayToggle.getAttribute("aria-checked") === "true") this.toggleReplay();
    this.list.replaceChildren(...this.initialRows.map((row) => row.cloneNode(true)));
    this.filter = "all";
    this.root.querySelectorAll("[data-rec-filter]").forEach((chip) => chip.setAttribute("aria-pressed", String(chip.dataset.recFilter === "all")));
    this.timer.textContent = "00:00";
    this.applyFilter();
  }
}

export function init(root) {
  new RecordingsDemo(root);
}
