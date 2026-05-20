"""Test decoding Google News article URLs."""
import json, sys, io, base64, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

gn_items = [n for n in news if "news.google.com" in n.get("url", "")]
print(f"Google News URLs to decode: {len(gn_items)}\n")

def decode_google_news_url(gn_url):
    """Try to decode the actual URL from a Google News article URL."""
    match = re.search(r'/articles/([^?]+)', gn_url)
    if not match:
        return None
    article_id = match.group(1)
    try:
        padding = 4 - len(article_id) % 4
        if padding != 4:
            article_id += '=' * padding
        decoded = base64.urlsafe_b64decode(article_id)
        urls = re.findall(rb'https?://[^\x00-\x1f\x7f-\x9f"<>\s]+', decoded)
        if urls:
            real_url = urls[0].decode('utf-8', errors='ignore')
            real_url = real_url.rstrip('/')
            if 'news.google.com' not in real_url:
                return real_url
    except Exception:
        pass
    return None

decoded = 0
for n in gn_items[:20]:
    url = n.get("url", "")
    title = (n.get("title_zh") or n.get("title", ""))[:55]
    result = decode_google_news_url(url)
    if result:
        decoded += 1
        print(f"✅ {title}")
        print(f"   -> {result[:90]}")
    else:
        print(f"❌ {title}")
        print(f"   raw: {url[:80]}")
    print()

print(f"\nDecoded: {decoded}/{min(len(gn_items), 20)}")
