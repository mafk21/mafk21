#!/usr/bin/env python3
"""Generate the one-card profile: the whole profile in a single animated SVG.

    python3 tools/make-card.py

Writes assets/card-<theme>.svg — 1000 × 1500, a 2:3 portrait sheet that holds
the masthead, the build-flow band, all six projects with their glyphs, the
principles, the toolbox and the links.

Why a card and not a stack of images
------------------------------------
A single file means the composition is controlled: nothing reflows, the theme
is unmistakable, and every element can animate on one shared timeline. Text is
kept as SVG <text> so it stays sharp and selectable, and every animated element
rests in its finished state.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from artlib import (  # noqa: E402
    KICKER, MONO, NAME, ORDER, PROJECTS, REDUCED, SANS, SERIF, STATIONS, THEMES,
    Theme, caps, head, ticks, travel,
)

OUT = Path(__file__).resolve().parent.parent / "assets"

W, H = 1000, 1560
PAD = 64


# ── small helpers ─────────────────────────────────────────────────────────────


def wrap(text: str, width: int, size: float) -> list[str]:
    """Greedy wrap. Average glyph advance is ~0.52em for the sans face used."""
    per = max(12, int(width / (size * 0.52)))
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) <= per:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(x: int, y: int, text: str, t: Theme, width: int, size: int = 17,
         lh: float = 1.55, op: float = 0.72, cls: str = "", font: str | None = None) -> str:
    lines = wrap(text, width, size)
    spans = "\n    ".join(
        f'<tspan x="{x}" dy="{0 if i == 0 else round(size * lh)}">{ln}</tspan>'
        for i, ln in enumerate(lines)
    )
    c = f' class="{cls}"' if cls else ""
    return (
        f'<text x="{x}" y="{y}"{c} fill="{t.ink}" fill-opacity="{op}" '
        f'font-family="{font or SANS}" font-size="{size}">\n    {spans}\n  </text>'
    )


def rule(x1: int, y: int, x2: int, t: Theme, op: float = 0.18,
         accent: bool = False, cls: str = "") -> str:
    c = f' class="{cls}"' if cls else ""
    col = t.accent if accent else t.ink
    return f'<path{c} d="M{x1} {y} H{x2}" stroke="{col}" stroke-opacity="{op}" fill="none"/>'


# ── the card ──────────────────────────────────────────────────────────────────


def masthead(t: Theme) -> tuple[str, int]:
    """Banner block on its own timeline. Returns markup and the y it ends at."""
    h = 268
    cx, cy = 806, 138
    ring = [(cx - 66, cy - 30), (cx + 64, cy - 22), (cx - 54, cy + 40),
            (cx + 50, cy + 42), (cx - 90, cy + 6)]
    leaves = [(cx - 84, cy - 58), (cx + 96, cy + 4)]
    edges = [((cx, cy), p) for p in ring] + [(ring[0], leaves[0]), (ring[1], leaves[1])]

    lines = "\n      ".join(
        f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" opacity="0.34" stroke-width="1"/>'
        for a, b in edges
    )
    dots = "\n      ".join(
        f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" opacity="{o}"/>'
        for p, r, o in [(p, 2.7, 0.9) for p in ring] + [(p, 2.0, 0.66) for p in leaves]
    )
    packets = "\n      ".join(
        travel(f"M{e[0][0]} {e[0][1]} L{e[1][0]} {e[1][1]}", 4.2, 0.45 * i, t.accent)
        for i, e in enumerate(edges[:5])
    )

    name_w, reveal = 372, 382
    markup = f"""
  <g clip-path="url(#nameclip)">
    <text x="64" y="182" fill="{t.ink}" font-family="{SERIF}" font-size="62"
          letter-spacing="0.2">{NAME}</text>
  </g>
  <rect class="writehead" x="{64 + reveal - 2}" y="126" width="2.5" height="58" fill="{t.accent}"/>

  {caps(t, 64, 92, KICKER, size=11, op=0.62, cls="rise-a", track=4.0)}
  {rule(64, 200, 64 + 372, t, op=0.9, accent=True, cls="rule-draw")}

  <g class="rise-c">
    <circle class="live" cx="72" cy="222" r="3.2" fill="{t.accent}"/>
    {caps(t, 86, 226, "BUILDING JARVIS · LOCAL-FIRST", size=10, op=0.58, track=3.0)}
  </g>

  <g stroke="{t.ink}" fill="{t.ink}">
      <circle class="orbit" cx="{cx}" cy="{cy}" r="52" fill="none" opacity="0.28"
              stroke-dasharray="3 9" stroke-width="1"/>
      {lines}
      {dots}
      <circle class="breath" cx="{cx}" cy="{cy}" r="7" fill="{t.accent}"/>
      {packets}
  </g>
  <circle cx="{cx}" cy="{cy}" r="2.3" fill="{t.bg}"/>
