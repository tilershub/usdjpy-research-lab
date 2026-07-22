from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(
        name="MarketSnapshot",
        fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("schema_version", models.PositiveSmallIntegerField(default=1)),
            ("generated_at", models.DateTimeField(db_index=True)),
            ("payload", models.JSONField()),
            ("created_at", models.DateTimeField(auto_now_add=True)),
        ],
        options={"ordering": ["-generated_at"]},
    )]
