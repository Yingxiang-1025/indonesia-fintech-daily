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
    # Indonesian mainstream financial media
    {"name": "CNBC Indonesia Tech", "url": "https://www.cnbcindonesia.com/tech/rss", "category": "fintech"},
    {"name": "CNBC ID Finance", "url": "https://www.cnbcindonesia.com/market/rss", "category": "mainstream"},
    {"name": "DailySocial", "url": "https://dailysocial.id/feed", "category": "fintech"},
    {"name": "Katadata", "url": "https://katadata.co.id/rss", "category": "mainstream"},
    {"name": "Tempo Business", "url": "https://rss.tempo.co/bisnis", "category": "mainstream"},
    {"name": "Detik Finance", "url": "https://finance.detik.com/rss", "category": "mainstream"},
    {"name": "Bisnis.com", "url": "https://www.bisnis.com/rss", "category": "mainstream"},
    {"name": "Kontan", "url": "https://www.kontan.co.id/rss", "category": "mainstream"},
    {"name": "Kompas Tech", "url": "https://tekno.kompas.com/rss", "category": "mainstream"},
    {"name": "Liputan6 Bisnis", "url": "https://www.liputan6.com/feed/rss2/bisnis", "category": "mainstream"},
    {"name": "IDN Times Business", "url": "https://www.idntimes.com/rss/business", "category": "mainstream"},
    # Regional / English fintech media
    {"name": "Fintech News SG", "url": "https://fintechnews.sg/feed/", "category": "fintech"},
    {"name": "Fintech News MY", "url": "https://fintechnews.my/feed/", "category": "fintech"},
    {"name": "e27", "url": "https://e27.co/feed/", "category": "fintech"},
    {"name": "Tech in Asia", "url": "https://www.techinasia.com/feed", "category": "fintech"},
    # Akulaku / brand-specific Google News RSS
    {"name": "GN Akulaku", "url": "https://news.google.com/rss/search?q=Akulaku+Indonesia&hl=en&gl=ID&ceid=ID:en", "category": "akulaku"},
    {"name": "GN Kredivo", "url": "https://news.google.com/rss/search?q=Kredivo+Indonesia&hl=en&gl=ID&ceid=ID:en", "category": "bnpl"},
    {"name": "GN HomeCredit ID", "url": "https://news.google.com/rss/search?q=%22Home+Credit%22+Indonesia&hl=en&gl=ID&ceid=ID:en", "category": "bnpl"},
    {"name": "GN BNPL ID", "url": "https://news.google.com/rss/search?q=BNPL+paylater+Indonesia&hl=en&gl=ID&ceid=ID:en", "category": "bnpl"},
    {"name": "GN Pinjol", "url": "https://news.google.com/rss/search?q=pinjol+OJK+2026&hl=id&gl=id&ceid=ID:id", "category": "cash_loan"},
]

