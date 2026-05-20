import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
news = json.load(open("data/news.json", "r", encoding="utf-8"))
items = [n for n in news if "fintechnews.sg" in n.get("url", "").lower()]

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

for n in items:
    title = n.get("title", "")[:60]
    all_text = " ".join([
        n.get("title", ""), n.get("summary", ""),
        n.get("title_zh", ""), n.get("summary_zh", ""),
    ]).lower()
    found = [g for g in INDONESIA_GEO if g in all_text]
    print(f"Title: {title}")
    print(f"  Summary: {n.get('summary', '')[:100]}")
    print(f"  Summary_zh: {n.get('summary_zh', '')[:100]}")
    print(f"  GEO matches: {found}")
    print()
