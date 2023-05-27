from django.contrib import admin

from rest_framework.authtoken.models import Token

from .models import User, UserProfile, OTP
from url_short_api.models import ShortURL
from qr_code_api.models import QRCode


# Register your models here.

class OTPInline(admin.StackedInline):
    model = OTP
    extra = 0
    
class TokenInline(admin.StackedInline):
    model = Token
    extra = 0
    
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    
class ShortURLInline(admin.TabularInline):
    model = ShortURL
    extra = 0
    
class QRCodeInline(admin.TabularInline):
    model = QRCode
    extra = 0

    
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'is_verified', 'last_login', 'is_staff')
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
    
    inlines = [OTPInline, UserProfileInline, TokenInline, ShortURLInline, QRCodeInline]
    
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'api_access', 'coins', 'gender', 'country', 'city')
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
    ]
    
class OTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'otp', 'purpose', 'is_used', 'created_at')
    fieldsets = [
        ("OTP Details", {
            "fields": (
                ['user', 'purpose', 'is_used']
            ),
        }),
    ]


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(OTP, OTPAdmin)

