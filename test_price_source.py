from datetime import date, timedelta

import pandas as pd
import pytest

from publish_snapshot import MIN_PRICE_OBSERVATIONS, resolve_price, usable_price
from trade90_model import PAIR_CONFIGS

TODAY = date(2026, 8, 18)


def series(count, end=TODAY, start_value=4400.0):
    index = pd.date_range(end=pd.Timestamp(end), periods=count, freq="D")
    return pd.Series([start_value + i for i in range(count)], index=index)


def frame(**columns):
    return pd.DataFrame(columns)


def test_gold_prefers_spot_so_the_quote_matches_a_broker():
    gold = PAIR_CONFIGS["XAU/USD"]
    assert gold.ticker == "XAUUSD=X"
    assert gold.fallback_ticker == "GC=F"
    assert gold.price_basis == "Spot"
    assert gold.fallback_basis == "COMEX futures"


def test_spot_is_used_when_it_is_deep_and_current():
    gold = PAIR_CONFIGS["XAU/USD"]
    close = frame(**{"XAUUSD=X": series(800), "GC=F": series(800, start_value=4460.0)})
    chosen, basis, note = resolve_price(close, gold, TODAY)
    assert basis == "Spot"
    assert "spot gold CFD" in note
    assert chosen.iloc[-1] == 4400.0 + 799


def test_futures_fallback_is_used_when_spot_is_too_sparse():
    gold = PAIR_CONFIGS["XAU/USD"]
    close = frame(**{"XAUUSD=X": series(20), "GC=F": series(800, start_value=4460.0)})
    _, basis, note = resolve_price(close, gold, TODAY)
    assert basis == "COMEX futures"
    assert "will not match a spot broker quote" in note


def test_futures_fallback_is_used_when_spot_has_gone_stale():
    gold = PAIR_CONFIGS["XAU/USD"]
    stale = series(800, end=TODAY - timedelta(days=30))
    close = frame(**{"XAUUSD=X": stale, "GC=F": series(800, start_value=4460.0)})
    _, basis, _ = resolve_price(close, gold, TODAY)
    assert basis == "COMEX futures"


def test_a_missing_spot_column_falls_back_rather_than_raising():
    gold = PAIR_CONFIGS["XAU/USD"]
    close = frame(**{"GC=F": series(800, start_value=4460.0)})
    _, basis, _ = resolve_price(close, gold, TODAY)
    assert basis == "COMEX futures"


def test_thin_spot_is_still_used_when_no_fallback_qualifies():
    """Better a labelled thin series than no market at all."""
    gold = PAIR_CONFIGS["XAU/USD"]
    close = frame(**{"XAUUSD=X": series(20), "GC=F": series(20, start_value=4460.0)})
    _, basis, _ = resolve_price(close, gold, TODAY)
    assert basis == "Spot"


def test_no_data_at_all_fails_loudly():
    gold = PAIR_CONFIGS["XAU/USD"]
    with pytest.raises(RuntimeError, match="XAU/USD"):
        resolve_price(frame(**{"AUDUSD=X": series(800)}), gold, TODAY)


def test_fx_pairs_have_no_fallback_and_report_spot():
    close = frame(**{"EURUSD=X": series(800)})
    _, basis, _ = resolve_price(close, PAIR_CONFIGS["EUR/USD"], TODAY)
    assert basis == "Spot"
    for symbol in ("EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"):
        assert PAIR_CONFIGS[symbol].fallback_ticker == "", symbol


@pytest.mark.parametrize("count, expected", [
    (MIN_PRICE_OBSERVATIONS - 1, False),
    (MIN_PRICE_OBSERVATIONS, True),
])
def test_depth_threshold_is_applied_at_the_boundary(count, expected):
    assert usable_price(series(count), TODAY) is expected


def test_an_empty_or_missing_series_is_never_usable():
    assert usable_price(None, TODAY) is False
    assert usable_price(pd.Series(dtype=float), TODAY) is False
