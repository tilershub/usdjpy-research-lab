# TRADE90 FX Research Terminal

An explainable, light-theme swing-research terminal for seven liquid FX majors, XAU/USD and BTC/USD. The published snapshot now includes native charts, event risk, positioning context, contribution audit and validation data for the TRADE90 website.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The dashboard downloads end-of-day market observations through `yfinance` and government-yield observations through FRED. Internet access is required.

## Model outputs

- Major-pair scanner ranked by evidence strength
- Pair-specific rate differentials and cross-asset drivers
- Composite score from -100 to +100
- Empirically calibrated five-day bullish, neutral, and bearish scenarios
- Data-quality grade, observation age, sample size and confidence label
- Regime, volatility, ATR-style range, support and resistance
- Full contribution audit for every signal
- Price, moving averages, yields and volatility
- Configurable entry threshold, transaction-cost assumption, and policy overlay
- Lagged, cost-aware backtest plus expanding walk-forward validation
- Market-implied Fed policy path: cut, hold and hike probabilities per quarterly window
- CFTC Commitments of Traders positioning, including gold from the Disaggregated report
- Official central-bank press releases mapped to the currencies each pair trades
- High-impact economic calendar with pair relevance and UTC countdowns
- Previous, consensus and actual values with post-release surprise calculation
- Event-risk warnings and historical absolute-reaction estimates

## Research caveats

Prices are end-of-day. XAU/USD is quoted spot, on the same basis as a spot gold CFD. If the spot feed is unavailable or too sparse to carry the model, the publisher falls back to COMEX front-month futures and relabels the market accordingly — futures carry a premium to spot that widens with rates and time to delivery, so a fallback quote will not match a broker. BTC/USD is a Yahoo composite. Every market declares the basis it was actually priced on, so a fallback is never presented as spot.

Fundamental data comes from official primary sources with no licence restriction: the Atlanta Fed Market Probability Tracker for rate probabilities, the CFTC public reporting API for positioning, and central-bank RSS for policy communications. Rate probabilities are market pricing, not forecasts. Newswire text from Bloomberg and Reuters is deliberately absent because their terms do not permit redistribution here.

This is an end-of-day public-data research product, not a real-time institutional feed. Empirical frequencies are not guarantees. The simulation excludes financing, taxes, broker spreads, execution slippage, and intraday gaps. Public data may be delayed, revised, missing, or aligned to different market closes. Calendar coverage uses Trading Economics guest access by default; set `TRADING_ECONOMICS_KEY` for licensed coverage. Upcoming events affect risk warnings, never the directional score. Validate source observations before using the output.

This software is for research and education, not individualized financial advice or an offer to trade.
