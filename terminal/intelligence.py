"""Evidence-led summaries of the existing published TRADE90 research snapshot.

No forecasts or quotes are generated in this module. Values are sourced from the
publisher's snapshot, and missing source coverage remains explicitly unknown.
"""
from datetime import datetime, timezone
from math import isfinite

from .event_guard import recent_high_impact


MARKET_NAMES = {
    "XAU/USD": "Gold", "EUR/USD": "Euro / US Dollar",
    "GBP/USD": "Pound / US Dollar", "USD/JPY": "US Dollar / Yen",
    "USD/CHF": "US Dollar / Swiss Franc", "USD/CAD": "US Dollar / Canadian Dollar",
    "AUD/USD": "Australian / US Dollar", "NZD/USD": "New Zealand / US Dollar",
    "BTC/USD": "Bitcoin",
}


def numeric(value):
    if isinstance(value, bool):
        return None
    try:
        result = float(value)
        return result if isfinite(result) else None
    except (ValueError, TypeError, OverflowError):
        return None


def as_utc(value):
    if not isinstance(value, str):
        return None
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if result.tzinfo is None:
            result = result.replace(tzinfo=timezone.utc)
        return result.astimezone(timezone.utc)
    except (ValueError, OverflowError):
        return None


def _pct(value):
    val = numeric(value)
    return round(val * 100, 1) if val is not None else None


def _observations(pair):
    history = pair.get("history") or []
    result = []
    for observation in history[-70:]:
        if not isinstance(observation, dict):
            continue
        price = numeric(observation.get("close"))
        date = observation.get("date")
        if price is not None and isinstance(date, str):
            result.append({"date": date[:10], "close": price})
    return result


def _news(pair):
    currencies = {pair.get("base"), pair.get("quote")}
    items = []
    for news in pair.get("news") or []:
        if not isinstance(news, dict) or news.get("currency") not in currencies:
            continue
        url = str(news.get("url") or "")
        if not url.startswith(("https://", "http://")):
            continue
        items.append({
            "headline": str(news.get("headline") or "")[:250],
            "source": str(news.get("source") or "")[:90],
            "currency": str(news.get("currency") or ""),
            "published_at": news.get("published_at"),
            "url": url,
        })
    return items[:4]


def _drivers(pair):
    audit = (pair.get("model") or {}).get("audit") or []
    results = []
    for row in audit:
        if not isinstance(row, dict):
            continue
        contribution = numeric(row.get("contribution"))
        if contribution is None:
            continue
        results.append({"name": str(row.get("name") or "Unlabelled")[:75],
                        "contribution": round(contribution, 1)})
    return sorted(results, key=lambda d: abs(d["contribution"]), reverse=True)[:5]


