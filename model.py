from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from typing import Dict, Mapping, Tuple
from urllib.parse import urlencode
from urllib.request import urlopen

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class PairConfig:
    symbol: str
    ticker: str
    base: str
    quote: str
    base_yield: str
    quote_yield: str
    driver: str
    driver_label: str
    driver_sign: float
    decimals: int = 5


PAIR_CONFIGS: Mapping[str, PairConfig] = {
    "EUR/USD": PairConfig("EUR/USD", "EURUSD=X", "EUR", "USD", "IRLTLT01EZM156N", "DGS10", "DX-Y.NYB", "US dollar index", -1),
    "GBP/USD": PairConfig("GBP/USD", "GBPUSD=X", "GBP", "USD", "IRLTLT01GBM156N", "DGS10", "DX-Y.NYB", "US dollar index", -1),
    "USD/JPY": PairConfig("USD/JPY", "JPY=X", "USD", "JPY", "DGS10", "IRLTLT01JPM156N", "^VIX", "VIX risk stress", -1, 3),
    "USD/CHF": PairConfig("USD/CHF", "CHF=X", "USD", "CHF", "DGS10", "IRLTLT01CHM156N", "^VIX", "VIX risk stress", -1),
    "USD/CAD": PairConfig("USD/CAD", "CAD=X", "USD", "CAD", "DGS10", "IRLTLT01CAM156N", "CL=F", "WTI crude oil", -1),
    "AUD/USD": PairConfig("AUD/USD", "AUDUSD=X", "AUD", "USD", "IRLTLT01AUM156N", "DGS10", "HG=F", "Copper", 1),
    "NZD/USD": PairConfig("NZD/USD", "NZDUSD=X", "NZD", "USD", "IRLTLT01NZM156N", "DGS10", "^GSPC", "Global risk proxy", 1),
}


