"""Final cleanup with word-boundary matching for short keywords."""
import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

INDONESIA_GEO = [
    "indonesia", "indonesian", "jakarta", "ojk", "rupiah",
    "印尼", "印度尼西亚", "雅加达",
    "tokopedia", "gojek", "goto", "bukalapak",
    "bank indonesia", "ihsg",
    "akulaku", "asetku", "kredivo", "adakami", "kredit pintar",
    "gopay", "shopeepay", "linkaja", "dana indonesia",
    "pinjol", "pinjaman online", "fintek",
    "bank jago", "sea bank", "allo bank", "superbank",
    "koinworks", "modalku", "investree", "amartha", "danamas",
]
GEO_WB = ["bri", "bni", "bca", "ovo", "idr", "idx"]

REGIONAL = ["fintech news sg", "fintech news my", "e27", "fintech singapore"]
DOMAINS = ["fintechnews.sg", "fintechnews.my", "e27.co"]

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

to_remove = []
for n in news:
    src = n.get("source", "").lower()
    url = n.get("url", "").lower()
    is_regional = any(r in src for r in REGIONAL) or any(d in url for d in DOMAINS)
    if not is_regional:
        continue

    text = " ".join([
        n.get("title", ""), n.get("summary", ""),
        n.get("title_zh", ""), n.get("summary_zh", ""),
    ]).lower()

    has_geo = any(g in text for g in INDONESIA_GEO)
    if not has_geo:
        has_geo = any(re.search(r'\b' + re.escape(w) + r'\b', text) for w in GEO_WB)
    if not has_geo:
        to_remove.append(n.get("url", ""))
        title = (n.get("title_zh") or n.get("title", ""))[:60]
        print(f"REMOVE: [{n.get('source','')}] {title}")

if to_remove:
    to_remove_set = set(to_remove)
    keep = [n for n in news if n.get("url", "") not in to_remove_set]
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(keep, f, ensure_ascii=False, indent=2)
    print(f"\nRemoved {len(to_remove)} items. Kept {len(keep)}")
else:
    print(f"\nNo items to remove. Total: {len(news)}")
