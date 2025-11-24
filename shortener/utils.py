import secrets
from django.conf import settings
from .models import ShortenedUrl

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
DOMAIN_NAME = settings.DOMAIN_NAME


def generate_short_code(length):
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def shorten_url(long_url, user):
    short_code_length = ShortenedUrl._meta.get_field("short_code").max_length
    generation_tries = 1

    while True:
        short_code = generate_short_code(short_code_length)
        exists = ShortenedUrl.objects.filter(short_code=short_code).exists()

        if not exists:
            ShortenedUrl.objects.create(
                original_url=long_url,
                short_code=short_code,
                user=user,
                generation_tries=generation_tries,
            )
            return DOMAIN_NAME + "/" + short_code

        generation_tries += 1