"""
    return markup, h


def flow_band(t: Theme, top: int) -> tuple[str, int]:
    """Four stations across the card. Scaled down from the 1280-wide band."""
    h = 250
    cy = top + 96
    xs = [150, 383, 616, 849]
    icons = {
        "brief": f'''<g stroke="{t.ink}" fill="none" stroke-width="1.5" stroke-linecap="round">
        <rect x="{0}" y="{0}" width="34" height="44" rx="2"/>
        <path d="M9 12 H23"/><path d="M9 21 H29"/><path d="M9 30 H17" opacity="0.5"/>
        <path d="M26 33 V42" stroke-width="2">
          <animate attributeName="opacity" values="1;0;1" dur="1.15s" repeatCount="indefinite"/></path></g>''',
        "agents": f'''<g stroke="{t.ink}" fill="none" stroke-width="1.5">
        <rect x="-8" y="12" width="16" height="11" rx="1.5" opacity="0.5"/></g>
        <g fill="{t.ink}">
          <path d="M-16 -14 l0 11 l3 -2.9 l2.2 4.9 l2.9 -1.3 l-2.3 -4.8 l4.2 -0.3 z">
            <animateTransform attributeName="transform" type="translate"
              values="0 -4;0 0;0 -4" dur="2.4s" repeatCount="indefinite"/></path>
          <path d="M1 1 l0 11 l3 -2.9 l2.2 4.9 l2.9 -1.3 l-2.3 -4.8 l4.2 -0.3 z">
            <animateTransform attributeName="transform" type="translate"
              values="0 -4;0 0;0 -4" dur="2.9s" repeatCount="indefinite"/></path>
          <path d="M15 -13 l0 11 l3 -2.9 l2.2 4.9 l2.9 -1.3 l-2.3 -4.8 l4.2 -0.3 z">
            <animateTransform attributeName="transform" type="translate"
              values="0 -4;0 0;0 -4" dur="3.4s" repeatCount="indefinite"/></path></g>''',
        "runtime": f'''<g stroke="{t.ink}" fill="none" stroke-width="1.5">
        <rect x="-17" y="-17" width="34" height="34" rx="2"/>
        <rect x="-9" y="-9" width="18" height="18" rx="1" opacity="0.55"/>
        <path d="M-3 0 h6 M0 -3 v6" opacity="0.8">
          <animate attributeName="opacity" values="0.8;0.2;0.8" dur="2.2s" repeatCount="indefinite"/></path>
        <path d="M-22 -12 h5 M17 -12 h5 M-22 0 h5 M17 0 h5 M-22 12 h5 M17 12 h5"/></g>''',
        "file": f'''<g stroke="{t.ink}" fill="none" stroke-width="1.5" stroke-linecap="round">
        <path d="M-16 -22 H6 L16 -12 V22 H-16 Z"/><path d="M6 -22 V-12 H16" opacity="0.55"/>
        <path d="M-8 3 l6 7 l12 -14" stroke-width="1.8">
          <animate attributeName="stroke-dasharray" values="0 34;30 34;30 34;0 34"
            keyTimes="0;0.45;0.75;1" dur="4.2s" repeatCount="indefinite"/></path></g>''',
    }

    parts = []
    for i, (x, (kind, name, gloss)) in enumerate(zip(xs, STATIONS)):
        d = 0.9 + i * 0.16
        parts.append(f'''
  <g transform="translate({x} {cy})" fill="{t.ink}" class="stn" style="animation-delay:{d}s">
    {icons[kind]}
  </g>
  {caps(t, x, cy + 58, f"0{i+1}", size=10, op=0.7, anchor="middle", fill=t.accent,
        cls="stn", track=2.2).replace('<text', f'<text style="animation-delay:{d + .12}s"', 1)}
  {caps(t, x, cy + 82, name, size=12, op=0.92, anchor="middle", cls="stn", track=3.2)
        .replace('<text', f'<text style="animation-delay:{d + .18}s"', 1)}
  {caps(t, x, cy + 101, gloss, size=11, op=0.44, anchor="middle", cls="stn")
        .replace('<text', f'<text style="animation-delay:{d + .24}s"', 1)}''')

    routes, packets = [], []
    for i in range(len(xs) - 1):
        a, b = xs[i] + 32, xs[i + 1] - 32
        routes.append(
            f'<path class="route" d="M{a} {cy} L{b} {cy}" opacity="0.4" '
            f'stroke-dasharray="2 7" stroke-width="1.2">'
            f'<animate attributeName="stroke-dashoffset" values="0;-18" dur="1.5s" '
            f'repeatCount="indefinite"/></path>'
        )
        packets.append(travel(f"M{a} {cy} L{b} {cy}", 3.0, 0.5 + i * 0.75, t.accent, 2.4))

    markup = f"""
  {caps(t, 64, top + 34, "HOW A BUILD RUNS", size=12, op=0.66, cls="rise-a", track=4.4)}
  {"".join(parts)}
  <g stroke="{t.accent}" fill="none" class="rise-b">{"".join(routes)}</g>
  <g fill="{t.accent}">{"".join(packets)}</g>
  {caps(t, W / 2, top + h - 12, "ONE MACHINE · NOTHING LEAVES IT", size=10, op=0.42,
        anchor="middle", cls="rise-c", track=3.2)}
