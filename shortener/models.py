import uuid
from django.db import models
from django.contrib.auth import get_user_model

AUTH_USER_MODEL = get_user_model()


class ShortenedUrl(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_url = models.URLField(max_length=400)
    short_code = models.CharField(max_length=7, unique=True)
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    generation_tries = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Shortened URL"
        verbose_name_plural = "Shortened URLs"

    def __str__(self):
        return f"Original URL: {self.original_url}, Short code: {self.short_code}"
