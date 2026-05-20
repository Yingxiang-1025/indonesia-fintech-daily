"""One-time cleanup: remove non-Indonesia articles and resolve Google News URLs."""
import json, sys, io, re, time
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

INDONESIA_GEO = [
    "indonesia", "indonesian", "jakarta", "ojk", "rupiah", "idr",
    "印尼", "印度尼西亚", "雅加达",
    "tokopedia", "gojek", "goto", "bukalapak",
    "bank indonesia", "ihsg", "idx", "bca", "bri", "mandiri", "bni",
    "akulaku", "asetku", "kredivo", "adakami", "kredit pintar",
    "gopay", "ovo", "shopeepay", "linkaja", "dana indonesia",
    "pinjol", "pinjaman", "fintek",
    "bank jago", "sea bank", "allo bank", "superbank",
    "koinworks", "modalku", "investree", "amartha", "danamas",
]

REGIONAL = ["fintech news sg", "fintech news my", "e27",
            "fintechnews.sg", "fintechnews.my", "e27.co"]

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

print(f"Total items before cleanup: {len(news)}")

keep = []
removed = []
gn_resolved = 0

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

print(f"\nRemoved {len(removed)} non-Indonesia articles:")
for n in removed:
    title = (n.get("title_zh") or n.get("title", ""))[:60]
    src = n.get("source", "")
    print(f"  [{n.get('published')}] [{src}] {title}")

# Try to resolve remaining Google News URLs
print(f"\nResolving Google News URLs...")
gn_items = [n for n in keep if "news.google.com" in n.get("url", "")]
print(f"Found {len(gn_items)} Google News URLs to resolve")

for n in gn_items:
    old_url = n["url"]
    try:
        resp = requests.get(
            old_url, allow_redirects=True, timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html",
            },
            stream=True,
        )
        resp.close()
        final = resp.url
        if final and "news.google.com" not in final:
            n["url"] = final
            gn_resolved += 1
            title = (n.get("title_zh") or n.get("title", ""))[:50]
            print(f"  ✅ Resolved: {title}")
            print(f"     -> {final[:80]}")

            url_date = None
            m = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", final)
            if m:
                url_date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
                if url_date != n.get("published") and int(url_date[:4]) >= 2026:
                    print(f"     Date: {n.get('published')} -> {url_date}")
                    n["published"] = url_date
    except Exception as e:
        title = (n.get("title_zh") or n.get("title", ""))[:50]
        print(f"  ❌ Failed: {title} ({e})")
    time.sleep(0.3)

remaining_gn = sum(1 for n in keep if "news.google.com" in n.get("url", ""))
print(f"\nResolved {gn_resolved} Google News URLs")
print(f"Remaining unresolved: {remaining_gn}")

with open("data/news.json", "w", encoding="utf-8") as f:
    json.dump(keep, f, ensure_ascii=False, indent=2)

print(f"\nFinal: {len(keep)} items saved (removed {len(removed)})")
