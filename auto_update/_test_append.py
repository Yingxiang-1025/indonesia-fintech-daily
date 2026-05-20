"""Test the dynamic append logic."""
import sys, io, logging
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
logging.basicConfig(level=logging.DEBUG)

from pathlib import Path

content = Path("../pages/akulaku.html").read_text(encoding="utf-8")
print(f"File length: {len(content)}")
print(f"Has CURATED: {'<!-- CURATED -->' in content}")
print(f"Has DYNAMIC_NEWS_START: {'<!-- DYNAMIC_NEWS_START -->' in content}")

footer = '<div class="footer">'
print(f"Has footer: {footer in content}")

if footer in content:
    idx = content.rfind(footer)
    before_footer = content[:idx].rstrip()
    print(f"before_footer ends with: ...{before_footer[-20:]!r}")
    print(f"endswith </div>: {before_footer.endswith('</div>')}")

# Test the actual function
from generator import generate_all_pages, _append_dynamic_news_to_curated
from fetcher import load_existing_news
from config import SECTION_PAGES
from datetime import datetime

news = load_existing_news()
sections = {key: [] for key in SECTION_PAGES}
for item in news:
    for sec in item.get("sections", []):
        if sec in sections:
            if "akulaku" in item.get("sections", []) and sec != "akulaku":
                continue
            sections[sec].append(item)

print(f"\nAkulaku section items: {len(sections.get('akulaku', []))}")
for n in sections.get("akulaku", [])[:3]:
    print(f"  [{n.get('published')}] {(n.get('title_zh') or n.get('title',''))[:50]}")

context = {"today_str": datetime.now().strftime("%Y-%m-%d")}
output_path = Path("../pages/akulaku.html")
_append_dynamic_news_to_curated(output_path, sections.get("akulaku", []), context)
print("\nDone! Check akulaku.html")
