"""Verify the Akulaku page: dynamic items, links, dates."""
import re

lines = open('../pages/akulaku.html', 'r', encoding='utf-8').readlines()
print(f'Total lines: {len(lines)}')

in_dyn = False
item_count = 0
for i, line in enumerate(lines, 1):
    if 'DYNAMIC_NEWS_START' in line:
        in_dyn = True
        print(f'\nLine {i}: {line.strip()}')
    elif 'DYNAMIC_NEWS_END' in line:
        print(f'\nLine {i}: {line.strip()}')
        in_dyn = False
    elif in_dyn and 'section-heading' in line:
        print(f'  Heading: {line.strip()[:100]}')
    elif in_dyn and '<div class="card"' in line:
        item_count += 1
        print(f'\n  Dynamic Item #{item_count} (line {i})')
    elif in_dyn and 'card-link' in line:
        m = re.search(r'href="([^"]+)"', line)
        if m:
            url = m.group(1)
            if 'news.google.com' in url:
                status = 'BROKEN (Google News RSS)'
            elif 'google.com/search' in url:
                status = 'OK (Google Search fallback)'
            else:
                status = f'OK (direct: {url[:60]})'
            print(f'    Link: {status}')
    elif in_dyn and '<span>' in line:
        text = line.strip().replace('<span>', '').replace('</span>', '')
        if text.startswith('20'):
            print(f'    Date: {text}')

# Check curated items
print('\n\n=== CURATED ITEMS (before dynamic) ===')
curated_count = 0
for i, line in enumerate(lines, 1):
    if 'DYNAMIC_NEWS_START' in line:
        break
    if '<div class="card"' in line:
        curated_count += 1
    if 'card-link' in line and curated_count > 0:
        m = re.search(r'href="([^"]+)"', line)
        if m:
            url = m.group(1)
            if 'news.google.com' in url:
                print(f'  Curated #{curated_count}: BROKEN (Google News RSS)')
            elif url.startswith('#'):
                print(f'  Curated #{curated_count}: anchor link')
            else:
                print(f'  Curated #{curated_count}: {url[:80]}')

print(f'\nTotal curated items: {curated_count}')
print(f'Total dynamic items: {item_count}')
