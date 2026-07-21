# USD/JPY Research Lab

An explainable swing-research model and Streamlit dashboard for USD/JPY. It combines technical structure, the US–Japan 10-year yield differential, volatility/risk sentiment, and a manual Fed–BoJ policy overlay. It also includes a cost-aware, one-day-lagged historical simulation.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The dashboard downloads USD/JPY and VIX observations through `yfinance`, plus the FRED series `DGS10` and `IRLTLT01JPM156N`. Internet access is required.

## Model outputs

- Composite score from -100 to +100
- Bullish, neutral, and bearish scenario interpretation
- Full contribution audit for every signal
- Price, moving averages, yields, volatility, and recent observations
- Configurable entry threshold, transaction-cost assumption, and policy overlay
- Backtest with CAGR, volatility, Sharpe ratio, maximum drawdown, hit rate, and equity curve

## Research caveats

The scenario percentages are transformations of the score and are not statistically calibrated probabilities. The simulation is not a brokerage-grade backtest: it excludes financing, taxes, broker spreads, execution slippage, and intraday gaps. Public data may be delayed, revised, missing, or aligned to different market closes. Validate the source observations before using the output.

This software is for research and education, not individualized financial advice or an offer to trade.
