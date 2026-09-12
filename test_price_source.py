from dataclasses import replace
from datetime import date, timedelta

import pandas as pd
import pytest

from publish_snapshot import MIN_PRICE_OBSERVATIONS, resolve_price, usable_price
from trade90_model import PAIR_CONFIGS

TODAY = date(2026, 8, 18)

# A stand-in for any market with a preferred feed plus a declared proxy. Gold no
# longer needs one — Yahoo publishes no spot XAU/USD series — but the fallback
# mechanism still has to work for whatever market next needs it.
WITH_FALLBACK = replace(
    PAIR_CONFIGS["XAU/USD"],
    ticker="PREFERRED=X",
    price_basis="Spot",
    price_note="preferred feed",
    fallback_ticker="PROXY=F",
    fallback_basis="Proxy futures",
    fallback_note="proxy feed, will not match a spot quote",
)


def series(count, end=TODAY, start_value=4400.0):
    index = pd.date_range(end=pd.Timestamp(end), periods=count, freq="D")
    return pd.Series([start_value + i for i in range(count)], index=index)


def frame(**columns):
    return pd.DataFrame(columns)


def test_gold_is_priced_from_the_futures_feed_that_exists():
    """Yahoo has no spot XAU/USD series, so the config must not claim one."""
    gold = PAIR_CONFIGS["XAU/USD"]
    assert gold.ticker == "GC=F"
    assert gold.price_basis == "COMEX futures"
    assert "not spot execution prices" in gold.price_note


def test_preferred_feed_is_used_when_deep_and_current():
    close = frame(**{"PREFERRED=X": series(800), "PROXY=F": series(800, start_value=4460.0)})
    chosen, basis, note, ticker = resolve_price(close, WITH_FALLBACK, TODAY)
    assert (basis, ticker) == ("Spot", "PREFERRED=X")
    assert note == "preferred feed"
    assert chosen.iloc[-1] == 4400.0 + 799


def test_fallback_is_used_when_the_preferred_feed_is_too_sparse():
    close = frame(**{"PREFERRED=X": series(20), "PROXY=F": series(800, start_value=4460.0)})
    _, basis, note, ticker = resolve_price(close, WITH_FALLBACK, TODAY)
    assert (basis, ticker) == ("Proxy futures", "PROXY=F")
    assert "will not match a spot quote" in note


def test_fallback_is_used_when_the_preferred_feed_has_gone_stale():
    stale = series(800, end=TODAY - timedelta(days=30))
    close = frame(**{"PREFERRED=X": stale, "PROXY=F": series(800, start_value=4460.0)})
    assert resolve_price(close, WITH_FALLBACK, TODAY)[1] == "Proxy futures"


def test_a_missing_preferred_column_falls_back_rather_than_raising():
    close = frame(**{"PROXY=F": series(800, start_value=4460.0)})
    assert resolve_price(close, WITH_FALLBACK, TODAY)[1] == "Proxy futures"


def test_a_thin_preferred_feed_is_kept_when_no_fallback_qualifies():
    """Better a labelled thin series than no market at all."""
    close = frame(**{"PREFERRED=X": series(20), "PROXY=F": series(20, start_value=4460.0)})
    assert resolve_price(close, WITH_FALLBACK, TODAY)[1] == "Spot"


def test_no_data_at_all_fails_loudly():
    with pytest.raises(RuntimeError, match="XAU/USD"):
        resolve_price(frame(**{"AUDUSD=X": series(800)}), PAIR_CONFIGS["XAU/USD"], TODAY)


def test_fx_pairs_have_no_fallback_and_report_spot():
    close = frame(**{"EURUSD=X": series(800)})
    assert resolve_price(close, PAIR_CONFIGS["EUR/USD"], TODAY)[1] == "Spot"
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


def test_future_and_nonpositive_prices_are_not_usable():
    future=pd.Series([100.0]*600,index=pd.bdate_range('2030-01-01',periods=600))
    assert not usable_price(future,TODAY)
    invalid=pd.Series([100.0]*600,index=pd.bdate_range(end=TODAY,periods=600));invalid.iloc[0]=0
    assert not usable_price(invalid,TODAY)
