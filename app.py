from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

from trade90_model import (
    PAIR_CONFIGS, ModelConfig, backtest, calibrated_probabilities, confidence_grade, pair_model_profile,
    benchmark_comparison, data_quality, expanding_probability_validation, fred_series, horizon_validation, prepare_features, regime, score_features, walk_forward_metrics,
)
from economic_events import event_risk_summary, events_for_pair, fetch_calendar, historical_event_reaction
from positioning import derivatives_availability, fetch_cftc, pair_positioning

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

@st.cache_data(ttl=1800, show_spinner=False)
def load_calendar(start_day: date, end_day: date):
    return fetch_calendar(start_day, end_day)

@st.cache_data(ttl=21600, show_spinner=False)
def load_positioning():
    return fetch_cftc()


def analyse(symbol: str, close: pd.DataFrame, config: ModelConfig, policy: float = 0.0):
    pair = PAIR_CONFIGS[symbol]
    price = close[pair.ticker].dropna().rename(symbol)
    driver = close[pair.driver].dropna() if pair.driver in close else None
    features = prepare_features(price, load_yield(pair.base_yield), load_yield(pair.quote_yield), driver, pair.driver_sign, config)
    scored, components = score_features(features, policy, symbol)
    scored = scored.loc[scored.index >= pd.Timestamp(end - timedelta(days=int(years * 365.25)))]
    latest = scored.dropna(subset=["score"]).iloc[-1]
    probs, sample = calibrated_probabilities(scored, float(latest.score))
    quality = data_quality(scored)
    return pair, scored, components.reindex(scored.index), latest, probs, sample, quality


with st.sidebar:
    st.header("Terminal controls")
    st.caption("Deployment: positioning v7 · 2026-07-22")
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
        calendar, calendar_status = load_calendar(end - timedelta(days=35), end + timedelta(days=14))
        cftc_history, cftc_status = load_positioning()
except Exception as exc:
    st.error(f"Terminal data could not be loaded: {exc}")
    st.info("Retry shortly. If the warning persists, a public market or macro source may be unavailable.")
    st.stop()

pair, scored, components, latest, probs, sample, quality = results[selected]
pair_events = events_for_pair(calendar, pair.base, pair.quote)
event_risk = event_risk_summary(pair_events)
positioning = pair_positioning(cftc_history, pair.base, pair.quote)
confidence = confidence_grade(probs, sample, str(quality["grade"]))
direction = "Bullish interpretation" if latest.score > threshold else "Bearish interpretation" if latest.score < -threshold else "Neutral interpretation"
profile = pair_model_profile(selected)
dominant_scenario = max(probs, key=probs.get)

scanner_rows = []
for symbol, (p, s, _, row, probability, n, q) in results.items():
    dominant = max(probability, key=probability.get)
    scanner_rows.append({
        "Pair": symbol, "Price": round(float(row.close), p.decimals), "Bias": dominant,
        "Score": round(float(row.score), 1), "Confidence": confidence_grade(probability, n, str(q["grade"])),
        "Regime": regime(row), "Volatility": float(row.volatility), "Data": q["grade"],
        "Event risk": event_risk_summary(events_for_pair(calendar, p.base, p.quote))["level"],
    })
scanner = pd.DataFrame(scanner_rows)
scanner["Conviction"] = scanner["Score"].abs()
scanner = scanner.sort_values(["Conviction", "Data"], ascending=[False, True]).drop(columns="Conviction")

st.subheader("Major-pair scanner")
st.dataframe(scanner.style.format({"Volatility": "{:.1%}", "Score": "{:+.1f}"}), use_container_width=True, hide_index=True)
st.caption("Ranking reflects evidence strength, not expected profit. Compare spreads, event risk and your trading horizon before selecting a pair.")

st.divider()
st.subheader(f"{selected} research brief")
st.caption("The terminal keeps observed facts, model interpretation, forecast probabilities, and planning context separate.")

