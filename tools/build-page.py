#!/usr/bin/env python3
"""Build the interactive profile page.

    python3 tools/build-page.py

Reads every assets/card-*.svg, scrubs the XML declaration, strips the outer
<svg> wrapper so each card can be inlined into the DOM, and writes index.html —
a single self-contained page with no build step, no dependencies and no network
calls beyond the card itself.

The page is the only place real interactivity can live: GitHub's markdown
sanitizer removes <script> contents and strips id attributes, so a README can
animate but cannot respond to input.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from artlib import ORDER, PROJECTS, THEMES  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUT = ROOT / "index.html"

SVG_OPEN = re.compile(r"<svg[^>]*>", re.S)


def inner(svg: str) -> str:
    """Everything between <svg ...> and </svg>."""
    start = SVG_OPEN.search(svg)
    if not start:
        raise ValueError("not an svg")
    return svg[start.end(): svg.rindex("</svg>")]


def cards() -> dict[str, str]:
    out = {}
    for key in ORDER:
        path = ASSETS / f"card-{key}.svg"
        svg = path.read_text(encoding="utf-8")
        svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
        out[key] = inner(svg)
    return out


def main() -> None:
    data = cards()
    themes = {
        k: {"label": THEMES[k].label, "bg": THEMES[k].bg,
            "accent": THEMES[k].accent, "ink": THEMES[k].ink}
        for k in ORDER
    }
    projects = [
        {"slug": slug, "name": name, "kind": kind,
         "blurb": blurb, "tag": tag,
         "url": f"https://github.com/mafk21/{slug}"}
        for slug, name, kind, blurb, tag in PROJECTS
    ]

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dr. Abo 3tab — local-first AI</title>
<meta name="description" content="Local-first AI systems, autonomous agents, and tools that ship as files.">
<meta name="color-scheme" content="dark">
<style>
  *, *::before, *::after {{ box-sizing: border-box; }}
  :root {{
    --bg: #08090c;
    --ink: #f2efe9;
    --accent: #e8a33d;
    --muted: rgba(242,239,233,.55);
    --line: rgba(242,239,233,.14);
    --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    --serif: Georgia, "Iowan Old Style", "Times New Roman", serif;
    --mono: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  }}
  html {{ background: var(--bg); }}
  body {{
    margin: 0; min-height: 100vh; background: var(--bg); color: var(--ink);
    font-family: var(--sans); display: flex; justify-content: center;
    padding: 28px 20px 64px;
    transition: background .45s ease, color .45s ease;
  }}

  .shell {{ width: 100%; max-width: 1000px; }}

  /* ── toolbar ─────────────────────────────────────────────────────────── */
  .bar {{
    display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
    margin-bottom: 16px; font-size: 12px; letter-spacing: .12em;
    text-transform: uppercase;
  }}
  .bar .label {{ color: var(--muted); }}
  .swatches {{ display: flex; gap: 7px; }}
  .swatch {{
    width: 22px; height: 22px; border-radius: 50%; cursor: pointer; padding: 0;
    border: 1px solid rgba(255,255,255,.22); background: none; position: relative;
    transition: transform .18s ease, border-color .18s ease;
  }}
  .swatch:hover {{ transform: scale(1.14); }}
  .swatch[aria-pressed="true"] {{ border-color: var(--accent); box-shadow: 0 0 0 2px var(--bg), 0 0 0 3px var(--accent); }}
  .swatch span {{
    position: absolute; inset: 4px; border-radius: 50%; display: block;
  }}
  .spacer {{ flex: 1 1 auto; }}
  .btn {{
    font: inherit; font-size: 11px; letter-spacing: .1em; text-transform: uppercase;
    color: var(--ink); background: transparent; cursor: pointer;
    border: 1px solid var(--line); border-radius: 999px; padding: 7px 13px;
    transition: border-color .18s, color .18s, background .18s;
  }}
  .btn:hover, .btn:focus-visible {{ border-color: var(--accent); color: var(--accent); outline: none; }}
  .btn[aria-pressed="true"] {{ border-color: var(--accent); color: var(--accent); }}

  /* ── stage ───────────────────────────────────────────────────────────── */
  .stage {{ position: relative; border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }}
  .stage svg {{ display: block; width: 100%; height: auto; }}
  .glyph {{ cursor: pointer; }}
  .glyph-target {{ cursor: pointer; }}
  .stage.replaying svg .rise-a,
  .stage.replaying svg .rise-b,
  .stage.replaying svg .rise-c,
  .stage.replaying svg .row,
  .stage.replaying svg .stn {{ animation: none; }}
  .stage.replaying svg .rule-draw {{ animation: none; stroke-dasharray: none; }}

  /* hover affordance on project rows */
  .stage svg .row {{ transition: opacity .2s ease; }}
  .stage.hovering svg .row:not(.is-hot) {{ opacity: .38; }}

  /* ── footer ──────────────────────────────────────────────────────────── */
  .foot {{
    margin-top: 18px; display: flex; gap: 10px; flex-wrap: wrap;
    align-items: center; font-size: 13px;
  }}
  .foot a {{ color: var(--ink); text-decoration: none; border-bottom: 1px solid var(--line); padding-bottom: 1px; }}
  .foot a:hover {{ color: var(--accent); border-color: var(--accent); }}
  .hint {{ color: var(--muted); font-size: 12px; }}
  .kbd {{
    font-family: var(--mono); font-size: 11px; border: 1px solid var(--line);
    border-radius: 4px; padding: 1px 5px; color: var(--ink);
  }}
  .live {{
    margin-left: auto; display: inline-flex; align-items: center; gap: 7px;
    color: var(--muted); font-size: 11px; letter-spacing: .12em; text-transform: uppercase;
  }}
  .dot {{ width: 6px; height: 6px; border-radius: 50%; background: var(--accent); }}
  @media (prefers-reduced-motion: reduce) {{
    body {{ transition: none; }}
    .stage svg * {{ animation: none !important; }}
  }}
</style>
</head>
<body>
<div class="shell">
  <div class="bar">
    <span class="label">Theme</span>
    <div class="swatches" id="swatches" role="group" aria-label="Profile theme"></div>
    <span class="spacer"></span>
    <button class="btn" id="replay" type="button">Replay intro</button>
    <button class="btn" id="motion" type="button" aria-pressed="false">Reduce motion</button>
  </div>

  <div class="stage" id="stage"></div>

  <div class="foot">
    <span class="hint">
      press <span class="kbd">1</span>–<span class="kbd">5</span> to switch theme ·
      <span class="kbd">R</span> to replay · click a project to open it
    </span>
    <span class="live"><span class="dot"></span>live</span>
  </div>
  <div class="foot">
    <a href="mailto:mbm143105@gmail.com">send me a message</a>
    <a href="https://guns.lol/dr.abo3tab" target="_blank" rel="noopener noreferrer">guns.lol/dr.abo3tab</a>
    <a href="https://github.com/mafk21?tab=repositories" target="_blank" rel="noopener noreferrer">all repositories</a>
  </div>
</div>

<script type="application/json" id="cards">{json.dumps(data)}</script>
<script type="application/json" id="themes">{json.dumps(themes)}</script>
<script type="application/json" id="projects">{json.dumps(projects)}</script>
<script>
(function () {{
  "use strict";

  var cards    = JSON.parse(document.getElementById("cards").textContent);
  var themes   = JSON.parse(document.getElementById("themes").textContent);
  var projects = JSON.parse(document.getElementById("projects").textContent);
  var order    = {json.dumps(ORDER)};

  var stage    = document.getElementById("stage");
  var swatches = document.getElementById("swatches");
  var motionBtn= document.getElementById("motion");
  var replayBtn= document.getElementById("replay");

  /* matchMedia is not guaranteed (older browsers, embedded webviews, some
     file:// contexts) — degrade to "motion on" rather than throwing. */
  var reduceMotion = (function () {{
    try {{
      return !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
    }} catch (e) {{ return false; }}
  }})();

  function stored() {{
    try {{ return localStorage.getItem("profile-theme"); }} catch (e) {{ return null; }}
  }}
  function store(key) {{
    try {{ localStorage.setItem("profile-theme", key); }} catch (e) {{}}
  }}

  var active = (function () {{
    var fromHash = (location.hash || "").replace("#", "");
    if (order.indexOf(fromHash) !== -1) return fromHash;
    var s = stored();
    if (s && order.indexOf(s) !== -1) return s;
    return order[0];
  }})();

  /* ── painting ─────────────────────────────────────────────────────────── */

  function paintSwatches() {{
    swatches.innerHTML = "";
    order.forEach(function (key, i) {{
      var t = themes[key];
      var b = document.createElement("button");
      b.className = "swatch";
      b.type = "button";
      b.title = t.label + "  (" + (i + 1) + ")";
      b.setAttribute("aria-label", t.label);
      b.setAttribute("aria-pressed", key === active ? "true" : "false");
      b.style.background = t.bg;
      var dot = document.createElement("span");
      dot.style.background = t.accent;
      b.appendChild(dot);
      b.addEventListener("click", function () {{ setTheme(key); }});
      swatches.appendChild(b);
    }});
  }}

  function applyVars() {{
    var t = themes[active];
    document.documentElement.style.setProperty("--bg", t.bg);
    document.documentElement.style.setProperty("--accent", t.accent);
    document.documentElement.style.setProperty("--ink", t.ink);
  }}

  /* Project rows inside a card sit at fixed, increasing offsets. Find them by
     locating each project name, then group the nodes that belong to that row. */
  function wireProjects() {{
    var svg = stage.querySelector("svg");
    if (!svg) return;
    var texts = Array.prototype.slice.call(svg.querySelectorAll("text"));
    projects.forEach(function (p) {{
      var hit = texts.filter(function (t) {{ return t.textContent.trim() === p.name; }})[0];
      if (!hit) return;

      /* the row group is the nearest ancestor <g class="row"> */
      var row = hit.closest ? hit.closest("g.row") : null;
      if (row) row.classList.add("glyph-target");

      var target = row || hit;
      target.style.cursor = "pointer";
      target.addEventListener("click", function () {{
        window.open(p.url, "_blank", "noopener");
      }});
      target.addEventListener("mouseenter", function () {{
        stage.classList.add("hovering");
        if (row) row.classList.add("is-hot");
      }});
      target.addEventListener("mouseleave", function () {{
        stage.classList.remove("hovering");
        if (row) row.classList.remove("is-hot");
      }});
    }});
  }}

  function setTheme(key) {{
    if (order.indexOf(key) === -1) return;
    active = key;
    store(key);
    if (history.replaceState && location.protocol !== "file:") {{
      history.replaceState(null, "", "#" + key);
    }}
    applyVars();
    paintSwatches();
    stage.innerHTML = '<svg viewBox="0 0 1000 1610" xmlns="http://www.w3.org/2000/svg">'
                    + cards[key] + "</svg>";
    var svg = stage.querySelector("svg");
    svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", "Profile card, " + themes[key].label + " theme");
    if (reduceMotion) stage.classList.add("replaying");
    wireProjects();
  }}

  /* ── controls ─────────────────────────────────────────────────────────── */

  function replay() {{
    if (reduceMotion) return;
    var key = active;
    stage.classList.add("replaying");
    /* force a reflow, then repaint so every animation restarts from zero */
    void stage.offsetWidth;
    stage.innerHTML = "";
    stage.classList.remove("replaying");
    setTheme(key);
  }}

  replayBtn.addEventListener("click", replay);

  function setReduceMotion(on) {{
    reduceMotion = on;
    motionBtn.setAttribute("aria-pressed", on ? "true" : "false");
    motionBtn.textContent = on ? "Motion on" : "Reduce motion";
    if (on) {{
      stage.classList.add("replaying");
    }} else {{
      stage.classList.remove("replaying");
      replay();
    }}
  }}

  motionBtn.addEventListener("click", function () {{ setReduceMotion(!reduceMotion); }});

  document.addEventListener("keydown", function (e) {{
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var n = parseInt(e.key, 10);
    if (!isNaN(n) && n >= 1 && n <= order.length) {{ setTheme(order[n - 1]); return; }}
    if (e.key === "r" || e.key === "R") replay();
  }});

  window.addEventListener("hashchange", function () {{
    var k = (location.hash || "").replace("#", "");
    if (order.indexOf(k) !== -1 && k !== active) setTheme(k);
  }});

  /* ── boot ─────────────────────────────────────────────────────────────── */
  if (reduceMotion) {{
    motionBtn.setAttribute("aria-pressed", "true");
    motionBtn.textContent = "Motion on";
  }}
  setTheme(active);
}})();
</script>
</body>
</html>
"""

    OUT.write_text(html, encoding="utf-8")
    kb = OUT.stat().st_size / 1024
    print(f"wrote index.html  {kb:,.0f} KB  ({len(data)} cards, {len(projects)} projects)")


if __name__ == "__main__":
    main()
