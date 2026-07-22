from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

from model import (
    PAIR_CONFIGS, ModelConfig, backtest, calibrated_probabilities, confidence_grade,
    benchmark_comparison, data_quality, expanding_probability_validation, fred_series, horizon_validation, prepare_features, regime, score_features, walk_forward_metrics,
)

st.set_page_config(page_title="TRADE90 Research Terminal", page_icon="📈", layout="wide")
st.markdown("""
<style>
:root {--green:#047857;--ink:#0f172a;--muted:#475569;--line:#cbd5e1;--soft:#f8fafc}
[data-testid="stAppViewContainer"],.stApp{background:#fff;color:var(--ink)}
[data-testid="stHeader"]{background:rgba(255,255,255,.97)}
[data-testid="stSidebar"]{background:var(--soft);border-right:1px solid var(--line)}
[data-testid="stSidebar"] *{color:var(--ink)!important}
.block-container{padding-top:2rem;max-width:1500px}
.brand{color:var(--green);font-size:.72rem;font-weight:900;letter-spacing:.25em;text-transform:uppercase}
.title{color:var(--ink);font-size:clamp(2rem,5vw,3.5rem);font-weight:900;letter-spacing:-.045em;line-height:1.02;margin:.45rem 0}.title span{color:var(--green)}
.subtitle{color:var(--muted);margin-bottom:1.4rem}
div[data-testid="stMetric"]{background:#fff;border:1px solid var(--line);border-radius:.8rem;padding:.9rem;box-shadow:0 5px 18px rgba(15,23,42,.05)}
div[data-testid="stMetric"] *{color:var(--ink)!important;opacity:1!important}
div[data-testid="stMetricDelta"] *{color:var(--green)!important}
[data-testid="stMarkdownContainer"],[data-testid="stCaptionContainer"],[data-testid="stTabs"] button{color:var(--ink)!important}
[data-testid="stDataFrame"],[data-testid="stPlotlyChart"]{background:#fff;border-radius:.7rem}
.quality{padding:.75rem 1rem;border:1px solid #a7f3d0;background:#ecfdf5;border-radius:.7rem;color:#064e3b;margin:.5rem 0 1rem}
@media(max-width:640px){.block-container{padding:1.3rem .8rem}.title{font-size:2rem}}
</style>
<div class="brand">TRADE90 · FX intelligence</div>
<div class="title">Research <span>Terminal</span></div>
<div class="subtitle">Major-pair scanner · macro and cross-asset context · calibrated swing scenarios</div>
""", unsafe_allow_html=True)


@st.cache_data(ttl=1800, show_spinner=False)
def load_prices(start: date, end: date):
    tickers = sorted({p.ticker for p in PAIR_CONFIGS.values()} | {p.driver for p in PAIR_CONFIGS.values()})
    raw = yf.download(tickers, start=start, end=end + timedelta(days=1), auto_adjust=True, progress=False, threads=True)
    if raw.empty:
        raise RuntimeError("The market-data provider returned no observations.")
    return raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw


@st.cache_data(ttl=21600, show_spinner=False)
def load_yield(series_id: str):
    return fred_series(series_id)


def analyse(symbol: str, close: pd.DataFrame, config: ModelConfig, policy: float = 0.0):
    pair = PAIR_CONFIGS[symbol]
    price = close[pair.ticker].dropna().rename(symbol)
    driver = close[pair.driver].dropna() if pair.driver in close else None
    features = prepare_features(price, load_yield(pair.base_yield), load_yield(pair.quote_yield), driver, pair.driver_sign, config)
    scored, components = score_features(features, policy)
    scored = scored.loc[scored.index >= pd.Timestamp(end - timedelta(days=int(years * 365.25)))]
    latest = scored.dropna(subset=["score"]).iloc[-1]
    probs, sample = calibrated_probabilities(scored, float(latest.score))
    quality = data_quality(scored)
    return pair, scored, components.reindex(scored.index), latest, probs, sample, quality


