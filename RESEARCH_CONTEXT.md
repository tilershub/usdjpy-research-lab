# Market research context

The terminal is moving from directional scoring to sourced market conditions.
This delivery is a working foundation, not a claim that every proposed commercial
service is connected or that research produces a particular trade win rate.

## Implemented

- Separate `research_context.py` publisher; a Yahoo price failure cannot prevent
  its macro, CFTC, calendar and official-communications refresh.
- 20 FRED indicators plus two direct Statistics Bureau of Japan indicators.
  The latter use narrowly validated official latest-indicator cards; missing,
  ambiguous or changed definitions fail closed. They do not supply historical
  changes or release timestamps.
- US/Japan GDP changes use quarter-on-quarter, not annualized, growth.
- CPI/M2 growth uses matching monthly periods, never shifted rows across gaps.
- US/Japan 10-year spread uses completed common monthly periods and rejects
  sparse US months. It is not a live spread or current policy-rate differential.
- Source URLs, publishers, units, observation periods, retrieval timestamps,
  freshness limits and revision limitations accompany macro values.
- Fed, BOJ and ECB official headline feeds. Headlines link to source documents;
  they are not automatic policy-stance summaries.
- Existing Atlanta Fed reference-window expectations; explicitly not next-meeting odds.
- CFTC speculative/intermediary net positions, report-to-report change, open
  interest, change in open interest and sample count. Markets remain separate.
- Calendar actual/consensus/previous/revised fields with official source links
  where provided. Zero is retained as a value. No claim of archived pre-release
  consensus or valid surprise backtests.
- Optional server-side Myfxbook session adapter with percentage validation.
  Retail provider samples are not combined and no contrarian signal is generated.
- Official policy/fiscal/trade/intervention reference library, with explicit
  distinction between reference links and analysed documents.

## Access and operation

Run `python research_context.py`. The scheduled GitHub workflow publishes
`public/research-context.json` hourly, independently from price research.

`TRADING_ECONOMICS_KEY`: provider-issued credential, optional; absent access is
reported as unavailable/guest according to actual response.
`MYFXBOOK_SESSION`: provider-issued session, optional. No passwords stored.
`MYFXBOOK_DISPLAY_ALLOWED=true`: set only when website-display permission has
been established. The workflow reads this from a repository variable and reads
credentials from GitHub Secrets. No credentials should be placed in JSON or code.

No subscriptions were purchased or credentials created by this change.
Public/API access does not itself establish redistribution rights; source-specific
conditions remain applicable. Official document links do not imply a licensed
news wire, bank-research feed or universal market-data licence.

## Remaining scope

- Japan's current BOJ target, bond purchase amounts, monetary aggregates and
  additional economic history; a monthly overnight market rate is labelled as
  such and never used as its policy-target substitute.
- Structured fiscal/trade policy analysis, intervention confirmation and
  corroborated geopolitical event classification. Reference links are provided,
  but these analyses are not claimed as complete.
- Licensed intraday yields/options/order flow, robust consistent spot-gold
  history, crypto exchange funding/liquidations, bank forecasts and additional
  retail-provider agreements. UI shows source coverage gaps explicitly.
- Full country templates beyond US/Japan; other instruments receive US/global
  context with a visible coverage notice.
- Release-time vintages, pre-release consensus archive, source-reconciled AI
  explanations and independently validated valuation ranges.

## Validation

Regression tests cover missing periods, stale/future/nonfinite values, common-month
spread alignment, nonannualized growth, zero calendar values, revision metadata,
RSS/RDF headlines, retail percentage validation and strict Japanese card parsing.
Fixtures verify implementation behavior, not forecasting profitability.

The first live retrieval returned 14 available / 3 stale / 5 unavailable FRED
indicators and 24 official headlines; CFTC and Atlanta Fed returned data and the
calendar was unavailable. Direct Japanese official-card retrieval was subsequently
validated. Each published run reports its own availability, which can change.

Latest integrated retrieval: 22 indicators, 20 available and 2 stale; 24 official
headlines; CFTC and Atlanta Fed available; economic calendar unavailable.
57 Python tests passed (one environment warning).
