from .content import landing_values
from .icons import icon
from .landing import demo_section, resolve_values
from .layout import json_script
from .markup import join, tag, text
from .widgets import control_templates

COPY = {
    "en": {
        "headline": ("Skell changes", "the game"),
        "lead": "An independent Minecraft client with a customizable interface, refined visuals, and tools that fit the way you play.",
        "explore": "Explore Skell",
        "nav": ("Features", "Access", "Project", "Studio", "Contact", "Documentation", "Getting started"),
        "projectMenu": ("Project status", "Changelog", "Credits"),
        "studioMenu": ("Mods menu", "HUD editor", "Module reference"),
        "preview": {
            "categories": "Client categories", "search": "Search",
            "labels": ("All", "HUD", "PvP", "Utility", "Visuals", "Cosmetics", "Client"),
            "cards": ("Interface", "HUD Elements", "Appearance"),
            "fields": ("Preset", "Layout", "Theme", "Display mode", "Intensity", "Accent colour", "Visible elements", "Scale", "Opacity"),
            "choices": (("Balanced", "Compact", "Minimal"), ("Compact", "Expanded", "Side panel"), ("Flat", "Glass", "Transparent")),
            "hints": ("Choose the default view for the client.", "Adjust the position and spacing of the interface.", "Set the base style for panels and widgets."),
            "modes": ("Normal", "Transparent"),
            "widgets": ("Waypoints", "Keybinds", "FPS", "Coordinates", "Potions", "Cooldowns", "Recordings", "Music"),
            "caption": "Everything you need, in one place.",
            "noResults": "No matching controls",
            "light": "Light preview", "dark": "Dark preview", "expand": "Expand preview",
        },
        "features": ("Advanced features", "An interface built for everyday play, with precise controls, flexible layouts, and visuals you can make your own.", "Open interactive studio"),
        "tiles": (
            ("In-game GUI", "Fine-tune modules and choose how their settings are displayed."),
            ("HUD Elements", "Position your widgets with anchors, snapping, and alignment guides."),
            ("Visual Effects", "Preview effects, adjust their appearance, and shape the look of your game."),
            ("Music & Captures", "Keep lyrics, recordings, and instant replays within reach."),
        ),
        "access": ("Client access", "Everything that comes with Skell Client.", "Overview", "Compatibility", "Build details"),
        "editions": (
            ("Skell Client", "Client", None, "Current version", "Get started", "docs:getting-started", ("Fabric client", "Custom HUD", "Visual effects", "Music and captures", "Bilingual interface", "Module settings")),
            ("Interactive Studio", "Browser", "Live", "Web preview", "Try the demo", "home:#studio", ("Interactive menu", "HUD editor", "Kill effects", "Recording controls", "Configurable previews", "Runs in the browser")),
            ("Documentation", "Guides", "EN / ES", "Two languages", "Read the docs", "docs:", ("Getting started", "Interface guide", "Module reference", "Troubleshooting", "Changelog", "Credits")),
        ),
        "help": ("Need help?", "Find answers about setup, client features, and the interactive preview."),
        "support": (
            ("book", "Open the knowledge base", "Setup, controls, and the full module reference.", "Open documentation", "docs:"),
            ("wrench", "Troubleshoot a problem", "Find solutions for common setup and launch issues.", "Read troubleshooting", "docs:troubleshooting"),
            ("layout", "Try the interactive studio", "Explore the controls before opening Minecraft.", "Open the demo", "home:#studio"),
            ("info", "Check the latest changes", "Review the changes included in this version.", "Open changelog", "docs:changelog"),
        ),
        "faq": (
            ("How do I get started?", "Check the getting-started guide for the required Minecraft, Fabric, and Java versions."),
            ("Where do I find support?", "The troubleshooting guide covers startup issues, controls, and common configuration questions."),
            ("Can I try the interface in a browser?", "Yes. The studio includes browser versions of the mods menu and several client previews."),
            ("How do I move my HUD widgets?", "Open the HUD editor, then drag a widget. You can use snapping, guides, and keyboard nudging."),
            ("Which Minecraft version is supported?", "This edition of Skell Client is built for Minecraft 1.21.11 on Fabric."),
            ("Which Java version is required?", "Use Java 21 with the supported Fabric Loader and Fabric API versions."),
            ("What can I change in the interface?", "The client offers settings layouts, accent colours, animations, and language controls."),
            ("Where can I see the available modules?", "The searchable module reference lists modules by category and describes their settings."),
            ("Can I preview a visual effect?", "Open Kill Effects in the studio and select an effect to adjust its browser preview."),
            ("How does instant replay work?", "The music and captures guide covers instant replay, recording, and the recordings library."),
            ("Is the site available in Spanish?", "Yes. Use the language selector to switch both the landing page and documentation."),
            ("What changed in the current version?", "The changelog lists changes to the interface, HUD, visual effects, and client tools."),
            ("Who develops Skell Client?", "Skell Client is independently developed by Take."),
            ("Is this an official Minecraft product?", "Skell Client is independent of Mojang Studios and Microsoft."),
        ),
    },
    "es": {
        "headline": ("Skell cambia", "el juego"),
        "lead": "Un cliente independiente de Minecraft con una interfaz personalizable, efectos visuales y herramientas que se adaptan a tu forma de jugar.",
        "explore": "Explorar Skell",
        "nav": ("Funciones", "Acceso", "Proyecto", "Estudio", "Ayuda", "Documentación", "Primeros pasos"),
        "projectMenu": ("Estado del proyecto", "Novedades", "Créditos"),
        "studioMenu": ("Menú de módulos", "Editor HUD", "Referencia de módulos"),
        "preview": {
            "categories": "Categorías del cliente", "search": "Buscar",
            "labels": ("Todo", "HUD", "PvP", "Utilidades", "Visuales", "Cosméticos", "Cliente"),
            "cards": ("Interfaz", "Elementos HUD", "Apariencia"),
            "fields": ("Perfil", "Diseño", "Tema", "Modo de vista", "Intensidad", "Color de acento", "Elementos visibles", "Escala", "Opacidad"),
            "choices": (("Equilibrado", "Compacto", "Mínimo"), ("Compacto", "Expandido", "Panel lateral"), ("Plano", "Cristal", "Transparente")),
            "hints": ("Elige la vista inicial del cliente.", "Ajusta la posición y separación de la interfaz.", "Define el estilo de paneles y widgets."),
            "modes": ("Normal", "Transparente"),
            "widgets": ("Puntos de ruta", "Teclas", "FPS", "Coordenadas", "Pociones", "Temporizadores", "Grabaciones", "Música"),
            "caption": "Todo lo que necesitas, en un solo lugar.",
            "noResults": "No se encontraron controles",
            "light": "Vista clara", "dark": "Vista oscura", "expand": "Ampliar vista",
        },
        "features": ("Funciones avanzadas", "Una interfaz para el juego diario, con controles precisos, diseños flexibles y efectos visuales personalizables.", "Abrir estudio interactivo"),
        "tiles": (
            ("Interfaz en juego", "Ajusta los módulos y elige cómo se muestran sus opciones."),
            ("Elementos HUD", "Coloca tus widgets con anclajes, ajuste automático y guías."),
            ("Efectos visuales", "Previsualiza efectos y ajusta su apariencia antes de aplicarlos."),
            ("Música y capturas", "Accede a letras, grabaciones y repeticiones instantáneas."),
        ),
        "access": ("Acceso al cliente", "Todo lo que incluye Skell Client.", "Resumen", "Compatibilidad", "Datos de la versión"),
        "editions": (
            ("Skell Client", "Cliente", None, "Versión actual", "Primeros pasos", "docs:getting-started", ("Cliente Fabric", "HUD personalizable", "Efectos visuales", "Música y capturas", "Interfaz bilingüe", "Ajustes de módulos")),
            ("Estudio interactivo", "Navegador", "Demo", "Vista web", "Probar la demo", "home:#studio", ("Menú interactivo", "Editor HUD", "Efectos de eliminación", "Controles de grabación", "Previews configurables", "Funciona en navegador")),
            ("Documentación", "Guías", "EN / ES", "Dos idiomas", "Leer las guías", "docs:", ("Primeros pasos", "Guía de la interfaz", "Referencia de módulos", "Solución de problemas", "Novedades", "Créditos")),
        ),
        "help": ("¿Necesitas ayuda?", "Encuentra respuestas sobre instalación, funciones y el estudio interactivo."),
        "support": (
            ("book", "Abre la base de conocimiento", "Instalación, controles y referencia de módulos.", "Abrir documentación", "docs:"),
            ("wrench", "Resuelve un problema", "Soluciones a problemas habituales de instalación e inicio.", "Leer la guía", "docs:troubleshooting"),
            ("layout", "Prueba el estudio interactivo", "Explora los controles antes de abrir Minecraft.", "Abrir demo", "home:#studio"),
            ("info", "Consulta los últimos cambios", "Revisa las novedades de esta versión.", "Ver novedades", "docs:changelog"),
        ),
        "faq": (
            ("¿Cómo empiezo?", "Consulta la guía de primeros pasos para conocer las versiones de Minecraft, Fabric y Java requeridas."),
            ("¿Dónde encuentro ayuda?", "La guía de solución de problemas cubre el inicio, los controles y la configuración."),
            ("¿Puedo probar la interfaz en el navegador?", "Sí. El estudio incluye el menú de módulos y varias vistas interactivas."),
            ("¿Cómo muevo los widgets del HUD?", "Abre el editor HUD y arrastra un widget. Hay guías, ajuste automático y movimiento con el teclado."),
            ("¿Qué versión de Minecraft es compatible?", "Esta versión de Skell Client funciona con Minecraft 1.21.11 y Fabric."),
            ("¿Qué versión de Java necesito?", "Usa Java 21 con las versiones compatibles de Fabric Loader y Fabric API."),
            ("¿Qué puedo cambiar en la interfaz?", "Puedes ajustar el diseño, los colores, las animaciones y el idioma."),
            ("¿Dónde están los módulos disponibles?", "La referencia de módulos se puede buscar y describe las opciones por categoría."),
            ("¿Puedo previsualizar un efecto visual?", "Abre Efectos de eliminación en el estudio y elige un efecto para ajustar su vista previa."),
            ("¿Cómo funciona la repetición instantánea?", "La guía de música y capturas explica la repetición, la grabación y la biblioteca."),
            ("¿El sitio está disponible en español?", "Sí. El selector de idioma cambia la portada y la documentación."),
            ("¿Qué cambió en esta versión?", "Las novedades detallan los cambios en la interfaz, el HUD, los efectos y las herramientas."),
            ("¿Quién desarrolla Skell Client?", "Take desarrolla Skell Client de forma independiente."),
            ("¿Es un producto oficial de Minecraft?", "Skell Client es independiente de Mojang Studios y Microsoft."),
        ),
    },
}

