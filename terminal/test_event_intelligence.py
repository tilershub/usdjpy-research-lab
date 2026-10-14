from datetime import datetime, timezone
from unittest.mock import patch

from django.core.cache import cache
from django.test import SimpleTestCase
from django.urls import reverse

from .event_intelligence import (
    NewsDiscoveryError, extract_articles, event_evidence, TRACKS,
)


NOW = datetime(2026, 10, 14, 13, 15, tzinfo=timezone.utc)
RESULTS = {
    "articles": [
        {
            "url": "https://www.reuters.com/world/middle-east/sample-coverage",
            "title": "Oil supply risk rises after strikes on Saudi Aramco facilities",
            "seendate": "20261014T125000Z",
        },
        {
            "url": "https://apnews.com/article/middle-east-houthi-saudi",
            "title": "Houthis threaten Saudi sites as fighting escalates",
            "seendate": "20261014T123000Z",
        },
        {
            "url": "https://www.reuters.com/world/middle-east/duplicate",
            "title": "Oil supply risk rises after strikes on Saudi Aramco facilities",
            "seendate": "20261014T125000Z",
        },
        {
            "url": "http://insecure.example.com/rumour",
            "title": "Rumour about commodity and currency prices",
            "seendate": "20261014T124500Z",
        },
        {
            "url": "https://random-blog.invalid/rumour",
            "title": "Unverified headline with fresh market claim",
            "seendate": "20261014T125000Z",
        },
        {
            "url": "https://www.bbc.com/news/old",
            "title": "Old macro story that should not be displayed as new",
            "seendate": "20261001T125000Z",
        },
    ]
}


class EventDiscoveryTests(SimpleTestCase):
    def setUp(self):
        cache.clear()

    def test_accepts_only_recent_allowlisted_publishers(self):
        items = extract_articles(RESULTS, now=NOW)
        self.assertEqual(len(items), 2)
        self.assertEqual({x["publisher"] for x in items}, {"www.reuters.com", "apnews.com"})
        self.assertTrue(all(x["url"].startswith("https://") for x in items))
        self.assertEqual(items[0]["source_type"], "third-party published report")

    @patch("terminal.event_intelligence._discover", return_value=RESULTS)
    def test_topics_both_separate_reports_from_market_reaction(self, fetch):
        data = event_evidence(now=NOW)
        self.assertEqual(data["status"], "ok")
        self.assertEqual(len(data["topics"]), len(TRACKS))
        self.assertEqual(data["topics"][0]["status"], "reports_found")
        self.assertEqual(data["topics"][0]["market_reaction"]["status"], "not_measured")
        self.assertEqual(data["topics"][0]["publisher_count"], 2)
        self.assertNotIn("bullish", str(data).lower())
        self.assertNotIn("bearish", str(data).lower())
        again = event_evidence(now=NOW)
        self.assertEqual(again, data)
        self.assertEqual(fetch.call_count, len(TRACKS))

    @patch("terminal.event_intelligence._discover", side_effect=NewsDiscoveryError("unavailable"))
    def test_news_upstream_unavailable_without_invented_claims(self, upstream):
        data = event_evidence(now=NOW)
        self.assertEqual(data["status"], "limited")
        self.assertTrue(all(t["status"] == "source_unavailable" for t in data["topics"]))
        self.assertTrue(all(not t["reports"] for t in data["topics"]))
        self.assertTrue(all(t["market_reaction"]["status"] == "not_measured" for t in data["topics"]))

    @patch("terminal.views.event_evidence")
    def test_page_endpoint_reports_checked_at_and_no_fake_quotes(self, engine):
        engine.return_value = event_evidence(now=NOW)
        response = self.client.get(reverse("market-events"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["news_index"], "GDELT Project DOC 2.0")
        self.assertNotIn("gold_price", response.json())
