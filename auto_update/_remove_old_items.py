"""Remove items that are definitively old (pre-2026) but have corrupted dates.
These were changed from their original dates to 2026-05-09 by _fix_dates.py.
We identify them by checking known old article indicators:
- IBS Intelligence Akulaku BNPL (2022)
- Singapore Fintech OJK Akulaku ban (2024)
- Katadata OVO (2020)
- Dana Syariah fraud (2023)
"""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

before = len(news)

OLD_MARKERS = [
    "IBS Intelligence",
    "新加坡金融科技",
    "OVO 电子货币",
    "OVO e-money",
    "Dana Syariah",
]

remove_urls = set()
for n in news:
    if n.get("published") == "2026-05-09" and n.get("fetched_date") == "2026-05-09":
        title = (n.get("title_zh") or n.get("title", "")) + " " + (n.get("source", ""))
        for marker in OLD_MARKERS:
            if marker.lower() in title.lower():
                remove_urls.add(n.get("url", ""))
                print(f"  REMOVE: {(n.get('title_zh') or n.get('title',''))[:65]}")
                break

clean = [n for n in news if n.get("url", "") not in remove_urls]
removed = before - len(clean)
print(f"\nBefore: {before}, After: {len(clean)}, Removed: {removed}")

if removed:
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(clean, f, ensure_ascii=False, indent=2)
    print("Saved.")

# Final check
remaining_may09 = [n for n in clean if n.get("published") == "2026-05-09" and n.get("fetched_date") == "2026-05-09"]
print(f"\nRemaining 2026-05-09 items: {len(remaining_may09)}")
for n in remaining_may09:
    title = (n.get("title_zh") or n.get("title", ""))[:65]
    print(f"  [{n.get('published')}] {title}")
