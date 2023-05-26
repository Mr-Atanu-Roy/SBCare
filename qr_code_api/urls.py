from django.urls import path

from .views import *

urlpatterns = [  
    #api urls
    path("api/qr-code/", GetCreateQR.as_view(), name="get_create_qr_api"),
    path("api/qr-code/<pk>", GetDeleteQR.as_view(), name="delete_qr_api"),
    
    #api-docs url
    
]