"""Check URLs of remaining May 9 items for date clues."""
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

may09 = [n for n in news if n.get("published") == "2026-05-09" and n.get("fetched_date") == "2026-05-09"]
print(f"Items with published=fetched=2026-05-09: {len(may09)}\n")
for n in may09:
    title = (n.get("title_zh") or n.get("title", ""))[:60]
    url = n.get("url", "")
    # Extract year patterns from URL
    url_years = re.findall(r'/20[12]\d/', url)
    url_short = url[:100] if len(url) > 100 else url
    print(f"  Title: {title}")
    print(f"  URL: {url_short}")
    if url_years:
        print(f"  URL year: {url_years}")
    print()
