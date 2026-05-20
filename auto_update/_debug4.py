import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
news = json.load(open("data/news.json", "r", encoding="utf-8"))
n = [x for x in news if "Paymentology" in x.get("title", "")][0]
all_text = " ".join([
    n.get("title", ""), n.get("summary", ""),
    n.get("title_zh", ""), n.get("summary_zh", ""),
]).lower()
idx = all_text.find("bri")
if idx >= 0:
    print(f"Found 'bri' at position {idx}")
    print(f"Context: ...{all_text[max(0,idx-20):idx+20]}...")
else:
    print("'bri' NOT found in all_text")
    print(f"all_text length: {len(all_text)}")
    print(f"Full text:\n{all_text[:500]}")
