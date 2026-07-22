from django.http import JsonResponse
from django.shortcuts import render
from .models import MarketSnapshot


def _latest():
    record = MarketSnapshot.objects.first()
    return record.payload if record else None


def terminal(request):
    return render(request, "terminal/terminal.html", {"snapshot": _latest()})


def snapshot(request):
    payload = _latest()
    if payload is None:
        return JsonResponse({"status": "unavailable", "detail": "No verified market snapshot has been published."}, status=503)
    return JsonResponse(payload)