with st.sidebar:
    st.header("Terminal controls")
    st.caption("Deployment: data-layer v2 · 2026-07-22")
    selected = st.selectbox("Currency pair", list(PAIR_CONFIGS), index=2)
    years = st.slider("Research history (years)", 3, 15, 7)
    threshold = st.slider("Signal threshold", 8, 40, 18)
    cost_bps = st.slider("Round-trip cost (bps)", 0.0, 12.0, 2.0, .5)
    policy = st.slider("Pair policy overlay", -1.0, 1.0, 0.0, .1, help="Relative central-bank view: negative favors the quote currency; positive favors the base currency.")
    st.divider()
    st.warning("Research and education only. Public feeds can be delayed or revised; verify prices with your broker.")

end = date.today()
start = end - timedelta(days=int(years * 365.25 + 450))
config = ModelConfig(entry_threshold=float(threshold), round_trip_cost_bps=float(cost_bps))

try:
    with st.spinner("Building the major-pair terminal…"):
        close = load_prices(start, end)
        results = {symbol: analyse(symbol, close, config, policy if symbol == selected else 0.0) for symbol in PAIR_CONFIGS}
except Exception as exc:
    st.error(f"Terminal data could not be loaded: {exc}")
    st.info("Retry shortly. If the warning persists, a public market or macro source may be unavailable.")
    st.stop()

pair, scored, components, latest, probs, sample, quality = results[selected]
confidence = confidence_grade(probs, sample, str(quality["grade"]))
direction = "Bullish" if latest.score > threshold else "Bearish" if latest.score < -threshold else "Neutral / wait"

scanner_rows = []
for symbol, (p, s, _, row, probability, n, q) in results.items():
    dominant = max(probability, key=probability.get)
    scanner_rows.append({
        "Pair": symbol, "Price": round(float(row.close), p.decimals), "Bias": dominant,
        "Score": round(float(row.score), 1), "Confidence": confidence_grade(probability, n, str(q["grade"])),
        "Regime": regime(row), "Volatility": float(row.volatility), "Data": q["grade"],
    })
scanner = pd.DataFrame(scanner_rows)
scanner["Conviction"] = scanner["Score"].abs()
scanner = scanner.sort_values(["Conviction", "Data"], ascending=[False, True]).drop(columns="Conviction")

st.subheader("Major-pair scanner")
st.dataframe(scanner.style.format({"Volatility": "{:.1%}", "Score": "{:+.1f}"}), use_container_width=True, hide_index=True)
st.caption("Ranking reflects evidence strength, not expected profit. Compare spreads, event risk and your trading horizon before selecting a pair.")

st.divider()
st.subheader(f"{selected} intelligence")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric(selected, f"{latest.close:.{pair.decimals}f}")
c2.metric("Composite score", f"{latest.score:+.1f}", direction)
c3.metric(f"{pair.base}–{pair.quote} 10Y spread", f"{latest.yield_spread:+.2f} pp" if pd.notna(latest.yield_spread) else "N/A")
c4.metric("20D volatility", f"{latest.volatility:.1%}")
c5.metric("Research confidence", confidence, f"Data {quality['grade']}")
st.markdown(f"<div class='quality'><b>Data check:</b> last market observation {quality['last_price']:%Y-%m-%d} · age {quality['price_age_days']} day(s) · usable inputs {quality['completeness']:.0%} · cross-asset driver: {pair.driver_label}</div>", unsafe_allow_html=True)
source_rows = [
    {"Input": f"{selected} close", "Provider": "Yahoo Finance", "Cadence": "End of day", "Age": f"{quality['price_age_days']}d", "Status": "Current" if quality['price_age_days'] <= 4 else "Stale"},
    {"Input": f"{pair.base} 10Y yield", "Provider": "FRED / OECD", "Cadence": "Daily or monthly", "Age": f"{quality['base_yield_age_days']}d" if quality['base_yield_age_days'] is not None else "Missing", "Status": "Usable" if quality['base_yield_age_days'] is not None and quality['base_yield_age_days'] <= 45 else "Excluded"},
    {"Input": f"{pair.quote} 10Y yield", "Provider": "FRED / OECD", "Cadence": "Daily or monthly", "Age": f"{quality['quote_yield_age_days']}d" if quality['quote_yield_age_days'] is not None else "Missing", "Status": "Usable" if quality['quote_yield_age_days'] is not None and quality['quote_yield_age_days'] <= 45 else "Excluded"},
    {"Input": pair.driver_label, "Provider": "Yahoo Finance", "Cadence": "End of day", "Age": f"{quality['driver_age_days']}d" if quality['driver_age_days'] is not None else "Missing", "Status": "Current" if quality['driver_age_days'] is not None and quality['driver_age_days'] <= 7 else "Excluded"},
]
with st.expander("Data sources, delay and freshness", expanded=quality["grade"] == "C"):
    st.dataframe(pd.DataFrame(source_rows), use_container_width=True, hide_index=True)
    if quality["stale_inputs"]:
        st.warning("Excluded from the current score: " + ", ".join(quality["stale_inputs"]) + ".")
    st.caption("Inputs use their latest published observation. Monthly yield series are valid for macro context but cannot be interpreted as live rates.")

