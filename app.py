from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

from model import ModelConfig, backtest, fred_series, prepare_features, scenario_probabilities, score_features


st.set_page_config(page_title="TRADE90 · USD/JPY Research", page_icon="90", layout="wide")
st.markdown("""
<style>
  :root { --trade90: #34d399; }
  [data-testid="stAppViewContainer"] { background: #0f172a; }
  [data-testid="stSidebar"] { background: #0b1220; border-right: 1px solid #1e293b; }
  .trade90-brand { color: var(--trade90); font-size: .72rem; font-weight: 900; letter-spacing: .28em; text-transform: uppercase; }
  .trade90-title { color: white; font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 900; letter-spacing: -.045em; line-height: 1; margin: .5rem 0 .8rem; text-transform: uppercase; }
  .trade90-title span { color: var(--trade90); }
  .trade90-subtitle { color: #94a3b8; margin-bottom: 1.5rem; }
  div[data-testid="stMetric"] { background: rgba(15,23,42,.7); border: 1px solid #1e293b; border-radius: 1rem; padding: 1rem; }
</style>
<div class="trade90-brand">TRADE90 · Market Research</div>
<div class="trade90-title">USD/JPY <span>Research Lab</span></div>
<div class="trade90-subtitle">Swing-horizon decision support · explainable signals · no trade execution</div>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600, show_spinner=False)
def load_market_data(start: date, end: date):
    raw = yf.download(["JPY=X", "^VIX"], start=start, end=end + timedelta(days=1), auto_adjust=True, progress=False)
    if raw.empty:
        raise RuntimeError("The market-data provider returned no observations.")
    close = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw
    fx = close["JPY=X"].dropna().rename("USDJPY")
    vix = close["^VIX"].dropna().rename("VIX") if "^VIX" in close else None
    us10y = fred_series("DGS10")
    jp10y = fred_series("IRLTLT01JPM156N")
    return fx, vix, us10y, jp10y


with st.sidebar:
    st.header("Research controls")
    years = st.slider("History (years)", 2, 15, 7)
    threshold = st.slider("Signal threshold", 5, 40, 18)
    cost_bps = st.slider("Round-trip cost (bps)", 0.0, 10.0, 2.0, 0.5)
    policy = st.slider("Manual policy overlay", -1.0, 1.0, 0.0, 0.1, help="Negative = relatively hawkish BoJ / dovish Fed; positive = relatively hawkish Fed / dovish BoJ.")
    st.divider()
    st.warning("Research tool only. Validate data and assumptions before making financial decisions.")

end = date.today()
start = end - timedelta(days=int(years * 365.25 + 400))
config = ModelConfig(entry_threshold=float(threshold), round_trip_cost_bps=float(cost_bps))

try:
    with st.spinner("Loading market and macro data…"):
        fx, vix, us10y, jp10y = load_market_data(start, end)
except Exception as exc:
    st.error(f"Live data could not be loaded: {exc}")
    st.info("Check your internet connection and data-provider availability, then retry.")
    st.stop()

features = prepare_features(fx, us10y, jp10y, vix, config)
scored, components = score_features(features, policy)
scored = scored.loc[scored.index >= pd.Timestamp(end - timedelta(days=int(years * 365.25)))]
components = components.reindex(scored.index)
latest = scored.dropna(subset=["score"]).iloc[-1]
latest_components = components.loc[latest.name].sort_values(key=abs, ascending=False)
probs = scenario_probabilities(float(latest["score"]))
bt, metrics = backtest(scored, config)

direction = "Bullish USD/JPY" if latest.score > threshold else "Bearish USD/JPY" if latest.score < -threshold else "Neutral / wait"
c1, c2, c3, c4 = st.columns(4)
c1.metric("USD/JPY", f"{latest.close:.3f}")
c2.metric("Composite score", f"{latest.score:+.1f}", direction)
c3.metric("US–Japan 10Y spread", f"{latest.yield_spread:.2f} pp" if pd.notna(latest.yield_spread) else "N/A")
c4.metric("20D annualized volatility", f"{latest.volatility:.1%}")

tabs = st.tabs(["Research view", "Signal audit", "Backtest", "Methodology"])
with tabs[0]:
    left, right = st.columns([2, 1])
    with left:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=scored.index, y=scored.close, name="USD/JPY", line=dict(color="#d8a635", width=2)))
        fig.add_trace(go.Scatter(x=scored.index, y=scored.ema_fast, name="EMA 20", line=dict(color="#59a5d8", width=1)))
        fig.add_trace(go.Scatter(x=scored.index, y=scored.ema_slow, name="EMA 50", line=dict(color="#9b7ede", width=1)))
        fig.update_layout(title="Price structure", height=430, margin=dict(l=10, r=10, t=45, b=10), hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.subheader("Scenario probabilities")
        for label, probability in probs.items():
            st.write(f"{label}: **{probability:.0%}**")
            st.progress(int(probability * 100))
        st.caption("Probabilities are a normalized interpretation of the score—not calibrated forecasts of future returns.")
    score_fig = go.Figure(go.Scatter(x=scored.index, y=scored.score, fill="tozeroy", line=dict(color="#d8a635"), name="Score"))
    score_fig.add_hline(y=threshold, line_dash="dash", line_color="#35a66f")
    score_fig.add_hline(y=-threshold, line_dash="dash", line_color="#d95c5c")
    score_fig.update_layout(title="Composite research score", yaxis_range=[-100, 100], height=310, margin=dict(l=10, r=10, t=45, b=10))
    st.plotly_chart(score_fig, use_container_width=True)

with tabs[1]:
    audit = pd.DataFrame({"Contribution": latest_components})
    audit["Direction"] = np.where(audit.Contribution > 0, "USD bullish", np.where(audit.Contribution < 0, "JPY bullish", "Neutral"))
    audit["Contribution"] = audit["Contribution"].map(lambda x: f"{x:+.2f}")
    st.dataframe(audit, use_container_width=True)
    st.caption(f"Observation date: {latest.name:%Y-%m-%d}. Positive scores favor a higher USD/JPY; negative scores favor a lower USD/JPY.")
    detail = scored[["close", "rsi", "momentum", "yield_spread", "spread_change", "vix", "score"]].tail(30).sort_index(ascending=False)
    st.dataframe(detail.style.format({"close": "{:.3f}", "rsi": "{:.1f}", "momentum": "{:.2%}", "yield_spread": "{:.2f}", "spread_change": "{:+.2f}", "vix": "{:.1f}", "score": "{:+.1f}"}), use_container_width=True)

with tabs[2]:
    a, b, c, d = st.columns(4)
    a.metric("CAGR", f"{metrics['CAGR']:.1%}")
    b.metric("Sharpe", f"{metrics['Sharpe (0% rf)']:.2f}")
    c.metric("Max drawdown", f"{metrics['Maximum drawdown']:.1%}")
    d.metric("Active-day hit rate", f"{metrics['Active-day hit rate']:.1%}")
    eq = go.Figure()
    eq.add_trace(go.Scatter(x=bt.index, y=bt.strategy_equity, name="Research strategy", line=dict(color="#d8a635", width=2)))
    eq.add_trace(go.Scatter(x=bt.index, y=bt.buy_hold_equity, name="Buy & hold USD/JPY", line=dict(color="#77818b", width=1)))
    eq.update_layout(title="Historical simulation (growth of 1.00)", height=420, margin=dict(l=10, r=10, t=45, b=10), hovermode="x unified")
    st.plotly_chart(eq, use_container_width=True)
    st.caption("Signals are delayed by one trading day. Costs apply when positions change. Results exclude financing, slippage, taxes, and broker-specific spreads; they are not evidence of future performance.")

with tabs[3]:
    st.markdown("""
### What the score means

The model combines price trend, 20-day momentum, RSI, the US–Japan 10-year government-yield differential, recent yield-spread change, VIX movement, and a manual central-bank-policy overlay. Contributions are bounded to reduce the influence of extreme observations.

### Interpretation

- **Above the positive threshold:** evidence favors USD strength / JPY weakness.
- **Between thresholds:** evidence is mixed; the model stays flat in the simulation.
- **Below the negative threshold:** evidence favors JPY strength / USD weakness.

### Important limitations

This is an explainable research heuristic, not a trained prediction engine. It does not yet include options-implied volatility, CFTC positioning, surprise indices, intraday market microstructure, intervention detection, or a live economic calendar. Yahoo Finance supplies market prices; FRED supplies government-yield series. Revisions, stale observations, differing market closes, and outages can affect results.
""")
