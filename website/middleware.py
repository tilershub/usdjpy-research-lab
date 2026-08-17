from django.db import connection
from django.http import HttpResponseNotAllowed, JsonResponse

HEALTH_PATH = "/health/"


def health_payload():
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        cursor.fetchone()
    response = JsonResponse({"status": "ok"})
    response["Cache-Control"] = "no-store"
    return response


class HealthCheckMiddleware:
    """Answer platform health probes before host and TLS validation run.

    Render probes the instance directly rather than through the public router, so
    the request arrives without the forwarded-proto header that keeps
    SECURE_SSL_REDIRECT quiet and with an internal Host value deliberately absent
    from ALLOWED_HOSTS. Both produce a non-2xx response, which Render reads as an
    unhealthy deploy. Resolving the probe here keeps redirect and host enforcement
    fully intact for every other path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path != HEALTH_PATH:
            return self.get_response(request)
        if request.method not in ("GET", "HEAD"):
            return HttpResponseNotAllowed(["GET", "HEAD"])
        return health_payload()
