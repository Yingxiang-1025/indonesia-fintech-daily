"""Manually trigger push for today's fetched items."""
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, ".")
from datetime import datetime
from notifier import send_wechat_notification

with open("data/news.json", "r", encoding="utf-8") as f:
    news = json.load(f)

today = datetime.now().strftime("%Y-%m-%d")
push_items = [n for n in news if n.get("fetched_date") == today]
print(f"Push items (fetched today): {len(push_items)}")
if push_items:
    ok = send_wechat_notification(push_items, today)
    print(f"Push result: {'OK' if ok else 'FAILED'}")
else:
    print("No items to push")
