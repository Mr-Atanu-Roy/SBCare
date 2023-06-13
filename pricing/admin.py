from django.contrib import admin
from .models import Pricing

# Register your models here.

class PricingAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'pricing_month', 'url_day', 'qr_day', 'api_day')
    fieldsets = [
        ("Plan Details", {
            "fields": (
                ['plan_name', 'pricing_month', 'url_day', 'qr_day', 'api_day', 'description']
            ),
        }),
    ]

admin.site.register(Pricing, PricingAdmin)
