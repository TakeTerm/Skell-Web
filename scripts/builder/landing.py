from .content import landing_values, substitute
from .demos import hud_editor, kill_demo, recordings_demo
from .gui_window import ACCENTS, hero_window, interactive_window
from .icons import icon
from .layout import json_script
from .markup import join, tag, text
from .widgets import clip_toast, control_templates, hud_widget, lyrics_island, shulker_demo

DEMO_TABS = [("gui", "sliders"), ("hud", "layout"), ("kill", "sparkles"), ("recordings", "video")]
STAGE_WIDGETS = [("fps", "t-l", 14, 14), ("coordinates", "t-l", 14, 52)]
WIDGET_NAMES = {"fps": "FPS", "coordinates": "Coordinates"}


def resolve_values(node, values):
    if isinstance(node, str):
        return substitute(node, values)
    if isinstance(node, list):
        return [resolve_values(item, values) for item in node]
    if isinstance(node, dict):
        return {key: resolve_values(value, values) for key, value in node.items()}
    return node


def headline(title):
    return text(title).replace("*", "\x00").replace("\x00", "<em>", 1).replace("\x00", "</em>", 1)


def hero(site, copy, modules, translate, demo, features):
    config = site.config
    primary = tag(
        "a",
        copy["primary"] + icon("arrow-down", 18, "icon icon-arrow"),
        class_="btn btn--primary",
        href="#demo",
    )
    secondary = tag("a", copy["secondary"], class_="btn btn--ghost", href=site.url("docs/getting-started"))
    note = tag("p", tag("span", "", class_="pulse") + text(copy["note"]), class_="hero__note")
    text_column = tag(
        "div",
        tag("p", text(copy["eyebrow"]), class_="eyebrow hero__rise", style="--i:0")
        + tag("h1", headline(copy["title"]), class_="display hero__title hero__rise", style="--i:1")
        + tag("p", text(copy["lead"]), class_="hero__lead hero__rise", style="--i:2")
        + tag("div", primary + secondary, class_="hero__actions hero__rise", style="--i:3")
        + tag("div", note, class_="hero__rise", style="--i:4"),
        class_="hero__copy",
    )
    window = tag(
        "div",
        tag("div", hero_window(modules, translate, demo["gui"], config), class_="frame__inner"),
        class_="frame hero__frame",
        role="img",
        aria_label=copy["previewLabel"],
    )
    floats = join(
        [
            tag("div", clip_toast(features["clip"]), class_="hero__float hero__float--toast", aria_hidden="true"),
            tag("div", hud_widget("fps", demo["hud"]), class_="hero__float hero__float--fps", aria_hidden="true"),
            tag("div", lyrics_island(features["lyrics"]), class_="hero__float hero__float--island", aria_hidden="true"),
        ]
    )
    stage = tag(
        "div",
        tag("div", "", class_="hero__glow") + window + floats,
        class_="hero__stage hero__rise hero__rise--stage",
        style="--i:2",
        data_hero_stage=True,
    )
    scroll = tag("a", text(copy["scrollHint"]) + icon("arrow-down", 16), class_="hero__scroll", href="#demo")
    intro = tag("div", tag("span", "", class_="intro__mark"), class_="intro", aria_hidden="true", data_intro=True)
    return tag(
        "section",
        intro + tag("div", text_column + stage, class_="container hero__grid") + scroll,
        class_="hero",
        id="top",
    )


