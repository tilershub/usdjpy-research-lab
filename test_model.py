import numpy as np
import pandas as pd
from unittest.mock import patch

from model import (
    PAIR_CONFIGS, ModelConfig, backtest, calibrated_probabilities, confidence_grade,
    benchmark_comparison, data_quality, expanding_probability_validation, fred_series, horizon_validation, prepare_features, scenario_probabilities, score_features,
    walk_forward_metrics,
)


def fixture():
    idx = pd.bdate_range("2020-01-01", periods=700)
    px = pd.Series(105 * np.exp(np.linspace(0, 0.25, len(idx)) + np.sin(np.arange(len(idx)) / 30) * 0.01), index=idx)
    us = pd.Series(np.linspace(1, 4.5, len(idx)), index=idx)
    jp = pd.Series(np.linspace(0, 1.0, len(idx)), index=idx)
    vix = pd.Series(20 + np.sin(np.arange(len(idx)) / 10), index=idx)
    return prepare_features(px, us, jp, vix)


def test_probabilities_sum_to_one():
    assert abs(sum(scenario_probabilities(25).values()) - 1) < 1e-12


def test_all_seven_major_pairs_have_pair_specific_inputs():
    assert len(PAIR_CONFIGS) == 7
    assert set(PAIR_CONFIGS) == {"EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"}
    assert all(pair.base_yield and pair.quote_yield and pair.driver for pair in PAIR_CONFIGS.values())


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


def test_empirical_calibration_and_walk_forward_are_finite():
    scored, _ = score_features(fixture())
    probabilities, sample = calibrated_probabilities(scored, float(scored["score"].dropna().iloc[-1]))
    assert abs(sum(probabilities.values()) - 1) < 1e-12
    assert sample >= 40
    result = walk_forward_metrics(scored)
    assert result["OOS observations"] > 0
    assert 0 <= result["OOS directional accuracy"] <= 1


def test_quality_and_confidence_penalize_stale_data():
    scored, _ = score_features(fixture())
    quality = data_quality(scored, pd.Timestamp("2025-01-01"))
    assert quality["grade"] == "C"
    assert confidence_grade({"Bullish": .7, "Range/neutral": .2, "Bearish": .1}, 120, "C") == "Moderate"


def test_quality_reports_component_freshness_and_stale_inputs():
    scored, _ = score_features(fixture())
    quality = data_quality(scored, scored.index[-1])
    assert quality["base_yield_age_days"] == 0
    assert quality["quote_yield_age_days"] == 0
    assert quality["driver_age_days"] == 0
    assert quality["stale_inputs"] == []


def test_stale_macro_and_driver_inputs_are_excluded_from_score():
    frame = fixture()
    frame.loc[frame.index[-1], ["base_yield_age_days", "quote_yield_age_days", "driver_age_days"]] = [60, 60, 10]
    _, components = score_features(frame)
    latest = components.iloc[-1]
    assert latest["Rate differential"] == 0
    assert latest["Rate impulse"] == 0
    assert latest["Cross-asset driver"] == 0


def test_fred_parser_accepts_observation_date_header():
    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_):
            return None

        def read(self):
            return b"observation_date,DGS10\n2026-07-17,4.25\n"

    with patch("model.urlopen", return_value=Response()):
        result = fred_series("DGS10")
    assert result.index[0] == pd.Timestamp("2026-07-17")
    assert result.iloc[0] == 4.25


def test_validation_suite_is_out_of_sample_and_benchmarked():
    scored, _ = score_features(fixture())
    horizons = horizon_validation(scored, ModelConfig(entry_threshold=5), train_days=300)
    assert set(horizons.index) == {"1D", "5D", "20D"}
    assert (horizons["OOS observations"] > 0).all()
    benchmarks = benchmark_comparison(scored)
    assert {"TRADE90 model", "Buy & hold", "MA trend", "Carry only", "Random direction"} == set(benchmarks.index)
    assert np.isfinite(benchmarks.loc["TRADE90 model", "Maximum drawdown"])


def test_expanding_probability_validation_uses_prior_history():
    scored, _ = score_features(fixture())
    metrics, reliability = expanding_probability_validation(scored, train_days=300, step=10)
    assert metrics["Forecasts"] > 0
    assert 0 <= metrics["Calibration error"] <= 1
    assert np.isfinite(metrics["Brier score"])
    assert reliability["Forecasts"].sum() == metrics["Forecasts"]
