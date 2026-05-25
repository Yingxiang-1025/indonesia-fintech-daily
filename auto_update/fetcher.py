"""
News fetcher module: RSS feeds + web search.
"""
import json
import logging
import re
import time
from datetime import datetime, timedelta
from typing import Optional

import feedparser
import requests
from dateutil import parser as date_parser

from config import (
    DATA_DIR,
    EXCLUDE_KEYWORDS,
    GLOBAL_KEYWORDS,
    INDONESIA_GEO_KEYWORDS,
    INDONESIA_GEO_WORD_BOUNDARY,
    REGIONAL_SOURCES,
    RSS_FEEDS,
    SEARCH_QUERIES,
    SERPAPI_KEY,
)

logger = logging.getLogger(__name__)


def _resolve_google_news_url(gn_url: str) -> str:
    """Resolve a Google News RSS redirect URL to the actual article URL.
    Uses googlenewsdecoder library first, then falls back to HTTP redirect."""
    if "news.google.com" not in gn_url:
        return gn_url
    try:
        from googlenewsdecoder import gnewsdecoder
        result = gnewsdecoder(gn_url, interval=0.5)
        if result.get("status") and result.get("decoded_url"):
            logger.debug(f"Decoded Google News URL: {result['decoded_url'][:80]}")
            return result["decoded_url"]
    except Exception as e:
        logger.debug(f"gnewsdecoder failed: {e}")
    try:
        resp = requests.get(
            gn_url, allow_redirects=True, timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html",
            },
            stream=True,
        )
        resp.close()
        final = resp.url
        if final and "news.google.com" not in final:
            return final
    except Exception:
        pass
    return gn_url


def _extract_date_from_url(url: str) -> str | None:
    """Extract YYYY-MM-DD from a URL path like /2026/05/10/article."""
    m = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", url)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return None


def _url_date_conflicts(url: str, pub_date_str: str) -> bool:
    """Return True if URL path contains a year that conflicts with published date."""
    if not url or not pub_date_str:
        return False
    url_years = re.findall(r"/(\d{4})/", url)
    if not url_years:
        return False
    try:
        pub_year = int(pub_date_str[:4])
    except (ValueError, IndexError):
        return False
    for y_str in url_years:
        y = int(y_str)
        if y < 2026 and abs(pub_year - y) > 1:
            logger.warning(
                f"URL date conflict: URL year {y} vs published {pub_date_str} "
                f"for {url[:80]}"
            )
            return True
    return False


# Sources that aggregate/republish content — dates may not be original
AGGREGATOR_SOURCES = ["MSN", "msn.com", "TradingView", "tradingview.com",
                      "Yahoo", "yahoo.com", "InvestorTrust"]

_MONTH_NAMES = {
    "januari": "01", "februari": "02", "maret": "03", "april": "04",
    "mei": "05", "juni": "06", "juli": "07", "agustus": "08",
    "september": "09", "oktober": "10", "november": "11", "desember": "12",
    "january": "01", "february": "02", "march": "03", "may": "05",
    "june": "06", "july": "07", "august": "08", "october": "10",
    "december": "12",
}


def _is_old_event_article(title: str, url: str) -> bool:
    """Detect articles about pre-2026 events based on title/URL patterns
    like 'pada Oktober 2025' or 'per November 2025'."""
    combined = (title + " " + url).lower()
    for month_name in _MONTH_NAMES:
        for pat in [
            rf"(?:pada|per|bulan|in)\s+{month_name}\s+(\d{{4}})",
            rf"{month_name}[-\s]+(\d{{4}})",
        ]:
            m = re.search(pat, combined)
            if m:
                year = int(m.group(1))
                if year < 2026:
                    has_in_url = any(
                        mn in url.lower() for mn in _MONTH_NAMES
                    ) and str(year) in url
                    if has_in_url:
                        return True
    return False


