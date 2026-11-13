from .content import landing_values, substitute
from .demos import hud_editor, kill_demo, recordings_demo
from .gui_window import ACCENTS, interactive_window
from .icons import icon
from .layout import json_script
from .markup import join, tag, text
from .widgets import control_templates, hud_widget

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


def demo_section(site, copy, modules, translate, demo, language, identifier="demo"):
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
        id=identifier,
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


