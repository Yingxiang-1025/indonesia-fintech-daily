import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REGIONAL = ["fintech news sg", "fintech news my", "e27",
            "fintechnews.sg", "fintechnews.my", "e27.co",
            "fintech singapore"]

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

for n in news:
    source = n.get("source", "").lower()
    url = n.get("url", "").lower()
    is_regional = any(rs in source or rs in url for rs in REGIONAL)
    if is_regional:
        title_zh = n.get("title_zh", "")[:60]
        print(f"Source: {n.get('source','')} | {title_zh}")
        text = (n.get("title", "") + " " + n.get("summary", "") + " " +
                n.get("title_zh", "") + " " + n.get("summary_zh", "")).lower()
        if "indonesia" in text:
            print(f"  -> Contains 'indonesia' in text")
        elif "印尼" in text or "印度尼西亚" in text:
            print(f"  -> Contains '印尼/印度尼西亚' in text")
        else:
            print(f"  -> NO Indonesia keyword found")
        print()
