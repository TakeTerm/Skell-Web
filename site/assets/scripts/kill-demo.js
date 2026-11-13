import { whileVisible } from "./lazy.js";
import { prefersReducedMotion } from "./strings.js";

const TAU = Math.PI * 2;
const FRAME = 1 / 60;
const MAX_STEP = 1 / 20;
const LOOP_PAUSE = 0.9;
const TOAST_MS = 2600;
const STATIC_PROGRESS = 0.42;
const FIGURE_HEIGHT = 66;
const SPRITE = { width: 56, height: 72, originX: 28, originY: 66 };
const PALETTES = {
  execution: ["#ff4d62", "#ffd4da"],
  singularity: ["#8f64ff", "#e0d2ff"],
  "soul-pyre": ["#4ee0ff", "#d2f8ff"],
  samurai: ["#ff7fae", "#ffe6ef"],
};
const EFFECT_NAMES = Object.keys(PALETTES);

const ease = {
  out: (t) => 1 - (1 - t) ** 3,
  inOut: (t) => (t < 0.5 ? 4 * t ** 3 : 1 - (-2 * t + 2) ** 3 / 2),
  clamp: (t) => Math.min(Math.max(t, 0), 1),
};
const span = (p, from, to) => ease.clamp((p - from) / (to - from));

function randomGenerator(seed) {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6d2b79f5) >>> 0;
    let value = Math.imul(state ^ (state >>> 15), 1 | state);
    value ^= value + Math.imul(value ^ (value >>> 7), 61 | value);
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

function buildSprite() {
  const canvas = document.createElement("canvas");
  canvas.width = SPRITE.width;
  canvas.height = SPRITE.height;
  const context = canvas.getContext("2d");
  const rect = (x, y, w, h, color) => {
    context.fillStyle = color;
    context.fillRect(SPRITE.originX + x, SPRITE.originY + y, w, h);
  };
  rect(-7, -66, 14, 14, "#9aa3c7");
  rect(-7, -66, 14, 3, "#b9c1e0");
  rect(-7, -52, 14, 24, "#6f7aa8");
  rect(-7, -52, 14, 3, "#8590bb");
  rect(-7, -34, 14, 2, "#474f78");
  rect(-14, -52, 7, 24, "#838eb8");
  rect(7, -52, 7, 24, "#838eb8");
  rect(-7, -28, 7, 28, "#4a5280");
  rect(0, -28, 7, 28, "#3f4673");
  rect(-7, -4, 7, 4, "#2b3055");
  rect(0, -4, 7, 4, "#2b3055");
  return canvas;
}

class Particle {
  constructor(values) {
    Object.assign(this, { vx: 0, vy: 0, gravity: 0, drag: 0, size: 1.5, life: 1, age: 0, shape: "dot", spin: 0, angle: 0 }, values);
  }

  step(dt) {
    this.age += dt;
    this.vy += this.gravity * dt;
    const damping = Math.max(0, 1 - this.drag * dt);
    this.vx *= damping;
    this.vy *= damping;
    this.x += this.vx * dt;
    this.y += this.vy * dt;
    this.angle += this.spin * dt;
  }

  get alive() {
    return this.age < this.life;
  }

  get fade() {
    return 1 - this.age / this.life;
  }
}

class Scene {
  constructor(canvas, options) {
    this.canvas = canvas;
    this.context = canvas.getContext("2d");
    this.options = options;
    this.sprite = buildSprite();
    this.width = 0;
    this.height = 0;
    this.pixelRatio = 1;
    this.begin("execution");
  }

  resize(width, height) {
    this.pixelRatio = Math.min(devicePixelRatio || 1, 2);
    this.width = width;
    this.height = height;
    this.canvas.width = Math.round(width * this.pixelRatio);
    this.canvas.height = Math.round(height * this.pixelRatio);
  }

  begin(effect) {
    this.effect = effect;
    this.time = 0;
    this.particles = [];
    this.random = randomGenerator(Math.floor(Math.random() * 1e9));
    this.fired = new Set();
  }

  get duration() {
    return this.options.duration;
  }

  get progress() {
    return this.time / this.duration;
  }

  get finished() {
    return this.progress >= 1;
  }

  colors() {
    const { colorMode, primary, secondary } = this.options;
    if (colorMode === "custom") return [primary, secondary];
    if (colorMode === "theme") {
      const style = getComputedStyle(this.canvas);
      return [style.getPropertyValue("--accent").trim() || "#6c7bff", style.getPropertyValue("--accent-2").trim() || "#b45cff"];
    }
    return PALETTES[this.effect];
  }

