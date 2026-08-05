#!/usr/bin/env python3
"""
Generate a simple neofetch-style SVG info card.
Usage: python scripts/make_info_card.py
Set env STATIC=1 to output a frozen (non-animated) frame.
"""
import os
from pathlib import Path

OUT = "info-card.svg"
LINES = [
    ("Now", "Open-source tinkerer"),
    ("Prev", "SRE & platform"),
    ("Stack", "Python • GitHub Actions • SVG"),
    ("Highlights", "ASCII art, live heatmap, no JS")
]

def make_svg(lines, out_path, static=False):
    w, h = 490, 300
    title = "avi@github"
    items = []
    base_y = 48
    for i, (k, v) in enumerate(lines):
        y = base_y + i * 44
        if static:
            anim = ''
        else:
            begin = f"{i * 0.12}s"
            anim = f'''<g transform="translate(0,0)" opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{begin}" fill="freeze"/>
      <text x="18" y="{y}" font-family="Inter, sans-serif" font-size="14" fill="#9aa3b2"><tspan font-weight="700">{k}</tspan> <tspan x="100">{v}</tspan></text>
    </g>'''
        items.append(anim or f'<text x="18" y="{y}" font-family="Inter, sans-serif" font-size="14" fill="#9aa3b2"><tspan font-weight="700">{k}</tspan> <tspan x="100">{v}</tspan></text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <rect rx="8" width="100%" height="100%" fill="#010409"/>
  <rect x="0" y="0" width="100%" height="36" rx="8" fill="#0f1720"/>
  <text x="18" y="22" font-family="Inter, sans-serif" font-size="14" fill="#c9d1d9">{title}</text>
  {"".join(items)}
</svg>'''
    Path(out_path).write_text(svg, encoding="utf-8")
    print("Wrote", out_path)

if __name__ == "__main__":
    static = os.environ.get("STATIC") == "1"
    make_svg(LINES, OUT, static=static)