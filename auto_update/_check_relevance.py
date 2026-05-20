"""Check articles that may not be Indonesia-specific."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

indonesia_kw = [
    "indonesia", "indonesian", "jakarta", "ojk", "rupiah", "idr",
    "印尼", "印度尼西亚", "雅加达", "卢比",
    "tokopedia", "gojek", "goto", "bukalapak", "shopee indonesia",
    "bank indonesia", "bi ", "ihsg", "idx",
]

print("=== Articles that may NOT be Indonesia-specific ===\n")
non_id = []
for n in news:
    text = (n.get("title", "") + " " + n.get("summary", "") + " " +
            n.get("title_zh", "") + " " + n.get("summary_zh", "")).lower()
    has_id = any(kw in text for kw in indonesia_kw)
    if not has_id:
        non_id.append(n)

print(f"Total news: {len(news)}")
print(f"Non-Indonesia-specific: {len(non_id)}")
print()
for n in non_id:
    title = (n.get("title_zh") or n.get("title", ""))[:65]
    source = n.get("source", "")
    pub = n.get("published", "?")
    sections = n.get("sections", [])
    print(f"  [{pub}] [{source}] {title}")
    print(f"     sections: {sections}")
    print(f"     URL: {n.get('url', '')[:80]}")
    print()
