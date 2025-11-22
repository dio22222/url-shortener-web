import uuid
from django.db import models


class ShortenedUrl(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_url = models.URLField(max_length=400, unique=True)
    shortened_code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Shortened URL"
        verbose_name_plural = "Shortened URLs"

    def __str__(self):
        return (
            f"Original URL: {self.original_url}, Shortened code: {self.shortened_code}"
        )
