"""Verify actual publication dates for remaining Akulaku articles via Google Search."""
import requests
import re
from urllib.parse import quote

articles = [
    {
        "name": "Business Wire - Indonesia Alternative Lending Market Report",
        "title": "Indonesia Alternative Lending Market Report 2025: Growth Driven by Regulatory Tightening",
        "source": "Business Wire",
        "our_date": "2026-01-05",
    },
    {
        "name": "Tech in Asia - Akulaku bets on Tier 2,3",
        "title": "Akulaku bets on Indonesia's Tier 2, 3 cities for BNPL growth",
        "source": "Tech in Asia",
        "our_date": "2026-05-04",
    },
    {
        "name": "inkl - From Akulaku to Skyro",
        "title": "From Akulaku to Skyro: Why Fintech Lenders Are More Popular Than Banks in Southeast Asia",
        "source": "inkl",
        "our_date": "2026-04-27",
    },
]

for art in articles:
    print(f"=== {art['name']} ===")
    print(f"  Our date: {art['our_date']}")
    
    # Search for the article
    query = f"{art['title']} {art['source']} site:{art['source'].lower().replace(' ', '')}.com"
    search_url = f"https://www.google.com/search?q={quote(art['title'][:80])}"
    print(f"  Search: {search_url[:120]}")
    print()