ACCENTS = ("#ee4c50", "#f58131", "#f2d442", "#41aa7f", "#70cef1", "#4a71e3", "#a77bdf")
CATEGORY_ICONS = ("layout", "hud", "target", "wrench", "eye", "sparkles", "sliders")


def link(label, url, style="", arrow=None):
    return tag("a", text(label) + (icon(arrow, 15) if arrow else ""), href=url, class_=style or None)


def brand(site):
    mark = tag("span", "", class_="reference-brand__mark", aria_hidden="true")
    return tag("a", mark + tag("span", "Skell"), href=site.url("home"), class_="reference-brand")


def dropdown(label, links):
    return tag("details", tag("summary", text(label) + icon("chevron-down", 12)) + tag("div", join(links)), class_="reference-dropdown")


def landing_header(site):
    copy = COPY[site.language]
    features, access, project, studio, contact, docs, start = copy["nav"]
    menu_label = site.interface["nav"]["open"]
    languages = [
        tag("a", label, href=site.url("home", code), hreflang=code, lang=code, data_language_choice=code, aria_current="true" if site.language == code else None)
        for code, label in (("en", "English"), ("es", "Español"))
    ]
    nav = join((
        link(features, "#features"),
        link(access, "#project"),
        dropdown(project, (link(label, site.resolve_link(target)) for label, target in zip(copy["projectMenu"], ("home:#project", "docs:changelog", "docs:credits")))),
        dropdown(studio, (link(label, site.resolve_link(target)) for label, target in zip(copy["studioMenu"], ("home:#studio", "docs:hud-editor", "docs:modules")))),
        link(contact, "#contact"),
    ))
    actions = dropdown("English" if site.language == "en" else "Español", languages) + link(docs, site.url("docs")) + link(start, site.url("docs/getting-started"), "reference-button", "arrow-right")
    mobile = tag("button", icon("menu", 21), class_="reference-menu", type="button", aria_expanded="false", aria_label=menu_label, aria_controls="reference-nav", data_reference_menu=True)
    navigation = tag("nav", tag("div", nav, class_="reference-links") + tag("div", actions, class_="reference-actions"), class_="reference-nav", id="reference-nav", aria_label=site.interface["nav"]["primary"])
    return tag("header", tag("div", brand(site) + navigation + mobile, class_="reference-header__inner"), class_="reference-header", data_header=True)


