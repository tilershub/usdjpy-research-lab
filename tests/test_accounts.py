import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import TradingWorkspace


class AccountSyncTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="trader@example.com", email="trader@example.com", password="safe-test-password")

    def test_account_routes_require_login(self):
        response = self.client.get(reverse("account-dashboard"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('account-dashboard')}")
        self.assertEqual(self.client.get(reverse("workspace-api")).status_code, 302)

    def test_signup_uses_email_as_identity(self):
        response = self.client.post(reverse("account-signup"), {"email":"new@example.com", "password1":"a-strong-test-password", "password2":"a-strong-test-password"})
        self.assertRedirects(response, reverse("account-dashboard"))
        self.assertTrue(get_user_model().objects.filter(username="new@example.com").exists())

    def test_workspace_isolated_and_round_trips(self):
        self.client.force_login(self.user)
        payload = {"journal":[{"id":1,"symbol":"XAUUSD"}], "plan":{"risk":"0.5%"}, "watchlist":["XAUUSD","BTCUSD"], "alert_preferences":{"enabled":False}, "daily_checklists":{"2026-07-22":["calendar"]}}
        response = self.client.put(reverse("workspace-api"), data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = self.client.get(reverse("workspace-api")).json()
        for key, value in payload.items():
            self.assertEqual(data[key], value)
        self.assertEqual(TradingWorkspace.objects.count(), 1)

    def test_rejects_bad_shape_and_anonymous_writes(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.put(reverse("workspace-api"), data=json.dumps({"journal":{}}), content_type="application/json").status_code, 400)
        self.client.logout()
        self.assertEqual(self.client.put(reverse("workspace-api"), data="{}", content_type="application/json").status_code, 302)
