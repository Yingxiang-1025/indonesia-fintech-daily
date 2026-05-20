"""Test all existing + candidate RSS feeds for Indonesia fintech coverage."""
import sys, io, time
import feedparser
from datetime import datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

FEEDS = [
    # --- Existing ---
    ("Kontan", "https://www.kontan.co.id/rss", "existing"),
    ("Bisnis.com", "https://rss.bisnis.com/finansial", "existing"),
    ("CNBC Indonesia", "https://www.cnbcindonesia.com/tech/rss", "existing"),
    ("DailySocial", "https://dailysocial.id/feed", "existing"),
    ("Tech in Asia", "https://www.techinasia.com/feed", "existing"),
    ("Katadata", "https://katadata.co.id/rss", "existing"),
    ("Detik Finance", "https://finance.detik.com/indeks/rss", "existing"),
    # --- Candidate new ---
    ("Kompas Finansial", "https://rss.kompas.com/finansial", "new"),
    ("Tempo Business", "https://rss.tempo.co/bisnis", "new"),
    ("Liputan6 Bisnis", "https://www.liputan6.com/feed/tag/bisnis", "new"),
    ("IDN Financials", "https://www.idnfinancials.com/rss", "new"),
    ("Fintech News SG", "https://fintechnews.sg/feed/", "new"),
    ("e27", "https://e27.co/feed/", "new"),
    ("Jakarta Globe", "https://jakartaglobe.id/feed", "new"),
    ("Jakarta Post Biz", "https://www.thejakartapost.com/feed/business", "new"),
    # --- Extra candidates ---
    ("Fintech News MY", "https://fintechnews.my/feed/", "new"),
    ("Kompas.com Money", "https://rss.kompas.com/money", "new"),
    ("CNBC ID Finance", "https://www.cnbcindonesia.com/market/rss", "new"),
    ("Detik Inet", "https://inet.detik.com/indeks/rss", "new"),
    ("Tirto Ekonomi", "https://tirto.id/feed/ekonomi", "new"),
]

FINTECH_KW = [
    "fintech", "lending", "pinjaman", "kredit", "bank digital", "e-wallet",
    "bnpl", "paylater", "gopay", "ovo", "dana", "akulaku", "kredivo",
    "ojk", "qris", "p2p", "digital", "payment", "fintek", "pinjol",
    "shopeepay", "gopaylater", "bank jago", "neobank", "dompet",
]

cutoff = datetime.now() - timedelta(days=14)

print(f"{'='*80}")
print(f"  RSS Feed Availability Test — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"  Cutoff: {cutoff.strftime('%Y-%m-%d')} (14 days back)")
print(f"{'='*80}\n")

summary = []
for name, url, status in FEEDS:
    try:
        feed = feedparser.parse(url)
        total = len(feed.entries)
        
        recent_count = 0
        fintech_count = 0
        sample_titles = []
        
        for entry in feed.entries[:30]:
            pub_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                pub_date = datetime(*entry.updated_parsed[:6])
            
            if pub_date and pub_date >= cutoff:
                recent_count += 1
                title = entry.get("title", "")
                text = (title + " " + entry.get("summary", "")).lower()
                if any(kw in text for kw in FINTECH_KW):
                    fintech_count += 1
                    if len(sample_titles) < 3:
                        sample_titles.append(f"  [{pub_date.strftime('%m-%d')}] {title[:60]}")
        
        tag = "[EXISTING]" if status == "existing" else "[NEW]    "
        ok = "✅" if total > 0 else "❌"
        ft = f"fintech={fintech_count}" if fintech_count > 0 else "fintech=0"
        print(f"{ok} {tag} {name}")
        print(f"   Total entries: {total} | Recent (14d): {recent_count} | {ft}")
        if sample_titles:
            for t in sample_titles:
                print(f"   {t}")
        print()
        
        summary.append((name, status, total, recent_count, fintech_count, total > 0))
        
    except Exception as e:
        print(f"❌ {name}: ERROR - {e}\n")
        summary.append((name, status, 0, 0, 0, False))
    
    time.sleep(0.5)

print(f"\n{'='*80}")
print(f"  SUMMARY")
print(f"{'='*80}")
print(f"{'Source':<25} {'Status':<10} {'Total':>6} {'Recent':>7} {'Fintech':>8} {'OK':>4}")
print(f"{'-'*25} {'-'*10} {'-'*6} {'-'*7} {'-'*8} {'-'*4}")
for name, status, total, recent, fintech, ok in summary:
    ok_str = "✅" if ok else "❌"
    print(f"{name:<25} {status:<10} {total:>6} {recent:>7} {fintech:>8} {ok_str:>4}")

viable_new = [(n, r, f) for n, s, t, r, f, ok in summary if s == "new" and ok and f > 0]
print(f"\nViable new sources with fintech content: {len(viable_new)}")
for n, r, f in viable_new:
    print(f"  ✅ {n}: {r} recent, {f} fintech")
