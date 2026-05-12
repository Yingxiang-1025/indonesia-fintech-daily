"""Deep check: verify published dates by examining article URLs for date clues,
and check if Google News RSS published dates match URL dates."""
import json, sys, io, re, requests
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

print(f"=== INDONESIA: Deep Date Verification ({len(news)} items) ===\n")

# Sort by published date descending
news.sort(key=lambda x: x.get("published", ""), reverse=True)

mismatches = []
for n in news[:30]:  # Check most recent 30
    pub = n.get("published", "?")
    fetch = n.get("fetched_date", "?")
    url = n.get("url", "")
    title = (n.get("title_zh") or n.get("title", ""))[:55]
    
    # Extract date from URL if possible
    url_dates = re.findall(r'/(\d{4})/(\d{2})/(\d{2})/', url)
    url_date_str = None
    if url_dates:
        y, m, d = url_dates[-1]
        url_date_str = f"{y}-{m}-{d}"
    
    # Check for year in URL path
    url_years = re.findall(r'/(\d{4})/', url)
    
    mismatch = ""
    if url_date_str and url_date_str != pub:
        mismatch = f"URL says {url_date_str} but pub={pub}"
        mismatches.append((n, mismatch))
    
    # For Google News URLs, try to resolve and check actual URL
    is_google = "news.google.com" in url
    
    marker = "⚠️" if mismatch else "  "
    google_tag = "[GN]" if is_google else "[DR]"
    print(f"{marker} [{pub}] (fetch:{fetch}) {google_tag} {title}")
    if url_date_str:
        print(f"     URL date: {url_date_str}" + (f" MISMATCH!" if mismatch else " ✓"))
    if url_years and not url_date_str:
        print(f"     URL year: {url_years}")

print(f"\n--- Mismatches found: {len(mismatches)} ---")
for n, reason in mismatches:
    title = (n.get("title_zh") or n.get("title", ""))[:55]
    print(f"  {reason}: {title}")

# Check Google News URL resolution for a sample
print(f"\n--- Resolving sample Google News URLs to check real dates ---")
google_items = [n for n in news if "news.google.com" in n.get("url", "")][:3]
for n in google_items:
    url = n.get("url", "")
    pub = n.get("published", "?")
    title = (n.get("title_zh") or n.get("title", ""))[:50]
    try:
        resp = requests.head(url, allow_redirects=True, timeout=10,
                           headers={"User-Agent": "Mozilla/5.0"})
        final_url = resp.url
        # Extract date from final URL
        dates = re.findall(r'/(\d{4})/(\d{2})/(\d{2})/', final_url)
        date_in_url = f"{dates[-1][0]}-{dates[-1][1]}-{dates[-1][2]}" if dates else "none"
        match = "✓" if date_in_url == pub or date_in_url == "none" else f"MISMATCH (real: {date_in_url})"
        print(f"  pub={pub} url_date={date_in_url} {match}")
        print(f"    {title}")
        print(f"    -> {final_url[:100]}")
    except Exception as e:
        print(f"  Failed to resolve: {e}")
        print(f"    {title}")
