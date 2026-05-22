"""
WeChat Work (企业微信) webhook notification for Indonesia daily news.

Format:
  Part 1 — 昨日动态：200-300字通顺中文段落
  Part 2 — 明细：每条含完整中文标题 + 完整摘要 + 原文链接
  Footer — 查看完整日报链接
Priority: Akulaku集团 > 监管(fintech相关) > 同行品牌 > 其他
监管仅含BNPL/现金贷/电子钱包/数字银行/同行相关，保险/证券归入其他。
推送总量上限 8 条。
"""
import json
import re
import logging
from pathlib import Path

import requests

from config import INSURANCE_SECURITIES_KEYWORDS, MACRO_EXCLUDE_KEYWORDS

logger = logging.getLogger(__name__)

MIN_PUSH_ITEMS = 3
MAX_PUSH_ITEMS = 8
MAX_REGULATION_IN_PUSH = 2

WECHAT_WEBHOOK_URL = (
    "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"
    "?key=3c6acacb-4017-4fc1-82b4-122387ef0f85"
)

WEBSITE_URL = "https://yingxiang-1025.github.io/indonesia-fintech-daily/"

SECTION_META = {
    "akulaku":        {"priority": 0, "label": "🔥 Akulaku集团", "emoji": "🔥", "show_all": True},
    "regulation":     {"priority": 1, "label": "监管动态",       "emoji": "📋", "show_all": True},
    "bnpl":           {"priority": 2, "label": "BNPL同行",       "emoji": "🛒", "show_all": True},
    "e_wallet":       {"priority": 3, "label": "电子钱包",       "emoji": "📲", "show_all": True},
    "cash_loan":      {"priority": 4, "label": "现金贷",         "emoji": "💵", "show_all": True},
    "digital_lending":{"priority": 5, "label": "数字信贷",       "emoji": "💰", "show_all": False},
    "p2p_lending":    {"priority": 6, "label": "P2P借贷",        "emoji": "🤝", "show_all": False},
    "credit_card":    {"priority": 7, "label": "信用卡",         "emoji": "💳", "show_all": False},
    "digital_bank":   {"priority": 8, "label": "数字银行",       "emoji": "📱", "show_all": False},
}

_DEFAULT_META = {"priority": 99, "label": "金融科技", "emoji": "📊", "show_all": False}

CONNECTORS = {
    "akulaku": "Akulaku集团方面，",
    "regulation": "监管层面，",
    "bnpl": "BNPL/同行竞品方面，",
    "e_wallet": "电子钱包领域，",
    "cash_loan": "现金贷方面，",
    "digital_lending": "数字信贷方面，",
    "p2p_lending": "P2P借贷方面，",
    "credit_card": "信用卡领域，",
    "digital_bank": "数字银行领域，",
}

_INNER_CONNECTORS = ["同时，", "此外，", "另外，", "值得关注的是，"]


# ─── Text Utils ──────────────────────────────────────────

def _clean(text: str) -> str:
    if not text:
        return ""
    out = text.replace("\n", " ").strip()
    if "<" in out:
        from bs4 import BeautifulSoup
        out = BeautifulSoup(out, "html.parser").get_text()
    return out


def _strip_trailing(text: str) -> str:
    """Strip trailing source names, dangling separators, and URLs."""
    for sep in [" - ", " — ", " | ", " · "]:
        pos = text.rfind(sep)
        if pos > len(text) // 3:
            text = text[:pos].strip()
    text = re.sub(r"\s+[A-Z][A-Za-z]{2,}(?:\s+[A-Z][A-Za-z]+)*\s*$", "", text)
    text = re.sub(r"\s*https?://\S+$", "", text)
    return text.strip()


def _sentence_cut(text: str, max_len: int) -> str:
    """Cut text at the last complete sentence boundary within max_len.
    Only cuts at full-stop (。) or semicolon (；) to avoid half-clauses.
    Strips trailing punctuation to prevent double-periods when joined."""
    text = text.rstrip("。；，、 ")
    if len(text) <= max_len:
        return text
    window = text[:max_len]
    for punc in ["。", "；"]:
        pos = window.rfind(punc)
        if pos > max_len * 0.35:
            return window[:pos].rstrip("。；，、 ")
    return window.rstrip("。；，、 ")


def _get_summary(item: dict) -> str:
    raw = _clean(item.get("summary_zh") or item.get("summary", ""))
    return _strip_trailing(raw)


