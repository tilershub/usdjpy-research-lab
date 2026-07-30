import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Idempotently create the deployment administrator from environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip().lower()
        if not username or not password:
            self.stdout.write(self.style.WARNING("Admin bootstrap skipped: deployment credentials are not configured."))
            return

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )
        changed = []
        if created:
            user.set_password(password)
            changed.append("password")
        if email and user.email != email:
            user.email = email
            changed.append("email")
        if not user.is_staff:
            user.is_staff = True
            changed.append("is_staff")
        if not user.is_superuser:
            user.is_superuser = True
            changed.append("is_superuser")
        if changed:
            user.save()

        action = "Created" if created else "Verified"
        self.stdout.write(self.style.SUCCESS(f"{action} deployment administrator '{username}'."))
