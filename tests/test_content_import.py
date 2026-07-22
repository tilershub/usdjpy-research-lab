from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from django.core.management import call_command
from django.test import TestCase


class ContentImportTests(TestCase):
    def test_parser_rejects_incomplete_library(self):
        with TemporaryDirectory() as directory:
            with self.assertRaisesMessage(ValueError, "Expected 38"):
                call_command("import_astro_content", source=directory, stdout=StringIO())

    def test_committed_source_has_complete_library(self):
        source = Path(__file__).resolve().parents[1] / "content_source"
        self.assertEqual(len(list(source.glob("**/*.md"))), 38)
