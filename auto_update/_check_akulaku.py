import json

data = json.load(open('data/news.json', 'r', encoding='utf-8'))
akulaku = [n for n in data if 'akulaku' in n.get('sections', [])]
print(f'Total Akulaku articles in news.json: {len(akulaku)}')
for a in akulaku:
    title = a.get('title_zh', a.get('title', ''))[:60]
    url = a.get('url', '')
    date = a.get('date', '?')
    fetched = a.get('fetched_date', '?')
    print(f'  [{date}] (fetched:{fetched}) {title}')
    print(f'    URL: {url[:120]}')
    print()
