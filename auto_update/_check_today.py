import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
news = json.load(open("data/news.json", "r", encoding="utf-8"))
today = [n for n in news if n.get("fetched_date") == "2026-05-09"]
print(f"Items with fetched_date=2026-05-09: {len(today)}")
for n in today:
    pub = n.get("published", "?")
    title = n.get("title_zh", n.get("title", ""))[:60]
    print(f"  [{pub}] {title}")
if not today:
    all_fd = set(n.get("fetched_date", "?") for n in news)
    print(f"All fetched_dates in DB: {sorted(all_fd, reverse=True)[:10]}")
