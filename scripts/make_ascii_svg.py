#!/usr/bin/env python3
"""
Convert data/source-prepped.png -> avi-ascii.svg
Usage: python scripts/make_ascii_svg.py [--cols N]
"""
import sys
from pathlib import Path
from PIL import Image
import math

RAMP = " .`:-=+*cs#%@"
FONT_SIZE = 12
FONT_FAMILY = "DejaVu Sans Mono, monospace"
OUT = "avi-ascii.svg"

def img_to_chars(img, cols=100):
    w, h = img.size
    # character aspect ratio correction
    char_w, char_h = 1.0, 2.2  # tweak: characters are taller; this compresses height
    new_w = cols
    new_h = int((h / w) * cols * (char_w / char_h))
    if new_h < 8:
        new_h = 8
    img = img.convert("L").resize((new_w, new_h), Image.LANCZOS)
    px = img.load()
    lines = []
    ramp_len = len(RAMP)
    for y in range(new_h):
        row = []
        for x in range(new_w):
            b = px[x, y] / 255.0
            idx = int((1.0 - b) * (ramp_len - 1))
            row.append(RAMP[idx])
        lines.append("".join(row))
    return lines, new_w, new_h

def make_svg(lines, cols, rows, out_path):
    char_w_px = FONT_SIZE * 0.6
    char_h_px = FONT_SIZE * 1.2
    svg_w = int(cols * char_w_px)
    svg_h = int(rows * char_h_px) + 8
    fill = "#c9d1d9"  # light gray
    # build rows with clipPath + SMIL animate on rect width
    rows_svg = []
    for i, line in enumerate(lines):
        y = int((i + 1) * char_h_px)
        clip_id = f"clip{i}"
        # animate width from 0 to full
        rect_w = svg_w
        begin = f"{i * 0.06}s"
        rows_svg.append(f'''
  <clipPath id="{clip_id}"><rect x="0" y="{y - int(char_h_px)}" width="0" height="{int(char_h_px)}">
    <animate attributeName="width" from="0" to="{rect_w}" dur="0.9s" begin="{begin}" fill="freeze" />
  </rect></clipPath>
  <text x="2" y="{y}" font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}" fill="{fill}" clip-path="url(#{clip_id})">{line}</text>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">
  <rect width="100%" height="100%" fill="#0b0b0b"/>
  {"".join(rows_svg)}
</svg>'''
    Path(out_path).write_text(svg, encoding="utf-8")
    print("Wrote", out_path)

if __name__ == "__main__":
    Path("data").mkdir(parents=True, exist_ok=True)
    cols = 100
    if len(sys.argv) > 1:
        try:
            cols = int(sys.argv[1])
        except:
            pass
    src = Path("data/source-prepped.png")
    if not src.exists():
        print("Missing", src, "- run scripts/prep_photo.py first")
        sys.exit(1)
    img = Image.open(src)
    lines, c, r = img_to_chars(img, cols=cols)
    make_svg(lines, c, r, OUT)