def tile_widget(title, entries, glyph):
    rows = join(tag("span", icon(glyph, 13) + text(label) + tag("small", value)) for label, value in entries)
    return tag("div", tag("b", icon(glyph, 13) + text(title)) + rows, class_="reference-widget")


def background(copy):
    widgets = copy["widgets"]
    groups = (
        (widgets[1], (("Zoom", "C"), ("Freelook", "F"), ("HUD", "H")), "sliders"),
        (widgets[3], (("XYZ", "128 64 −32"),), "layout"),
        ("Skell", (("FPS", "144"), ("Ping", "14 ms")), "bolt"),
        (widgets[4], (("Speed", "0:42"), ("Strength", "1:20")), "sparkles"),
        (widgets[0], (("Spawn", "16 m"), ("Base", "120 m")), "target"),
        (widgets[6], (("Clip", "00:30"),), "video"),
        (widgets[7], (("Midnight Drive", "02:18"),), "music"),
    )
    return tag("div", join(tile_widget(*group) for group in groups), class_="reference-blueprint", aria_hidden="true")


def preview_select(label, choices):
    return tag("select", join(tag("option", text(choice)) for choice in choices), aria_label=label)


def preview_range(label, minimum, maximum, value):
    slider = tag("input", type="range", min=minimum, max=maximum, value=value, aria_label=label)
    return tag("label", tag("span", text(label)) + slider + tag("output", str(value)), class_="preview-range")


