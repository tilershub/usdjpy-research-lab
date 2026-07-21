# TRADE90 FX Research Terminal

An explainable, light-theme swing-research terminal for the seven liquid FX majors: EUR/USD, GBP/USD, USD/JPY, USD/CHF, USD/CAD, AUD/USD and NZD/USD.

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

## Research caveats

This is an end-of-day public-data research product, not a real-time institutional feed. Empirical frequencies are not guarantees. The simulation excludes financing, taxes, broker spreads, execution slippage, and intraday gaps. Public data may be delayed, revised, missing, or aligned to different market closes. Validate source observations before using the output.

This software is for research and education, not individualized financial advice or an offer to trade.
