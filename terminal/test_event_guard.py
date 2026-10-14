from datetime import datetime, timezone
from unittest.mock import patch

from django.test import SimpleTestCase

from .event_guard import parse_official_ical, recent_high_impact
from .intelligence import build_intelligence
from .test_intelligence import example_snapshot


BLS_EVENTS = {
    "source_status": "BLS CPI verified test schedule",
    "events": [{
        "name": "Consumer Price Index",
        "scheduled_at": "2026-10-14T12:30:00+00:00",
        "url": "https://www.bls.gov/schedule/news_release/cpi.htm",
        "source": "Bureau of Labor Statistics"
    }],
}


class MacroEventGuardTests(SimpleTestCase):
    def test_ical_parses_ny_timezone_and_high_impact_only(self):
        text = """BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART;TZID=America/New_York:20261014T083000
SUMMARY:Consumer Price Index
END:VEVENT
BEGIN:VEVENT
DTSTART:20261015T123000Z
SUMMARY:Producer Price Index
END:VEVENT
BEGIN:VEVENT
DTSTART:20261014T120000Z
SUMMARY:Administrative News
END:VEVENT
END:VCALENDAR"""
        events = parse_official_ical(text)
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["scheduled_at"], "2026-10-14T12:30:00+00:00")

    @patch("terminal.event_guard.get_bls_scheduled", return_value=BLS_EVENTS)
    def test_pre_release_flag_protects_prior_forecast(self, calendar):
        now = datetime(2026, 10, 14, 11, 30, tzinfo=timezone.utc)
        result = recent_high_impact(now)
        self.assertEqual(result["status"], "upcoming")
        with patch("terminal.intelligence.recent_high_impact", return_value=result):
            published = build_intelligence(example_snapshot(), now=now)
        gold = published["markets"][0]
        self.assertTrue(gold["pre_event_snapshot"])
        self.assertEqual(gold["current_direction"], "Not established")
        self.assertEqual(gold["published_bias_use"], "historical_only")

    @patch("terminal.event_guard.get_bls_scheduled", return_value=BLS_EVENTS)
    def test_post_release_primary_source_not_a_price_signal(self, calendar):
        now = datetime(2026, 10, 14, 13, 0, tzinfo=timezone.utc)
        event = recent_high_impact(now)
        self.assertEqual(event["status"], "released_or_due")
        self.assertEqual(event["official_release"]["headline_yoy_pct"], 3.7)
        self.assertEqual(event["official_release"]["core_mom_pct"], 0.3)
        self.assertNotIn("gold", event["message"].lower())
        with patch("terminal.intelligence.recent_high_impact", return_value=event):
            result = build_intelligence(example_snapshot(), now=now)
        gold = result["markets"][0]
        self.assertTrue(gold["pre_event_snapshot"])
        self.assertTrue(any("NOT been recalculated" in w for w in gold["warnings"]))
        self.assertTrue(gold["score_bias_conflict"])
        self.assertEqual(gold["current_direction"], "Not established")
        self.assertEqual(result["high_impact"]["name"], "Consumer Price Index")

    @patch("terminal.event_guard.get_bls_scheduled", return_value=BLS_EVENTS)
    def test_event_expires_and_does_not_fake_upcoming(self, calendar):
        now = datetime(2026, 10, 17, 13, tzinfo=timezone.utc)
        event = recent_high_impact(now)
        self.assertEqual(event["status"], "unknown")
        self.assertIn("NOT cleared", event["message"])

    @patch("terminal.intelligence.recent_high_impact", return_value={"status":"unknown"})
    def test_no_event_still_cannot_claim_live_trading_bias(self, context):
        result = build_intelligence(example_snapshot(), now=datetime(2026, 10, 13, 23, 50, tzinfo=timezone.utc))
        gold = result["markets"][0]
        self.assertEqual(gold["current_direction"], "Not established")
        self.assertEqual(gold["published_bias_use"], "historical_only")
        self.assertIsNone(gold["high_impact_event"])
