"""Evidence-first, low-cost headline discovery for TRADE90.

GDELT indexes publisher links; it does not independently verify an event. This
module NEVER infers a market move, a quote, or a buy/sell recommendation from a
headline. Source timestamps are FIRST-SEEN metadata, not occurrence times.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json
import re

from django.core.cache import cache

GDELT_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
CACHE_KEY = "trade90:macro_evidence:v1"
CACHE_SECONDS = 600
MAX_AGE_HOURS = 48
MAX_UPSTREAM_BYTES = 200_000
ALLOWED_HOSTS = (
    "reuters.com", "apnews.com", "bbc.com", "ft.com", "bloomberg.com",
    "wsj.com", "theguardian.com", "cnbc.com", "aljazeera.com",
    "spglobal.com", "marketwatch.com", "dw.com", "france24.com",
)
TRACKS = [
    {
        "id": "gulf_supply", "title": "Gulf, Saudi Arabia & energy supply",
        "query": '(Houthis OR Houthi OR "Saudi Arabia" OR Hormuz) (Aramco OR oil OR missile OR shipping)',
        "instruments": ["XAU/USD", "EUR/USD", "USD/JPY", "USD/CAD", "BTC/USD"],
        "mechanisms": [
            "Shipping or production risks can change energy supply expectations.",
            "Higher energy prices can affect inflation and central-bank expectations.",
            "Gold can respond in opposite directions to safe-haven demand versus real yields and the U.S. dollar.",
        ],
    },
    {
        "id": "iran_us", "title": "Iran–U.S. developments",
        "query": '(Iran OR Iranian) ("United States" OR US OR America) (sanctions OR attack OR negotiations OR oil OR Hormuz)',
        "instruments": ["XAU/USD", "EUR/USD", "USD/JPY", "BTC/USD"],
        "mechanisms": [
            "Diplomatic or military developments can change perceived risk and energy supply exposure.",
            "USD, U.S. yields, crude oil and gold should be checked together before attributing a move.",
        ],
    },
    {
        "id": "us_inflation", "title": "U.S. inflation, Treasury yields & Fed",
        "query": '("CPI" OR "US inflation" OR "Federal Reserve") (dollar OR yields OR interest OR rates)',
        "instruments": ["XAU/USD", "EUR/USD", "USD/JPY", "GBP/USD", "BTC/USD"],
        "mechanisms": [
            "Compare official inflation data against the pre-release consensus, not just its previous reading.",
            "Check U.S. 2-year/10-year Treasury yields and the dollar around the release timestamp.",
            "A dollar/yield reaction is not proof that a particular asset followed for the same reason.",
        ],
    },
]

class NewsDiscoveryError(Exception):
    pass


def _host(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username:
            return None
        host = parsed.hostname.lower()
        if any(host == x or host.endswith("." + x) for x in ALLOWED_HOSTS):
            return host
    except (TypeError, ValueError):
        pass
    return None


def _timestamp(value):
    if not isinstance(value, str):
        return None
    for fmt in ("%Y%m%dT%H%M%SZ", "%Y%m%d%H%M%S"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def extract_articles(payload, *, now=None):
    now = now or datetime.now(timezone.utc)
    if not isinstance(payload, dict) or not isinstance(payload.get("articles"), list):
        raise NewsDiscoveryError("Unrecognized source discovery response")
    seen = set()
    results = []
    for row in payload["articles"]:
        if not isinstance(row, dict):
            continue
        url = row.get("url")
        host = _host(url)
        stamp = _timestamp(row.get("seendate"))
        headline = re.sub(r"\s+", " ", str(row.get("title") or "")).strip()
        if not host or not stamp or len(headline) < 18 or len(headline) > 400:
            continue
        age_hours = (now - stamp).total_seconds() / 3600
        if not -0.2 <= age_hours <= MAX_AGE_HOURS:
            continue
        key = re.sub(r"\W+", "", headline.lower())[:180]
        if key in seen:
            continue
        seen.add(key)
        results.append({
            "headline": headline[:220], "url": url,
            "publisher": host, "first_seen_at": stamp.isoformat(),
            "source_type": "third-party published report",
        })
    results.sort(key=lambda x: x["first_seen_at"], reverse=True)
    # Prefer broader independent coverage when possible, while including
    # a small number of per-outlet updates about the same ongoing topic.
    selected = []
    counts = {}
    for item in results:
        domain = item["publisher"]
        if counts.get(domain, 0) >= 2:
            continue
        selected.append(item)
        counts[domain] = counts.get(domain, 0) + 1
        if len(selected) == 7:
            break
    return selected


def _discover(track):
    args = urlencode({
        "query": track["query"], "mode": "artlist", "format": "json",
        "maxrecords": 45, "timespan": "48h",
    })
    request = Request(GDELT_URL + "?" + args, headers={
        "Accept": "application/json", "User-Agent": "TRADE90 research brief/1.0",
    })
    try:
        with urlopen(request, timeout=7) as response:
            if response.status != 200:
                raise NewsDiscoveryError("News index returned an upstream HTTP error")
            raw = response.read(MAX_UPSTREAM_BYTES + 1)
            if len(raw) > MAX_UPSTREAM_BYTES:
                raise NewsDiscoveryError("News index response too large")
        return json.loads(raw)
    except (HTTPError, URLError, OSError, ValueError) as exc:
        raise NewsDiscoveryError("News discovery is temporarily unavailable") from exc


def _one(track, now):
    try:
        source = _discover(track)
        reports = extract_articles(source, now=now)
        status = "reports_found" if reports else "no_reliable_reports"
    except NewsDiscoveryError:
        reports, status = [], "source_unavailable"
    publishers = sorted({x["publisher"] for x in reports})
    return {
        "id": track["id"], "title": track["title"],
        "status": status,
        "instruments": track["instruments"],
        "reports": reports, "publisher_count": len(publishers),
        "market_reaction": {
            "status": "not_measured",
            "detail": "No licensed, timestamp-aligned event-price series is connected. News volume is not price movement.",
        },
        "mechanisms_to_investigate": track["mechanisms"],
        "evidence_note": (
            "Links show recent reports discovered in the news index. Reporting is not independent confirmation, "
            "and the first-seen timestamp may differ from the event time."
        ),
    }


def event_evidence(now=None):
    now = now or datetime.now(timezone.utc)
    cached = cache.get(CACHE_KEY)
    if cached is not None:
        return cached
    with ThreadPoolExecutor(max_workers=3) as pool:
        tracks = list(pool.map(lambda x: _one(x, now), TRACKS))
    result = {
        "status": "ok" if any(t["status"] == "reports_found" for t in tracks) else "limited",
        "checked_at": now.isoformat(),
        "news_index": "GDELT Project DOC 2.0",
        "method": "Headline/link discovery from selected publishers, not automated fact verification.",
        "event_time_precision": "first_seen_at is a news-index observation, not an event or market price timestamp",
        "market_reaction_policy": "No causal claims or numerical event reactions without licensed event-aligned candles.",
        "topics": tracks,
    }
    cache.set(CACHE_KEY, result, timeout=CACHE_SECONDS)
    return result
