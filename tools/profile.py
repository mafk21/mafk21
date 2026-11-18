#!/usr/bin/env python3
"""Pick the active profile theme.

    python3 tools/profile.py                 # list themes, mark the active one
    python3 tools/profile.py 03              # switch by number
    python3 tools/profile.py paper           # switch by name
    python3 tools/profile.py --current       # print just the active name

Switching rewrites only the art references and the theme notes in README.md.
The written content — intro, projects, principles, links — is shared by every
theme, so the profile never drifts out of sync with itself.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from artlib import ORDER, PROJECTS, THEMES  # noqa: E402

BANNER_RE = re.compile(r'<source media="\(prefers-color-scheme: dark\)" srcset="assets/[\w-]+/banner\.svg">\n\s*<img src="assets/[\w-]+/banner\.svg"')
BAND_RE = re.compile(r'<source media="\(prefers-color-scheme: dark\)" srcset="assets/[\w-]+/band\.svg">\n\s*<img src="assets/[\w-]+/band\.svg"')
GLYPH_RE = re.compile(r'src="assets/(?:[\w-]+/)?(glyph-[\w-]+)\.svg"')
THEME_LINE_RE = re.compile(r'<!-- theme: \w+ -->')


def current() -> str:
    m = THEME_LINE_RE.search(README.read_text())
    return m.group(0).split("theme: ")[1].rstrip(" ->") if m else ORDER[0]


def render(theme: str) -> None:
    md = README.read_text()
    t = THEMES[theme]

    md = BANNER_RE.sub(
        f'<source media="(prefers-color-scheme: dark)" srcset="assets/{theme}/banner.svg">\n'
        f'  <img src="assets/{theme}/banner.svg"',
        md,
    )
    md = BAND_RE.sub(
        f'<source media="(prefers-color-scheme: dark)" srcset="assets/{theme}/band.svg">\n'
        f'  <img src="assets/{theme}/band.svg"',
        md,
    )
    md = GLYPH_RE.sub(lambda m: f'src="assets/{theme}/{m.group(1)}.svg"', md)

    theme_line = f"<!-- theme: {theme} -->"
    if THEME_LINE_RE.search(md):
        md = THEME_LINE_RE.sub(theme_line, md, count=1)
    else:  # first switch: stamp it right under the banner
        md = md.replace("</picture>\n\n", f"</picture>\n\n{theme_line}\n\n", 1)

    md = re.sub(
        r'<!-- theme-note -->.*?<!-- /theme-note -->',
        f"<!-- theme-note -->{t.label} — {t.note}<!-- /theme-note -->",
        md,
        flags=re.S,
    )
    README.write_text(md)


def resolve(arg: str) -> str | None:
    arg = arg.strip().lower()
    if arg.isdigit():
        i = int(arg) - 1
        return ORDER[i] if 0 <= i < len(ORDER) else None
    return arg if arg in THEMES else None


def main() -> int:
    args = sys.argv[1:]

    if "--current" in args:
        print(current())
        return 0

    if not args:
        active = current()
        print("themes:")
        for i, key in enumerate(ORDER, 1):
            t = THEMES[key]
            mark = "● active" if key == active else "○      "
            print(f"  {i:02d}  {mark}  {t.label:11s}  {t.note}")
        print("\nswitch with:  python3 tools/profile.py 02")
        return 0

    theme = resolve(args[0])
    if not theme:
        print(f"unknown theme {args[0]!r}. options: {', '.join(ORDER)}", file=sys.stderr)
        return 2

    before = current()
    render(theme)
    print(f"active theme: {before} → {theme}")
    print("commit README.md to publish it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
