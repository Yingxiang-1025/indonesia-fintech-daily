import json

data = json.load(open('data/news.json', 'r', encoding='utf-8'))
akulaku = [n for n in data if 'akulaku' in n.get('sections', [])]

for i, a in enumerate(akulaku, 1):
    print(f'#{i}: {list(a.keys())}')
    print(f'  published={a.get("published", "NONE")}')
    print(f'  fetched_date={a.get("fetched_date", "NONE")}')
    print(f'  date={a.get("date", "NONE")}')
    print(f'  title={a.get("title", "")[:60]}')
    print(f'  url={a.get("url", "")[:100]}')
    print()
