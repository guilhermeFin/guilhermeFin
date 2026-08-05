#!/usr/bin/env python3
"""Render data/contributions.json into contrib-heatmap.svg."""
import json
from pathlib import Path

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
IN_PATH = Path("data/contributions.json")
OUT_PATH = Path("contrib-heatmap.svg")


def render_heatmap():
    if not IN_PATH.exists():
        raise SystemExit("Missing data/contributions.json. Run scripts/fetch_contributions.py first.")

    data = json.loads(IN_PATH.read_text(encoding="utf-8"))
    days = data.get("days", [])
    if not days:
        raise SystemExit("No contribution days found in data/contributions.json.")

    cols = 53
    rows = 7
    cell = 14
    gap = 4
    width = cols * (cell + gap)
    height = rows * (cell + gap) + 42

    rects = []
    for idx, day in enumerate(days):
        col = idx // 7
        row = idx % 7
        x = col * (cell + gap)
        y = row * (cell + gap)
        level = max(0, min(int(day.get("level", 0)), len(PALETTE) - 1))
        color = PALETTE[level]
        delay = (col + row) * 0.02
        rects.append(
            f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{color}" style="opacity:0; animation:rise 0.45s ease {delay}s forwards" data-date="{day["date"]}" data-count="{day["count"]}"/>'
        )

    legend = "".join(
        f'<rect x="{50 + i * 26}" y="0" width="18" height="12" rx="3" fill="{color}" />'
        for i, color in enumerate(PALETTE[1:], start=1)
    )
    stats = data.get("total", 0)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#0b0b0b"/>
  <style>
    @keyframes rise {{
      from {{ transform: translate(-10px,-10px) scale(0.92); opacity: 0; }}
      to {{ transform: translate(0,0) scale(1); opacity: 1; }}
    }}
    .legend text {{ font-family: Inter, sans-serif; font-size: 12px; fill: #b9c0c8; }}
  </style>
  <g transform="translate(0,10)">
    {''.join(rects)}
  </g>
  <g transform="translate(0, {rows * (cell + gap) + 18})" class="legend">
    <text x="0" y="12">Less</text>
    {legend}
    <text x="{50 + 26 * 5}" y="12">More</text>
    <text x="{width - 260}" y="12" font-family="Inter, sans-serif" font-size="12" fill="#9aa3b2">{stats} contributions in the last year</text>
  </g>
</svg>'''

    OUT_PATH.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    render_heatmap()
