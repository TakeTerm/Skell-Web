from .content import CATEGORY_ORDER, load_doc, substitute
from .demos import hud_editor, recordings_demo
from .gui_window import hero_window
from .icons import icon
from .layout import json_script, page
from .landing import layout_visual, mini_hud
from .markdown import Renderer
from .markup import join, tag, text
from .widgets import clip_toast, hud_widget, lyrics_island, shulker_demo

MODULE_MARKER = "modules"


def docs_nav(site, guides, current):
    labels = site.interface["docs"]["groups"]
    sections = []
    for group in guides["groups"]:
        entries = [entry for entry in guides["pages"] if entry["group"] == group]
        links = join(
            tag(
                "li",
                tag(
                    "a",
                    icon(entry["icon"], 18) + tag("span", text(entry["title"])),
                    href=site.url("docs/" + entry["slug"]),
                    aria_current="page" if entry["slug"] == current else None,
                ),
            )
            for entry in entries
        )
        sections.append(tag("div", tag("h2", text(labels[group])) + tag("ul", links), class_="docs-nav__group"))
    return join(sections)


def mobile_bar(site, guides, current, title):
    strings = site.interface["docs"]
    return tag(
        "div",
        tag(
            "button",
            icon("menu", 18)
            + tag("span", tag("small", text(strings["menu"])) + text(title))
            + icon("chevron-down", 18, "icon docs-bar__chevron"),
            type="button",
            class_="docs-bar__button",
            aria_expanded="false",
            aria_controls="docs-sheet",
            data_docs_menu_button=True,
        )
        + tag(
            "div",
            tag("nav", docs_nav(site, guides, current), class_="docs-nav", aria_label=strings["menu"]),
            class_="docs-bar__sheet",
            id="docs-sheet",
        ),
        class_="docs-bar",
        data_docs_bar=True,
    )


def breadcrumb(site, guides, entry):
    strings = site.interface["docs"]
    group = strings["groups"][entry["group"]]
    parts = [tag("a", text(strings["title"]), href=site.url("docs"))]
    if entry["slug"] != "index":
        parts.append(tag("span", text(group)))
        parts.append(tag("span", text(entry["title"]), aria_current="page"))
    return tag("nav", join(tag("span", part, class_="breadcrumb__item") for part in parts), class_="breadcrumb", aria_label=strings["breadcrumb"])


def table_of_contents(site, headings):
    entries = [(level, title, anchor) for level, title, anchor in headings if level in (2, 3)]
    if len(entries) < 2:
        return ""
    links = join(
        tag("li", tag("a", text(title), href=f"#{anchor}", data_toc_link=anchor), class_=f"toc__item toc__item--{level}")
        for level, title, anchor in entries
    )
    return tag(
        "aside",
        tag("h2", text(site.interface["docs"]["onThisPage"])) + tag("ul", links),
        class_="docs__toc",
        data_toc=True,
    )


def pager(site, guides, slug):
    pages = guides["pages"]
    index = next(i for i, entry in enumerate(pages) if entry["slug"] == slug)
    strings = site.interface["docs"]
    cells = []
    for offset, label, arrow, side in ((-1, strings["previous"], "arrow-left", "prev"), (1, strings["next"], "arrow-right", "next")):
        target = index + offset
        if 0 <= target < len(pages):
            entry = pages[target]
            cells.append(
                tag(
                    "a",
                    tag("span", icon(arrow, 16) + text(label), class_="pager__label") + tag("strong", text(entry["title"])),
                    class_=f"pager__link pager__link--{side}",
                    href=site.url("docs/" + entry["slug"]),
                )
            )
        else:
            cells.append(tag("span", "", class_="pager__spacer"))
    return tag("nav", join(cells), class_="pager", aria_label=strings["title"])


def setting_summary(setting, reference, translate):
    kind = setting["type"]
    if kind == "bool":
        state = reference["on"] if setting.get("default") else reference["off"]
        return f"{state} ({reference['defaultValue']})"
    if kind == "number" and "min" in setting:
        low, high = (f"{setting[key]:g}" for key in ("min", "max"))
        return reference["range"].format(min=low, max=high) + f" ({reference['defaultValue']} {setting['default']:g})"
    if kind == "mode" and setting.get("options"):
        return " · ".join(translate(option) for option in setting["options"])
    if kind == "color":
        return reference["color"]
    if kind == "string":
        return reference["text"]
    return ""


def module_entry(module, reference, translate, strings):
    settings = module["settings"]
    rows = join(
        tag(
            "li",
            tag("span", text(translate(setting["name"])), class_="modref__setting") + tag("span", text(setting_summary(setting, reference, translate)), class_="modref__value"),
        )
        for setting in settings
    )
    count_label = reference["settingsOne"] if len(settings) == 1 else reference["settingsMany"]
    badge = tag("span", strings["newBadge"], class_="badge badge--new") if module["new"] else ""
    head = tag(
        "div",
        tag("h4", text(translate(module["name"])) + badge) + tag("p", text(translate(module["description"]))),
        class_="modref__head",
    )
    if settings:
        details = tag(
            "details",
            tag("summary", tag("span", f"{len(settings)} {count_label}") + icon("chevron-down", 16)) + tag("ul", rows),
            class_="modref__settings",
        )
    else:
        details = tag("p", text(reference["noSettings"]), class_="modref__none")
    search_text = f"{translate(module['name'])} {translate(module['description'])}".lower()
    return tag(
        "article",
        head + details,
        class_="modref",
        data_search=search_text,
        id=f"module-{module['id']}",
    )


