from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class ContentPage(Page):
    summary = models.TextField(blank=True)
    body = RichTextField(blank=True)
    published_on = models.DateField(blank=True, null=True)
    reading_time = models.PositiveSmallIntegerField(default=5)
    source_path = models.CharField(max_length=255, blank=True, unique=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
        FieldPanel("body"),
        FieldPanel("published_on"),
        FieldPanel("reading_time"),
    ]

    promote_panels = Page.promote_panels

    class Meta:
        verbose_name = "TRADE90 content page"
