from django.contrib import admin

from rest_framework.authtoken.models import Token

from .models import User, UserProfile
from url_short_api.models import ShortURL


# Register your models here.

class TokenInline(admin.StackedInline):
    model = Token
    extra = 0
    
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    
class ShortURLInline(admin.StackedInline):
    model = ShortURL
    extra = 0
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_verified', 'last_login', 'is_staff')
    fieldsets = [
        ("User Details", {
            "fields": (
                ['email', 'password', 'first_name', 'last_name']
            ),
        }),
        ("More Details", {
            "fields": (
                ['is_verified', 'date_joined', 'last_login', 'last_logout']
            ), 'classes': ['collapse']
        }),
        ("Permissions", {
            "fields": (
                ['is_staff', 'is_superuser', 'is_active', 'user_permissions', 'groups']
            ),
        }),
    ]
    
    inlines = [UserProfileInline, TokenInline, ShortURLInline]
    
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'api_access', 'coins', 'gender', 'country', 'city')
    fieldsets = [
        ("User Details", {
            "fields": (
                ['api_access', 'coins', 'gender']
            ),
        }),
        ("Residentialgol Details", {
            "fields": (
                ['country', 'city', 'address1', 'address2']
            )
        }),
        ("Verifying Token", {
            "fields": (
                ['auth_token']
            ),
        }),
    ]


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

