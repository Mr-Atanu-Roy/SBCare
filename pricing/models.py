from django.db import models
from accounts.utils import BaseModel


# Create your models here.

class Pricing(BaseModel):
    
    plan_name = models.CharField(max_length=300, unique=True)
    pricing_month = models.IntegerField(verbose_name="Pricing per Month", default=0)
    url_day = models.IntegerField(default=0, verbose_name="URL per Day")
    qr_day = models.IntegerField(default=0, verbose_name="QR per Day")
    api_day = models.IntegerField(default=0, verbose_name="API Request per Day")
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.plan_name
    
    class Meta:
        verbose_name_plural = "Pricing and Plans"