  once(key, action) {
    if (this.fired.has(key)) return;
    this.fired.add(key);
    action();
  }

  emit(count, factory) {
    for (let index = 0; index < count; index++) this.particles.push(new Particle(factory(index, this.random)));
  }

  step(dt) {
    this.time += dt;
    EFFECTS[this.effect].step(this, this.progress);
    this.particles.forEach((particle) => particle.step(dt));
    this.particles = this.particles.filter((particle) => particle.alive);
  }

  advance(seconds) {
    for (let elapsed = 0; elapsed < seconds; elapsed += FRAME) this.step(FRAME);
  }

  render() {
    const { context, width, height, pixelRatio } = this;
    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    context.clearRect(0, 0, width, height);
    const unit = height * 0.0092 * this.options.scale;
    context.save();
    context.translate(width / 2, height * 0.86);
    context.scale(unit, unit);
    this.drawGround();
    EFFECTS[this.effect].draw(this, this.progress);
    this.drawParticles();
    context.restore();
  }

  drawGround() {
    const [main] = this.colors();
    const { context } = this;
    const gradient = context.createRadialGradient(0, 0, 0, 0, 0, 46);
    gradient.addColorStop(0, `${main}55`);
    gradient.addColorStop(1, "transparent");
    context.fillStyle = gradient;
    context.beginPath();
    context.ellipse(0, 1, 46, 8, 0, 0, TAU);
    context.fill();
  }

  drawParticles() {
    const { context } = this;
    const [main, light] = this.colors();
    context.save();
    for (const particle of this.particles) {
      context.globalAlpha = Math.max(0, particle.fade) * (particle.shape === "petal" ? 0.9 : 0.75);
      context.globalCompositeOperation = particle.shape === "petal" || !this.options.bloom ? "source-over" : "lighter";
      context.fillStyle = particle.tone === "light" ? light : main;
      context.save();
      context.translate(particle.x, particle.y);
      context.rotate(particle.angle);
      if (particle.shape === "petal") {
        context.beginPath();
        context.ellipse(0, 0, particle.size * 1.6, particle.size, 0, 0, TAU);
        context.fill();
      } else if (particle.shape === "shard") {
        context.fillRect(-particle.size, -particle.size * 0.4, particle.size * 2, particle.size * 0.8);
      } else {
        context.beginPath();
        context.arc(0, 0, particle.size * Math.max(0.35, particle.fade), 0, TAU);
        context.fill();
      }
      context.restore();
    }
    context.restore();
  }

  glow(color, blur) {
    if (!this.options.bloom) return;
    this.context.shadowColor = color;
    this.context.shadowBlur = blur;
  }

  clearGlow() {
    this.context.shadowBlur = 0;
  }

  drawFigure(alpha = 1, offsetX = 0, offsetY = 0) {
    const { context, sprite } = this;
    context.save();
    context.globalAlpha = alpha;
    context.imageSmoothingEnabled = false;
    context.drawImage(sprite, offsetX - SPRITE.originX, offsetY - SPRITE.originY);
    context.restore();
  }

  drawHalves(angle, spread, fade, tilt) {
    const { context } = this;
    const normal = [-Math.sin(angle), Math.cos(angle)];
    const along = [Math.cos(angle), Math.sin(angle)];
    const center = [0, -FIGURE_HEIGHT / 2];
    for (const side of [1, -1]) {
      context.save();
      context.beginPath();
      const far = 120;
      context.moveTo(center[0] - along[0] * far, center[1] - along[1] * far);
      context.lineTo(center[0] + along[0] * far, center[1] + along[1] * far);
      context.lineTo(center[0] + along[0] * far + normal[0] * far * side, center[1] + along[1] * far + normal[1] * far * side);
      context.lineTo(center[0] - along[0] * far + normal[0] * far * side, center[1] - along[1] * far + normal[1] * far * side);
      context.closePath();
      context.clip();
      context.translate(center[0] + normal[0] * spread * side, center[1] + normal[1] * spread * side);
      context.rotate(tilt * side);
      context.translate(-center[0], -center[1]);
      this.drawFigure(fade);
      context.restore();
    }
  }

