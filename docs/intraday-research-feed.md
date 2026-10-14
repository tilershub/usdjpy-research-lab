# TRADE90 intraday research data feed (15-minute / 1-hour)

## What is implemented

- Backend adapter: `terminal/intraday.py` uses Twelve Data `/time_series`, requesting **100 UTC OHLC bars**, restricted to nine allowlisted markets and to `15min` or `1h`.
- Strict validation: check symbol/timeframe metadata, finite positive OHLC, chronology, duplicate timestamps, finished bars only, minimum 55 clean bars, and price age. A forming bar is never included in indicators.
- Calculated per source, never blended with daily snapshots: EMA20/50, RSI14 (Wilder smoothing), ATR14, prior-20-bar range excluding the current completed bar, 16-bar price change, and descriptive market-structure classification.
- Output provenance: published source, quote basis, last completed bar close time, age, number of validated candles; market gaps or weekends marked **stale** after 3 bar intervals.
- Cache: Django per-symbol/per-timeframe cache for 600 seconds; failed requests cached for 75 seconds, with a short lock against duplicate concurrent provider calls. Single-instance local cache only; use shared Redis for larger scale.
- Public route: `/market-intelligence/intraday.json?symbol=EUR%2FUSD&interval=15min`. The market intelligence page attempts to show data when enabled; otherwise reports that a licensed source is required.

**This is not connected to real data yet** unless the verified licensing contract and credentials have been supplied. No fallback to historical snapshot prices; the TradingView widget display remains separate.

## Commercial licensing: required BEFORE enabling production

The TRADE90 site is public, not a personal trading terminal. Twelve Data's **individual plans do not allow public commercial display**; its business plans have different display rights, and third-party redistribution may require a separate written agreement. Confirm that your contract specifically permits all of the following:

1. Retrieving Gold XAU/USD, seven spot-Forex pairs, and BTC/USD intraday OHLC through the chosen plan with adequate symbol-specific coverage and call quotas.
2. **Publicly showing derived statistics**, levels, trends and research summaries to visitors, and any intended retention of derived research/candles. TradingView widgets do **not** grant rights to harvest or calculate from widget quotes.
3. Any required attribution and market-specific licenses. Display a visible Twelve Data attribution link where licensed data is shown.

Relevant official policies:
- https://support.twelvedata.com/en/articles/5332349-commercial-and-personal-usage
- https://twelvedata.com/terms
- https://support.twelvedata.com/en/articles/12647398-attribution-guidelines-for-using-twelve-data

## Activation procedure

Until commercial terms are accepted, leave the feed safely off. After obtaining licensing approval and a provider key, in Render's secure service environment configure:

- `TWELVEDATA_API_KEY` = secret API key (never commit or paste into a public repo).
- `TRADE90_INTRADAY_PUBLIC_LICENSED` = `true` **only** after rights are confirmed.

Deploy/restart the service, then test the JSON endpoint and both selected timeframes. A 503 with `not_configured` is intentional when disabled. A 503 with `unavailable` means the provider has insufficient, invalid, or unavailable candles. A `stale` response contains historical indicator values but must not be described as current. Never silently switch Gold futures to spot or vice versa.

If terms require a different provider, keep the tested, provider-agnostic indicator engine and implement a licensed OHLC adapter that produces the same normalized candle list.

## SLO and known limitations

- Read-through request/caching, not guaranteed background ingestion. No paid Render cron service has been added.
- A 10-minute cache helps control call volume, but is **not** sub-minute research. At high traffic/multi-instance scale, move to provider-licensed scheduled ingestion, persistent history, a shared cache, monitor 429s and quotas.
- This phase does not cover order execution, intraday economic events, broker spreads or correlation forecasts. Indicators are descriptive research, not proven signals.
- An intermittent provider or closed FX session results in stale/unavailable status; it must never be interpreted as "no market risk".
- Test indicators and coverage against known independent reference series for each instrument before considering paid-user claims.
