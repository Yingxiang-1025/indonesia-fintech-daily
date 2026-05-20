"""Full RSS + keyword verification: 2026-01-01 to now."""
import sys, io, time, json
from collections import Counter
import feedparser
from datetime import datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

FEEDS = [
    # --- Existing ---
    ("Kontan", "https://www.kontan.co.id/rss", "existing"),
    ("Bisnis.com", "https://rss.bisnis.com/finansial", "existing"),
    ("CNBC Indonesia Tech", "https://www.cnbcindonesia.com/tech/rss", "existing"),
    ("DailySocial", "https://dailysocial.id/feed", "existing"),
    ("Tech in Asia", "https://www.techinasia.com/feed", "existing"),
    ("Katadata", "https://katadata.co.id/rss", "existing"),
    ("Detik Finance", "https://finance.detik.com/indeks/rss", "existing"),
    # --- Candidate new ---
    ("Tempo Business", "https://rss.tempo.co/bisnis", "new"),
    ("Fintech News SG", "https://fintechnews.sg/feed/", "new"),
    ("e27", "https://e27.co/feed/", "new"),
    ("Fintech News MY", "https://fintechnews.my/feed/", "new"),
    ("CNBC ID Finance", "https://www.cnbcindonesia.com/market/rss", "new"),
    # --- Additional candidates ---
    ("Kompas Finansial", "https://rss.kompas.com/finansial", "new"),
    ("Liputan6 Bisnis", "https://www.liputan6.com/feed/tag/bisnis", "new"),
    ("IDN Financials", "https://www.idnfinancials.com/rss", "new"),
    ("Jakarta Globe", "https://jakartaglobe.id/feed", "new"),
    ("Jakarta Post Biz", "https://www.thejakartapost.com/feed/business", "new"),
    ("Detik Inet", "https://inet.detik.com/indeks/rss", "new"),
    ("Tirto Ekonomi", "https://tirto.id/feed/ekonomi", "new"),
    ("Kompas.com Money", "https://rss.kompas.com/money", "new"),
    # --- More candidates ---
    ("Kontan Keuangan", "https://www.kontan.co.id/rss/keuangan", "new"),
    ("Bisnis.com Tech", "https://rss.bisnis.com/teknologi", "new"),
    ("CNBC ID Tech", "https://www.cnbcindonesia.com/tech/rss", "new-dup"),
    ("Detik Finance Alt", "https://finance.detik.com/rss", "new"),
    ("Investor Daily", "https://investor.id/feed", "new"),
    ("iNews Finance", "https://www.inews.id/finance/rss", "new"),
]

# All keywords to test - both existing and candidate
KEYWORDS_EN = [
    "fintech", "lending", "pinjaman", "kredit", "digital bank", "e-wallet",
    "BNPL", "paylater", "GoPay", "OVO", "DANA", "Akulaku", "Asetku",
    "Kredivo", "OJK", "Bank Indonesia", "QRIS", "P2P", "fintech lending",
    "digital payment", "dompet digital", "neobank",
]

KEYWORDS_ID = [
    "pinjol", "fintek", "bank digital", "pembayaran digital",
    "kartu kredit", "dompet digital", "pinjaman online",
    "suku bunga", "regulasi keuangan", "inklusi keuangan",
    "pinjaman", "kredit", "teknologi keuangan",
    "ShopeePay", "GoPayLater", "LinkAja", "Bank Jago",
    "Sea Bank", "Allo Bank", "AdaKami", "Kredit Pintar",
    "Danamas", "Amartha", "KoinWorks", "Modalku", "Investree",
]

ALL_KEYWORDS = list(set([k.lower() for k in KEYWORDS_EN + KEYWORDS_ID]))

cutoff = datetime(2026, 1, 1)

print(f"{'='*80}")
print(f"  Full RSS + Keyword Verification")
print(f"  Time window: 2026-01-01 ~ {datetime.now().strftime('%Y-%m-%d')}")
print(f"  Keywords to test: {len(ALL_KEYWORDS)}")
print(f"{'='*80}\n")

all_articles = []
summary = []

