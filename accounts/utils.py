from django.db import models
from .manager import NonDelete

import datetime
import pytz
from django.core.mail import send_mail
from django.conf import settings

from threading import Thread

import re
special_char_regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')


# Get the timezone object for the timezone specified in settings.py
tz = pytz.timezone(settings.TIME_ZONE)

# Get the current time in the timezone
current_time = datetime.datetime.now(tz)


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



def check_str_special(string):
    if special_char_regex.search(string):
        return True
    else:
        return False
    
    
class SendEmail(Thread):
    '''
    Using threads to send mails
    '''
    
    sender = settings.EMAIL_HOST_USER
    
    def __init__(self, subject, message, *receiver):
        self.recipient_list = [emails for emails in receiver]
        self.subject = subject
        self.message = message
        Thread.__init__(self)
        
    def run(self):
        send_mail(self.subject, self.message, self.sender, self.recipient_list)