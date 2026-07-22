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
    assert len(payload["pairs"]) == 7
    required = {"symbol", "price", "score", "bias", "probabilities", "quality", "market", "model"}
    assert all(required <= set(pair) for pair in payload["pairs"])
