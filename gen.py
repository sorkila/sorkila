"""The signature: sorkila.com's hero as one small SVG per theme.

"Erik Nielsen" in Pirata One and "Design and engineering, Stockholm" in
Literata, shaped with HarfBuzz and outlined to paths, so nothing depends on
the visitor's fonts and nothing is fetched from inside the SVG (GitHub's
image proxy forbids it). One motion: a gold printing edge wipes the name in
on the house ease, the subtitle rises after it. Then still. Nothing loops.

    pip install uharfbuzz fonttools
    python3 gen.py

Fonts are fetched from github.com/google/fonts into ./fonts on first run.
"""
import io, os, urllib.request
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.varLib.instancer import instantiateVariableFont

NAME = "Erik Nielsen"
SUB = "Design and engineering, Stockholm"
W = 620                    # matches width="620" in the README
NAME_PX = 66
SUB_PX = 17
GAP = 38                   # name baseline to subtitle baseline
PAD_TOP, PAD_BOT = 30, 26
EASE = "0.16 1 0.3 1"      # the house ease

FONTS = {
    "pirata": ("fonts/PirataOne-Regular.ttf",
               "https://github.com/google/fonts/raw/main/ofl/pirataone/PirataOne-Regular.ttf"),
    "literata": ("fonts/Literata.ttf",
                 "https://github.com/google/fonts/raw/main/ofl/literata/Literata%5Bopsz%2Cwght%5D.ttf"),
}

THEMES = {
    # ink and secondary are the site's --text / --text-secondary; gold is the about card's foil peak
    "dark":  dict(ink="#e8e6e1", sub="#9a9590", gold="#e8cf8b"),
    "light": dict(ink="#1a1a1a", sub="#7a756d", gold="#c19a49"),
}


def fetch(key):
    path, url = FONTS[key]
    if not os.path.exists(path):
        os.makedirs("fonts", exist_ok=True)
        urllib.request.urlretrieve(url, path)
    return path


def font_bytes(path, axes=None):
    tt = TTFont(path)
    if axes:
        tt = instantiateVariableFont(tt, axes)
    buf = io.BytesIO()
    tt.save(buf)
    return buf.getvalue(), tt


def outline(text, blob, tt, px, x, y):
    """Shape text with HarfBuzz (kerning on) and return (path d, ink bounds)."""
    face = hb.Face(blob)
    font = hb.Font(face)
    upm = face.upem
    font.scale = (upm, upm)
    b = hb.Buffer()
    b.add_str(text)
    b.guess_segment_properties()
    hb.shape(font, b, {"kern": True, "liga": True})
    glyphs = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    s = px / upm
    pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:.2f}")
    bounds = BoundsPen(glyphs)
    cx = 0
    for info, pos in zip(b.glyph_infos, b.glyph_positions):
        gname = order[info.codepoint]
        gx = x + (cx + pos.x_offset) * s
        gy = y - pos.y_offset * s
        t = (s, 0, 0, -s, gx, gy)
        glyphs[gname].draw(TransformPen(pen, t))
        glyphs[gname].draw(TransformPen(bounds, t))
        cx += pos.x_advance
    return pen.getCommands(), bounds.bounds, cx * s


def build(theme, name_d, sub_d, name_box, edge_y0, edge_h, H):
    c = THEMES[theme]
    x0, y0, x1, y1 = name_box
    clip_x, clip_w = x0 - 6, (x1 - x0) + 12
    # every animation begins at 0s and HOLDS its hidden value until its cue: a begin= delay would
    # show the base (finished) frame for that long first, a flash of the answer before the reveal
    WIPE_BEGIN, WIPE_DUR = 0.15, 1.1
    SUB_BEGIN, SUB_DUR = 0.75, 0.7
    WIPE_END, SUB_END = WIPE_BEGIN + WIPE_DUR, SUB_BEGIN + SUB_DUR
    k_wipe = f"{WIPE_BEGIN / WIPE_END:.4f}"
    k_edge_on = f"{(WIPE_BEGIN + 0.06) / (WIPE_END + 0.15):.4f}"
    k_sub = f"{SUB_BEGIN / SUB_END:.4f}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{NAME}. {SUB}.">