  drawSlash(angle, reach, alpha, thickness = 1.6) {
    const { context } = this;
    const [main, light] = this.colors();
    const length = 74 * reach;
    const dx = Math.cos(angle) * length;
    const dy = Math.sin(angle) * length;
    context.save();
    context.globalAlpha = alpha;
    context.lineCap = "round";
    this.glow(main, 22);
    context.strokeStyle = main;
    context.lineWidth = thickness * 2.4;
    context.beginPath();
    context.moveTo(-dx, -FIGURE_HEIGHT / 2 - dy);
    context.lineTo(dx, -FIGURE_HEIGHT / 2 + dy);
    context.stroke();
    context.strokeStyle = light;
    context.lineWidth = thickness;
    context.stroke();
    this.clearGlow();
    context.restore();
  }

  drawOrb(x, y, radius, alpha) {
    const { context } = this;
    const [main, light] = this.colors();
    context.save();
    context.globalAlpha = alpha;
    this.glow(main, 36);
    context.fillStyle = "#05060d";
    context.beginPath();
    context.arc(x, y, radius, 0, TAU);
    context.fill();
    context.lineWidth = 1.6;
    context.strokeStyle = light;
    context.stroke();
    context.lineWidth = 0.8;
    context.strokeStyle = main;
    context.beginPath();
    context.arc(x, y, radius * 1.45, this.time * 4, this.time * 4 + 4.2);
    context.stroke();
    this.clearGlow();
    context.restore();
  }

  drawRing(radius, alpha) {
    const { context } = this;
    const [main] = this.colors();
    context.save();
    context.globalAlpha = alpha;
    this.glow(main, 20);
    context.strokeStyle = main;
    context.lineWidth = 2;
    context.beginPath();
    context.ellipse(0, -FIGURE_HEIGHT / 2, radius, radius, 0, 0, TAU);
    context.stroke();
    this.clearGlow();
    context.restore();
  }
}

const burst = (scene, x, y, count, speed, extra = {}) =>
  scene.emit(count, (_, random) => {
    const angle = random() * TAU;
    const power = speed * (0.35 + random() * 0.65);
    return { x, y, vx: Math.cos(angle) * power, vy: Math.sin(angle) * power, size: 0.8 + random() * 1.4, life: 0.5 + random() * 0.7, drag: 1.6, gravity: 40, tone: random() > 0.5 ? "light" : "main", ...extra };
  });

