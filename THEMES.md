# Profile themes

Four complete profiles live in this repo. One is active; the rest are one command
away. Nothing here depends on a branch, a build step, or a third-party service —
every pixel is generated from `tools/make-themes.py`.

## The four

| | Theme | Background | Type | What moves |
| :--: | :-- | :-- | :-- | :-- |
| `01` | **Signal** | near-black `#08090c` | serif | the name is written out by a clip reveal with an amber write-head, then fills; amber rule draws under it; the graph answers with amber packets and slow orbit rings |
| `02` | **Swarm** | GitHub dark `#0d1117` | serif | node graph with packets travelling its edges, hub pulse, cursors drawing the page |
| `03` | **Typewriter** | terminal black `#0b0f14` | monospace | the name types itself, block caret blinks, scanline sweeps, captions rise in sequence |
| `04` | **Blueprint** | drafting navy `#0a1a2b` | sans | every rule draws itself left-to-right, dimension marks appear, labels rise in order |
| `05` | **Paper** | warm off-white `#f4efe5` | serif | name rises, "APPROVED · LOCAL ONLY" stamp lands with a rotate-and-settle, marks fade in |

Each theme carries the same written content — intro, six projects, principles,
links — and its own band + six project glyphs, so switching never leaves a
mismatched image behind.

## Switching

```bash
python3 tools/profile.py          # list, with the active one marked
python3 tools/profile.py 02       # by number
python3 tools/profile.py paper    # by name
```

That rewrites the art references in `README.md` and stamps the active theme in a
comment. Commit `README.md` and the profile changes.

## Why they look the same on light and dark GitHub

Every theme paints its own background inside the SVG. That means no
`prefers-color-scheme` juggling, no second copy of each asset, and no risk of
pale art vanishing on a pale page. The trade-off is deliberate: the profile is
always *the theme's* colour, not GitHub's.

## Adding another

1. Add a `Theme` to `THEMES` in `tools/artlib.py` and its key to `ORDER`.
2. Add a `banner_<name>()` to `BANNERS` in `tools/make-themes.py`.
3. `python3 tools/make-themes.py`, then `python3 tools/profile.py <name>`.

`band()` and `glyph()` are shared, so a new theme only needs a background, an
ink colour, an accent, and a banner.

## Motion notes

- Animations are **CSS `@keyframes`** inside the SVG. This is what the
  contribution snake (`Platane/snk`) and `capsule-render` do — both are known to
  animate on GitHub. SFML/SMIL is used only where a shape must travel a path.
- Every animated element's *resting* state is its finished state, so if animation
  is stripped the art still reads correctly rather than appearing half-drawn.
- Each file ends with a `prefers-reduced-motion` block that disables motion.

## Credit where it is due

The approach was chosen by reading the output of the tools people recommend
rather than their descriptions:

- **[DenverCoder1/readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg)** — the only widely used way to animate *text*; it emits SMIL `<animate>`.
- **[Platane/snk](https://github.com/Platane/snk)** — the contribution snake; generates CSS `@keyframes`.
- **[kyechan99/capsule-render](https://github.com/kyechan99/capsule-render)** — wave headers with `fadeIn` / `scaleIn` / `twinkling`.
