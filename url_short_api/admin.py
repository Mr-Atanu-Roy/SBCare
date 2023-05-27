from django.contrib import admin
from .models import ShortURL

# Register your models here.

class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'short_url', 'source', 'created_at', 'is_deleted')
    fieldsets = [
        ("URL Details", {
            "fields": (
                ['user', 'title', 'original_url', 'short_url', 'source']
            ),
        }),
    ]


admin.site.register(ShortURL, ShortURLAdmin)
