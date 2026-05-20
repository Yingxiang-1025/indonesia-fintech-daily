"""Diagnose: dates, broken links, cross-country, Akulaku coverage."""
import json, sys, io
from datetime import datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

print(f"=== 1. Yesterday ({yesterday}) items ===")
yitems = [n for n in news if n.get("published") == yesterday]
print(f"Count: {len(yitems)}")
for i, n in enumerate(yitems[:10]):
    title = (n.get("title_zh") or n.get("title", ""))[:60]
    url = n.get("url", "")
    is_gn = "news.google.com" in url
    print(f"  {i+1}. [{n['published']}] {title}")
    print(f"     URL type: {'Google News' if is_gn else 'Direct'}")
    print(f"     URL: {url[:90]}")

print(f"\n=== 2. Akulaku section items ===")
aku = [n for n in news if "akulaku" in n.get("sections", [])]
print(f"Count: {len(aku)}")
for n in aku:
    title = (n.get("title_zh") or n.get("title", ""))[:60]
    pub = n.get("published", "?")
    ok = "✅" if pub >= "2026" else "❌"
    print(f"  {ok} [{pub}] {title}")
    print(f"     URL: {n.get('url', '')[:90]}")

print(f"\n=== 3. Items with published year < 2026 ===")
old = [n for n in news if n.get("published", "9999") < "2026-01-01"]
print(f"Count: {len(old)}")
for n in old[:10]:
    title = (n.get("title_zh") or n.get("title", ""))[:60]
    print(f"  [{n.get('published')}] fetch={n.get('fetched_date')} {title}")

print(f"\n=== 4. Cross-country items (Thailand/Philippines in title) ===")
cross_kw = ["thailand", "thai", "philippines", "philippine", "泰国", "菲律宾",
            "bangkok", "manila", "PromptPay", "GCash", "TrueMoney"]
cross = []
for n in news:
    text = (n.get("title", "") + " " + n.get("title_zh", "")).lower()
    matched = [w for w in cross_kw if w.lower() in text]
    if matched:
        cross.append((n, matched))
print(f"Count: {len(cross)}")
for n, kws in cross:
    title = (n.get("title_zh") or n.get("title", ""))[:60]
    print(f"  [{n.get('published')}] {title}")
    print(f"     Matched: {kws}")

print(f"\n=== 5. Akulaku coverage check ===")
aku_all = []
for n in news:
    text = (n.get("title", "") + " " + n.get("summary", "")).lower()
    if "akulaku" in text or "asetku" in text or "silvrr" in text:
        aku_all.append(n)
print(f"Total items mentioning Akulaku/Asetku/Silvrr: {len(aku_all)}")
print(f"In akulaku section: {len(aku)}")
print(f"Not in akulaku section: {len(aku_all) - len(aku)}")
not_in_section = [n for n in aku_all if "akulaku" not in n.get("sections", [])]
for n in not_in_section:
    title = (n.get("title_zh") or n.get("title", ""))[:60]
    print(f"  [{n.get('published')}] sections={n.get('sections',[])} {title}")

print(f"\n=== 6. Search for 'Tech in Asia' articles about Akulaku ===")
tia = [n for n in news if "tech in asia" in n.get("source", "").lower() or "techinasia" in n.get("url", "").lower()]
print(f"Tech in Asia articles total: {len(tia)}")
for n in tia:
    title = (n.get("title_zh") or n.get("title", ""))[:60]
    print(f"  [{n.get('published')}] {title}")
