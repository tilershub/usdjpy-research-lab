from django.urls import path
from . import views

app_name = "terminal"
urlpatterns = [
    path("", views.terminal, name="terminal"),
    path("snapshot.json", views.snapshot, name="snapshot"),
]
