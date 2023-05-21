from django.contrib import admin
from .models import ShortURL

# Register your models here.

class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_url', 'created_at')
    fieldsets = [
        ("URL Details", {
            "fields": (
                ['user', 'original_url', 'short_url']
            ),
        }),
    ]


admin.site.register(ShortURL, ShortURLAdmin)
