import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
news = json.load(open("data/news.json", "r", encoding="utf-8"))
today = [n for n in news if n.get("fetched_date") == "2026-05-09"]
print(f"=== Indonesia: {len(today)} items fetched 2026-05-09 ===")
for n in today:
    pub = n.get("published", "?")
    fetch = n.get("fetched_date", "?")
    title = (n.get("title_zh") or n.get("title", ""))[:65]
    print(f"  pub={pub}  fetch={fetch}  {title}")
