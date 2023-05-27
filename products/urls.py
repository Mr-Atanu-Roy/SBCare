from django.urls import path
from .views import *

urlpatterns = [
    #products urls
    path("url-shorter", url_shorter, name="url_shorter"),
    path("qrcode", qrcode, name="qrcode"),
    
    #ajax request urls
    path("get-short-url-ajax", get_short_url_ajax, name="get-short-url-ajax"),
    path("create-short-url-ajax", create_short_url_ajax, name="create-short-url-ajax"),
    path("delete-short-url-ajax", delete_short_url_ajax, name="delete-short-url-ajax"),
    
    path("get-qrcode-ajax", get_qrcode_ajax, name="get-qrcode-ajax"),
    path("create-qr-ajax", create_qr_ajax, name="create-qr-ajax"),
    path("delete-qr-ajax", delete_qr_ajax, name="delete-qr-ajax"),
]