"""
    return markup, h


def glyph_signal(slug: str, kind: str, t: Theme) -> str:
    """Inline schematic, translated to sit inside a project row."""
    ink = t.ink
    s = f'stroke="{ink}" fill="none" stroke-width="1.3" stroke-linecap="round"'

    if kind == "jarvis":
        bars = "".join(
            f'<path d="M{x} {-h/2} V{h/2}"><animate attributeName="d" '
            f'values="M{x} {-h/2} V{h/2};M{x} {-h} V{h};M{x} {-h/2} V{h/2}" '
            f'dur="{1.2 + i*0.18}s" repeatCount="indefinite"/></path>'
            for i, (x, h) in enumerate([(-34, 14), (-25, 22), (-16, 10)])
        )
        body = (f'<g {s}>{bars}</g><circle cx="8" cy="0" r="14" {s}/>'
                f'<circle cx="8" cy="0" r="22" {s} opacity="0.32"/>'
                f'<circle cx="8" cy="0" r="3.8" fill="{ink}" stroke="none"/>')
    elif kind == "swarmcraft":
        cur = "".join(
            f'<path d="M{x} {y} l0 8 l2.4 -2.2 l1.7 3.8 l2.2 -1 l-1.7 -3.7 l3.2 -0.3 z" '
            f'fill="{ink}" stroke="none"><animateTransform attributeName="transform" '
            f'type="translate" values="0 -3;0 0;0 -3" dur="{2+i*0.45}s" '
            f'repeatCount="indefinite"/></path>'
            for i, (x, y) in enumerate([(-26, -16), (-2, -2), (-14, 12)])
        )
        body = (f'<g {s}><rect x="-36" y="-24" width="72" height="42" rx="2" opacity="0.85"/>'
                f'<path d="M-28 -12 H0" opacity="0.55"/><path d="M-28 -3 H8" opacity="0.3"/>'
                f'</g>{cur}')
    elif kind == "osint":
        body = (f'<g {s}><circle cx="0" cy="0" r="23" opacity="0.26"/>'
                f'<circle cx="0" cy="0" r="15" opacity="0.34"/>'
                f'<path d="M0 -15 L21 5 L-21 9 Z" opacity="0.45"/></g>'
                f'<g fill="{ink}" stroke="none"><circle cx="0" cy="-15" r="2.4"/>'
                f'<circle cx="21" cy="5" r="2.4"/><circle cx="-21" cy="9" r="2.4"/>'
                f'<circle cx="0" cy="0" r="3.2"/></g>')
    elif kind == "nexus":
        body = (f'<g {s}><rect x="-34" y="6" width="48" height="19" rx="2" opacity="0.26"/>'
                f'<rect x="-26" y="-2" width="48" height="19" rx="2" opacity="0.46"/>'
                f'<g><animateTransform attributeName="transform" type="translate" '
                f'values="0 2;0 -2;0 2" dur="4.6s" repeatCount="indefinite"/>'
                f'<rect x="-18" y="-12" width="48" height="19" rx="2"/>'
                f'<path d="M-18 -6 H30" opacity="0.45"/>'
                f'<circle cx="-12" cy="-9" r="1.3" fill="{ink}" stroke="none" opacity="0.7"/>'
                f'<path d="M-10 1 H12" opacity="0.55"/></g></g>')
    elif kind == "connect":
        dots = []
        for r in range(3):
            for c in range(5):
                x, y = -30 + c * 15, -12 + r * 12
                sel = (r, c) == (1, 2)
                dots.append(f'<circle cx="{x}" cy="{y}" r="{2.9 if sel else 1.6}" '
                            f'opacity="{1 if sel else 0.42}"/>')
        body = (f'<g fill="{ink}" stroke="none">{"".join(dots)}'
                f'<circle cx="0" cy="0" r="6.5" fill="none" stroke="{ink}" stroke-width="1.1" '
                f'opacity="0.7"><animate attributeName="r" values="5.5;9.5" dur="2.6s" '
                f'repeatCount="indefinite"/><animate attributeName="opacity" values="0.7;0" '
                f'dur="2.6s" repeatCount="indefinite"/></circle></g>')
    else:  # powerpoint
        body = (f'<g {s}><rect x="-38" y="-14" width="34" height="24" rx="2" opacity="0.5"/>'
                f'<rect x="6" y="-14" width="34" height="24" rx="2"/>'
                f'<path d="M-20 0 H0" opacity="0.5" stroke-dasharray="2 4"/></g>'
                f'<path d="M-6 -6 l5 5 l-5 5" {s}><animate attributeName="opacity" '
                f'values="1;0.25;1" dur="2.2s" repeatCount="indefinite"/></path>')
    return f'<g transform="translate(0 0)">{body}</g>'


def projects_block(t: Theme, top: int) -> tuple[str, int]:
    """Rows size themselves: name, then wrapped blurb, then tag, then a rule."""
    size, lh, text_w = 14, 21, W - PAD * 2 - 120
    rows = []
    y = top + 52
    for i, (slug, label, kind, blurb, tag) in enumerate(PROJECTS):
        n = len(wrap(blurb, text_w, size))
        d = 0.55 + i * 0.09
        name_y = y
        body_y = y + 22
        tag_y = body_y + (n - 1) * lh + 24
        sep_y = tag_y + 16
        rows.append(f'''
  <g class="row" style="animation-delay:{d}s">
    <g transform="translate({PAD + 52} {name_y + 8})">{glyph_signal(slug, kind, t)}</g>
    <text x="{PAD + 120}" y="{name_y + 6}" fill="{t.ink}" font-family="{SANS}" font-size="19"
          font-weight="600">{label}</text>
    {para(PAD + 120, body_y + 6, blurb, t, width=text_w, size=size, lh=lh / size, op=0.66)}
    {caps(t, PAD + 120, tag_y + 6, tag.upper(), size=9, op=0.55, fill=t.accent, track=2.6)}
  </g>
  {rule(PAD, sep_y, W - PAD, t, op=0.10)}''')
        y = sep_y + 22
    markup = f"""
  {caps(t, PAD, top + 10, "SELECTED WORK", size=12, op=0.66, cls="rise-a", track=4.4)}
  {"".join(rows)}
