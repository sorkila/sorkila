# Sólhvarf: the rebirth merch

Merch for Simployer's product and tech team. The entire product was burned
down and rebuilt. Solstice is the new design system, live, built by Erik.
The shirt is the record that came out, not a tour announcement.

Internal only: designers and engineers who get the reference. The logo may
be unreadable. Everything else must not be.

Erik renders in Grok Imagine. Claude is the AD. This folder is the handoff.

## Files

- `board.html` — the concept board, nine concepts with placement schematics,
  specs, AD notes, field notes from real black metal bands, and a prompt
  pack. Open it in a browser. Also published at
  https://claude.ai/artifact/E7LFGhBtW46PYCxFEev4j9 (same content, private).
- `prompts.md` — every Grok prompt as plain text, four per concept, plus the
  tracklist in three languages. GENERATED from `board.html` by
  `extract-prompts.js`; edit the board and regenerate, never both.
- `extract-prompts.js` — the generator.
  `node merch/extract-prompts.js merch/board.html merch/prompts.md`
- `inspo/colleague-render.png` — the colleague's Grok render that started
  it: "Gjenfødt", Mørketid / Solverv, the Simpløyer imprint. The sun in it
  is a wheel. Ours is a disc.

## The lore (decided)

- Band: **Sólhvarf**. Old Norse for solstice, "sun's turn", attested in
  Cleasby-Vigfusson from Grettis saga.
- Album: **Gjenfødt** (Norwegian, "reborn"). The colleague's word.
- Sides: **Mørketid** (the dark time, the old product) / **Solverv** (the turn).
- Imprint: **Simpløyer MMXXVI**, small, back only. The only place the company appears.
- Alt names: Endrborinn (Old Norse "born again", used in the Edda of Helgi;
  confirm spelling with a Norse reader before print), Återfödd (Swedish,
  for the Stockholm concept only).
- Tracklist: eight tracks, side one burns, side two builds. See `prompts.md`.
  Swap any title for a truer one from the team.

## Three directing rules

1. One unreadable thing per shirt. The logo can be a thicket; title,
   tracklist and imprint stay legible (Szpajdel's own rule).
2. The sun is a disc, never a wheel. Half-sunk on a ridge, thin rays upward
   only. A closed wheel of bent spokes is the sonnenrad. Never.
3. The lyrics are true. Every title is something the team did. No puns.

## Palette and type

From the sorkila design system (see `../gen.py`): bone `#e8e6e1` (the
site's ink), gold `#e8cf8b` (the foil peak, metallic ink on the sun disc
only), oxblood `#9a2626` (the one new colour, Uppland runestone paint).
Pirata One for display, Literata for everything that must be read. One
accent per shirt, never two.

## The nine concepts, one line each

1. **Sólhvarf** — the signature. Birch-branch logo, gold sun on a ridge,
   the record on the back. Render first.
2. **Endrborinn** — 1992 xerox demo tape. One ink, cheapest, most credible.
3. **Mørketid** — no logo, typeset tracklist high on the back. The Tuesday shirt.
4. **Solvarv** — the sun drawn from Solstice's real token values. Needs the
   spacing and type scale from the system.
5. **Runsten** — Uppland runestone on the back with the team's names in
   Younger Futhark. Needs names signed off and a rune-literate transliteration.
6. **Brenn** — burning dead tree in Doré etching, birch shoots at the roots.
7. **Återfödd** — Stockholm death metal, acid green, "Cut at Sunlight".
8. **Turné** — longsleeve, rebuilt modules as tour dates. Needs the real
   module list and launch months.
9. **Jól** — ecru cotton, one charcoal sun, released 21 December. Also the
   beanie and patch.

## What only Erik can supply

- Module names and launch months for 08.
- Team names (or the release commit hash) for 05.
- Solstice's spacing and type scale values for 04, and its UI typeface name.
- A look at mjolksyra.club, which was blocked from the cloud session.
  Fold its voice into the copy if it earns it.

## Workflow

1. Copy a prompt from `prompts.md` (start with Sólhvarf, art only, 3:4).
   Quality mode, four generations, keep one.
2. Fix a misspelled logo with the edit prompt at the top of `prompts.md`,
   one change per edit. Reject anything with a skull, pentagram, inverted
   cross, sun wheel, horned helmet or a recognisable band logo.
3. Tracklist, token legend and sleeve text never render: composite real
   Literata over an art-only render in Figma.
4. Save keepers to `merch/renders/<concept>/` (gitignored until chosen).
5. Update `board.html` as decisions land, then
   `node merch/extract-prompts.js merch/board.html merch/prompts.md`.

## Do not

No sonnenrad, black sun, wolfsangel or othala. No inverted crosses,
pentagrams or goat heads. No lifted band logos or fonts. No pun shirts.
No company logo on the front.

## Production

Oversized boxy heavyweight 240 to 250 gsm, garment-dyed washed black.
Water-based or discharge print, bone base ink, one accent. Metallic gold
on the sun disc only. XS to 3XL. Count the team, add 20 percent, order once.
