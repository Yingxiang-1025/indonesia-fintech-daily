"""Fix Akulaku articles: remove pre-2026 items and broken URLs."""
import json

# Fix news.json
news = json.load(open('data/news.json', 'r', encoding='utf-8'))
before = len(news)

to_remove = []
for i, n in enumerate(news):
    if 'akulaku' not in n.get('sections', []):
        continue
    url = n.get('url', '')
    title = n.get('title', '')
    
    # Remove Asetku homepage (broken DNS)
    if url == 'https://asetku.com/':
        to_remove.append(i)
        print(f"REMOVE: Asetku homepage - {title[:60]}")
    
    # Remove DailySocial (actual pub date is 2024-03-22, not 2026)
    if 'akulaku-dikabarkan-dapat-fasilitas-debt' in url:
        to_remove.append(i)
        print(f"REMOVE: DailySocial pre-2026 - {title[:60]}")

news = [n for i, n in enumerate(news) if i not in to_remove]
print(f"\nnews.json: {before} -> {len(news)} items")

with open('data/news.json', 'w', encoding='utf-8') as f:
    json.dump(news, f, ensure_ascii=False, indent=2)

# Fix seed_news.json
seed = json.load(open('data/seed_news.json', 'r', encoding='utf-8'))
before_seed = len(seed)

seed = [n for n in seed if n.get('url') not in [
    'https://asetku.com/',
    'https://news.dailysocial.id/post/akulaku-dikabarkan-dapat-fasilitas-debt-rp15-triliun-dari-hsbc/'
]]
print(f"seed_news.json: {before_seed} -> {len(seed)} items")

with open('data/seed_news.json', 'w', encoding='utf-8') as f:
    json.dump(seed, f, ensure_ascii=False, indent=2)

# Verify remaining Akulaku items
news = json.load(open('data/news.json', 'r', encoding='utf-8'))
akulaku = [n for n in news if 'akulaku' in n.get('sections', [])]
print(f"\nRemaining Akulaku articles: {len(akulaku)}")
for a in akulaku:
    print(f"  [{a.get('published','?')}] {a.get('title','')[:60]}")
    print(f"    URL: {a.get('url','')[:100]}")
