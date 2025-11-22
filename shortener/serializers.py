from rest_framework import serializers
from .models import ShortenedUrl


class ShortenerInputSerializer(serializers.Serializer):
    url = serializers.URLField(
        max_length=ShortenedUrl._meta.get_field("original_url").max_length
    )
