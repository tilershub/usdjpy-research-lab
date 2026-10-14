from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from django.test import SimpleTestCase
from django.urls import reverse

from .live_quotes import QuoteUnavailable, fetch_quote


class IndicativeMarketQuoteTests(SimpleTestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 14, 4, 0, 0, tzinfo=timezone.utc)

    @patch("terminal.live_quotes._get_json")
    def test_swissquote_uses_dealer_timestamp_and_actual_bid_ask(self, get_json):
        get_json.return_value = [{
            "topo": {"platform": "SwissquoteCapitalMarkets"},
            "spreadProfilePrices": [
                {"spreadProfile": "premium", "bid": "1.11711", "ask": "1.11716"},
            ],
            "ts": int((self.now - timedelta(seconds=30)).timestamp() * 1000),
        }]
        result = fetch_quote("EUR/USD", now=self.now)
        self.assertEqual(result["status"], "current")
        self.assertEqual(result["bid"], 1.11711)
        self.assertEqual(result["ask"], 1.11716)
        self.assertEqual(result["age_seconds"], 30)
        self.assertIn("Swissquote", result["provider"])

    @patch("terminal.live_quotes._get_json")
    def test_quote_stale_on_weekend_or_old_timestamp(self, get_json):
        get_json.return_value = [{
            "topo": {"platform": "AT"}, "spreadProfilePrices": [{"bid": 4300, "ask": 4301}],
            "ts": int((self.now - timedelta(minutes=10)).timestamp() * 1000),
        }]
        result = fetch_quote("XAU/USD", now=self.now)
        self.assertEqual(result["status"], "stale")
        self.assertIsNone(result["mid"])
        self.assertIsNone(result["bid"])

    @patch("terminal.live_quotes._get_json")
    def test_coinbase_trade_time_and_spot_basis(self, get_json):
        get_json.return_value = {
            "bid": "78000", "ask": "78001", "time": (self.now - timedelta(seconds=10)).isoformat(),
        }
        result = fetch_quote("BTC/USD", now=self.now)
        self.assertEqual(result["status"], "current")
        self.assertEqual(result["mid"], 78000.5)
        self.assertIn("Coinbase", result["provider"])
        self.assertIn("spot", result["basis"])

    @patch("terminal.live_quotes._get_json")
    def test_malformed_spread_no_fake_quote(self, get_json):
        get_json.return_value = [{"ts": int(self.now.timestamp() * 1000),
                                  "spreadProfilePrices": [{"bid": 1.2, "ask": 1.1}]}]
        result = fetch_quote("GBP/USD", now=self.now)
        self.assertEqual(result["status"], "unavailable")
        self.assertIsNone(result["mid"])

    @patch("terminal.live_quotes._get_json")
    def test_missing_timestamp_not_treated_as_live(self, get_json):
        get_json.return_value = [{"spreadProfilePrices": [{"bid": 4300, "ask": 4301}]}]
        self.assertEqual(fetch_quote("XAU/USD", now=self.now)["status"], "unavailable")

    @patch("terminal.live_quotes._get_json", side_effect=QuoteUnavailable("timeout"))
    def test_provider_timeout_no_fabricated_fallback(self, get_json):
        r = fetch_quote("EUR/USD", now=self.now)
        self.assertEqual(r["status"], "unavailable")
        self.assertIsNone(r["observed_at"])

    def test_unsupported_symbol_is_rejected_without_network(self):
        result = fetch_quote("GBP/ZAR", now=self.now)
        self.assertEqual(result["status"], "unavailable")

    @patch("terminal.views.cached_quote")
    def test_public_quote_route(self, cached):
        cached.return_value = {
            "status": "current", "symbol": "EUR/USD",
            "bid": 1.2, "ask": 1.2001, "mid": 1.20005, "observed_at": self.now.isoformat(),
        }
        r = self.client.get(reverse("market-quote"), {"symbol": "EUR/USD"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Cache-Control"], "no-store")
        self.assertEqual(r.json()["mid"], 1.20005)

    @patch("terminal.views.cached_quote")
    def test_quote_route_rejects_unavailable(self, cached):
        cached.return_value = {"status": "stale", "symbol": "XAU/USD", "bid": None, "ask": None, "mid": None}
        r = self.client.get(reverse("market-quote"), {"symbol": "XAU/USD"})
        self.assertEqual(r.status_code, 503)
        self.assertIsNone(r.json()["mid"])
