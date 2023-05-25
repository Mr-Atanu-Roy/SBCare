from django.db import models

from accounts.models import BaseModel, User 

# Create your models here.
class URLShorterProduct(BaseModel):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, blank=True, null=True)
    original_url = models.CharField(max_length=600)
    short_url = models.CharField(max_length=250)

    def __str__(self):
        return str(self.user)
