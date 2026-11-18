#!/usr/bin/env python3
"""Drawing library for the profile themes.

Four complete looks, each with its own background so it reads the same on
GitHub's light and dark themes. Every theme animates text, band, and glyphs:

  01 signal      near-black, the name writes itself out, amber graph
  02 swarm       the node graph, travelling packets, nine cursors
  03 typewriter  terminal card, typed title with a block caret, scanline
  04 blueprint   deep blue sheet, self-drawing lines, dimension marks
  05 paper       warm off-white, serif, ink stamp, hand-rule marks

Motion is CSS `@keyframes` (works on GitHub — snk and capsule-render both rely
on it) with SMIL only where a shape has to travel a path.
"""

from dataclasses import dataclass

SERIF = "Georgia, 'Iowan Old Style', 'Times New Roman', serif"
SANS = "-apple-system, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"


@dataclass(frozen=True)
class Theme:
    key: str
    label: str
    bg: str
    ink: str
    accent: str
    muted: str
    font: str
    note: str
    light: bool = False


THEMES = {
    "typewriter": Theme(
        "typewriter", "Typewriter",
        bg="#0b0f14", ink="#e6edf3", accent="#7ee787", muted="#8b949e",
        font=MONO,
        note="Terminal card. The name types itself out, then the caret blinks.",
    ),
    "blueprint": Theme(
        "blueprint", "Blueprint",
        bg="#0a1a2b", ink="#cfe6ff", accent="#4cc2ff", muted="#7f9dbb",
        font=SANS,
        note="Engineering sheet. Every rule draws itself, then labels rise in order.",
    ),
    "paper": Theme(
        "paper", "Paper",
        bg="#f4efe5", ink="#1b1a17", accent="#a8441f", muted="#7a7264",
        font=SERIF, light=True,
        note="Light editorial page. Serif name, rubber stamp, marks fade in.",
    ),
    "signal": Theme(
        "signal", "Signal",
        bg="#08090c", ink="#f2efe9", accent="#e8a33d", muted="#8b8b86",
        font=SERIF,
        note="Darkest look. The name draws itself, fills letter by letter, "
             "and the graph answers in amber.",
    ),
    "swarm": Theme(
        "swarm", "Swarm",
        bg="#0d1117", ink="#e9e7e1", accent="#d9b98a", muted="#8b8b86",
        font=SERIF,
        note="Node graph with packets in flight; nine cursors draw the page.",
    ),
}

ORDER = ["signal", "swarm", "typewriter", "blueprint", "paper"]


# ── shared ────────────────────────────────────────────────────────────────────

REDUCED = """
    @media (prefers-reduced-motion: reduce) {
      * { animation: none !important; }
    }"""


def head(t: Theme, w: int, h: int, label: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
    )


def card(t: Theme, w: int, h: int, rx: int = 10) -> str:
    return f'<rect width="{w}" height="{h}" rx="{rx}" fill="{t.bg}"/>'


def caps(t: Theme, x: int, y: int, text: str, size: int = 12, op: float = 0.62,
         anchor: str = "start", cls: str = "", fill: str | None = None,
         track: float = 4.4) -> str:
    c = f' class="{cls}"' if cls else ""
    return (
        f'<text x="{x}" y="{y}"{c} text-anchor="{anchor}" fill="{fill or t.ink}" '
        f'fill-opacity="{op}" font-family="{SANS}" font-size="{size}" '
        f'letter-spacing="{track}" font-weight="500">{text}</text>'
    )


def rise(cls: str, delay: float) -> str:
    """Staggered rise-in; one class per element so no inline styles are needed."""
    return (
        f".{cls} {{ animation: rise .7s cubic-bezier(.2,.7,.3,1) both; "
        f"animation-delay: {delay}s; }}"
    )


def ticks(y: int, w: int, step: int, colour: str, length: int = 7) -> str:
    out = [f'<path d="M0 {y} H{w}" opacity="0.30"/>']
    x, i = 0, 0
    while x <= w:
        ln = length + 5 if i % 4 == 0 else length
        op = max(0.09, 0.28 - i * 0.011)
        out.append(f'<path d="M{x} {y} V{y + ln}" opacity="{op:.2f}"/>')
        x += step
        i += 1
    return "\n      ".join(out)


def travel(path: str, dur: float, begin: float, ink: str, r: float = 2.2) -> str:
    return (
        f'<circle cx="0" cy="0" r="{r}" fill="{ink}" opacity="0">\n'
        f'        <animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" '
        f'path="{path}" calcMode="spline" keyPoints="0;1" keyTimes="0;1" '
        f'keySplines="0.4 0 0.6 1"/>\n'
        f'        <animate attributeName="opacity" dur="{dur}s" begin="{begin}s" '
        f'repeatCount="indefinite" values="0;0.9;0.9;0" keyTimes="0;0.12;0.86;1"/>\n'
        f'      </circle>'
    )


# ── shared content ────────────────────────────────────────────────────────────

NAME = "Dr. Abo 3tab"
KICKER = "LOCAL-FIRST AI  ·  AUTONOMOUS AGENTS  ·  TOOLS THAT SHIP AS FILES"
STATIONS = [
    ("brief", "BRIEF", "you type it"),
    ("agents", "AGENTS", "they build it"),
    ("runtime", "RUNTIME", "local, yours"),
    ("file", "FILE", "you keep it"),
]
PROJECTS = [
    ("jarvis", "JARVIS", "jarvis",
     "A local-first AI system that can see, speak, remember, and act — voice, "
     "screen vision, computer control, durable memory, long-running work.",
     "Windows · macOS · Linux"),
    ("swarmcraft", "Swarmcraft", "swarmcraft",
     "Describe a website and nine AI cursors draw it in front of you. Your own "
     "Gemini key, no backend, no model-written CSS.", "You keep the HTML"),
    ("osint", "OSINT Monster", "osint",
     "Autonomous recon engine: 45+ passive collectors, fully offline forensic "
     "decoders, graph studio, a validated 760-tool arsenal.", "Zero pip dependencies"),
    ("nexus", "NEXUS", "nexus",
     "A desktop that reshapes itself per task — categories → setups → "
     "activation, each with its own wallpaper, accent, and shortcuts.", "Electron"),
    ("connect", "Connect Everything", "connect",
     "534 hand-curated resources across 504 domains with 64 controlled tags. "
     "No accounts, no tracking, no ads.", "One click out"),
    ("powerpoint", "PowerPoint Skill", "powerpoint",
     "An AI skill for decks built on real research — Morph transitions, 13 "
     "layout blueprints, an Arabic/RTL path.", "238-record database"),
]
