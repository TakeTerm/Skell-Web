import json

from .icons import icon
from .markup import join, tag, text

def language_prefix(language, default_language):
    return "" if language == default_language else f"/{language}"


class Site:
    def __init__(self, config, language, interface):
        self.config = config
        self.language = language
        self.interface = interface

    def url(self, page, language=None):
        language = language or self.language
        prefix = language_prefix(language, self.config["defaultLanguage"])
        path = "" if page == "home" else page.rstrip("/") + "/"
        return f"{prefix}/{path}"

    def absolute(self, page, language=None):
        return self.config["siteUrl"].rstrip("/") + self.url(page, language)

    def asset(self, path):
        return f"/assets/{path}"

    def resolve_link(self, target):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            return target
        scheme, _, rest = target.partition(":")
        page, hash_mark, anchor = rest.partition("#")
        if scheme == "docs":
            return self.url("docs/" + page if page else "docs") + (f"#{anchor}" if hash_mark else "")
        if scheme == "home":
            return self.url("home") + (f"#{anchor}" if hash_mark else "")
        raise ValueError(f"Unknown link {target}")


def alternate_links(site, page):
    links = [
        tag("link", rel="alternate", hreflang=code, href=site.absolute(page, code))
        for code in site.config["languages"]
    ]
    links.append(
        tag("link", rel="alternate", hreflang="x-default", href=site.absolute(page, site.config["defaultLanguage"]))
    )
    return join(links)


def head(site, page, title, description, styles, structured_data=""):
    interface = site.interface
    full_title = f"{title} · {site.config['name']}" if page != "home" else title
    canonical = site.absolute(page)
    image = site.config["siteUrl"].rstrip("/") + f"/assets/brand/og-{site.language}.png"
    pieces = [
        tag("meta", charset="utf-8"),
        tag("meta", name="viewport", content="width=device-width, initial-scale=1, viewport-fit=cover"),
        tag("title", text(full_title)),
        tag("meta", name="description", content=description),
        tag("meta", name="theme-color", content="#07080e"),
        tag("meta", name="color-scheme", content="dark"),
        tag("link", rel="canonical", href=canonical),
        alternate_links(site, page),
        tag("meta", property="og:type", content="website"),
        tag("meta", property="og:site_name", content=site.config["name"]),
        tag("meta", property="og:title", content=full_title),
        tag("meta", property="og:description", content=description),
        tag("meta", property="og:url", content=canonical),
        tag("meta", property="og:locale", content=interface["lang"]["locale"]),
        tag("meta", property="og:image", content=image),
        tag("meta", property="og:image:width", content="1200"),
        tag("meta", property="og:image:height", content="630"),
        tag("meta", property="og:image:alt", content=interface["meta"]["imageAlt"]),
        tag("meta", name="twitter:card", content="summary_large_image"),
        tag("meta", name="twitter:title", content=full_title),
        tag("meta", name="twitter:description", content=description),
        tag("meta", name="twitter:image", content=image),
        tag("link", rel="icon", href="/assets/brand/favicon.svg", type="image/svg+xml"),
        tag("link", rel="icon", href="/assets/brand/favicon-32.png", type="image/png", sizes="32x32"),
        tag("link", rel="apple-touch-icon", href="/assets/brand/apple-touch-icon.png"),
        tag("link", rel="manifest", href="/assets/brand/site.webmanifest"),
        tag("link", rel="preload", href="/assets/fonts/bricolage-grotesque-latin-wght-normal.woff2", as_="font", type="font/woff2", crossorigin=True),
        tag("link", rel="preload", href="/assets/fonts/inter-latin-wght-normal.woff2", as_="font", type="font/woff2", crossorigin=True),
        join(tag("link", rel="stylesheet", href=f"/assets/{name}") for name in styles),
        structured_data,
    ]
    return tag("head", join(pieces))


