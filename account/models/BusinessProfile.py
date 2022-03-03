from django.db import models
from core.common.fields import (DefaultTextField, 
                                DefaultTimeField,
                                DefaultIntegerField,
                                DefaultCharField)
from core.common.models import BaseModel
from core.manager import CustomManager
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse



class BusinessProfile(BaseModel):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL,
                                    related_name='businessProfile',
                                    on_delete=models.CASCADE)
    name        = models.CharField(max_length=250,unique=True)
    key         = models.CharField(
                                    max_length=7,
                                    unique=True
                                )
    minimum_age_allowed    = models.IntegerField(default=1)
    slug        = models.SlugField(blank=True,db_index=False)
    address     = models.CharField(max_length=255)
    state       = models.CharField(max_length=255)
    country     = models.CharField(max_length=255)
    iso_code    = models.CharField(max_length=2)
    profile_picture       = models.ImageField(upload_to='profile',null=True)
    timezone    = models.CharField(max_length=255)

    ordering_feature_active = models.BooleanField(default=False)
    has_orders  = models.BooleanField(default=False)
    total_amount_earned   = DefaultIntegerField()
    total_amount_received = DefaultIntegerField()
    
    
    objects = CustomManager()


    class Meta:
        verbose_name = '[Business Profile] '
        ordering = ["-created_at"]
        indexes = [
                    models.Index(fields=['name',
                                        'address',
                                        'state'])
            ]
            
        
 
    def __str__(self):
        return f"[ Business ] - >  {self.user.first_name}"

    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True
        self.slug = slugify(self.name)
        super(BusinessProfile, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.is_active = False
        super(BusinessProfile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:user_detailview',
                        args=[
                              str(self.key),
                              self.slug
                            ])









