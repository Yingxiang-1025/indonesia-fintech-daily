import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

REGIONAL = ["fintech news sg", "fintech news my", "e27", "fintech singapore"]
REGIONAL_DOMAINS = ["fintechnews.sg", "fintechnews.my", "e27.co"]

INDONESIA_GEO = [
    "indonesia", "indonesian", "jakarta", "ojk", "rupiah", "idr",
    "印尼", "印度尼西亚", "雅加达",
    "tokopedia", "gojek", "goto", "bukalapak",
    "bank indonesia", "ihsg", "idx", "bca", "bri", "mandiri", "bni",
    "akulaku", "asetku", "kredivo", "adakami", "kredit pintar",
    "gopay", "ovo", "shopeepay", "linkaja",
    "pinjol", "pinjaman", "fintek",
    "bank jago", "sea bank", "allo bank", "superbank",
    "koinworks", "modalku", "investree", "amartha", "danamas",
]

to_remove_urls = set()
for n in news:
    src = n.get("source", "").lower()
    url = n.get("url", "").lower()
    is_regional = (any(r in src for r in REGIONAL) or
                   any(d in url for d in REGIONAL_DOMAINS))
    if is_regional:
        all_text = " ".join([
            n.get("title", ""), n.get("summary", ""),
            n.get("title_zh", ""), n.get("summary_zh", ""),
        ]).lower()
        if not any(g in all_text for g in INDONESIA_GEO):
            to_remove_urls.add(n.get("url", ""))
            title = (n.get("title_zh") or n.get("title", ""))[:60]
            print(f"Will remove: [{src}] {title}")

if to_remove_urls:
    keep = [n for n in news if n.get("url", "") not in to_remove_urls]
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(keep, f, ensure_ascii=False, indent=2)
    print(f"\nRemoved {len(to_remove_urls)} items. Kept {len(keep)}")
else:
    print(f"\nNo items to remove. Total: {len(news)}")