def module_reference(site, modules, guides, translate):
    strings = site.interface["docs"]
    reference = guides["reference"]
    visible = [module for module in modules if module["id"] != "skellusers"]
    chips = join(
        [tag("button", text(strings["allCategories"]) + tag("span", str(len(visible))), type="button", class_="chip", aria_pressed="true", data_category_filter="")]
        + [
            tag(
                "button",
                text(translate(category)) + tag("span", str(sum(1 for m in visible if m["category"] == category))),
                type="button",
                class_="chip",
                aria_pressed="false",
                data_category_filter=category,
            )
            for category in CATEGORY_ORDER
            if any(m["category"] == category for m in visible)
        ]
    )
    controls = tag(
        "div",
        tag(
            "label",
            icon("search", 18)
            + tag("input", type="search", placeholder=strings["searchModules"], aria_label=strings["searchModules"], autocomplete="off", data_module_search=True),
            class_="modsearch",
        )
        + tag("div", chips, class_="modchips", role="group"),
        class_="modref-controls",
    )
    sections = []
    for category in CATEGORY_ORDER:
        members = [m for m in visible if m["category"] == category]
        if not members:
            continue
        entries = join(module_entry(m, reference, translate, strings) for m in members)
        sections.append(
            tag(
                "section",
                tag("h3", text(translate(category)) + tag("span", f"{len(members)} {strings['modulesCount']}"), id=f"category-{category.lower()}")
                + tag("div", entries, class_="modref-list"),
                class_="modref-section",
                data_category=category,
            )
        )
    empty = tag("p", text(strings["noModules"]), class_="modref-empty", hidden=True, data_module_empty=True)
    return tag("div", controls + join(sections) + empty, class_="modref-root", data_module_reference=True)


def figures(site, modules, translate, demo, landing):
    features = landing["features"]
    return {
        "menu-window": lambda: tag("div", tag("div", hero_window(modules, translate, demo["gui"], site.config), class_="frame__inner"), class_="frame"),
        "layouts": lambda: layout_visual(features["layouts"]),
        "hud-editor": lambda: mini_hud({**demo, "features": features}, translate),
        "hud-widgets": lambda: tag("div", join(hud_widget(kind, demo["hud"]) for kind in ("fps", "coordinates", "keystrokes", "radar", "armor", "music")), class_="figure__widgets"),
        "clip-toast": lambda: tag("div", clip_toast(features["clip"]), class_="figure__center"),
        "lyrics-island": lambda: tag("div", lyrics_island(features["lyrics"]), class_="figure__center"),
        "shulker": lambda: shulker_demo(features["shulker"]),
        "recordings": lambda: recordings_demo(demo["recordings"]),
    }


def build_doc(site, entry, guides, modules, translate, demo, landing):
    values, source = load_doc(site.language, entry["slug"], site.config)
    renderer = Renderer(site.language, site.resolve_link, figures(site, modules, translate, demo, landing), slug_prefix=entry["slug"] + "-")
    body = renderer.render(source)
    if entry["slug"] == "modules":
        body = body.replace(tag("div", "", data_marker=MODULE_MARKER), module_reference(site, modules, guides, translate))
    title = entry["title"]
    description = substitute(entry["description"], site.config)
    header = tag(
        "header",
        tag("p", text(site.interface["docs"]["groups"][entry["group"]]), class_="eyebrow")
        + tag("h1", text(title), class_="display docs__title")
        + tag("p", text(description), class_="docs__summary"),
        class_="docs__header",
    )
    article = tag("article", header + tag("div", body, class_="prose"), class_="docs__article")
    layout = tag(
        "div",
        tag("aside", tag("nav", docs_nav(site, guides, entry["slug"]), class_="docs-nav", aria_label=site.interface["docs"]["menu"]), class_="docs__sidebar")
        + tag(
            "div",
            mobile_bar(site, guides, entry["slug"], title) + breadcrumb(site, guides, entry) + article + pager(site, guides, entry["slug"]),
            class_="docs__content",
        )
        + table_of_contents(site, renderer.headings),
        class_="container docs",
        data_docs=True,
    )
    layout += json_script("demo-strings", {key: demo[key] for key in ("hud", "recordings")})
    return page(
        site,
        f"docs/{entry['slug']}",
        title,
        description,
        layout,
        ["site.css", "docs.css"],
        ["scripts/main.js"],
        active_section="docs",
        main_class="docs-page",
    )


def build_docs_index(site, guides):
    strings = site.interface["docs"]
    groups = []
    for group in guides["groups"]:
        entries = [entry for entry in guides["pages"] if entry["group"] == group]
        cards = join(
            tag(
                "a",
                tag("span", icon(entry["icon"], 22), class_="guide-card__icon")
                + tag("strong", text(entry["title"]))
                + tag("span", text(substitute(entry["description"], site.config)))
                + tag("span", icon("arrow-right", 18), class_="guide-card__arrow"),
                class_="guide-card",
                href=site.url("docs/" + entry["slug"]),
            )
            for entry in entries
        )
        groups.append(tag("section", tag("h2", text(strings["groups"][group]), class_="docs-index__group") + tag("div", cards, class_="guide-grid"), class_="docs-index__section"))
    header = tag(
        "header",
        tag("p", text(strings["title"]), class_="eyebrow")
        + tag("h1", text(site.interface["docsIndex"]["title"]), class_="display docs__title")
        + tag("p", text(site.interface["docsIndex"]["lead"]), class_="docs__summary"),
        class_="docs__header docs__header--index",
    )
    body = tag("div", header + join(groups), class_="container docs-index")
    return page(
        site,
        "docs",
        strings["title"],
        site.interface["docsIndex"]["lead"],
        body,
        ["site.css", "docs.css"],
        ["scripts/main.js"],
        active_section="docs",
        main_class="docs-page",
    )