def preview_card(title, glyph, body, categories):
    favorite = tag("button", "☆", type="button", class_="preview-favorite", aria_label=f"★ {title}", aria_pressed="false")
    toggle = tag("input", type="checkbox", checked=True, class_="preview-toggle", aria_label=title)
    head = tag("div", tag("h3", icon(glyph, 16) + text(title)) + favorite + toggle, class_="preview-card__head")
    return tag("article", head + tag("div", body, class_="preview-card__body"), class_="preview-card", data_preview_card=categories)


def preview_cards(copy):
    fields, cards = copy["fields"], copy["cards"]
    glyphs = ("sliders", "layout", "sparkles")
    fields_start = [
        tag("label", icon(glyph, 15) + text(fields[i])) + tag("p", hint) + preview_select(fields[i], copy["choices"][i])
        for i, (glyph, hint) in enumerate(zip(glyphs, copy["hints"]))
    ]
    modes = tag("div", join(
        tag("button", text(label), type="button", data_preview_mode=value, aria_pressed="true" if value == "solid" else "false")
        for value, label in zip(("solid", "glass"), copy["modes"])
    ), class_="preview-modes")
    colors = tag("div", join(
        tag("button", "", type="button", style=f"--swatch:{color}", data_preview_accent=color, aria_label=color, aria_pressed="false")
        for color in ACCENTS
    ), class_="preview-colors")
    widgets = tag("div", join(
        tag("label", icon(glyph, 14) + text(name) + tag("input", type="checkbox", checked=True, aria_label=name))
        for glyph, name in zip(("target", "sliders", "bolt", "layout"), copy["widgets"])
    ), class_="preview-widgets")
    return join((
        preview_card(cards[0], glyphs[0], fields_start[0] + preview_range(fields[4], 0, 100, 62) + tag("label", icon("sparkles", 15) + text(fields[5])) + colors, "2 3 4 5 6"),
        preview_card(cards[1], glyphs[1], fields_start[1] + tag("label", icon("eye", 15) + text(fields[3])) + modes + preview_range(fields[7], 50, 150, 100), "1 2 3 6"),
        preview_card(cards[2], glyphs[2], fields_start[2] + tag("label", icon("hud", 15) + text(fields[6])) + widgets + preview_range(fields[8], 15, 100, 85), "1 4 5 6"),
    ))


