import json
import requests

data = json.load(open('data/news.json', 'r', encoding='utf-8'))
akulaku = [n for n in data if 'akulaku' in n.get('sections', [])]

print(f'=== Akulaku articles in news.json: {len(akulaku)} ===\n')
for i, a in enumerate(akulaku, 1):
    title = a.get('title_zh', a.get('title', ''))
    url = a.get('url', '')
    date = a.get('date', 'MISSING')
    fetched = a.get('fetched_date', 'MISSING')
    source = a.get('source', 'MISSING')
    print(f'#{i}:')
    print(f'  Title: {title[:80]}')
    print(f'  Date: {date} | Fetched: {fetched} | Source: {source}')
    print(f'  URL: {url[:150]}')
    
    # Test if URL is accessible
    try:
        resp = requests.head(url, timeout=5, allow_redirects=True)
        final_url = resp.url
        print(f'  Status: {resp.status_code} | Final: {final_url[:120]}')
    except Exception as e:
        print(f'  Status: ERROR - {e}')
    print()