<defs>
  <!-- the wipe: base width is the full name, so a frozen renderer still shows the finished frame -->
  <clipPath id="wipe">
    <rect x="{clip_x:.1f}" y="0" width="{clip_w:.1f}" height="{H}">
      <animate attributeName="width" values="0;0;{clip_w:.1f}" keyTimes="0;{k_wipe};1" begin="0s" dur="{WIPE_END}s" fill="freeze"
        calcMode="spline" keySplines="0 0 1 1;{EASE}"/>
    </rect>
  </clipPath>
</defs>
<g clip-path="url(#wipe)">
  <path fill="{c['ink']}" d="{name_d}"/>
</g>
<!-- the printing edge: a gold hairline leads the reveal and dies at the far margin -->
<rect x="{clip_x:.1f}" y="{edge_y0:.1f}" width="2" height="{edge_h:.1f}" fill="{c['gold']}" opacity="0">
  <animate attributeName="x" values="{clip_x:.1f};{clip_x:.1f};{clip_x+clip_w:.1f}" keyTimes="0;{k_wipe};1" begin="0s" dur="{WIPE_END}s" fill="freeze" calcMode="spline" keySplines="0 0 1 1;{EASE}"/>
  <animate attributeName="opacity" values="0;0;0.9;0.9;0" keyTimes="0;{k_wipe};{k_edge_on};0.62;1" begin="0s" dur="{WIPE_END+0.15}s" fill="freeze"/>
</rect>
<!-- the subtitle rises 4px into place after the name has landed -->
<g fill="{c['sub']}">
  <path d="{sub_d}">
    <animate attributeName="opacity" values="0;0;1" keyTimes="0;{k_sub};1" begin="0s" dur="{SUB_END}s" fill="freeze" calcMode="spline" keySplines="0 0 1 1;{EASE}"/>
    <animateTransform attributeName="transform" type="translate" values="0 4;0 4;0 0" keyTimes="0;{k_sub};1" begin="0s" dur="{SUB_END}s" fill="freeze" calcMode="spline" keySplines="0 0 1 1;{EASE}"/>
  </path>
</g>
</svg>
'''


def main():
    pirata_blob, pirata = font_bytes(fetch("pirata"))
    literata_blob, literata = font_bytes(fetch("literata"), {"wght": 400, "opsz": 14})

    # shape once at x=0 to measure, then center
    _, nb, name_adv = outline(NAME, pirata_blob, pirata, NAME_PX, 0, 0)
    _, sb, sub_adv = outline(SUB, literata_blob, literata, SUB_PX, 0, 0)
    name_x = (W - (nb[2] - nb[0])) / 2 - nb[0]
    sub_x = (W - (sb[2] - sb[0])) / 2 - sb[0]
    name_y = PAD_TOP - nb[1]                  # top of the tallest glyph sits at PAD_TOP
    sub_y = name_y + GAP
    name_d, name_box, _ = outline(NAME, pirata_blob, pirata, NAME_PX, name_x, name_y)
    sub_d, sub_box, _ = outline(SUB, literata_blob, literata, SUB_PX, sub_x, sub_y)
    H = round(sub_box[3] + PAD_BOT)
    edge_y0, edge_h = name_box[1] - 6, (name_box[3] - name_box[1]) + 12

    for theme in THEMES:
        svg = build(theme, name_d, sub_d, name_box, edge_y0, edge_h, H)
        open(f"sorkila-{theme}.svg", "w").write(svg)
        print(theme, f"{len(svg)/1024:.1f} KB", f"{W}x{H}")


if __name__ == "__main__":
    main()
