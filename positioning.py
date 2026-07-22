from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from io import StringIO
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

CFTC_URL = "https://www.cftc.gov/dea/newcot/FinFutWk.txt"

CURRENCY_NAMES = {
    "EUR": ("EURO FX",),
    "GBP": ("BRITISH POUND",),
    "JPY": ("JAPANESE YEN",),
    "CHF": ("SWISS FRANC",),
    "CAD": ("CANADIAN DOLLAR",),
    "AUD": ("AUSTRALIAN DOLLAR",),
    "NZD": ("NEW ZEALAND DOLLAR",),
}

@dataclass(frozen=True)
class PositioningStatus:
    provider: str
    fetched_at: datetime
    cadence: str
    message: str = ""


def _column(frame: pd.DataFrame, *needles: str) -> str | None:
    normalized = {str(c).lower().replace("_", " ").strip(): c for c in frame.columns}
    for name, original in normalized.items():
        if all(needle.lower() in name for needle in needles):
            return original
    return None


def normalize_cftc(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=["currency", "date", "leveraged_net", "asset_manager_net", "open_interest"])
    market_col = _column(frame, "market") or frame.columns[0]
    date_col = _column(frame, "report", "date") or _column(frame, "as of date")
    lev_long = _column(frame, "lev", "long")
    lev_short = _column(frame, "lev", "short")
    am_long = _column(frame, "asset", "long")
    am_short = _column(frame, "asset", "short")
    oi_col = _column(frame, "open interest")
    if date_col is None or lev_long is None or lev_short is None:
        raise ValueError("CFTC file does not contain the expected TFF columns")

    records = []
    market = frame[market_col].astype(str).str.upper()
    for currency, aliases in CURRENCY_NAMES.items():
        mask = pd.Series(False, index=frame.index)
        for alias in aliases:
            mask |= market.str.contains(alias, regex=False)
        subset = frame.loc[mask].copy()
        if subset.empty:
            continue
        dates = pd.to_datetime(subset[date_col], errors="coerce", utc=True)
        for idx in subset.index:
            records.append({
                "currency": currency,
                "date": dates.loc[idx],
                "leveraged_net": pd.to_numeric(subset.loc[idx, lev_long], errors="coerce") - pd.to_numeric(subset.loc[idx, lev_short], errors="coerce"),
                "asset_manager_net": (
                    pd.to_numeric(subset.loc[idx, am_long], errors="coerce") - pd.to_numeric(subset.loc[idx, am_short], errors="coerce")
                    if am_long is not None and am_short is not None else np.nan
                ),
                "open_interest": pd.to_numeric(subset.loc[idx, oi_col], errors="coerce") if oi_col is not None else np.nan,
            })
    result = pd.DataFrame(records).dropna(subset=["date", "leveraged_net"])
    return result.sort_values(["currency", "date"]).reset_index(drop=True)


def fetch_cftc(timeout: int = 15) -> tuple[pd.DataFrame, PositioningStatus]:
    now = datetime.now(timezone.utc)
    request = Request(CFTC_URL, headers={"User-Agent": "TRADE90-research/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
        frame = pd.read_csv(StringIO(raw))
        return normalize_cftc(frame), PositioningStatus("CFTC Traders in Financial Futures", now, "Weekly; normally published Friday")
    except Exception as exc:
        return pd.DataFrame(columns=["currency", "date", "leveraged_net", "asset_manager_net", "open_interest"]), PositioningStatus(
            "CFTC Traders in Financial Futures", now, "Weekly", f"Positioning unavailable: {exc}"
        )


def currency_snapshot(history: pd.DataFrame, currency: str, now: datetime | None = None) -> dict:
    subset = history.loc[history["currency"] == currency].dropna(subset=["leveraged_net"]).sort_values("date")
    if subset.empty:
        return {"currency": currency, "available": False}
    latest = subset.iloc[-1]
    window = subset.tail(156)
    values = window["leveraged_net"].astype(float)
    percentile = float((values <= float(latest["leveraged_net"])).mean())
    mean, std = float(values.mean()), float(values.std(ddof=0))
    zscore = (float(latest["leveraged_net"]) - mean) / std if std > 0 else 0.0
    current = pd.Timestamp(now or datetime.now(timezone.utc))
    report_date = pd.Timestamp(latest["date"])
    if current.tzinfo is None:
        current = current.tz_localize("UTC")
    if report_date.tzinfo is None:
        report_date = report_date.tz_localize("UTC")
    age = max((current.normalize() - report_date.normalize()).days, 0)
    crowded = "Crowded long" if percentile >= .9 else "Crowded short" if percentile <= .1 else "Balanced"
    return {
        "currency": currency, "available": True, "date": report_date, "age_days": int(age),
        "leveraged_net": float(latest["leveraged_net"]), "asset_manager_net": float(latest["asset_manager_net"]) if pd.notna(latest["asset_manager_net"]) else np.nan,
        "percentile_3y": percentile, "zscore_3y": float(zscore), "crowding": crowded,
        "stale": age > 10,
    }


def pair_positioning(history: pd.DataFrame, base: str, quote: str, now: datetime | None = None) -> dict:
    base_view = currency_snapshot(history, base, now)
    quote_view = currency_snapshot(history, quote, now)
    available = base_view.get("available", False) and quote_view.get("available", False)
    if not available:
        return {"available": False, "base": base_view, "quote": quote_view, "relative_percentile": np.nan, "warning": "A complete base/quote CFTC comparison is unavailable."}
    relative = float(base_view["percentile_3y"] - quote_view["percentile_3y"])
    warning = ""
    if base_view["stale"] or quote_view["stale"]:
        warning = "CFTC observations are stale and excluded from directional interpretation."
    elif abs(relative) >= .75:
        warning = "Positioning is extremely one-sided; reversal and squeeze risk may be elevated."
    return {"available": True, "base": base_view, "quote": quote_view, "relative_percentile": relative, "warning": warning}


def derivatives_availability() -> pd.DataFrame:
    return pd.DataFrame([
        {"Dataset": "CFTC leveraged funds", "Status": "Available", "Provider": "CFTC", "Cadence": "Weekly / delayed"},
        {"Dataset": "CFTC asset managers", "Status": "Available when reported", "Provider": "CFTC", "Cadence": "Weekly / delayed"},
        {"Dataset": "FX implied volatility", "Status": "Provider required", "Provider": "Not configured", "Cadence": "—"},
        {"Dataset": "25-delta risk reversal", "Status": "Provider required", "Provider": "Not configured", "Cadence": "—"},
        {"Dataset": "Retail positioning", "Status": "Provider required", "Provider": "Not configured", "Cadence": "—"},
    ])