def _title_text(item: dict) -> str:
    raw = item.get("title_zh") or item.get("title", "")
    body = raw.split("】")[-1].strip() if "】" in raw else raw
    return _strip_trailing(body)


# ─── Grouping ────────────────────────────────────────────

def _is_non_fintech_regulation(item: dict) -> bool:
    """Check if a regulation item is NOT about fintech (insurance/securities/macro).
    These get demoted to 'other' in push priority."""
    sections = item.get("sections", [])
    if "regulation" not in sections:
        return False
    fintech_sections = {
        "bnpl", "cash_loan", "e_wallet", "digital_bank",
        "digital_lending", "p2p_lending", "akulaku",
    }
    if fintech_sections & set(sections):
        return False
    text = (
        (item.get("title") or "") + " " +
        (item.get("title_zh") or "") + " " +
        (item.get("summary") or "") + " " +
        (item.get("summary_zh") or "")
    ).lower()
    if any(kw.lower() in text for kw in INSURANCE_SECURITIES_KEYWORDS):
        return True
    if any(kw.lower() in text for kw in MACRO_EXCLUDE_KEYWORDS):
        return True
    return False


def _best_section(item: dict) -> str:
    """Determine the best section for push grouping.
    Non-fintech regulation is demoted to 'other'."""
    sections = item.get("sections", [])
    if not sections:
        return "other"
    if _is_non_fintech_regulation(item):
        remaining = [s for s in sections if s != "regulation"]
        if not remaining:
            return "other"
        return min(remaining, key=lambda s: SECTION_META.get(s, _DEFAULT_META)["priority"])
    return min(sections, key=lambda s: SECTION_META.get(s, _DEFAULT_META)["priority"])


def _meta(section: str) -> dict:
    return SECTION_META.get(section, _DEFAULT_META)


