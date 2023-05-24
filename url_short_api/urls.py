from django.urls import path

from .views import *

urlpatterns = [
    path("<token>", redirect_link, name="redirect_link"),
    path("api/short-url/", GetCreateShortURL.as_view(), name="get_create_short_url_api"),
    path("api/short-url/<pk>", GetUpdateDeleteShortURL.as_view(), name="get_update_delete_short_url_api"),
    
]
