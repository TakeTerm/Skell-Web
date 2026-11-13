import re

from .icons import icon
from .markup import join, tag, text

HEADING = re.compile(r"^(#{2,4}) (.+?)(?: \{#([\w-]+)\})?$")
DIRECTIVE = re.compile(r"^:::(\w+)(?: (.*))?$")
LIST_ITEM = re.compile(r"^(?:[-*]|\d+\.) (.*)$")
TABLE_SEPARATOR = re.compile(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?$")
CALLOUT_ICONS = {"note": "info", "tip": "sparkles", "warn": "warning", "soon": "bolt"}


class Renderer:
    def __init__(self, language, resolve_link, figures, slug_prefix=""):
        self.language = language
        self.resolve_link = resolve_link
        self.figures = figures
        self.slug_prefix = slug_prefix
        self.headings = []
        self.faq_total = 0

    def inline(self, source):
        codes = []

        def stash(match):
            codes.append(tag("code", text(match[1])))
            return f"\x00{len(codes) - 1}\x00"

        value = re.sub(r"`([^`]+)`", stash, source)
        value = text(value)
        value = re.sub(r"\[\[([^\]]+)\]\]", lambda m: tag("kbd", m[1]), value)
        value = re.sub(r"\*\*(.+?)\*\*", lambda m: tag("strong", m[1]), value)
        value = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", lambda m: tag("em", m[1]), value)
        value = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", self.link, value)
        return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m[1])], value)

    def link(self, match):
        label, target = match.groups()
        href = self.resolve_link(target)
        if href.startswith("http"):
            return tag("a", label + icon("external", 14, "icon icon--inline"), href=href, rel="noopener noreferrer", target="_blank")
        return tag("a", label, href=href)

    def heading(self, level, title, anchor):
        anchor = anchor or re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        self.headings.append((level, title, anchor))
        link = tag("a", icon("link", 16), class_="anchor", href=f"#{anchor}", aria_label=title)
        return tag(f"h{level}", self.inline(title) + link, id=anchor)

    def table(self, rows):
        cells = [[cell.strip() for cell in row.strip().strip("|").split("|")] for row in rows]
        header = join(tag("th", self.inline(cell)) for cell in cells[0])
        body = join(
            tag("tr", join(tag("td", self.inline(cell)) for cell in row)) for row in cells[2:]
        )
        table = tag("table", tag("thead", tag("tr", header)) + tag("tbody", body))
        return tag("div", table, class_="table-wrap")

    def items(self, lines, ordered):
        entries = [tag("li", self.inline(line)) for line in lines]
        return tag("ol" if ordered else "ul", join(entries))

    def callout(self, kind, title, lines):
        body = self.blocks(lines)
        heading = tag("p", self.inline(title), class_="callout__title") if title else ""
        icon_html = tag("span", icon(CALLOUT_ICONS[kind], 20), class_="callout__icon")
        return tag("aside", icon_html + tag("div", heading + body), class_=f"callout callout--{kind}")

    def faq(self, lines):
        entries, question, answer = [], None, []
        for line in lines + ["### "]:
            if line.startswith("### "):
                if question:
                    entries.append((question, answer))
                question, answer = line[4:], []
            else:
                answer.append(line)
        items = []
        for question, answer in entries:
            identifier = f"faq-{self.slug_prefix}{self.faq_total}"
            self.faq_total += 1
            button = tag(
                "button",
                tag("span", self.inline(question)) + icon("chevron-down", 20),
                type="button",
                class_="faq__question",
                id=f"{identifier}-button",
                aria_expanded="false",
                aria_controls=identifier,
            )
            panel = tag(
                "div",
                tag("div", self.blocks(answer), class_="faq__answer"),
                class_="faq__panel",
                id=identifier,
                role="region",
                aria_labelledby=f"{identifier}-button",
            )
            items.append(tag("div", tag("h3", button) + panel, class_="faq__item"))
        return tag("div", join(items), class_="faq", data_faq=True)

    def steps(self, lines):
        entries = [LIST_ITEM.match(line)[1] for line in lines if LIST_ITEM.match(line)]
        items = [
            tag("li", tag("span", str(index), class_="steps__number") + tag("div", self.inline(entry)))
            for index, entry in enumerate(entries, 1)
        ]
        return tag("ol", join(items), class_="steps")

    def figure(self, name, lines):
        caption = " ".join(line for line in lines if line).strip()
        figure = self.figures[name]()
        caption_html = tag("figcaption", self.inline(caption)) if caption else ""
        return tag("figure", figure + caption_html, class_="figure")

    def directive(self, name, argument, lines):
        if name in CALLOUT_ICONS:
            return self.callout(name, argument, lines)
        if name == "faq":
            return self.faq(lines)
        if name == "steps":
            return self.steps(lines)
        if name == "figure":
            return self.figure(argument, lines)
        if name == "marker":
            return tag("div", "", data_marker=argument)
        raise ValueError(f"Unknown directive {name}")

    def blocks(self, lines):
        output, index = [], 0
        while index < len(lines):
            line = lines[index]
            if not line.strip():
                index += 1
                continue
            directive = DIRECTIVE.match(line)
            if directive:
                end = next(i for i in range(index + 1, len(lines)) if lines[i] == ":::")
                output.append(self.directive(directive[1], directive[2], lines[index + 1 : end]))
                index = end + 1
                continue
            if line.startswith("```"):
                end = next(i for i in range(index + 1, len(lines)) if lines[i].startswith("```"))
                code = "\n".join(lines[index + 1 : end])
                output.append(tag("pre", tag("code", text(code))))
                index = end + 1
                continue
            heading = HEADING.match(line)
            if heading:
                output.append(self.heading(len(heading[1]), heading[2], heading[3]))
                index += 1
                continue
            if line.startswith("|"):
                end = index
                while end < len(lines) and lines[end].startswith("|"):
                    end += 1
                output.append(self.table(lines[index:end]))
                index = end
                continue
            if LIST_ITEM.match(line):
                ordered = bool(re.match(r"^\d+\.", line))
                entries = []
                while index < len(lines) and (LIST_ITEM.match(lines[index]) or lines[index].startswith("  ")):
                    match = LIST_ITEM.match(lines[index])
                    if match:
                        entries.append(match[1])
                    else:
                        entries[-1] += " " + lines[index].strip()
                    index += 1
                output.append(self.items(entries, ordered))
                continue
            paragraph = [line]
            index += 1
            while index < len(lines) and lines[index].strip() and not self.starts_block(lines[index]):
                paragraph.append(lines[index])
                index += 1
            output.append(tag("p", self.inline(" ".join(paragraph))))
        return join(output)

    @staticmethod
    def starts_block(line):
        return bool(
            HEADING.match(line) or DIRECTIVE.match(line) or LIST_ITEM.match(line) or line.startswith(("|", "```"))
        )

    def render(self, source):
        return self.blocks(source.splitlines())