def _group_by_section(items: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for item in items:
        sec = _best_section(item)
        groups.setdefault(sec, []).append(item)
    return dict(
        sorted(groups.items(), key=lambda kv: _meta(kv[0])["priority"])
    )


# ─── Part 1: 昨日动态 ────────────────────────────────────

def _build_digest(groups: dict[str, list[dict]], total: int) -> str:
    """Build 200-300 char fluent Chinese paragraph with complete sentences only.

    When item count is small, uses ALL items for a richer summary.
    """
    all_sentences = []
    items_per_section = max(2, 6 // max(len(groups), 1))

    for sec, items in groups.items():
        prefix = CONNECTORS.get(sec, "此外，")
        for idx, item in enumerate(items[:items_per_section]):
            summary = _get_summary(item)
            title = _title_text(item)
            text = summary if len(summary) > 15 else title
            text = _sentence_cut(text, 90)

            if idx == 0:
                all_sentences.append(f"{prefix}{text}")
            else:
                conn = _INNER_CONNECTORS[min(idx - 1, len(_INNER_CONNECTORS) - 1)]
                all_sentences.append(f"{conn}{text}")

            current = "。".join(all_sentences) + "。"
            if len(current) >= 280:
                break
        if len("。".join(all_sentences) + "。") >= 280:
            break

    digest = "。".join(all_sentences)
    if not digest.endswith("。"):
        digest += "。"
    return digest


# ─── Part 2: 明细 ────────────────────────────────────────

def _build_details(groups: dict[str, list[dict]], digest: str = "") -> list[str]:
    """Build detail lines. Skip summary if already in digest."""
    lines = []
    item_no = 0
    for sec, items in groups.items():
        meta = _meta(sec)
        lines.append(f"{meta['emoji']} **{meta['label']}**（{len(items)}条）")
        cap = len(items) if meta.get("show_all") else 3
        for item in items[:cap]:
            item_no += 1
            title = _title_text(item)
            url = item.get("url", "")
            major_tag = "🔴" if item.get("is_major") else ""
            summary = _get_summary(item)
            summary = _sentence_cut(summary, 120)

            display_title = f"{major_tag}{title}" if major_tag else title
            lines.append(f"{item_no}. **{display_title}**")
            if summary and summary[:20] not in digest:
                lines.append(f"> {summary}")
            if url:
                lines.append(f"[查看原文]({url})")
        if len(items) > cap:
            lines.append(f"...另有{len(items) - cap}条")
        lines.append("")
    return lines


# ─── Assemble ────────────────────────────────────────────

def build_message(new_items: list[dict], today_str: str) -> str | None:
    if not new_items:
        return None

    groups = _group_by_section(new_items)
    total = len(new_items)
    major_count = sum(1 for n in new_items if n.get("is_major"))
    digest = _build_digest(groups, total)

    lines = [
        f"📰 **印尼金融科技日报 | {today_str}**",
        f"新增<font color=\"info\">{total}</font>条资讯",
    ]
    if major_count:
        lines[-1] += f"　其中<font color=\"warning\">{major_count}条重大</font>"
    lines.append("")

    lines.append("**📋 昨日动态**")
    lines.append(f"> {digest}")
    lines.append("")

    lines.append("**📝 明细**")
    lines.extend(_build_details(groups, digest))

    lines.append(f"[🌐 查看完整日报]({WEBSITE_URL})")

    return "\n".join(lines)


_PUSH_HISTORY_FILE = Path(__file__).parent / "data" / "pushed_history.json"


def _load_push_history() -> dict:
    if _PUSH_HISTORY_FILE.exists():
        try:
            with open(_PUSH_HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_push_history(history: dict):
    _PUSH_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(_PUSH_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def _filter_unpushed(items: list[dict]) -> list[dict]:
    """Filter out items that have already been pushed."""
    history = _load_push_history()
    unpushed = []
    for item in items:
        url = item.get("url", "")
        title = item.get("title", "")
        key = url or title
        if key and key not in history:
            unpushed.append(item)
    skipped = len(items) - len(unpushed)
    if skipped:
        logger.info(f"Push dedup: {skipped} items already pushed, {len(unpushed)} new")
    return unpushed


def _record_pushed(items: list[dict], push_date: str):
    """Record pushed items in history."""
    history = _load_push_history()
    for item in items:
        url = item.get("url", "")
        title = item.get("title", "")
        key = url or title
        if key:
            history[key] = push_date
    # Keep history manageable: only last 90 days (approx 500 items)
    if len(history) > 500:
        sorted_items = sorted(history.items(), key=lambda x: x[1], reverse=True)
        history = dict(sorted_items[:500])
    _save_push_history(history)


def send_wechat_notification(new_items: list[dict], today_str: str) -> bool:
    # Filter out already-pushed items
    unpushed = _filter_unpushed(new_items) if new_items else []

    if not unpushed:
        message = (
            f"📰 **印尼金融科技日报 | {today_str}**\n\n"
            f"昨日无新增资讯更新。\n\n"
            f"[🌐 查看完整日报]({WEBSITE_URL})"
        )
        logger.info("No unpushed yesterday news — sending 'no update' notification.")
    else:
        items = sorted(unpushed, key=lambda n: _meta(_best_section(n))["priority"])
        # Cap regulation items at MAX_REGULATION_IN_PUSH
        reg_count = 0
        capped_items = []
        for item in items:
            if _best_section(item) == "regulation":
                reg_count += 1
                if reg_count > MAX_REGULATION_IN_PUSH:
                    continue
            capped_items.append(item)
        if reg_count > MAX_REGULATION_IN_PUSH:
            logger.info(f"Regulation cap: {reg_count} -> {MAX_REGULATION_IN_PUSH}")
        items = capped_items

        if len(items) > MAX_PUSH_ITEMS:
            logger.info(f"Push cap: trimming {len(items)} items to {MAX_PUSH_ITEMS}")
            items = items[:MAX_PUSH_ITEMS]
        if len(items) < MIN_PUSH_ITEMS:
            logger.info(f"Only {len(items)} items, below minimum {MIN_PUSH_ITEMS}")
        message = build_message(items, today_str)
        if not message:
            return False

        while len(message.encode("utf-8")) > 3800 and len(items) > MIN_PUSH_ITEMS:
            items = items[:-1]
            message = build_message(items, today_str)
        logger.info(f"Message length: {len(message)} chars, {len(message.encode('utf-8'))} bytes, items: {len(items)}")

    payload = {"msgtype": "markdown", "markdown": {"content": message}}

    try:
        resp = requests.post(WECHAT_WEBHOOK_URL, json=payload, timeout=10)
        result = resp.json()
        if result.get("errcode") == 0:
            if unpushed:
                _record_pushed(unpushed, today_str)
            logger.info(f"WeChat push OK: {len(unpushed)} items sent")
            return True
        logger.warning(f"WeChat webhook error: {result.get('errmsg', '?')}")
        return False
    except Exception as e:
        logger.error(f"WeChat push failed: {e}")
        return False
