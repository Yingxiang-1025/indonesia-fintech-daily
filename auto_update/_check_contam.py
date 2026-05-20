import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

news = json.load(open('data/news.json', 'r', encoding='utf-8'))

for n in news:
    title = n.get('title', '')
    if 'Kredivo Group Acquires' in title or 'AdaKami Contributes' in title:
        print(f"Title: {title}")
        print(f"Published: {n.get('published', '')}")
        print(f"Source: {n.get('source', '')}")
        print(f"Sections: {n.get('sections', [])}")
        summary = n.get('summary', '')[:200].replace('\xa0', ' ')
        print(f"Summary: {summary}")
        print()
