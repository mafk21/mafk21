#!/usr/bin/env python3
"""Pick the active profile theme.

    python3 tools/profile.py                 # list themes, mark the active one
    python3 tools/profile.py 03              # switch by number
    python3 tools/profile.py paper           # switch by name
    python3 tools/profile.py --current       # print just the active name

The profile is a single animated card, so switching rewrites one `src`/`srcset`
pair in README.md. The card carries all the written content, which keeps the
README from drifting out of sync with itself.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from artlib import ORDER, PROJECTS, THEMES  # noqa: E402

CARD_RE = re.compile(r'assets/card-[\w-]+(?:\.compact)?\.svg')
ART_RE = re.compile(r'assets/[\w./-]+\.svg')
THEME_LINE_RE = re.compile(r'<!-- theme: [\w-]+ -->\n*')


def current() -> str:
    m = THEME_LINE_RE.search(README.read_text())
    if not m:
        return ORDER[0]
    # capture the name itself, not the raw match (which carries trailing newlines)
    return re.search(r'<!-- theme: ([\w-]+) -->', m.group(0)).group(1)


def render(theme: str) -> None:
    md = README.read_text()
    t = THEMES[theme]

    # Two refs per card now: desktop and the compact phone variant.
    def swap(m: re.Match) -> str:
        suffix = "-compact" if "compact" in m.group(0) else ""
        return f"assets/card-{theme}{suffix}.svg"
    md = CARD_RE.sub(swap, md)

    # One marker, always at the top, however many times this runs.
    theme_line = f"<!-- theme: {theme} -->"
    md = THEME_LINE_RE.sub("", md).lstrip("\n")
    md = f"{theme_line}\n\n{md}"

    # The note is documentation only. Whatever we write here must stay inside a
    # comment, or it renders as body copy on the profile.
    md = re.sub(
        r'<!-- theme-note: .*?-->',
        f"<!-- theme-note: {t.label} — {t.note} -->",
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
