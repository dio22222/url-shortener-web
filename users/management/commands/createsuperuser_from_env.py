import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

AUTH_USER_MODEL = get_user_model()


class Command(BaseCommand):
    help = "Created superuser account from environment variables"

    def handle(self, *args, **kwargs):
        username = os.environ.get("_USERNAME")
        password = os.environ.get("PASSWORD")

        if not username or not password:
            raise CommandError("Cannot create superuser without username and password")

        exists = AUTH_USER_MODEL.objects.filter(username=username).exists()

        if exists:
            raise CommandError(f"User with the username: {username} already exists")

        AUTH_USER_MODEL.objects.create_superuser(username=username, password=password)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created Superuser with username: {username} and password: {"*" * len(password)}")
        )
