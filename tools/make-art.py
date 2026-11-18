#!/usr/bin/env python3
"""Generate every piece of art used by the profile README.

Design language (shared with the masthead):
  hairline strokes, wide-tracked small caps, serif names, monochrome ink,
  a ruler line, and motion only where it means something.

    python3 tools/make-art.py

Writes:
  assets/banner-{light,dark}.svg   masthead + live node graph
  assets/loop-{light,dark}.svg     "how a build runs" schematic
  assets/glyph-*.svg               six project schematics (theme-neutral)

Everything is vector, hand-drawn from primitives, and animates with SMIL so it
works inside GitHub's `<img>` sandbox (no scripts, no external CSS).
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

INK = {"light": "#1c1c1c", "dark": "#e9e7e1"}
NEUTRAL = "#8a8a8a"  # glyphs sit in a table, so one file must read on both themes

SERIF = "Georgia, 'Iowan Old Style', 'Times New Roman', serif"
SANS = "-apple-system, 'Helvetica Neue', Helvetica, Arial, sans-serif"

NAME = "Dr. Abo 3tab"
EYEBROW = "LOCAL-FIRST AI  ·  AUTONOMOUS AGENTS  ·  TOOLS THAT SHIP AS FILES"


# ── primitives ────────────────────────────────────────────────────────────────


def head(w: int, h: int, label: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
    )


def ruler(w: int, y: int, step: int = 64, length: int = 7) -> str:
    """A measured line: ticks hanging below y, fading toward the right."""
    out = [f'<path d="M0 {y} H{w}" opacity="0.34"/>']
    x, i = 0, 0
    while x <= w:
        ln = length + 5 if i % 4 == 0 else length
        op = max(0.10, 0.30 - i * 0.012)
        out.append(f'<path d="M{x} {y} V{y + ln}" opacity="{op:.2f}"/>')
        x += step
        i += 1
    return "\n    ".join(out)


def caps(x: int, y: int, text: str, ink: str, size: int = 13, op: float = 0.62,
         anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{ink}" fill-opacity="{op}" '
        f'font-family="{SANS}" font-size="{size}" letter-spacing="4.6" '
        f'font-weight="500">{text}</text>'
    )


def travel(path: str, dur: float, begin: float, ink: str, r: float = 2.2) -> str:
    """A dot that runs a route and fades at both ends."""
    return (
        f'<circle cx="0" cy="0" r="{r}" fill="{ink}" opacity="0">\n'
        f'      <animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" '
        f'path="{path}" calcMode="spline" keyPoints="0;1" keyTimes="0;1" '
        f'keySplines="0.4 0 0.6 1"/>\n'
        f'      <animate attributeName="opacity" dur="{dur}s" begin="{begin}s" '
        f'repeatCount="indefinite" values="0;0.85;0.85;0" keyTimes="0;0.12;0.86;1"/>\n'
        f'    </circle>'
    )


# ── 1. masthead ───────────────────────────────────────────────────────────────


def banner(ink: str) -> str:
    W, H = 1280, 188
    cx, cy = 1128, 104
    ring = [(cx - 96, cy - 38), (cx + 92, cy - 28), (cx - 78, cy + 52),
            (cx + 74, cy + 56), (cx - 128, cy + 8)]
    leaves = [(cx - 120, cy - 78), (cx + 136, cy + 6)]
    edges = [((cx, cy), p) for p in ring] + [(ring[0], leaves[0]), (ring[1], leaves[1])]

    lines = "\n      ".join(
        f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" opacity="0.38" stroke-width="1"/>'
        for a, b in edges
    )
    dots = "\n      ".join(
        f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" opacity="{o}"/>'
        for p, r, o in [(p, 3.0, 0.95) for p in ring] + [(p, 2.2, 0.72) for p in leaves]
    )
    # Packets run hub→leaf and leaf→hub, so the graph reads as traffic, not decoration.
    packets = "\n      ".join(
        travel(f"M{e[0][0]} {e[0][1]} L{e[1][0]} {e[1][1]}", 3.6, 0.35 * i, ink)
        for i, e in enumerate(edges[:5])
    )

    return f"""{head(W, H, f"{NAME} — local-first AI systems, autonomous agents, and tools that run on your own machine")}
  <g stroke="{ink}" fill="none">
    {ruler(W, 34)}
    <path d="M0 176 H{W}" opacity="0.34"/>
  </g>

  {caps(4, 86, EYEBROW, ink)}

  <text x="2" y="150" fill="{ink}" font-family="{SERIF}" font-size="66"
        letter-spacing="0.5">{NAME}</text>

  <g stroke="{ink}" fill="{ink}">
      {lines}
      <circle cx="{cx}" cy="{cy}" r="5" opacity="1"/>
      {dots}
      {packets}
      <circle cx="{cx}" cy="{cy}" r="8" fill="none" opacity="0.5">
        <animate attributeName="r" values="7;20" dur="3.4s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.45;0" dur="3.4s" repeatCount="indefinite"/>
      </circle>
  </g>
