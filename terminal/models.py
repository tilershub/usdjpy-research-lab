from django.db import models


class MarketSnapshot(models.Model):
    schema_version = models.PositiveSmallIntegerField(default=1)
    generated_at = models.DateTimeField(db_index=True)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-generated_at"]

    def __str__(self):
        return f"Snapshot {self.generated_at:%Y-%m-%d %H:%M UTC}"
