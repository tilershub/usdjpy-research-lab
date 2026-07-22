from datetime import datetime, timezone

import pandas as pd

from positioning import currency_snapshot, derivatives_availability, normalize_cftc, pair_positioning


def sample_frame():
    return pd.DataFrame({
        "Market_and_Exchange_Names": ["EURO FX", "JAPANESE YEN"] * 3,
        "Report_Date_as_YYYY_MM_DD": ["2026-07-01", "2026-07-01", "2026-07-08", "2026-07-08", "2026-07-15", "2026-07-15"],
        "Lev_Money_Positions_Long_All": [100, 80, 120, 90, 150, 60],
        "Lev_Money_Positions_Short_All": [80, 100, 80, 110, 70, 120],
        "Asset_Mgr_Positions_Long_All": [200, 150, 210, 155, 220, 160],
        "Asset_Mgr_Positions_Short_All": [100, 100, 100, 100, 100, 100],
        "Open_Interest_All": [1000] * 6,
    })


def test_cftc_normalization_and_pair_relative_positioning():
    history = normalize_cftc(sample_frame())
    assert set(history["currency"]) == {"EUR", "JPY"}
    view = pair_positioning(history, "EUR", "JPY", datetime(2026, 7, 18, tzinfo=timezone.utc))
    assert view["available"]
    assert view["base"]["leveraged_net"] == 80
    assert view["quote"]["leveraged_net"] == -60
    assert view["relative_percentile"] > 0


def test_missing_currency_is_never_invented():
    history = normalize_cftc(sample_frame())
    view = currency_snapshot(history, "USD", datetime(2026, 7, 18, tzinfo=timezone.utc))
    assert not view["available"]


def test_unlicensed_derivatives_are_explicitly_unavailable():
    coverage = derivatives_availability().set_index("Dataset")
    assert coverage.loc["FX implied volatility", "Status"] == "Provider required"
    assert coverage.loc["25-delta risk reversal", "Provider"] == "Not configured"
