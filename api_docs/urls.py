from django.urls import path

from .views import *

urlpatterns = [
    path("", getting_started, name="getting-started"),
    path("access-tokens", access_tokens, name="access-tokens"),
    path("short-urls", short_urls, name="short-urls"),
    path("qr-codes", qr_codes, name="qr-codes"),
    
]