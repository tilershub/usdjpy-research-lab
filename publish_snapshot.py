from __future__ import annotations

import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

from trade90_model import (
    PAIR_CONFIGS,
    ModelConfig,
    calibrated_probabilities,
    confidence_grade,
    data_quality,
    fred_series,
    horizon_validation,
    pair_model_profile,
    prepare_features,
    regime,
    score_features,
    walk_forward_metrics,
)
from economic_events import event_risk_summary, events_for_pair, fetch_calendar
from newsfeed import fetch_news, news_for_pair
from policy_calendar import fetch_fomc_calendar, upcoming as upcoming_meetings
from policy_expectations import fetch_policy_expectations
from positioning import fetch_cftc, pair_positioning

OUTPUT = Path("public/terminal-snapshot.json")
YEARS = 7


def clean(value):
    if isinstance(value, dict):
        return {str(key): clean(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(item) for item in value]
    if value is None or (isinstance(value, (float, np.floating)) and not np.isfinite(value)):
        return None
    if isinstance(value, (pd.Timestamp, datetime, date)):
        return value.isoformat()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    return value


MIN_PRICE_OBSERVATIONS = 500
MAX_PRICE_AGE_DAYS = 7


def usable_price(series: pd.Series | None, today: date) -> bool:
    """A price feed is only usable if it is both deep enough and current."""
    if series is None or series.dropna().empty:
        return False
    clean_series = series.dropna()
    if len(clean_series) < MIN_PRICE_OBSERVATIONS:
        return False
    last = pd.Timestamp(clean_series.index[-1]).date()
    return (today - last).days <= MAX_PRICE_AGE_DAYS


def resolve_price(close: pd.DataFrame, pair, today: date) -> tuple[pd.Series, str, str]:
    """Prefer the configured feed, fall back only when it cannot carry the model.

    The basis and note travel with whichever series wins, so the terminal never
    labels a futures proxy as spot.
    """
    preferred = close[pair.ticker] if pair.ticker in close else None
    if usable_price(preferred, today):
        return preferred.dropna().rename(pair.symbol), pair.price_basis, pair.price_note
    if pair.fallback_ticker:
        fallback = close[pair.fallback_ticker] if pair.fallback_ticker in close else None
        if usable_price(fallback, today):
            return fallback.dropna().rename(pair.symbol), pair.fallback_basis, pair.fallback_note
    if preferred is not None and not preferred.dropna().empty:
        return preferred.dropna().rename(pair.symbol), pair.price_basis, pair.price_note
    raise RuntimeError(f"No usable price series for {pair.symbol}")


def history_payload(scored: pd.DataFrame, limit: int = 120) -> list[dict]:
    columns = ["close", "ema_fast", "ema_slow", "score"]
    history = scored[columns].dropna(subset=["close"]).tail(limit)
    return [
        {
            "date": clean(index),
            "close": clean(row.get("close")),
            "ema_fast": clean(row.get("ema_fast")),
            "ema_slow": clean(row.get("ema_slow")),
            "score": clean(row.get("score")),
        }
        for index, row in history.iterrows()
    ]


def event_payload(events: pd.DataFrame, now: datetime) -> dict:
    risk = event_risk_summary(events, now)
    upcoming = events.loc[events["time"] >= pd.Timestamp(now)].head(8) if not events.empty else events
    rows = []
    for _, row in upcoming.iterrows():
        rows.append({
            "time": clean(row.get("time")),
            "currency": clean(row.get("currency")),
            "event": clean(row.get("event")),
            "side": clean(row.get("side")),
            "previous": clean(row.get("previous")),
            "forecast": clean(row.get("forecast")),
        })
    return {"risk": clean(risk), "upcoming": rows}


def validation_payload(scored: pd.DataFrame) -> dict:
    walk_forward = clean(walk_forward_metrics(scored))
    horizons = horizon_validation(scored).reset_index()
    return {
        "walk_forward": walk_forward,
        "horizons": clean(horizons.to_dict(orient="records")),
    }


def main() -> None:
    end = date.today()
    generated_at = datetime.now(timezone.utc)
    start = end - timedelta(days=int(YEARS * 365.25 + 450))
    tickers = sorted(
        {p.ticker for p in PAIR_CONFIGS.values()}
        | {p.driver for p in PAIR_CONFIGS.values()}
        | {p.fallback_ticker for p in PAIR_CONFIGS.values() if p.fallback_ticker}
    )
    raw = yf.download(tickers, start=start, end=end + timedelta(days=1), auto_adjust=True, progress=False, threads=True)
    if raw.empty:
        raise RuntimeError("Market-data provider returned no observations")
    close = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw

    calendar, calendar_status = fetch_calendar(end - timedelta(days=35), end + timedelta(days=14))
    cftc_history, cftc_status = fetch_cftc()
    policy, policy_status = fetch_policy_expectations()
    news, news_status = fetch_news()
    meetings, meeting_status = fetch_fomc_calendar()

    pairs = []
    for symbol, pair in PAIR_CONFIGS.items():
        price, price_basis, price_note = resolve_price(close, pair, end)
        driver = close[pair.driver].dropna() if pair.driver in close else None
        features = prepare_features(
            price,
            fred_series(pair.base_yield),
            fred_series(pair.quote_yield),
            driver,
            pair.driver_sign,
            ModelConfig(),
            pair.macro_mode,
        )
        scored, components = score_features(features, pair_symbol=symbol)
        scored = scored.loc[scored.index >= pd.Timestamp(end - timedelta(days=int(YEARS * 365.25)))]
        latest = scored.dropna(subset=["score"]).iloc[-1]
        probabilities, sample = calibrated_probabilities(scored, float(latest.score))
        quality = data_quality(scored)
        profile = pair_model_profile(symbol)
        score = float(latest.score)
        bias = max(probabilities, key=probabilities.get)
        pair_events = events_for_pair(calendar, pair.base, pair.quote)
        positioning = pair_positioning(cftc_history, pair.base, pair.quote, generated_at)
        audit = components.loc[latest.name].sort_values(key=abs, ascending=False)
        pairs.append({
            "symbol": symbol,
            "base": pair.base,
            "quote": pair.quote,
            "asset_class": pair.asset_class,
            "price": clean(latest.close),
            "price_basis": price_basis,
            "price_note": price_note,
            "decimals": pair.decimals,
            "score": round(score, 1),
            "bias": bias,
            "confidence": confidence_grade(probabilities, sample, str(quality["grade"])),
            "probabilities": {key: round(float(value), 4) for key, value in probabilities.items()},
            "sample_size": sample,
            "quality": {
                "grade": quality["grade"],
                "completeness": round(float(quality["completeness"]), 4),
                "last_price": clean(quality["last_price"]),
                "price_age_days": quality["price_age_days"],
                "stale_inputs": quality["stale_inputs"],
            },
            "market": {
                "yield_spread": clean(latest.get("yield_spread")),
                "macro_label": pair.macro_label,
                "volatility": clean(latest.get("volatility")),
                "regime": regime(latest),
                "support20": clean(latest.get("support20")),
                "resistance20": clean(latest.get("resistance20")),
                "atr20": clean(latest.get("atr20")),
                "driver": pair.driver_label,
            },
            "model": {
                "thesis": profile.thesis,
                "price_note": price_note,
                "audit": [
                    {"name": str(name), "contribution": clean(value)}
                    for name, value in audit.items()
                ],
            },
            "history": history_payload(scored),
            "events": event_payload(pair_events, generated_at),
            "news": clean(news_for_pair(news, pair.base, pair.quote)),
            "positioning": {
                **clean(positioning),
                "provider": cftc_status.provider,
                "cadence": cftc_status.cadence,
                "fetched_at": clean(cftc_status.fetched_at),
                "provider_message": cftc_status.message,
            },
            "validation": validation_payload(scored),
        })

    payload = {
        "schema_version": 1,
        "generated_at": generated_at.isoformat(),
        "cadence": "Research model, events and positioning refresh every six hours; source series retain their published cadence",
        "sources": {
            "calendar": {
                "provider": calendar_status.provider,
                "mode": calendar_status.mode,
                "fetched_at": clean(calendar_status.fetched_at),
                "message": calendar_status.message,
            },
            "positioning": {
                "provider": cftc_status.provider,
                "cadence": cftc_status.cadence,
                "fetched_at": clean(cftc_status.fetched_at),
                "message": cftc_status.message,
            },
            "policy_expectations": {
                "provider": policy_status.provider,
                "cadence": policy_status.cadence,
                "fetched_at": clean(policy_status.fetched_at),
                "message": policy_status.message,
            },
            "policy_calendar": {
                "provider": meeting_status.provider,
                "cadence": meeting_status.cadence,
                "fetched_at": clean(meeting_status.fetched_at),
                "message": meeting_status.message,
            },
            "news": {
                "provider": news_status.provider,
                "cadence": news_status.cadence,
                "fetched_at": clean(news_status.fetched_at),
                "message": news_status.message,
            },
        },
        "policy_expectations": clean(policy),
        "policy_calendar": clean(upcoming_meetings(meetings, generated_at)),
        "pairs": sorted(pairs, key=lambda item: abs(item["score"]), reverse=True),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
