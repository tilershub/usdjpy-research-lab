from datetime import datetime, timezone

from positioning import (
    DISAGGREGATED_FIELDS,
    DISAGGREGATED_MARKETS,
    TFF_FIELDS,
    TFF_MARKETS,
    currency_snapshot,
    derivatives_availability,
    normalize_cftc,
    pair_positioning,
)


def sample_records():
    """Shaped like the CFTC public reporting API: named fields, string numbers."""
    rows = []
    for date, eur_long, eur_short, jpy_long, jpy_short in (
        ("2026-07-01T00:00:00.000", 100, 80, 80, 100),
        ("2026-07-08T00:00:00.000", 120, 80, 90, 110),
        ("2026-07-15T00:00:00.000", 150, 70, 60, 120),
    ):
        for name, long_side, short_side in (
            (TFF_MARKETS["EUR"], eur_long, eur_short),
            (TFF_MARKETS["JPY"], jpy_long, jpy_short),
        ):
            rows.append({
                "market_and_exchange_names": name,
                "report_date_as_yyyy_mm_dd": date,
                "lev_money_positions_long": str(long_side),
                "lev_money_positions_short": str(short_side),
                "asset_mgr_positions_long": "200",
                "asset_mgr_positions_short": "100",
                "open_interest_all": "1000",
            })
    return rows


def normalized_sample():
    return normalize_cftc(sample_records(), TFF_MARKETS, TFF_FIELDS, "TFF")


def test_cftc_normalization_and_pair_relative_positioning():
    history = normalized_sample()
    assert set(history["currency"]) == {"EUR", "JPY"}
    view = pair_positioning(history, "EUR", "JPY", datetime(2026, 7, 18, tzinfo=timezone.utc))
    assert view["available"]
    assert view["base"]["leveraged_net"] == 80
    assert view["quote"]["leveraged_net"] == -60
    assert view["relative_percentile"] > 0


def test_missing_currency_is_never_invented():
    view = currency_snapshot(normalized_sample(), "USD", datetime(2026, 7, 18, tzinfo=timezone.utc))
    assert not view["available"]


def test_unrecognised_markets_are_ignored_rather_than_guessed():
    records = sample_records() + [{
        "market_and_exchange_names": "WHEAT - CHICAGO BOARD OF TRADE",
        "report_date_as_yyyy_mm_dd": "2026-07-15T00:00:00.000",
        "lev_money_positions_long": "500",
        "lev_money_positions_short": "100",
    }]
    assert set(normalize_cftc(records, TFF_MARKETS, TFF_FIELDS, "TFF")["currency"]) == {"EUR", "JPY"}


def test_gold_reads_the_disaggregated_report_vocabulary():
    """Gold is a commodity, so it is absent from Traders in Financial Futures."""
    assert "XAU" not in TFF_MARKETS
    assert DISAGGREGATED_MARKETS["XAU"] == "GOLD - COMMODITY EXCHANGE INC."
    records = [{
        "market_and_exchange_names": DISAGGREGATED_MARKETS["XAU"],
        "report_date_as_yyyy_mm_dd": "2026-08-11T00:00:00.000",
        "m_money_positions_long_all": "148634",
        "m_money_positions_short_all": "10972",
        "swap_positions_long_all": "19092",
        "swap__positions_short_all": "243797",
        "open_interest_all": "400309",
    }]
    history = normalize_cftc(records, DISAGGREGATED_MARKETS, DISAGGREGATED_FIELDS, "DISAGGREGATED")
    view = currency_snapshot(history, "XAU", datetime(2026, 8, 14, tzinfo=timezone.utc))
    assert view["available"]
    assert view["leveraged_net"] == 137662
    assert view["speculative_label"] == "Managed money"


def test_unlicensed_derivatives_are_explicitly_unavailable():
    coverage = derivatives_availability().set_index("Dataset")
    assert coverage.loc["FX implied volatility", "Status"] == "Provider required"
    assert coverage.loc["25-delta risk reversal", "Provider"] == "Not configured"
