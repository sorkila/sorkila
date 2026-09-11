# github.com/sorkila

Erik Nielsen's GitHub profile README. The companion site repo
(`~/Repositories/Sorkila`, sorkila.com) holds the design system this
borrows from; its CLAUDE.md has the full story.

## Files

- `README.md` — the profile. "The signature" (chosen 2026-09-11 from nine
  directions, the brief was "even more clean and simple"): the site's hero
  as an image, one centered line of five product links separated by middle
  dots, then sorkila.com. No heading, no bio sentence, no bullets. The
  sidebar already says the name and the handle; the README adds only the
  typeface and the products. Keep it this small.
- `sorkila-dark.svg`, `sorkila-light.svg` — the hero, picked by a
  `<picture>` tag. GENERATED, do not hand-edit.
- `gen.py` — the generator. `pip install uharfbuzz fonttools`, then
  `python3 gen.py` rewrites both SVGs. It fetches Pirata One and Literata
  from github.com/google/fonts into `fonts/` (gitignored) on first run.

## The hero

"Erik Nielsen" in Pirata One (66px) over "Design and engineering,
Stockholm" in Literata (17px, instanced at wght 400 / opsz 14), the same
pair as every site page. Both lines are shaped with HarfBuzz (kerning on)
and OUTLINED TO PATHS. Geometry, not text, because GitHub's image proxy
blocks every fetch from inside an SVG, so no webfont could load, and an
embedded font would still be at the mercy of the visitor's renderer.
620x150, about 33 KB per theme.

One motion, then still. Nothing loops:

- a clip wipes the name in left to right on the house ease
  (`0.16 1 0.3 1`), 1.1s from 0.15s, led by a 2px gold printing edge that
  fades at the far margin
- the subtitle rises 4px into place and fades in from 0.75s, 0.7s

Every animation has `begin="0s"` and HOLDS its hidden value in `keyTimes`
until its cue. A `begin` delay shows the base frame for that long first:
the finished name flashed for 150ms before wiping in (seen in the frame
sheet 2026-09-11, fixed the same hour). The base attributes ARE the
finished frame (clip at full width, opacity 1) on purpose: a renderer that
never runs SMIL (Firefox has frozen animated SVGs with embedded images)
shows the settled hero, not an empty box.

Palette: ink `#e8e6e1` on dark / `#1a1a1a` on light (the site's --text),
subtitle `#9a9590` / `#7a756d` (--text-secondary), gold `#e8cf8b` /
`#c19a49`.

## Changing it

1. Edit `NAME`, `SUB`, sizes, or timings in `gen.py`, run `python3 gen.py`.
2. Bump `?v=` on BOTH image URLs in `README.md`. GitHub's image proxy and
   raw.githubusercontent.com cache by path for several minutes; without
   the bump the old SVG keeps playing.
3. Commit the SVGs and README together.

Preview before pushing: serve a page with the README's markup on GitHub's
grounds (#ffffff / #0d1117) with Playwright WebKit (headless Chrome hangs
on Erik's Mac), record light and dark with `recordVideo`, extract frames
at 8 fps with homebrew ffmpeg, and judge the motion in the frame sheet,
not from a still. Erik reviews recordings on the Desktop before anything
ships.

An SVG in an `<img>` cannot read prefers-reduced-motion: keep every
motion slow and non-flashing, and never add a loop. Copy voice, as on the
site: short sentences, no em dashes, no semicolons, wry not jokey.

## History

- 2026-08-25: figlet "ANSI Shadow" wordmark redrawn as SVG geometry, typed
  tagline, looping foil sheen. Replaced 2026-09-11 because it read as a
  terminal, not as the site.
