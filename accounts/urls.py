from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import *

urlpatterns = [
    path("signup", signup, name="signup"),
    path("login", login, name="login"),
    path("logout", logout, name="logout"),
    path("email-verify/", email_verify, name="email_verify"),
    path("email-verify/<token>", email_verify_link, name="email_verify_link"),
    
    path("generate-authtoken", obtain_auth_token, name="generate_authtoken"),
]