const EFFECTS = {
  execution: {
    angle: -0.5,
    step(scene, p) {
      if (p > 0.24) scene.once("sparks", () => burst(scene, 0, -33, 70, 130));
    },
    draw(scene, p) {
      const angle = this.angle;
      if (p < 0.26) {
        scene.drawFigure(1, 0, -Math.sin(p * 26) * 0.5);
        const reach = ease.out(span(p, 0.08, 0.24));
        if (reach > 0) scene.drawSlash(angle, reach, 1);
        return;
      }
      const open = ease.out(span(p, 0.26, 0.7));
      scene.drawSlash(angle, 1, 1 - span(p, 0.26, 0.4));
      scene.drawHalves(angle, open * 20, 1 - span(p, 0.6, 1), open * 0.16);
    },
  },
  singularity: {
    step(scene, p) {
      if (p < 0.34 && scene.random() > 0.35) {
        const angle = scene.random() * TAU;
        const radius = 58 + scene.random() * 14;
        scene.emit(1, () => ({ x: Math.cos(angle) * radius, y: -50 + Math.sin(angle) * radius * 0.7, vx: -Math.cos(angle) * 90, vy: Math.sin(angle) * -63, life: 0.55, size: 1.2, tone: "light" }));
      }
      if (p > 0.72) scene.once("collapse", () => burst(scene, 0, -50, 60, 120));
    },
    draw(scene, p) {
      const grow = ease.out(span(p, 0, 0.3));
      const pull = ease.inOut(span(p, 0.3, 0.72));
      const orbRadius = 10 * grow * (1 - span(p, 0.72, 0.78));
      if (p < 0.72) {
        const context = scene.context;
        context.save();
        context.translate(0, -50 * pull * 0.6 - 33 * pull * 0.4);
        const shrink = 1 - pull * 0.9;
        context.scale(shrink, shrink * (1 + pull * 0.6));
        context.translate(0, 33 * pull);
        scene.drawFigure(1 - pull * 0.4);
        context.restore();
      }
      if (orbRadius > 0.2) scene.drawOrb(0, -50, orbRadius, 1);
      if (p > 0.72) scene.drawRing(8 + ease.out(span(p, 0.72, 1)) * 60, 1 - span(p, 0.72, 1));
    },
  },
  "soul-pyre": {
    step(scene, p) {
      const line = -FIGURE_HEIGHT * span(p, 0.1, 0.62);
      if (p > 0.1 && p < 0.66) {
        scene.emit(2, (_, random) => ({ x: (random() - 0.5) * 18, y: line + random() * 8, vx: (random() - 0.5) * 14, vy: -26 - random() * 34, life: 0.7 + random() * 0.6, size: 0.9 + random() * 1.3, drag: 0.6, tone: random() > 0.4 ? "main" : "light" }));
      }
      if (p > 0.45 && p < 0.9 && scene.random() > 0.8) {
        scene.emit(1, (_, random) => ({ x: (random() - 0.5) * 12, y: -10, vx: 0, vy: -40 - random() * 20, life: 1.4, size: 2.6, drag: 0.2, tone: "light", spin: 2 }));
      }
    },
    draw(scene, p) {
      const gone = span(p, 0.1, 0.62);
      const context = scene.context;
      context.save();
      context.beginPath();
      context.rect(-40, -FIGURE_HEIGHT * (1 - gone) - 2, 80, 80);
      context.clip();
      scene.drawFigure(1 - gone * 0.3);
      context.restore();
      if (p > 0.1 && p < 0.7) {
        const [main] = scene.colors();
        const y = -FIGURE_HEIGHT * gone;
        context.save();
        scene.glow(main, 14);
        context.fillStyle = main;
        context.fillRect(-9, y - 0.6, 18, 1.2);
        scene.clearGlow();
        context.restore();
      }
    },
  },
  samurai: {
    cuts: [-0.9, 0.7, -0.2],
    step(scene, p) {
      this.cuts.forEach((_, index) => {
        if (p > 0.1 + index * 0.1) scene.once(`cut-${index}`, () => burst(scene, 0, -33, 16, 80));
      });
      if (p > 0.42) scene.once("petals", () => scene.emit(36, (_, random) => ({ x: (random() - 0.5) * 30, y: -30 - random() * 20, vx: (random() - 0.5) * 40, vy: -10 - random() * 20, gravity: 22, life: 1.3 + random() * 0.8, size: 1.3, shape: "petal", spin: (random() - 0.5) * 6, drag: 0.8, tone: "light" })));
    },
    draw(scene, p) {
      const slashes = this.cuts.map((angle, index) => ({ angle, start: 0.1 + index * 0.1 }));
      if (p < 0.42) scene.drawFigure(1, Math.sin(p * 60) * 0.4, 0);
      for (const { angle, start } of slashes) {
        const local = span(p, start, start + 0.08);
        if (local > 0 && local < 1) scene.drawSlash(angle, ease.out(local), 1 - local * 0.6, 1.3);
      }
      if (p >= 0.42) {
        const open = ease.out(span(p, 0.42, 0.85));
        scene.drawHalves(this.cuts.at(-1), open * 16, 1 - span(p, 0.65, 1), open * 0.12);
      }
    },
  },
};

const OPTION_LABELS = { duration: (value) => `${Number(value).toFixed(1)} s`, scale: (value) => `${Number(value).toFixed(1)}×` };

function createOptions() {
  return { effect: "random", colorMode: "style", primary: "#6597ff", secondary: "#ff8061", duration: 2.5, scale: 1, bloom: true, loop: true };
}

class Player {
  constructor(canvas, options, hooks = {}) {
    this.canvas = canvas;
    this.options = options;
    this.hooks = hooks;
    this.scene = new Scene(canvas, options);
    this.visible = false;
    this.running = false;
    this.pauseLeft = 0;
    this.reduced = prefersReducedMotion();
    new ResizeObserver(() => this.fit()).observe(canvas);
    whileVisible(canvas, (visible) => {
      this.visible = visible;
      if (visible) this.start();
    });
  }

  fit() {
    const box = this.canvas.getBoundingClientRect();
    if (!box.width || !box.height) return;
    this.scene.resize(box.width, box.height);
    if (!this.running) this.scene.render();
  }

  pickEffect() {
    const effect = this.options.effect;
    return effect === "random" ? EFFECT_NAMES[Math.floor(Math.random() * EFFECT_NAMES.length)] : effect;
  }

  play() {
    this.scene.begin(this.pickEffect());
    this.pauseLeft = 0;
    if (this.reduced) {
      this.scene.advance(this.options.duration * STATIC_PROGRESS);
      this.scene.render();
      return;
    }
    this.start();
  }

  start() {
    if (this.running || this.reduced || !this.visible) return;
    this.running = true;
    this.last = performance.now();
    requestAnimationFrame((now) => this.frame(now));
  }

