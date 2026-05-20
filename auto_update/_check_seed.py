import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("data/seed_news.json", "r", encoding="utf-8") as f:
    seed = json.load(f)

print(f"Seed items: {len(seed)}")
for n in seed:
    url = n.get("url", "")
    pub = n.get("published", "?")
    has_2024 = "2024" in url
    old_pub = pub < "2026" if pub and pub != "?" else False
    if has_2024 or old_pub:
        title = (n.get("title_zh") or n.get("title", ""))[:70]
        print(f"  [{pub}] URL_2024={has_2024}  {title}")
        print(f"     {url[:90]}")
