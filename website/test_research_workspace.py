from django.test import SimpleTestCase
from django.urls import reverse


class ResearchWorkspaceTests(SimpleTestCase):
    def test_route_renders_research_workspace(self):
        response = self.client.get(reverse("research-workspace"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Verified research snapshot")
        self.assertContains(response, "Write a quick plan")
        self.assertContains(response, "Personal notes and plans")

    def test_snapshot_is_loaded_from_existing_verified_endpoint(self):
        response = self.client.get(reverse("research-workspace"))
        self.assertContains(response, "/tools/fx-research-terminal/snapshot.json")
        self.assertContains(response, "schema_version!==1")

    def test_workspace_is_linked_from_today(self):
        response = self.client.get(reverse("today"))
        self.assertContains(response, 'href="/research-workspace/"')
