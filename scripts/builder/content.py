import json
import pathlib
import re
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
CATEGORY_ORDER = ["HUD", "PvP", "Utility", "Visuals", "Cosmetics", "Client"]
CONFIGURATION_KEYS = ("name", "author", "year", "version", "minecraft", "fabricLoader", "fabricApi", "java")


def read_json(path):
    return json.loads(pathlib.Path(path).read_text())


def load_config():
    return read_json(ROOT / "site.config.json")


def load_modules():
    return read_json(CONTENT / "modules.json")


def load_stats():
    return read_json(CONTENT / "stats.json")


def load_interface(language):
    return read_json(CONTENT / language / "interface.json")


def load_landing(language):
    return read_json(CONTENT / language / "landing.json")


def load_guides(language):
    return read_json(CONTENT / language / "guides.json")


def substitute(text, config):
    return re.sub(
        r"\{\{(\w+)\}\}", lambda match: str(config[match[1]]) if match[1] in config else match[0], text
    )


def split_front_matter(source):
    if not source.startswith("---\n"):
        return {}, source
    header, _, body = source[4:].partition("\n---\n")
    values = dict(line.split(": ", 1) for line in header.splitlines() if ": " in line)
    return values, body


def load_doc(language, slug, config):
    path = CONTENT / language / "docs" / f"{slug}.md"
    values, body = split_front_matter(substitute(path.read_text(), config))
    return values, body


def slugify(value):
    folded = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", folded.lower()).strip("-")


class Translator:
    def __init__(self, language):
        path = CONTENT / language / "client-strings.json"
        self.terms = read_json(path) if path.exists() else {}

    def __call__(self, term):
        return self.terms.get(term, term)


def load_demo(language):
    return read_json(CONTENT / language / "demo.json")


def landing_values(config, modules, stats):
    count = len(modules) // 10 * 10
    return {
        **{key: config[key] for key in CONFIGURATION_KEYS},
        "modules": f"{count}+",
        "lines": stats["publishedFigure"],
    }
