import { readStrings, format } from "./strings.js";

const SCALE_STEP = 0.05;
const SCALE_RANGE = [0.5, 2];
const HISTORY_LIMIT = 60;
const NUDGE = 1;
const NUDGE_LARGE = 10;
const BAR_MARGIN = 4;
const SETTLE_MS = 420;
const ARROW_DIRECTIONS = {
  ArrowLeft: [-1, 0],
  ArrowRight: [1, 0],
  ArrowUp: [0, -1],
  ArrowDown: [0, 1],
};
const VERTICAL = { t: 0, m: 0.5, b: 1 };
const HORIZONTAL = { l: 0, c: 0.5, r: 1 };

const clamp = (value, low, high) => Math.min(Math.max(value, low), high);
const roundToStep = (value) => Math.round(value / SCALE_STEP) * SCALE_STEP;

class Widget {
  constructor(element) {
    const [vertical, horizontal] = element.dataset.anchor.split("-");
    this.element = element;
    this.kind = element.dataset.widget;
    this.name = element.dataset.name ?? this.kind;
    this.initial = {
      vertical,
      horizontal,
      dx: Number(element.dataset.dx),
      dy: Number(element.dataset.dy),
      scale: 1,
      hidden: false,
    };
    this.state = { ...this.initial };
  }

  get width() {
    return this.element.offsetWidth * this.state.scale;
  }

  get height() {
    return this.element.offsetHeight * this.state.scale;
  }

  position(stage) {
    const { vertical, horizontal, dx, dy } = this.state;
    const x = (stage.width - this.width) * HORIZONTAL[horizontal] + (horizontal === "r" ? -dx : dx);
    const y = (stage.height - this.height) * VERTICAL[vertical] + (vertical === "b" ? -dy : dy);
    return { x, y };
  }

  anchorAt(x, y, stage) {
    const centerX = (x + this.width / 2) / stage.width;
    const centerY = (y + this.height / 2) / stage.height;
    const horizontal = centerX < 1 / 3 ? "l" : centerX > 2 / 3 ? "r" : "c";
    const vertical = centerY < 1 / 3 ? "t" : centerY > 2 / 3 ? "b" : "m";
    const baseX = (stage.width - this.width) * HORIZONTAL[horizontal];
    const baseY = (stage.height - this.height) * VERTICAL[vertical];
    this.state.horizontal = horizontal;
    this.state.vertical = vertical;
    this.state.dx = Math.round(horizontal === "r" ? baseX - x : x - baseX);
    this.state.dy = Math.round(vertical === "b" ? baseY - y : y - baseY);
  }
}

class HudEditor {
  constructor(root) {
    this.root = root;
    this.mini = root.hasAttribute("data-mini");
    this.text = readStrings().hud;
    this.stage = root.querySelector("[data-stage]");
    this.guides = { x: root.querySelector('[data-guide="x"]'), y: root.querySelector('[data-guide="y"]') };
    this.resizeHandle = root.querySelector("[data-resize]");
    this.bar = root.querySelector("[data-bar]");
    this.selectedLabel = root.querySelector("[data-selected-label]");
    this.anchorLabel = root.querySelector("[data-anchor-label]");
    this.announcer = root.querySelector("[data-announce]");
    this.actions = Object.fromEntries([...root.querySelectorAll("[data-action]")].map((button) => [button.dataset.action, button]));
    this.widgets = [...root.querySelectorAll("[data-widget]")].map((element) => new Widget(element));
    this.snapThreshold = Number(root.dataset.snap);
    this.gap = Number(root.dataset.gap);
    this.selected = null;
    this.undoStack = [];
    this.redoStack = [];
    this.stageBox = { width: 0, height: 0 };
    this.bind();
    new ResizeObserver(() => this.layoutAll()).observe(this.stage);
  }

  bind() {
    for (const widget of this.widgets) {
      widget.element.addEventListener("pointerdown", (event) => this.startDrag(event, widget));
      widget.element.addEventListener("keydown", (event) => this.handleWidgetKey(event, widget));
      widget.element.addEventListener("focus", () => this.select(widget));
    }
    this.stage.addEventListener("pointerdown", (event) => {
      if (!event.target.closest("[data-widget], [data-bar], [data-resize]")) this.select(null);
    });
    this.root.addEventListener("keydown", (event) => this.handleHistoryKey(event));
    this.root.closest("[data-panel]")?.addEventListener("demo-reset", () => this.resetLayout(false));
    if (this.mini) return;
    this.resizeHandle.addEventListener("pointerdown", (event) => this.startResize(event));
    this.actions.undo.addEventListener("click", () => this.step(this.undoStack, this.redoStack, this.text.undone));
    this.actions.redo.addEventListener("click", () => this.step(this.redoStack, this.undoStack, this.text.redone));
    this.actions.reset.addEventListener("click", () => this.resetLayout(true));
    this.root.querySelectorAll("[data-widget-toggle]").forEach((toggle) => toggle.addEventListener("click", () => this.toggleVisibility(toggle)));
    this.bindBar();
  }

