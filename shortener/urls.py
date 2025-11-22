from django.urls import path
from .views import ShortenURL, NavigateToOriginalURL

urlpatterns = [
    path("", ShortenURL.as_view()),
    path("<shortened_code>", NavigateToOriginalURL.as_view()),
]