# ─── Web Search Queries (run daily) ─────────────────────
SEARCH_QUERIES = [
    # ── Akulaku Group (highest priority, 12 queries) ──
    "Akulaku Indonesia news 2026",
    "PT Akulaku Finance Indonesia",
    "Akulaku BNPL growth Indonesia",
    "Akulaku Asetku Silvrr fintech",
    "Akulaku berita terbaru Indonesia",
    "Akulaku OneAsia fintech Indonesia",
    "Akulaku multifinance OJK",
    "Akulaku paylater Indonesia terbaru",
    "Akulaku kredit digital Indonesia",
    "PT Akulaku Silvrr Group Indonesia",
    "Akulaku annual report Indonesia",
    "Akulaku partnership Indonesia 2026",
    # ── OJK & Regulation (fintech-focused) ──
    "OJK fintech regulation 2026",
    "OJK sanksi fintech lending",
    "OJK daftar P2P lending terbaru",
    "OJK kebijakan pinjol terbaru 2026",
    "OJK regulasi BNPL paylater 2026",
    "Bank Indonesia QRIS pembayaran digital 2026",
    # ── BNPL / Peer brands - English (expanded) ──
    "Kredivo Indonesia news 2026",
    "Kredivo BNPL paylater growth Indonesia",
    "Home Credit Indonesia fintech news",
    "Home Credit Indonesia BNPL 2026",
    "ShopeePay Indonesia news 2026",
    "GoPaylater GoPayLater Indonesia",
    "GoPaylater Gojek paylater terbaru",
    "Indodana Atome Indonesia BNPL",
    "Atome Indonesia BNPL paylater 2026",
    "Kredit Pintar AdaKami Indonesia",
    "JULO fintech lending Indonesia",
    "Bank Jago Sea Bank digital Indonesia",
    "DANA e-wallet Indonesia news",
    "OVO digital payment Indonesia 2026",
    "LinkAja Indonesia digital payment",
    # ── BNPL / Peer brands - Indonesian ──
    "Kredivo pinjaman Indonesia terbaru",
    "Kredivo cicilan tanpa kartu kredit",
    "Home Credit cicilan Indonesia terbaru",
    "ShopeePay promo terbaru Indonesia",
    "GoPay QRIS pembayaran digital",
    "DANA dompet digital terbaru",
    "OVO promo cashback Indonesia",
    "Atome cicilan Indonesia 2026",
    "paylater Indonesia perbandingan terbaru",
    # ── General fintech - English ──
    "Indonesia fintech lending news",
    "Indonesia P2P lending OJK 2026",
    "Indonesia BNPL paylater news 2026",
    "Indonesia digital bank news 2026",
    "Indonesia cash loan pinjaman online",
    # ── General fintech - Indonesian ──
    "pinjaman online OJK terdaftar 2026",
    "fintek Indonesia berita terbaru",
    "BNPL Indonesia berita terbaru",
    "dompet digital Indonesia 2026",
    "pinjol legal OJK terbaru",
    "kredit digital Indonesia fintek",
    "pembayaran digital QRIS Indonesia",
    "bank digital Indonesia terbaru",
]

# ─── Keyword Filters ────────────────────────────────────
# News must match at least one keyword group to be included

SECTION_KEYWORDS = {
    "regulation": [
        "POJK", "moratorium", "fintech lending", "P2P regulation", "consumer protection",
        "regulasi fintek", "regulasi pinjol", "regulasi pinjaman online",
        "regulasi BNPL", "regulasi paylater", "regulasi dompet digital",
        "aturan fintech", "aturan pinjol", "kebijakan fintech",
        "sanksi fintech", "sanksi pinjol", "izin fintech",
        "fintech regulation", "lending regulation", "digital payment regulation",
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
        "BNPL", "paylater", "pay later", "Kredivo", "Akulaku", "Indodana", "Atome",
        "Home Credit", "GoPaylater", "GoPayLater", "cicilan", "installment",
        "buy now pay later", "beli sekarang bayar nanti",
    ],
    "e_wallet": [
        "e-wallet", "GoPay", "OVO", "DANA", "ShopeePay", "LinkAja",
        "digital wallet", "dompet digital", "QRIS", "mobile payment",
        "pembayaran digital", "cashless",
    ],
    "digital_bank": [
        "digital bank", "Bank Jago", "Allo Bank", "Bank Neo Commerce", "Sea Bank", "SuperBank", "neobank",
    ],
    "akulaku": [
        "Akulaku", "akulaku", "Asetku", "asetku", "Silvrr", "silvrr",
        "OneAsia", "oneasia", "PT Pintar Inovasi Digital",
        "PT Akulaku Finance",
    ],
}

