from django.urls import path

from .views import *

urlpatterns = [
    path("", pricing, name="pricing"),
    path("buy/", buy_plan, name="buy_plan"),

]