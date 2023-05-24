from django.contrib import admin
from .models import ShortURL

# Register your models here.

class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'short_url', 'created_at')
    fieldsets = [
        ("URL Details", {
            "fields": (
                ['user', 'title', 'original_url', 'short_url']
            ),
        }),
    ]


admin.site.register(ShortURL, ShortURLAdmin)
