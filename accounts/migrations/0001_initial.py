import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [("auth", "0012_alter_user_first_name_max_length")]
    operations = [migrations.CreateModel(name="TradingWorkspace", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("journal", models.JSONField(blank=True, default=list)), ("plan", models.JSONField(blank=True, default=dict)),
        ("daily_checklists", models.JSONField(blank=True, default=dict)), ("watchlist", models.JSONField(blank=True, default=list)),
        ("alert_preferences", models.JSONField(blank=True, default=dict)), ("updated_at", models.DateTimeField(auto_now=True)),
        ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="trading_workspace", to=settings.AUTH_USER_MODEL)),
    ], options={"ordering": ["-updated_at"]})]
