from django.db import models
from django.core.files.base import ContentFile

from accounts.models import User, BaseModel, SoftModel
from url_short_api.models import source_choices

from io import BytesIO
import random
import qrcode

type_choices = (
    ("url", "url"),
    ("me-card", "me-card"),
    ("wifi", "wifi"),
)

# Create your models here.
class QRCode(BaseModel, SoftModel):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    type = models.CharField(choices=type_choices, default="url", max_length=300)
    qr_code = models.ImageField(upload_to="qr-codes/", blank=True, null=True)
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
    
    
    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        type = self.type
        if type == "url":
            qr_data = self.url
        elif type == "wifi":
            qr_data = f"WIFI:T:{self.security};S:{self.ssid};P:{self.password};;"
        elif type == "me-card":
            qr_data = f"BEGIN:VCARD\nVERSION:3.0\nN:{self.name}\nTEL;TYPE=CELL:{self.phone}\nEMAIL:{self.email}"
            if self.url:
                qr_data += f"\nURL:{self.url}"
            qr_data += "\nEND:VCARD"
        
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_code_image = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        qr_code_image.save(buffer, format="PNG")
        self.qr_code.save(f'qrcode_{self.type}_{random.randint(1000, 999999)}.png', ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "QR Code API"
    
    