"""
Configuration for Indonesia Fintech Daily Brief auto-updater.
"""
import os
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR
PAGES_DIR = OUTPUT_DIR / "pages"
DATA_DIR = Path(__file__).resolve().parent / "data"
TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"

# ─── OpenAI / LLM API (for Chinese summaries) ───────────
# Set via environment variable or .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
ENABLE_AI_SUMMARY = bool(OPENAI_API_KEY)

# ─── SerpAPI (for Google-like web search) ────────────────
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

# ─── RSS Feeds ───────────────────────────────────────────
RSS_FEEDS = [
    {
        "name": "Kontan",
        "url": "https://www.kontan.co.id/rss",
        "category": "mainstream",
    },
    {
        "name": "Bisnis.com",
        "url": "https://rss.bisnis.com/finansial",
        "category": "mainstream",
    },
    {
        "name": "CNBC Indonesia",
        "url": "https://www.cnbcindonesia.com/tech/rss",
        "category": "fintech",
    },
    {
        "name": "DailySocial",
        "url": "https://dailysocial.id/feed",
        "category": "fintech",
    },
    {
        "name": "Tech in Asia",
        "url": "https://www.techinasia.com/feed",
        "category": "fintech",
    },
    {
        "name": "Katadata",
        "url": "https://katadata.co.id/rss",
        "category": "mainstream",
    },
    {
        "name": "Detik Finance",
        "url": "https://finance.detik.com/indeks/rss",
        "category": "mainstream",
    },
]

# ─── Web Search Queries (run daily) ─────────────────────
SEARCH_QUERIES = [
    "Indonesia fintech lending news",
    "Indonesia P2P lending OJK 2026",
    "Indonesia BNPL paylater news",
    "Akulaku Indonesia news",
    "Asetku Indonesia",
    "GoPay OVO DANA fintech Indonesia",
    "Indonesia digital bank news",
    "OJK fintech regulation 2026",
    "Indonesia cash loan pinjaman online",
]

# ─── Keyword Filters ────────────────────────────────────
# News must match at least one keyword group to be included

SECTION_KEYWORDS = {
    "regulation": [
        "OJK", "Bank Indonesia", "regulasi", "POJK", "moratorium", "fintech lending",
        "P2P regulation", "consumer protection",
    ],
    "credit_card": [
        "credit card", "kartu kredit", "Mastercard", "Visa", "BCA card", "BRI card",
    ],
    "digital_lending": [
        "digital lending", "pinjaman digital", "MSME", "UKM", "fintech lending",
        "Investree", "Modalku", "KoinWorks",
    ],
    "cash_loan": [
        "cash loan", "pinjaman online", "pinjol", "AdaKami", "Kredit Pintar", "UangTeman", "Tunaiku",
    ],
    "p2p_lending": [
        "P2P", "peer-to-peer", "Asetku", "Investree", "Modalku", "Danamas", "KoinWorks", "Amartha",
        "registered lending",
    ],
    "bnpl": [
        "BNPL", "paylater", "pay later", "Kredivo", "Akulaku", "Indodana", "Atome", "Home Credit", "GoPaylater",
    ],
    "e_wallet": [
        "e-wallet", "GoPay", "OVO", "DANA", "ShopeePay", "LinkAja", "digital wallet", "dompet digital", "QRIS",
    ],
    "digital_bank": [
        "digital bank", "Bank Jago", "Allo Bank", "Bank Neo Commerce", "Sea Bank", "SuperBank", "neobank",
    ],
    "akulaku": [
        "Akulaku", "akulaku", "Asetku", "asetku", "Silvrr",
    ],
}

# Global relevance filter: an article must contain at least ONE of these
# (kept specific to fintech/finance to avoid noise like mining, politics, etc.)
GLOBAL_KEYWORDS = [
    "fintech", "lending", "pinjaman", "kredit", "digital bank", "e-wallet", "BNPL", "paylater", "GoPay", "OVO", "DANA",
    "Akulaku", "Asetku", "Kredivo", "OJK", "Bank Indonesia", "QRIS", "P2P", "fintech lending", "digital payment",
    "dompet digital", "neobank",
]

# ─── Section → HTML page mapping ────────────────────────
SECTION_PAGES = {
    "regulation": "regulation.html",
    "credit_card": "credit-card.html",
    "digital_lending": "digital-lending.html",
    "cash_loan": "cash-loan.html",
    "p2p_lending": "p2p-lending.html",
    "bnpl": "bnpl.html",
    "e_wallet": "e-wallet.html",
    "digital_bank": "digital-bank.html",
    "akulaku": "akulaku.html",
}

# ─── Tag styling classes ─────────────────────────────────
SECTION_TAG_CLASSES = {
    "regulation": "tag-regulation",
    "credit_card": "tag-product",
    "digital_lending": "tag-funding",
    "cash_loan": "tag-product",
    "p2p_lending": "tag-funding",
    "bnpl": "tag-market",
    "e_wallet": "tag-product",
    "digital_bank": "tag-product",
    "akulaku": "tag-akulaku",
}

SECTION_DISPLAY_NAMES = {
    "regulation": "监管动态",
    "credit_card": "信用卡",
    "digital_lending": "数字信贷",
    "cash_loan": "现金贷",
    "p2p_lending": "P2P借贷",
    "bnpl": "先买后付",
    "e_wallet": "电子钱包",
    "digital_bank": "数字银行",
    "akulaku": "Akulaku专题",
}
