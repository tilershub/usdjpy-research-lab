from django.conf import settings
from django.db import models


class TradingWorkspace(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="trading_workspace")
    journal = models.JSONField(default=list, blank=True)
    plan = models.JSONField(default=dict, blank=True)
    daily_checklists = models.JSONField(default=dict, blank=True)
    watchlist = models.JSONField(default=list, blank=True)
    alert_preferences = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"TRADE90 workspace for {self.user_id}"
