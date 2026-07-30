from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase


class AdminBootstrapTests(TestCase):
    def test_skips_without_deployment_credentials(self):
        output = StringIO()
        with patch.dict(
            "os.environ",
            {"DJANGO_SUPERUSER_USERNAME": "", "DJANGO_SUPERUSER_PASSWORD": ""},
            clear=False,
        ):
            call_command("bootstrap_admin", stdout=output)
        self.assertIn("skipped", output.getvalue().lower())
        self.assertFalse(get_user_model().objects.filter(is_superuser=True).exists())

    def test_creates_admin_once_without_resetting_password(self):
        first = {
            "DJANGO_SUPERUSER_USERNAME": "trade90-admin",
            "DJANGO_SUPERUSER_PASSWORD": "first-deployment-password",
        }
        with patch.dict("os.environ", first, clear=False):
            call_command("bootstrap_admin", stdout=StringIO())

        user = get_user_model().objects.get(username="trade90-admin")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("first-deployment-password"))

        second = {**first, "DJANGO_SUPERUSER_PASSWORD": "replacement-password"}
        with patch.dict("os.environ", second, clear=False):
            call_command("bootstrap_admin", stdout=StringIO())
        user.refresh_from_db()
        self.assertTrue(user.check_password("first-deployment-password"))
        self.assertFalse(user.check_password("replacement-password"))
