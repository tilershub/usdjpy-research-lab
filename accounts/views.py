import json

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import SignUpForm
from .models import TradingWorkspace

FIELDS = {"journal": list, "plan": dict, "daily_checklists": dict, "watchlist": list, "alert_preferences": dict}
MAX_PAYLOAD_BYTES = 2 * 1024 * 1024


def signup(request):
    if request.user.is_authenticated:
        return redirect("account-dashboard")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("account-dashboard")
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def dashboard(request):
    workspace, _ = TradingWorkspace.objects.get_or_create(user=request.user)
    return render(request, "accounts/dashboard.html", {"workspace": workspace})


@login_required
@require_http_methods(["GET", "PUT"])
def workspace_api(request):
    workspace, _ = TradingWorkspace.objects.get_or_create(user=request.user)
    if request.method == "GET":
        return JsonResponse({**{name: getattr(workspace, name) for name in FIELDS}, "updated_at": workspace.updated_at.isoformat()})
    if int(request.META.get("CONTENT_LENGTH") or 0) > MAX_PAYLOAD_BYTES:
        return JsonResponse({"error": "Payload is too large."}, status=413)
    try:
        payload = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON."}, status=400)
    if not isinstance(payload, dict):
        return JsonResponse({"error": "Expected an object."}, status=400)
    changed = []
    for name, expected_type in FIELDS.items():
        if name not in payload:
            continue
        if not isinstance(payload[name], expected_type):
            return JsonResponse({"error": f"{name} has an invalid format."}, status=400)
        setattr(workspace, name, payload[name])
        changed.append(name)
    if not changed:
        return JsonResponse({"error": "No supported fields supplied."}, status=400)
    workspace.save(update_fields=[*changed, "updated_at"])
    return JsonResponse({"ok": True, "updated_at": workspace.updated_at.isoformat()})
