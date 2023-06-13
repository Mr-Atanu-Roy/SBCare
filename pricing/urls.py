from django.urls import path

from .views import *

urlpatterns = [
    path("", pricing, name="pricing"),
    path("buy/", buy_plan, name="buy_plan"),
    path("payment-success/", payment_success, name="payment_success"),
    
    #ajax calls
    path("get_plan_info/", get_plan_info, name="get_plan_info"),

]