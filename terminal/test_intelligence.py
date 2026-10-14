from datetime import datetime, timezone
from unittest.mock import patch

from django.test import SimpleTestCase
from django.urls import reverse

from .intelligence import build_intelligence


def example_snapshot():
    return {
        "schema_version": 1,
        "generated_at": "2026-10-13T23:17:00+00:00",
        "sources": {"calendar": {"mode": "unavailable", "provider": "Trading Economics"}},
        "pairs": [{
            "symbol": "XAU/USD", "base": "XAU", "quote": "USD", "asset_class": "Commodity",
            "price": 4183.3, "price_basis": "COMEX futures",
            "price_note": "Futures are different from spot contracts.", "decimals": 2,
            "score": -77.1, "bias": "Bullish", "confidence": "Moderate",
            "probabilities": {"Bullish": 0.4407, "Range/neutral": 0.1696, "Bearish": 0.3897},
            "quality": {"grade": "A", "last_price": "2026-10-13T00:00:00", "stale_inputs": []},
            "market": {"regime": "High volatility", "support20": 4140.7,
                       "resistance20": 4424.9, "atr20": 32.98, "volatility": .17,
                       "driver": "US dollar index"},
            "model": {"thesis": "Gold, yields, dollar, trend.",
                      "audit": [{"name": "Trend", "contribution": -18.1},
                                {"name": "Rate differential", "contribution": -24.5}]},
            "history": [{"date": "2026-10-12", "close": 4190.7},
                        {"date": "2026-10-13", "close": 4183.3}],
            "events": {"risk": {"level": "Unknown"}, "upcoming": []},
            "news": [
                {"currency": "JPY", "headline": "Irrelevant note", "source": "BoJ",
                 "url": "https://example.org/jpy", "published_at": "2026-10-13"},
                {"currency": "USD", "headline": "Federal Reserve release", "source": "Fed",
                 "url": "https://www.federalreserve.gov/pressrelease", "published_at": "2026-10-13"}
            ],
            "positioning": {"available": True, "base": {"date": "2026-10-06", "crowding": "Balanced"}},
            "validation": {"horizons": [{
                "Horizon": "5D", "Model accuracy": .5409, "Majority baseline": .5956,
                "OOS observations": 183
            }]}
        }],
    }


class IntelligenceSummaryTests(SimpleTestCase):
    def test_market_brief_uses_published_data_and_flags_caveats(self):
        result = build_intelligence(example_snapshot(), now=datetime(2026, 10, 14, 1, tzinfo=timezone.utc))
        self.assertEqual(result["status"], "ok")
        market = result["markets"][0]
        self.assertEqual(market["symbol"], "XAU/USD")
        self.assertEqual(market["price"], 4183.3)
        self.assertEqual(market["price_basis"], "COMEX futures")
        self.assertEqual(market["events"]["coverage"], "Unknown — provider unavailable")
        self.assertTrue(market["score_bias_conflict"])
        self.assertLess(market["validation"]["lift_pp"], 0)
        self.assertEqual([n["currency"] for n in market["news"]], ["USD"])
        self.assertEqual(len(market["chart"]), 2)
        self.assertTrue(any("baseline" in w for w in market["warnings"]))
        self.assertTrue(any("COMEX" in w for w in market["warnings"]))

    def test_stale_publication_and_unavailable_source(self):
        old = build_intelligence(example_snapshot(), now=datetime(2026, 10, 18, tzinfo=timezone.utc))
        self.assertTrue(old["markets"][0]["snapshot_old"])
        self.assertTrue(any("36 hours" in w for w in old["markets"][0]["warnings"]))
        self.assertEqual(build_intelligence(None)["status"], "unavailable")

    def test_missing_non_finite_price_is_never_shown_as_a_quote(self):
        source = example_snapshot()
        source["pairs"][0]["price"] = float("nan")
        result = build_intelligence(source)
        self.assertIsNone(result["markets"][0]["price"])


class IntelligenceViewTests(SimpleTestCase):
    def test_research_page_renders(self):
        response = self.client.get(reverse("market-intelligence"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Three scenarios to review")
        self.assertContains(response, "Historical validation")
        self.assertContains(response, "/market-intelligence/data.json")

    @patch("terminal.views._latest", return_value=example_snapshot())
    def test_data_endpoint_returns_research_and_no_store(self, latest):
        response = self.client.get(reverse("market-intelligence-data"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(response.json()["markets"][0]["price_basis"], "COMEX futures")

    @patch("terminal.views._latest", return_value=None)
    def test_missing_publisher_returns_503(self, latest):
        response = self.client.get(reverse("market-intelligence-data"))
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["status"], "unavailable")
