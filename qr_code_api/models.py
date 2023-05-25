from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from accounts.models import User, BaseModel
from url_short_api.models import source_choices

import random
import segno

type_choices = (
    ("url", "url"),
    ("me-card", "me-card"),
    ("wifi", "wifi"),
)

# Create your models here.
class QRCode(BaseModel):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    type = models.CharField(choices=type_choices, default="url", max_length=300)
    qr_code = models.FileField(max_length=650, upload_to="qr-codes/", blank=True, null=True)
    source = models.CharField(choices=source_choices, max_length=255, default="api-service")
    
    #qr-code data fields
    #url
    url = models.CharField(blank=True, null=True, max_length=350)
    #me-card
    name = models.CharField(blank=True, null=True, max_length=350)
    email = models.CharField(blank=True, null=True, max_length=350)
    phone = models.CharField(blank=True, null=True, max_length=350)
    #wifi
    ssid = models.CharField(blank=True, null=True, max_length=350)
    password = models.CharField(blank=True, null=True, max_length=350)
    security = models.CharField(blank=True, null=True, max_length=350)
    
        
    def __str__(self):
        return self.title
    
    



#signals
@receiver(post_save, sender=QRCode)
def create_qrcode_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal will be executed each time a new extry is inserted in QRCode db. This signal is responsible for generating qrcodes
    '''
    
    if created:
        type = instance.type
    
        if type=="url":
            qrcode = segno.make(instance.url)
        
        if type=="me-card":
            qrcode = segno.helpers.make_mecard(name=instance.name, email=instance.email, phone=instance.phone)
        
        if type=="wifi":
            qrcode = segno.helpers.make_wifi(ssid=instance.ssid, password=instance.password, security=instance.security)
            
        qr_dir = f'{settings.MEDIA_ROOT}\qrcode_{instance.type}_{random.randint(1000, 999999)}.png'
        instance.qr_code = qr_dir

        qrcode.save(qr_dir, scale=10)

    
    