from django.contrib import admin
from .models import ShortURL

# Register your models here.

class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('user', 'id','title', 'short_url', 'source', 'created_at')
    fieldsets = [
        ("URL Details", {
            "fields": (
                ['user', 'title', 'original_url', 'short_url', 'source']
            ),
        }),
    ]


admin.site.register(ShortURL, ShortURLAdmin)