st.markdown("#### 1 · Market facts")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Observed close", f"{latest.close:.{pair.decimals}f}")
c2.metric(f"{pair.base}–{pair.quote} 10Y spread", f"{latest.yield_spread:+.2f} pp" if pd.notna(latest.yield_spread) else "N/A")
c3.metric("20D realised volatility", f"{latest.volatility:.1%}")
c4.metric("Market regime", regime(latest))
c5.metric("Data quality", str(quality["grade"]), f"{quality['completeness']:.0%} usable")
st.markdown(f"<div class='quality'><b>Observed-data check:</b> last FX observation {quality['last_price']:%Y-%m-%d} · age {quality['price_age_days']} day(s) · cross-asset series: {pair.driver_label}. Values above are measurements, not forecasts.</div>", unsafe_allow_html=True)

left_layer, right_layer = st.columns(2)
with left_layer:
    with st.container(border=True):
        st.markdown("#### 2 · Model interpretation")
        st.metric("Composite evidence score", f"{latest.score:+.1f}", direction)
        st.write(profile.thesis)
        st.caption(f"Pair-specific weighted interpretation · threshold ±{threshold} · manual policy overlay {policy:+.1f}. The overlay is disclosed judgment, not observed data.")
with right_layer:
    with st.container(border=True):
        st.markdown(f"#### 3 · {config.forward_days}-day probabilistic forecast")
        st.metric("Most frequent historical outcome", dominant_scenario, f"{probs[dominant_scenario]:.0%}")
        st.write(f"Bullish {probs['Bullish']:.0%} · Range/neutral {probs['Range/neutral']:.0%} · Bearish {probs['Bearish']:.0%}")
        st.caption(f"Based on {sample} similar historical observations · confidence {confidence}. Frequencies are calibrated estimates, not promises.")

with st.container(border=True):
    st.markdown("#### 4 · Trade-planning context")
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("20D support", f"{latest.support20:.{pair.decimals}f}")
    p2.metric("20D resistance", f"{latest.resistance20:.{pair.decimals}f}")
    p3.metric("ATR-style daily range", f"{latest.atr20:.{pair.decimals}f}")
    p4.metric("Scheduled-event risk", event_risk["level"])
    st.caption("Reference levels describe recent market structure and volatility. They are not entry, stop-loss, take-profit, position-size, or trade recommendations.")
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

tabs = st.tabs(["Market facts", "Event risk", "Positioning", "Forecast", "Interpretation", "Validation", "Methodology"])
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
        st.markdown("#### Planning reference map")
        st.metric("Market regime", regime(latest))
        st.metric("20-day support", f"{latest.support20:.{pair.decimals}f}")
        st.metric("20-day resistance", f"{latest.resistance20:.{pair.decimals}f}")
        st.metric("ATR-style daily range", f"{latest.atr20:.{pair.decimals}f}")
    score_fig = go.Figure(go.Scatter(x=scored.index, y=scored.score, fill="tozeroy", line=dict(color="#047857"), name="Score"))
    score_fig.add_hline(y=threshold, line_dash="dash", line_color="#16a34a"); score_fig.add_hline(y=-threshold, line_dash="dash", line_color="#dc2626")
    score_fig.update_layout(title="Composite evidence score", yaxis_range=[-100,100], height=290, margin=dict(l=10,r=10,t=45,b=10))
    st.plotly_chart(score_fig, use_container_width=True)

