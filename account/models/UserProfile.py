from django.db import models
from django.conf import settings
from account.models.BusinessProfile import BusinessProfile
from core.common.fields import (DefaultTimeField, 
                                DefaultIntegerField,
                                DefaultCharField)
from core.common.models import BaseModel
from core.manager import CustomManager
from account.models import BusinessProfile
from users.models import UserQueue
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
                                     related_name='people_present',
                                     null=True,
                                     blank=True)
    current_user_queue   = models.ForeignKey("users.UserQueue",
                                     on_delete=models.PROTECT,
                                     related_name='people_present',
                                     null=True,
                                     blank=True)
    timezone      = models.CharField(max_length=255)
    
   
    time          = DefaultTimeField()
    total_seconds = DefaultIntegerField()
    country       = models.CharField(max_length=255)
    iso_code      = models.CharField(max_length=2)
    card_information = models.CharField(max_length=1000000, null=True,
                                          default='[]')
    
    
    objects = CustomManager()


    class Meta:
        verbose_name = '[User Profile]'
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"[ User Profile ] - >{self.user.first_name} {self.user.last_name}"

    










class UserCalendar(BaseModel):
    owner                = models.ForeignKey(UserProfile,
                                        related_name='calendar',
                                        on_delete = models.DO_NOTHING)    
    days_open           = DefaultCharField()  
    mo_o                = DefaultTimeField()
    mo_c                = DefaultTimeField()
    tu_o                = DefaultTimeField()
    tu_c                = DefaultTimeField()
    we_o                = DefaultTimeField()
    we_c                = DefaultTimeField()
    th_o                = DefaultTimeField()
    th_c                = DefaultTimeField()
    fr_o                = DefaultTimeField()
    fr_c                = DefaultTimeField()
    sa_o                = DefaultTimeField()
    sa_c                = DefaultTimeField()
    su_o                = DefaultTimeField()
    su_c                = DefaultTimeField()
    objects = CustomManager()

    class Meta:
        verbose_name = '[User Profile] Calendar'
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"Calendar for {self.owner}"
