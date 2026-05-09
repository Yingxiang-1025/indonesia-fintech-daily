"""Fix published dates for recently fetched old articles."""
import json, sys, io
from datetime import datetime, timedelta
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

today = datetime.now().strftime("%Y-%m-%d")
date_floor = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
fixed = 0
for n in news:
    if n.get("fetched_date") == today and n.get("published", "9999") < date_floor:
        old_pub = n["published"]
        n["published"] = today
        title = (n.get("title_zh") or n.get("title", ""))[:50]
        print(f"  Fixed: {old_pub} -> {today}  {title}")
        fixed += 1

print(f"\nFixed {fixed} items")
if fixed:
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    print("Saved.")
