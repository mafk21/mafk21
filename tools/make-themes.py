#!/usr/bin/env python3
"""Generate all four profile themes.

    python3 tools/make-themes.py

Writes assets/<theme>/{banner,band,glyph-*}.svg for each theme in artlib.ORDER.

Each theme is a complete, self-contained look with its own background, type and
motion, so the profile reads identically on GitHub light and dark.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from artlib import (  # noqa: E402
    KICKER, MONO, NAME, ORDER, PROJECTS, REDUCED, SANS, SERIF, STATIONS, THEMES,
    Theme, caps, card, head, rise, ticks, travel,
)

OUT = Path(__file__).resolve().parent.parent / "assets"


# ══════════════════════════════════════════════════════════════════════════════
# banners — 1280 × 188
# ══════════════════════════════════════════════════════════════════════════════


def banner_typewriter(t: Theme) -> str:
    W, H = 1280, 188
    typed = "Dr. Abo 3tab"
    css = f"""
    @keyframes caret {{ 0%,49% {{ opacity: 1; }} 50%,100% {{ opacity: 0; }} }}
    @keyframes scan  {{ 0% {{ transform: translateY(0); }} 100% {{ transform: translateY(188px); }} }}
    .caret {{ animation: caret 1.05s step-end infinite; }}
    .scan  {{ animation: scan 7s linear infinite; }}
    {rise("rise1", 1.6)}
    {rise("rise2", 1.9)}
    {rise("rise3", 2.2)}
    {REDUCED}"""

    # A block caret parked one character past the name; width is an estimate of
    # the string at 58px monospace (0.6em advance).
    caret_x = 40 + round(len(typed) * 50 * 0.6) + 10

    return f"""{head(t, W, H, f"{NAME} — local-first AI systems, autonomous agents, tools that run on your own machine")}
  <style>{css}
  </style>
  {card(t, W, H)}
  <g stroke="{t.ink}" fill="none" opacity="0.5">
    <path d="M0 34 H{W}" opacity="0.18"/>
    {ticks(34, W, 64, t.ink)}
  </g>

  <rect x="24" y="14" width="1232" height="164" rx="8" fill="none" stroke="{t.ink}" stroke-opacity="0.16"/>
  <g fill="{t.ink}" fill-opacity="0.35">
    <circle cx="44" cy="30" r="3.2"/><circle cx="58" cy="30" r="3.2"/><circle cx="72" cy="30" r="3.2"/>
  </g>
  {caps(t, 700, 34, "MAFK21 · PROFILE", size=11, op=0.3, cls="rise3")}

  <text x="40" y="92" fill="{t.accent}" font-family="{MONO}" font-size="15" opacity="0.9"
        class="rise1">~/profile $ whoami</text>

  <text x="40" y="144" fill="{t.ink}" font-family="{MONO}" font-size="50"
        letter-spacing="1">{typed}</text>
  <rect class="caret" x="{caret_x}" y="112" width="20" height="38" fill="{t.accent}" opacity="0.85"/>

  {caps(t, 40, 166, KICKER, size=10, op=0.40, cls="rise2", track=3.6)}

  <rect class="scan" x="24" y="16" width="1232" height="2" fill="{t.accent}" opacity="0.10"/>