for name, url, status in FEEDS:
    if status == "new-dup":
        continue
    try:
        feed = feedparser.parse(url)
        total = len(feed.entries)

        recent_count = 0
        fintech_count = 0
        matched_kws = Counter()
        sample_titles = []

        for entry in feed.entries[:50]:
            pub_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                pub_date = datetime(*entry.updated_parsed[:6])

            if pub_date and pub_date >= cutoff:
                recent_count += 1
                title = entry.get("title", "")
                summ = entry.get("summary", entry.get("description", ""))
                if summ and "<" in summ:
                    from bs4 import BeautifulSoup
                    summ = BeautifulSoup(summ, "html.parser").get_text()
                text = (title + " " + (summ or "")).lower()

                article_matched = False
                for kw in ALL_KEYWORDS:
                    if kw in text:
                        matched_kws[kw] += 1
                        article_matched = True

                if article_matched:
                    fintech_count += 1
                    if len(sample_titles) < 3:
                        sample_titles.append(
                            f"  [{pub_date.strftime('%m-%d')}] {title[:65]}"
                        )
                    all_articles.append({
                        "source": name,
                        "title": title[:80],
                        "date": pub_date.strftime("%Y-%m-%d"),
                        "matched_kws": [k for k in ALL_KEYWORDS if k in text],
                    })

        tag = "[EXISTING]" if status == "existing" else "[NEW]    "
        ok = "✅" if total > 0 else "❌"
        print(f"{ok} {tag} {name}")
        print(f"   Entries: {total} | Since 2026-01: {recent_count} | Fintech match: {fintech_count}")
        if matched_kws:
            top5 = matched_kws.most_common(5)
            kw_str = ", ".join(f"{k}({v})" for k, v in top5)
            print(f"   Top keywords: {kw_str}")
        if sample_titles:
            for t in sample_titles:
                print(f"   {t}")
        print()

        summary.append((name, status, total, recent_count, fintech_count, total > 0, matched_kws))

    except Exception as e:
        print(f"❌ [{status.upper():<8}] {name}: ERROR - {e}\n")
        summary.append((name, status, 0, 0, 0, False, Counter()))

    time.sleep(0.5)


# ── Keyword effectiveness summary ──
print(f"\n{'='*80}")
print(f"  KEYWORD EFFECTIVENESS (across all working feeds)")
print(f"{'='*80}")

global_kw_counts = Counter()
for _, _, _, _, _, ok, kws in summary:
    if ok:
        global_kw_counts.update(kws)

en_kws = [(k, global_kw_counts.get(k.lower(), 0)) for k in KEYWORDS_EN]
id_kws = [(k, global_kw_counts.get(k.lower(), 0)) for k in KEYWORDS_ID]

print(f"\n--- English keywords ---")
print(f"{'Keyword':<25} {'Matches':>8}")
print(f"{'-'*25} {'-'*8}")
for k, c in sorted(en_kws, key=lambda x: -x[1]):
    flag = "✅" if c > 0 else "❌"
    print(f"{flag} {k:<23} {c:>8}")

print(f"\n--- Indonesian keywords (existing + candidate) ---")
print(f"{'Keyword':<25} {'Matches':>8}")
print(f"{'-'*25} {'-'*8}")
for k, c in sorted(id_kws, key=lambda x: -x[1]):
    flag = "✅" if c > 0 else "❌"
    print(f"{flag} {k:<23} {c:>8}")

# ── Final summary ──
print(f"\n{'='*80}")
print(f"  FEED SUMMARY")
print(f"{'='*80}")
print(f"{'Source':<25} {'Status':<10} {'Entries':>7} {'2026':>6} {'Fintech':>8} {'OK':>4}")
print(f"{'-'*25} {'-'*10} {'-'*7} {'-'*6} {'-'*8} {'-'*4}")
for name, status, total, recent, fintech, ok, _ in summary:
    ok_str = "✅" if ok and fintech > 0 else ("⚠️" if ok else "❌")
    print(f"{name:<25} {status:<10} {total:>7} {recent:>6} {fintech:>8} {ok_str}")

effective_existing = sum(1 for _, s, _, _, f, ok, _ in summary if s == "existing" and ok and f > 0)
effective_new = sum(1 for _, s, _, _, f, ok, _ in summary if s == "new" and ok and f > 0)
print(f"\nExisting feeds with fintech: {effective_existing}/7")
print(f"New candidate feeds with fintech: {effective_new}")
print(f"Total fintech articles found: {len(all_articles)}")
