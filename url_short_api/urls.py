from django.urls import path

from .views import *

urlpatterns = [
    path("<token>", redirect_link, name="redirect_link"),
    path("api/short-url/create", CreateShortURL.as_view(), name="create_short_url_api"),
]
