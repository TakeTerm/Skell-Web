import json
import pathlib
import re
import sys
from collections import Counter

STRING = r'"((?:[^"\\]|\\.)*)"'
CLARITY_PACKAGE = "clarity/modules/visual"
SETTING_PATTERN = re.compile(
    r"add\(new (Bool|Number|Mode|Color|String)Setting\(([^;]*?)\)\)(?:\.in\(" + STRING + r"\))?",
    re.S,
)
OPTION_OVERRIDES = {
    ("Kill Efects", "Effect"): ["Random", "Execution", "Singularity", "Soul Pyre", "Tung Tung", "Tung Tung Floss", "Samurai"],
}
CATEGORY_LABELS = {
    "HUD": "HUD",
    "PVP": "PvP",
    "UTILITY": "Utility",
    "VISUALS": "Visuals",
    "COSMETICS": "Cosmetics",
    "CLIENT": "Client",
}


def read_registered_classes(source):
    manager = (source / "module/ModuleManager.java").read_text()
    direct = re.findall(r"MODULES\.add\(new (\w+)\(\)\)", manager)
    clarity_block = re.search(r"for \(String n : new String\[\] \{(.*?)\}\)", manager, re.S)
    clarity = re.findall(r'"(\w+)"', clarity_block[1]) if clarity_block else []
    return direct, clarity


def read_catalog(source):
    text = (source / "ui/Catalog.java").read_text()
    new_ids = re.search(r"Set<String> NEW = Set\.of\((.*?)\);", text, re.S)
    groups = {}
    for match in re.finditer(r'\bg\("([^"]+)",((?:\s*"[^"]+",?)+)\)', text):
        for module_id in re.findall(r'"([^"]+)"', match[2]):
            groups.setdefault(module_id, match[1])
    return set(re.findall(r'"([^"]+)"', new_ids[1])), groups


def split_camel_case(name):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name)


def detect_category(text, constructor_tail):
    explicit = re.search(r"Category\.(\w+)", constructor_tail[:240])
    if explicit:
        return explicit[1]
    if re.search(r"extends (?:Stat)?HudModule", text):
        return "HUD"
    if "extends Cosmetic" in text:
        return "COSMETICS"
    return "CLIENT"


def parse_number(arguments):
    numbers = re.findall(r"(?<![\w.])-?(?:\d+(?:\.\d+)?|\.\d+)", arguments)
    if len(numbers) < 3:
        return {}
    values = {"default": float(numbers[0]), "min": float(numbers[1]), "max": float(numbers[2])}
    if len(numbers) >= 4:
        values["step"] = float(numbers[3])
    return values


def parse_settings(text):
    settings = []
    for match in SETTING_PATTERN.finditer(text):
        kind, arguments, group = match.groups()
        strings = re.findall(STRING, arguments)
        if not strings:
            continue
        owner = re.search(r"(\w+)\s*=\s*$", text[: match.start()])
        hidden = owner and re.search(
            r"\b" + re.escape(owner[1]) + r"\.visible\s*=\s*\(\)\s*->\s*false", text
        )
        if hidden:
            continue
        entry = {"name": strings[0], "type": kind.lower(), "group": group}
        remainder = arguments[arguments.find('"', arguments.find('"') + 1) + 1 :]
        if kind == "Bool":
            entry["default"] = bool(re.match(r"\s*,\s*true", remainder))
        elif kind == "Number":
            entry.update(parse_number(remainder))
        elif kind == "Mode":
            options_text, _, default_text = arguments.partition(").def(")
            options = re.findall(STRING, options_text)[1:]
            entry["options"] = options
            default = re.findall(STRING, default_text)
            entry["default"] = default[0] if default else (options[0] if options else None)
        elif kind == "String":
            entry["default"] = strings[1] if len(strings) > 1 else ""
        settings.append(entry)
    return settings


def parse_clarity_settings(rows):
    settings = []
    for label, kind, value in (row[:3] for row in rows):
        entry = {"name": label, "group": None}
        if kind == "check":
            entry.update(type="bool", default=value)
        elif kind == "range":
            entry.update(type="number", min=value[0], max=value[1], default=value[2])
        elif kind in ("select", "skinselect", "capeselect"):
            entry.update(type="mode", options=value if isinstance(value, list) else [value])
        elif kind in ("text", "keybind"):
            entry.update(type="string", default=value)
        elif kind == "color":
            entry.update(type="color")
        else:
            continue
        settings.append(entry)
    return settings


def build_module(path, clarity_catalog, new_ids, groups):
    text = path.read_text()
    full = re.search(r"super\(\s*" + STRING + r"\s*,\s*" + STRING, text)
    short = re.search(
        r"super\(\s*" + STRING + r"\s*,\s*(?:dev\.skell\.client\.module\.)?Category\.(\w+)", text
    )
    if full:
        name, description = full.groups()
        category = detect_category(text, text[full.end() :])
        settings = parse_settings(text)
    elif short:
        name, category = short.groups()
        description = clarity_catalog["descriptions"].get(name, "").rstrip(".")
        settings = parse_clarity_settings(clarity_catalog["settings"].get(name, []))
    else:
        raise ValueError("Unrecognized module constructor in " + path.name)
    for setting in settings:
        override = OPTION_OVERRIDES.get((name, setting["name"]))
        if override:
            setting["options"], setting["default"] = override, override[0]
    display = name if " " in name else split_camel_case(name)
    module_id = display.lower().replace(" ", "")
    return {
        "id": module_id,
        "name": display,
        "description": description,
        "category": CATEGORY_LABELS[category],
        "group": groups.get(module_id),
        "new": module_id in new_ids,
        "settings": settings,
    }


def main(source, catalog_path, output):
    source = pathlib.Path(source)
    clarity_catalog = json.loads(pathlib.Path(catalog_path).read_text())
    direct, clarity = read_registered_classes(source)
    new_ids, groups = read_catalog(source)
    order = direct[:-3] + clarity + direct[-3:]
    modules = []
    for class_name in order:
        path = next(source.rglob(class_name + ".java"))
        modules.append(build_module(path, clarity_catalog, new_ids, groups))
    ids = [module["id"] for module in modules]
    assert len(set(ids)) == len(ids), [i for i, n in Counter(ids).items() if n > 1]
    pathlib.Path(output).write_text(json.dumps(modules, indent=1, ensure_ascii=False) + "\n")
    counts = Counter(module["category"] for module in modules)
    print(len(modules), "modules", dict(counts))


if __name__ == "__main__":
    main(*sys.argv[1:4])