def market_brief(pair, generated_at, source_status, now, event_context=None):
    symbol = pair.get("symbol")
    if symbol not in MARKET_NAMES:
        return None
    quality = pair.get("quality") or {}
    market = pair.get("market") or {}
    model = pair.get("model") or {}
    validation = pair.get("validation") or {}
    horizons = validation.get("horizons") or []
    five_day = next((h for h in horizons if isinstance(h, dict) and h.get("Horizon") == "5D"), {})
    event = pair.get("events") or {}
    risk = event.get("risk") or {}
    positioning = pair.get("positioning") or {}
    base_position = positioning.get("base") or {}

    score = numeric(pair.get("score"))
    bias = pair.get("bias") if pair.get("bias") in ("Bullish", "Bearish", "Neutral") else "Unknown"
    conflicting = (score is not None and
                   ((score <= -20 and bias == "Bullish") or (score >= 20 and bias == "Bearish")))
    probs = pair.get("probabilities") or {}
    bullish = _pct(probs.get("Bullish"))
    bearish = _pct(probs.get("Bearish"))
    neutral = _pct(probs.get("Range/neutral"))
    diff = round(bullish - bearish, 1) if bullish is not None and bearish is not None else None
    small_margin = diff is not None and abs(diff) < 10

    model_acc = _pct(five_day.get("Model accuracy"))
    baseline_acc = _pct(five_day.get("Majority baseline"))
    lift = round(model_acc - baseline_acc, 1) if model_acc is not None and baseline_acc is not None else None
    validation_message = (
        "Five-day model did not beat its majority baseline in this test."
        if lift is not None and lift <= 0 else
        "Five-day model beat its majority baseline in this sample only; no future edge is assured."
        if lift is not None else "Historical model comparison is unavailable."
    )

    last_price = quality.get("last_price")
    observed_at = as_utc(last_price)
    snapshot_time = as_utc(generated_at)
    snapshot_age_hours = max(0, (now - snapshot_time).total_seconds() / 3600) if snapshot_time else None
    observation_age_days = max(0, (now - observed_at).total_seconds() / 86400) if observed_at else None

    calendar_source = source_status.get("calendar") or {}
    calendar_available = calendar_source.get("mode") not in ("unavailable", "failed", "error") and (
        bool((event.get("upcoming") or [])) or risk.get("level") not in (None, "Unknown", "Unavailable"))
    grade = str(quality.get("grade") or "Unknown")
    stale_inputs = [str(x) for x in (quality.get("stale_inputs") or [])][:8]
    quality_warnings = []
    if snapshot_age_hours is None:
        quality_warnings.append("Snapshot publication time unavailable.")
    elif snapshot_age_hours > 36:
        quality_warnings.append("Published snapshot is more than 36 hours old.")
    if observed_at is None:
        quality_warnings.append("Price observation time unavailable.")
    elif observation_age_days > 3:
        quality_warnings.append("Last price observation is more than three calendar days old; check market holidays.")
    if grade in ("C", "D", "F", "Unknown"):
        quality_warnings.append("Data-quality grade is " + grade + ".")
    if stale_inputs:
        quality_warnings.append("Missing or stale model inputs: " + ", ".join(stale_inputs) + ".")
    if not calendar_available:
        quality_warnings.append("Economic calendar coverage unavailable; event risk is unknown.")
    if conflicting:
        quality_warnings.append("Published directional bias conflicts with the signed model score; do not infer a trade signal.")
    if small_margin:
        quality_warnings.append("Bullish and bearish scenario frequencies are close; conviction is limited.")
    if lift is not None and lift <= 0:
        quality_warnings.append("Five-day validation did not outperform a simple majority-class baseline.")

    support = numeric(market.get("support20"))
    resistance = numeric(market.get("resistance20"))
    basis = str(pair.get("price_basis") or "Unspecified")
    if symbol == "XAU/USD" and "futures" in basis.lower():
        quality_warnings.append("Gold reference is COMEX futures, not spot CFD: broker execution levels will differ.")

    # A recently scheduled major US macro release invalidates the *currentness*
    # of a pre-release directional label. We never auto-flip bullish to bearish
    # without an observed, licensed intraday data series.
    macro_release = event_context if isinstance(event_context, dict) else {}
    near_event = macro_release.get("status") in ("upcoming", "released_or_due")
    event_time = as_utc(macro_release.get("scheduled_at"))
    pre_event_snapshot = (
        near_event and event_time is not None and
        (snapshot_time is None or snapshot_time < event_time)
    )
    if pre_event_snapshot:
        quality_warnings.insert(0,
            "High-impact BLS event occurred after this snapshot or is imminent. "
            "The historical bias has NOT been recalculated for the release.")
    elif near_event:
        quality_warnings.insert(0,
            "High-impact U.S. event window: the historical model is not confirmed "
            "to incorporate the release or current market reaction.")
    if conflicting:
        quality_warnings.insert(0,
            "Historical Bullish/Bearish classification is contradicted by "
            "the signed model score. Do not treat it as a current bias.")
    quality_warnings.insert(0,
        "No verified current-session OHLC evidence in this publisher snapshot. "
        "Bias and levels are historical; no current direction is established.")


    return {
        "symbol": symbol, "slug": symbol.replace("/", "").lower(),
        "name": MARKET_NAMES[symbol], "asset_class": pair.get("asset_class"),
        "price": numeric(pair.get("price")), "price_basis": basis,
        "price_note": str(pair.get("price_note") or "")[:500],
        "decimals": min(6, max(0, int(pair.get("decimals") or 2))),
        "price_observed_at": last_price, "observation_age_days": round(observation_age_days, 1) if observation_age_days is not None else None,
        "quality_grade": grade, "stale_inputs": stale_inputs,
        "model_score": score, "published_bias": bias,
        "score_bias_conflict": conflicting, "confidence_label": pair.get("confidence"),
        "published_bias_use": "historical_only",
        "current_direction": "Not established",
        "high_impact_event": macro_release if near_event else None,
        "pre_event_snapshot": bool(pre_event_snapshot),
        "scenario_frequencies": {"bullish": bullish, "neutral": neutral, "bearish": bearish},
        "frequency_margin": diff,
        "regime": market.get("regime") or "Unknown",
        "volatility_annualized": _pct(market.get("volatility")),
        "support20": support, "resistance20": resistance,
        "atr20": numeric(market.get("atr20")), "cross_asset_driver": market.get("driver"),
        "macro_label": market.get("macro_label"),
        "model_thesis": str(model.get("thesis") or "")[:300],
        "drivers": _drivers(pair), "chart": _observations(pair),
        "positioning": {
            "available": bool(positioning.get("available")),
            "as_of": base_position.get("date"),
            "crowding": base_position.get("crowding"),
            "stale": bool(base_position.get("stale")),
            "warning": str(positioning.get("warning") or "")[:240],
        },
        "events": {
            "coverage": "Available" if calendar_available else "Unknown — provider unavailable",
            "level": risk.get("level") if calendar_available else "Unknown",
            "upcoming": (event.get("upcoming") or [])[:5] if calendar_available else [],
        },
        "news": _news(pair),
        "validation": {
            "horizon": "5D", "accuracy_pct": model_acc, "baseline_pct": baseline_acc,
            "lift_pp": lift, "observations": five_day.get("OOS observations"),
            "message": validation_message,
        },
        "warnings": quality_warnings,
        "snapshot_old": snapshot_age_hours is None or snapshot_age_hours > 36,
    }


