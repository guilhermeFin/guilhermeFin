#!/usr/bin/env python3
"""Fetch the public GitHub contribution calendar and write data/contributions.json.

Usage:
  python scripts/fetch_contributions.py <username>

If no username is provided, the script reads env var GITHUB_USERNAME, USERNAME, or USER.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

OUT = Path("data/contributions.json")


def get_username(argv):
    if len(argv) > 1:
        return argv[1]
    return (
        os.environ.get("GITHUB_USERNAME")
        or os.environ.get("USERNAME")
        or os.environ.get("USER")
        or "guilhermeFin"
    )


def fetch_contributions(username: str):
    url = f"https://github.com/users/{username}/contributions"
    print(f"Fetching {url}")
    response = requests.get(url, timeout=15, headers={"User-Agent": "github-profile-art/1.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    tooltips = {}
    for tooltip in soup.find_all("tool-tip"):
        target = tooltip.get("for")
        text = tooltip.get_text(strip=True)
        if not target or not text:
            continue
        if "No contributions" in text:
            count = 0
        else:
            parts = text.split(" ")
            try:
                count = int(parts[0].replace(",", ""))
            except ValueError:
                count = 0
        tooltips[target] = count

    day_elements = soup.find_all(attrs={"data-date": True})
    if not day_elements:
        raise SystemExit("No contribution data found; check that the username is correct.")

    days = []
    for day_elem in day_elements:
        date = day_elem.get("data-date")
        level = int(day_elem.get("data-level", "0"))
        elem_id = day_elem.get("id")
        count = tooltips.get(elem_id, 0)
        days.append({"date": date, "count": count, "level": level})

    days.sort(key=lambda day: day["date"])
    total = sum(day["count"] for day in days)
    best = max(days, key=lambda day: day["count"]) if days else None

    streaks = []
    current_streak = 0
    longest_streak = 0
    running = 0
    for day in days:
        if day["count"] > 0:
            running += 1
        else:
            if running > 0:
                streaks.append(running)
            running = 0
    if running > 0:
        streaks.append(running)
    if streaks:
        longest_streak = max(streaks)
        current_streak = streaks[-1] if days and days[-1]["count"] > 0 else 0

    out = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "username": username,
        "total": total,
        "best": best,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "days": days,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    username = get_username(sys.argv)
    fetch_contributions(username)
