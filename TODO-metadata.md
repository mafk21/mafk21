# Copy-paste values for the things only the account owner can change

The API token available to the agent is repo-scoped, so descriptions, topics,
the profile bio and pinned repositories all return 403. These are the exact
values to paste.

## Profile → About (top right of your profile page)

**Bio** (160 char limit, this is 148):

```
Building local-first AI: systems that run on your machine and hand back a file you own. JARVIS, Swarmcraft, OSINT Monster.
```

**Website:** `https://guns.lol/dr.abo3tab`

**Location / Company:** optional, currently empty.

## Pinned repositories — pin these six, in this order

1. `jarvis` — most starred (8★), your strongest project. **Must be first.**
2. `swarmcraft` — polished README, 10 topics already
3. `OSINT`
4. `NEXUS`
5. `connect-everything`
6. `PowerPoint-skill`

## Repository descriptions + topics

### jarvis
Description:
```
A local-first AI that sees your screen, speaks, remembers, and operates your computer — voice, vision, computer control, durable memory, long-running work. Windows, macOS, Linux.
```
Homepage: `https://jarvis-khaki-eight.vercel.app/docs/`
Topics:
```
ai, local-first, computer-use, voice-assistant, screen-vision,
autonomous-agents, python, llm, anthropic, privacy
```

### OSINT
Description:
```
Autonomous OSINT and DFIR suite: 45+ passive collectors, offline forensic decoders, graph studio and 760 verified tools. Zero pip dependencies, zero API keys.
```
Topics:
```
osint, dfir, recon, forensics, threat-intelligence, python,
security-tools, stix, mcp, graph
```

### NEXUS
Description:
```
A desktop that reshapes itself per task — categories, setups and activation, each with its own wallpaper, accent colour and shortcuts. Electron.
```
Topics:
```
electron, desktop-app, productivity, customisation, javascript, windows
```

### connect-everything
Description:
```
534 hand-curated resources across 504 domains with 64 controlled tags. No accounts, no tracking, no ads — every card is one click out.
```
Homepage: `https://connect-everything-tau.vercel.app`
Topics:
```
awesome-list, curated, astro, resources, no-tracking, directory
```

### PowerPoint-skill
Description:
```
An AI skill for professional decks: Morph transitions, 13 layout blueprints, an Arabic/RTL path, and a queried 238-record SQLite database of techniques.
```
Topics:
```
powerpoint, presentations, ai-skill, python-pptx, morph-transition, rtl, arabic
```

### swarmcraft (already good — no change needed)
10 topics already set: `ai, canvas, design-tools, gemini, generative-ai, local-first, no-backend, react, typescript, website-builder`

## Also worth doing

- **Rename `OSINT`.** A repo named `OSINT` cannot be searched or discovered.
  `osint-monster` matches what the README already calls it. GitHub redirects the
  old URL, so nothing breaks.
- Settings → Pages: set to **None** if you enabled it while the interactive
  page existed.