"""
    return markup, y - top


def footer_block(t: Theme, top: int) -> tuple[str, int]:
    principles = [
        ("Local-first by default.", "Your keys, your machine, your files."),
        ("The output is a file.", "HTML you can open, a .pptx you can edit, evidence you can keep."),
        ("Say the limits out loud.", "Unverified installers and trade-offs are written down, not discovered."),
        ("Fewer, better parts.", "Zero pip dependencies where possible; one clear path to run it."),
    ]
    items = []
    y = top + 40
    for i, (lead, rest) in enumerate(principles):
        items.append(f'''
  <g class="row" style="animation-delay:{0.9 + i * 0.09}s">
    <circle cx="{PAD + 4}" cy="{y - 5}" r="3" fill="{t.accent}" opacity="0.85"/>
    <text x="{PAD + 20}" y="{y}" fill="{t.ink}" font-family="{SANS}" font-size="15"
          font-weight="600">{lead}
      <tspan fill="{t.ink}" fill-opacity="0.62" font-weight="400">{rest}</tspan>
    </text>
  </g>''')
        y += 30

    stack = ["Python", "TypeScript", "JavaScript", "Astro", "Node",
             "Electron", "Playwright", "SQLite / FTS5", "MCP", "GitHub Actions"]
    x, sy = PAD, y + 26
    chips = []
    for label in stack:
        w = 22 + len(label) * 7.4
        if x + w > W - PAD:
            x, sy = PAD, sy + 34
        chips.append(
            f'<rect x="{x:.0f}" y="{sy - 16}" width="{w:.0f}" height="26" rx="13" '
            f'fill="{t.ink}" fill-opacity="0.06" stroke="{t.ink}" stroke-opacity="0.14"/>'
            f'<text x="{x + w/2:.0f}" y="{sy + 2}" text-anchor="middle" fill="{t.ink}" '
            f'fill-opacity="0.72" font-family="{MONO}" font-size="11">{label}</text>'
        )
        x += w + 10

    markup = f"""
  {caps(t, PAD, top - 4, "HOW I BUILD", size=12, op=0.66, cls="rise-a", track=4.4)}
  {"".join(items)}
  <g class="rise-c">{"".join(chips)}</g>
  {rule(PAD, sy + 34, W - PAD, t, op=0.2)}

  <g class="rise-c">
    <text x="{PAD}" y="{sy + 66}" fill="{t.ink}" font-family="{SANS}" font-size="14"
          fill-opacity="0.8">guns.lol/dr.abo3tab</text>
    <circle cx="{W/2 - 30}" cy="{sy + 62}" r="1.8" fill="{t.accent}" opacity="0.8"/>
    <text x="{W/2 - 12}" y="{sy + 66}" fill="{t.ink}" font-family="{SANS}" font-size="14"
          fill-opacity="0.8">mbm143105@gmail.com</text>
    <circle cx="{W - PAD - 132}" cy="{sy + 62}" r="1.8" fill="{t.accent}" opacity="0.8"/>
    <text x="{W - PAD - 114}" y="{sy + 66}" fill="{t.ink}" font-family="{SANS}" font-size="14"
          fill-opacity="0.8">github.com/mafk21</text>
  </g>