  measure() {
    const box = this.stage.getBoundingClientRect();
    this.stageBox = { width: box.width, height: box.height, left: box.left, top: box.top };
  }

  layoutAll() {
    this.measure();
    this.widgets.forEach((widget) => this.place(widget));
    this.updateHandle();
  }

  place(widget) {
    const { x, y } = widget.position(this.stageBox);
    this.setPosition(widget, x, y);
  }

  setPosition(widget, x, y) {
    const style = widget.element.style;
    style.setProperty("--x", `${x}px`);
    style.setProperty("--y", `${y}px`);
    style.setProperty("--pv-scale", widget.state.scale);
    widget.current = { x, y };
  }

  select(widget) {
    this.selected = widget;
    this.widgets.forEach((other) => other.element.classList.toggle("is-selected", other === widget));
    if (this.selectedLabel) this.selectedLabel.textContent = widget ? format(this.text.selected, { name: widget.name }) : this.text.nothingSelected;
    this.updateAnchorLabel();
    this.updateHandle();
  }

  updateAnchorLabel() {
    if (!this.anchorLabel) return;
    const widget = this.selected;
    if (!widget) {
      this.anchorLabel.textContent = "";
      return;
    }
    const { vertical, horizontal, dx, dy } = widget.state;
    const label = format(this.text.anchored, { vertical: this.text.anchors[vertical], horizontal: this.text.anchors[horizontal] });
    this.anchorLabel.textContent = `${label} · ${dx}, ${dy} px`;
  }

  updateHandle() {
    if (!this.resizeHandle) return;
    const widget = this.selected;
    const visible = Boolean(widget) && !widget.state.hidden;
    this.resizeHandle.classList.toggle("is-visible", visible);
    if (!visible) return;
    this.resizeHandle.style.left = `${widget.current.x + widget.width}px`;
    this.resizeHandle.style.top = `${widget.current.y + widget.height}px`;
  }

  snapshot() {
    return this.widgets.map((widget) => ({ ...widget.state }));
  }

  restore(snapshot) {
    snapshot.forEach((state, index) => {
      const widget = this.widgets[index];
      widget.state = { ...state };
      this.applyVisibility(widget);
    });
    this.settle(() => this.layoutAll());
    this.updateAnchorLabel();
  }

  settle(change) {
    this.widgets.forEach((widget) => widget.element.classList.add("is-settling"));
    change();
    clearTimeout(this.settleTimer);
    this.settleTimer = setTimeout(() => this.widgets.forEach((widget) => widget.element.classList.remove("is-settling")), SETTLE_MS);
  }

  record(before) {
    if (JSON.stringify(before) === JSON.stringify(this.snapshot())) return;
    this.undoStack.push(before);
    if (this.undoStack.length > HISTORY_LIMIT) this.undoStack.shift();
    this.redoStack = [];
    this.updateHistoryButtons();
  }

  step(from, to, message) {
    if (!from.length) return;
    to.push(this.snapshot());
    this.restore(from.pop());
    this.updateHistoryButtons();
    this.announce(message);
  }

  updateHistoryButtons() {
    if (this.mini) return;
    this.actions.undo.disabled = !this.undoStack.length;
    this.actions.redo.disabled = !this.redoStack.length;
  }

  announce(message) {
    if (this.announcer) this.announcer.textContent = message;
  }

  applyVisibility(widget) {
    const hidden = widget.state.hidden;
    widget.element.classList.toggle("is-hidden", hidden);
    widget.element.tabIndex = hidden ? -1 : 0;
    widget.element.toggleAttribute("aria-hidden", hidden);
    this.root.querySelector(`[data-widget-toggle="${widget.kind}"]`)?.setAttribute("aria-checked", String(!hidden));
    if (hidden && this.selected === widget) this.select(null);
  }

  setHidden(widget, hidden) {
    const before = this.snapshot();
    widget.state.hidden = hidden;
    this.applyVisibility(widget);
    this.record(before);
    this.announce(format(hidden ? this.text.hiddenWidget : this.text.shownWidget, { name: widget.name }));
  }

