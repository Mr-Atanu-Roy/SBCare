from django.contrib import admin

from .models import URLShorterProduct

# Register your models here.

class URLShorterProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'short_url', 'created_at')
    fieldsets = [
        ("URL Details", {
            "fields": (
                ['title', 'user', 'url_api', 'original_url', 'short_url']
            ),
        }),
    ]
    
admin.site.register(URLShorterProduct, URLShorterProductAdmin)

