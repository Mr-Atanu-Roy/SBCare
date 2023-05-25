from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from accounts.models import BaseModel, User
from .utils import generate_random_string


source_choices = (
    ("api-call", "api-call"),
    ("product", "product"),
)

#utility func
def generate_unique_short_url():
    unique = False
    
    while(unique==False):
        unique_short_url = settings.BASE_URL+f"r/{generate_random_string(8)}"
        check_url = ShortURL.objects.filter(short_url=unique_short_url)
        if check_url is not None:
            unique = True
    
    return unique_short_url


# Create your models here.
class ShortURL(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    title = models.CharField(max_length=300, blank=True, null=True)
    original_url = models.URLField()
    short_url = models.CharField(max_length=50, null=True, blank=True, unique=True)
    source = models.CharField(choices=source_choices, max_length=255, default="api-call")
    
    def __str__(self):
        return str(self.short_url)
    
    
    
#signals
@receiver(post_save, sender=ShortURL)
def create_short_url_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal will be executed each time a new extry is inserted in ShortURL db. This signal is responsible for generating short url
    '''
    
    if created:
        instance.short_url = generate_unique_short_url()
        instance.save()
    