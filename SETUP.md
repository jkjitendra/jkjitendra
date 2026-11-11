# GitHub profile deployment — @jkjitendra

The package is a complete `jkjitendra/jkjitendra` repository drop-in. It uses **GitHub README-compatible SVGs**, not JavaScript or embedded HTML applications.

## Included files

- `README.md` — final profile markup with verified portfolio/project links and resume-based information.
- `assets/network.svg` — animated center-logo pulse + inward-moving request bubbles + project links visualized as a map. Project names appear **away from** the pulse radius; individual clickable repository links are below the illustration in `README.md` because GitHub's Markdown image embedding isn't an interactive map.
- `assets/jk-logo.png` — the new custom blue-and-gold JK logo uploaded by you. It is trimmed and embedded inside the SVGs so there are no external image dependencies.
- `assets/moons.svg` — four celestial project cards.
- `assets/terminal.svg` — profile terminal and animated cursor.
- `assets/stack.svg` — full resume-based technology display.
- `assets/header.svg` — animated matching header.
- `assets/showcase.svg` — currently selected daily network/terminal artwork.
- `scripts/rotate_showcase.py` — day-based switcher; uses timezone `Asia/Kolkata`.
- `.github/workflows/rotate-profile.yml` — Github Action that regenerates the daily showcase and changes the image URL cache key.
- `scripts/build_assets.py` — optional SVG asset rebuilding tool (requires Pillow, an optional dev dependency). `rotate_showcase.py` requires only Python's standard library.

## Installation (recommended)

1. Clone your existing [profile repository](https://github.com/jkjitendra/jkjitendra) locally:
   ```bash
   git clone https://github.com/jkjitendra/jkjitendra.git
   cd jkjitendra
   ```
2. Copy **the contents of this package**, including hidden `.github/`, into the cloned repo. Replace the old `README.md`. To preserve other existing files, don't delete them unnecessarily.
3. Commit and push:
   ```bash
   git add README.md assets scripts .github/workflows/rotate-profile.yml
   git commit -m "feat: add animated GitHub engineering profile"
   git push origin main
   ```
4. Open **Repository → Actions → Rotate GitHub profile showcase → Run workflow** once. Confirm the workflow has permission to push content. If it's blocked, set **Settings → Actions → General → Workflow permissions → Read and write permissions** (repository policy permitting). The workflow also explicitly declares `contents: write`.
5. View <https://github.com/jkjitendra>. If a previous image appears due to GitHub's Camo image proxy, reload after the new commit propagates. The action changes the URL's date parameter daily to minimize caching problems.

## Exact alternation

- Anchor: **2026-11-11** (Asia/Kolkata) is network day.
- **2026-11-12** is developer terminal day.
- **2026-11-13** is network day, and the pattern continues.
- Schedule: **18:33 UTC / 00:03 IST** daily, best-effort. GitHub may delay or drop a scheduled job during load. This means the change may not happen exactly at midnight.
- The README's technology table remains visible every day. On **network days**, the developer terminal appears **below the featured project cards**; on **terminal days**, the developer terminal replaces the network in the main showcase and is hidden from the lower section to prevent duplication.

Run locally for a specific day:
```bash
python3 scripts/rotate_showcase.py --date 2026-11-12
python3 scripts/rotate_showcase.py --date 2026-11-13
```
The script updates `assets/showcase.svg`, the versioned image URL, and the marked lower terminal section in `README.md`. Leave `STATIC_TERMINAL_START`/`STATIC_TERMINAL_END` comments intact.

## Motion and GitHub limitations

- GitHub profile READMEs **cannot execute JavaScript**. The map uses SVG-native `<animate>` and `<animateMotion>` elements, which work when the browser and GitHub image rendering support SVG animation. Static SVG previews remain usable.
- Pulses grow from radius 62 to 98 units, fade to transparent and restart. Adjacent project labels are positioned outside this ring.
- Request bubbles travel on curved SVG paths from project nodes into the center. Paths have different durations and start offsets to avoid synchronized movement.
- You cannot click **each** inner SVG map node when the SVG is embedded as a normal README image. The real repository links are provided directly below the moon cards.
- The project network includes **DrostScope**, labeled "IN DEVELOPMENT", rather than claiming its repository is public.
- The map is a **visual representation**, not real-time server or repository traffic. The tiny bubbles do **not** call GitHub, backend APIs or external sites.

## Optional edits

- Edit project positions/titles and colors in `scripts/build_assets.py`, then run `python3 scripts/build_assets.py` after installing `Pillow` (`python3 -m pip install Pillow`). The `jk-logo.png` asset is preserved.
- To disable alternation, disable the workflow and replace `assets/showcase.svg` with whichever SVG you prefer. If you make manual README changes, keep the showcase image URL and the `STATIC_TERMINAL_START`/`STATIC_TERMINAL_END` comments recognizable to the rotation script. To change the lower terminal block, edit `TERMINAL_BELOW_PROJECTS` in `scripts/rotate_showcase.py`.
- To link other repositories, edit the Markdown project links below the graphic. Public projects and employer/private features should be described appropriately.

The illustrated tech stack from the third reference image remains available at `assets/stack.svg` for use in the future, but is **not** in the alternating showcase.
