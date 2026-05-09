"""Regenerate HTML pages from current news.json."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, ".")

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

from generator import generate_all_pages, get_next_vol_number
vol = get_next_vol_number()
generate_all_pages(news, vol_number=vol)
print(f"Regenerated HTML pages. Vol: {vol:03d}")