  toggleVisibility(toggle) {
    const widget = this.widgets.find((item) => item.kind === toggle.dataset.widgetToggle);
    this.setHidden(widget, !widget.state.hidden);
    if (!widget.state.hidden) this.select(widget);
  }

  resetLayout(recordable) {
    const before = this.snapshot();
    this.settle(() => {
      this.widgets.forEach((widget) => {
        widget.state = { ...widget.initial };
        this.applyVisibility(widget);
      });
      this.layoutAll();
    });
    this.select(null);
    if (recordable) {
      this.record(before);
      this.announce(this.text.resetDone);
    } else {
      this.undoStack = [];
      this.redoStack = [];
      this.updateHistoryButtons();
    }
    this.returnBar();
  }

  snapTargets(moving) {
    const stage = this.stageBox;
    const xs = [0, stage.width / 2, stage.width];
    const ys = [0, stage.height / 2, stage.height];
    for (const other of this.widgets) {
      if (other === moving || other.state.hidden) continue;
      const { x, y } = other.current;
      xs.push(x, x + other.width / 2, x + other.width, x - this.gap, x + other.width + this.gap);
      ys.push(y, y + other.height / 2, y + other.height, y - this.gap, y + other.height + this.gap);
    }
    return { xs, ys };
  }

  snapAxis(position, size, targets, threshold) {
    const edges = [position, position + size / 2, position + size];
    let best = { distance: threshold + 1, shift: 0, line: null };
    for (const edge of edges) {
      for (const target of targets) {
        const distance = Math.abs(target - edge);
        if (distance < best.distance) best = { distance, shift: target - edge, line: target };
      }
    }
    return best.distance <= threshold ? best : { shift: 0, line: null };
  }

  showGuide(axis, line) {
    const guide = this.guides[axis];
    guide.classList.toggle("is-visible", line !== null);
    if (line !== null) guide.style[axis === "x" ? "left" : "top"] = `${line}px`;
  }

  startDrag(event, widget) {
    if (event.button > 0 || widget.state.hidden) return;
    this.measure();
    this.select(widget);
    const element = widget.element;
    element.setPointerCapture(event.pointerId);
    const before = this.snapshot();
    const origin = { ...widget.current };
    const start = { x: event.clientX, y: event.clientY };
    const targets = this.snapTargets(widget);
    let moved = false;
    const move = (moveEvent) => {
      const distance = Math.hypot(moveEvent.clientX - start.x, moveEvent.clientY - start.y);
      if (!moved && distance < 3) return;
      if (!moved) {
        moved = true;
        element.classList.add("is-dragging");
      }
      let x = clamp(origin.x + moveEvent.clientX - start.x, 0, this.stageBox.width - widget.width);
      let y = clamp(origin.y + moveEvent.clientY - start.y, 0, this.stageBox.height - widget.height);
      if (moveEvent.shiftKey) {
        this.showGuide("x", null);
        this.showGuide("y", null);
      } else {
        const snapX = this.snapAxis(x, widget.width, targets.xs, this.snapThreshold);
        const snapY = this.snapAxis(y, widget.height, targets.ys, this.snapThreshold);
        x = clamp(x + snapX.shift, 0, this.stageBox.width - widget.width);
        y = clamp(y + snapY.shift, 0, this.stageBox.height - widget.height);
        this.showGuide("x", snapX.line);
        this.showGuide("y", snapY.line);
      }
      this.setPosition(widget, x, y);
      this.updateHandle();
    };
    const end = () => {
      element.removeEventListener("pointermove", move);
      element.removeEventListener("pointerup", end);
      element.removeEventListener("pointercancel", end);
      element.classList.remove("is-dragging");
      this.showGuide("x", null);
      this.showGuide("y", null);
      if (!moved) return;
      widget.anchorAt(widget.current.x, widget.current.y, this.stageBox);
      this.place(widget);
      this.updateAnchorLabel();
      this.record(before);
      this.announce(format(this.text.moved, { name: widget.name }));
    };
    element.addEventListener("pointermove", move);
    element.addEventListener("pointerup", end);
    element.addEventListener("pointercancel", end);
  }

