from __future__ import annotations

import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

# The legacy newcot text file is published without a header row, so a positional
# parse silently mislabels every column. CFTC's public reporting API serves the
# same weekly reports as named JSON fields and needs no key.
TFF_URL = "https://publicreporting.cftc.gov/resource/gpe5-46if.json"
DISAGGREGATED_URL = "https://publicreporting.cftc.gov/resource/72hh-3qpy.json"

# Traders in Financial Futures covers currencies, rates and equity indices only.
# Metals are commodities and appear exclusively in the Disaggregated report, so
# gold needs a second request against a different dataset and column vocabulary.
TFF_MARKETS = {
    "USD": "USD INDEX - ICE FUTURES U.S.",
    "EUR": "EURO FX - CHICAGO MERCANTILE EXCHANGE",
    "GBP": "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE",
    "JPY": "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE",
    "CHF": "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE",
    "CAD": "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
    "AUD": "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
    "NZD": "NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE",
    "BTC": "BITCOIN - CHICAGO MERCANTILE EXCHANGE",
}
DISAGGREGATED_MARKETS = {
    "XAU": "GOLD - COMMODITY EXCHANGE INC.",
}

# Speculative leg first, intermediary leg second. The two reports name these
# groups differently, so each dataset maps onto the same pair of series.
TFF_FIELDS = ("lev_money_positions_long", "lev_money_positions_short", "asset_mgr_positions_long", "asset_mgr_positions_short")
DISAGGREGATED_FIELDS = ("m_money_positions_long_all", "m_money_positions_short_all", "swap_positions_long_all", "swap__positions_short_all")

REPORT_LABELS = {
    "TFF": "CFTC Traders in Financial Futures",
    "DISAGGREGATED": "CFTC Disaggregated (commodities)",
}
SPECULATIVE_LABELS = {"TFF": "Leveraged funds", "DISAGGREGATED": "Managed money"}
INTERMEDIARY_LABELS = {"TFF": "Asset managers", "DISAGGREGATED": "Swap dealers"}

COLUMNS = ["currency", "date", "leveraged_net", "asset_manager_net", "open_interest", "report"]

@dataclass(frozen=True)
class PositioningStatus:
    provider: str
    fetched_at: datetime
    cadence: str
    message: str = ""


def normalize_cftc(records: Iterable[dict], markets: Mapping[str, str], fields: Sequence[str], report: str) -> pd.DataFrame:
    """Reduce one CFTC report to a net-position series per traded asset."""
    spec_long, spec_short, inter_long, inter_short = fields
    by_market = {name: key for key, name in markets.items()}
    rows = []
    for record in records:
        key = by_market.get(str(record.get("market_and_exchange_names", "")).strip())
        if key is None:
            continue
        rows.append({
            "currency": key,
            "date": pd.to_datetime(record.get("report_date_as_yyyy_mm_dd"), errors="coerce", utc=True),
            "leveraged_net": _numeric(record.get(spec_long)) - _numeric(record.get(spec_short)),
            "asset_manager_net": _numeric(record.get(inter_long)) - _numeric(record.get(inter_short)),
            "open_interest": _numeric(record.get("open_interest_all")),
            "report": report,
        })
    if not rows:
        return pd.DataFrame(columns=COLUMNS)
    return pd.DataFrame(rows).dropna(subset=["date", "leveraged_net"])


def _numeric(value) -> float:
    return pd.to_numeric(value, errors="coerce")


def _request(url: str, markets: Mapping[str, str], timeout: int) -> list[dict]:
    names = ",".join("'" + name.replace("'", "''") + "'" for name in markets.values())
    query = urlencode({
        "$where": f"market_and_exchange_names in({names})",
        "$order": "report_date_as_yyyy_mm_dd DESC",
        "$limit": 5000,
    })
    request = Request(f"{url}?{query}", headers={"User-Agent": "TRADE90-research/1.0", "Accept": "application/json"})
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_cftc(timeout: int = 30) -> tuple[pd.DataFrame, PositioningStatus]:
    now = datetime.now(timezone.utc)
    frames, failures = [], []
    for url, markets, fields, report in (
        (TFF_URL, TFF_MARKETS, TFF_FIELDS, "TFF"),
        (DISAGGREGATED_URL, DISAGGREGATED_MARKETS, DISAGGREGATED_FIELDS, "DISAGGREGATED"),
    ):
        try:
            frames.append(normalize_cftc(_request(url, markets, timeout), markets, fields, report))
        except Exception as exc:
            failures.append(f"{REPORT_LABELS[report]}: {exc}")
    combined = pd.concat([f for f in frames if not f.empty], ignore_index=True) if any(not f.empty for f in frames) else pd.DataFrame(columns=COLUMNS)
    if not combined.empty:
        combined = combined.sort_values(["currency", "date"]).reset_index(drop=True)
    provider = "CFTC Commitments of Traders (TFF + Disaggregated)"
    cadence = "Weekly; positions as of Tuesday, published Friday"
    if failures and combined.empty:
        return combined, PositioningStatus(provider, now, cadence, "Positioning unavailable: " + "; ".join(failures))
    return combined, PositioningStatus(provider, now, cadence, "; ".join(failures))


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
    report = str(latest["report"]) if "report" in subset.columns else "TFF"
    return {
        "currency": currency, "available": True, "date": report_date, "age_days": int(age),
        "leveraged_net": float(latest["leveraged_net"]), "asset_manager_net": float(latest["asset_manager_net"]) if pd.notna(latest["asset_manager_net"]) else np.nan,
        "percentile_3y": percentile, "zscore_3y": float(zscore), "crowding": crowded,
        "stale": age > 10,
        "report": REPORT_LABELS.get(report, report),
        "speculative_label": SPECULATIVE_LABELS.get(report, "Speculative"),
        "intermediary_label": INTERMEDIARY_LABELS.get(report, "Intermediary"),
        "open_interest": float(latest["open_interest"]) if pd.notna(latest["open_interest"]) else np.nan,
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