# Global relevance filter: article must match at least 1 keyword
GLOBAL_KEYWORDS = [
    # English core
    "fintech", "lending", "pinjaman", "kredit", "digital bank", "e-wallet",
    "BNPL", "paylater", "GoPay",
    "QRIS",
    "P2P", "fintech lending", "digital payment", "dompet digital", "neobank",
    # Akulaku group
    "Akulaku", "Asetku", "Silvrr", "OneAsia",
    "PT Akulaku Finance", "PT Pintar Inovasi Digital",
    # Peer brands - BNPL / lending
    "Kredivo", "Home Credit", "GoPayLater", "GoPaylater", "Indodana", "Atome",
    "AdaKami", "Kredit Pintar", "JULO", "UangTeman", "Tunaiku",
    # Peer brands - e-wallet / payment
    "ShopeePay", "LinkAja", "Sea Money",
    # Peer brands - digital bank
    "Bank Jago", "Sea Bank", "Allo Bank", "SuperBank",
    # Peer brands - P2P / SME lending
    "Danamas", "Amartha", "KoinWorks", "Modalku", "Investree",
    # Indonesian
    "pinjol", "fintek", "bank digital", "pembayaran digital",
    "kartu kredit", "pinjaman online",
    "inklusi keuangan", "teknologi keuangan",
    "cicilan", "kredit digital",
]

# Keywords that require word-boundary matching to avoid false positives
WORD_BOUNDARY_KEYWORDS = ["DANA", "OVO", "JULO"]

# Indonesia geographic keywords — used to filter regional sources
INDONESIA_GEO_KEYWORDS = [
    "indonesia", "indonesian", "jakarta", "ojk", "rupiah",
    "印尼", "印度尼西亚", "雅加达",
    "tokopedia", "gojek", "goto", "bukalapak", "shopee indonesia",
    "bank indonesia", "ihsg", "kemenkominfo",
    "akulaku", "asetku", "silvrr", "oneasia", "kredivo", "adakami", "kredit pintar",
    "gopay", "shopeepay", "linkaja", "dana indonesia", "sea money",
    "home credit indonesia", "indodana", "atome indonesia",
    "pinjol", "pinjaman online", "fintek", "cicilan",
    "bank jago", "sea bank", "allo bank", "superbank", "bank neo commerce",
    "koinworks", "modalku", "investree", "amartha", "danamas",
    "julo", "uangteman", "tunaiku",
]
# Short keywords that need word-boundary matching to avoid substring false positives
INDONESIA_GEO_WORD_BOUNDARY = ["bri", "bni", "bca", "ovo", "idr", "idx"]

# RSS sources that cover the whole region (not Indonesia-specific)
# Articles from these must also match INDONESIA_GEO_KEYWORDS
REGIONAL_SOURCES = [
    "Fintech News SG", "Fintech News MY", "e27",
    "fintechnews.sg", "fintechnews.my", "e27.co",
]

# Insurance / securities regulation keywords — these stay in the regulation
# section page but are excluded from yesterday/monthly summaries and
# treated as low-priority "other" in WeChat push.
# Macro-economic keywords — regulation items matching these (without fintech
# keywords) are excluded from regulation section, kept only if they match
# other fintech sections.
MACRO_EXCLUDE_KEYWORDS = [
    "suku bunga acuan", "BI rate", "BI 7-day", "7-Day Reverse Repo",
    "inflasi", "inflation", "deflasi",
    "nilai tukar", "exchange rate", "kurs rupiah", "USD/IDR",
    "cadangan devisa", "foreign reserve",
    "neraca perdagangan", "trade balance",
    "pertumbuhan ekonomi", "GDP", "PDB",
    "JCI", "IHSG",
]

# Maximum number of regulation items in daily/monthly summaries
REGULATION_DAILY_CAP = 5

INSURANCE_SECURITIES_KEYWORDS = [
    # Insurance (English + Indonesian)
    "insurance", "asuransi", "reinsurance", "reasuransi",
    "life insurance", "asuransi jiwa", "health insurance", "asuransi kesehatan",
    "underwriting", "actuarial", "premi asuransi", "klaim asuransi",
    "AAUI", "AAJI",
    # Securities / Capital market (English + Indonesian)
    "securities", "efek", "stock exchange", "bursa efek",
    "capital market", "pasar modal", "IPO", "saham",
    "bond", "obligasi", "mutual fund", "reksa dana", "reksadana",
    "IHSG", "IDX", "BEI", "securities commission",
    "stock manipulation", "insider trading",
    "emiten", "waran", "right issue",
]

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