def demo_section(site, copy, modules, translate, demo, language):
    config = site.config
    tab_buttons = join(
        tag(
            "button",
            icon(icon_name, 17) + text(copy["tabs"][key]),
            type="button",
            class_="tabs__tab",
            role="tab",
            id=f"tab-{key}",
            aria_selected="true" if index == 0 else "false",
            aria_controls=f"panel-{key}",
            tabindex=0 if index == 0 else -1,
            data_tab=key,
        )
        for index, (key, icon_name) in enumerate(DEMO_TABS)
    )
    tabs = tag(
        "div",
        tag("span", "", class_="tabs__indicator", data_indicator=True) + tab_buttons,
        class_="tabs",
        role="tablist",
        aria_label=copy["eyebrow"],
    )
    contents = {
        "gui": interactive_window(modules, translate, demo["gui"], config, language),
        "hud": hud_editor(demo["hud"], translate),
        "kill": kill_demo(demo["kill"], translate),
        "recordings": recordings_demo(demo["recordings"]),
    }
    panels = join(
        tag(
            "div",
            contents[key],
            class_="demo__panel" + (" is-active" if index == 0 else ""),
            role="tabpanel",
            id=f"panel-{key}",
            aria_labelledby=f"tab-{key}",
            data_panel=key,
        )
        for index, (key, _) in enumerate(DEMO_TABS)
    )
    head = tag(
        "div",
        tag("p", text(copy["eyebrow"]), class_="eyebrow")
        + tag("h2", text(copy["title"]), class_="display section__title")
        + tag("p", text(copy["lead"]), class_="section__lead"),
        class_="section__head reveal",
    )
    frame = tag(
        "div",
        tag("div", tag("div", panels, class_="demo__panels"), class_="frame__inner"),
        class_="frame demo__frame reveal",
        style="--delay:2",
    )
    return tag(
        "section",
        tag(
            "div",
            head
            + tag(
                "div",
                tabs + tag("button", icon("reset", 16) + text(copy["reset"]), type="button", class_="btn btn--ghost btn--small demo__reset", data_demo_reset=True),
                class_="demo__tabs reveal",
                style="--delay:1",
            )
            + frame
            + tag("p", text(copy["note"]), class_="demo__note"),
            class_="container",
        ),
        class_="section demo",
        id="demo",
        data_demo=True,
        style="--glow: radial-gradient(70% 55% at 50% 40%, rgba(108,123,255,.11), transparent)",
    )


def layout_visual(strings):
    options = join(
        tag("button", text(label), type="button", class_="segmented__option", aria_pressed="true" if value == "sheet" else "false", data_viz_layout=value)
        for value, label in (("sheet", strings["sheet"]), ("panel", strings["panel"]))
    )
    swatches = join(
        tag("button", "", type="button", class_="swatch", style=f"--swatch:{color}", aria_label=name, aria_pressed="true" if index == 0 else "false", data_viz_accent=color)
        for index, (name, color) in enumerate(ACCENTS)
    )
    cards = join(tag("span", tag("i", "") + tag("b", "") + tag("u", ""), class_="viz__card") for _ in range(6))
    mock = tag(
        "div",
        tag("div", tag("span", "") * 3, class_="viz__bar")
        + tag("div", tag("span", "", class_="viz__side") + tag("div", cards, class_="viz__cards") + tag("div", tag("i", "") * 5, class_="viz__settings"), class_="viz__body"),
        class_="viz__window",
        aria_hidden="true",
    )
    controls = tag("div", tag("div", options, class_="segmented", role="group", aria_label=strings["label"]) + tag("div", swatches, class_="swatches", role="group"), class_="viz__controls")
    return tag("div", mock + controls, class_="viz", data_layout_viz=True, data_layout="sheet")


def mini_hud(strings, translate):
    widgets = join(
        hud_widget(
            kind,
            strings["hud"],
            tabindex=0,
            role="button",
            aria_label=f"{translate(WIDGET_NAMES[kind])}. {strings['hud']['widgetHelp']}",
            data_anchor=anchor,
            data_dx=dx,
            data_dy=dy,
            data_name=translate(WIDGET_NAMES[kind]),
        )
        for kind, anchor, dx, dy in STAGE_WIDGETS
    )
    stage = tag(
        "div",
        tag("span", "", class_="hude__scene hude__scene--mini", aria_hidden="true")
        + tag("div", tag("i", "", data_guide="x") + tag("i", "", data_guide="y"), class_="hude__guides", aria_hidden="true")
        + widgets,
        class_="hude__stage",
        data_stage=True,
    )
    hint = tag("p", icon("grip", 16) + text(strings["features"]["hudMini"]["hint"]), class_="viz__hint")
    return tag("div", stage + hint, class_="hude hude--mini", data_hud_editor=True, data_mini=True, data_snap=6, data_gap=4)


def kill_visual(strings):
    return tag(
        "div",
        tag("canvas", "", class_="killd__canvas", data_kill_mini=True, role="img", aria_label=strings["kill"]["canvasLabel"])
        + tag("div", clip_toast(strings["features"]["clip"]), class_="viz__toast", data_mini_toast=True),
        class_="viz viz--kill",
    )


def music_visual(strings):
    return tag(
        "div",
        tag("div", lyrics_island(strings["features"]["lyrics"]), class_="viz__island")
        + tag("div", hud_widget("music", strings["hud"]), class_="viz__music"),
        class_="viz viz--music",
    )


