"""License-gated, timestamp-aware intraday OHLC research (never trade signals).

The Twelve Data adapter is inactive without both a server-side key and explicit
approval for PUBLIC commercial display/derived-data publication. In particular,
an individual plan is not sufficient for TRADE90's public visitors.
"""
import json
import os
from datetime import datetime, timedelta, timezone
from math import isfinite
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from django.conf import settings
from django.core.cache import cache


SYMBOLS = frozenset({
    "XAU/USD", "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF",
    "USD/CAD", "AUD/USD", "NZD/USD", "BTC/USD",
})
INTERVALS = {"15min": 15, "1h": 60}
MIN_CANDLES = 55
MAX_AGE_MULTIPLIER = 3
CACHE_SECONDS = 600
ERROR_CACHE_SECONDS = 75


class IntradayProviderError(Exception):
    pass


def _finite_price(raw):
    if isinstance(raw, bool):
        raise ValueError("Boolean is not a price")
    number = float(raw)
    if not isfinite(number) or number <= 0:
        raise ValueError("Price must be finite and positive")
    return number


def _open_timestamp(value):
    if not isinstance(value, str):
        raise ValueError("Candle has no timestamp")
    # Twelve Data datetime is the candle START, in UTC when timezone=UTC.
    dt = datetime.fromisoformat(value.replace(" ", "T").replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def clean_completed_candles(payload, symbol, interval, now=None):
    """Validate chronology, ignore unfinished candles and reject invalid OHLC."""
    if symbol not in SYMBOLS or interval not in INTERVALS:
        raise ValueError("Unsupported symbol or timeframe")
    now = now or datetime.now(timezone.utc)
    if not isinstance(payload, dict) or payload.get("status") == "error":
        raise IntradayProviderError("Provider did not return candle data")
    meta = payload.get("meta") or {}
    if str(meta.get("symbol", "")).upper() != symbol:
        raise IntradayProviderError("Source symbol does not match requested market")
    if meta.get("interval") != interval:
        raise IntradayProviderError("Source timeframe does not match requested interval")
    values = payload.get("values")
    if not isinstance(values, list) or len(values) > 5000:
        raise IntradayProviderError("Provider returned invalid candle series")
    span = timedelta(minutes=INTERVALS[interval])
    dedup = {}
    for raw in values:
        if not isinstance(raw, dict):
            continue
        try:
            opened = _open_timestamp(raw.get("datetime"))
            if opened + span > now:  # Do not calculate on a forming candle.
                continue
            op = _finite_price(raw.get("open"))
            hi = _finite_price(raw.get("high"))
            lo = _finite_price(raw.get("low"))
            cl = _finite_price(raw.get("close"))
            if lo > min(op, cl) or hi < max(op, cl) or hi < lo:
                continue
            dedup[opened] = {"open_at": opened, "open": op,
                             "high": hi, "low": lo, "close": cl}
        except (ValueError, TypeError, OverflowError):
            continue
    candles = [dedup[t] for t in sorted(dedup)]
    if len(candles) < MIN_CANDLES:
        raise IntradayProviderError("Insufficient complete, validated candles")
    return candles[-150:]


def _ema(values, period):
    if len(values) < period:
        raise IntradayProviderError("Insufficient data to calculate EMA")
    ema = sum(values[:period]) / period
    weight = 2 / (period + 1)
    for value in values[period:]:
        ema = weight * value + (1 - weight) * ema
    return ema


def _rsi14(closes):
    moves = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    period = 14
    gain = sum(max(0, m) for m in moves[:period]) / period
    loss = sum(max(0, -m) for m in moves[:period]) / period
    for move in moves[period:]:
        gain = (gain * (period - 1) + max(0, move)) / period
        loss = (loss * (period - 1) + max(0, -move)) / period
    if loss == 0:
        return 50.0 if gain == 0 else 100.0
    return 100 - (100 / (1 + gain / loss))


def _atr14(candles):
    trs = []
    prev_close = None
    for candle in candles:
        high, low = candle["high"], candle["low"]
        tr = high - low if prev_close is None else max(
            high - low, abs(high - prev_close), abs(low - prev_close))
        trs.append(tr)
        prev_close = candle["close"]
    atr = sum(trs[:14]) / 14
    for tr in trs[14:]:
        atr = (atr * 13 + tr) / 14
    return atr


def analyze_candles(candles, symbol, interval, *, now=None, provider="Twelve Data", basis="Provider OHLC"):
    """Use CLOSED candles, last-20 *prior* candles for breakout context."""
    if symbol not in SYMBOLS or interval not in INTERVALS:
        raise ValueError("Unsupported symbol or timeframe")
    if len(candles) < MIN_CANDLES:
        raise IntradayProviderError("Not enough completed candles")
    now = now or datetime.now(timezone.utc)
    closes = [c["close"] for c in candles]
    close = closes[-1]
    ema20, ema50 = _ema(closes, 20), _ema(closes, 50)
    rsi, atr = _rsi14(closes), _atr14(candles)
    high = max(c["high"] for c in candles[-21:-1])
    low = min(c["low"] for c in candles[-21:-1])
    if close > ema20 > ema50:
        structure = "Upward structure"
    elif close < ema20 < ema50:
        structure = "Downward structure"
    else:
        structure = "Mixed / transition"
    location = ("Above prior 20-candle high" if close > high else
                "Below prior 20-candle low" if close < low else "Inside prior 20-candle range")
    # Do not label a 16-bar delta "four hours": weekends and gaps are possible.
    change16 = (close / closes[-17] - 1) * 100
    observed = candles[-1]["open_at"] + timedelta(minutes=INTERVALS[interval])
    age_minutes = (now - observed).total_seconds() / 60
    is_current = -1 <= age_minutes <= INTERVALS[interval] * MAX_AGE_MULTIPLIER
    warnings = []
    if not is_current:
        warnings.append("Last completed candle is stale or has a future timestamp; not current intraday evidence.")
    if symbol == "XAU/USD":
        warnings.append("Provider gold candles are not your broker's CFD quotes; confirm instrument basis.")
    return {
        "status": "current" if is_current else "stale",
        "symbol": symbol, "interval": interval, "provider": provider,
        "price_basis": basis, "observed_at": observed.isoformat(),
        "age_minutes": round(age_minutes, 1),
        "last_completed_close": round(close, 6),
        "candle_count": len(candles),
        "structure": structure, "range_context": location,
        "ema20": round(ema20, 6), "ema50": round(ema50, 6),
        "rsi14": round(rsi, 2), "atr14": round(atr, 6),
        "prior20_high": round(high, 6), "prior20_low": round(low, 6),
        "change16_candles_pct": round(change16, 2),
        "warnings": warnings,
        "interpretation": (
            f"{interval} closing structure: {structure.lower()}; "
            f"last close is {location.lower()}. RSI(14) {rsi:.1f}; "
            "descriptive conditions, not a forecast or a trading signal."
        ),
    }


def provider_payload(symbol, interval, api_key):
    args = urlencode({
        "symbol": symbol, "interval": interval, "outputsize": 100,
        "timezone": "UTC", "order": "desc", "apikey": api_key,
    })
    endpoint = "https://api.twelvedata.com/time_series?" + args
    request = Request(endpoint, headers={"Accept": "application/json", "User-Agent": "TRADE90/1.0"})
    try:
        with urlopen(request, timeout=8) as response:
            if response.status != 200:
                raise IntradayProviderError("Provider HTTP error")
            chunk = response.read(260_001)
            if len(chunk) > 260_000:
                raise IntradayProviderError("Provider response exceeds safe size")
        return json.loads(chunk)
    except (HTTPError, URLError, OSError, ValueError) as exc:
        # Do not surface provider error messages that might contain API keys.
        raise IntradayProviderError("Could not retrieve intraday provider candles") from exc


def enabled():
    return (
        bool(getattr(settings, "TRADE90_INTRADAY_PUBLIC_LICENSED", False))
        and bool(os.environ.get("TWELVEDATA_API_KEY", "").strip())
    )


def get_intraday(symbol, interval):
    if symbol not in SYMBOLS or interval not in INTERVALS:
        return {"status": "invalid", "detail": "Unsupported instrument or timeframe"}
    if not enabled():
        return {
            "status": "not_configured",
            "detail": "Intraday analysis requires a licensed public-data agreement and a configured provider API key.",
        }
    cache_key = "trade90:intraday:v1:" + symbol.replace("/", "") + ":" + interval
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    lock_key = cache_key + ":lock"
    if not cache.add(lock_key, True, timeout=15):
        return {"status": "pending", "detail": "Research update already in progress; refresh shortly"}
    try:
        payload = provider_payload(symbol, interval, os.environ["TWELVEDATA_API_KEY"].strip())
        candles = clean_completed_candles(payload, symbol, interval)
        meta = payload.get("meta") or {}
        output = analyze_candles(
            candles, symbol, interval, provider="Twelve Data",
            basis=str(meta.get("exchange") or "Twelve Data aggregated reference")[:100],
        )
        cache.set(cache_key, output, timeout=CACHE_SECONDS)
        return output
    except (IntradayProviderError, ValueError, TypeError):
        result = {"status": "unavailable",
                  "detail": "No valid, sufficiently recent intraday candle data for this market/timeframe."}
        cache.set(cache_key, result, timeout=ERROR_CACHE_SECONDS)
        return result
    finally:
        cache.delete(lock_key)
