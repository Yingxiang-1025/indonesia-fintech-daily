import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

for n in news:
    src = n.get("source", "")
    url = n.get("url", "")
    if "fintechnews" in url.lower() or "e27" in url.lower() or "fintech news" in src.lower() or "fintech singapore" in src.lower():
        title = (n.get("title_zh") or n.get("title", ""))[:50]
        print(f"Source=[{src}]  URL_domain=[{url[:40]}]")
        print(f"  {title}")
        all_text = " ".join([n.get("title",""),n.get("summary",""),n.get("title_zh",""),n.get("summary_zh","")]).lower()
        found = [geo for geo in ["indonesia","indonesian","印尼","印度尼西亚","akulaku","kredivo","shopeepay","gopay","ovo","ojk","pinjol"] if geo in all_text]
        print(f"  GEO matches: {found}")
        print()