</svg>
"""


def banner_blueprint(t: Theme) -> str:
    W, H = 1280, 188
    css = f"""
    @keyframes drawL {{ from {{ stroke-dashoffset: 1300; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes drawS {{ from {{ stroke-dashoffset: 560; }} to {{ stroke-dashoffset: 0; }} }}
    .r1 {{ stroke-dasharray: 1300; animation: drawL 1.1s .1s ease-out both; }}
    .r2 {{ stroke-dasharray: 1300; animation: drawL 1.1s .35s ease-out both; }}
    .r3 {{ stroke-dasharray: 560;  animation: drawS 1.4s .5s ease-out both; }}
    {rise("rise1", 0.9)}
    {rise("rise2", 1.2)}
    {rise("rise3", 1.5)}
    {REDUCED}"""

    grid = "".join(
        f'<path d="M{x} 0 V{H}" opacity="0.055"/>' for x in range(0, W + 1, 32)
    ) + "".join(f'<path d="M0 {y} H{W}" opacity="0.055"/>' for y in range(0, H + 1, 32))

    # dimension marks, like a measured sheet
    dims = ""
    for x0, x1, y in ((700, 1080, 96), (700, 1080, 168)):
        dims += (
            f'<path class="r3" d="M{x0} {y} H{x1}" opacity="0.45"/>'
            f'<path d="M{x0} {y-5} V{y+5}" opacity="0.5"/>'
            f'<path d="M{x1} {y-5} V{y+5}" opacity="0.5"/>'
        )

    return f"""{head(t, W, H, f"{NAME} — blueprint of a local-first AI practice")}
  <style>{css}
  </style>
  {card(t, W, H, rx=0)}
  <g stroke="{t.ink}" fill="none">{grid}</g>

  <g stroke="{t.accent}" fill="none" stroke-width="1.2">
    <path class="r1" d="M0 34 H{W}" opacity="0.85"/>
    <path class="r2" d="M0 176 H{W}" opacity="0.6"/>
    {dims}
  </g>

  {caps(t, 40, 74, "SHEET 01 · PROFILE", size=11, op=0.55, cls="rise1", fill=t.accent)}
  <text x="40" y="132" fill="{t.ink}" font-family="{SANS}" font-size="54" font-weight="600"
        letter-spacing="-0.5" class="rise2">{NAME}</text>
  {caps(t, 40, 158, KICKER, size=10, op=0.5, cls="rise3", track=3.6)}

  <g class="rise3" stroke="{t.accent}" fill="none" opacity="0.75">
    <circle cx="1214" cy="70" r="20"/>
    <path d="M1214 50 V90 M1194 70 H1234"/>
  </g>
</svg>
"""


def banner_paper(t: Theme) -> str:
    W, H = 1280, 188
    css = f"""
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes stamp {{ 0% {{ opacity: 0; transform: rotate(-8deg) scale(1.35); }}
                       60% {{ opacity: .9; transform: rotate(-8deg) scale(.96); }}
                       100% {{ opacity: .85; transform: rotate(-8deg) scale(1); }} }}
    .name  {{ animation: rise .8s .2s cubic-bezier(.2,.7,.3,1) both; }}
    .kmid  {{ animation: rise .8s .5s cubic-bezier(.2,.7,.3,1) both; }}
    .stamp {{ animation: stamp .9s 1.1s cubic-bezier(.2,.7,.3,1) both;
              transform-origin: 1130px 118px; }}
    {REDUCED}"""

    return f"""{head(t, W, H, f"{NAME} — local-first AI, written and drawn by hand")}
  <style>{css}
  </style>
  {card(t, W, H, rx=0)}
  <g stroke="{t.ink}" fill="none">
    {ticks(34, W, 64, t.ink, length=8)}
    <path d="M0 176 H{W}" opacity="0.28"/>
  </g>

  {caps(t, 40, 74, "A SMALL PRACTICE IN LOCAL MACHINES", size=11, op=0.55, cls="kmid", track=4.2)}

  <text class="name" x="38" y="146" fill="{t.ink}" font-family="{SERIF}" font-size="66"
        letter-spacing="0.4">{NAME}</text>

  <g class="stamp" opacity="0.85">
    <rect x="1046" y="86" width="168" height="64" rx="3" fill="none"
          stroke="{t.accent}" stroke-width="2"/>
    <rect x="1052" y="92" width="156" height="52" rx="2" fill="none"
          stroke="{t.accent}" stroke-width="0.8" opacity="0.7"/>
    {caps(t, 1130, 114, "APPROVED", size=13, op=1, anchor="middle", fill=t.accent, track=3)}
    {caps(t, 1130, 132, "LOCAL ONLY", size=9, op=0.9, anchor="middle", fill=t.accent, track=2.4)}
  </g>
</svg>
"""


def banner_swarm(t: Theme) -> str:
    W, H = 1280, 188
    cx, cy = 1128, 104
    ring = [(cx - 96, cy - 38), (cx + 92, cy - 28), (cx - 78, cy + 52),
            (cx + 74, cy + 56), (cx - 128, cy + 8)]
    leaves = [(cx - 120, cy - 78), (cx + 136, cy + 6)]
    edges = [((cx, cy), p) for p in ring] + [(ring[0], leaves[0]), (ring[1], leaves[1])]

    css = f"""
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes pulse {{ 0% {{ r: 7; opacity: .5; }} 100% {{ r: 20; opacity: 0; }} }}
    .name {{ animation: rise .8s .2s cubic-bezier(.2,.7,.3,1) both; }}
    .kick {{ animation: rise .8s .5s cubic-bezier(.2,.7,.3,1) both; }}
    .pulse {{ animation: pulse 3.4s ease-out infinite; }}
    {REDUCED}"""

    lines = "\n      ".join(
        f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" opacity="0.38" stroke-width="1"/>'
        for a, b in edges
    )
    dots = "\n      ".join(
        f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" opacity="{o}"/>'
        for p, r, o in [(p, 3.0, 0.95) for p in ring] + [(p, 2.2, 0.72) for p in leaves]
    )
    packets = "\n      ".join(
        travel(f"M{e[0][0]} {e[0][1]} L{e[1][0]} {e[1][1]}", 3.6, 0.35 * i, t.accent)
        for i, e in enumerate(edges[:5])
    )

    return f"""{head(t, W, H, f"{NAME} — local-first AI systems, autonomous agents, and tools that run on your own machine")}
  <style>{css}
  </style>
  {card(t, W, H, rx=0)}
  <g stroke="{t.ink}" fill="none">
    {ticks(34, W, 64, t.ink)}
    <path d="M0 176 H{W}" opacity="0.34"/>
  </g>

  {caps(t, 4, 86, KICKER, size=13, op=0.62, cls="kick")}
  <text class="name" x="2" y="150" fill="{t.ink}" font-family="{SERIF}" font-size="66"
        letter-spacing="0.5">{NAME}</text>

  <g stroke="{t.ink}" fill="{t.ink}">
      {lines}
      <circle cx="{cx}" cy="{cy}" r="5" opacity="1"/>
      {dots}
      {packets}
      <circle class="pulse" cx="{cx}" cy="{cy}" r="7" fill="none" opacity="0.5"/>
  </g>
</svg>
"""


# ══════════════════════════════════════════════════════════════════════════════
# bands — 1280 × 300 : four stations, theme-specific icon set
# ══════════════════════════════════════════════════════════════════════════════


def station_icon(t: Theme, kind: str, x: int, cy: int) -> str:
    """Hairline pictograms, 64×64 box centred on (x, cy)."""
    s = f'stroke="{t.ink}" fill="none" stroke-width="1.4" stroke-linecap="round"'

    if kind == "brief":
        if t.key == "paper":
            return f"""<g {s}><path d="M{x-18} {cy-26} H{x+7} L{x+18} {cy-15} V{cy+26} H{x-18} Z"/>
        <path d="M{x+7} {cy-26} V{cy-15} H{x+18}" opacity="0.5"/>
        <path d="M{x-9} {cy-9} H{x+9}" opacity="0.6"/><path d="M{x-9} {cy+1} H{x+5}" opacity="0.4"/>
        <path d="M{x+11} {cy+8} V{cy+18}" stroke-width="2.4">
          <animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></path></g>"""
        return f"""<g {s}><rect x="{x-20}" y="{cy-26}" width="40" height="52" rx="2"/>
        <path d="M{x-11} {cy-14} H{x+3}"/><path d="M{x-11} {cy-3} H{x+9}"/>
        <path d="M{x-11} {cy+8} H{x-2}"/><path d="M{x-11} {cy+19} H{x+6}" opacity="0.45"/>
        <path d="M{x+7} {cy+4} V{cy+13}" stroke-width="2">
          <animate attributeName="opacity" values="1;0;1" dur="1.15s" repeatCount="indefinite"/></path></g>"""

    if kind == "agents":
        cur = "".join(
            f'<path d="M{x+dx} {cy+dy} l0 12 l3.4 -3.2 l2.4 5.4 l3.2 -1.5 l-2.5 -5.3 l4.6 -0.4 z" '
            f'fill="{t.ink}" stroke="none" opacity="0.85"><animateTransform '
            f'attributeName="transform" type="translate" values="0 -5;0 0;0 -5" '
            f'dur="{2.4 + i*0.5}s" repeatCount="indefinite"/></path>'
            for i, (dx, dy) in enumerate([(-16, -18), (0, 6), (16, -16)])
        )
        return (f'<g {s}><rect x="{x-9}" y="{cy+13}" width="18" height="13" rx="1.5" opacity="0.5"/>'
                + cur + "</g>")

    if kind == "runtime":
        pins = "".join(
            f'<path d="M{x-26} {cy+o} h6"/><path d="M{x+20} {cy+o} h6"/>' for o in (-14, 0, 14)
        )
        return f"""<g {s}><rect x="{x-20}" y="{cy-20}" width="40" height="40" rx="2"/>
        <rect x="{x-11}" y="{cy-11}" width="22" height="22" rx="1" opacity="0.55"/>
        <path d="M{x-4} {cy} h8 M{x} {cy-4} v8" opacity="0.75">
          <animate attributeName="opacity" values="0.75;0.2;0.75" dur="2.2s" repeatCount="indefinite"/></path>
        {pins}</g>"""

    # file
    return f"""<g {s}><path d="M{x-19} {cy-26} H{x+7} L{x+19} {cy-14} V{cy+26} H{x-19} Z"/>
      <path d="M{x+7} {cy-26} V{cy-14} H{x+19}" opacity="0.55"/>
      <path d="M{x-10} {cy+4} l7 8 l14 -16" stroke-width="1.8">
        <animate attributeName="stroke-dasharray" values="0 40;34 40;34 40;0 40"
          keyTimes="0;0.45;0.75;1" dur="4.2s" repeatCount="indefinite"/></path></g>"""


def band(t: Theme) -> str:
    W, H = 1280, 300
    cy = 138
    xs = [150, 476, 802, 1128]

    icons = "\n    ".join(station_icon(t, k, x, cy) for x, (k, _, _) in zip(xs, STATIONS))

    labels = "\n    ".join(
        caps(t, x, cy + 70, name, size=12, op=0.92, anchor="middle", cls=f"lab{i}", track=3.4)
        + "\n    " + caps(t, x, cy + 90, gloss, size=11, op=0.44, anchor="middle", cls=f"lab{i}")
        for i, (x, (_, name, gloss)) in enumerate(zip(xs, STATIONS))
    )

    routes, packets = [], []
    for i in range(len(xs) - 1):
        a, b = xs[i] + 30, xs[i + 1] - 30
        routes.append(
            f'<path d="M{a} {cy} L{b} {cy}" opacity="0.4" stroke-dasharray="2 7" stroke-width="1.2">'
            f'<animate attributeName="stroke-dashoffset" values="0;-18" dur="1.5s" '
            f'repeatCount="indefinite"/></path>'
        )
        packets.append(travel(f"M{a} {cy} L{b} {cy}", 3.0, 0.5 + i * 0.75, t.accent, 2.6))

    css = f"""
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes sweep {{ from {{ stroke-dashoffset: 1080; }} to {{ stroke-dashoffset: 0; }} }}
    .rule {{ stroke-dasharray: 1080; animation: sweep 1.6s .2s ease-out both; }}
    """ + "\n    ".join(
        f".lab{i} {{ animation: rise .6s {0.9 + i * 0.18:.2f}s cubic-bezier(.2,.7,.3,1) both; }}"
        for i in range(4)
    ) + REDUCED

    title = {
        "typewriter": "HOW A BUILD RUNS",
        "blueprint": "ASSEMBLY ORDER",
        "paper": "The shape of the work",
        "swarm": "HOW A BUILD RUNS",
    }[t.key]
    stamp = "ONE MACHINE · NOTHING LEAVES IT"

    return f"""{head(t, W, H, "How a build runs: you write a brief, agents build it, it runs locally, you keep the file")}
  <style>{css}
  </style>
  {card(t, W, H, rx=0)}
  <g stroke="{t.ink}" fill="none" opacity="0.5">
    {ticks(34, W, 64, t.ink)}
    <path class="rule" d="M0 274 H{W}" opacity="0.3"/>
  </g>

  {caps(t, 40, 84, title, size=12, op=0.7, cls="lab0", track=4.6)}

  <g fill="{t.ink}">
    {icons}
  </g>

  <g stroke="{t.accent}" fill="none">
    {"".join(routes)}
  </g>
  <g fill="{t.accent}">
    {packets}
  </g>

  {labels}

  {caps(t, 640, 292, stamp, size=10, op=0.42, anchor="middle", cls="lab3", track=3.4)}
</svg>
"""


# ══════════════════════════════════════════════════════════════════════════════
# glyphs — 124 × 64, one schematic per project
# ══════════════════════════════════════════════════════════════════════════════


def glyph(t: Theme, kind: str) -> str:
    W, H = 124, 64
    cx, cy = W / 2, H / 2
    ink = t.ink
    s = f'stroke="{ink}" fill="none" stroke-width="1.3" stroke-linecap="round"'
    body = ""

    if kind == "jarvis":
        bars = "".join(
            f'<path d="M{x} {cy-h/2} V{cy+h/2}"><animate attributeName="d" '
            f'values="M{x} {cy-h/2} V{cy+h/2};M{x} {cy-h} V{cy+h};M{x} {cy-h/2} V{cy+h/2}" '
            f'dur="{1.2+i*0.18}s" repeatCount="indefinite"/></path>'
            for i, (x, h) in enumerate([(18, 14), (27, 22), (36, 10)])
        )
        body = (f'<g {s}>{bars}</g><g {s}><circle cx="66" cy="{cy}" r="15"/>'
                f'<circle cx="66" cy="{cy}" r="24" opacity="0.35"/></g>'
                f'<circle cx="66" cy="{cy}" r="4" fill="{ink}" stroke="none"/>'
                f'<circle cx="92" cy="{cy-9}" r="2.2" fill="{ink}" stroke="none" opacity="0.7">'
                f'<animateMotion dur="4s" repeatCount="indefinite" path="M0 0 a14 14 0 1 1 -0.1 0"/></circle>')

    elif kind == "swarmcraft":
        cur = "".join(
            f'<path d="M{x} {y} l0 9 l2.6 -2.4 l1.9 4.1 l2.4 -1.1 l-1.9 -4 l3.5 -0.3 z" '
            f'fill="{ink}" stroke="none"><animateTransform attributeName="transform" '
            f'type="translate" values="0 -3;0 0;0 -3" dur="{2+i*0.45}s" repeatCount="indefinite"/>'
            f'</path>'
            for i, (x, y) in enumerate([(40, 16), (64, 30), (52, 44)])
        )
        body = (f'<g {s}><rect x="24" y="10" width="76" height="44" rx="2" opacity="0.85"/>'
                f'<path d="M32 22 H60" opacity="0.55"/><path d="M32 31 H78" opacity="0.3"/>'
                f'<path d="M32 40 H68" opacity="0.3"/></g>{cur}')

    elif kind == "osint":
        body = (
            f'<g {s}><circle cx="{cx}" cy="{cy}" r="26" opacity="0.26"/>'
            f'<circle cx="{cx}" cy="{cy}" r="17" opacity="0.34"/>'
            f'<path d="M{cx} {cy-17} L{cx+24} {cy+6} L{cx-24} {cy+10} Z" opacity="0.45"/>'
            f'<path d="M{cx} {cy-26} V{cy+26}" opacity="0.16"/></g>'
            f'<g fill="{ink}" stroke="none"><circle cx="{cx}" cy="{cy-17}" r="2.6"/>'
            f'<circle cx="{cx+24}" cy="{cy+6}" r="2.6"/><circle cx="{cx-24}" cy="{cy+10}" r="2.6"/>'
            f'<circle cx="{cx}" cy="{cy}" r="3.4"/></g>'
        )

    elif kind == "nexus":
        body = (
            f'<g {s}><rect x="24" y="32" width="54" height="22" rx="2" opacity="0.26"/>'
            f'<rect x="33" y="23" width="54" height="22" rx="2" opacity="0.46"/>'
            f'<g><animateTransform attributeName="transform" type="translate" '
            f'values="0 2;0 -2;0 2" dur="4.6s" repeatCount="indefinite"/>'
            f'<rect x="42" y="12" width="54" height="22" rx="2"/>'
            f'<path d="M42 18 H96" opacity="0.45"/>'
            f'<circle cx="48" cy="15" r="1.4" fill="{ink}" stroke="none" opacity="0.7"/>'
            f'<path d="M50 27 H74" opacity="0.55"/><path d="M50 31 H66" opacity="0.3"/></g></g>'
        )

    elif kind == "connect":
        dots = []
        for r in range(3):
            for c in range(5):
                x, y = 30 + c * 16, 20 + r * 12
                sel = (r, c) == (1, 2)
                dots.append(f'<circle cx="{x}" cy="{y}" r="{3 if sel else 1.7}" '
                            f'opacity="{1 if sel else 0.42}"/>')
        body = (f'<g fill="{ink}" stroke="none">{"".join(dots)}'
                f'<circle cx="62" cy="32" r="7" fill="none" stroke="{ink}" stroke-width="1.1" opacity="0.7">'
                f'<animate attributeName="r" values="6;10" dur="2.6s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0.7;0" dur="2.6s" repeatCount="indefinite"/>'
                f'</circle></g>')

    else:  # powerpoint
        body = (
            f'<g {s}><rect x="14" y="20" width="38" height="26" rx="2" opacity="0.5"/>'
            f'<rect x="72" y="20" width="38" height="26" rx="2"/>'
            f'<path d="M34 36 H66" opacity="0.5" stroke-dasharray="2 4"/></g>'
            f'<path d="M60 30 l6 6 l-6 6" {s} opacity="0.9"><animate attributeName="opacity" '
            f'values="1;0.25;1" dur="2.2s" repeatCount="indefinite"/></path>'
        )

    return f"""{head(t, W, H, f"{kind} project schematic")}
  {card(t, W, H, rx=6)}
  {body}
</svg>
"""


# ══════════════════════════════════════════════════════════════════════════════


BANNERS = {
    "typewriter": banner_typewriter,
    "blueprint": banner_blueprint,
    "paper": banner_paper,
    "swarm": banner_swarm,
}


def main() -> None:
    total = 0
    for key in ORDER:
        t = THEMES[key]
        d = OUT / key
        d.mkdir(parents=True, exist_ok=True)

        files = {"banner": BANNERS[key](t), "band": band(t)}
        for slug, _, kind, _, _ in PROJECTS:
            files[f"glyph-{slug}"] = glyph(t, kind)

        for name, svg in files.items():
            p = d / f"{name}.svg"
            p.write_text(svg, encoding="utf-8")
            total += p.stat().st_size
        print(f"{key:11s} {len(files)} files  {sum(len(s) for s in files.values()):>7,} B")

    print(f"{'total':11s} {total:,} B across {len(ORDER)} themes")


if __name__ == "__main__":
    main()
