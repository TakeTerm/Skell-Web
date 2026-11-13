import json
import pathlib
import sys


def collect_terms(modules):
    terms = set()
    for module in modules:
        terms.update([module["name"], module["description"], module["category"]])
        if module["group"]:
            terms.add(module["group"])
        for setting in module["settings"]:
            terms.add(setting["name"])
            terms.update(option for option in setting.get("options", []))
            if setting["group"]:
                terms.add(setting["group"])
    return terms


def main(translations_path, modules_path, output):
    translations = json.loads(pathlib.Path(translations_path).read_text())
    modules = json.loads(pathlib.Path(modules_path).read_text())
    extra = ["Modules", "Style", "Client", "Search", "Enabled", "Reset to defaults", "Keybind", "Language", "Animations",
             "Settings layout", "Sheet", "Side panel", "Menus", "Full", "Reduced", "Off", "Favorites", "Edit HUD", "Recordings",
             "Widgets", "All", "Enabled only", "Profiles", "English", "Spanish"]
    wanted = collect_terms(modules) | set(extra)
    subset = {term: translations[term] for term in sorted(wanted) if term in translations}
    pathlib.Path(output).write_text(json.dumps(subset, indent=1, ensure_ascii=False) + "\n")
    print(len(subset), "translated terms of", len(wanted))


if __name__ == "__main__":
    main(*sys.argv[1:4])
