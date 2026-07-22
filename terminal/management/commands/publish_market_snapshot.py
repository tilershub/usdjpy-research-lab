import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

import publish_snapshot
from terminal.models import MarketSnapshot


class Command(BaseCommand):
    help = "Generate, validate, and persist the latest nine-market research snapshot."

    def handle(self, *args, **options):
        publish_snapshot.main()
        path = Path(publish_snapshot.OUTPUT)
        payload = json.loads(path.read_text(encoding="utf-8"))
        pairs = payload.get("pairs", [])
        if payload.get("schema_version") != 1 or len(pairs) != 9:
            raise ValueError("Refusing to publish a snapshot that does not contain all nine markets")
        generated_at = parse_datetime(payload["generated_at"])
        MarketSnapshot.objects.update_or_create(
            generated_at=generated_at,
            defaults={"schema_version": 1, "payload": payload},
        )
        self.stdout.write(self.style.SUCCESS(f"Published {len(pairs)} markets at {generated_at.isoformat()}"))
