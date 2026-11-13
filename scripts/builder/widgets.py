from .icons import icon
from .markup import join, tag, text

KEY_ROWS = [["", "W", ""], ["A", "S", "D"]]
RADAR_DOTS = [(0.62, 0.3, "player"), (0.3, 0.62, "player"), (0.72, 0.68, "checkpoint")]


def keystrokes():
    cells = [
        tag("span", letter, class_="hudk" + (" hudk--empty" if not letter else ""), data_key=letter or None)
        for row in KEY_ROWS
        for letter in row
    ]
    return tag("div", join(cells) + tag("span", "", class_="hudk hudk--space", data_key="space"), class_="hudw__keys")


def radar():
    dots = join(
        tag("circle", "", cx=round(x * 100), cy=round(y * 100), r=4, class_=f"hudw__dot hudw__dot--{kind}")
        for x, y, kind in RADAR_DOTS
    )
    letters = join(
        tag("text", letter, x=x, y=y, class_="hudw__compass", text_anchor="middle")
        for letter, x, y in (("N", 50, 13), ("E", 91, 54), ("S", 50, 95), ("W", 9, 54))
    )
    ring = tag("circle", "", cx=50, cy=50, r=44, class_="hudw__ring") + tag("circle", "", cx=50, cy=50, r=24, class_="hudw__ring hudw__ring--inner")
    sweep = tag("path", "", d="M50 50 L50 6 A44 44 0 0 1 88 28 Z", class_="hudw__sweep")
    return tag("svg", ring + sweep + letters + dots, viewBox="0 0 100 100", class_="hudw__radar", aria_hidden="true")


def music(strings):
    cover = tag("span", icon("music", 20), class_="hudw__cover")
    info = tag(
        "div",
        tag("strong", text(strings["song"])) + tag("span", text(strings["artist"])) + tag("span", tag("i", ""), class_="hudw__progress"),
        class_="hudw__track",
    )
    return cover + info


def armor():
    slots = [tag("span", icon("box", 16), class_="hudw__slot") for _ in range(4)]
    return join(slots)


def hud_widget(kind, strings, **attributes):
    labels = strings["widgets"]
    contents = {
        "fps": tag("span", labels["fps"], class_="hudw__label") + tag("span", "144", class_="hudw__value"),
        "coordinates": tag("span", "XYZ", class_="hudw__label") + tag("span", "128 · 72 · −340", class_="hudw__value"),
        "keystrokes": keystrokes(),
        "radar": radar(),
        "music": music(labels),
        "armor": armor(),
    }
    return tag(
        "div",
        contents[kind],
        class_=f"hudw hudw--{kind}",
        data_widget=kind,
        **attributes,
    )


def clip_toast(strings, **attributes):
    return tag(
        "div",
        tag("span", icon("check", 18), class_="toast__icon")
        + tag("div", tag("strong", text(strings["title"])) + tag("span", text(strings["subtitle"])))
        + tag("span", tag("i", ""), class_="toast__timer"),
        class_="toast",
        role="status",
        **attributes,
    )


def lyrics_island(strings, **attributes):
    equalizer = tag("span", tag("i", "") * 4, class_="island__eq")
    disc = tag("span", "", class_="island__disc")
    return tag(
        "div",
        disc + tag("span", tag("span", text(strings["line"]), class_="island__line"), class_="island__window") + equalizer,
        class_="island",
        **attributes,
    )


def shulker_slots(count_labels):
    counts = {1: "64", 4: "16", 8: "3", 11: "64", 14: "1", 20: "32", 23: "12"}
    cells = []
    for index in range(27):
        filled = index in counts
        content = tag("span", counts[index], class_="shulker__count") if filled and count_labels else ""
        cells.append(tag("span", content, class_="shulker__slot" + (" is-filled" if filled else ""), style=f"--n:{index}"))
    return join(cells)


def shulker_demo(strings):
    box = tag(
        "button",
        tag("span", "", class_="shulker__lid") + tag("span", "", class_="shulker__body") + tag("span", text(strings["hint"]), class_="shulker__hint"),
        type="button",
        class_="shulker__box",
        aria_pressed="false",
        aria_label=strings["label"],
        data_shulker_box=True,
    )
    tooltip = tag(
        "div",
        tag("strong", text(strings["title"])) + tag("div", shulker_slots(True), class_="shulker__grid"),
        class_="shulker__tooltip",
        data_shulker_tooltip=True,
        aria_hidden="true",
    )
    return tag("div", box + tooltip, class_="shulker", data_shulker=True)


def control_templates(strings):
    label = tag("span", "", class_="skrow__label")
    templates = {
        "group": tag("h5", "", class_="skset__group"),
        "bool": tag("div", label + tag("button", tag("span", "", class_="skswitch__knob"), type="button", class_="skswitch", role="switch"), class_="skrow"),
        "number": tag(
            "div",
            label + tag("div", tag("input", type="range", class_="skslider__input") + tag("output", "", class_="skslider__value"), class_="skslider"),
            class_="skrow skrow--stack",
        ),
        "mode": tag("div", label + tag("div", "", class_="segmented", role="group"), class_="skrow skrow--stack"),
        "select": tag(
            "div",
            label + tag("div", tag("select", "", class_="skselect__input") + icon("chevron-down", 16), class_="skselect"),
            class_="skrow",
        ),
        "color": tag("div", label + tag("input", type="color", class_="skcolor"), class_="skrow"),
        "text": tag("div", label + tag("input", type="text", class_="sktext", maxlength=32), class_="skrow"),
        "keybind": tag("div", label + tag("button", "", type="button", class_="skkey"), class_="skrow"),
    }
    return join(tag("template", markup, id=f"template-{name}") for name, markup in templates.items())
