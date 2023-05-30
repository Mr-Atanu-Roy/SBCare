from django.urls import path

from .views import *
from .api_view import GetCreateAuthToken, DeleteAuthToken

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout", logout, name="logout"),
    path("logout/", logout, name="logout"),
    
    path("dashboard/profile/", profile, name="profile"),
    path("dashboard/dev-settings/", dev_settings, name="dev-settings"),
    
    path("email-verify/", email_verify, name="email_verify"),
    path("email-verify/<token>", email_verify_link, name="email_verify_link"),
    
    path("reset-password/", reset_password, name="reset_password"),
    path("reset-password/<token>", reset_password_link, name="reset_password_link"),
    
    path("api/generate-authtoken/", GetCreateAuthToken.as_view(), name="generate_authtoken"),
    path("api/delete-authtoken/<pk>", DeleteAuthToken.as_view(), name="delete_authtoken"),
    
    #ajax urls
    path("submit-profile-form/", submit_profile_form, name="submit-profile-form"),
    
    path("get-auth-tokens/", get_authtoken, name="get-auth-tokens"),
    path("create-auth-token/", create_authtoken, name="create-auth-token"),
    path("delete-auth-token", delete_authtoken, name="delete-auth-token"),

]
