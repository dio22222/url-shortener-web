from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ShortenerInputSerializer
from .models import ShortenedUrl
import hashlib
from django.conf import settings

DOMAIN_NAME = settings.DOMAIN_NAME


class ShortenURL(APIView):
    def hash_url(self, url: str):
        return hashlib.sha256(url.encode()).hexdigest()[:6]

    def add_trailing_slash(self, url: str):
        if url[-1] != "/":
            url += "/"
        return url

    def post(self, request):
        serializer = ShortenerInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data.get("url")
        url = self.add_trailing_slash(url)
        hashed_url = self.hash_url(url)
        shortened_url = DOMAIN_NAME + "/" + hashed_url

        existing = ShortenedUrl.objects.filter(shortened_code=hashed_url).exists()

        # TODO: Detect collisions and recover

        if not existing:
            ShortenedUrl.objects.create(original_url=url, shortened_code=hashed_url)

        return Response(
            {"shortened_url": shortened_url}, status=status.HTTP_201_CREATED
        )


class NavigateToOriginalURL(APIView):
    def get(self, request, shortened_code):
        try:
            shortened_url = ShortenedUrl.objects.get(shortened_code=shortened_code)
        except ShortenedUrl.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(
            status=status.HTTP_302_FOUND,
            headers={"Location": shortened_url.original_url},
        )