  startResize(event) {
    const widget = this.selected;
    if (!widget) return;
    event.preventDefault();
    this.resizeHandle.setPointerCapture(event.pointerId);
    const before = this.snapshot();
    const startScale = widget.state.scale;
    const startWidth = widget.width;
    const startX = event.clientX;
    const move = (moveEvent) => {
      const ratio = (startWidth + moveEvent.clientX - startX) / startWidth;
      widget.state.scale = clamp(roundToStep(startScale * ratio), ...SCALE_RANGE);
      const anchored = widget.current;
      this.setPosition(widget, anchored.x, anchored.y);
      this.updateHandle();
    };
    const end = () => {
      this.resizeHandle.removeEventListener("pointermove", move);
      this.resizeHandle.removeEventListener("pointerup", end);
      this.resizeHandle.removeEventListener("pointercancel", end);
      this.measure();
      widget.anchorAt(widget.current.x, widget.current.y, this.stageBox);
      this.place(widget);
      this.updateHandle();
      this.updateAnchorLabel();
      this.record(before);
    };
    this.resizeHandle.addEventListener("pointermove", move);
    this.resizeHandle.addEventListener("pointerup", end);
    this.resizeHandle.addEventListener("pointercancel", end);
  }

  nudge(widget, dx, dy) {
    const before = this.snapshot();
    this.measure();
    const x = clamp(widget.current.x + dx, 0, this.stageBox.width - widget.width);
    const y = clamp(widget.current.y + dy, 0, this.stageBox.height - widget.height);
    widget.anchorAt(x, y, this.stageBox);
    this.place(widget);
    this.updateHandle();
    this.updateAnchorLabel();
    this.record(before);
  }

  handleWidgetKey(event, widget) {
    if (event.ctrlKey || event.metaKey || event.altKey) return;
    if (event.key in ARROW_DIRECTIONS) {
      event.preventDefault();
      const [dx, dy] = ARROW_DIRECTIONS[event.key];
      const amount = event.shiftKey ? NUDGE_LARGE : NUDGE;
      this.nudge(widget, dx * amount, dy * amount);
    } else if (event.key === "Delete" || event.key === "Backspace") {
      event.preventDefault();
      this.setHidden(widget, true);
      this.root.querySelector(`[data-widget-toggle="${widget.kind}"]`)?.focus({ preventScroll: true });
    } else if (event.key.toLowerCase() === "r") {
      const before = this.snapshot();
      widget.state = { ...widget.initial, hidden: widget.state.hidden };
      this.settle(() => this.place(widget));
      this.updateHandle();
      this.updateAnchorLabel();
      this.record(before);
    }
  }

  handleHistoryKey(event) {
    if (this.mini || !(event.ctrlKey || event.metaKey)) return;
    const key = event.key.toLowerCase();
    if (key === "z" && !event.shiftKey) {
      event.preventDefault();
      this.step(this.undoStack, this.redoStack, this.text.undone);
    } else if (key === "y" || (key === "z" && event.shiftKey)) {
      event.preventDefault();
      this.step(this.redoStack, this.undoStack, this.text.redone);
    }
  }

  bindBar() {
    const grip = this.bar.querySelector("[data-bar-handle]");
    this.barOffset = { x: 0, y: 0 };
    grip.addEventListener("dblclick", () => this.returnBar());
    grip.addEventListener("pointerdown", (event) => {
      this.bar.classList.remove("is-returning");
      grip.setPointerCapture(event.pointerId);
      const stage = this.stage.getBoundingClientRect();
      const box = this.bar.getBoundingClientRect();
      const start = { x: event.clientX, y: event.clientY, offset: { ...this.barOffset } };
      const move = (moveEvent) => {
        const dx = clamp(moveEvent.clientX - start.x, stage.left + BAR_MARGIN - box.left, stage.right - BAR_MARGIN - box.right);
        const dy = clamp(moveEvent.clientY - start.y, stage.top + BAR_MARGIN - box.top, stage.bottom - BAR_MARGIN - box.bottom);
        this.setBarOffset(start.offset.x + dx, start.offset.y + dy);
      };
      const end = () => {
        grip.removeEventListener("pointermove", move);
        grip.removeEventListener("pointerup", end);
        grip.removeEventListener("pointercancel", end);
      };
      grip.addEventListener("pointermove", move);
      grip.addEventListener("pointerup", end);
      grip.addEventListener("pointercancel", end);
    });
  }

  setBarOffset(x, y) {
    this.barOffset = { x, y };
    this.bar.style.setProperty("--bar-x", `${x}px`);
    this.bar.style.setProperty("--bar-y", `${y}px`);
  }

  returnBar() {
    if (!this.bar || (!this.barOffset.x && !this.barOffset.y)) return;
    this.bar.classList.add("is-returning");
    this.setBarOffset(0, 0);
    setTimeout(() => this.bar.classList.remove("is-returning"), SETTLE_MS + 100);
  }
}

export function init(root) {
  new HudEditor(root);
}
