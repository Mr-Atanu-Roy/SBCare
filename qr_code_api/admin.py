from django.contrib import admin

from .models import QRCode

# Register your models here.
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'type', 'source', 'created_at')
    fieldsets = [
        ("QR Details", {
            "fields": (
                ['user', 'title', 'type', 'qr_code', 'source']
            ),
        }),
        ("QR Data Details", {
            "fields": (
                ['url', 'name', 'phone', 'email', 'ssid', 'password', 'security']
            ), 'classes': ['collapse']
        }),
    ]


admin.site.register(QRCode, QRCodeAdmin)
