from django.urls import path
from .views import *

urlpatterns = [
    path("", url_short, name="url_short_api"),
]
