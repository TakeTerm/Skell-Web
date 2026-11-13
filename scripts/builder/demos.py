from .icons import icon
from .markup import join, tag, text
from .widgets import clip_toast, hud_widget

HUD_WIDGETS = [
    ("fps", "FPS", "t-l", 16, 16),
    ("coordinates", "Coordinates", "t-l", 16, 58),
    ("keystrokes", "Keystrokes", "b-l", 16, 76),
    ("radar", "Radar", "t-r", 16, 16),
    ("armor", "Armor Status", "m-r", 16, 0),
    ("music", "Music Player", "b-r", 16, 76),
]
KILL_EFFECTS = ["Random", "Execution", "Singularity", "Soul Pyre", "Samurai"]
RECORDING_FILTERS = ["all", "recording", "clip"]


def switch_button(label, on=False, **attributes):
    return tag(
        "button",
        tag("span", "", class_="skswitch__knob"),
        type="button",
        class_="skswitch",
        role="switch",
        aria_checked="true" if on else "false",
        aria_label=label,
        **attributes,
    )


def hud_scene():
    return tag(
        "div",
        tag("span", "", class_="hude__sun")
        + tag("span", "", class_="hude__hills")
        + tag("span", "", class_="hude__ground")
        + tag("span", "", class_="hude__crosshair")
        + tag("span", "".join(tag("i", "") for _ in range(9)), class_="hude__hotbar"),
        class_="hude__scene",
        aria_hidden="true",
    )


def hud_editor(strings, translate):
    widgets = join(
        hud_widget(
            kind,
            strings,
            tabindex=0,
            role="button",
            aria_label=f"{translate(name)}. {strings['widgetHelp']}",
            data_anchor=anchor,
            data_dx=dx,
            data_dy=dy,
            data_name=translate(name),
        )
        for kind, name, anchor, dx, dy in HUD_WIDGETS
    )
    stage = tag(
        "div",
        hud_scene()
        + tag("div", tag("i", "", data_guide="x") + tag("i", "", data_guide="y"), class_="hude__guides", aria_hidden="true")
        + widgets
        + tag("span", "", class_="hude__resize", data_resize=True, aria_hidden="true")
        + hud_bar(strings),
        class_="hude__stage",
        data_stage=True,
    )
    return tag(
        "div",
        tag("div", stage + tag("p", text(strings["hint"]), class_="hude__hint"), class_="hude__main")
        + widgets_panel(strings, translate)
        + tag("div", "", class_="hude__announce visually-hidden", role="status", aria_live="polite", data_announce=True),
        class_="hude",
        data_hud_editor=True,
        data_snap=6,
        data_gap=4,
    )


def hud_bar(strings):
    buttons = [
        ("undo", "undo", strings["undo"]),
        ("redo", "redo", strings["redo"]),
        ("reset", "reset", strings["reset"]),
    ]
    actions = join(
        tag("button", icon(name, 17), type="button", class_="hude__action", aria_label=label, title=label, disabled=True if key != "reset" else None, data_action=key)
        for key, name, label in buttons
    )
    handle = tag("span", icon("grip", 18), class_="hude__grip", data_bar_handle=True, aria_label=strings["barHandle"], title=strings["barHandle"], role="img")
    selected = tag("span", text(strings["nothingSelected"]), class_="hude__selected", data_selected_label=True)
    return tag("div", handle + tag("span", strings["editHud"], class_="hude__bar-title") + actions + selected, class_="hude__bar", data_bar=True)


def widgets_panel(strings, translate):
    rows = join(
        tag(
            "li",
            tag("span", text(translate(name)), class_="hude__row-name")
            + switch_button(f"{strings['show']}: {translate(name)}", True, data_widget_toggle=kind),
            class_="hude__row",
        )
        for kind, name, _, _, _ in HUD_WIDGETS
    )
    return tag(
        "aside",
        tag("h4", text(strings["panel"])) + tag("ul", rows) + tag("p", "", class_="hude__anchor", data_anchor_label=True),
        class_="hude__panel",
    )


