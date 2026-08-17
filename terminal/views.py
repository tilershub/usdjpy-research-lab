import json
from datetime import timezone as dt_timezone

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import MarketSnapshot


def _committed():
    try:
        payload = json.loads(settings.TERMINAL_SNAPSHOT_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
    if not isinstance(payload, dict):
        return None
    pairs = payload.get("pairs")
    if payload.get("schema_version") != 1 or not isinstance(pairs, list) or len(pairs) != 9:
        return None
    return payload


def _generated_at(payload):
    stamp = parse_datetime(str(payload.get("generated_at", "")))
    if stamp is None:
        return None
    return stamp if timezone.is_aware(stamp) else timezone.make_aware(stamp, dt_timezone.utc)


def _latest():
    """Serve whichever verified snapshot was generated most recently.

    The database is written by the publish command and the committed file is
    refreshed by the scheduled job. Preferring the database unconditionally lets a
    single stale row outrank every later file, freezing the terminal on old prices.
    """
    record = MarketSnapshot.objects.first()
    committed = _committed()
    if record is None:
        return committed
    if committed is None:
        return record.payload
    committed_at = _generated_at(committed)
    if committed_at and record.generated_at and committed_at > record.generated_at:
        return committed
    return record.payload


def terminal(request):
    return render(request, "terminal/terminal.html", {"snapshot": _latest()})


def snapshot(request):
    payload = _latest()
    if payload is None:
        return JsonResponse({"status": "unavailable", "detail": "No verified market snapshot has been published."}, status=503)
    return JsonResponse(payload)