def footer(site):
    from .portal import LEGAL, local

    labels = site.interface["footer"]
    groups = (
        (local(site, "Product", "Producto"), (
            (local(site, "Features", "Funciones"), "home:#features"),
            (local(site, "Pricing", "Precios"), "home:#pricing"),
            (local(site, "Profile", "Perfil"), "account"),
            (local(site, "Documentation", "Documentación"), "docs:"),
        )),
        (local(site, "Studio", "Estudio"), (
            (local(site, "Textures", "Texturas"), "textures"),
            (local(site, "Resource packs", "Paquetes de recursos"), "resourcepacks"),
            (local(site, "Support", "Ayuda"), "faq"),
            (local(site, "Changelog", "Novedades"), "docs:changelog"),
        )),
        (local(site, "Project", "Proyecto"), (
            (local(site, "Partnership", "Colaboraciones"), "partnership"),
            (local(site, "Press kit", "Material de prensa"), "partnership/press"),
            (local(site, "Affiliates", "Afiliados"), "partnership/affiliates"),
            (local(site, "Contacts", "Contacto"), "legal/contacts"),
        )),
    )
    columns = []
    for title, entries in groups:
        links = join(tag("li", tag("a", text(name), href=site.resolve_link(target) if ":" in target else site.url(target))) for name, target in entries)
        columns.append(tag("div", tag("h2", text(title)) + tag("ul", links)))
    brand = tag(
        "div",
        tag(
            "a",
            tag("span", "", class_="brand__mark") + tag("span", 'Skell <span class="brand__client">Client</span>'),
            class_="brand",
            href=site.url("home"),
        )
        + tag("p", labels["tagline"])
        + tag("p", labels["developedBy"], class_="site-footer__credit"),
        class_="site-footer__brand",
    )
    legal = tag(
        "div",
        tag("p", f"© {site.config['year']} {site.config['author']}. {labels['rights']}")
        + tag("p", labels["trademark"])
        + tag("nav", join(tag("a", text(local(site, english, spanish)), href=site.url("legal/" + slug)) for slug, english, spanish, _ in LEGAL) + tag("button", local(site, "Cookie settings", "Preferencias de cookies"), type="button", data_cookie_open=True), class_="reference-legal-links"),
        class_="site-footer__legal",
    )
    return tag(
        "footer",
        tag(
            "div",
            tag("div", brand + tag("div", join(columns), class_="site-footer__columns"), class_="site-footer__grid") + legal,
            class_="container",
        ),
        class_="site-footer",
    )


def page(site, key, title, description, body, styles, scripts, main_class="", data=None):
    from .frontpage import landing_header
    from .portal import cookie_panel

    shell = join(
        [
            tag("a", site.interface["skip"], class_="skip-link", href="#main"),
            tag("div", "", class_="backdrop"),
            landing_header(site, key),
            tag("main", body, id="main", class_=main_class),
            footer(site),
            cookie_panel(site),
            join(tag("script", "", type="module", src=f"/assets/{name}") for name in scripts),
        ]
    )
    script_flag = tag(
        "script",
        "var d=document.documentElement,redirect=false;d.classList.add('js');"
        "try{var saved=localStorage.getItem('skell-language');"
        f"if(saved&&saved!=='{site.language}'&&location.pathname==='{site.url('home')}'&&!location.hash)"
        "{redirect=true;location.replace(saved==='es'?'/es/':'/')}}catch(e){}"
        "try{if(!redirect){if(matchMedia('(prefers-reduced-motion: reduce)').matches||sessionStorage.getItem('skell-intro')||location.hash)"
        "d.classList.add('no-intro');sessionStorage.setItem('skell-intro','1')}}catch(e){}",
    )
    document = join(
        [
            "<!doctype html>",
            f'<html lang="{site.language}">',
            head(site, key, title, description, styles).replace("</head>", script_flag + "</head>"),
            tag("body", shell, **(data or {})),
            "</html>",
        ]
    )
    return document


def json_script(identifier, value):
    payload = json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/json" id="{identifier}">{payload}</script>'
