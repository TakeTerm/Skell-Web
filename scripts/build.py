import json
import pathlib
import re
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from builder.content import (
    ROOT,
    Translator,
    load_config,
    load_demo,
    load_guides,
    load_interface,
    load_landing,
    load_modules,
    load_stats,
    landing_values,
    substitute,
)
from builder.docs import build_doc, build_docs_index
from builder.frontpage import build_landing, build_studio_fragment
from builder.landing import resolve_values
from builder.layout import Site, page
from builder.markup import tag
from builder.portal import build_portal, portal_routes

OUTPUT = ROOT / "site"
SOURCE = ROOT / "src"
STYLESHEETS = {
    "site.css": ["base.css", "components.css", "layout.css", "landing.css", "skell-ui.css", "demos.css"],
    "docs.css": ["docs.css"],
    "frontpage.css": ["frontpage.css", "preview.css"],
    "portal.css": ["portal.css"],
}
LANDING_STYLES = ["site.css", "frontpage.css", "portal.css"]
LANDING_SCRIPTS = ["scripts/main.js", "scripts/frontpage.js", "scripts/portal.js"]
NOT_FOUND = {
    "en": ("Page not found", "That page does not exist. Head back to the start.", "Back to Skell Client"),
    "es": ("Página no encontrada", "Esa página no existe. Vuelve al inicio.", "Volver a Skell Client"),
}


def minify_css(source):
    source = re.sub(r"\s+", " ", source)
    source = re.sub(r"\s*([{};,>])\s*", r"\1", source)
    source = re.sub(r":\s+", ":", source)
    return source.replace(";}", "}").strip()


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def copy_assets():
    shutil.copytree(SOURCE / "assets", OUTPUT / "assets" / "", dirs_exist_ok=True)
    shutil.copytree(SOURCE / "scripts", OUTPUT / "assets" / "scripts", dirs_exist_ok=True)
    for bundle, files in STYLESHEETS.items():
        combined = "\n".join((SOURCE / "styles" / name).read_text() for name in files)
        write(OUTPUT / "assets" / bundle, minify_css(combined))


def settings_payload(modules, translate):
    payload = {}
    for module in modules:
        groups = {}
        for setting in module["settings"]:
            entry = {
                "name": translate(setting["name"]),
                "key": setting["name"],
                "type": setting["type"],
                "default": setting.get("default"),
                "min": setting.get("min"),
                "max": setting.get("max"),
                "step": setting.get("step"),
                "options": [{"value": option, "label": translate(option)} for option in setting.get("options", [])],
            }
            groups.setdefault(translate(setting["group"]) if setting["group"] else "", []).append(entry)
        payload[module["id"]] = {
            "name": translate(module["name"]),
            "category": module["category"],
            "groups": [{"name": name, "settings": entries} for name, entries in groups.items()],
        }
    return payload


def build_language(language, config, modules, stats):
    interface = load_interface(language)
    values = landing_values(config, modules, stats)
    site = Site(config, language, resolve_values(interface, values))
    translate = Translator(language)
    demo = load_demo(language)
    landing = resolve_values(load_landing(language), values)
    guides = load_guides(language)
    prefix = site.url("home")
    home = page(
        site,
        "home",
        site.interface["meta"]["title"],
        site.interface["meta"]["description"],
        build_landing(site),
        LANDING_STYLES,
        LANDING_SCRIPTS,
        main_class="landing",
        data={"data_page": "home"},
    )
    write(OUTPUT / prefix.lstrip("/") / "index.html", home)
    write(OUTPUT / "assets" / "data" / f"studio.{language}.html", build_studio_fragment(site, modules, stats, translate, demo, landing))
    write(OUTPUT / "assets" / "data" / f"settings.{language}.json", json.dumps(settings_payload(modules, translate), ensure_ascii=False, separators=(",", ":")))
    write(OUTPUT / site.url("docs").lstrip("/") / "index.html", build_docs_index(site, guides))
    for entry in guides["pages"]:
        resolved = {**entry, "description": substitute(entry["description"], config)}
        html = build_doc(site, resolved, guides, modules, translate, demo, landing)
        write(OUTPUT / site.url("docs/" + entry["slug"]).lstrip("/") / "index.html", html)
    for route in portal_routes():
        title, body = build_portal(site, route)
        html = page(
            site, route, title, site.interface["meta"]["description"], body, LANDING_STYLES,
            LANDING_SCRIPTS + (["scripts/studio.js"] if route in ("textures", "resourcepacks") else []),
            main_class="landing portal-page", data={"data_page": "portal", "data_portal": route},
        )
        write(OUTPUT / site.url(route).lstrip("/") / "index.html", html)
    return [site.url("home"), site.url("docs")] + [site.url("docs/" + entry["slug"]) for entry in guides["pages"]] + [site.url(route) for route in portal_routes()]


def build_not_found(config):
    title, message, label = NOT_FOUND["en"]
    spanish_title, spanish_message, spanish_label = NOT_FOUND["es"]
    body = tag(
        "main",
        tag("p", "404", class_="not-found__code display")
        + tag("h1", f"{title} · {spanish_title}", class_="display")
        + tag("p", f"{message} {spanish_message}")
        + tag("a", f"{label} / {spanish_label}", class_="btn btn--primary", href="/"),
        class_="not-found",
    )
    document = (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>404 · {config['name']}</title>"
        "<meta name=\"robots\" content=\"noindex\">"
        "<link rel=\"icon\" href=\"/assets/brand/favicon.svg\" type=\"image/svg+xml\">"
        "<link rel=\"stylesheet\" href=\"/assets/site.css\"></head>"
        f"<body>{body}</body></html>"
    )
    write(OUTPUT / "404.html", document)


def build_sitemap(config, urls):
    base = config["siteUrl"].rstrip("/")
    prefixes = {code: ("" if code == config["defaultLanguage"] else f"/{code}") for code in config["languages"]}
    entries = []
    for url in urls:
        language = next((code for code in config["languages"] if code != config["defaultLanguage"] and url.startswith(f"/{code}/")), config["defaultLanguage"])
        path = url[len(prefixes[language]):] or "/"
        alternates = "".join(
            f'<xhtml:link rel="alternate" hreflang="{code}" href="{base}{prefixes[code]}{path}"/>' for code in config["languages"]
        )
        entries.append(f"<url><loc>{base}{url}</loc>{alternates}</url>")
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
        + "".join(entries)
        + "</urlset>"
    )
    write(OUTPUT / "sitemap.xml", sitemap)
    write(OUTPUT / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")


def main():
    config = load_config()
    modules = load_modules()
    stats = load_stats()
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    copy_assets()
    urls = []
    for language in config["languages"]:
        urls += build_language(language, config, modules, stats)
    build_not_found(config)
    build_sitemap(config, urls)
    shutil.copy(ROOT / "vercel.json", OUTPUT / "vercel.json")
    print(f"Built {len(urls)} pages into {OUTPUT}")


if __name__ == "__main__":
    main()
