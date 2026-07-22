from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):
    initial = True
    dependencies = [("wagtailcore", "0094_alter_page_locale")]
    operations = [migrations.CreateModel(
        name="ContentPage",
        fields=[
            ("page_ptr", models.OneToOneField(auto_created=True, on_delete=models.CASCADE, parent_link=True, primary_key=True, serialize=False, to="wagtailcore.page")),
            ("summary", models.TextField(blank=True)),
            ("body", wagtail.fields.RichTextField(blank=True)),
            ("published_on", models.DateField(blank=True, null=True)),
            ("reading_time", models.PositiveSmallIntegerField(default=5)),
            ("source_path", models.CharField(blank=True, max_length=255, null=True, unique=True)),
        ],
        options={"verbose_name": "TRADE90 content page"},
        bases=("wagtailcore.page",),
    )]