"""
    return markup, sy + 66 - top


def card(t: Theme) -> str:
    name_w, reveal = 372, 382

    css = f"""
    @keyframes rise    {{ from {{ opacity: 0; transform: translateY(9px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes draw    {{ from {{ stroke-dashoffset: 372; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes writehead {{ 0% {{ opacity: 0; }} 6% {{ opacity: .95; }} 94% {{ opacity: .95; }} 100% {{ opacity: .22; }} }}
    @keyframes breath  {{ 0%,100% {{ opacity: .55; r: 7; }} 50% {{ opacity: .95; r: 9; }} }}
    @keyframes spin    {{ to {{ transform: rotate(360deg); }} }}
    @keyframes live    {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .3; }} }}
    .rise-a {{ animation: rise .7s .35s cubic-bezier(.2,.7,.3,1) both; }}
    .rise-b {{ animation: rise .7s .8s cubic-bezier(.2,.7,.3,1) both; }}
    .rise-c {{ animation: rise .7s 1.1s cubic-bezier(.2,.7,.3,1) both; }}
    .row    {{ animation: rise .6s cubic-bezier(.2,.7,.3,1) both; }}
    .stn    {{ animation: rise .6s cubic-bezier(.2,.7,.3,1) both; }}
    .rule-draw {{ stroke-dasharray: 372; animation: draw 1.1s 1.0s ease-out both; }}
    .writehead {{ animation: writehead 1.9s ease-out both; }}
    .breath {{ animation: breath 4.2s ease-in-out infinite; }}
    .orbit  {{ animation: spin 46s linear infinite; transform-origin: 806px 138px; }}
    .live   {{ animation: live 2.4s ease-in-out infinite; }}
    {REDUCED}"""

    mast, mast_h = masthead(t)
    band_top = mast_h + 12
    band, band_h = flow_band(t, band_top)
    proj_top = band_top + band_h + 14
    proj, proj_h = projects_block(t, proj_top)
    foot_top = proj_top + proj_h + 18
    foot, foot_h = footer_block(t, foot_top)

    body = mast + band + proj + foot
    used = foot_top + foot_h + 56          # room for the closing rule
    height = int(used + 24)

    return f"""{head(t, W, height, "Dr. Abo 3tab — local-first AI: an animated profile card showing selected work, how a build runs, and how I build")}
  <defs>
    <radialGradient id="cglow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{t.accent}" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="{t.accent}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="nameclip">
      <rect x="64" y="120" width="{reveal}" height="80">
        <animate attributeName="width" from="0" to="{reveal}" dur="1.8s" begin="0.3s"
                 fill="freeze" calcMode="spline" keySplines="0.22 0.9 0.25 1"
                 keyTimes="0;1" values="0;{reveal}"/>
      </rect>
    </clipPath>
  </defs>
  <style>{css}
  </style>

  <rect width="{W}" height="{height}" fill="{t.bg}"/>
  <ellipse cx="210" cy="176" rx="300" ry="120" fill="url(#cglow)" opacity="0.30"/>

  <g stroke="{t.ink}" fill="none" opacity="0.5">
    {ticks(44, W, 56, t.ink, length=6)}
  </g>
  <path d="M{PAD} {mast_h - 10} H{W - PAD}" stroke="{t.ink}" stroke-opacity="0.16" fill="none"/>

  {body}
</svg>
"""


def main() -> None:
    for key in ORDER:
        t = THEMES[key]
        svg = card(t)
        p = OUT / f"card-{key}.svg"
        p.write_text(svg, encoding="utf-8")
        # sanity: the card must not overflow its own canvas
        print(f"{key:11s} card  {p.stat().st_size:>7,} B")


if __name__ == "__main__":
    main()
