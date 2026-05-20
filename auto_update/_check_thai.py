import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)
for n in news:
    src = n.get("source", "")
    title = n.get("title", "")
    title_zh = n.get("title_zh", "")
    if "Thailand" in src or "Thailand" in title or "泰国" in title_zh:
        print(f"Title: {title[:80]}")
        print(f"Title_zh: {title_zh[:80]}")
        print(f"Source: {src}")
        print(f"Sections: {n.get('sections', [])}")
        print()