with tabs[1]:
    st.markdown(f"#### {selected} economic-event monitor")
    e1, e2, e3 = st.columns(3)
    e1.metric("Current event risk", event_risk["level"])
    e2.metric("High-impact events / 24h", event_risk["count_24h"])
    e3.metric("Next event", f"{event_risk['hours']:.1f}h" if event_risk["hours"] is not None else "None scheduled")
    if event_risk["level"] in {"Extreme", "High"}:
        st.warning(f"{event_risk['next_event']} is approaching. Spreads, slippage and gap risk can rise; the directional model does not predict the release result.")
    upcoming = pair_events[pair_events["time"] >= pd.Timestamp(datetime.now(timezone.utc))].head(12).copy()
    if upcoming.empty:
        st.info(calendar_status.message or "No upcoming supported high-impact events were returned for this pair.")
    else:
        upcoming["UTC"] = upcoming["time"].dt.strftime("%Y-%m-%d %H:%M")
        upcoming["Countdown"] = upcoming["hours"].clip(lower=0).map(lambda value: f"{value:.1f}h")
        display = upcoming[["UTC", "Countdown", "currency", "event", "side", "previous", "forecast"]].rename(columns={"currency":"CCY", "event":"Event", "side":"Pair side", "previous":"Previous", "forecast":"Consensus"})
        st.dataframe(display, use_container_width=True, hide_index=True)
    st.caption(f"Provider: {calendar_status.provider} · mode: {calendar_status.mode} · fetched {calendar_status.fetched_at:%Y-%m-%d %H:%M} UTC. Calendar figures can change; verify them with the primary release source.")
    released = pair_events[(pair_events["time"] < pd.Timestamp(datetime.now(timezone.utc))) & pair_events["actual"].ne("—")].tail(15).copy()
    st.markdown("#### Recent releases and surprises")
    if released.empty:
        st.caption("No validated actual-versus-consensus releases are available from the current provider response.")
    else:
        released["UTC"] = released["time"].dt.strftime("%Y-%m-%d %H:%M")
        released["Surprise"] = released["surprise_pct"].map(lambda value: f"{value:+.1%}" if pd.notna(value) else "—")
        st.dataframe(released[["UTC", "currency", "event", "actual", "forecast", "previous", "Surprise"]].rename(columns={"currency":"CCY", "event":"Event", "actual":"Actual", "forecast":"Consensus", "previous":"Previous"}), use_container_width=True, hide_index=True)
        selected_category = st.selectbox("Historical reaction category", released["category"].dropna().unique())
        reaction = historical_event_reaction(pair_events, scored["close"], selected_category)
        if reaction["observations"]:
            st.info(f"After {reaction['observations']} comparable releases in the available window, the median next-session absolute move was {reaction['median_move']:.2%}. This measures movement, not direction.")
        else:
            st.caption("Not enough aligned observations to estimate a historical reaction.")
    st.info("Upcoming events change the risk label only. They do not add bullish or bearish points. A surprise is calculated only after actual and consensus values are both available.")