</svg>
"""


# ── 2. "how a build runs" ─────────────────────────────────────────────────────


def station_icon(kind: str, x: int, y: int, ink: str) -> str:
    """Hairline pictograms, drawn around a 64×64 box centred on (x, y)."""
    s = f'stroke="{ink}" fill="none" stroke-width="1.4" stroke-linecap="round"'
    if kind == "brief":  # a page with lines and a live caret
        return f"""<g {s}>
        <rect x="{x-20}" y="{y-26}" width="40" height="52" rx="2"/>
        <path d="M{x-11} {y-14} H{x+3}"/><path d="M{x-11} {y-3} H{x+9}"/>
        <path d="M{x-11} {y+8} H{x-2}"/><path d="M{x-11} {y+19} H{x+6}" opacity="0.45"/>
        <path d="M{x+7} {y+4} V{y+13}" stroke-width="2">
          <animate attributeName="opacity" values="1;0;1" dur="1.15s" repeatCount="indefinite"/>
        </path>
      </g>"""
    if kind == "agents":  # three cursors landing on a target
        c = []
        for i, (dx, dy) in enumerate([(-16, -18), (0, 6), (16, -16)]):
            c.append(f"""<path d="M{x+dx} {y+dy} l0 12 l3.4 -3.2 l2.4 5.4 l3.2 -1.5 l-2.5 -5.3 l4.6 -0.4 z"
          fill="{ink}" stroke="none" opacity="0.85">
          <animateTransform attributeName="transform" type="translate"
            values="0 -5;0 0;0 -5" dur="{2.4 + i * 0.5}s" repeatCount="indefinite"/>
        </path>""")
        return (f'<g {s}><rect x="{x-9}" y="{y+13}" width="18" height="13" rx="1.5" opacity="0.5"/>'
                + "".join(c) + "</g>")
    if kind == "runtime":  # nested processor with pins
        pins = "".join(
            f'<path d="M{x-26} {y+o} h6"/><path d="M{x+20} {y+o} h6"/>' for o in (-14, 0, 14)
        )
        return f"""<g {s}>
        <rect x="{x-20}" y="{y-20}" width="40" height="40" rx="2"/>
        <rect x="{x-11}" y="{y-11}" width="22" height="22" rx="1" opacity="0.55"/>
        <path d="M{x-4} {y} h8 M{x} {y-4} v8" opacity="0.75">{""}
          <animate attributeName="opacity" values="0.75;0.2;0.75" dur="2.2s" repeatCount="indefinite"/>
        </path>
        {pins}
      </g>"""
    # a file you keep: page, folded corner, check
    return f"""<g {s}>
      <path d="M{x-19} {y-26} H{x+7} L{x+19} {y-14} V{y+26} H{x-19} Z"/>
      <path d="M{x+7} {y-26} V{y-14} H{x+19}" opacity="0.55"/>
      <path d="M{x-10} {y+4} l7 8 l14 -16" stroke-width="1.8">
        <animate attributeName="stroke-dasharray" values="0 40;34 40;34 40;0 40"
          keyTimes="0;0.45;0.75;1" dur="4.2s" repeatCount="indefinite"/>
      </path>
    </g>"""


def loop(ink: str) -> str:
    W, H = 1280, 312
    cy = 156
    stations = [
        (140, "brief", "BRIEF", "you type it"),
        (470, "agents", "AGENTS", "they build it"),
        (800, "runtime", "RUNTIME", "local, yours"),
        (1130, "file", "FILE", "you keep it"),
    ]

    icons = "\n    ".join(station_icon(k, x, cy, ink) for x, k, _, _ in stations)

    labels = "\n    ".join(
        caps(x, cy + 72, name, ink, size=12, op=0.9, anchor="middle")
        + "\n    " + caps(x, cy + 92, gloss, ink, size=11, op=0.42, anchor="middle")
        for x, _, name, gloss in stations
    )

    # Dashed routes flow left-to-right; a packet rides each one a beat later.
    routes, packets = [], []
    for (x1, *_), (x2, *_) in zip(stations, stations[1:]):
        a, b = x1 + 30, x2 - 30
        d = f"M{a} {cy} L{b} {cy}"
        routes.append(
            f'<path d="{d}" opacity="0.38" stroke-dasharray="2 7" stroke-width="1.2">'
            f'<animate attributeName="stroke-dashoffset" values="0;-18" dur="1.5s" '
            f'repeatCount="indefinite"/></path>'
        )
    for i, ((x1, *_), (x2, *_)) in enumerate(zip(stations, stations[1:])):
        packets.append(travel(f"M{x1+30} {cy} L{x2-30} {cy}", 3.0, 0.5 + i * 0.75, ink, 2.6))

    return f"""{head(W, H, "How a build runs: you write a brief, agents build, it runs locally, you keep the file")}
  <g stroke="{ink}" fill="none">
    {ruler(W, 34)}
  </g>

  {caps(4, 86, "HOW A BUILD RUNS", ink)}

  <g fill="{ink}">
    {icons}
  </g>

  <g stroke="{ink}" fill="none">
    {"".join(routes)}
  </g>
  <g fill="{ink}">
    {packets}
  </g>

  {labels}

  <g stroke="{ink}" fill="none" opacity="0.32">
    <path d="M110 270 V278 H1174 V270"/>
  </g>
  {caps(635, 300, "ONE MACHINE · NOTHING LEAVES IT", ink, size=11, op=0.5, anchor="middle")}