def _extract_pub_date_from_page(url: str) -> str | None:
    """Fetch a page and extract the real publication date from meta tags.
    Looks for og:article:published_time, datePublished, etc."""
    if not url or "google.com/search" in url:
        return None
    try:
        resp = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html",
            },
            timeout=10,
            allow_redirects=True,
        )
        if resp.status_code >= 400:
            return None
        html = resp.text[:20000]

        for pattern in [
            r'property="article:published_time"\s+content="([^"]+)"',
            r'property="og:article:published_time"\s+content="([^"]+)"',
            r'content="([^"]+)"\s+property="article:published_time"',
            r'name="publish[_-]?date"\s+content="([^"]+)"',
            r'name="date"\s+content="([^"]+)"',
            r'name="DC\.date"\s+content="([^"]+)"',
            r'"datePublished"\s*:\s*"([^"]+)"',
            r'"publishedDate"\s*:\s*"([^"]+)"',
            r'"date_published"\s*:\s*"([^"]+)"',
            r'itemprop="datePublished"\s+content="([^"]+)"',
            r'content="([^"]+)"\s+itemprop="datePublished"',
            r'"dateCreated"\s*:\s*"([^"]+)"',
            r'data-publishdate="([^"]+)"',
            r'name="pubdate"\s+content="([^"]+)"',
        ]:
            m = re.search(pattern, html)
            if m:
                raw = m.group(1)
                try:
                    dt = date_parser.parse(raw)
                    return dt.strftime("%Y-%m-%d")
                except (ValueError, TypeError):
                    continue

        # Try URL of final destination (after redirects)
        final_url = resp.url
        url_date = _extract_date_from_url(final_url)
        if url_date:
            return url_date

    except Exception as e:
        logger.debug(f"Failed to extract date from {url[:60]}: {e}")
    return None


def _is_aggregator_source(source: str) -> bool:
    """Check if a source is a known content aggregator."""
    src_lower = source.lower()
    return any(agg.lower() in src_lower for agg in AGGREGATOR_SOURCES)


_URL_CHECK_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def _validate_url(url: str) -> bool:
    """Quick check that a URL is reachable (not 404 or DNS failure).
    Returns True if OK or uncertain (403/timeout = anti-bot, counts as OK).
    Returns False only for hard failures: 404, 410, DNS resolution errors."""
    if not url:
        return False
    try:
        resp = requests.head(
            url, headers=_URL_CHECK_HEADERS, timeout=8, allow_redirects=True,
        )
        if resp.status_code == 405:
            resp = requests.get(
                url, headers=_URL_CHECK_HEADERS, timeout=8,
                allow_redirects=True, stream=True,
            )
            resp.close()
        if resp.status_code in (404, 410, 500, 502, 503):
            logger.info(f"URL check failed [{resp.status_code}]: {url[:80]}")
            return False
        return True
    except requests.exceptions.ConnectionError:
        logger.info(f"URL check DNS fail: {url[:80]}")
        return False
    except requests.exceptions.Timeout:
        return True
    except Exception:
        return True


def _url_with_fallback(url: str, title: str, source: str) -> str | None:
    """Return the URL if valid, otherwise None (skip this item)."""
    if _validate_url(url):
        return url
    logger.info(f"URL unreachable, skipping: {title[:50]}")
    return None


class NewsItem:
    """Represents a single news article."""

    def __init__(
        self,
        title: str,
        url: str,
        summary: str,
        source: str,
        published: Optional[str] = None,
        sections: Optional[list] = None,
        summary_zh: str = "",
        is_major: bool = False,
    ):
        self.title = title
        self.url = url
        self.summary = summary
        self.source = source
        self.published = published
        self.sections = sections or []
        self.summary_zh = summary_zh
        self.is_major = is_major

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "summary": self.summary,
            "source": self.source,
            "published": self.published,
            "sections": self.sections,
            "summary_zh": self.summary_zh,
            "is_major": self.is_major,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


