import json, sys, io
from datetime import datetime, timedelta
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, ".")
from notifier import build_message

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

today = datetime.now().strftime("%Y-%m-%d")
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

yn = [n for n in news if n.get("published") == yesterday]
tn = [n for n in news if n.get("published") == today]
push = yn + tn

print(f"=== ID ALIGNMENT CHECK ===")
print(f"Yesterday ({yesterday}): {len(yn)} items")
for n in yn:
    tz = n.get("title_zh") or n.get("title", "")
    print(f"  - {tz[:60]}")
print(f"Today ({today}): {len(tn)} items")
for n in tn:
    tz = n.get("title_zh") or n.get("title", "")
    print(f"  - {tz[:60]}")
print(f"Total push: {len(push)}")
