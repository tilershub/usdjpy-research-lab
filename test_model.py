import numpy as np
import pandas as pd

from model import ModelConfig, backtest, prepare_features, scenario_probabilities, score_features


def fixture():
    idx = pd.bdate_range("2020-01-01", periods=700)
    px = pd.Series(105 * np.exp(np.linspace(0, 0.25, len(idx)) + np.sin(np.arange(len(idx)) / 30) * 0.01), index=idx)
    us = pd.Series(np.linspace(1, 4.5, len(idx)), index=idx)
    jp = pd.Series(np.linspace(0, 1.0, len(idx)), index=idx)
    vix = pd.Series(20 + np.sin(np.arange(len(idx)) / 10), index=idx)
    return prepare_features(px, us, jp, vix)


def test_probabilities_sum_to_one():
    assert abs(sum(scenario_probabilities(25).values()) - 1) < 1e-12


def test_scores_bounded_and_backtest_finite():
    scored, _ = score_features(fixture())
    assert scored["score"].dropna().between(-100, 100).all()
    bt, metrics = backtest(scored, ModelConfig())
    assert len(bt) > 500
    assert np.isfinite(metrics["Maximum drawdown"])


def test_backtest_uses_lagged_position():
    scored, _ = score_features(fixture())
    bt, _ = backtest(scored, ModelConfig(entry_threshold=0))
    expected = np.sign(scored.loc[bt.index, "score"].shift(1).fillna(0))
    assert (bt["position"] == expected).all()

