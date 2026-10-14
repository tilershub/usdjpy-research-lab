from datetime import datetime, timedelta, timezone
from django.test import SimpleTestCase

from .asset_drivers import CATALOG, research_driver_profile
from .technical_zones import technical_zones


def bars(count=90):
    start = datetime(2026, 10, 10, tzinfo=timezone.utc)
    result = []
    for i in range(count):
        # Three separated retests of a ceiling near 109, below a steady high of 110,
        # and several bounces from a floor around 95.
        high = 109.1 if i in (24, 39, 61) else 102.1
        low = 95.0 if i in (15, 35, 70) else 98.8
        close = 101.0 + (i % 3) * .1
        result.append({
            "open_at": start + timedelta(minutes=15 * i),
            "open": 100.5, "high": high, "low": low, "close": close,
        })
    return result


class InstrumentSpecificFactorsTests(SimpleTestCase):
    def test_all_nine_markets_have_distinct_macro_drivers(self):
        self.assertEqual(len(CATALOG), 9)
        for symbol in CATALOG:
            profile = research_driver_profile(symbol)
            self.assertEqual(profile["instrument"], symbol)
            self.assertGreaterEqual(len(profile["driver_watchlist"]), 4)
            self.assertTrue(all(d["status"] == "not_assessed" for d in profile["driver_watchlist"]))
            self.assertTrue(all(d["required_evidence"] for d in profile["driver_watchlist"]))

    def test_gold_and_usd_jpy_are_not_the_same_macro_template(self):
        gold = research_driver_profile("XAU/USD")
        yen = research_driver_profile("USD/JPY")
        self.assertIn("Central-bank", str(gold))
        self.assertIn("MOF intervention", str(yen))
        self.assertNotEqual(gold["driver_watchlist"], yen["driver_watchlist"])

    def test_no_synthetic_direction_or_fake_source_values(self):
        profile = research_driver_profile("BTC/USD")
        self.assertEqual(profile["driver_watchlist"][0]["status"], "not_assessed")
        self.assertNotIn("probability", str(profile).lower())


class TechnicalZoneTests(SimpleTestCase):
    def test_pivots_are_derived_from_closed_candles(self):
        result = technical_zones(bars(), 2.0)
        self.assertEqual(result["status"], "derived_from_closed_candles")
        self.assertTrue(result["overhead"])
        self.assertTrue(result["underfoot"])
        near_high = result["overhead"][0]
        self.assertGreater(near_high["zone_low"], result["reference_close"])
        self.assertGreaterEqual(near_high["confirmed_swing_count"], 2)
        self.assertTrue(near_high["stop_cluster_proxy"])
        self.assertLess(result["underfoot"][0]["zone_high"], result["reference_close"])
        self.assertIn("not observable", result["limitations"][0])

    def test_future_bar_cannot_form_early_confirmed_pivot(self):
        candles = bars()
        candles[-2]["high"] = 140
        early = technical_zones(candles[:-2], 2.0)
        later = technical_zones(candles, 2.0)
        # Latest unconfirmed bar should not be reported as a confirmed swing.
        self.assertFalse(any(zone["center"] > 120 for zone in later["overhead"]))
        self.assertTrue(early["overhead"])

    def test_low_information_does_not_generate_zones(self):
        self.assertEqual(technical_zones(bars()[:40], 2.0)["status"], "unavailable")
        self.assertEqual(technical_zones(bars(), 0)["status"], "unavailable")
