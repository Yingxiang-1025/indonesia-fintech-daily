"""
Built-in English→Chinese translation for fintech news.
Uses Google Translate (free, via deep-translator) for full-sentence translation.
Falls back to clean English if translation unavailable.
"""
import logging
import time

logger = logging.getLogger(__name__)

_translator = None


def _get_translator():
    global _translator
    if _translator is None:
        try:
            from deep_translator import GoogleTranslator
            _translator = GoogleTranslator(source="en", target="zh-CN")
            logger.info("Google Translator initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to init Google Translator: {e}")
    return _translator


def google_translate(text: str) -> str:
    """Translate English text to Chinese via free Google Translate.
    Returns original text unchanged on any failure."""
    if not text or not text.strip():
        return text
    translator = _get_translator()
    if not translator:
        return text
    try:
        chunk = text[:4500] if len(text) > 4500 else text
        result = translator.translate(chunk)
        time.sleep(0.35)
        return result if result else text
    except Exception as e:
        logger.warning(f"Google Translate failed: {e}")
        return text


SOURCE_MAP = {
    "Kontan": "Kontan财经",
    "Bisnis.com": "Bisnis商业",
    "CNBC Indonesia": "CNBC印尼",
    "DailySocial": "DailySocial科技",
    "Tech in Asia": "Tech in Asia",
    "Katadata": "Katadata数据",
    "Detik Finance": "Detik财经",
    "Google News": "谷歌新闻",
    "Jakarta Post": "雅加达邮报",
}


def _title_prefix(title: str) -> str:
    """Determine a Chinese category prefix based on English title keywords."""
    t = title.lower()
    if "akulaku" in t or "asetku" in t:
        return "【Akulaku】"
    if any(
        k in t
        for k in [
            "ojk ", " bank indonesia", "regulasi", "regulation", "moratorium",
            "oversight", "compliance", "pojk",
        ]
    ):
        return "【监管】"
    if any(
        k in t
        for k in [
            "p2p", "peer-to-peer", "peer to peer", "asetku", "investree", "modalku",
            "danamas", "amartha", "registered lending",
        ]
    ):
        return "【P2P】"
    if any(
        k in t
        for k in [
            "e-wallet", "e wallet", "gopay", "ovo ", " dana", "shopeepay", "linkaja",
            "dompet digital", "digital wallet", "qris",
        ]
    ):
        return "【电子钱包】"
    if any(k in t for k in ["credit card", "mastercard", "visa ", "kartu kredit"]):
        return "【信用卡】"
    if any(
        k in t
        for k in [
            "bnpl", "buy now pay later", "paylater", "pay later", "kredivo", "indodana",
        ]
    ):
        return "【BNPL】"
    if any(
        k in t
        for k in [
            "cash loan", "pinjaman online", "pinjol", "tunaiku", "kredit pintar", "uangteman", "adakami",
        ]
    ):
        return "【现金贷】"
    if any(
        k in t
        for k in [
            "digital bank", "bank jago", "allo bank", "neo commerce", "sea bank", "superbank", "neobank",
        ]
    ):
        return "【数字银行】"
    if any(
        k in t
        for k in [
            "lending", "loan", "kredit", "pinjaman", "msme", "ukm", "financing", "fintech lending",
        ]
    ):
        return "【信贷】"
    if any(k in t for k in ["raises", "funding", "investment", " million", " billion"]):
        return "【融资】"
    if any(k in t for k in ["fintech", "digital", "payment", "qris", "remittance"]):
        return "【金融科技】"
    return "【金融科技】"


def translate_title(title: str) -> str:
    """Translate title to Chinese with a category prefix."""
    prefix = _title_prefix(title)
    zh = google_translate(title)
    return f"{prefix} {zh}"


def translate_summary(summary: str) -> str:
    """Translate summary to Chinese using Google Translate."""
    if not summary:
        return summary
    return google_translate(summary)


def translate_source(source: str) -> str:
    """Translate source name to Chinese (exact-match dictionary)."""
    return SOURCE_MAP.get(source, source)


def translate_news_item(item: dict) -> dict:
    """Translate a news item dict in-place. Always re-translates title and source;
    only translates summary_zh if it's missing or still identical to English."""
    summary_zh = item.get("summary_zh", "")
    summary_en = item.get("summary", "")

    needs_summary_translation = (
        not summary_zh
        or summary_zh == summary_en
        or _looks_garbled(summary_zh)
    )
    if needs_summary_translation:
        item["summary_zh"] = translate_summary(summary_en)

    item["title_zh"] = translate_title(item.get("title", ""))
    item["source_zh"] = translate_source(item.get("source", ""))
    return item


def _looks_garbled(text: str) -> bool:
    """Detect garbled translations from the old TERM_MAP approach."""
    markers = ["SEC(证监会)", "BSP(央行)", "人工智能(AI)", "先买后付(BNPL)", "中小微企业(MSME)"]
    return any(m in text for m in markers)
