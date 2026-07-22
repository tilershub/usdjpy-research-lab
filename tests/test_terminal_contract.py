from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from terminal.models import MarketSnapshot


class TerminalContractTests(TestCase):
    def test_terminal_renders_without_snapshot(self):
        response = self.client.get(reverse("terminal:terminal"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No forecast values are fabricated")

    def test_snapshot_api_fails_honestly_without_data(self):
        response = self.client.get(reverse("terminal:snapshot"))
        self.assertEqual(response.status_code, 503)

    def test_snapshot_api_returns_latest_payload(self):
        payload = {"schema_version": 1, "generated_at": timezone.now().isoformat(), "pairs": [{"symbol": "BTC/USD"}]}
        MarketSnapshot.objects.create(schema_version=1, generated_at=timezone.now(), payload=payload)
        response = self.client.get(reverse("terminal:snapshot"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pairs"][0]["symbol"], "BTC/USD")
