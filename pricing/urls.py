from django.urls import path

from .views import *

urlpatterns = [
    path("", pricing, name="pricing"),

]