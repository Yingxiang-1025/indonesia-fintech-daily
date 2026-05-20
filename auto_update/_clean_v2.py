"""Aggressive cleanup: remove all non-Indonesia articles from regional sources."""
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

REGIONAL_DOMAINS = [
    "fintechnews.sg", "fintechnews.my", "e27.co",
]
REGIONAL_SOURCES = [
    "fintech news sg", "fintech news my", "e27",
    "fintech singapore", "fintech news singapore",
]

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

keep = []
removed = []
for n in news:
    source_lower = n.get("source", "").lower()
    url_lower = n.get("url", "").lower()

    is_regional_source = any(rs in source_lower for rs in REGIONAL_SOURCES)
    is_regional_domain = any(rd in url_lower for rd in REGIONAL_DOMAINS)
    is_regional = is_regional_source or is_regional_domain

    if is_regional:
        all_text = " ".join([
            n.get("title", ""), n.get("summary", ""),
            n.get("title_zh", ""), n.get("summary_zh", ""),
        ]).lower()
        has_indonesia = any(geo in all_text for geo in INDONESIA_GEO)
        if not has_indonesia:
            removed.append(n)
            title_zh = n.get("title_zh", "")[:60]
            print(f"REMOVE: [{n.get('source','')}] {title_zh}")
            continue

    keep.append(n)

print(f"\nRemoved: {len(removed)}, Kept: {len(keep)}")

with open("data/news.json", "w", encoding="utf-8") as f:
    json.dump(keep, f, ensure_ascii=False, indent=2)
