from datetime import date
from pathlib import Path

import markdown
import yaml
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from wagtail.models import Site

from website.models import ContentPage


HUB_TITLES = {"psychology": "Trading Psychology", "risk-management": "Risk Management", "trading-plans": "Trading Plans", "prop-firms": "Prop Firms", "performance": "Performance"}
STATIC_PAGES = {
    "about": ("About TRADE90", "Education, professional tools, and evidence-led market research for disciplined traders.", "<h2>Built for disciplined traders</h2><p>TRADE90 helps funded and independent traders build repeatable processes around risk, psychology, planning, and performance.</p>"),
    "contact": ("Contact TRADE90", "Contact the TRADE90 editorial and platform team.", "<h2>Contact</h2><p>Use the official TRADE90 channels for platform, editorial, or partnership enquiries.</p>"),
    "disclaimer": ("Risk Disclaimer", "Important trading-risk and educational-use disclosure.", "<h2>Educational use only</h2><p>Trading involves substantial risk of loss and is not suitable for every investor. TRADE90 does not provide financial, investment, or trading advice.</p>"),
    "privacy": ("Privacy Policy", "How TRADE90 handles site and account information.", "<h2>Privacy</h2><p>TRADE90 collects only the information required to operate, secure, and improve the platform. Account and alert features will provide specific controls when enabled.</p>"),
    "editorial-policy": ("Editorial Policy", "TRADE90 research, corrections, sourcing, and independence standards.", "<h2>Evidence before opinion</h2><p>TRADE90 separates observable facts, model interpretation, probabilistic forecasts, and trade-planning context. Material corrections are made transparently.</p>"),
}


def parse_document(path):
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        raise ValueError(f"Missing YAML front matter: {path}")
    _, front_matter, body = raw.split("---", 2)
    return yaml.safe_load(front_matter) or {}, body.strip()


def as_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


class Command(BaseCommand):
    help = "Idempotently import the current Astro Markdown library into Wagtail."

    def add_arguments(self, parser):
        parser.add_argument("--source", default=str(settings.BASE_DIR / "content_source"))

    def handle(self, *args, **options):
        source = Path(options["source"])
        documents = sorted(source.glob("articles/*/*.md")) + sorted(source.glob("posts/*.md"))
        if len(documents) != 38:
            raise ValueError(f"Expected 38 source documents, found {len(documents)}")
        root = Site.objects.get(is_default_site=True).root_page.specific
        parents = {"blog": self.ensure_parent(root, "blog", "Blog")}
        for slug, title in HUB_TITLES.items():
            parents[slug] = self.ensure_parent(root, slug, title)
        for slug, (title, summary, body) in STATIC_PAGES.items():
            self.ensure_static_page(root, slug, title, summary, body)
        created = updated = 0
        for path in documents:
            data, body = parse_document(path)
            is_article = path.parts[-3] == "articles"
            section = data["hub"] if is_article else "blog"
            source_key = str(path.relative_to(source))
            values = {
                "title": data["title"], "slug": slugify(path.stem),
                "summary": data.get("description") or data.get("excerpt", ""),
                "body": markdown.markdown(body, extensions=["extra", "sane_lists"]),
                "published_on": as_date(data.get("published_at") or data.get("updated")),
                "updated_on": as_date(data.get("updated_at") or data.get("updated")),
                "reading_time": data.get("reading_time") or 5, "author": data.get("author", "TRADE90"),
                "tags": data.get("tags", [HUB_TITLES.get(section, section)]),
                "metadata": {key: value for key, value in data.items() if key not in {"title", "description", "excerpt", "published_at", "updated_at", "updated", "reading_time", "author", "tags"}},
                "seo_title": data.get("meta_title") or data["title"],
                "search_description": data.get("meta_description") or data.get("description") or data.get("excerpt", ""),
            }
            page = ContentPage.objects.filter(source_path=source_key).first()
            if page is None:
                page = ContentPage(source_path=source_key, **values)
                parents[section].add_child(instance=page)
                created += 1
            else:
                for key, value in values.items():
                    setattr(page, key, value)
                page.save()
                updated += 1
            page.save_revision().publish()
        self.stdout.write(self.style.SUCCESS(f"Imported 38 documents: {created} created, {updated} updated"))

    def ensure_parent(self, root, slug, title):
        existing = root.get_children().filter(slug=slug).first()
        if existing:
            return existing.specific
        page = ContentPage(title=title, slug=slug, summary=f"TRADE90 {title}", source_path=f"section:{slug}")
        root.add_child(instance=page)
        page.save_revision().publish()
        return page

    def ensure_static_page(self, root, slug, title, summary, body):
        source_path = f"static:{slug}"
        page = ContentPage.objects.filter(source_path=source_path).first()
        if page is None:
            existing = root.get_children().filter(slug=slug).first()
            page = existing.specific if existing else ContentPage(title=title, slug=slug, source_path=source_path)
            if not existing:
                root.add_child(instance=page)
        page.title, page.summary, page.body = title, summary, body
        page.seo_title, page.search_description = title, summary
        page.save_revision().publish()
        return page
