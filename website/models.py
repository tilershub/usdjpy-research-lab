from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class ContentPage(Page):
    summary = models.TextField(blank=True)
    body = RichTextField(blank=True)
    published_on = models.DateField(blank=True, null=True)
    reading_time = models.PositiveSmallIntegerField(default=5)
    updated_on = models.DateField(blank=True, null=True)
    author = models.CharField(max_length=100, default="TRADE90")
    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    source_path = models.CharField(max_length=255, blank=True, unique=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
        FieldPanel("body"),
        FieldPanel("published_on"),
        FieldPanel("reading_time"),
        FieldPanel("updated_on"),
        FieldPanel("author"),
        FieldPanel("tags"),
    ]

    promote_panels = Page.promote_panels

    class Meta:
        verbose_name = "TRADE90 content page"