  frame(now) {
    if (!this.visible) {
      this.running = false;
      return;
    }
    const dt = Math.min((now - this.last) / 1000, MAX_STEP);
    this.last = now;
    if (this.scene.finished) this.rest(dt);
    else this.scene.step(dt);
    this.scene.render();
    if (this.scene.finished && !this.options.loop && !this.scene.particles.length) {
      this.running = false;
      return;
    }
    requestAnimationFrame((time) => this.frame(time));
  }

  rest(dt) {
    this.scene.particles.forEach((particle) => particle.step(dt));
    this.scene.particles = this.scene.particles.filter((particle) => particle.alive);
    if (!this.options.loop) return;
    if (this.pauseLeft === 0) {
      this.pauseLeft = LOOP_PAUSE;
      this.hooks.onFinish?.();
    }
    this.pauseLeft -= dt;
    if (this.pauseLeft <= 0) this.play();
  }
}

class KillDemo {
  constructor(root) {
    this.root = root;
    this.options = createOptions();
    this.player = new Player(root.querySelector("[data-kill-canvas]"), this.options);
    this.bind();
    this.syncOutputs();
    this.player.play();
  }

  bind() {
    const { root } = this;
    root.querySelectorAll("[data-effect]").forEach((chip) =>
      chip.addEventListener("click", () => {
        this.options.effect = chip.dataset.effect;
        root.querySelectorAll("[data-effect]").forEach((other) => other.setAttribute("aria-pressed", String(other === chip)));
        this.player.play();
      })
    );
    root.querySelectorAll("[data-color-mode]").forEach((button) =>
      button.addEventListener("click", () => {
        this.options.colorMode = button.dataset.colorMode;
        root.querySelectorAll("[data-color-mode]").forEach((other) => other.setAttribute("aria-pressed", String(other === button)));
        root.querySelector("[data-custom-colors]").hidden = this.options.colorMode !== "custom";
        this.refresh();
      })
    );
    root.querySelectorAll("[data-kill-option]").forEach((input) =>
      input.addEventListener("input", () => {
        this.options[input.dataset.killOption] = Number(input.value);
        this.syncOutputs();
        this.refresh();
      })
    );
    root.querySelectorAll("[data-kill-toggle]").forEach((toggle) =>
      toggle.addEventListener("click", () => {
        const on = toggle.getAttribute("aria-checked") !== "true";
        toggle.setAttribute("aria-checked", String(on));
        this.options[toggle.dataset.killToggle] = on;
        if (on) this.player.start();
        this.refresh();
      })
    );
    root.querySelectorAll("[data-kill-color]").forEach((input) =>
      input.addEventListener("input", () => {
        this.options[input.dataset.killColor] = input.value;
        this.refresh();
      })
    );
    root.querySelector("[data-kill-replay]").addEventListener("click", () => this.player.play());
    root.closest("[data-panel]")?.addEventListener("demo-reset", () => this.reset());
  }

  refresh() {
    if (!this.player.running) this.player.scene.render();
  }

  syncOutputs() {
    this.root.querySelectorAll("[data-kill-option]").forEach((input) => {
      const output = input.parentElement.querySelector("output");
      output.textContent = OPTION_LABELS[input.dataset.killOption](input.value);
      const span = input.max - input.min;
      input.style.setProperty("--fill", `${((input.value - input.min) / span) * 100}%`);
    });
  }

  reset() {
    Object.assign(this.options, createOptions());
    this.root.querySelectorAll("[data-kill-option]").forEach((input) => (input.value = this.options[input.dataset.killOption]));
    this.root.querySelectorAll("[data-kill-toggle]").forEach((toggle) => toggle.setAttribute("aria-checked", String(this.options[toggle.dataset.killToggle])));
    this.root.querySelectorAll("[data-kill-color]").forEach((input) => (input.value = this.options[input.dataset.killColor]));
    this.root.querySelectorAll("[data-effect]").forEach((chip) => chip.setAttribute("aria-pressed", String(chip.dataset.effect === "random")));
    this.root.querySelectorAll("[data-color-mode]").forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.colorMode === "style")));
    this.root.querySelector("[data-custom-colors]").hidden = true;
    this.syncOutputs();
    this.player.play();
  }
}

function initMini(canvas) {
  const toast = canvas.parentElement.querySelector("[data-mini-toast]");
  const options = { ...createOptions(), duration: 2.2 };
  const player = new Player(canvas, options, {
    onFinish() {
      toast.classList.add("is-visible");
      setTimeout(() => toast.classList.remove("is-visible"), TOAST_MS);
    },
  });
  player.play();
}

export function init(element) {
  if (element.hasAttribute("data-kill-mini")) initMini(element);
  else new KillDemo(element);
}