@dataclass(frozen=True)
class ModelConfig:
    fast_ema: int = 20
    slow_ema: int = 50
    rsi_period: int = 14
    momentum_period: int = 20
    forward_days: int = 5
    entry_threshold: float = 18.0
    round_trip_cost_bps: float = 2.0


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss = -delta.clip(upper=0).ewm(alpha=1 / period, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(50)


def rolling_zscore(series: pd.Series, window: int = 252) -> pd.Series:
    minimum = max(20, window // 4)
    mean = series.rolling(window, min_periods=minimum).mean()
    std = series.rolling(window, min_periods=minimum).std()
    return ((series - mean) / std.replace(0, np.nan)).clip(-3, 3)


def fred_series(series_id: str, timeout: int = 15) -> pd.Series:
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
    with urlopen(f"{url}?{urlencode({'id': series_id})}", timeout=timeout) as response:
        text = response.read().decode("utf-8")
    frame = pd.read_csv(StringIO(text))
    date_column = next((c for c in frame.columns if c.strip().lower() in {"date", "observation_date"}), frame.columns[0])
    frame[date_column] = pd.to_datetime(frame[date_column], errors="coerce")
    if series_id not in frame.columns:
        raise ValueError(f"FRED response did not contain the requested series: {series_id}")
    values = pd.to_numeric(frame[series_id], errors="coerce")
    series = pd.Series(values.values, index=frame[date_column], name=series_id)
    return series.loc[series.index.notna()].dropna().sort_index()


def prepare_features(
    price: pd.Series,
    base_yield: pd.Series | None = None,
    quote_yield: pd.Series | None = None,
    driver: pd.Series | None = None,
    driver_sign: float = 1.0,
    config: ModelConfig = ModelConfig(),
) -> pd.DataFrame:
    px = price.dropna().astype(float).sort_index()
    df = pd.DataFrame(index=px.index)
    df["close"] = px
    df["return"] = px.pct_change()
    df["ema_fast"] = px.ewm(span=config.fast_ema, adjust=False).mean()
    df["ema_slow"] = px.ewm(span=config.slow_ema, adjust=False).mean()
    df["rsi"] = rsi(px, config.rsi_period)
    df["momentum"] = px.pct_change(config.momentum_period)
    df["volatility"] = df["return"].rolling(20).std() * np.sqrt(252)
    true_range = pd.concat([px.diff().abs(), px.pct_change().abs() * px.shift(1)], axis=1).max(axis=1)
    df["atr20"] = true_range.rolling(20).mean()
    df["support20"] = px.rolling(20).min()
    df["resistance20"] = px.rolling(20).max()

    if base_yield is not None and quote_yield is not None:
        macro = pd.concat([base_yield.rename("base_yield"), quote_yield.rename("quote_yield")], axis=1).sort_index().ffill()
        macro["yield_spread"] = macro["base_yield"] - macro["quote_yield"]
        df = df.join(macro, how="left").ffill()
        df["spread_z"] = rolling_zscore(df["yield_spread"], 252)
        df["spread_change"] = df["yield_spread"].diff(20)
    else:
        df[["base_yield", "quote_yield", "yield_spread", "spread_z", "spread_change"]] = np.nan

    if driver is not None:
        aligned = driver.reindex(df.index).ffill()
        df["driver"] = aligned
        df["driver_return"] = aligned.pct_change(20) * float(driver_sign)
        df["driver_z"] = rolling_zscore(df["driver_return"], 252)
    else:
        df[["driver", "driver_return", "driver_z"]] = np.nan
    df["forward_return"] = px.pct_change(config.forward_days).shift(-config.forward_days)
    return df


def score_features(df: pd.DataFrame, policy_bias: float = 0.0) -> Tuple[pd.DataFrame, pd.DataFrame]:
    out = df.copy()
    components = pd.DataFrame(index=out.index)
    components["Trend"] = np.tanh(((out["ema_fast"] / out["ema_slow"]) - 1) * 80) * 24
    components["Momentum"] = np.tanh(out["momentum"] * 20) * 16
    components["RSI"] = np.tanh((out["rsi"] - 50) / 15) * 10
    components["Rate differential"] = np.tanh(out["spread_z"].fillna(0) / 1.5) * 22
    components["Rate impulse"] = np.tanh(out["spread_change"].fillna(0) * 3) * 10
    components["Cross-asset driver"] = np.tanh(out["driver_z"].fillna(0) / 1.5) * 11
    components["Policy overlay"] = float(np.clip(policy_bias, -1, 1)) * 7
    out["score"] = components.sum(axis=1).clip(-100, 100)
    return out, components


def calibrated_probabilities(scored: pd.DataFrame, score: float, min_sample: int = 40) -> Tuple[Dict[str, float], int]:
    history = scored[["score", "forward_return"]].dropna()
    if history.empty:
        return heuristic_probabilities(score), 0
    distance = (history["score"] - score).abs()
    sample = history.loc[distance.nsmallest(min(min_sample * 3, len(history))).index].copy()
    bandwidth = max(float(sample["score"].std()), 8.0)
    weights = np.exp(-0.5 * ((sample["score"] - score) / bandwidth) ** 2)
    neutral_band = max(float(sample["forward_return"].abs().median()) * 0.35, 0.0005)
    outcomes = np.where(sample["forward_return"] > neutral_band, 0, np.where(sample["forward_return"] < -neutral_band, 2, 1))
    weighted = np.array([weights[outcomes == i].sum() for i in range(3)]) + 2.0
    probs = weighted / weighted.sum()
    return {k: float(v) for k, v in zip(("Bullish", "Range/neutral", "Bearish"), probs)}, len(sample)


def heuristic_probabilities(score: float) -> Dict[str, float]:
    logits = np.array([score / 22.0, -abs(score) / 35.0 + 0.35, -score / 22.0])
    probs = np.exp(logits - logits.max())
    probs /= probs.sum()
    return {k: float(v) for k, v in zip(("Bullish", "Range/neutral", "Bearish"), probs)}


def scenario_probabilities(score: float) -> Dict[str, float]:
    return heuristic_probabilities(score)


def data_quality(scored: pd.DataFrame, today: pd.Timestamp | None = None) -> Dict[str, object]:
    last_price = scored["close"].dropna().index.max()
    today = (today or pd.Timestamp.utcnow()).tz_localize(None).normalize()
    age = max(int((today - pd.Timestamp(last_price).tz_localize(None).normalize()).days), 0)
    latest = scored.loc[last_price]
    macro_available = pd.notna(latest.get("yield_spread"))
    driver_available = pd.notna(latest.get("driver"))
    completeness = float(pd.Series([macro_available, driver_available, pd.notna(latest.get("atr20"))]).mean())
    grade = "A" if age <= 3 and completeness == 1 else "B" if age <= 4 and completeness >= 2 / 3 else "C"
    return {"grade": grade, "price_age_days": age, "completeness": completeness, "last_price": last_price}


def confidence_grade(probabilities: Dict[str, float], sample_size: int, quality_grade: str) -> str:
    edge = max(probabilities.values()) - 1 / 3
    points = (2 if edge >= 0.18 else 1 if edge >= 0.10 else 0) + (1 if sample_size >= 100 else 0) + (1 if quality_grade == "A" else 0)
    return "High" if points >= 4 else "Moderate" if points >= 2 else "Low"


def regime(latest: pd.Series) -> str:
    trend = abs(float(latest["ema_fast"] / latest["ema_slow"] - 1))
    vol = float(latest.get("volatility", np.nan))
    if pd.notna(vol) and vol > 0.16:
        return "High volatility"
    if trend > 0.01:
        return "Trending"
    return "Range / transition"


def backtest(scored: pd.DataFrame, config: ModelConfig = ModelConfig()) -> Tuple[pd.DataFrame, Dict[str, float]]:
    bt = scored[["close", "return", "score"]].dropna().copy()
    raw = np.where(bt["score"] > config.entry_threshold, 1, np.where(bt["score"] < -config.entry_threshold, -1, 0))
    bt["position"] = pd.Series(raw, index=bt.index).shift(1).fillna(0)
    turnover = bt["position"].diff().abs().fillna(bt["position"].abs())
    cost = turnover * (config.round_trip_cost_bps / 2) / 10_000
    bt["strategy_return"] = bt["position"] * bt["return"] - cost
    bt["strategy_equity"] = (1 + bt["strategy_return"].fillna(0)).cumprod()
    bt["buy_hold_equity"] = (1 + bt["return"].fillna(0)).cumprod()
    years = max((bt.index[-1] - bt.index[0]).days / 365.25, 1 / 252)
    vol = bt["strategy_return"].std() * np.sqrt(252)
    drawdown = bt["strategy_equity"] / bt["strategy_equity"].cummax() - 1
    active = bt.loc[bt["position"] != 0, "strategy_return"]
    metrics = {
        "Total return": bt["strategy_equity"].iloc[-1] - 1,
        "CAGR": bt["strategy_equity"].iloc[-1] ** (1 / years) - 1,
        "Annual volatility": vol,
        "Sharpe (0% rf)": bt["strategy_return"].mean() * 252 / vol if vol > 0 else np.nan,
        "Maximum drawdown": drawdown.min(),
        "Active-day hit rate": (active > 0).mean() if len(active) else np.nan,
        "Position changes": float((turnover > 0).sum()),
    }
    return bt, metrics



def _risk_metrics(returns: pd.Series) -> Dict[str, float]:
    returns = returns.dropna().astype(float)
    if returns.empty:
        return {"Total return": np.nan, "CAGR": np.nan, "Sharpe": np.nan, "Maximum drawdown": np.nan, "Hit rate": np.nan, "Profit factor": np.nan}
    equity = (1 + returns).cumprod()
    years = max((returns.index[-1] - returns.index[0]).days / 365.25, 1 / 252)
    vol = returns.std() * np.sqrt(252)
    losses = -returns[returns < 0].sum()
    return {
        "Total return": float(equity.iloc[-1] - 1),
        "CAGR": float(equity.iloc[-1] ** (1 / years) - 1),
        "Sharpe": float(returns.mean() * 252 / vol) if vol > 0 else np.nan,
        "Maximum drawdown": float((equity / equity.cummax() - 1).min()),
        "Hit rate": float((returns > 0).mean()),
        "Profit factor": float(returns[returns > 0].sum() / losses) if losses > 0 else np.nan,
    }


def benchmark_comparison(scored: pd.DataFrame, config: ModelConfig = ModelConfig(), seed: int = 90) -> pd.DataFrame:
    data = scored[["return", "score", "ema_fast", "ema_slow", "yield_spread"]].dropna(subset=["return", "score"]).copy()
    model_signal = np.where(data["score"] > config.entry_threshold, 1, np.where(data["score"] < -config.entry_threshold, -1, 0))
    signals = {
        "TRADE90 model": pd.Series(model_signal, index=data.index),
        "Buy & hold": pd.Series(1.0, index=data.index),
        "MA trend": np.sign(data["ema_fast"] - data["ema_slow"]).fillna(0),
        "Carry only": np.sign(data["yield_spread"]).fillna(0),
        "Random direction": pd.Series(np.random.default_rng(seed).choice([-1, 0, 1], len(data)), index=data.index),
    }
    rows = []
    for name, raw_signal in signals.items():
        position = raw_signal.shift(1).fillna(0)
        turnover = position.diff().abs().fillna(position.abs())
        cost = turnover * (config.round_trip_cost_bps / 2) / 10_000
        strategy_return = position * data["return"] - cost
        rows.append({"Benchmark": name, **_risk_metrics(strategy_return), "Active days": int((position != 0).sum())})
    return pd.DataFrame(rows).set_index("Benchmark")


def horizon_validation(
    scored: pd.DataFrame,
    config: ModelConfig = ModelConfig(),
    horizons: Tuple[int, ...] = (1, 5, 20),
    train_days: int = 504,
) -> pd.DataFrame:
    data = scored[["close", "score", "ema_fast", "ema_slow"]].dropna().copy()
    rows = []
    for horizon in horizons:
        future_return = data["close"].shift(-horizon) / data["close"] - 1
        test = data.iloc[train_days:].copy()
        test["future_return"] = future_return.reindex(test.index)
        test = test.dropna(subset=["future_return"])
        signal = np.where(test["score"] > config.entry_threshold, 1, np.where(test["score"] < -config.entry_threshold, -1, 0))
        active = pd.Series(signal, index=test.index) != 0
        model_correct = (np.sign(pd.Series(signal, index=test.index)[active] * test.loc[active, "future_return"]) > 0)
        ma_signal = np.sign(test["ema_fast"] - test["ema_slow"])
        ma_correct = np.sign(ma_signal[active] * test.loc[active, "future_return"]) > 0
        base_rate = max(float((test.loc[active, "future_return"] > 0).mean()), float((test.loc[active, "future_return"] < 0).mean())) if active.any() else np.nan
        rows.append({
            "Horizon": f"{horizon}D",
            "OOS observations": int(active.sum()),
            "Model accuracy": float(model_correct.mean()) if len(model_correct) else np.nan,
            "MA accuracy": float(ma_correct.mean()) if len(ma_correct) else np.nan,
            "Majority baseline": base_rate,
            "Lift vs baseline": float(model_correct.mean() - base_rate) if len(model_correct) else np.nan,
        })
    return pd.DataFrame(rows).set_index("Horizon")


def expanding_probability_validation(
    scored: pd.DataFrame,
    train_days: int = 504,
    step: int = 5,
    min_sample: int = 40,
) -> Tuple[Dict[str, float], pd.DataFrame]:
    data = scored[["score", "forward_return"]].dropna().copy()
    records = []
    for i in range(train_days, len(data), step):
        history = data.iloc[:i]
        current = data.iloc[i]
        probabilities, sample = calibrated_probabilities(history, float(current["score"]), min_sample)
        neutral_band = max(float(history["forward_return"].abs().median()) * 0.35, 0.0005)
        actual = "Bullish" if current["forward_return"] > neutral_band else "Bearish" if current["forward_return"] < -neutral_band else "Range/neutral"
        records.append({"date": data.index[i], **probabilities, "actual": actual, "sample": sample})
    if not records:
        return {"Brier score": np.nan, "Log loss": np.nan, "Calibration error": np.nan, "Forecasts": 0.0}, pd.DataFrame()
    forecasts = pd.DataFrame(records).set_index("date")
    labels = ["Bullish", "Range/neutral", "Bearish"]
    y = np.column_stack([(forecasts["actual"] == label).astype(float) for label in labels])
    p = forecasts[labels].to_numpy()
    brier = float(np.mean(np.sum((p - y) ** 2, axis=1)))
    log_loss = float(-np.mean(np.log(np.clip(p[np.arange(len(p)), np.argmax(y, axis=1)], 1e-9, 1))))
    confidence = p.max(axis=1)
    correct = (np.array(labels)[p.argmax(axis=1)] == forecasts["actual"].to_numpy()).astype(float)
    bins = pd.cut(confidence, bins=[0, .4, .5, .6, .7, .8, 1], include_lowest=True)
    reliability = pd.DataFrame({"confidence": confidence, "correct": correct, "bin": bins}).groupby("bin", observed=True).agg(
        Forecasts=("correct", "size"), Mean_confidence=("confidence", "mean"), Observed_accuracy=("correct", "mean")
    )
    ece = float(sum(reliability["Forecasts"] / len(forecasts) * (reliability["Mean_confidence"] - reliability["Observed_accuracy"]).abs()))
    return {"Brier score": brier, "Log loss": log_loss, "Calibration error": ece, "Forecasts": float(len(forecasts))}, reliability


def walk_forward_metrics(scored: pd.DataFrame, config: ModelConfig = ModelConfig(), train_days: int = 504) -> Dict[str, float]:
    data = scored[["return", "score"]].dropna().copy()
    if len(data) <= train_days + 20:
        return {"OOS directional accuracy": np.nan, "OOS observations": 0.0}
    rolling_scale = data["score"].rolling(train_days, min_periods=train_days).std().shift(1)
    adaptive_threshold = (rolling_scale * 0.65).clip(lower=config.entry_threshold * 0.7, upper=config.entry_threshold * 1.5)
    signal = np.where(data["score"] > adaptive_threshold, 1, np.where(data["score"] < -adaptive_threshold, -1, 0))
    position = pd.Series(signal, index=data.index).shift(1)
    oos = pd.DataFrame({"position": position, "return": data["return"]}).iloc[train_days:].dropna()
    active = oos[oos["position"] != 0]
    accuracy = (np.sign(active["position"] * active["return"]) > 0).mean() if len(active) else np.nan
    return {"OOS directional accuracy": float(accuracy), "OOS observations": float(len(active))}
