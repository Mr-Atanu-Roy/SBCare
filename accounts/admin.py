from django.contrib import admin

from accounts.models import User, UserProfile, OTP, UserToken
from url_short_api.models import ShortURL
from qr_code_api.models import QRCode


# Register your models here.

class OTPInline(admin.StackedInline):
    model = OTP
    extra = 0
    classes = ['collapse']
    
class UserTokenInline(admin.StackedInline):
    model = UserToken
    extra = 0
    classes = ['collapse']
    
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    classes = ['collapse']
    
class ShortURLInline(admin.TabularInline):
    model = ShortURL
    extra = 0
    classes = ['collapse']
    
class QRCodeInline(admin.TabularInline):
    model = QRCode
    extra = 0
    classes = ['collapse']


    
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
            ), 'classes': ['collapse']
        }),
    ]
    
    inlines = [UserProfileInline, OTPInline, UserTokenInline, ShortURLInline, QRCodeInline]
    
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'api_access', 'gender', 'country', 'city')
    fieldsets = [
        ("User Details", {
            "fields": (
                ['gender', 'dob']
            ),
        }),
        ("Residential Details", {
            "fields": (
                ['country', 'city', 'address1', 'address2']
            )
        }),
        ("Product/API Details", {
            "fields": (
                ['api_access', 'plan', 'last_paid', 'url_mo', 'qr_mo', 'api_mo']
            ), 'classes': ['collapse']
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
    
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'role', 'created_at')
    fieldsets = [
        ("Token Details", {
            "fields": (
                ['user', 'role']
            ),
        }),
    ]


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(OTP, OTPAdmin)
admin.site.register(UserToken, UserTokenAdmin)

