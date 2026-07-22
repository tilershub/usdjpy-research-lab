from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from website import views as website_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("cms/", include(wagtailadmin_urls)),
    path("tools/fx-research-terminal/", include("terminal.urls")),
    path("tools/position-size-calculator/", website_views.calculator, {"tool": "position"}),
    path("tools/drawdown-calculator/", website_views.calculator, {"tool": "drawdown"}),
    path("risk-reward-calculator/", website_views.calculator, {"tool": "risk_reward"}),
    path("pip-value-calculator/", website_views.calculator, {"tool": "pip_value"}),
    path("tools/profit-calculator/", website_views.calculator, {"tool": "profit"}),
    path("tools/compounding-calculator/", website_views.calculator, {"tool": "compounding"}),
    path("today/", website_views.today, name="today"),
    path("journal/", website_views.journal, name="journal"),
    path("tools/trading-plan-builder/", website_views.trading_plan, name="trading-plan"),
    path("", website_views.home, name="home"),
    path("", include(wagtail_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
