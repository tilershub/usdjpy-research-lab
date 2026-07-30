import json
from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from terminal.models import MarketSnapshot


class TerminalContractTests(TestCase):
    def test_terminal_renders_without_snapshot(self):
        with TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.json"
            with override_settings(TERMINAL_SNAPSHOT_PATH=missing):
                response = self.client.get(reverse("terminal:terminal"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No forecast values are fabricated")
        self.assertContains(response, "Watchlist only")
        self.assertContains(response, "Account &amp; Sync")

    def test_snapshot_api_fails_honestly_without_data(self):
        with TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.json"
            with override_settings(TERMINAL_SNAPSHOT_PATH=missing):
                response = self.client.get(reverse("terminal:snapshot"))
                self.assertEqual(response.status_code, 503)

    def test_snapshot_api_returns_latest_payload(self):
        payload = {"schema_version": 1, "generated_at": timezone.now().isoformat(), "pairs": [{"symbol": "BTC/USD"}]}
        MarketSnapshot.objects.create(schema_version=1, generated_at=timezone.now(), payload=payload)
        response = self.client.get(reverse("terminal:snapshot"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pairs"][0]["symbol"], "BTC/USD")

    def test_snapshot_api_uses_valid_committed_snapshot(self):
        payload = {
            "schema_version": 1,
            "generated_at": timezone.now().isoformat(),
            "pairs": [{"symbol": f"PAIR-{index}"} for index in range(9)],
        }
        with TemporaryDirectory() as directory:
            path = Path(directory) / "terminal-snapshot.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with override_settings(TERMINAL_SNAPSHOT_PATH=path):
                response = self.client.get(reverse("terminal:snapshot"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["pairs"]), 9)
