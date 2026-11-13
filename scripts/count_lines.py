import json
import pathlib
import sys
from collections import Counter

SOURCE_SUFFIXES = {".java", ".vsh", ".fsh", ".glsl"}
SOURCE_ROOTS = ("src/main", "src/test")
THIRD_PARTY_MARKERS = ("dev/skell/client/clarity/", "assets/skellclient/clarity/")
GROUP_ANCHOR = "dev/skell/client/"
THRESHOLD_STEP = 10_000


def classify_lines(path):
    physical = blank = comment = 0
    inside_block = False
    for line in path.read_text(errors="replace").splitlines():
        physical += 1
        stripped = line.strip()
        if not stripped:
            blank += 1
        elif inside_block:
            comment += 1
            inside_block = "*/" not in stripped
        elif stripped.startswith("//"):
            comment += 1
        elif stripped.startswith("/*"):
            comment += 1
            inside_block = "*/" not in stripped
    return physical, blank, comment


def group_of(relative):
    if relative.startswith("src/test"):
        return "tests"
    if GROUP_ANCHOR in relative:
        rest = relative.split(GROUP_ANCHOR, 1)[1]
        return rest.split("/")[0] if "/" in rest else "root"
    return "shaders"


def collect(root):
    own = Counter()
    third_party = Counter()
    groups = Counter()
    files = 0
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if not path.is_file() or path.suffix not in SOURCE_SUFFIXES:
            continue
        if not relative.startswith(SOURCE_ROOTS):
            continue
        physical, blank, comment = classify_lines(path)
        code = physical - blank - comment
        if any(marker in relative for marker in THIRD_PARTY_MARKERS):
            third_party["physical"] += physical
            third_party["code"] += code
            continue
        files += 1
        own["physical"] += physical
        own["code"] += code
        groups[group_of(relative)] += physical
    return own, third_party, groups, files


def main(root, version, output):
    own, third_party, groups, files = collect(pathlib.Path(root))
    figure = own["physical"] // THRESHOLD_STEP * THRESHOLD_STEP // 1000
    report = {
        "version": version,
        "files": files,
        "ownPhysicalLines": own["physical"],
        "ownCodeLines": own["code"],
        "excludedThirdPartyPhysicalLines": third_party["physical"],
        "publishedFigure": f"{figure}k+",
        "groups": dict(groups.most_common()),
    }
    pathlib.Path(output).write_text(json.dumps(report, indent=1) + "\n")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
