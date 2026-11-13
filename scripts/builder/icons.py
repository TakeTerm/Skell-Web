PATHS = {
    "menu": "M4 7h16M4 12h16M4 17h16",
    "close": "M6 6l12 12M18 6L6 18",
    "chevron-down": "M6 9l6 6 6-6",
    "arrow-right": "M5 12h14M13 6l6 6-6 6",
    "arrow-left": "M19 12H5M11 6l-6 6 6 6",
    "arrow-down": "M12 5v14M6 13l6 6 6-6",
    "search": "M11 4a7 7 0 100 14 7 7 0 000-14zM20 20l-4-4",
    "link": "M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1",
    "check": "M5 12.5l4.5 4.5L19 7.5",
    "external": "M14 5h5v5M19 5l-8 8M18 13v5a1 1 0 01-1 1H6a1 1 0 01-1-1V7a1 1 0 011-1h5",
    "sliders": "M4 7h9M17 7h3M4 17h3M11 17h9M13 5v4M7 15v4",
    "layout": "M4 5h16v14H4zM4 10h16M10 10v9",
    "eye": "M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12zM12 9.5a2.5 2.5 0 100 5 2.5 2.5 0 000-5z",
    "sparkles": "M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM19 16l.7 1.8L21.5 18.5l-1.8.7L19 21l-.7-1.8-1.8-.7 1.8-.7z",
    "music": "M9 18V6l10-2v12M9 18a3 3 0 11-6 0 3 3 0 016 0zM19 16a3 3 0 11-6 0 3 3 0 016 0z",
    "video": "M4 7h11v10H4zM15 11l5-3v8l-5-3",
    "box": "M12 3l8 4.5v9L12 21l-8-4.5v-9zM12 12l8-4.5M12 12L4 7.5M12 12v9",
    "grip": "M9 6h.01M15 6h.01M9 12h.01M15 12h.01M9 18h.01M15 18h.01",
    "undo": "M9 7L4 12l5 5M4 12h10a6 6 0 010 12",
    "redo": "M15 7l5 5-5 5M20 12H10a6 6 0 000 12",
    "reset": "M4 12a8 8 0 112.5 5.8M4 19v-5h5",
    "play": "M7 5l12 7-12 7z",
    "folder": "M3 7a1 1 0 011-1h5l2 2h8a1 1 0 011 1v9a1 1 0 01-1 1H4a1 1 0 01-1-1z",
    "trash": "M5 7h14M10 7V4h4v3M7 7l1 13h8l1-13M10 11v5M14 11v5",
    "info": "M12 3a9 9 0 100 18 9 9 0 000-18zM12 11v5M12 8h.01",
    "warning": "M12 4l9 16H3zM12 10v4M12 17h.01",
    "book": "M5 4h11a3 3 0 013 3v13H8a3 3 0 01-3-3zM5 17a3 3 0 013-3h11",
    "scissors": "M6 6a2.5 2.5 0 100 5 2.5 2.5 0 000-5zM6 13a2.5 2.5 0 100 5 2.5 2.5 0 000-5zM8 10l12 8M8 14L20 6",
    "target": "M12 3a9 9 0 100 18 9 9 0 000-18zM12 8a4 4 0 100 8 4 4 0 000-8zM12 12h.01",
    "wrench": "M14.5 6.5a4 4 0 005 5l-9 9a2.1 2.1 0 01-3-3l9-9a4 4 0 00-2-2z",
    "hud": "M4 5h16v14H4zM7 8h4M7 11h3M15 15h2",
    "bolt": "M13 3L5 13h6l-1 8 8-10h-6z",
}


def icon(name, size=20, class_name="icon"):
    path = PATHS[name]
    return (
        f'<svg class="{class_name}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true" focusable="false"><path d="{path}"/></svg>'
    )
