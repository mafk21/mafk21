# Profile themes

The profile is **one animated card** — a single 1000 × 1610 SVG holding the
masthead, the build-flow band, all six projects, the principles, the toolbox and
the contact links. Five themes are built; one is active.

```bash
python3 tools/profile.py          # list, active marked
python3 tools/profile.py 04       # switch by number
python3 tools/profile.py paper    # switch by name
```

Switching rewrites one `src`/`srcset` pair in `README.md`. Commit it and the
profile changes.

## The five

| | Theme | Ground | Accent | Type |
| :--: | :-- | :-- | :-- | :-- |
| `01` | **Signal** | near-black `#08090c` | amber `#e8a33d` | serif |
| `02` | **Swarm** | GitHub dark `#0d1117` | sand `#d9b98a` | serif |
| `03` | **Typewriter** | terminal black `#0b0f14` | green `#7ee787` | monospace |
| `04` | **Blueprint** | drafting navy `#0a1a2b` | azure `#4cc2ff` | sans |
| `05` | **Paper** | warm off-white `#f4efe5` | rust `#a8441f` | serif |

## Why one card

A stack of images reflows unpredictably: GitHub controls the column width, so
three separate images never line up the way you composed them. One file means
the composition is fixed, the theme is unmistakable, and every element can
animate on a shared timeline.

Text stays as SVG `<text>`, so it is sharp at any width and selectable, rather
than baked into pixels.

## What animates

On the card: the name is written out by a clip reveal with a write-head that
fades once it lands · an accent rule draws underneath · the kicker and status
line rise · stations and their labels stagger in · route packets travel between
stations · every project row rises in sequence · glyphs animate on their own
loops · the node graph carries packets and an orbiting ring.

Motion is **CSS `@keyframes`** — the technique the contribution snake
(`Platane/snk`) and `capsule-render` use in production on GitHub. SMIL is used
only where a dot must travel a path.

Every animated element **rests in its finished state**, so if a viewer strips
animation the card is still complete, never half-drawn. Each file ends with a
`prefers-reduced-motion` block.

## Building

```bash
python3 tools/make-card.py       # the five cards
python3 tools/make-banners.py    # the five standalone mastheads, if you want one
```

`tools/artlib.py` holds the palettes, the shared copy, and the drawing
primitives. Adding a theme means adding a `Theme` to `THEMES`, its key to
`ORDER`, and a `banner_<name>()` to `tools/make-banners.py`.

## Note for future edits

The theme marker in `README.md` is an HTML comment and must stay one. An earlier
version wrote `<-- theme-note -->text<!-- /theme-note -->`, which put the text
*outside* the comment — so a sentence about the theme rendered as body copy on
the live profile. Anything written there must sit inside a single `<!-- -->`.
