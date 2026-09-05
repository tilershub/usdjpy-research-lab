import json
from datetime import timedelta
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

    def _file_payload(self, generated_at, marker):
        return {
            "schema_version": 1,
            "generated_at": generated_at.isoformat(),
            "pairs": [{"symbol": marker} for _ in range(9)],
        }

    def test_newer_committed_snapshot_outranks_a_stale_database_row(self):
        """A one-off manual publish must not freeze the terminal on old prices."""
        stale = timezone.now() - timedelta(days=9)
        MarketSnapshot.objects.create(
            schema_version=1,
            generated_at=stale,
            payload={"schema_version": 1, "generated_at": stale.isoformat(), "pairs": [{"symbol": "STALE-DB"}]},
        )
        with TemporaryDirectory() as directory:
            path = Path(directory) / "terminal-snapshot.json"
            path.write_text(json.dumps(self._file_payload(timezone.now(), "FRESH-FILE")), encoding="utf-8")
            with override_settings(TERMINAL_SNAPSHOT_PATH=path):
                response = self.client.get(reverse("terminal:snapshot"))
        self.assertEqual(response.json()["pairs"][0]["symbol"], "FRESH-FILE")

    def test_fresher_database_snapshot_still_wins(self):
        fresh = timezone.now()
        MarketSnapshot.objects.create(
            schema_version=1,
            generated_at=fresh,
            payload={"schema_version": 1, "generated_at": fresh.isoformat(), "pairs": [{"symbol": "FRESH-DB"}]},
        )
        with TemporaryDirectory() as directory:
            path = Path(directory) / "terminal-snapshot.json"
            older = timezone.now() - timedelta(days=3)
            path.write_text(json.dumps(self._file_payload(older, "OLD-FILE")), encoding="utf-8")
            with override_settings(TERMINAL_SNAPSHOT_PATH=path):
                response = self.client.get(reverse("terminal:snapshot"))
        self.assertEqual(response.json()["pairs"][0]["symbol"], "FRESH-DB")


class PriceBasisDisclosureTests(TestCase):
    def test_gold_is_quoted_spot_with_a_declared_futures_fallback(self):
        from trade90_model import PAIR_CONFIGS

        gold = PAIR_CONFIGS["XAU/USD"]
        self.assertEqual(gold.ticker, "XAUUSD=X")
        self.assertEqual(gold.price_basis, "Spot")
        self.assertEqual(gold.fallback_ticker, "GC=F")
        self.assertEqual(gold.fallback_basis, "COMEX futures")
        self.assertIn("will not match a spot broker quote", gold.fallback_note)

    def test_non_spot_markets_still_declare_their_basis(self):
        from trade90_model import PAIR_CONFIGS

        self.assertEqual(PAIR_CONFIGS["BTC/USD"].price_basis, "Composite")

    def test_fx_majors_are_spot_quoted(self):
        from trade90_model import PAIR_CONFIGS

        for symbol in ("EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "USD/CAD", "AUD/USD", "NZD/USD"):
            self.assertEqual(PAIR_CONFIGS[symbol].price_basis, "Spot", symbol)

    def test_terminal_script_renders_the_basis_and_note(self):
        script = (Path(__file__).resolve().parents[1] / "static" / "js" / "terminal.js").read_text(encoding="utf-8")
        self.assertIn("price_basis", script)
        self.assertIn("price_note", script)


class SourceHealthTests(TestCase):
    def test_snapshot_reports_health_for_every_configured_source(self):
        payload = json.loads((Path(__file__).resolve().parents[1] / "public" / "terminal-snapshot.json").read_text(encoding="utf-8"))
        sources = payload["sources"]
        for name in ("calendar", "positioning", "policy_expectations", "policy_calendar", "news"):
            self.assertIn(name, sources, name)
            self.assertIn("provider", sources[name], name)

    def test_terminal_page_exposes_the_source_health_region(self):
        response = self.client.get(reverse("terminal:terminal"))
        self.assertContains(response, 'id="source-health"')

    def test_script_marks_a_failing_source_rather_than_hiding_it(self):
        script = (Path(__file__).resolve().parents[1] / "static" / "js" / "terminal.js").read_text(encoding="utf-8")
        self.assertIn("source-down", script)
        self.assertIn("renderSourceHealth", script)