with tabs[2]:
    st.markdown(f"#### {selected} positioning and derivatives")
    st.caption("Positioning is contextual evidence, not a live signal. CFTC data is weekly and published with a delay.")
    if positioning["available"]:
        base_pos, quote_pos = positioning["base"], positioning["quote"]
        x1, x2, x3, x4 = st.columns(4)
        x1.metric(f"{pair.base} leveraged net", f"{base_pos['leveraged_net']:,.0f}", f"{base_pos['percentile_3y']:.0%} percentile")
        x2.metric(f"{pair.quote} leveraged net", f"{quote_pos['leveraged_net']:,.0f}", f"{quote_pos['percentile_3y']:.0%} percentile")
        x3.metric("Relative crowding", f"{positioning['relative_percentile']:+.0%}")
        x4.metric("Latest report age", f"{max(base_pos['age_days'], quote_pos['age_days'])} days")
        position_rows = pd.DataFrame([
            {"Currency": pair.base, "Leveraged net": base_pos["leveraged_net"], "Asset-manager net": base_pos["asset_manager_net"], "3Y percentile": base_pos["percentile_3y"], "3Y z-score": base_pos["zscore_3y"], "State": base_pos["crowding"], "Report": base_pos["date"].strftime("%Y-%m-%d")},
            {"Currency": pair.quote, "Leveraged net": quote_pos["leveraged_net"], "Asset-manager net": quote_pos["asset_manager_net"], "3Y percentile": quote_pos["percentile_3y"], "3Y z-score": quote_pos["zscore_3y"], "State": quote_pos["crowding"], "Report": quote_pos["date"].strftime("%Y-%m-%d")},
        ])
        st.dataframe(position_rows.style.format({"Leveraged net":"{:,.0f}", "Asset-manager net":"{:,.0f}", "3Y percentile":"{:.0%}", "3Y z-score":"{:+.2f}"}), use_container_width=True, hide_index=True)
        if positioning["warning"]:
            st.warning(positioning["warning"])
    else:
        st.info(positioning["warning"])
    st.caption(f"Provider: {cftc_status.provider} · cadence: {cftc_status.cadence} · fetched {cftc_status.fetched_at:%Y-%m-%d %H:%M} UTC.")
    if cftc_status.message:
        st.warning(cftc_status.message)
    st.markdown("#### Derivatives and sentiment coverage")
    st.dataframe(derivatives_availability(), use_container_width=True, hide_index=True)
    st.info("Implied volatility, 25-delta risk reversals and retail positioning remain unavailable until verified provider credentials are configured. The terminal does not manufacture proxies or feed unavailable values into its score.")

with tabs[3]:
    st.markdown(f"#### Empirical {config.forward_days}-trading-day scenarios")
    cols = st.columns(3)
    for col, label in zip(cols, ("Bullish", "Range/neutral", "Bearish")):
        col.metric(label, f"{probs[label]:.0%}")
        col.progress(int(probs[label] * 100))
    st.info(f"Calibration uses {sample} historically similar score observations. Confidence: {confidence}. These are empirical research frequencies, not guaranteed forecasts.")

with tabs[4]:
    st.info(f"Interpretation only — pair model: {profile.thesis}. Weights are pair-specific and change modestly with volatility and trend regime.")
    audit = components.loc[latest.name].sort_values(key=abs, ascending=False).rename("Contribution").to_frame()
    audit["Interpretation"] = np.where(audit.Contribution > 0, f"{pair.base} supportive", np.where(audit.Contribution < 0, f"{pair.quote} supportive", "Neutral"))
    st.dataframe(audit.style.format({"Contribution":"{:+.2f}"}), use_container_width=True)
    st.caption("Every component is bounded. Contributions explain the model interpretation; they are not observed facts or trade instructions.")

with tabs[5]:
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

with tabs[6]:
    st.markdown(f"""
### How TRADE90 evaluates {selected}

The terminal combines trend, momentum, RSI, the **{pair.base}–{pair.quote} 10-year yield differential**, its recent impulse, and **{pair.driver_label}**. A manual policy overlay is kept separate so judgment never masquerades as observed data.

This pair uses a dedicated model profile: **{pair_model_profile(selected).thesis}**. Its component weights differ from the other six major pairs and adapt modestly between high-volatility, trending, and transitional regimes. The Validation tab evaluates the selected pair's resulting score independently.

### Accuracy safeguards

- Signals are lagged before historical returns are calculated.
- Scenario percentages are calibrated from historically similar observations.
- Walk-forward validation uses only prior data to set its adaptive threshold.
- Data age and completeness directly limit the confidence label.
- Stale yields and cross-asset observations are automatically excluded from the score.
- Provider, cadence, age and inclusion status are visible above the analysis tabs.
- The audit exposes every contribution instead of hiding the result in a black box.

### Current limitations

This public-data edition is end-of-day research, not a real-time dealing terminal. The event engine displays provider-supplied high-impact calendar observations and keeps them out of the directional score. It does not yet include licensed tick data, options surfaces, CFTC positioning, live news or broker execution. FRED, Yahoo and calendar observations may be delayed, revised or aligned to different closes.
""")
