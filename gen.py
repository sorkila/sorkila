import html, re
ART = """\
███████╗ ██████╗ ██████╗ ██╗  ██╗██╗██╗      █████╗
██╔════╝██╔═══██╗██╔══██╗██║ ██╔╝██║██║     ██╔══██╗
███████╗██║   ██║██████╔╝█████╔╝ ██║██║     ███████║
╚════██║██║   ██║██╔══██╗██╔═██╗ ██║██║     ██╔══██║
███████║╚██████╔╝██║  ██║██║  ██╗██║███████╗██║  ██║
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝""".split("\n")
COLS = max(len(l) for l in ART)
ART = [l.ljust(COLS) for l in ART]
TAG = "design and engineering, stockholm"

# ---------- A: static ----------
pad = COLS - len(TAG) - 2
rule = "─"*(pad//2) + " " + TAG + " " + "─"*(pad - pad//2)
open("A.md","w").write("```text\n" + "\n".join(l.rstrip() for l in ART) + "\n" + rule + "\n```\n")

# ---------- B: ansi (256-color warm gradient by row, shadow glyphs dim) ----------
rows = [223, 222, 221, 179, 178, 136]   # cream -> amber, xterm-256 indices
dim = 240
SH = set("╔═╗║╝╚")
def ansi_line(line, col):
    out, cur = "", None
    for ch in line:
        want = dim if ch in SH else col
        if want != cur:
            out += f"\x1b[38;5;{want}m"; cur = want
        out += ch
    return out + "\x1b[0m"
b = ["```ansi"] + [ansi_line(l.rstrip(), c) for l, c in zip(ART, rows)]
b.append(f"\x1b[38;5;{dim}m" + "─"*(pad//2) + f" \x1b[38;5;180m{TAG}\x1b[38;5;{dim}m " + "─"*(pad - pad//2) + "\x1b[0m")
b.append("```")
open("B.md","w").write("\n".join(b) + "\n")

# ---------- C: animated SVG ----------
CW, LH, FS = 11.0, 19, 18.5          # cell width, line height, font size
PADX, PADY = 24, 22
W = int(COLS*CW + 2*PADX)             # 620
ART_H = len(ART)*LH
TAG_Y = PADY + ART_H + 30
H = TAG_Y + 22
TCW = 8.3
TAGW = len(TAG)*TCW

def runs(line):
    # split into (text, is_shadow) runs so shadow glyphs get their own fill
    return [(m.group(0), m.group(0)[0] in SH) for m in re.finditer(r"[╔═╗║╝╚]+|[^╔═╗║╝╚]+", line)]

def build(theme):
    if theme == "dark":
        ink, shadow, gold, tag, cursor = "#e9e6df", "#57534a", "#e8cf8b", "#8d887c", "#c19a49"
    else:
        ink, shadow, gold, tag, cursor = "#1c1b18", "#b8b3a8", "#c19a49", "#6f6a60", "#c19a49"

    # ---- geometry: faces = merged rect runs, shadow = double hairlines (box-drawing, redrawn) ----
    CH = LH
    def cell(c, r): return PADX + c*CW, PADY + r*CH
    faces, shade = [], []
    for r, l in enumerate(ART):
        c = 0
        while c < COLS:
            if l[c] == "█":
                s = c
                while c < COLS and l[c] == "█": c += 1
                x, y = cell(s, r)
                faces.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{(c-s)*CW:.1f}" height="{CH}"/>')
            else:
                c += 1
    g = 2.2   # gap between the two hairlines
    for r, l in enumerate(ART):
        for c, ch in enumerate(l):
            if ch not in SH: continue
            x, y = cell(c, r); mx, my = x + CW/2, y + CH/2
            H_, V_ = ch in "═╔╗╚╝", ch in "║╔╗╚╝"
            if ch == "═":
                for d in (-g, g): shade.append(f'M{x:.1f} {my+d:.1f}h{CW:.1f}')
            elif ch == "║":
                for d in (-g, g): shade.append(f'M{mx+d:.1f} {y:.1f}v{CH}')
            else:
                # corner: outer and inner L-shapes
                sx = 1 if ch in "╔╚" else -1     # horizontal arm direction
                sy = 1 if ch in "╔╗" else -1     # vertical arm direction
                xe = x + CW if sx > 0 else x
                ye = y + CH if sy > 0 else y
                for d in (g, -g):               # d>0 outer, d<0 inner
                    ox, oy = mx - sx*d, my - sy*d
                    shade.append(f'M{xe:.1f} {oy:.1f}H{ox:.1f}V{ye:.1f}')
    art = (f'<g class="f">{"".join(faces)}</g>'
           f'<path class="s" d="{" ".join(shade)}"/>')

    # typing: discrete widths, one char per step, slightly uneven cadence
    n = len(TAG)
    vals = ";".join(f"{k*TCW:.1f}" for k in range(n+1))
    kt = [0.0]
    for k in range(1, n+1):
        kt.append(kt[-1] + (1.0 if TAG[k-1] != " " else 1.6))
    kt = [round(v/kt[-1], 4) for v in kt]
    kts = ";".join(str(v) for v in kt)
    cur_vals = ";".join(f"{PADX + k*TCW:.1f}" for k in range(n+1))
    TYPE_DUR, TYPE_BEGIN = 1.6, 1.15
    type_end = TYPE_BEGIN + TYPE_DUR

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="sorkila. {TAG}">
<style>
  text {{ font-family: ui-monospace, "SF Mono", Menlo, Consolas, "DejaVu Sans Mono", "Liberation Mono", monospace; font-size: {FS}px; }}
  .f {{ fill: url(#sheen); }}
  .s {{ fill: none; stroke: {shadow}; stroke-width: 1.2; stroke-linecap: butt; stroke-linejoin: miter; }}
  .tag {{ fill: {tag}; font-size: 13.5px; letter-spacing: 0.02em; }}
</style>
<defs>
  <!-- warm foil sheen: a narrow diagonal band of gold that sweeps the letter faces, then rests -->
  <linearGradient id="sheen" gradientUnits="userSpaceOnUse" gradientTransform="translate(-{W+40} 0)" x1="0" y1="0" x2="{W}" y2="{ART_H+PADY}">
    <stop offset="0" stop-color="{ink}"/>
    <stop offset="0.38" stop-color="{ink}"/>
    <stop offset="0.50" stop-color="{gold}"/>
    <stop offset="0.62" stop-color="{ink}"/>
    <stop offset="1" stop-color="{ink}"/>
    <animateTransform attributeName="gradientTransform" type="translate"
      values="-{W+40} 0; {W+40} 0; {W+40} 0" keyTimes="0; 0.28; 1"
      calcMode="spline" keySplines="0.45 0 0.55 1; 0 0 1 1"
      begin="2.3s" dur="7.5s" repeatCount="indefinite"/>
  </linearGradient>
  <clipPath id="wipe">
    <rect x="0" y="0" width="0" height="{PADY+ART_H+8}">
      <animate attributeName="width" from="0" to="{W}" begin="0.15s" dur="1.1s" fill="freeze"
        calcMode="spline" keySplines="0.16 1 0.3 1"/>
    </rect>
  </clipPath>
  <clipPath id="type">
    <rect x="{PADX}" y="{TAG_Y-16}" width="0" height="24">
      <animate attributeName="width" values="{vals}" keyTimes="{kts}" calcMode="discrete"
        begin="{TYPE_BEGIN}s" dur="{TYPE_DUR}s" fill="freeze"/>
    </rect>
  </clipPath>
</defs>

<g clip-path="url(#wipe)">
{art}
</g>
<!-- the printing edge: a gold hairline that leads the reveal and dies at the margin -->
<rect x="-2" y="{PADY-6}" width="2" height="{ART_H+12}" fill="{gold}" opacity="0.9">
  <animate attributeName="x" from="-2" to="{W}" begin="0.15s" dur="1.1s" fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1"/>
  <animate attributeName="opacity" from="0.9" to="0" begin="0.85s" dur="0.5s" fill="freeze"/>
</rect>

<g clip-path="url(#type)">
  <text class="tag" x="{PADX}" y="{TAG_Y}" textLength="{TAGW:.0f}" lengthAdjust="spacingAndGlyphs" xml:space="preserve">{TAG}</text>
</g>
<!-- block cursor: rides the typing, then blinks -->
<rect x="{PADX}" y="{TAG_Y-13}" width="{TCW-1:.1f}" height="15" fill="{cursor}" opacity="0">
  <animate attributeName="opacity" from="0" to="0.85" begin="{TYPE_BEGIN-0.25}s" dur="0.2s" fill="freeze"/>
  <animate attributeName="x" values="{cur_vals}" keyTimes="{kts}" calcMode="discrete" begin="{TYPE_BEGIN}s" dur="{TYPE_DUR}s" fill="freeze"/>
  <animate attributeName="opacity" values="0.85;0.85;0;0" keyTimes="0;0.5;0.5;1" begin="{type_end+0.4}s" dur="1.06s" repeatCount="indefinite"/>
</rect>
</svg>
'''

for t in ("dark", "light"):
    open(f"sorkila-{t}.svg","w").write(build(t))
open("C.md","w").write('''<picture>
  <source media="(prefers-color-scheme: dark)" srcset="sorkila-dark.svg">
  <img alt="sorkila. designer and ai tinkerer, stockholm" src="sorkila-light.svg" width="620">
</picture>
''')
print(W, H)
