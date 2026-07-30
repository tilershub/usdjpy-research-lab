import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from .models import MarketSnapshot


def _latest():
    record = MarketSnapshot.objects.first()
    if record:
        return record.payload
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


def terminal(request):
    return render(request, "terminal/terminal.html", {"snapshot": _latest()})


def snapshot(request):
    payload = _latest()
    if payload is None:
        return JsonResponse({"status": "unavailable", "detail": "No verified market snapshot has been published."}, status=503)
    return JsonResponse(payload)
