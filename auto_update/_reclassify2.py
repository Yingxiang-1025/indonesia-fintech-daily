"""Re-classify all items with updated regulation keywords."""
import json
from collections import Counter
from config import SECTION_KEYWORDS

with open("data/news.json", "r", encoding="utf-8") as f:
    all_news = json.load(f)

akulaku_group = ["akulaku", "asetku", "silvrr", "oneasia",
                 "pt pintar inovasi digital", "pt akulaku finance"]

before_reg = sum(1 for n in all_news if "regulation" in n.get("sections", []))

for item in all_news:
    text = (item.get("title", "") + " " + item.get("summary", "")).lower()
    matched = []
    for section, keywords in SECTION_KEYWORDS.items():
        if any(kw.lower() in text for kw in keywords):
            matched.append(section)
    if not matched:
        matched = ["digital_lending"]
    if any(kw in text for kw in akulaku_group):
        if "akulaku" not in matched:
            matched.append("akulaku")
    item["sections"] = matched

after_reg = sum(1 for n in all_news if "regulation" in n.get("sections", []))

with open("data/news.json", "w", encoding="utf-8") as f:
    json.dump(all_news, f, ensure_ascii=False, indent=2)

# Verify immediately after write
with open("data/news.json", "r", encoding="utf-8") as f:
    verify = json.load(f)
verify_reg = sum(1 for n in verify if "regulation" in n.get("sections", []))

print(f"Before: {before_reg} regulation items")
print(f"After:  {after_reg} regulation items")
print(f"Verify: {verify_reg} regulation items (re-read from disk)")
print(f"Total:  {len(all_news)} items")

section_counts = Counter()
for item in verify:
    for sec in item.get("sections", []):
        section_counts[sec] += 1

names = {
    "regulation": "监管动态", "credit_card": "信用卡", "digital_lending": "数字信贷",
    "cash_loan": "现金贷", "p2p_lending": "P2P借贷", "bnpl": "先买后付(BNPL)",
    "e_wallet": "电子钱包", "digital_bank": "数字银行", "akulaku": "Akulaku专题",
}
print("\n--- 板块分布 ---")
for sec, count in section_counts.most_common():
    name = names.get(sec, sec)
    pct = count / len(verify) * 100
    print(f"  {name:15s} {count:4d} ({pct:5.1f}%)")
