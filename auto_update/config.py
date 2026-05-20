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
    # Verified working (2026-05-20)
    {"name": "CNBC Indonesia Tech", "url": "https://www.cnbcindonesia.com/tech/rss", "category": "fintech"},
    {"name": "CNBC ID Finance", "url": "https://www.cnbcindonesia.com/market/rss", "category": "mainstream"},
    {"name": "DailySocial", "url": "https://dailysocial.id/feed", "category": "fintech"},
    {"name": "Katadata", "url": "https://katadata.co.id/rss", "category": "mainstream"},
    {"name": "Tempo Business", "url": "https://rss.tempo.co/bisnis", "category": "mainstream"},
    {"name": "Detik Finance", "url": "https://finance.detik.com/rss", "category": "mainstream"},
    {"name": "Fintech News SG", "url": "https://fintechnews.sg/feed/", "category": "fintech"},
    {"name": "Fintech News MY", "url": "https://fintechnews.my/feed/", "category": "fintech"},
    {"name": "e27", "url": "https://e27.co/feed/", "category": "fintech"},
]

# ─── Web Search Queries (run daily) ─────────────────────
SEARCH_QUERIES = [
    # General fintech
    "Indonesia fintech lending news",
    "Indonesia P2P lending OJK 2026",
    "Indonesia BNPL paylater news",
    "Indonesia digital bank news",
    "Indonesia cash loan pinjaman online",
    # Brand tracking - English
    "Akulaku Indonesia news",
    "Kredivo Indonesia news",
    "Home Credit Indonesia fintech",
    "ShopeePay Indonesia news",
    "GoPay OVO digital payment Indonesia",
    "GoPayLater paylater Indonesia",
    "Indodana Atome Indonesia",
    # Brand tracking - Indonesian
    "Akulaku berita terbaru",
    "Kredivo pinjaman Indonesia",
    "pinjol legal OJK terdaftar 2026",
    # OJK regulatory depth
    "OJK fintech regulation 2026",
    "OJK sanksi fintech lending",
    "OJK daftar P2P lending terbaru",
    # Indonesian language queries
    "fintek Indonesia berita terbaru",
    "pembayaran digital QRIS Indonesia",
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

# Global relevance filter: article must match at least 1 keyword
GLOBAL_KEYWORDS = [
    # English
    "fintech", "lending", "pinjaman", "kredit", "digital bank", "e-wallet",
    "BNPL", "paylater", "GoPay", "OVO",
    "Akulaku", "Asetku", "Kredivo", "OJK", "Bank Indonesia", "QRIS",
    "P2P", "fintech lending", "digital payment", "dompet digital", "neobank",
    # Brands
    "ShopeePay", "GoPayLater", "LinkAja", "Indodana", "Atome", "Home Credit",
    "Bank Jago", "Sea Bank", "Allo Bank", "AdaKami", "Kredit Pintar",
    "Danamas", "Amartha", "KoinWorks", "Modalku", "Investree",
    # Indonesian
    "pinjol", "fintek", "bank digital", "pembayaran digital",
    "kartu kredit", "pinjaman online", "suku bunga",
    "regulasi keuangan", "inklusi keuangan", "teknologi keuangan",
]

# Keywords that require word-boundary matching to avoid false positives
# e.g. "DANA" should not match "Danantara"
WORD_BOUNDARY_KEYWORDS = ["DANA"]

EXCLUDE_KEYWORDS = [
    "PAYPAYA", "เพย์พาญ่า", "Bank of Thailand", "BOT Thailand",
    "PromptPay", "TrueMoney", "กู้เงิน", "สินเชื่อ",
    "BSP Philippines", "Bangko Sentral", "Philippines fintech",
    "UnionBank Philippines", "GCash", "Maya Philippines",
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
