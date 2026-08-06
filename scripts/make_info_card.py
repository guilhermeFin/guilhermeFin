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
    ("Now", "AI Business Analytics & Econometrics student / Building ML‑driven analytics & Next.js apps"),
    ("Prev", "SRE & platform"),
    ("Stack", "React (TS) • Next.js (App Router) • Tailwind CSS • Supabase (Postgres) • OpenAI • LangChain • Prisma/Drizzle • Vercel • GitHub Actions"),
    ("Highlights", "Built a quant research OS and a 5‑asset self‑improving paper‑trading bot (AlphaForge / Hermes); shipped a 12‑section portfolio stress‑testing suite (Vantage); created M&A tooling that generates teasers/CIMs and a scored buyer‑universe (AdvisorBrain, Atlas); built a local command HUD with a sandboxed AI runner (vault‑os); developed multi‑model LLM review and routing systems (LLM Council, OmniRoute); and automated document sync and deployments across Railway/Google Apps Script, plus a Garmin Coach pipeline for endurance training.")
]

def make_svg(lines, out_path, static=False):
    w, h = 490, 300
    title = "gui@github"
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