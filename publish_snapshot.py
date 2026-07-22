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
    pair_model_profile,
    prepare_features,
    regime,
    score_features,
)

OUTPUT = Path("public/terminal-snapshot.json")
YEARS = 7


def clean(value):
    if value is None or (isinstance(value, (float, np.floating)) and not np.isfinite(value)):
        return None
    if isinstance(value, (pd.Timestamp, datetime, date)):
        return value.isoformat()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    return value


def main() -> None:
    end = date.today()
    start = end - timedelta(days=int(YEARS * 365.25 + 450))
    tickers = sorted({p.ticker for p in PAIR_CONFIGS.values()} | {p.driver for p in PAIR_CONFIGS.values()})
    raw = yf.download(tickers, start=start, end=end + timedelta(days=1), auto_adjust=True, progress=False, threads=True)
    if raw.empty:
        raise RuntimeError("Market-data provider returned no observations")
    close = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw

    pairs = []
    for symbol, pair in PAIR_CONFIGS.items():
        price = close[pair.ticker].dropna().rename(symbol)
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
        scored, _ = score_features(features, pair_symbol=symbol)
        scored = scored.loc[scored.index >= pd.Timestamp(end - timedelta(days=int(YEARS * 365.25)))]
        latest = scored.dropna(subset=["score"]).iloc[-1]
        probabilities, sample = calibrated_probabilities(scored, float(latest.score))
        quality = data_quality(scored)
        profile = pair_model_profile(symbol)
        score = float(latest.score)
        bias = max(probabilities, key=probabilities.get)
        pairs.append({
            "symbol": symbol,
            "base": pair.base,
            "quote": pair.quote,
            "asset_class": pair.asset_class,
            "price": clean(latest.close),
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
            "model": {"thesis": profile.thesis, "price_note": pair.price_note},
        })

    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cadence": "End-of-day FX, gold-futures and crypto data; macro series may be daily or monthly",
        "pairs": sorted(pairs, key=lambda item: abs(item["score"]), reverse=True),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