def feature_visual(item_id, strings, translate):
    builders = {
        "interface": lambda: layout_visual(strings["features"]["layouts"]),
        "hud": lambda: mini_hud(strings, translate),
        "visuals": lambda: kill_visual(strings),
        "music": lambda: music_visual(strings),
        "utilities": lambda: shulker_demo(strings["features"]["shulker"]),
    }
    return builders[item_id]()


def feature(site, item, strings, translate, index):
    wide = index % 2 == 0
    link = tag("a", item["link"] + icon("arrow-right", 16), class_="text-link", href=site.resolve_link(item["target"]))
    copy = tag(
        "div",
        tag("p", icon(item["icon"], 18) + text(item["kicker"]), class_="feature__kicker")
        + tag("h3", text(item["title"]), class_="display feature__title")
        + tag("p", text(item["text"]), class_="feature__text")
        + link,
        class_="feature__copy",
    )
    visual = tag("div", feature_visual(item["id"], strings, translate), class_="feature__visual")
    modifier = "wide" if wide else "compact"
    flip = " feature--flip" if (wide and index % 4 == 2) or (not wide and index % 4 == 3) else ""
    return tag(
        "article",
        copy + visual,
        class_=f"feature feature--{modifier}{flip} reveal",
        id=item["id"],
    )


def features_section(site, copy, strings, translate):
    head = tag(
        "div",
        tag("p", text(copy["eyebrow"]), class_="eyebrow")
        + tag("h2", text(copy["title"]), class_="display section__title")
        + tag("p", text(copy["lead"]), class_="section__lead"),
        class_="section__head reveal",
    )
    items = join(feature(site, item, strings, translate, index) for index, item in enumerate(copy["items"]))
    return tag(
        "section",
        tag("div", head + tag("div", items, class_="features__list"), class_="container"),
        class_="section features",
        id="features",
        style="--glow: radial-gradient(60% 40% at 15% 30%, rgba(108,123,255,.08), transparent), radial-gradient(50% 40% at 90% 75%, rgba(180,92,255,.07), transparent)",
    )


def project_section(site, copy, values):
    stats = join(
        tag(
            "div",
            tag("strong", text(stat["value"]), class_="display") + tag("span", text(stat["label"])),
            class_="project__stat reveal",
            style=f"--delay:{index}",
        )
        for index, stat in enumerate(copy["stats"])
    )
    actions = join(
        [
            tag("a", copy["actions"]["learn"], class_="btn btn--primary", href="#features"),
            tag("a", copy["actions"]["demo"], class_="btn btn--ghost", href="#demo"),
            tag("a", copy["actions"]["guides"], class_="btn btn--ghost", href=site.url("docs/getting-started")),
        ]
    )
    mark = tag("span", "", class_="project__mark", aria_hidden="true")
    body = tag(
        "div",
        tag("p", text(copy["eyebrow"]), class_="eyebrow")
        + tag("p", text(copy["statement"]), class_="display project__statement")
        + tag("p", tag("span", "", class_="project__credit-mark") + text(copy["developedBy"]), class_="project__credit")
        + tag("p", tag("span", "", class_="pulse") + text(copy["launch"]), class_="hero__note")
        + tag("div", actions, class_="project__actions")
        + tag("div", stats, class_="project__stats")
        + tag("p", text(copy["linesNote"]), class_="project__note"),
        class_="project__body reveal",
    )
    return tag(
        "section",
        mark + tag("div", body, class_="container"),
        class_="section project",
        id="project",
        style="--glow: radial-gradient(60% 55% at 70% 50%, rgba(180,92,255,.12), transparent), radial-gradient(50% 50% at 20% 60%, rgba(108,123,255,.08), transparent)",
    )


def build_landing(site, modules, stats, translate, demo, landing):
    values = landing_values(site.config, modules, stats)
    copy = resolve_values(landing, values)
    language = site.language
    body = join(
        [
            hero(site, copy["hero"], modules, translate, demo, copy["features"]),
            demo_section(site, copy["demo"], modules, translate, demo, language),
            features_section(site, copy["features"], {**demo, "features": copy["features"]}, translate),
            project_section(site, copy["project"], values),
            control_templates(demo["gui"]),
            json_script("demo-strings", {"gui": demo["gui"], "hud": demo["hud"], "kill": demo["kill"], "recordings": demo["recordings"]}),
        ]
    )
    return body
