from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
import json
import os
import re
from typing import Iterable
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

CURRENCY_COUNTRIES = {"USD":"United States","EUR":"Euro Area","GBP":"United Kingdom","JPY":"Japan","CHF":"Switzerland","CAD":"Canada","AUD":"Australia","NZD":"New Zealand"}
COUNTRY_CURRENCIES = {country.lower(): currency for currency, country in CURRENCY_COUNTRIES.items()}

@dataclass(frozen=True)
class CalendarStatus:
    provider: str
    fetched_at: datetime
    mode: str
    message: str = ""

def _number(value) -> float:
    if value is None or value == "": return np.nan
    if isinstance(value, (int, float)): return float(value)
    text = str(value).strip().replace(",", "")
    match = re.search(r"[-+]?\d*\.?\d+", text)
    if not match: return np.nan
    number, upper = float(match.group()), text.upper()
    return number * (1e9 if "B" in upper else 1e6 if "M" in upper else 1e3 if "K" in upper else 1.0)

def normalize_calendar(records: Iterable[dict], now: datetime | None = None) -> pd.DataFrame:
    now = now or datetime.now(timezone.utc)
    rows = []
    for item in records:
        country = str(item.get("Country") or item.get("country") or "").strip()
        currency = COUNTRY_CURRENCIES.get(country.lower())
        timestamp = pd.to_datetime(item.get("Date") or item.get("date"), utc=True, errors="coerce")
        if not currency or pd.isna(timestamp): continue
        actual, forecast, previous = (_number(item.get(key)) for key in ("Actual", "Forecast", "Previous"))
        surprise = actual - forecast if np.isfinite(actual) and np.isfinite(forecast) else np.nan
        scale = max(abs(forecast), abs(previous) if np.isfinite(previous) else 0.0, 1e-9)
        rows.append({"time":timestamp,"currency":currency,"country":country,"event":str(item.get("Event") or item.get("Category") or "Economic release"),"category":str(item.get("Category") or ""),"importance":int(float(item.get("Importance") or 0)),"actual":item.get("Actual") or "—","forecast":item.get("Forecast") or "—","previous":item.get("Previous") or "—","surprise":surprise,"surprise_pct":surprise/scale if np.isfinite(surprise) else np.nan,"hours":(timestamp.to_pydatetime()-now).total_seconds()/3600})
    columns=["time","currency","country","event","category","importance","actual","forecast","previous","surprise","surprise_pct","hours"]
    return pd.DataFrame(rows,columns=columns).sort_values("time") if rows else pd.DataFrame(columns=columns)

def fetch_calendar(start: date, end: date, timeout: int = 15) -> tuple[pd.DataFrame, CalendarStatus]:
    key=os.getenv("TRADING_ECONOMICS_KEY","guest:guest")
    countries=",".join(CURRENCY_COUNTRIES.values())
    base=f"https://api.tradingeconomics.com/calendar/country/{quote(countries,safe=',')}"
    url=f"{base}/{start.isoformat()}/{end.isoformat()}?{urlencode({'c':key,'importance':3})}"
    fetched_at=datetime.now(timezone.utc)
    try:
        with urlopen(Request(url,headers={"User-Agent":"TRADE90-FX-Research/1.0","Accept":"application/json"}),timeout=timeout) as response: payload=json.loads(response.read().decode("utf-8"))
        if not isinstance(payload,list): raise ValueError("calendar provider returned an unexpected response")
        frame=normalize_calendar(payload,fetched_at)
        return frame,CalendarStatus("Trading Economics",fetched_at,"licensed" if key!="guest:guest" else "guest","" if not frame.empty else "No supported high-impact events were returned for this window.")
    except Exception as exc:
        return normalize_calendar([],fetched_at),CalendarStatus("Trading Economics",fetched_at,"unavailable",str(exc))

def events_for_pair(events: pd.DataFrame, base: str, quote_currency: str) -> pd.DataFrame:
    if events.empty: return events.copy()
    result=events[events["currency"].isin([base,quote_currency])].copy()
    result["side"]=np.where(result["currency"].eq(base),"Base currency","Quote currency")
    return result.sort_values("time")

def event_risk_summary(events: pd.DataFrame, now: datetime | None = None) -> dict:
    now=now or datetime.now(timezone.utc)
    if events.empty: return {"level":"Unknown","next_event":None,"hours":None,"count_24h":0}
    upcoming=events[events["time"]>=pd.Timestamp(now)].sort_values("time")
    if upcoming.empty: return {"level":"Low","next_event":None,"hours":None,"count_24h":0}
    hours=(upcoming.iloc[0]["time"].to_pydatetime()-now).total_seconds()/3600
    count=int((upcoming["time"]<=pd.Timestamp(now+timedelta(hours=24))).sum())
    level="Extreme" if hours<=2 else "High" if hours<=8 else "Elevated" if hours<=24 else "Normal"
    return {"level":level,"next_event":upcoming.iloc[0]["event"],"hours":max(hours,0.0),"count_24h":count}

def historical_event_reaction(events: pd.DataFrame, prices: pd.Series, category: str, horizon_days: int = 1) -> dict:
    if events.empty or prices.empty: return {"observations":0,"median_move":np.nan,"average_move":np.nan}
    matched=events[(events["category"]==category)&events["actual"].ne("—")]
    moves=[]; clean=prices.dropna().sort_index()
    for timestamp in matched["time"]:
        position=clean.index.searchsorted(pd.Timestamp(timestamp).tz_localize(None).normalize())
        if position<len(clean)-horizon_days: moves.append(abs(float(clean.iloc[position+horizon_days]/clean.iloc[position]-1)))
    return {"observations":len(moves),"median_move":float(np.median(moves)) if moves else np.nan,"average_move":float(np.mean(moves)) if moves else np.nan}
