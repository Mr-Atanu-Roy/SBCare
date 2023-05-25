from django.urls import path
from .views import *

urlpatterns = [
    #product urls
    path("url-shorter", url_shorter, name="url_shorter"),
    
    #ajax request urls
    path("create-short-url-ajax", create_short_url_ajax, name="create-short-url-ajax"),
    path("delete-short-url-ajax", delete_short_url_ajax, name="delete-short-url-ajax"),
]