</svg>
"""


# ── 3. project glyphs ─────────────────────────────────────────────────────────


def glyph(kind: str) -> str:
    """132×64 schematics. One neutral file that reads on light and dark."""
    W, H = 132, 64
    cx, cy = W / 2, H / 2
    ink = NEUTRAL
    s = f'stroke="{ink}" fill="none" stroke-width="1.3" stroke-linecap="round"'
    body = ""

    if kind == "jarvis":  # a head that listens, plus a wave
        bars = "".join(
            f'<path d="M{x} {cy - h/2} V{cy + h/2}"><animate attributeName="d" '
            f'values="M{x} {cy-h/2} V{cy+h/2};M{x} {cy-h} V{cy+h};M{x} {cy-h/2} V{cy+h/2}" '
            f'dur="{1.2 + i*0.18}s" repeatCount="indefinite"/></path>'
            for i, (x, h) in enumerate([(24, 14), (33, 22), (42, 10)])
        )
        body = f'<g {s}>{bars}</g><g {s}><circle cx="72" cy="{cy}" r="15"/><circle cx="72" cy="{cy}" r="24" opacity="0.4"/></g>'
        body += (f'<circle cx="72" cy="{cy}" r="4" fill="{ink}" stroke="none"/>')
        body += (f'<circle cx="96" cy="{cy-9}" r="2.2" fill="{ink}" stroke="none" opacity="0.7">'
                 f'<animateMotion dur="4s" repeatCount="indefinite" path="M0 0 a14 14 0 1 1 -0.1 0"/></circle>')

    elif kind == "swarmcraft":  # a page being drawn by cursors
        cur = "".join(
            f'<path d="M{x} {y} l0 9 l2.6 -2.4 l1.9 4.1 l2.4 -1.1 l-1.9 -4 l3.5 -0.3 z" '
            f'fill="{ink}" stroke="none"><animateTransform attributeName="transform" '
            f'type="translate" values="0 -3;0 0;0 -3" dur="{2 + i*0.45}s" repeatCount="indefinite"/>'
            f'</path>'
            for i, (x, y) in enumerate([(46, 16), (70, 30), (58, 44)])
        )
        body = (f'<g {s}><rect x="30" y="10" width="72" height="44" rx="2" opacity="0.85"/>'
                f'<path d="M38 22 H66" opacity="0.55"/><path d="M38 31 H84" opacity="0.3"/>'
                f'<path d="M38 40 H74" opacity="0.3"/></g>{cur}')

    elif kind == "osint":  # linked evidence, tightening inward
        body = (
            f'<g {s}><circle cx="{cx}" cy="{cy}" r="26" opacity="0.28"/>'
            f'<circle cx="{cx}" cy="{cy}" r="17" opacity="0.36"/>'
            f'<path d="M{cx} {cy-17} L{cx+24} {cy+6} L{cx-24} {cy+10} Z" opacity="0.45"/>'
            f'<path d="M{cx} {cy-26} V{cy+26}" opacity="0.18"/></g>'
            f'<g fill="{ink}" stroke="none">'
            f'<circle cx="{cx}" cy="{cy-17}" r="2.6"/><circle cx="{cx+24}" cy="{cy+6}" r="2.6"/>'
            f'<circle cx="{cx-24}" cy="{cy+10}" r="2.6"/><circle cx="{cx}" cy="{cy}" r="3.4"/></g>'
        )

    elif kind == "nexus":  # stacked desktops, the front one lifting on a loop
        body = (
            f'<g {s}><rect x="28" y="32" width="54" height="22" rx="2" opacity="0.28"/>'
            f'<rect x="37" y="23" width="54" height="22" rx="2" opacity="0.5"/>'
            f'<g><animateTransform attributeName="transform" type="translate" '
            f'values="0 2;0 -2;0 2" dur="4.6s" repeatCount="indefinite"/>'
            f'<rect x="46" y="12" width="54" height="22" rx="2"/>'
            f'<path d="M46 18 H100" opacity="0.45"/>'
            f'<circle cx="52" cy="15" r="1.4" fill="{ink}" stroke="none" opacity="0.7"/>'
            f'<path d="M54 27 H78" opacity="0.55"/><path d="M54 31 H70" opacity="0.3"/>'
            f'</g></g>'
        )

    elif kind == "connect":  # a curated grid, one thing singled out
        dots = []
        for r in range(3):
            for c in range(5):
                x, y = 34 + c * 16, 20 + r * 12
                sel = (r, c) == (1, 2)
                dots.append(
                    f'<circle cx="{x}" cy="{y}" r="{3 if sel else 1.7}" opacity="{1 if sel else 0.45}"/>'
                )
        body = (f'<g fill="{ink}" stroke="none">{"".join(dots)}'
                f'<circle cx="66" cy="32" r="7" fill="none" stroke="{ink}" stroke-width="1.1" opacity="0.7">'
                f'<animate attributeName="r" values="6;10" dur="2.6s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0.7;0" dur="2.6s" repeatCount="indefinite"/>'
                f'</circle></g>')

    else:  # powerpoint: one slide morphs into the next
        body = (
            f'<g {s}><rect x="20" y="20" width="38" height="26" rx="2" opacity="0.5"/>'
            f'<rect x="74" y="20" width="38" height="26" rx="2"/>'
            f'<path d="M40 36 H72" opacity="0.5" stroke-dasharray="2 4"/></g>'
            f'<path d="M66 30 l6 6 l-6 6" {s}><animate attributeName="opacity" '
            f'values="1;0.25;1" dur="2.2s" repeatCount="indefinite"/></path>'
        )

    return f"""{head(W, H, f"{kind} project schematic")}
  {body}
</svg>
"""


GLYPHS = {
    "jarvis": "jarvis",
    "swarmcraft": "swarmcraft",
    "osint": "osint",
    "nexus": "nexus",
    "connect": "connect",
    "powerpoint": "ppt",
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    written = []

    for theme, ink in INK.items():
        for name, builder in (("banner", banner), ("loop", loop)):
            path = OUT / f"{name}-{theme}.svg"
            path.write_text(builder(ink), encoding="utf-8")
            written.append(path)

    for name, kind in GLYPHS.items():
        path = OUT / f"glyph-{name}.svg"
        path.write_text(glyph(kind), encoding="utf-8")
        written.append(path)

    for p in sorted(written):
        print(f"{p.relative_to(OUT.parent)}  {p.stat().st_size:,} B")


if __name__ == "__main__":
    main()
