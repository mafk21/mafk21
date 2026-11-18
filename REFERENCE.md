# Animation reference set

Profiles and tools whose motion is worth copying, verified by reading their
actual SVG output rather than their descriptions.

| Repo | Stars | What actually animates | Technique |
| :-- | --: | :-- | :-- |
| [DenverCoder1/readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg) | 9.5k | text — types and deletes | SMIL `<animate>` |
| [Platane/snk](https://github.com/Platane/snk) | 6.2k | contribution grid | CSS `@keyframes` |
| [kyechan99/capsule-render](https://github.com/kyechan99/capsule-render) | 1.9k | header gradients + text | CSS `@keyframes` (fadeIn, scaleIn, twinkling) |
| [SP-XD/SP-XD](https://github.com/SP-XD/SP-XD) | 95 | eight GIF icons | GIF (92 KB – 1.7 MB each) |
| [thmsgbrt/thmsgbrt](https://github.com/thmsgbrt/thmsgbrt) | 540 | one small GIF | GIF |
| [DenverCoder1/DenverCoder1](https://github.com/DenverCoder1/DenverCoder1) | 749 | typing line + 21 live cards | mixed |
| [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats) | 79.8k | nothing — static cards | static SVG |
| [lowlighter/metrics](https://github.com/lowlighter/metrics) | 17.5k | nothing — static infographic | static SVG |

## Two findings worth keeping

**Andrew6rant's terminal banner is not animated.** [Andrew6rant/Andrew6rant](https://github.com/Andrew6rant/Andrew6rant)
is the most-copied profile graphic on GitHub; its `dark_mode.svg` contains zero
animation tags and no `@keyframes`. It is a static SVG that reads as animated.

**No widely used profile animates body text.** The only real exception is
readme-typing-svg, which does it with SMIL. Everything else that "feels active"
moves images, not words.
