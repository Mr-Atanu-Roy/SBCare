from django.urls import path

from .views import *

urlpatterns = [
    path("", getting_started, name="getting-started"),
    path("what-is-access-tokens", access_tokens, name="access-tokens"),

]