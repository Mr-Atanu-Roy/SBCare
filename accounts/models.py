from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import Usermanager, NonDelete

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token

import uuid
from .utils import SendEmail

#choices
gender_choices = (
    ("male", "Male"),
    ("female", "Female"),
    ("not-specify", "not-specify")
)


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
        
class SoftModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    
    everything = models.Manager()
    objects = NonDelete()

    def delete(self):
        self.is_deleted = True
        self.save()
        
    def restore(self):
        self.is_deleted = False
        self.save()
        
    class Meta:
        abstract = True



class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    last_logout = models.DateTimeField(null=True, blank=True)
    
    objects = Usermanager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'auth_user'
        verbose_name_plural = "SB-Care User"
        ordering = ['date_joined']
    
    def __str__(self):
        return self.email
    
    
class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='profile')
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(choices=gender_choices, max_length=50, default="male")
    address1 = models.TextField(blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    
    coins = models.IntegerField(default=0)
    api_access = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user)
    
    class Meta:
        verbose_name_plural = "User Profile"
        

class OTP(BaseModel):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    purpose = models.CharField(choices=(("email_verify", "email_verify"), ("reset_password", "reset_password")), default="email_verify", max_length=255)
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.otp)
    
    
    class Meta:
        verbose_name_plural = "OTPs"



@receiver(post_save, sender=User)
def User_created_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal will be executed each time a new user is created. This signal is responsible for generating a token for drf token auth and creating new userProfile and sending email for email-verification
    '''
    if created:    
        
        #generating token
        Token.objects.create(user=instance)  
        
        #sending email          
        subject = "Greetings from SB Care"
        message = f"Hello!!! Thank you for signing up with us {instance.first_name}... Your registration was recorded at {instance.date_joined}"
        
        #starting the thread to send email
        SendEmail(subject, message, instance.email).start()
        
        #creating a otp instance for verifying email
        newOTP = OTP(user=instance)
        newOTP.save()
        
        #creating a UserProfile instance
        newProfile = UserProfile.objects.create(user=instance)
        newProfile.save()
        


@receiver(post_save, sender=OTP)
def User_created_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal will be executed each time a new otp is created. This signal is responsible for generating a token creating otp for email verification/reset password and sending that via email
    '''
    if created:    
        
        #sending email 
        otp = instance.otp
        if instance.purpose == "reset_password":
            subject = "Reset your account password"
            message = f"There was a request for reseting your account password for: {instance.user.email}. Reset your by clicking on the given link {settings.BASE_URL}auth/reset-password/{otp}. This link will be expired after 15min."
        else:
            subject = "Please verify your email"
            message = f"Please verify your email : {instance.user.email} by clicking on the given link {settings.BASE_URL}auth/email-verify/{otp}. This link will be expired after 15min."
            
        
        #starting the thread to send email
        SendEmail(subject, message, instance.user.email).start()

        