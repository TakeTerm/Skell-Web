import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "src" / "assets" / "brand"
FONTS = ROOT / "src" / "assets" / "fonts"
BACKGROUND = "#07080e"
ICON_SIZES = {"favicon-32.png": 32, "apple-touch-icon.png": 180, "icon-192.png": 192, "icon-512.png": 512}


def mark_geometry():
    source = (BRAND / "skell-mark.svg").read_text()
    path = re.search(r' d="([^"]+)"', source).group(1)
    width, height = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', source).groups())
    return path, width, height


def icon_svg(padding):
    path, width, height = mark_geometry()
    size = 512
    scale = (size * (1 - 2 * padding)) / height
    x = (size - width * scale) / 2
    y = (size - height * scale) / 2
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">'
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8f9bff"/><stop offset="1" stop-color="#c06bff"/></linearGradient></defs>'
        f'<rect width="{size}" height="{size}" rx="112" fill="{BACKGROUND}"/>'
        f'<path transform="translate({x:.2f} {y:.2f}) scale({scale:.4f})" fill="url(#g)" fill-rule="evenodd" d="{path}"/></svg>'
    )


def write_icons():
    (BRAND / "favicon.svg").write_text(icon_svg(0.2))
    source = BRAND / "icon-source.svg"
    source.write_text(icon_svg(0.22))
    for name, size in ICON_SIZES.items():
        subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(source), "-o", str(BRAND / name)], check=True)
    source.unlink()
    manifest = {
        "name": "Skell Client",
        "short_name": "Skell",
        "start_url": "/",
        "display": "standalone",
        "background_color": BACKGROUND,
        "theme_color": BACKGROUND,
        "icons": [
            {"src": "/assets/brand/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/brand/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    (BRAND / "site.webmanifest").write_text(json.dumps(manifest, indent=2) + "\n")


def social_card(language, config):
    hero = json.loads((ROOT / "content" / language / "landing.json").read_text())["hero"]
    path, width, height = mark_geometry()
    title = hero["title"].replace("*", "")
    note = hero["note"]
    fonts = "".join(
        f'@font-face{{font-family:"{family}";src:url("file://{FONTS / file}");font-weight:{weight}}}'
        for family, file, weight in (
            ("Bricolage", "bricolage-grotesque-latin-wght-normal.woff2", "200 800"),
            ("Inter", "inter-latin-wght-normal.woff2", "100 900"),
            ("Mono", "jetbrains-mono-latin-500-normal.woff2", "500"),
        )
    )
    return f"""<!doctype html><meta charset="utf-8"><style>{fonts}
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;overflow:hidden;background:{BACKGROUND};color:#f3f4fb;font-family:Inter;position:relative}}
.glow{{position:absolute;inset:0;background:radial-gradient(60% 80% at 82% 40%,rgba(124,118,255,.32),transparent),radial-gradient(50% 60% at 10% 100%,rgba(180,92,255,.18),transparent)}}
.mark{{position:absolute;right:96px;top:90px;width:{width * 1.9:.0f}px;height:{height * 1.9:.0f}px;opacity:.95}}
.copy{{position:absolute;left:84px;top:84px;bottom:84px;width:640px;display:flex;flex-direction:column;justify-content:space-between}}
.brand{{font-family:Bricolage;font-weight:700;font-size:34px}}
.brand span{{font-weight:300;color:#aeb3d6}}
h1{{font-family:Bricolage;font-weight:800;font-size:148px;line-height:.95;letter-spacing:-.03em}}
h1 em{{font-style:normal;background:linear-gradient(110deg,#8f9bff,#c06bff);-webkit-background-clip:text;color:transparent}}
.meta{{font-family:Mono;font-size:22px;letter-spacing:.06em;color:#9aa0c8;text-transform:uppercase}}
</style><div class="glow"></div>
<svg class="mark" viewBox="0 0 {width} {height}"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8f9bff"/><stop offset="1" stop-color="#c06bff"/></linearGradient></defs><path fill="url(#g)" fill-rule="evenodd" d="{path}"/></svg>
<div class="copy"><div class="brand">Skell <span>Client</span></div>
<h1>{hero["title"].replace("*", "<em>", 1).replace("*", "</em>", 1)}</h1>
<div class="meta">Fabric · Minecraft {config["minecraft"]} · {note}</div></div>"""


async def write_social_cards():
    from playwright.async_api import async_playwright

    config = json.loads((ROOT / "site.config.json").read_text())
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        page = await browser.new_page(viewport={"width": 1200, "height": 630})
        for language in config["languages"]:
            html = BRAND / f"og-{language}.html"
            html.write_text(social_card(language, config))
            await page.goto(html.as_uri())
            await page.evaluate("document.fonts.ready")
            await page.screenshot(path=str(BRAND / f"og-{language}.png"))
            html.unlink()
        await browser.close()


if __name__ == "__main__":
    write_icons()
    if "--no-social" not in sys.argv:
        asyncio.run(write_social_cards())
