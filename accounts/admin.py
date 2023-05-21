from django.contrib import admin
from .models import User


# Register your models here.
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

