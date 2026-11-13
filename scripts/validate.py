import ast
import html.parser
import io
import json
import pathlib
import re
import sys
import tokenize

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
LANGUAGES = ("en", "es")
HEADING_ID = re.compile(r"^#{1,6}\s.*\{#([\w-]+)\}\s*$", re.MULTILINE)
HEADING_LINE = re.compile(r"^(#{1,6})\s", re.MULTILINE)
DIRECTIVE = re.compile(r"^:::(\w+)", re.MULTILINE)


def flatten(value, prefix=""):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from flatten(child, f"{prefix}.{key}" if prefix else key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from flatten(child, f"{prefix}[{index}]")
    else:
        yield prefix


def check_json_parity():
    problems = []
    for path in sorted((ROOT / "content" / "en").glob("*.json")):
        counterpart = ROOT / "content" / "es" / path.name
        if not counterpart.exists():
            problems.append(f"missing Spanish file {path.name}")
            continue
        english = set(flatten(json.loads(path.read_text())))
        spanish = set(flatten(json.loads(counterpart.read_text())))
        for key in sorted(english - spanish):
            problems.append(f"{path.name}: {key} missing in es")
        for key in sorted(spanish - english):
            problems.append(f"{path.name}: {key} missing in en")
    return problems


def check_doc_parity():
    problems = []
    english_dir = ROOT / "content" / "en" / "docs"
    spanish_dir = ROOT / "content" / "es" / "docs"
    for path in sorted(english_dir.glob("*.md")):
        counterpart = spanish_dir / path.name
        if not counterpart.exists():
            problems.append(f"missing Spanish doc {path.name}")
            continue
        english, spanish = path.read_text(), counterpart.read_text()
        if HEADING_ID.findall(english) != HEADING_ID.findall(spanish):
            problems.append(f"{path.name}: heading ids differ")
        if [m.group(1) for m in HEADING_LINE.finditer(english)] != [m.group(1) for m in HEADING_LINE.finditer(spanish)]:
            problems.append(f"{path.name}: heading levels differ")
        if DIRECTIVE.findall(english) != DIRECTIVE.findall(spanish):
            problems.append(f"{path.name}: directive sequence differs")
    return problems


class PageIndex(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.append(attributes["id"])
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes["href"])


def resolve_target(source, href):
    path, _, fragment = href.partition("#")
    if not path:
        return source, fragment
    target = (SITE / path.lstrip("/")) if path.startswith("/") else (source.parent / path)
    target = target.resolve()
    if target.is_dir():
        target = target / "index.html"
    return target, fragment


def check_site():
    problems = []
    index = {}
    for page in sorted(SITE.rglob("*.html")):
        parser = PageIndex()
        parser.feed(page.read_text())
        index[page.resolve()] = parser
        duplicated = {identifier for identifier in parser.ids if parser.ids.count(identifier) > 1}
        for identifier in sorted(duplicated):
            problems.append(f"{page.relative_to(SITE)}: duplicate id {identifier}")
    for page, parser in index.items():
        for href in parser.links:
            if href.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            target, fragment = resolve_target(page, href)
            if not target.exists():
                problems.append(f"{page.relative_to(SITE)}: broken link {href}")
            elif fragment and target in index and fragment not in index[target].ids:
                problems.append(f"{page.relative_to(SITE)}: missing anchor {href}")
    return problems


def python_comments(path):
    source = path.read_text()
    found = []
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.COMMENT and not token.string.startswith("#!"):
            found.append(token.start[0])
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            if ast.get_docstring(node, clean=False) is not None:
                found.append(node.body[0].lineno)
    return found


def script_comments(path):
    text = path.read_text()
    found = []
    index, line, quote = 0, 1, None
    while index < len(text):
        char = text[index]
        pair = text[index : index + 2]
        if char == "\n":
            line += 1
        if quote:
            if char == "\\":
                index += 1
            elif char == quote:
                quote = None
        elif char in "\"'`":
            quote = char
        elif pair == "//" and text[index - 1 : index] != ":":
            found.append(line)
            index = text.find("\n", index) - 1
            if index < 0:
                break
        elif pair == "/*":
            found.append(line)
            end = text.find("*/", index)
            line += text.count("\n", index, end)
            index = end + 1
        index += 1
    return found


def stylesheet_comments(path):
    text = path.read_text()
    return [text.count("\n", 0, match.start()) + 1 for match in re.finditer(r"/\*", text)]


def check_comments():
    problems = []
    scanners = (
        (ROOT / "scripts", "*.py", python_comments),
        (ROOT / "src" / "scripts", "*.js", script_comments),
        (ROOT / "src" / "styles", "*.css", stylesheet_comments),
    )
    for directory, pattern, scanner in scanners:
        for path in sorted(directory.rglob(pattern)):
            for line in scanner(path):
                problems.append(f"{path.relative_to(ROOT)}:{line}: comment")
    return problems


def main():
    checks = {
        "json parity": check_json_parity,
        "doc parity": check_doc_parity,
        "built site": check_site,
        "comments": check_comments,
    }
    failed = False
    for name, check in checks.items():
        problems = check()
        print(f"{name}: {'ok' if not problems else len(problems)}")
        for problem in problems:
            print(f"  {problem}")
        failed = failed or bool(problems)
    sys.exit(1 if failed else 0)


main()