def client_preview(site, copy):
    labels = copy["labels"]
    category = join(
        tag("button", icon(glyph, 17) + text(label), type="button", data_preview_category=i, aria_pressed="true" if i == 0 else "false")
        for i, (glyph, label) in enumerate(zip(CATEGORY_ICONS, labels))
    )
    profile = tag("div", tag("b", "S") + tag("span", "Skell Client" + tag("small", site.config["version"])), class_="preview-profile")
    side = tag("aside", brand(site) + tag("p", copy["categories"]) + category + profile, class_="preview-side")
    search = tag("label", icon("search", 14) + tag("input", type="search", placeholder=copy["search"], aria_label=copy["search"], data_preview_search=True) + tag("kbd", "⌘ K"), class_="preview-search")
    tools = tag("div",
        tag("button", "☆", type="button", data_preview_favorites=True, aria_pressed="false", aria_label="Favourites" if site.language == "en" else "Favoritos")
        + tag("button", "☼", type="button", data_preview_theme="light", aria_label=copy["light"], aria_pressed="false")
        + tag("button", "☾", type="button", data_preview_theme="dark", aria_label=copy["dark"], aria_pressed="true")
        + tag("button", "⤢", type="button", data_preview_expand=True, aria_label=copy["expand"], aria_pressed="false"),
        class_="preview-tools",
    )
    head = tag("div", tag("strong", icon("layout", 15) + tag("span", labels[0], data_preview_title=True)) + search + tools, class_="preview-toolbar")
    body = tag("div", head + tag("div", preview_cards(copy), class_="preview-grid") + tag("p", copy["noResults"], class_="preview-empty", data_preview_empty=True, hidden=True), class_="preview-body")
    return tag("form", side + body, class_="client-preview", data_client_preview=True, aria_label="Skell Client")


def hero(site, copy):
    preview = copy["preview"]
    intro = tag("div", tag("span", "Skell", class_="reference-script"), class_="reference-intro", aria_hidden="true")
    headline = tag("h1", join(tag("span", text(line)) for line in copy["headline"]))
    lead = tag("p", copy["lead"], class_="reference-hero__lead")
    cta = link(copy["explore"], "#demo", "reference-button reference-button--hero", "external")
    stage = tag("div", client_preview(site, preview), class_="reference-stage", id="demo")
    caption = tag("div", tag("p", preview["caption"]) + tag("p", " · ".join(copy["studioMenu"] + preview["widgets"][5:8])), class_="preview-caption")
    return tag("section", intro + background(preview) + tag("div", headline + lead + cta, class_="reference-hero__copy") + stage + caption, class_="reference-hero", id="top")


def section_head(title, lead):
    return tag("div", tag("h2", text(title)) + tag("p", text(lead)), class_="reference-heading")


def section_wrap(identifier, body, extra=""):
    return tag("section", tag("div", body, class_="reference-width"), id=identifier, class_=f"reference-section {extra}".strip())


def feature_art(index, preview):
    widgets = preview["widgets"]
    groups = (
        (widgets[1], (("Zoom", "C"), ("Freelook", "F"), ("HUD", "H")), "sliders"),
        (widgets[0], (("Spawn", "16 m"), ("Base", "120 m"), ("Village", "820 m")), "target"),
        (widgets[4], (("Speed", "0:42"), ("Strength", "1:20"), ("Resistance", "0:12")), "sparkles"),
        (widgets[6], (("Clip 12", "00:30"), ("Clip 11", "00:18")), "video"),
    )
    if index in (0, 2):
        art = tile_widget(*groups[index]) + tile_widget(*groups[index + 1])
    elif index == 1:
        art = join(tile_widget(*groups[i % 4]) for i in range(12))
    else:
        art = join(tag("span", icon(glyph, 13) + text(label), class_="reference-pill") for glyph, label in zip(("music", "video", "sparkles", "bolt", "hud", "target", "sliders", "video") * 6, (widgets[7], widgets[6], "00:30", "144 FPS", widgets[2], widgets[0], widgets[1], "Clip 12") * 6))
    return tag("div", art, class_=f"reference-tile__art art-{index + 1}", aria_hidden="true")


