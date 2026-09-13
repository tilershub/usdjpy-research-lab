"""Sourced market conditions. No directional scores, signals or fair-value targets.

Observation dates are not release timestamps. The public FRED CSV contains
latest-vintage data; we retain that limitation on every observation.
"""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd
from trade90_model import fred_series
from economic_events import fetch_calendar
from newsfeed import fetch_news
from positioning import fetch_cftc, currency_snapshot
from policy_expectations import fetch_policy_expectations
from retail_sentiment import fetch_retail
from japan_statistics import fetch_japan_statistics


@dataclass(frozen=True)
class Indicator:
    id: str
    label: str
    country: str
    section: str
    unit: str
    frequency: str
    max_age_days: int
    publisher: str
    transform: str = 'level'
    note: str = ''


INDICATORS = [
    Indicator('DFEDTARL', 'Fed target lower bound', 'US', 'policy', '%', 'Daily', 7, 'Federal Reserve'),
    Indicator('DFEDTARU', 'Fed target upper bound', 'US', 'policy', '%', 'Daily', 7, 'Federal Reserve'),
    Indicator('DFF', 'Effective federal funds rate', 'US', 'policy', '%', 'Daily', 7, 'Federal Reserve', note='Observed overnight rate, not the target range.'),
    Indicator('IRSTCI01JPM156N', 'Japan overnight call/interbank rate', 'JP', 'policy', '%', 'Monthly', 100, 'OECD via FRED', note='Monthly market-rate series; not the current BOJ policy target.'),
    Indicator('CPIAUCNS', 'Headline CPI inflation', 'US', 'economy', '% YoY', 'Monthly', 75, 'BLS', 'yoy', 'All items, not seasonally adjusted.'),
    Indicator('PCEPILFE', 'Core PCE inflation', 'US', 'economy', '% YoY', 'Monthly', 75, 'BEA', 'yoy', 'Excludes food and energy; seasonally adjusted index.'),
    Indicator('UNRATE', 'Unemployment', 'US', 'economy', '%', 'Monthly', 75, 'BLS', note='Seasonally adjusted; national definitions differ.'),
    Indicator('PAYEMS', 'Payroll employment change', 'US', 'economy', 'thousand jobs', 'Monthly', 75, 'BLS', 'diff', 'Change from previous month; seasonally adjusted.'),
    Indicator('GDPC1', 'Real GDP growth', 'US', 'economy', '% QoQ', 'Quarterly', 200, 'BEA', 'qoq', 'Quarter-on-quarter, NOT annualized; seasonally adjusted.'),
    Indicator('JPNRGDPEXP', 'Real GDP growth', 'JP', 'economy', '% QoQ', 'Quarterly', 200, 'Cabinet Office Japan', 'qoq', 'Quarter-on-quarter, NOT annualized; seasonally adjusted.'),
    Indicator('DGS2', 'US 2-year Treasury yield', 'US', 'yields', '%', 'Daily', 7, 'Federal Reserve'),
    Indicator('DGS10', 'US 10-year Treasury yield', 'US', 'yields', '%', 'Daily', 7, 'Federal Reserve'),
    Indicator('IRLTLT01JPM156N', 'Japan 10-year government yield', 'JP', 'yields', '%', 'Monthly', 100, 'OECD via FRED', note='Monthly series. Never subtract from a daily US quote without aligning periods.'),
    Indicator('DFII10', 'US 10-year real yield', 'US', 'yields', '%', 'Daily', 7, 'Federal Reserve', note='Inflation-indexed Treasury yield.'),
    Indicator('T10YIE', 'US 10-year breakeven inflation', 'US', 'yields', '%', 'Daily', 7, 'Federal Reserve Bank of St. Louis', note='Market measure includes risk and liquidity premia; not a pure inflation forecast.'),
    Indicator('WALCL', 'Federal Reserve total assets', 'US', 'liquidity', 'USD million', 'Weekly', 14, 'Federal Reserve', note='Balance-sheet stock. A change alone does not identify QE, QT or its purpose.'),
    Indicator('M2SL', 'US broad money growth', 'US', 'liquidity', '% YoY', 'Monthly', 90, 'Federal Reserve', 'yoy', 'M2; distinct from reserves, lending and cross-border flows.'),
    Indicator('VIXCLS', 'Equity implied volatility (VIX)', 'Global', 'risk', 'index', 'Daily', 7, 'CBOE via FRED', note='US equity options measure; not FX or gold implied volatility.'),
    Indicator('DTWEXBGS', 'Broad US dollar index', 'Global', 'risk', 'index', 'Daily', 10, 'Federal Reserve'),
    Indicator('DCOILWTICO', 'WTI crude spot', 'Global', 'risk', 'USD/barrel', 'Daily', 10, 'EIA', note='Energy-price context; does not confirm a geopolitical cause.'),
]


def iso(value):
    return pd.Timestamp(value).isoformat()


