from django.shortcuts import render

from .models import ContentPage


FEATURED_SOURCE_PATHS = [
    "articles/psychology/why-traders-fail.md",
    "articles/risk-management/risk-of-ruin.md",
    "articles/trading-plans/how-to-build-a-trading-plan.md",
    "articles/prop-firms/prop-firm-rules-explained.md",
    "articles/performance/trading-journal-guide.md",
    "articles/psychology/revenge-trading.md",
]


def home(request):
    pages = {page.source_path: page for page in ContentPage.objects.filter(source_path__in=FEATURED_SOURCE_PATHS).live()}
    featured = [pages[path] for path in FEATURED_SOURCE_PATHS if path in pages]
    return render(request, "website/home.html", {"featured": featured})
