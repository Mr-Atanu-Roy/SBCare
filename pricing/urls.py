from django.urls import path

from .views import *

urlpatterns = [
    path("", pricing, name="pricing"),
    path("buy/", buy_pricing, name="buy_pricing"),

]