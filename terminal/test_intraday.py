import os
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from django.core.cache import cache
from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from .intraday import (
    IntradayProviderError, analyze_candles, clean_completed_candles,
    enabled, get_intraday,
)


FIXED = datetime(2026, 10, 14, 12, 30, tzinfo=timezone.utc)


def fixture(symbol="EUR/USD", interval="15min", count=100, now=FIXED):
    span = 15 if interval == "15min" else 60
    values = []
    for index in range(count):
        opened = now - timedelta(minutes=(count - index) * span)
        close = 1.10 + index * .0001
        values.append({
            "datetime": opened.strftime("%Y-%m-%d %H:%M:%S"),
            "open": str(close - .00005), "high": str(close + .00005),
            "low": str(close - .0002), "close": str(close),
        })
    values.insert(0, {
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "open": "999", "high": "999", "low": "999", "close": "999",
    })
    return {"meta": {"symbol": symbol, "interval": interval, "exchange": "Test Reference"},
            "values": list(reversed(values))}


class IntradayAnalysisTests(SimpleTestCase):
    def test_only_completed_candles_and_chronology(self):
        rows = clean_completed_candles(fixture(), "EUR/USD", "15min", FIXED)
        self.assertEqual(len(rows), 100)
        self.assertLess(rows[-1]["close"], 2)
        self.assertEqual(rows[-1]["open_at"] + timedelta(minutes=15), FIXED)
        self.assertLess(rows[0]["open_at"], rows[-1]["open_at"])

    def test_ema_rsi_atr_and_breakout_research(self):
        rows = clean_completed_candles(fixture(), "EUR/USD", "15min", FIXED)
        result = analyze_candles(rows, "EUR/USD", "15min", now=FIXED)
        self.assertEqual(result["status"], "current")
        self.assertEqual(result["structure"], "Upward structure")
        self.assertEqual(result["range_context"], "Above prior 20-candle high")
        self.assertGreater(result["rsi14"], 50)
        self.assertGreater(result["atr14"], 0)
        self.assertGreater(result["ema20"], result["ema50"])
        self.assertEqual(result["age_minutes"], 0)
        self.assertNotIn("signal", result["structure"].lower())

    def test_weekend_stale_data_not_labelled_live(self):
        rows = clean_completed_candles(fixture(), "EUR/USD", "15min", FIXED)
        result = analyze_candles(rows, "EUR/USD", "15min", now=FIXED + timedelta(hours=2))
        self.assertEqual(result["status"], "stale")
        self.assertTrue(result["warnings"])

    def test_discard_invalid_ohlc_and_reject_wrong_market(self):
        payload = fixture()
        payload["values"][1]["high"] = "0"
        rows = clean_completed_candles(payload, "EUR/USD", "15min", FIXED)
        self.assertEqual(len(rows), 99)
        with self.assertRaises(IntradayProviderError):
            clean_completed_candles(payload, "GBP/USD", "15min", FIXED)

    def test_avoid_incomplete_data(self):
        with self.assertRaises(IntradayProviderError):
            clean_completed_candles(fixture(count=25), "EUR/USD", "15min", FIXED)

    def test_hourly_supported(self):
        rows = clean_completed_candles(fixture(interval="1h"), "EUR/USD", "1h", FIXED)
        result = analyze_candles(rows, "EUR/USD", "1h", now=FIXED)
        self.assertEqual(result["status"], "current")
        self.assertEqual(result["interval"], "1h")

    def test_no_arbitrary_symbol_or_interval(self):
        with self.assertRaises(ValueError):
            clean_completed_candles(fixture(), "EUR/ZAR", "15min", FIXED)
        with self.assertRaises(ValueError):
            clean_completed_candles(fixture(), "EUR/USD", "1min", FIXED)


class IntradayGateAndViewTests(SimpleTestCase):
    def setUp(self):
        cache.clear()

    @override_settings(TRADE90_INTRADAY_PUBLIC_LICENSED=False)
    @patch.dict(os.environ, {"TWELVEDATA_API_KEY": "test-key"})
    @patch("terminal.intraday.provider_payload")
    def test_unlicensed_never_fetches(self, upstream):
        self.assertFalse(enabled())
        result = get_intraday("EUR/USD", "15min")
        self.assertEqual(result["status"], "not_configured")
        upstream.assert_not_called()

    @override_settings(TRADE90_INTRADAY_PUBLIC_LICENSED=True)
    @patch.dict(os.environ, {"TWELVEDATA_API_KEY": ""})
    def test_missing_key_disables_public_endpoint(self):
        result = self.client.get(reverse("market-intraday"), {"symbol": "EUR/USD"})
        self.assertEqual(result.status_code, 503)
        self.assertEqual(result.json()["status"], "not_configured")

    @override_settings(TRADE90_INTRADAY_PUBLIC_LICENSED=True)
    @patch.dict(os.environ, {"TWELVEDATA_API_KEY": "test-key"})
    @patch("terminal.intraday.provider_payload")
    def test_data_endpoint_with_fixture_and_cached_result(self, upstream):
        # Construct fixture relative to runtime clock so no test-live leakage.
        now = datetime.now(timezone.utc)
        upstream.return_value = fixture(now=now)
        first = self.client.get(reverse("market-intraday"), {"symbol": "EUR/USD", "interval": "15min"})
        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.json()["status"], "current")
        self.assertEqual(first.json()["provider"], "Twelve Data")
        self.assertEqual(first["Cache-Control"], "no-store")
        second = self.client.get(reverse("market-intraday"), {"symbol": "EUR/USD", "interval": "15min"})
        self.assertEqual(second.status_code, 200)
        upstream.assert_called_once()

    @override_settings(TRADE90_INTRADAY_PUBLIC_LICENSED=True)
    @patch.dict(os.environ, {"TWELVEDATA_API_KEY": "test-key"})
    @patch("terminal.intraday.provider_payload", side_effect=IntradayProviderError("upstream failure"))
    def test_upstream_failure_never_falls_back_to_old_price(self, upstream):
        result = self.client.get(reverse("market-intraday"), {"symbol": "EUR/USD"})
        self.assertEqual(result.status_code, 503)
        self.assertEqual(result.json()["status"], "unavailable")
        self.assertNotIn("last_completed_close", result.json())

    def test_reject_unknown_interval_before_market_network(self):
        result = self.client.get(reverse("market-intraday"), {"symbol": "EUR/USD", "interval": "2min"})
        self.assertEqual(result.status_code, 400)

    def test_page_has_clear_license_limited_panel(self):
        result = self.client.get(reverse("market-intelligence"))
        self.assertContains(result, "Intraday market structure")
        self.assertContains(result, "/market-intelligence/intraday.json")
        self.assertContains(result, "licensed provider access required")
