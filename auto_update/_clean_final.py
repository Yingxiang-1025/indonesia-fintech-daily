"""Final cleanup: remove remaining non-Indonesia regional source articles."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

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

REGIONAL = ["fintech news sg", "fintech news my", "e27",
            "fintechnews.sg", "fintechnews.my", "e27.co",
            "fintech singapore"]

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

keep = []
removed = []
for n in news:
    source = n.get("source", "").lower()
    url = n.get("url", "").lower()
    is_regional = any(rs in source or rs in url for rs in REGIONAL)
    if is_regional:
        text = (n.get("title", "") + " " + n.get("summary", "") + " " +
                n.get("title_zh", "") + " " + n.get("summary_zh", "")).lower()
        if not any(geo in text for geo in INDONESIA_GEO):
            removed.append(n)
            continue
    keep.append(n)

print(f"Removed {len(removed)} more non-Indonesia articles:")
for n in removed:
    title = (n.get("title_zh") or n.get("title", ""))[:60]
    print(f"  [{n.get('published')}] [{n.get('source','')}] {title}")

with open("data/news.json", "w", encoding="utf-8") as f:
    json.dump(keep, f, ensure_ascii=False, indent=2)
print(f"\nFinal: {len(keep)} items (removed {len(removed)})")
