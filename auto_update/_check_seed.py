import json

seed = json.load(open('data/seed_news.json', 'r', encoding='utf-8'))
akulaku_seed = [n for n in seed if 'akulaku' in n.get('sections', [])]
print(f'Akulaku items in seed_news.json: {len(akulaku_seed)}')
for i, a in enumerate(akulaku_seed, 1):
    print(f'  #{i}: [{a.get("published","?")}] {a.get("title","")[:60]}')
    print(f'       URL: {a.get("url","")[:100]}')
