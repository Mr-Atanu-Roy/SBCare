from django.db import models
from accounts.utils import BaseModel


#choices


# Create your models here.

class Pricing(BaseModel):
    
    plan_name = models.CharField(max_length=300)
    pricing = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.plan_name
    
    class Meta:
        verbose_name_plural = "Pricing and Plans"


