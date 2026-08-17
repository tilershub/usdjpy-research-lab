from pathlib import Path

import yaml
from django.contrib.staticfiles import finders
from django.test import TestCase, override_settings
from django.urls import reverse

from website.middleware import HEALTH_PATH


ROOT = Path(__file__).resolve().parents[1]


class DeploymentReadinessTests(TestCase):
    def test_health_check_reaches_database(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertEqual(response["Cache-Control"], "no-store")

    def test_health_check_path_matches_blueprint_and_middleware(self):
        blueprint = yaml.safe_load((ROOT / "render.yaml").read_text(encoding="utf-8"))
        self.assertEqual(reverse("health"), blueprint["services"][0]["healthCheckPath"])
        self.assertEqual(reverse("health"), HEALTH_PATH)

    @override_settings(SECURE_SSL_REDIRECT=True)
    def test_health_check_survives_probe_without_forwarded_proto(self):
        """Render probes over plain HTTP; a 301 would fail the deploy."""
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    @override_settings(ALLOWED_HOSTS=["trade90.example"])
    def test_health_check_survives_probe_from_unlisted_host(self):
        """Render probes the instance directly, so the Host is not the public one."""
        response = self.client.get(reverse("health"), headers={"host": "10.0.0.5"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    @override_settings(ALLOWED_HOSTS=["trade90.example"])
    def test_unlisted_host_is_still_rejected_off_the_health_path(self):
        response = self.client.get("/", headers={"host": "10.0.0.5"})
        self.assertEqual(response.status_code, 400)

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

    def test_base_template_static_assets_exist(self):
        for asset in (
            "images/favicon.svg",
            "images/og-image.png",
            "css/trade90.css",
            "css/workflow-tools.css",
            "css/article.css",
            "css/calculators.css",
            "js/site.js",
        ):
            self.assertIsNotNone(finders.find(asset), asset)

    def test_market_refresh_workflow_is_valid_yaml(self):
        workflow = yaml.safe_load(
            (ROOT / ".github" / "workflows" / "publish-terminal-snapshot.yml").read_text(encoding="utf-8")
        )
        self.assertIn("jobs", workflow)
        self.assertIn("snapshot", workflow["jobs"])
