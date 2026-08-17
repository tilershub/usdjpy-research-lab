"""Official central-bank communications.

Bloomberg and Reuters do not license their wires on terms this product can meet,
and republishing their text without a licence is not an option, so the feed is
built from primary sources instead: the central banks that actually move rates,
publishing their own statements, decisions and speeches.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

FEEDS = (
    ("Federal Reserve", "USD", "https://www.federalreserve.gov/feeds/press_all.xml"),
    ("European Central Bank", "EUR", "https://www.ecb.europa.eu/rss/press.html"),
)

# Gold responds to the policy path rather than to any single currency, so
# every central bank release is relevant to it.
BROAD_MARKET_ASSETS = ("XAU", "BTC")


@dataclass(frozen=True)
class NewsStatus:
    provider: str
    fetched_at: datetime
    cadence: str
    message: str = ""


def _text(node, *names: str) -> str:
    for name in names:
        found = node.find(name)
        if found is not None and (found.text or "").strip():
            return found.text.strip()
    return ""


def _published(raw: str) -> datetime | None:
    if not raw:
        return None
    try:
        stamp = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        try:
            stamp = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return None
    if stamp is None:
        return None
    return stamp if stamp.tzinfo else stamp.replace(tzinfo=timezone.utc)


def parse_feed(payload: bytes, source: str, currency: str, limit: int = 8) -> list[dict]:
    root = ET.fromstring(payload)
    items = []
    for item in root.iter("item"):
        published = _published(_text(item, "pubDate", "{http://purl.org/dc/elements/1.1/}date"))
        title = _text(item, "title")
        if not title:
            continue
        items.append({
            "source": source,
            "currency": currency,
            "headline": title,
            "url": _text(item, "link"),
            "published_at": published.astimezone(timezone.utc).isoformat() if published else "",
        })
    items.sort(key=lambda entry: entry["published_at"], reverse=True)
    return items[:limit]


def fetch_news(timeout: int = 20, limit: int = 8) -> tuple[list[dict], NewsStatus]:
    now = datetime.now(timezone.utc)
    provider = "Central bank press releases (" + ", ".join(name for name, _, _ in FEEDS) + ")"
    cadence = "Continuous; official primary sources"
    entries, failures = [], []
    for source, currency, url in FEEDS:
        request = Request(url, headers={"User-Agent": "TRADE90-research/1.0"})
        try:
            with urlopen(request, timeout=timeout) as response:
                entries.extend(parse_feed(response.read(), source, currency, limit))
        except Exception as exc:
            failures.append(f"{source}: {exc}")
    entries.sort(key=lambda entry: entry["published_at"], reverse=True)
    if failures and not entries:
        return [], NewsStatus(provider, now, cadence, "News unavailable: " + "; ".join(failures))
    return entries, NewsStatus(provider, now, cadence, "; ".join(failures))


def news_for_pair(entries: list[dict], base: str, quote: str, limit: int = 4) -> list[dict]:
    """Headlines whose issuing central bank sets policy for one leg of the pair."""
    relevant = BROAD_MARKET_ASSETS if base in BROAD_MARKET_ASSETS else (base, quote)
    if base in BROAD_MARKET_ASSETS:
        matched = list(entries)
    else:
        matched = [entry for entry in entries if entry["currency"] in relevant]
    return matched[:limit]
