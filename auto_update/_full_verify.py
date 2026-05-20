"""Comprehensive verification of all pages and data integrity."""
import json
import re
import os
import requests
from datetime import datetime

print("=" * 60)
print("COMPREHENSIVE VERIFICATION REPORT")
print("=" * 60)

# 1. Verify news.json data integrity
print("\n1. NEWS DATA INTEGRITY")
print("-" * 40)
news = json.load(open('data/news.json', 'r', encoding='utf-8'))
print(f"Total articles: {len(news)}")

issues = []
for i, n in enumerate(news):
    title = n.get('title', '')[:50]
    pub = n.get('published', '')
    url = n.get('url', '')
    sections = n.get('sections', [])
    
    # Check date format
    if not pub or len(pub) != 10:
        issues.append(f"  BAD DATE [{pub}]: {title}")
    else:
        try:
            dt = datetime.strptime(pub, "%Y-%m-%d")
            if dt.year < 2026:
                issues.append(f"  PRE-2026 [{pub}]: {title}")
        except ValueError:
            issues.append(f"  INVALID DATE [{pub}]: {title}")
    
    # Check for empty URLs
    if not url:
        issues.append(f"  NO URL: {title}")
    
    # Check for empty sections
    if not sections:
        issues.append(f"  NO SECTIONS: {title}")
    
    # Check for translation
    if not n.get('title_zh'):
        issues.append(f"  NO TITLE_ZH: {title}")

if issues:
    print(f"  ISSUES FOUND: {len(issues)}")
    for issue in issues[:10]:
        print(issue)
    if len(issues) > 10:
        print(f"  ... and {len(issues)-10} more")
else:
    print("  ALL CHECKS PASSED")

# 2. Check for duplicates
print("\n2. DUPLICATE CHECK")
print("-" * 40)
urls = [n.get('url', '') for n in news]
url_counts = {}
for url in urls:
    if url:
        url_counts[url] = url_counts.get(url, 0) + 1
dupes = {k: v for k, v in url_counts.items() if v > 1}
if dupes:
    print(f"  DUPLICATES FOUND: {len(dupes)}")
    for url, count in dupes.items():
        print(f"  [{count}x] {url[:80]}")
else:
    print("  NO DUPLICATES")

# 3. Check cross-country contamination
print("\n3. CROSS-COUNTRY CHECK")
print("-" * 40)
non_indo_keywords = ['thailand', 'thai', 'philippines', 'filipino', 'manila', 'bangkok', 'vietnam']
contaminated = []
for n in news:
    text = (n.get('title', '') + ' ' + n.get('summary', '')).lower()
    source = n.get('source', '').lower()
    for kw in non_indo_keywords:
        if kw in text and 'indonesia' not in text and 'jakarta' not in text:
            contaminated.append(f"  [{kw}] {n.get('title', '')[:60]}")
            break
if contaminated:
    print(f"  POTENTIAL CONTAMINATION: {len(contaminated)}")
    for c in contaminated[:5]:
        print(c)
else:
    print("  NO CONTAMINATION DETECTED")

# 4. Check Google News URLs (broken links)
print("\n4. GOOGLE NEWS URL CHECK")
print("-" * 40)
gn_urls = [n for n in news if 'news.google.com/rss/articles/' in n.get('url', '')]
print(f"  Articles with Google News RSS URLs: {len(gn_urls)}")
print("  (These are converted to Google Search URLs in the generator)")

# 5. Check page files exist
print("\n5. PAGE FILES CHECK")
print("-" * 40)
pages_dir = '../pages'
expected_pages = [
    'yesterday.html', 'monthly.html', 'akulaku.html', 'overview.html',
    'regulation.html', 'credit-card.html', 'digital-lending.html',
    'cash-loan.html', 'p2p-lending.html', 'bnpl.html', 'e-wallet.html',
    'digital-bank.html'
]
for page in expected_pages:
    path = os.path.join(pages_dir, page)
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"  OK: {page} ({size} bytes)")
    else:
        print(f"  MISSING: {page}")

# Check index.html
idx_path = '../index.html'
if os.path.exists(idx_path):
    print(f"  OK: index.html ({os.path.getsize(idx_path)} bytes)")
else:
    print("  MISSING: index.html")

# 6. Akulaku section check
print("\n6. AKULAKU SECTION")
print("-" * 40)
akulaku = [n for n in news if 'akulaku' in n.get('sections', [])]
print(f"  Akulaku articles: {len(akulaku)}")
for a in akulaku:
    url = a.get('url', '')
    is_gn = 'news.google.com' in url
    print(f"  [{a.get('published','')}] {a.get('title_zh', a.get('title',''))[:50]}")
    print(f"    URL: {'[Google News->Search fallback]' if is_gn else url[:80]}")

# 7. Check Akulaku not in BNPL
print("\n7. AKULAKU-BNPL EXCLUSION CHECK")
print("-" * 40)
bnpl = [n for n in news if 'bnpl' in n.get('sections', [])]
akulaku_in_bnpl = [n for n in bnpl if 'akulaku' in n.get('sections', [])]
if akulaku_in_bnpl:
    print(f"  WARNING: {len(akulaku_in_bnpl)} Akulaku items still in BNPL")
    for a in akulaku_in_bnpl:
        print(f"    {a.get('title','')[:60]}")
else:
    print("  OK: No Akulaku items in BNPL section (exclusion works in generator)")

# 8. Section distribution
print("\n8. SECTION DISTRIBUTION")
print("-" * 40)
section_counts = {}
for n in news:
    for sec in n.get('sections', []):
        section_counts[sec] = section_counts.get(sec, 0) + 1
for sec, count in sorted(section_counts.items(), key=lambda x: -x[1]):
    print(f"  {sec}: {count} articles")

# 9. Date distribution
print("\n9. DATE DISTRIBUTION (by month)")
print("-" * 40)
month_counts = {}
for n in news:
    pub = n.get('published', '')[:7]
    if pub:
        month_counts[pub] = month_counts.get(pub, 0) + 1
for month, count in sorted(month_counts.items()):
    print(f"  {month}: {count} articles")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
