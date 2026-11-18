#!/usr/bin/env python3
"""Generate the five mastheads.

    python3 tools/make-banners.py

Writes assets/<theme>/banner.svg for each theme in artlib.ORDER.
The profile body is a single animated card (tools/make-card.py).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from artlib import (  # noqa: E402
    KICKER, MONO, NAME, ORDER, REDUCED, SANS, SERIF, THEMES, Theme,
    caps, card, head, rise, ticks, travel,
)

OUT = Path(__file__).resolve().parent.parent / "assets"

def banner_signal(t: Theme) -> str:
    """The refined swarm: darkest ground, the name writes itself, amber answers.

    Motion, in order of what the eye catches:
      1. a soft amber glow breathes behind the name
      2. the name is revealed left-to-right by a clip, with a write-head riding
         the edge and fading once the reveal finishes
      3. an amber rule draws itself underneath, then the kicker and status pill
         rise in
      4. the graph answers: amber packets, a slow ring, breathing nodes
    Everything rests in its finished state, so a still frame is complete.
    """
    W, H = 1280, 216
    cx, cy = 1124, 110
    ring = [(cx - 92, cy - 40), (cx + 88, cy - 30), (cx - 74, cy + 54),
            (cx + 70, cy + 58), (cx - 124, cy + 10)]
    leaves = [(cx - 116, cy - 80), (cx + 132, cy + 8)]
    edges = [((cx, cy), p) for p in ring] + [(ring[0], leaves[0]), (ring[1], leaves[1])]

    name_w = 470            # measured: "Dr. Abo 3tab" at 74px Georgia ≈ 465px
    reveal = name_w + 10

    css = f"""
    @keyframes glow   {{ 0%,100% {{ opacity: .20; }} 50% {{ opacity: .40; }} }}
    @keyframes head   {{ 0% {{ opacity: 0; }} 8% {{ opacity: .95; }} 92% {{ opacity: .95; }} 100% {{ opacity: .25; }} }}
    @keyframes breath {{ 0%,100% {{ opacity: .55; r: 8; }} 50% {{ opacity: .95; r: 10; }} }}
    @keyframes spin   {{ to {{ transform: rotate(360deg); }} }}
    @keyframes rise   {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes live   {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
    @keyframes draw   {{ from {{ stroke-dashoffset: 460; }} to {{ stroke-dashoffset: 0; }} }}
    .glow  {{ animation: glow 7s ease-in-out infinite; }}
    .head  {{ animation: head 1.9s ease-out both; }}
    .ring  {{ animation: spin 46s linear infinite; transform-origin: {cx}px {cy}px; }}
    .breath{{ animation: breath 4.2s ease-in-out infinite; }}
    .k1    {{ animation: rise .8s 1.15s cubic-bezier(.2,.7,.3,1) both; }}
    .k2    {{ animation: rise .8s 1.35s cubic-bezier(.2,.7,.3,1) both; }}
    .rule  {{ stroke-dasharray: 460; animation: draw 1.1s 1.0s ease-out both; }}
    .live  {{ animation: live 2.4s ease-in-out infinite; }}
    {REDUCED}"""

    lines = "\n      ".join(
        f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" opacity="0.34" stroke-width="1"/>'
        for a, b in edges
    )
    dots = "\n      ".join(
        f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" opacity="{o}"/>'
        for p, r, o in [(p, 2.9, 0.9) for p in ring] + [(p, 2.1, 0.66) for p in leaves]
    )
    packets = "\n      ".join(
        travel(f"M{e[0][0]} {e[0][1]} L{e[1][0]} {e[1][1]}", 4.2, 0.45 * i, t.accent)
        for i, e in enumerate(edges[:5])
    )

    return f"""{head(t, W, H, f"{NAME} — local-first AI systems, autonomous agents, tools that run on your own machine")}
  <defs>
    <radialGradient id="sglow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{t.accent}" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="{t.accent}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="sclip"><rect class="clip" x="0" y="60" width="{reveal}" height="90">
      <animate attributeName="width" from="0" to="{reveal}" dur="1.8s" begin="0.35s"
               fill="freeze" calcMode="spline" keySplines="0.22 0.9 0.25 1"
               keyTimes="0;1" values="0;{reveal}"/>
    </rect></clipPath>
  </defs>
  <style>{css}
  </style>
  {card(t, W, H, rx=0)}

  <ellipse class="glow" cx="236" cy="126" rx="300" ry="58" fill="url(#sglow)" opacity="0.26"/>

  <g stroke="{t.ink}" fill="none" opacity="0.5">
    {ticks(30, W, 64, t.ink)}
    <path d="M0 198 H{W}" opacity="0.22"/>
  </g>

  <g clip-path="url(#sclip)">
    <text x="2" y="150" fill="{t.ink}" font-family="{SERIF}" font-size="74"
          letter-spacing="0.2">{NAME}</text>
  </g>

  <rect class="head" x="{reveal - 2}" y="88" width="2.5" height="66" fill="{t.accent}"/>

  <path class="rule" d="M2 174 H462" stroke="{t.accent}" stroke-width="1.6" opacity="0.85"/>

  {caps(t, 4, 70, KICKER, size=12, op=0.6, cls="k1", track=4.4)}

  <g class="k2">
    <circle class="live" cx="16" cy="196" r="3.4" fill="{t.accent}"/>
    {caps(t, 30, 200, "BUILDING JARVIS · LOCAL-FIRST", size=10, op=0.58, track=3.2)}
  </g>

  <g stroke="{t.ink}" fill="{t.ink}">
      <circle class="ring" cx="{cx}" cy="{cy}" r="64" fill="none" opacity="0.30"
              stroke-dasharray="3 9" stroke-width="1"/>
      {lines}
      {dots}
      <circle class="breath" cx="{cx}" cy="{cy}" r="8" fill="{t.accent}"/>
      {packets}
  </g>
  <circle cx="{cx}" cy="{cy}" r="2.6" fill="{t.bg}"/>
</svg>
"""


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



BANNERS = {
    "signal": banner_signal,
    "typewriter": banner_typewriter,
    "blueprint": banner_blueprint,
    "paper": banner_paper,
    "swarm": banner_swarm,
}


def main() -> None:
    total = 0
    for key in ORDER:
        d = OUT / key
        d.mkdir(parents=True, exist_ok=True)
        svg = BANNERS[key](THEMES[key])
        p = d / "banner.svg"
        p.write_text(svg, encoding="utf-8")
        total += p.stat().st_size
        print(f"{key:11s} banner.svg  {p.stat().st_size:>6,} B")
    print(f"{'total':11s} {total:,} B")


if __name__ == "__main__":
    main()