def transform_series(series, spec):
    """Reindex periods before differences; a missing month must not become a year."""
    s = pd.to_numeric(series, errors='coerce').sort_index()
    if s.index.has_duplicates or not np.isfinite(s.dropna().to_numpy()).all():
        raise ValueError('Invalid observations')
    if spec.transform == 'level':
        return s.dropna()
    freq = 'Q' if spec.frequency == 'Quarterly' else 'M'
    s.index = s.index.to_period(freq)
    if s.index.has_duplicates:
        raise ValueError('Duplicate observation period')
    s = s.reindex(pd.period_range(s.index.min(), s.index.max(), freq=freq))
    if spec.transform == 'diff':
        result = s.diff()
    else:
        lag = 12 if spec.transform == 'yoy' else 1
        result = (s / s.shift(lag).replace(0, np.nan) - 1) * 100
    result.index = result.index.to_timestamp()
    return result.dropna()


def observation(spec, raw, now):
    result = {**asdict(spec), 'source_url': f'https://fred.stlouisfed.org/series/{spec.id}',
              'retrieved_at': iso(now), 'released_at': None, 'vintage': 'latest available; revisions possible',
              'status': 'unavailable', 'value': None, 'previous': None, 'change': None, 'history': []}
    try:
        values = transform_series(raw, spec)
        if values.empty:
            return result
        latest_date = values.index[-1]
        age = (pd.Timestamp(now).tz_localize(None).normalize() - latest_date.normalize()).days
        if age < 0:
            raise ValueError('Future observation')
        latest = float(values.iloc[-1])
        if not np.isfinite(latest):
            raise ValueError('Nonfinite result')
        previous = float(values.iloc[-2]) if len(values) > 1 else None
        result.update(status='stale' if age > spec.max_age_days else 'available', value=latest,
                      previous=previous, change=latest-previous if previous is not None else None,
                      observed_at=iso(latest_date), age_days=age,
                      history=[{'date': iso(t), 'value': float(v)} for t, v in values.tail(24).items()])
    except (ValueError, TypeError, IndexError):
        result['message'] = 'Observation failed validation.'
    return result


def load_indicator(spec, now):
    try:
        raw = fred_series(spec.id, timeout=20)
        return observation(spec, raw, now), raw
    except Exception:
        # Never echo request URLs/credentials from provider exceptions.
        return {**observation(spec, pd.Series(dtype=float), now), 'message': 'Source retrieval failed.'}, pd.Series(dtype=float)


def aligned_yield_spread(raw, now):
    """Only compare complete overlapping monthly averages, never daily vs monthly."""
    us, jp = raw.get('DGS10'), raw.get('IRLTLT01JPM156N')
    base = {'id': 'USJP10Y', 'label': 'US–Japan 10Y yield spread', 'unit': 'percentage points',
            'status': 'unavailable', 'value': None, 'change': None,
            'method': 'US daily observations averaged by month minus Japan monthly yield; completed common months only.',
            'source_ids': ['DGS10', 'IRLTLT01JPM156N']}
    if us is None or jp is None or us.empty or jp.empty:
        return base
    a, b = us.groupby(us.index.to_period('M')).mean(), jp.groupby(jp.index.to_period('M')).mean()
    # Reject sparse US months and do not forward fill missing Japanese months.
    count = us.groupby(us.index.to_period('M')).count()
    a = a[count >= 15]
    both = pd.concat([a.rename('US'), b.rename('JP')], axis=1).dropna()
    both = both[both.index < pd.Timestamp(now).tz_localize(None).to_period('M')]
    if both.empty:
        return base
    spread = both.US - both.JP
    stamp = spread.index[-1].to_timestamp()
    age = (pd.Timestamp(now).tz_localize(None) - stamp).days
    previous = float(spread.iloc[-2]) if len(spread)>1 else None
    return {**base, 'status': 'stale' if age > 100 else 'available', 'value': float(spread.iloc[-1]),
            'previous': previous, 'change': float(spread.iloc[-1])-previous if previous is not None else None,
            'observed_at': iso(stamp)}