def kill_demo(strings, translate):
    effects = join(
        tag(
            "button",
            text(translate(name) if name != "Random" else strings["random"]),
            type="button",
            class_="chip",
            aria_pressed="true" if index == 0 else "false",
            data_effect=name.lower().replace(" ", "-"),
        )
        for index, name in enumerate(KILL_EFFECTS)
    )
    color_modes = join(
        tag("button", text(label), type="button", class_="segmented__option", aria_pressed="true" if index == 0 else "false", data_color_mode=value)
        for index, (value, label) in enumerate(zip(("style", "theme", "custom"), strings["colorModes"]))
    )
    sliders = join(
        tag(
            "label",
            tag("span", text(label), class_="skrow__label")
            + tag("div", tag("input", type="range", min=low, max=high, step=step, value=value, class_="skslider__input", data_kill_option=key) + tag("output", "", class_="skslider__value"), class_="skslider"),
            class_="skrow skrow--stack",
        )
        for key, label, low, high, step, value in (
            ("duration", translate("Duration"), 0.5, 6, 0.1, 2.5),
            ("scale", translate("Scale"), 0.5, 2, 0.1, 1),
        )
    )
    toggles = join(
        tag("div", tag("span", text(label), class_="skrow__label") + switch_button(label, on, data_kill_toggle=key), class_="skrow")
        for key, label, on in (("bloom", translate("Bloom"), True), ("loop", strings["loop"], True))
    )
    colors = tag(
        "div",
        tag("label", tag("span", text(translate("Primary Color")), class_="skrow__label") + tag("input", type="color", value="#6597ff", class_="skcolor", data_kill_color="primary"), class_="skrow")
        + tag("label", tag("span", text(translate("Secondary Color")), class_="skrow__label") + tag("input", type="color", value="#ff8061", class_="skcolor", data_kill_color="secondary"), class_="skrow"),
        class_="killd__colors",
        data_custom_colors=True,
        hidden=True,
    )
    stage = tag(
        "div",
        tag("canvas", "", class_="killd__canvas", data_kill_canvas=True, aria_label=strings["canvasLabel"], role="img")
        + tag("span", text(strings["badge"]), class_="killd__badge")
        + tag("button", icon("play", 16) + text(strings["replay"]), type="button", class_="btn btn--ghost btn--small killd__replay", data_kill_replay=True),
        class_="killd__stage",
    )
    controls = tag(
        "div",
        tag("div", effects, class_="killd__effects", role="group", aria_label=strings["effect"])
        + tag("div", tag("span", text(translate("Colors")), class_="skrow__label") + tag("div", color_modes, class_="segmented", role="group"), class_="skrow skrow--stack")
        + colors
        + sliders
        + toggles
        + tag("p", text(strings["note"]), class_="killd__note"),
        class_="killd__controls",
    )
    return tag("div", stage + controls, class_="killd", data_kill_demo=True)


def recording_row(strings, name, kind, duration, size, date):
    thumb = tag("span", icon("play", 16), class_="rec__thumb", style=f"--seed:{sum(map(ord, name)) % 360}")
    meta = tag(
        "span",
        text(f"{duration} · {size} · {date}"),
        class_="rec__meta",
    )
    kind_label = strings["kinds"][kind]
    title = tag("span", tag("strong", text(name)) + meta, class_="rec__title")
    actions = tag(
        "span",
        tag("button", icon("play", 16), type="button", class_="rec__action", aria_label=f"{strings['play']}: {name}", data_rec_action="play")
        + tag("button", icon("folder", 16), type="button", class_="rec__action", aria_label=f"{strings['show']}: {name}", data_rec_action="show")
        + tag("button", icon("trash", 16), type="button", class_="rec__action rec__action--danger", aria_label=f"{strings['delete']}: {name}", data_rec_action="delete", data_confirm_label=strings["confirmDelete"]),
        class_="rec__actions",
    )
    return tag("li", tag("div", thumb + title + tag("span", text(kind_label), class_=f"rec__kind rec__kind--{kind}") + actions, class_="rec__row"), class_="rec__item", data_kind=kind)


def recordings_demo(strings):
    filters = join(
        tag("button", text(label), type="button", class_="chip", aria_pressed="true" if index == 0 else "false", data_rec_filter=value)
        for index, (value, label) in enumerate(zip(RECORDING_FILTERS, strings["filters"]))
    )
    rows = join(recording_row(strings, *row) for row in strings["rows"])
    recorder = tag(
        "div",
        tag("div", tag("span", icon("video", 18), class_="rec__card-icon") + tag("div", tag("strong", text(strings["recorder"])) + tag("span", text(strings["recorderHint"]))), class_="rec__card-head")
        + tag("div", tag("span", "720p · 60 FPS · " + strings["audio"], class_="rec__spec") + tag("span", "00:00", class_="rec__timer", data_rec_timer=True), class_="rec__card-row")
        + tag("button", tag("span", "", class_="rec__dot") + tag("span", text(strings["start"]), data_rec_label=True), type="button", class_="btn btn--ghost btn--small", data_recorder_toggle=True, data_start=strings["start"], data_stop=strings["stop"]),
        class_="rec__card",
    )
    replay = tag(
        "div",
        tag("div", tag("span", icon("scissors", 18), class_="rec__card-icon") + tag("div", tag("strong", text(strings["instantReplay"])) + tag("span", text(strings["instantReplayHint"]))), class_="rec__card-head")
        + tag("div", tag("span", text(strings["warmup"]), class_="rec__spec", data_replay_status=True) + switch_button(strings["instantReplay"], False, data_replay_toggle=True), class_="rec__card-row")
        + tag("div", tag("i", ""), class_="rec__bar", data_replay_bar=True)
        + tag("button", tag("kbd", "F8") + text(strings["saveClip"]), type="button", class_="btn btn--primary btn--small", data_save_clip=True),
        class_="rec__card",
    )
    toast = clip_toast(strings["toast"], data_clip_toast=True, aria_hidden="true")
    return tag(
        "div",
        tag("div", recorder + replay, class_="rec__cards")
        + tag("div", tag("div", filters, class_="rec__filters", role="group", aria_label=strings["filterLabel"]) + tag("ul", rows, class_="rec__list", data_rec_list=True) + tag("p", text(strings["empty"]), class_="rec__empty", hidden=True, data_rec_empty=True), class_="rec__library")
        + toast,
        class_="rec",
        data_recordings_demo=True,
    )