def features(site, copy, full_demo):
    title, lead, studio = copy["features"]
    targets = ("interface", "hud-editor", "visuals", "music-and-captures")
    identifiers = ("interface", "hud", "visuals", "music")
    tiles = []
    for index, (label, description) in enumerate(copy["tiles"]):
        caption = tag("small", f"{index + 1:02d}") + tag("div", tag("h3", label) + tag("p", description))
        tiles.append(tag("a", feature_art(index, copy["preview"]) + tag("div", caption, class_="reference-tile__copy"), class_="reference-tile", href=site.url("docs/" + targets[index]), id=identifiers[index]))
    lab = tag("details", tag("summary", icon("layout", 16) + text(studio) + icon("chevron-down", 14)) + full_demo, id="studio", class_="reference-lab")
    return section_wrap("features", section_head(title, lead) + tag("div", join(tiles), class_="reference-tiles") + lab)


def access_section(site, copy, launch):
    title, lead, overview, compatibility, build = copy["access"]
    config = site.config
    plans = []
    for name, badge, value, meta, action, href, inclusions in copy["editions"]:
        heading = tag("div", tag("span", name) + tag("small", badge), class_="access-card__heading")
        amount = tag("div", tag("strong", text(value or config["version"])) + tag("span", text(meta)), class_="access-card__amount")
        versions = tag("div", tag("span", "— Minecraft") + tag("small", config["minecraft"]) + tag("small", "Fabric"), class_="access-card__versions")
        items = tag("ul", join(tag("li", icon(glyph, 14) + text(label)) for glyph, label in zip(("box", "layout", "sparkles", "video", "book", "sliders"), inclusions)))
        plans.append(tag("article", heading + amount + versions + items + link(action, site.resolve_link(href), "reference-button access-card__action", "arrow-right"), class_="access-card"))
    modes = tag("div", tag("button", overview, type="button", data_access_toggle="overview", aria_pressed="true") + tag("button", compatibility, type="button", data_access_toggle="compatibility", aria_pressed="false"), class_="access-toggle")
    specs = (("Minecraft", config["minecraft"]), ("Fabric Loader", config["fabricLoader"]), ("Fabric API", config["fabricApi"]), ("Java", config["java"]))
    compatibility_panel = tag("div", tag("h3", build) + tag("dl", join(tag("div", tag("dt", name) + tag("dd", value)) for name, value in specs)), class_="access-specs", data_access_panel="compatibility", hidden=True)
    return section_wrap("project", section_head(title, lead) + modes + tag("div", join(plans), class_="access-grid", data_access_panel="overview") + compatibility_panel + tag("p", launch, class_="access-note"))


def help_section(site, copy):
    support = join(
        tag("a", tag("h3", icon(glyph, 16) + text(title)) + tag("p", text(description)) + tag("span", text(label) + icon("arrow-right", 14)), class_="reference-support", href=site.resolve_link(href))
        for glyph, title, description, label, href in copy["support"]
    )
    faq = join(
        tag("details", tag("summary", tag("span", f"{index + 1:02d}") + text(question) + tag("i", "+", aria_hidden="true")) + tag("p", text(answer)), name="skell-faq")
        for index, (question, answer) in enumerate(copy["faq"])
    )
    return section_wrap("contact", section_head(*copy["help"]) + tag("div", tag("div", support, class_="reference-supports") + tag("div", faq, class_="reference-faq"), class_="reference-help"))


def build_landing(site, modules, stats, translate, demo, landing):
    content = resolve_values(landing, landing_values(site.config, modules, stats))
    copy = COPY[site.language]
    lab = demo_section(site, content["demo"], modules, translate, demo, site.language, identifier="studio-demo")
    return join((
        hero(site, copy),
        features(site, copy, lab),
        access_section(site, copy, content["project"]["launch"]),
        help_section(site, copy),
        control_templates(demo["gui"]),
        json_script("demo-strings", {key: demo[key] for key in ("gui", "hud", "kill", "recordings")}),
    ))