SOURCE_WATCH = [
    {'section': 'Monetary policy', 'name': 'Federal Reserve decisions and projections', 'url': 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm', 'status': 'Official document reference'},
    {'section': 'Monetary policy', 'name': 'Bank of Japan decisions', 'url': 'https://www.boj.or.jp/en/mopo/mpmdeci/index.htm', 'status': 'Official document reference'},
    {'section': 'Bond purchases', 'name': 'BOJ market operations', 'url': 'https://www.boj.or.jp/en/mopo/outline/index.htm', 'status': 'Official document reference'},
    {'section': 'Fiscal policy', 'name': 'US Treasury fiscal data', 'url': 'https://fiscaldata.treasury.gov/', 'status': 'Official document reference'},
    {'section': 'Fiscal policy', 'name': 'Japan Ministry of Finance budget', 'url': 'https://www.mof.go.jp/english/policy/budget/index.html', 'status': 'Official document reference'},
    {'section': 'Trade', 'name': 'Japan trade statistics', 'url': 'https://www.customs.go.jp/toukei/info/index_e.htm', 'status': 'Official document reference'},
    {'section': 'FX intervention', 'name': 'Japan MOF confirmed operations', 'url': 'https://www.mof.go.jp/english/policy/international_policy/reference/feio/index.html', 'status': 'Official document reference'},
]


def service_status(retail=None):
    return [
        {'name': 'Retail positioning', 'status': (retail or {}).get('status','Credentials and display permission required'), 'source': 'Myfxbook / broker-specific samples'},
        {'name': 'Other retail sentiment', 'status': 'Provider agreement required', 'source': 'IG / other permitted providers; samples must remain separate'},
        {'name': 'Institutional forecast revisions', 'status': 'Licensed research feed required', 'source': 'Bank publications / licensed news'},
        {'name': 'Geopolitical event verification', 'status': 'Curated or licensed feed required', 'source': 'Official announcements plus corroborating reporting'},
        {'name': 'FX options and order flow', 'status': 'Licensed market feed required', 'source': 'Venue-specific data; no global spot-FX order book'},
        {'name': 'Gold spot history and ETF flows', 'status': 'Consistent historical feed required', 'source': 'Spot provider and fund issuers; futures history is separate'},
        {'name': 'Crypto funding, liquidations and flows', 'status': 'Exchange adapters required', 'source': 'Venue-specific coverage; no universal institutional-flow measure'},
        {'name': 'Fair-value estimates', 'status': 'Not established', 'source': 'No validated valuation model; no target displayed'},
    ]


def clean(value):
    if isinstance(value, dict): return {str(k): clean(v) for k,v in value.items()}
    if isinstance(value, (list, tuple)): return [clean(v) for v in value]
    if isinstance(value, (pd.Timestamp, datetime)): return iso(value)
    if isinstance(value, (float, np.floating)): return float(value) if np.isfinite(value) else None
    if isinstance(value, np.integer): return int(value)
    return value


def recent_events(frame, now):
    rows=[]
    for _, row in frame.sort_values('time').iterrows():
        if not now-timedelta(days=7) <= row.time.to_pydatetime() <= now+timedelta(days=14): continue
        rows.append({k: clean(row.get(k)) for k in ('time','currency','event','actual','forecast','previous','revised','source_url','unit')})
    return rows


def build_context(now=None):
    now = now or datetime.now(timezone.utc)
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda spec: load_indicator(spec, now), INDICATORS))
    indicators = [r[0] for r in results] + fetch_japan_statistics(now)
    raw = {spec.id: result[1] for spec, result in zip(INDICATORS, results)}
    with ThreadPoolExecutor(max_workers=4) as pool:
        calendar_job = pool.submit(fetch_calendar, (now-timedelta(days=7)).date(), (now+timedelta(days=14)).date())
        news_job = pool.submit(fetch_news)
        positioning_job = pool.submit(fetch_cftc)
        policy_job = pool.submit(fetch_policy_expectations)
        calendar, calendar_status = calendar_job.result()
        news, news_status = news_job.result()
        positions, positions_status = positioning_job.result()
        policy, policy_status = policy_job.result()
    retail = fetch_retail()
    try:
        policy_age = (pd.Timestamp(now).tz_localize(None) - pd.Timestamp(policy.get('observed')).tz_localize(None)).days
        policy_availability = 'available' if 0 <= policy_age <= 7 else 'stale'
    except (TypeError, ValueError):
        policy_availability = 'unavailable'
    return clean({'schema_version': 1, 'methodology': 'research-context-1', 'generated_at': now,
        'retail': retail, 'indicators': indicators, 'comparisons': [aligned_yield_spread(raw, now)],
        'communications': news, 'communications_status': 'partial' if news_status.message else 'available',
        'events': recent_events(calendar, now), 'calendar_status': calendar_status.mode,
        'calendar_note': 'Provider-reported consensus; pre-release forecast snapshots are not yet archived. No surprise backtest is claimed.',
        'positioning': [currency_snapshot(positions, c, now) for c in ('USD','JPY','EUR','GBP','CHF','CAD','AUD','NZD','XAU','BTC')],
        'positioning_status': 'partial' if positions_status.message else 'available',
        'policy_expectations': policy, 'policy_expectations_status': 'unavailable' if policy_status.message else policy_availability,
        'policy_expectations_note': 'Atlanta Fed model estimates for reference windows, not central-bank commitments or next-meeting odds.',
        'official_references': SOURCE_WATCH, 'services': service_status(retail),
        'limitations': ['Latest-vintage macro data; observation dates are not release timestamps.',
                       'Cadences differ; monthly Japanese rates are not current policy targets.',
                       'Official reference links are not automatically verified policy summaries.',
                       'No directional score, trade signal, causal certainty or validated fair-value estimate.']})


if __name__ == '__main__':
    payload = build_context()
    path = Path('public/research-context.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, allow_nan=False)+'\n')
    print(json.dumps({'indicators': len(payload['indicators']), 'available': sum(x['status']=='available' for x in payload['indicators']),
                      'stale': sum(x['status']=='stale' for x in payload['indicators']), 'communications': len(payload['communications']),
                      'events': len(payload['events']), 'calendar_status': payload['calendar_status']}))
