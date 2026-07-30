from pathlib import Path

import yaml
from django.test import TestCase
from django.urls import reverse


ROOT = Path(__file__).resolve().parents[1]


class DeploymentReadinessTests(TestCase):
    def test_health_check_reaches_database(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertEqual(response["Cache-Control"], "no-store")

    def test_render_blueprint_is_free_web_only_and_singapore_based(self):
        blueprint = yaml.safe_load((ROOT / "render.yaml").read_text(encoding="utf-8"))
        services = blueprint["services"]
        self.assertEqual(len(services), 1)
        service = services[0]
        self.assertEqual(service["type"], "web")
        self.assertEqual(service["plan"], "free")
        self.assertEqual(service["region"], "singapore")
        self.assertEqual(service["healthCheckPath"], "/health/")
        self.assertNotIn("cron", {item["type"] for item in services})

    def test_render_build_bootstraps_content_and_admin(self):
        script = (ROOT / "render-build.sh").read_text(encoding="utf-8")
        for command in (
            "pip install -r requirements-web.txt",
            "manage.py collectstatic --noinput",
            "manage.py migrate --noinput",
            "manage.py import_astro_content",
            "manage.py bootstrap_admin",
        ):
            self.assertIn(command, script)

    def test_market_refresh_workflow_is_valid_yaml(self):
        workflow = yaml.safe_load(
            (ROOT / ".github" / "workflows" / "publish-terminal-snapshot.yml").read_text(encoding="utf-8")
        )
        self.assertIn("jobs", workflow)
        self.assertIn("snapshot", workflow["jobs"])