def build_intelligence(snapshot, now=None):
    now = now or datetime.now(timezone.utc)
    if not isinstance(snapshot, dict) or snapshot.get("schema_version") != 1:
        return {"status": "unavailable", "markets": [], "detail": "No verified published snapshot available."}
    pairs = snapshot.get("pairs")
    if not isinstance(pairs, list):
        return {"status": "unavailable", "markets": [], "detail": "Published snapshot has no markets."}
    generated_at = snapshot.get("generated_at")
    source_status = snapshot.get("sources") or {}
    high_impact = recent_high_impact(now)
    markets = [market_brief(p, generated_at, source_status, now, high_impact)
               for p in pairs if isinstance(p, dict)]
    markets = [m for m in markets if m is not None]
    if not markets:
        return {"status": "unavailable", "markets": [], "detail": "No usable market research available."}
    return {
        "status": "ok",
        "generated_at": generated_at,
        "snapshot_age_hours": round(max(0, (now - as_utc(generated_at)).total_seconds() / 3600), 1) if as_utc(generated_at) else None,
        "cadence": snapshot.get("cadence"),
        "high_impact": high_impact,
        "assessment_integrity": "Historical daily research, NOT a live recommendation. Major BLS releases temporarily supersede old model labels.",
        "sources": {
            "calendar": {"provider": (source_status.get("calendar") or {}).get("provider"),
                         "status": (source_status.get("calendar") or {}).get("mode") or "unknown"},
            "policy_expectations": {"status": "unavailable" if (source_status.get("policy_expectations") or {}).get("message") else "check source"},
        },
        "markets": markets,
        "disclosure": "Delayed, end-of-day and source-dependent research. No trade signals, executable quotes or guarantees.",
    }
