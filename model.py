from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from typing import Dict, Tuple
from urllib.parse import urlencode
from urllib.request import urlopen

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ModelConfig:
    fast_ema: int = 20
    slow_ema: int = 50
    rsi_period: int = 14
    momentum_period: int = 20
    entry_threshold: float = 18.0
    round_trip_cost_bps: float = 2.0


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss = -delta.clip(upper=0).ewm(alpha=1 / period, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(50)


def rolling_zscore(series: pd.Series, window: int = 252) -> pd.Series:
    mean = series.rolling(window, min_periods=max(20, window // 4)).mean()
    std = series.rolling(window, min_periods=max(20, window // 4)).std()
    return ((series - mean) / std.replace(0, np.nan)).clip(-3, 3)


def fred_series(series_id: str, timeout: int = 15) -> pd.Series:
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
    with urlopen(f"{url}?{urlencode({'id': series_id})}", timeout=timeout) as response:
        text = response.read().decode("utf-8")
    frame = pd.read_csv(StringIO(text))
    frame["DATE"] = pd.to_datetime(frame["DATE"])
    values = pd.to_numeric(frame[series_id], errors="coerce")
    return pd.Series(values.values, index=frame["DATE"], name=series_id).dropna()


def prepare_features(
    price: pd.Series,
    us_10y: pd.Series | None = None,
    jp_10y: pd.Series | None = None,
    vix: pd.Series | None = None,
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

    if us_10y is not None and jp_10y is not None:
        macro = pd.concat([us_10y.rename("us10y"), jp_10y.rename("jp10y")], axis=1)
        macro = macro.sort_index().ffill()
        macro["yield_spread"] = macro["us10y"] - macro["jp10y"]
        df = df.join(macro, how="left").ffill()
        df["spread_z"] = rolling_zscore(df["yield_spread"], 252)
        df["spread_change"] = df["yield_spread"].diff(20)
    else:
        df[["us10y", "jp10y", "yield_spread", "spread_z", "spread_change"]] = np.nan

    if vix is not None:
        df["vix"] = vix.reindex(df.index).ffill()
        df["vix_change"] = df["vix"].pct_change(10)
    else:
        df[["vix", "vix_change"]] = np.nan
    return df


def score_features(df: pd.DataFrame, policy_bias: float = 0.0) -> Tuple[pd.DataFrame, pd.DataFrame]:
    out = df.copy()
    components = pd.DataFrame(index=out.index)
    components["Trend"] = np.tanh(((out["ema_fast"] / out["ema_slow"]) - 1) * 80) * 25
    components["Momentum"] = np.tanh(out["momentum"] * 20) * 18
    components["RSI"] = np.tanh((out["rsi"] - 50) / 15) * 12
    components["Yield differential"] = np.tanh(out["spread_z"].fillna(0) / 1.5) * 20
    components["Yield impulse"] = np.tanh(out["spread_change"].fillna(0) * 3) * 10
    components["Risk sentiment"] = -np.tanh(out["vix_change"].fillna(0) * 5) * 8
    components["Policy overlay"] = float(np.clip(policy_bias, -1, 1)) * 7
    out["score"] = components.sum(axis=1).clip(-100, 100)
    return out, components


def scenario_probabilities(score: float) -> Dict[str, float]:
    logits = np.array([score / 22.0, -abs(score) / 35.0 + 0.35, -score / 22.0])
    probs = np.exp(logits - logits.max())
    probs /= probs.sum()
    return {k: float(v) for k, v in zip(("Bullish USD/JPY", "Range/neutral", "Bearish USD/JPY"), probs)}


def backtest(scored: pd.DataFrame, config: ModelConfig = ModelConfig()) -> Tuple[pd.DataFrame, Dict[str, float]]:
    bt = scored[["close", "return", "score"]].dropna().copy()
    raw_position = np.where(bt["score"] > config.entry_threshold, 1, np.where(bt["score"] < -config.entry_threshold, -1, 0))
    bt["position"] = pd.Series(raw_position, index=bt.index).shift(1).fillna(0)
    turnover = bt["position"].diff().abs().fillna(bt["position"].abs())
    cost = turnover * (config.round_trip_cost_bps / 2) / 10_000
    bt["strategy_return"] = bt["position"] * bt["return"] - cost
    bt["strategy_equity"] = (1 + bt["strategy_return"].fillna(0)).cumprod()
    bt["buy_hold_equity"] = (1 + bt["return"].fillna(0)).cumprod()
    years = max((bt.index[-1] - bt.index[0]).days / 365.25, 1 / 252)
    total = bt["strategy_equity"].iloc[-1] - 1
    cagr = bt["strategy_equity"].iloc[-1] ** (1 / years) - 1
    vol = bt["strategy_return"].std() * np.sqrt(252)
    sharpe = (bt["strategy_return"].mean() * 252 / vol) if vol > 0 else np.nan
    drawdown = bt["strategy_equity"] / bt["strategy_equity"].cummax() - 1
    active = bt.loc[bt["position"] != 0, "strategy_return"]
    metrics = {
        "Total return": total,
        "CAGR": cagr,
        "Annual volatility": vol,
        "Sharpe (0% rf)": sharpe,
        "Maximum drawdown": drawdown.min(),
        "Active-day hit rate": (active > 0).mean() if len(active) else np.nan,
        "Position changes": float((turnover > 0).sum()),
    }
    return bt, metrics
