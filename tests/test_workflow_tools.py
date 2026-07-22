import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("url", "marker"),
    [
        ("/today/", "Daily Risk Budget"),
        ("/journal/", "Log a Trade"),
        ("/tools/trading-plan-builder/", "6 sections written"),
    ],
)
def test_workflow_routes_preserve_legacy_contract(client, url, marker):
    response = client.get(url)
    assert response.status_code == 200
    body = response.content.decode()
    assert marker in body
    assert "workflow-tools.js" in body


@pytest.mark.django_db
def test_workflow_pages_have_metadata_and_storage_disclosure(client):
    for url in ("/today/", "/journal/", "/tools/trading-plan-builder/"):
        body = client.get(url).content.decode()
        assert '<link rel="canonical"' in body
    assert "Stored only in this browser" in client.get("/journal/").content.decode()
    assert "Stored only in this browser" in client.get("/tools/trading-plan-builder/").content.decode()