tabs = st.tabs(["Market", "Scenarios", "Signal audit", "Validation", "Methodology"])
with tabs[0]:
    left, right = st.columns([2, 1])
    with left:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=scored.index, y=scored.close, name=selected, line=dict(color="#047857", width=2)))
        fig.add_trace(go.Scatter(x=scored.index, y=scored.ema_fast, name="EMA 20", line=dict(color="#2563eb", width=1)))
        fig.add_trace(go.Scatter(x=scored.index, y=scored.ema_slow, name="EMA 50", line=dict(color="#7c3aed", width=1)))
        fig.update_layout(title="Price structure", height=410, margin=dict(l=10,r=10,t=45,b=10), hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.markdown("#### Current map")
        st.metric("Market regime", regime(latest))
        st.metric("20-day support", f"{latest.support20:.{pair.decimals}f}")
        st.metric("20-day resistance", f"{latest.resistance20:.{pair.decimals}f}")
        st.metric("ATR-style daily range", f"{latest.atr20:.{pair.decimals}f}")
    score_fig = go.Figure(go.Scatter(x=scored.index, y=scored.score, fill="tozeroy", line=dict(color="#047857"), name="Score"))
    score_fig.add_hline(y=threshold, line_dash="dash", line_color="#16a34a"); score_fig.add_hline(y=-threshold, line_dash="dash", line_color="#dc2626")
    score_fig.update_layout(title="Composite evidence score", yaxis_range=[-100,100], height=290, margin=dict(l=10,r=10,t=45,b=10))
    st.plotly_chart(score_fig, use_container_width=True)

with tabs[1]:
    st.markdown(f"#### Empirical {config.forward_days}-trading-day scenarios")
    cols = st.columns(3)
    for col, label in zip(cols, ("Bullish", "Range/neutral", "Bearish")):
        col.metric(label, f"{probs[label]:.0%}")
        col.progress(int(probs[label] * 100))
    st.info(f"Calibration uses {sample} historically similar score observations. Confidence: {confidence}. These are empirical research frequencies, not guaranteed forecasts.")

with tabs[2]:
    audit = components.loc[latest.name].sort_values(key=abs, ascending=False).rename("Contribution").to_frame()
    audit["Interpretation"] = np.where(audit.Contribution > 0, f"{pair.base} supportive", np.where(audit.Contribution < 0, f"{pair.quote} supportive", "Neutral"))
    st.dataframe(audit.style.format({"Contribution":"{:+.2f}"}), use_container_width=True)
    st.caption("Every component is bounded. Positive contributions favor a higher pair; negative contributions favor a lower pair.")

with tabs[3]:
    bt, metrics = backtest(scored, config)
    horizons = horizon_validation(scored, config)
    calibration, reliability = expanding_probability_validation(scored)
    benchmarks = benchmark_comparison(scored, config)
    st.markdown("#### Out-of-sample forecast evidence")
    a,b,c,d = st.columns(4)
    five_day = horizons.loc["5D"]
    a.metric("5D OOS accuracy", f"{five_day['Model accuracy']:.1%}" if pd.notna(five_day["Model accuracy"]) else "N/A")
    b.metric("5D lift vs baseline", f"{five_day['Lift vs baseline']:+.1%}" if pd.notna(five_day["Lift vs baseline"]) else "N/A")
    c.metric("Calibration error", f"{calibration['Calibration error']:.1%}" if pd.notna(calibration["Calibration error"]) else "N/A")
    d.metric("OOS probability tests", f"{int(calibration['Forecasts'])}")
    st.dataframe(horizons.style.format({"Model accuracy":"{:.1%}","MA accuracy":"{:.1%}","Majority baseline":"{:.1%}","Lift vs baseline":"{:+.1%}"}), use_container_width=True)
    st.caption("The first 504 observations are reserved for training. Each forecast is evaluated only against later prices; probability tests use prior observations only.")

    st.markdown("#### Benchmark comparison")
    st.dataframe(benchmarks.style.format({"Total return":"{:.1%}","CAGR":"{:.1%}","Sharpe":"{:.2f}","Maximum drawdown":"{:.1%}","Hit rate":"{:.1%}","Profit factor":"{:.2f}"}), use_container_width=True)
    st.caption("All strategies use one-day-lagged positions and the same transaction-cost assumption. The random benchmark is deterministic for reproducibility.")

    if not reliability.empty:
        st.markdown("#### Probability reliability")
        chart_data = reliability.reset_index(drop=True)
        rel = go.Figure()
        rel.add_trace(go.Scatter(x=chart_data.Mean_confidence, y=chart_data.Observed_accuracy, mode="lines+markers", name="Observed"))
        rel.add_trace(go.Scatter(x=[.33,1], y=[.33,1], mode="lines", line=dict(dash="dash",color="#64748b"), name="Perfect calibration"))
        rel.update_layout(xaxis_title="Forecast confidence", yaxis_title="Observed accuracy", height=320, margin=dict(l=10,r=10,t=25,b=10))
        st.plotly_chart(rel, use_container_width=True)

    st.markdown("#### Historical simulation")
    eq = go.Figure()
    eq.add_trace(go.Scatter(x=bt.index,y=bt.strategy_equity,name="TRADE90 simulation",line=dict(color="#047857",width=2)))
    eq.add_trace(go.Scatter(x=bt.index,y=bt.buy_hold_equity,name=f"Hold {selected}",line=dict(color="#64748b",width=1)))
    eq.update_layout(title="Lagged, cost-aware simulation",height=400,margin=dict(l=10,r=10,t=45,b=10))
    st.plotly_chart(eq,use_container_width=True)
    st.warning("A positive backtest is not proof of future profitability. Financing, slippage, broker spreads and event gaps remain excluded.")

with tabs[4]:
    st.markdown(f"""
### How TRADE90 evaluates {selected}

The terminal combines trend, momentum, RSI, the **{pair.base}–{pair.quote} 10-year yield differential**, its recent impulse, and **{pair.driver_label}**. A manual policy overlay is kept separate so judgment never masquerades as observed data.

### Accuracy safeguards

- Signals are lagged before historical returns are calculated.
- Scenario percentages are calibrated from historically similar observations.
- Walk-forward validation uses only prior data to set its adaptive threshold.
- Data age and completeness directly limit the confidence label.
- Stale yields and cross-asset observations are automatically excluded from the score.
- Provider, cadence, age and inclusion status are visible above the analysis tabs.
- The audit exposes every contribution instead of hiding the result in a black box.

### Current limitations

This public-data edition is end-of-day research, not a real-time dealing terminal. It does not yet include licensed tick data, options surfaces, CFTC positioning, consensus-surprise data, live news, economic-calendar scoring or broker execution. FRED and Yahoo observations may be delayed, revised or aligned to different closes.
""")
