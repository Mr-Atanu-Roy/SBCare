from django.contrib import admin
from .models import Pricing

# Register your models here.

class PricingAdmin(admin.ModelAdmin):
    list_display = ('id', 'plan_name', 'pricing')
    fieldsets = [
        ("Plan Details", {
            "fields": (
                ['plan_name', 'pricing', 'description']
            ),
        }),
    ]

admin.site.register(Pricing, PricingAdmin)
