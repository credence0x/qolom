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
                                    related_name='business',
                                    on_delete=models.CASCADE)
    name        = DefaultCharField()
    key         = models.CharField(max_length=7,null=True,
                                   blank=True,unique=True,
                                   db_index=False)
    minimum_age_allowed    = DefaultIntegerField()
    slug        = models.SlugField(blank=True,db_index=False)
    address     = DefaultCharField()
    state       = DefaultCharField()
    country     = DefaultCharField()
    iso_code    = models.CharField(max_length=2, null=True)
    profile_picture       = models.ImageField(upload_to='profile',null=True)
    timezone    = DefaultCharField()

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
            
        

    # def filename(self): # delete
    #     return os.path.basename(self.profile_picture.name)    
        
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










class Calendar(BaseModel):
    business                = models.ForeignKey(BusinessProfile,
                                        related_name='calendar',
                                        on_delete = models.DO_NOTHING)    
    days_open     = DefaultCharField()  
    mo_o            = DefaultTimeField()
    mo_c            = DefaultTimeField()
    tu_o            = DefaultTimeField()
    tu_c            = DefaultTimeField()
    we_o            = DefaultTimeField()
    we_c            = DefaultTimeField()
    th_o            = DefaultTimeField()
    th_c            = DefaultTimeField()
    fr_o            = DefaultTimeField()
    fr_c            = DefaultTimeField()
    sa_o            = DefaultTimeField()
    sa_c            = DefaultTimeField()
    su_o            = DefaultTimeField()
    su_c            = DefaultTimeField()
    objects = CustomManager()

    class Meta:
        verbose_name = '[Business Profile] Calendar'
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"Calendar for {self.business}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True
        super(Calendar, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        super(Calendar, self).save(*args, **kwargs)
