import json
news = json.load(open("data/news.json", "r", encoding="utf-8"))
items = [n for n in news if "fintechnews.sg" in n.get("url", "").lower()]
REGIONAL = ["fintech news sg", "fintech news my", "e27", "fintech singapore"]
DOMAINS = ["fintechnews.sg", "fintechnews.my", "e27.co"]
GEO = ["indonesia", "indonesian", "jakarta", "ojk"]

for n in items:
    src = n.get("source", "").lower()
    url = n.get("url", "").lower()
    r1 = any(r in src for r in REGIONAL)
    r2 = any(d in url for d in DOMAINS)
    print(f"src=[{src}] r_by_src={r1} r_by_url={r2}")
    text = " ".join([n.get("title",""),n.get("summary",""),n.get("title_zh",""),n.get("summary_zh","")]).lower()
    has_geo = any(g in text for g in GEO)
    print(f"  has_geo={has_geo}")
    print(f"  title={n.get('title','')[:50]}")
    print()