def fetch_rss_feeds(max_age_days: int = 14) -> list[NewsItem]:
    """Fetch news from configured RSS feeds."""
    items = []
    cutoff = datetime.now() - timedelta(days=max_age_days)

    for feed_config in RSS_FEEDS:
        try:
            logger.info(f"Fetching RSS: {feed_config['name']}...")
            feed = feedparser.parse(feed_config["url"])

            for entry in feed.entries[:20]:
                pub_date = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])

                if not pub_date or pub_date.year < 2026:
                    continue
                if pub_date < cutoff:
                    continue

                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                summary = entry.get("summary", entry.get("description", "")).strip()
                # Remove HTML tags from summary
                if "<" in summary:
                    from bs4 import BeautifulSoup

                    summary = BeautifulSoup(summary, "html.parser").get_text()
                summary = summary[:500]

                if not _is_relevant(title, summary, source=feed_config["name"]):
                    continue

                if _is_old_event_article(title, link):
                    logger.info(f"Skip old event article: {title[:50]}")
                    continue

                actual_link = _resolve_google_news_url(link)
                url_date = _extract_date_from_url(actual_link)
                pub_str = pub_date.strftime("%Y-%m-%d") if pub_date else None
                if url_date:
                    url_year = int(url_date[:4])
                    if url_year < 2026:
                        logger.info(f"Skip old article (url_date={url_date}): {title[:50]}")
                        continue
                    if url_date != pub_str:
                        pub_str = url_date

                # Always verify date from page meta tags
                real_date = _extract_pub_date_from_page(actual_link or link)
                if real_date:
                    real_year = int(real_date[:4])
                    if real_year < 2026:
                        logger.info(
                            f"Skip old article (real_date={real_date}): "
                            f"{title[:50]}"
                        )
                        continue
                    if real_date != pub_str:
                        logger.info(
                            f"Date corrected: {pub_str} -> {real_date}: "
                            f"{title[:50]}"
                        )
                        pub_str = real_date

                if _url_date_conflicts(actual_link, pub_str):
                    continue

                final_url = actual_link if actual_link != link else link
                final_url = _url_with_fallback(final_url, title, feed_config["name"])
                if not final_url:
                    continue

                item = NewsItem(
                    title=title,
                    url=final_url,
                    summary=summary,
                    source=feed_config["name"],
                    published=pub_str,
                )
                items.append(item)

        except Exception as e:
            logger.warning(f"Failed to fetch RSS from {feed_config['name']}: {e}")

    logger.info(f"RSS: fetched {len(items)} relevant articles")
    return items


def search_web(queries: Optional[list] = None) -> list[NewsItem]:
    """
    Search for news using SerpAPI (Google Search API).
    Falls back to Google News RSS if no API key configured.
    """
    queries = queries or SEARCH_QUERIES
    items = []

    if SERPAPI_KEY:
        items = _search_serpapi(queries)
    else:
        items = _search_google_news_rss(queries)

    logger.info(f"Web search: fetched {len(items)} relevant articles")
    return items


def _search_serpapi(queries: list) -> list[NewsItem]:
    """Use SerpAPI for Google search results."""
    items = []
    seen_urls = set()

    for query in queries:
        try:
            resp = requests.get(
                "https://serpapi.com/search",
                params={
                    "q": query,
                    "api_key": SERPAPI_KEY,
                    "engine": "google_news",
                    "gl": "id",
                    "hl": "en",
                },
                timeout=15,
            )
            data = resp.json()

            for result in data.get("news_results", [])[:5]:
                url = result.get("link", "")
                if url in seen_urls:
                    continue
                seen_urls.add(url)

                if "date" not in result:
                    continue
                try:
                    parsed_date = date_parser.parse(result["date"])
                except (ValueError, TypeError):
                    continue
                if parsed_date.year < 2026:
                    continue
                pub_date = parsed_date.strftime("%Y-%m-%d")

                title_text = result.get("title", "")
                snippet = result.get("snippet", "")
                src_name = result.get("source", {}).get("name", "Web")
                if not _is_relevant(title_text, snippet, source=src_name):
                    continue
                if _url_date_conflicts(url, pub_date):
                    continue
                item = NewsItem(
                    title=title_text,
                    url=url,
                    summary=snippet,
                    source=result.get("source", {}).get("name", "Web"),
                    published=pub_date,
                )
                items.append(item)

            time.sleep(1)

        except Exception as e:
            logger.warning(f"SerpAPI search failed for '{query}': {e}")

    return items


