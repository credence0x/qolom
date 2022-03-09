from django.db import models
from django.conf import settings
from core.common.fields import (DefaultTimeField, 
                                DefaultIntegerField,
                                DefaultCharField)
from core.common.models import BaseModel
from core.manager import CustomManager
from business.models import BusinessQueue



class UserProfile(BaseModel):
    user          = models.OneToOneField(settings.AUTH_USER_MODEL,
                                    related_name='userProfile',
                                    on_delete=models.DO_NOTHING,
                                    blank=True)
   
    d_o_b          = models.DateField()
    ticket        = models.CharField(max_length=10,blank=True)
    favourites    = models.ManyToManyField("BusinessProfile",
                                    related_name='favourites')

    current_business_queue        = models.ForeignKey(BusinessQueue,
                                     on_delete=models.PROTECT,
                                     related_name='people_on_queue',
                                     null=True,
                                     blank=True)

    current_user_queue   = models.ForeignKey("users.UserQueue",
                                     on_delete=models.PROTECT,
                                     related_name='people_on_queue',
                                     null=True,
                                     blank=True)

    time_of_queue_entry  = DefaultTimeField()
       
    total_seconds = DefaultIntegerField()
    country       = models.CharField(max_length=255)
    iso_code      = models.CharField(max_length=2)
    
    
    
    objects = CustomManager()


    class Meta:
        verbose_name = '[User Profile]'
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"[ User Profile ] - >{self.user.first_name} {self.user.last_name}"

    








class CardInformation(models.Model):
    owner            = models.ForeignKey("account.UserProfile",
                                     on_delete=models.DO_NOTHING,
                                     related_name='card',
                                    )
   
    authorization_code          = DefaultCharField()
    card_bin        = DefaultCharField()
    last4    = DefaultCharField()
    exp_month= DefaultCharField()
    exp_year = DefaultCharField()
    brand = DefaultCharField()
    signature = DefaultCharField()
    account_name = DefaultCharField()
    created_at = models.DateTimeField(auto_now_add=True)

    


    class Meta:
        verbose_name = '[User Profile] [Card Information]'
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"[ User Profile ] [ Card Information ] - > {self.owner}"

    
