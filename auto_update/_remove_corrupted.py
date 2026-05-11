"""Remove the 9 items whose published dates were corrupted by _fix_dates.py."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

before = len(news)
# These 9 items have published=fetched=2026-05-09, originally from 2020-2025
corrupted_urls = set()
for n in news:
    if n.get("published") == "2026-05-09" and n.get("fetched_date") == "2026-05-09":
        title = n.get("title_zh") or n.get("title", "")
        for y in ["2020", "2021", "2022", "2023", "2024", "2025"]:
            if y in title or y in (n.get("summary_zh") or n.get("summary", "")):
                corrupted_urls.add(n.get("url", ""))
                print(f"  REMOVE: [{n.get('published')}] {title[:60]}")
                break

clean = [n for n in news if n.get("url", "") not in corrupted_urls]
# Also remove any items from 2026-05-09 fetched=2026-05-09 that were not caught above
# but are clearly old (Akulaku BNPL from 2022, OVO from 2020, etc.)
remaining_may09 = [n for n in clean if n.get("published") == "2026-05-09" and n.get("fetched_date") == "2026-05-09"]
print(f"\nRemaining 2026-05-09/2026-05-09 items: {len(remaining_may09)}")
for n in remaining_may09:
    title = (n.get("title_zh") or n.get("title", ""))[:60]
    print(f"  [{n.get('published')}] {title}")

removed = before - len(clean)
print(f"\nBefore: {before}, After: {len(clean)}, Removed: {removed}")
if removed:
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(clean, f, ensure_ascii=False, indent=2)
    print("Saved.")
