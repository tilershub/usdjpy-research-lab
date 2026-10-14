"""Indicative, timestamp-validated public market quotes.

Quotes are NOT trade-executable prices, a unified consolidated feed, or inputs
to the slower research model. Expose no quote as current without source time.
Review provider commercial display/redistribution terms before relying on
these public endpoints in a monetized service.
"""
import json
from datetime import datetime, timezone
from math import isfinite
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.core.cache import cache

SWISSQUOTE_SYMBOLS = frozenset({
    "XAU/USD", "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF",
    "USD/CAD", "AUD/USD", "NZD/USD",
})
ALL_SYMBOLS = SWISSQUOTE_SYMBOLS | {"BTC/USD"}
CACHE_SECONDS = 20
MAX_QUOTE_AGE_SECONDS = 300
USER_AGENT = "TRADE90-Research/1.0 (indicative research quotes; no order execution)"


class QuoteUnavailable(Exception):
    pass


def _number(value):
    if isinstance(value, bool):
        raise QuoteUnavailable("Invalid quote value")
    try:
        num = float(value)
        if not isfinite(num) or num <= 0:
            raise ValueError()
        return num
    except (TypeError, ValueError, OverflowError) as exc:
        raise QuoteUnavailable("Invalid quote value") from exc


def _get_json(url):
    req = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=5) as response:
            if response.status != 200:
                raise QuoteUnavailable("Upstream provider did not return success")
            payload = response.read(180_001)
            if len(payload) > 180_000:
                raise QuoteUnavailable("Upstream payload too large")
        return json.loads(payload)
    except (OSError, ValueError, URLError, HTTPError) as exc:
        raise QuoteUnavailable("Upstream quote temporarily unavailable") from exc


def _swissquote(symbol):
    response = _get_json(
        "https://forex-data-feed.swissquote.com/public-quotes/"
        "bboquotes/instrument/" + symbol
    )
    if not isinstance(response, list):
        raise QuoteUnavailable("Provider returned invalid quote data")
    for line in response:
        if not isinstance(line, dict):
            continue
        ts = line.get("ts")
        try:
            stamp = datetime.fromtimestamp(float(ts) / 1000, tz=timezone.utc)
        except (ValueError, TypeError, OSError, OverflowError):
            continue
        for profile in line.get("spreadProfilePrices") or []:
            if not isinstance(profile, dict):
                continue
            try:
                bid = _number(profile.get("bid"))
                ask = _number(profile.get("ask"))
            except QuoteUnavailable:
                continue
            if ask < bid or (ask - bid) / bid > 0.05:
                continue
            return {"bid": bid, "ask": ask, "observed_at": stamp,
                    "provider": "Swissquote public indicative BBO",
                    "venue": str((line.get("topo") or {}).get("platform") or "Dealer"),
                    "basis": "Dealer spot/CFD quote; broker prices may differ"}
    raise QuoteUnavailable("No valid timestamped dealer quotes received")


def _coinbase():
    response = _get_json("https://api.exchange.coinbase.com/products/BTC-USD/ticker")
    if not isinstance(response, dict):
        raise QuoteUnavailable("Provider returned invalid quote data")
    observed = response.get("time")
    if not isinstance(observed, str):
        raise QuoteUnavailable("Provider omitted trade timestamp")
    try:
        stamp = datetime.fromisoformat(observed.replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            raise ValueError()
        stamp = stamp.astimezone(timezone.utc)
    except (ValueError, OverflowError) as exc:
        raise QuoteUnavailable("Invalid provider timestamp") from exc
    bid, ask = _number(response.get("bid")), _number(response.get("ask"))
    if ask < bid or (ask - bid) / bid > 0.05:
        raise QuoteUnavailable("Invalid provider bid/ask")
    return {"bid": bid, "ask": ask, "observed_at": stamp,
            "provider": "Coinbase Exchange",
            "venue": "BTC-USD spot order book",
            "basis": "BTC-USD exchange spot; other exchanges differ"}


def _unavailable(symbol, message):
    return {"symbol": symbol, "status": "unavailable",
            "message": message, "bid": None, "ask": None,
            "mid": None, "observed_at": None}


def fetch_quote(symbol, now=None):
    if symbol not in ALL_SYMBOLS:
        return _unavailable(symbol, "Unsupported instrument")
    now = now or datetime.now(timezone.utc)
    try:
        raw = _coinbase() if symbol == "BTC/USD" else _swissquote(symbol)
    except QuoteUnavailable:
        return _unavailable(symbol, "Provider quote or timestamp unavailable")
    age = (now - raw["observed_at"]).total_seconds()
    if age < -90:
        return _unavailable(symbol, "Provider timestamp is ahead of server clock")
    if age > MAX_QUOTE_AGE_SECONDS:
        return {
            "symbol": symbol, "status": "stale",
            "message": "Latest available quote is too old to display as current",
            "bid": None, "ask": None, "mid": None,
            "observed_at": raw["observed_at"].isoformat(),
            "provider": raw["provider"], "basis": raw["basis"],
            "age_seconds": round(age),
        }
    bid, ask = raw["bid"], raw["ask"]
    return {
        "symbol": symbol, "status": "current",
        "message": "Indicative, source-timestamped market quote; not executable",
        "bid": bid, "ask": ask, "mid": (bid + ask) / 2,
        "spread": ask - bid,
        "observed_at": raw["observed_at"].isoformat(),
        "age_seconds": round(max(0, age)),
        "provider": raw["provider"], "venue": raw["venue"], "basis": raw["basis"],
    }


def cached_quote(symbol):
    if symbol not in ALL_SYMBOLS:
        return _unavailable(symbol, "Unsupported instrument")
    cache_key = "trade90-quote-v1:" + symbol.replace("/", "")
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    result = fetch_quote(symbol)
    cache.set(cache_key, result, CACHE_SECONDS)
    return result
