from .content import CATEGORY_ORDER
from .icons import icon
from .markup import join, tag, text

CATEGORY_ICONS = {
    "HUD": "hud",
    "PvP": "target",
    "Utility": "wrench",
    "Visuals": "eye",
    "Cosmetics": "sparkles",
    "Client": "sliders",
}
NAVIGATION = [("modules", ["HUD", "PvP", "Utility", "Visuals"]), ("style", ["Cosmetics"]), ("client", ["Client"])]
GROUP_ORDER = {
    "HUD": ["Info", "Player", "Media", "Game UI"],
    "PvP": ["Combat info", "Stats"],
    "Utility": ["Movement", "Capture", "Inventory", "World", "System"],
    "Visuals": ["Combat", "World", "Camera", "Hands & motion", "Player", "Effects"],
}
ACCENTS = [
    ("Indigo", "#6c7bff"),
    ("Orange", "#ff8a2b"),
    ("Purple", "#a970ff"),
    ("Blue", "#4da3ff"),
    ("Red", "#ff4d5e"),
    ("Pink", "#ff6fb5"),
    ("Green", "#4dff9a"),
    ("White", "#f2f2f2"),
]
HIDDEN_MODULES = {"interface", "skellusers", "discordrpc"}
HERO_MODULES = ["fps", "coordinates", "musicplayer", "lyrics", "radar", "clock", "lightmeter", "pickupfeed"]
HERO_ENABLED = {"fps", "coordinates", "musicplayer", "lyrics"}
DEMO_ENABLED = {"fps", "coordinates", "keystrokes", "zoom", "killefects", "cape"}


def switch(on, label):
    return tag(
        "button",
        tag("span", "", class_="skswitch__knob"),
        type="button",
        class_="skswitch",
        role="switch",
        aria_checked="true" if on else "false",
        aria_label=label,
    )


def module_card(module, translate, strings, on):
    name = translate(module["name"])
    badge = tag("span", "NEW", class_="badge badge--new") if module["new"] else ""
    title = tag("h4", tag("span", text(name), class_="skcard__name") + badge)
    body = tag("div", title + tag("p", text(translate(module["description"]))), class_="skcard__text")
    controls = tag(
        "div",
        tag(
            "button",
            icon("sliders", 16),
            type="button",
            class_="skcard__gear",
            aria_label=f"{strings['settings']}: {name}",
            data_open_settings=True,
        )
        + switch(on, f"{strings['enabled']}: {name}"),
        class_="skcard__controls",
    )
    return tag(
        "article",
        tag("span", icon(CATEGORY_ICONS[module["category"]], 18), class_="skcard__icon") + body + controls,
        class_="skcard" + (" is-on" if on else "") + (" is-new" if module["new"] else ""),
        data_module=module["id"],
        data_group=module["group"],
    )


def navigation_button(category, translate, total, active_count, selected):
    return tag(
        "button",
        icon(CATEGORY_ICONS[category], 18)
        + tag("span", text(translate(category)), class_="skui__nav-name")
        + tag("span", f"{active_count}/{total}", class_="skui__nav-count") * (category != "Client"),
        type="button",
        class_="skui__nav" + (" is-active" if selected else ""),
        data_page_target=category,
        aria_current="page" if selected else None,
    )


def sidebar(modules, translate, strings, enabled, selected="HUD"):
    sections = []
    for key, categories in NAVIGATION:
        buttons = []
        for category in categories:
            members = [m for m in modules if m["category"] == category]
            active = sum(1 for m in members if m["id"] in enabled)
            buttons.append(navigation_button(category, translate, len(members), active, category == selected))
        sections.append(tag("p", text(strings["sections"][key]), class_="skui__label") + join(buttons))
    return tag("nav", join(sections), class_="skui__side", aria_label=strings["title"])


def group_chips(category, members, translate, strings):
    counts = {}
    for module in members:
        counts[module["group"]] = counts.get(module["group"], 0) + 1
    chips = [
        tag(
            "button",
            text(strings["allGroup"]) + tag("span", str(len(members))),
            type="button",
            class_="skchip is-active",
            data_group_filter="",
        )
    ]
    for group in GROUP_ORDER[category]:
        if group in counts:
            chips.append(
                tag(
                    "button",
                    text(translate(group)) + tag("span", str(counts[group])),
                    type="button",
                    class_="skchip",
                    data_group_filter=group,
                )
            )
    return tag("div", join(chips), class_="skui__chips", role="group")


def ordered(members, category):
    groups = GROUP_ORDER[category]
    return sorted(members, key=lambda m: (not m["new"], groups.index(m["group"]) if m["group"] in groups else 99))


def module_page(category, modules, translate, strings, enabled, selected):
    members = [m for m in modules if m["category"] == category and m["id"] not in HIDDEN_MODULES]
    if category == "Cosmetics":
        cards = join(module_card(m, translate, strings, m["id"] in enabled) for m in members)
        chips = ""
    else:
        cards = join(module_card(m, translate, strings, m["id"] in enabled) for m in ordered(members, category))
        chips = group_chips(category, members, translate, strings)
    header = tag(
        "div",
        tag("h3", text(translate(category))) + chips,
        class_="skui__page-head",
    )
    return tag(
        "div",
        header + tag("div", cards, class_="skui__grid"),
        class_="skui__page",
        data_page=category,
        hidden=not selected,
    )


