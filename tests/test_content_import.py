from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from django.core.management import call_command
from django.test import TestCase
from wagtail.models import Site
from website.models import ContentPage


class ContentImportTests(TestCase):
    def test_parser_rejects_incomplete_library(self):
        with TemporaryDirectory() as directory:
            with self.assertRaisesMessage(ValueError, "Expected 38"):
                call_command("import_astro_content", source=directory, stdout=StringIO())

    def test_committed_source_has_complete_library(self):
        source = Path(__file__).resolve().parents[1] / "content_source"
        self.assertEqual(len(list(source.glob("**/*.md"))), 38)

    def test_import_creates_design_hubs_static_pages_and_stable_articles(self):
        source = Path(__file__).resolve().parents[1] / "content_source"
        call_command("import_astro_content", source=source, stdout=StringIO())
        root = Site.objects.get(is_default_site=True).root_page
        self.assertTrue(ContentPage.objects.child_of(root).filter(slug="risk-management").exists())
        self.assertTrue(ContentPage.objects.child_of(root).filter(slug="about", source_path="static:about").exists())
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertContains(self.client.get("/"), "Become a Consistently")
        hub = self.client.get("/risk-management/")
        self.assertEqual(hub.status_code, 200)
        self.assertContains(hub, "TRADE90 Learning Hub")
        self.assertContains(hub, 'rel="canonical"')
        self.assertEqual(self.client.get("/about/").status_code, 200)

    def test_import_remains_idempotent_with_static_pages(self):
        source = Path(__file__).resolve().parents[1] / "content_source"
        call_command("import_astro_content", source=source, stdout=StringIO())
        count = ContentPage.objects.count()
        call_command("import_astro_content", source=source, stdout=StringIO())
        self.assertEqual(ContentPage.objects.count(), count)
