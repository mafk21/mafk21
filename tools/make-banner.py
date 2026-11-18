#!/usr/bin/env python3
"""Generate the profile banner in light and dark variants.

The banner is deliberately a masthead, not an illustration: a ruler rule, one
eyebrow line, the name, and a small node graph that stands in for "systems".
Everything is hairline and text, so it stays legible at mobile width and never
looks like a stock hero image.

    python3 tools/make-banner.py

Writes assets/banner-light.svg and assets/banner-dark.svg.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

W, H = 1280, 188

INK = {
    "light": "#1c1c1c",
    "dark": "#e9e7e1",
}

SERIF = "Georgia, 'Iowan Old Style', 'Times New Roman', serif"
SANS = "-apple-system, 'Helvetica Neue', Helvetica, Arial, sans-serif"

NAME = "Dr. Abo 3tab"
EYEBROW = "LOCAL-FIRST AI  ·  AUTONOMOUS AGENTS  ·  TOOLS THAT SHIP AS FILES"


def ticks(x0: int, x1: int, y: int, step: int, length: int) -> str:
    """A ruler line: tick marks hanging below y, fading toward the right."""
    parts = []
    x = x0
    i = 0
    while x <= x1:
        # Alternate a long tick every fourth mark for a measured, not mechanical, feel.
        ln = length if i % 4 else length + 5
        op = max(0.10, 0.30 - (i * 0.012))
        parts.append(
            f'<path d="M{x} {y} V{y + ln}" opacity="{op:.2f}"/>'
        )
        x += step
        i += 1
    return "\n    ".join(parts)


def node_graph(cx: int, cy: int) -> str:
    """Seven nodes, one hub. Reads as a system diagram at any size."""
    hub = (cx, cy)
    ring = [
        (cx - 96, cy - 44),
        (cx + 92, cy - 34),
        (cx - 78, cy + 52),
        (cx + 74, cy + 56),
        (cx - 128, cy + 8),
    ]
    leaves = [(cx - 120, cy - 78), (cx + 136, cy + 6)]

    edges = [(hub, p) for p in ring] + [(ring[0], leaves[0]), (ring[1], leaves[1])]
    lines = "\n    ".join(
        f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" opacity="0.38" stroke-width="1"/>'
        for a, b in edges
    )
    dots = "\n    ".join(
        f'<circle cx="{p[0]}" cy="{p[1]}" r="{r}" opacity="{o}"/>'
        for p, r, o in [(hub, 5.0, 1.0)]
        + [(p, 3.0, 0.95) for p in ring]
        + [(p, 2.2, 0.72) for p in leaves]
    )
    return f'<g stroke="CURRENT" fill="CURRENT">\n    {lines}\n    {dots}\n  </g>'


def build(ink: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{NAME} — local-first AI systems, autonomous agents, and tools that run on your own machine">
  <g stroke="{ink}" fill="none">
    <path d="M0 34 H{W}" opacity="0.34"/>
    {ticks(0, W, 34, 64, 7)}
    <path d="M0 176 H{W}" opacity="0.34"/>
  </g>

  <text x="4" y="86" fill="{ink}" fill-opacity="0.62"
        font-family="{SANS}" font-size="13" letter-spacing="4.6" font-weight="500">{EYEBROW}</text>

  <text x="2" y="150" fill="{ink}" font-family="{SERIF}" font-size="66" letter-spacing="0.5">{NAME}</text>

  {node_graph(1128, 104).replace("CURRENT", ink)}
</svg>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for theme, ink in INK.items():
        path = OUT / f"banner-{theme}.svg"
        path.write_text(build(ink), encoding="utf-8")
        print(f"wrote {path.relative_to(OUT.parent)} ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
