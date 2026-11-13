from html import escape

VOID_TAGS = {"img", "input", "br", "meta", "link", "hr", "source"}


def attributes(values):
    parts = []
    for name, value in values.items():
        key = name.rstrip("_").replace("_", "-")
        if value is None or value is False:
            continue
        parts.append(f" {key}" if value is True else f' {key}="{escape(str(value), quote=True)}"')
    return "".join(parts)


def tag(element, content="", /, **values):
    opening = f"<{element}{attributes(values)}>"
    if element in VOID_TAGS:
        return opening
    return f"{opening}{content}</{element}>"


def join(parts):
    return "".join(part for part in parts if part)


def text(value):
    return escape(str(value), quote=False)
