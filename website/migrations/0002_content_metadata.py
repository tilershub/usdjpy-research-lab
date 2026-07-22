from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("website", "0001_initial")]
    operations = [
        migrations.AddField(model_name="contentpage", name="updated_on", field=models.DateField(blank=True, null=True)),
        migrations.AddField(model_name="contentpage", name="author", field=models.CharField(default="TRADE90", max_length=100)),
        migrations.AddField(model_name="contentpage", name="tags", field=models.JSONField(blank=True, default=list)),
        migrations.AddField(model_name="contentpage", name="metadata", field=models.JSONField(blank=True, default=dict)),
    ]
