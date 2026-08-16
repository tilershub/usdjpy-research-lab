import json
from pathlib import Path

from publish_snapshot import clean


def test_snapshot_clean_rejects_non_finite_values():
    assert clean(float("nan")) is None
    assert clean(float("inf")) is None


def test_snapshot_contract_if_present():
    path = Path("public/terminal-snapshot.json")
    if not path.exists():
        return
    payload = json.loads(path.read_text())
    assert payload["schema_version"] == 1
    assert len(payload["pairs"]) == 9
    required = {"symbol", "price", "score", "bias", "probabilities", "quality", "market", "model"}
    assert all(required <= set(pair) for pair in payload["pairs"])


def test_snapshot_contains_native_terminal_layers_if_present():
    path = Path("public/terminal-snapshot.json")
    if not path.exists():
        return
    payload = json.loads(path.read_text())
    optional_layers = {"history", "events", "positioning", "validation"}
    enriched = [pair for pair in payload["pairs"] if optional_layers <= set(pair)]
    if enriched:
        assert all(pair["history"] for pair in enriched)
        assert all("audit" in pair["model"] for pair in enriched)
