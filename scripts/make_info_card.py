#!/usr/bin/env python3
"""
Generate a simple neofetch-style SVG info card.
Usage: python scripts/make_info_card.py
Set env STATIC=1 to output a frozen (non-animated) frame.
"""
import os
from pathlib import Path
from xml.sax.saxutils import escape

OUT = "info-card.svg"
LINES = [
    ("Now", "AI Business Analytics & Econometrics student at USF / Building ML‑driven analytics & Next.js apps"),
    ("Stack", "React (TS) • Next.js (App Router) • Tailwind CSS • Supabase (Postgres) • OpenAI • LangChain • Prisma/Drizzle • Vercel • GitHub Actions"),
    ("Highlights", "• Built a quantitative research operating system.\n• Created Hermes, a self-improving trading bot covering five asset classes.\n• Developed Vantage, a 12-section portfolio stress-testing suite designed for wealth managers.\n• Built M&A tooling that generates teasers, Confidential Information Memorandums (CIMs), and a scored buyer universe.\n• Created a Garmin Coach pipeline for endurance training.\n• Built an options trading bot based on a profitable, backtested trading edge.")
]

def make_svg(lines, out_path, static=False):
    w, h = 960, 520
    title = "gui@github"
    items = []
    base_y = 58
    for i, (k, v) in enumerate(lines):
        safe_key = escape(k)
        safe_value = escape(v)
        lines_for_card = [line for line in safe_value.splitlines() if line]
        if not lines_for_card:
            lines_for_card = [safe_value]

        first_y = base_y + i * 100
        body_lines = []
        for raw_line in lines_for_card:
            wrapped = []
            words = raw_line.split()
            current = ""
            for word in words:
                candidate = f"{current} {word}".strip()
                if len(candidate) <= 95:
                    current = candidate
                else:
                    if current:
                        wrapped.append(current)
                    current = word
            if current:
                wrapped.append(current)
            if not wrapped:
                wrapped = [raw_line]
            for wrapped_line in wrapped:
                body_lines.append((wrapped_line, first_y))
                first_y += 20

        if static:
            anim = ''
        else:
            begin = f"{i * 0.12}s"
            anim = f'''<g transform="translate(0,0)" opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{begin}" fill="freeze"/>
      <text x="18" y="{base_y + i * 100}" font-family="Inter, sans-serif" font-size="16" fill="#9aa3b2"><tspan font-weight="700">{safe_key}</tspan></text>
'''
            for j, (line, y_pos) in enumerate(body_lines):
                indent = 120 if j > 0 else 120
                if line.startswith("•"):
                    anim += f'      <text x="{indent}" y="{y_pos}" font-family="Inter, sans-serif" font-size="16" fill="#9aa3b2">{line}</text>\n'
                else:
                    anim += f'      <text x="{indent}" y="{y_pos}" font-family="Inter, sans-serif" font-size="16" fill="#9aa3b2">{line}</text>\n'
            anim += '    </g>'
        if static:
            rendered = [f'<text x="18" y="{base_y + i * 100}" font-family="Inter, sans-serif" font-size="16" fill="#9aa3b2"><tspan font-weight="700">{safe_key}</tspan></text>']
            for j, (line, y_pos) in enumerate(body_lines):
                rendered.append(f'<text x="120" y="{y_pos}" font-family="Inter, sans-serif" font-size="16" fill="#9aa3b2">{line}</text>')
            items.append("".join(rendered))
        else:
            items.append(anim)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <rect rx="8" width="100%" height="100%" fill="#010409"/>
  <rect x="0" y="0" width="100%" height="36" rx="8" fill="#0f1720"/>
  <text x="18" y="24" font-family="Inter, sans-serif" font-size="18" fill="#c9d1d9">{escape(title)}</text>
  {"".join(items)}
</svg>'''
    Path(out_path).write_text(svg, encoding="utf-8")
    print("Wrote", out_path)

if __name__ == "__main__":
    static = os.environ.get("STATIC") == "1"
    make_svg(LINES, OUT, static=static)