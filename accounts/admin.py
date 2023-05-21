from django.contrib import admin

from rest_framework.authtoken.models import Token

from .models import User
from url_short_api.models import ShortURL


# Register your models here.

class TokenInline(admin.StackedInline):
    model = Token
    extra = 0
    
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
    
    inlines = [TokenInline, ShortURLInline]


admin.site.register(User, UserAdmin)