def client_page(translate, strings, language):
    labels = strings["client"]
    layout = tag(
        "div",
        join(
            tag(
                "button",
                text(label),
                type="button",
                class_="segmented__option",
                aria_pressed="true" if index == 0 else "false",
                data_layout_choice=value,
            )
            for index, (value, label) in enumerate(zip(("sheet", "panel"), labels["layoutOptions"]))
        ),
        class_="segmented",
        role="group",
        aria_label=labels["layout"],
    )
    animations = tag(
        "div",
        join(
            tag(
                "button",
                text(label),
                type="button",
                class_="segmented__option",
                aria_pressed="true" if index == 0 else "false",
                data_animation_choice=value,
            )
            for index, (value, label) in enumerate(zip(("full", "reduced", "off"), labels["animationsOptions"]))
        ),
        class_="segmented",
        role="group",
        aria_label=labels["animations"],
    )
    languages = tag(
        "div",
        join(
            tag(
                "a",
                text(name),
                class_="segmented__option",
                href=f"{prefix}#demo",
                aria_current="true" if code == language else None,
                data_language_choice=code,
                lang=code,
            )
            for code, name, prefix in (("en", "English", "/"), ("es", "Español", "/es/"))
        ),
        class_="segmented",
    )
    accent = tag(
        "div",
        join(
            tag("button", "", type="button", class_="swatch", style=f"--swatch:{color}", aria_label=translate(name) if name != "Indigo" else name, aria_pressed="true" if index == 0 else "false", data_accent=color)
            for index, (name, color) in enumerate(ACCENTS)
        ),
        class_="swatches",
        role="group",
        aria_label=labels["accent"],
    )
    rows = join(
        tag(
            "div",
            tag("div", tag("strong", text(label)) + tag("span", text(hint)), class_="skrow__text") + control,
            class_="skrow skrow--client",
        )
        for label, hint, control in (
            (labels["accent"], labels["accentHint"], accent),
            (labels["layout"], labels["layoutHint"], layout),
            (labels["animations"], labels["animationsHint"], animations),
            (labels["language"], labels["languageHint"], languages),
        )
    )
    return tag(
        "div",
        tag("div", tag("h3", text(translate("Client"))), class_="skui__page-head") + tag("div", rows, class_="skui__client"),
        class_="skui__page",
        data_page="Client",
        hidden=True,
    )


def settings_surface(strings):
    return tag(
        "aside",
        tag(
            "div",
            tag("div", "", class_="skset__preview", data_preview=True)
            + tag(
                "div",
                tag("h4", "", data_settings_title=True)
                + tag(
                    "button",
                    icon("close", 18),
                    type="button",
                    class_="skset__close",
                    aria_label=strings["close"],
                    data_close_settings=True,
                ),
                class_="skset__head",
            )
            + tag("div", "", class_="skset__body", data_settings_body=True)
            + tag(
                "button",
                icon("reset", 16) + text(strings["reset"]),
                type="button",
                class_="skset__reset",
                data_reset_settings=True,
            ),
            class_="skset__inner",
        ),
        class_="skset",
        data_settings=True,
        hidden=True,
        aria_label=strings["settings"],
    )


def search_bar(strings):
    return tag(
        "label",
        icon("search", 16)
        + tag(
            "input",
            type="search",
            placeholder=strings["search"],
            aria_label=strings["search"],
            autocomplete="off",
            spellcheck="false",
            data_search=True,
        )
        + tag("kbd", strings["searchKeys"]),
        class_="skui__search",
    )


def title_bar(strings, version, with_search):
    return tag(
        "div",
        tag("span", "", class_="skui__logo")
        + tag("span", text(strings["title"]), class_="skui__title")
        + tag("span", version, class_="skui__version")
        + (search_bar(strings) if with_search else ""),
        class_="skui__bar",
    )


def interactive_window(modules, translate, strings, config, language):
    pages = [
        module_page(category, modules, translate, strings, DEMO_ENABLED, category == "HUD")
        for category in ("HUD", "PvP", "Utility", "Visuals", "Cosmetics")
    ]
    pages.append(client_page(translate, strings, language))
    results = tag(
        "div",
        tag("div", "", class_="skui__grid", data_results=True)
        + tag("p", text(strings["noResults"]), class_="skui__empty", data_empty=True, hidden=True),
        class_="skui__page skui__page--results",
        data_page="results",
        hidden=True,
    )
    main = tag("section", join(pages) + results, class_="skui__main", data_main=True)
    body = tag("div", sidebar(modules, translate, strings, DEMO_ENABLED) + main + settings_surface(strings), class_="skui__body")
    return tag(
        "div",
        title_bar(strings, config["version"], True) + body,
        class_="skui",
        data_gui=True,
        data_layout="sheet",
    )


def hero_window(modules, translate, strings, config):
    by_id = {module["id"]: module for module in modules}
    cards = join(
        module_card(by_id[module_id], translate, strings, module_id in HERO_ENABLED) for module_id in HERO_MODULES
    )
    head = tag("div", tag("h3", text(translate("HUD"))), class_="skui__page-head")
    main = tag("section", tag("div", head + tag("div", cards, class_="skui__grid"), class_="skui__page"), class_="skui__main")
    body = tag("div", sidebar(modules, translate, strings, HERO_ENABLED) + main, class_="skui__body")
    return tag("div", title_bar(strings, config["version"], False) + body, class_="skui skui--static")
