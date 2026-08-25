# github.com/sorkila

Erik Nielsen's GitHub profile README. The companion site repo
(`~/Repositories/Sorkila`, sorkila.com) holds the design system this
borrows from; its CLAUDE.md has the full story.

## Files

- `README.md` — the profile. Deliberately minimal: the wordmark, three
  one-line product links, sorkila.com. No heading, no bio sentence (the
  sidebar bio and the typed tagline already say it). Keep it that way.
- `sorkila-dark.svg`, `sorkila-light.svg` — the animated wordmark, picked
  by a `<picture>` tag. GENERATED, do not hand-edit.
- `gen.py` — the generator (python 3, no dependencies). `python3 gen.py`
  rewrites both SVGs (it also emits `A.md`/`B.md`/`C.md`, the two rejected
  static variants and the picture snippet; ignore or delete them).

## The wordmark

Figlet "ANSI Shadow" redrawn as SVG geometry: merged rects for the block
faces, double hairlines for the `╔═╝` shadow. Geometry, not text, because
block glyphs render from the visitor's monospace font and showed seams.
SMIL animation, no JS (GitHub strips scripts but runs SVG animation inside
`<img>`):

- a gold printing edge wipes the name in left to right, ease
  `0.16 1 0.3 1` (the site's house ease), 1.1s
- the tagline types one cell at a time (discrete keyTimes, spaces linger)
  with an amber block cursor that rides the text, then blinks forever
- a diagonal foil sheen (narrow gold band in a userSpaceOnUse gradient,
  translated across) sweeps the faces every 7.5s, sweep ~2.1s, resting
  off-canvas between sweeps (it must start off-canvas or the K sits gold
  on load)

Palette: ink #e9e6df on the dark ground, #1c1b18 on light; gold #e8cf8b /
#c19a49; shadow hairlines #57534a / #b8b3a8. Tagline is the site subtitle,
"design and engineering, stockholm", lowercase.

## Changing it

1. Edit `TAG`, colors, or timings in `gen.py`, run `python3 gen.py`.
2. Bump `?v=` on BOTH image URLs in `README.md`. GitHub's image proxy and
   raw.githubusercontent.com cache by path for several minutes; without
   the bump the old SVG keeps playing.
3. Commit the SVGs and README together.

Preview before pushing: render `C.md`'s picture tag in a page with
Playwright WebKit (headless Chrome hangs on Erik's Mac), record light and
dark, and judge the motion in playback, not from a still.

An SVG in an `<img>` cannot read prefers-reduced-motion: keep every
motion slow and non-flashing. Copy voice, as on the site: short sentences,
no em dashes, no semicolons, wry not jokey.