def _search_google_news_rss(queries: list) -> list[NewsItem]:
    """Fallback: use Google News RSS (free, no API key needed).
    Searches in both English and Indonesian to maximize coverage."""
    items = []
    seen_urls = set()

    for query in queries:
        # Detect if query is already Indonesian (contains common ID words)
        id_markers = ["berita", "terbaru", "pinjol", "pinjaman", "dompet", "cicilan",
                       "pembayaran", "fintek", "terdaftar", "kebijakan", "sanksi"]
        is_indonesian = any(m in query.lower() for m in id_markers)
        if is_indonesian:
            lang_configs = [("id", "id", "ID:id")]
        else:
            lang_configs = [("en", "ID", "ID:en")]

        for hl, gl, ceid in lang_configs:
            try:
                from urllib.parse import quote
                suffix = "" if is_indonesian else " Indonesia"
                encoded_query = quote(query + suffix)
                rss_url = (
                    f"https://news.google.com/rss/search?q={encoded_query}&hl={hl}&gl={gl}&ceid={ceid}"
                )
                feed = feedparser.parse(rss_url)

                for entry in feed.entries[:10]:
                    gn_url = entry.get("link", "")
                    if gn_url in seen_urls:
                        continue
                    seen_urls.add(gn_url)

                    if not (
                        hasattr(entry, "published_parsed") and entry.published_parsed
                    ):
                        continue
                    dt_pub = datetime(*entry.published_parsed[:6])
                    if dt_pub.year < 2026:
                        continue
                    pub_date = dt_pub.strftime("%Y-%m-%d")

                    actual_url = _resolve_google_news_url(gn_url)
                    url_date = _extract_date_from_url(actual_url)
                    if url_date and url_date != pub_date:
                        url_year = int(url_date[:4])
                        if url_year < 2026:
                            logger.info(f"Skip old article (url_date={url_date}): {entry.get('title','')[:50]}")
                            continue
                        pub_date = url_date

                    raw_summary = entry.get("summary", "").strip()
                    if "<" in raw_summary:
                        from bs4 import BeautifulSoup
                        raw_summary = BeautifulSoup(raw_summary, "html.parser").get_text()
                    raw_summary = raw_summary[:500]

                    title_text = entry.get("title", "").strip()
                    gn_source = entry.get("source", {}).get("title", "Google News")
                    if not _is_relevant(title_text, raw_summary, source=gn_source):
                        continue

                    if _is_old_event_article(title_text, actual_url or gn_url):
                        logger.info(f"Skip old event article: {title_text[:50]}")
                        continue

                    # Always verify date from page meta tags
                    real_date = _extract_pub_date_from_page(actual_url or gn_url)
                    if real_date:
                        real_year = int(real_date[:4])
                        if real_year < 2026:
                            logger.info(
                                f"Skip old article (real={real_date}): "
                                f"{title_text[:50]}"
                            )
                            continue
                        if real_date != pub_date:
                            pub_date = real_date

                    if _url_date_conflicts(actual_url, pub_date):
                        continue
                    final_url = actual_url if actual_url != gn_url else gn_url
                    final_url = _url_with_fallback(final_url, title_text, gn_source)
                    if not final_url:
                        continue

                    item = NewsItem(
                        title=title_text,
                        url=final_url,
                        summary=raw_summary,
                        source=gn_source,
                        published=pub_date,
                    )
                    items.append(item)

                time.sleep(0.5)

            except Exception as e:
                logger.warning(f"Google News RSS search failed for '{query}': {e}")

    return items


def _is_relevant(title: str, summary: str, source: str = "") -> bool:
    """Check if article is relevant to Indonesia fintech.
    Requires at least 1 keyword match, no cross-country exclusions,
    and for regional sources, must also mention Indonesia specifically."""
    text = (title + " " + summary).lower()
    for ex in EXCLUDE_KEYWORDS:
        if ex.lower() in text:
            return False
    from config import WORD_BOUNDARY_KEYWORDS
    has_fintech_kw = False
    for kw in GLOBAL_KEYWORDS:
        kw_lower = kw.lower()
        if kw in WORD_BOUNDARY_KEYWORDS:
            if re.search(r'\b' + re.escape(kw_lower) + r'\b', text):
                has_fintech_kw = True
                break
        elif kw_lower in text:
            has_fintech_kw = True
            break
    if not has_fintech_kw:
        return False
    if _is_regional_source(source):
        has_geo = any(geo.lower() in text for geo in INDONESIA_GEO_KEYWORDS)
        if not has_geo:
            has_geo = any(
                re.search(r'\b' + re.escape(wb.lower()) + r'\b', text)
                for wb in INDONESIA_GEO_WORD_BOUNDARY
            )
        if not has_geo:
            return False
    return True


def _is_regional_source(source: str) -> bool:
    """Check if the source is a regional (non-Indonesia-specific) outlet."""
    src_lower = source.lower()
    return any(rs.lower() in src_lower for rs in REGIONAL_SOURCES)


def load_existing_news() -> list[dict]:
    """Load previously saved news from JSON file."""
    news_file = DATA_DIR / "news.json"
    if news_file.exists():
        with open(news_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_news(items: list[dict]):
    """Save news items to JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    news_file = DATA_DIR / "news.json"
    with open(news_file, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved {len(items)} news items to {news_file}")


def deduplicate(new_items: list[NewsItem], existing: list[dict]) -> list[NewsItem]:
    """Remove duplicates based on URL."""
    existing_urls = {item["url"] for item in existing}
    return [item for item in new_items if item.url not in existing_urls]
