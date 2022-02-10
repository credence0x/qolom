from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.http import request
import os



class Business_line(models.Model):
    name         = models.CharField(max_length=50)
    instruction  = models.CharField(max_length=250,null=True)
    information  = models.CharField(max_length=250,null=True)
    
    uniquefield  = models.CharField(max_length=8,
                                       blank=True,
                                       unique=True,
                                       null=True)
    slug         = models.SlugField(max_length=80,
                                    db_index=False)
    business     = models.ForeignKey('Business_signup',
                                    on_delete=models.CASCADE,
                                    related_name='business_line'
                                    )
    

    def delete(self, *args, **kwargs):
        self.people_present.set([])
        super(Business_line, self).save(*args, **kwargs)
        super(Business_line, self).delete(*args, **kwargs)

    def __str__(self):
        return '{} at {}'.format(self.name,self.business)
    def get_absolute_url(self):
        return reverse('business:business_detailview',
                        args=[
                              str(self.slug)
                            ])
       
                        
        
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Business_line, self).save(*args, **kwargs)










class Special_line(models.Model):
    name         = models.CharField(max_length=50)
    instruction  = models.CharField(max_length=250,null=True)
    information  = models.CharField(max_length=250,null=True)
    
    uniquefield  = models.CharField(max_length=8,
                                       blank=True,
                                       unique=True,
                                       null=True)
    slug         = models.SlugField(max_length=80,
                                    db_index=False)
    days_open    = models.CharField(max_length=42,
                                     blank=True,null=True)
    created      = models.DateTimeField(auto_now_add=True,null=True)
    
    mo_o     = models.TimeField(blank=True,null=True)
    mo_c    = models.TimeField(blank=True,null=True)

    
    tu_o     = models.TimeField(blank=True,null=True)
    tu_c    = models.TimeField(blank=True,null=True)

    
    we_o     = models.TimeField(blank=True,null=True)
    we_c    = models.TimeField(blank=True,null=True)

    
    th_o     = models.TimeField(blank=True,null=True)
    th_c    = models.TimeField(blank=True,null=True)

    
    fr_o     = models.TimeField(blank=True,null=True)
    fr_c    = models.TimeField(blank=True,null=True)

    
    sa_o      = models.TimeField(blank=True,null=True)
    sa_c     = models.TimeField(blank=True,null=True)

    
    su_o    = models.TimeField(blank=True,null=True)
    su_c    = models.TimeField(blank=True,null=True)


    admin_user     = models.OneToOneField('User_signup',
                                    on_delete=models.CASCADE,
                                    related_name='admin_special_line',
                                    null=True
                                    )
    

    def delete(self, *args, **kwargs):
        self.all_present.set([])
        super(Special_line, self).save(*args, **kwargs)
        super(Special_line, self).delete(*args, **kwargs)

    def __str__(self):
        return '{} by {}'.format(self.name,self.admin_user)
        
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Special_line, self).save(*args, **kwargs)




        
class User_signup(models.Model):
    user          = models.OneToOneField(settings.AUTH_USER_MODEL,
                                    related_name='user_signup',
                                    on_delete=models.CASCADE,blank=True)
    first_name    = models.CharField(max_length=15,blank=True)
    last_name     = models.CharField(max_length=30,blank=True)
    age          = models.DateField(null=True,blank=True)
    unique     = models.CharField(max_length=7,
                                  blank=True,
                                  null=True,
                                  unique=True,
                                  db_index=False)
    
    ticket        = models.CharField(max_length=10,blank=True)
    favourites    = models.ManyToManyField('Business_signup',
                                    related_name='favourites')
    present_line  = models.ForeignKey(Business_line,
                                     on_delete=models.PROTECT,
                                     related_name='people_present',
                                     null=True,
                                     blank=True)
    special_line  = models.ForeignKey(Special_line,
                                     on_delete=models.PROTECT,
                                     related_name='all_present',
                                     null=True,
                                     blank=True)
    timezone      = models.CharField(max_length=100,
                                   blank=True,
                                   null=True)
    
   
    time          = models.DateTimeField(blank=True,null=True)
    total_seconds = models.IntegerField(blank=True,null=True)
    country       = models.CharField(max_length=300, null=True)
    iso_code      = models.CharField(max_length=2, null=True)
    card_information = models.CharField(max_length=1000000, null=True,
                                          default='[]')
    
    def __str__(self):
        return self.first_name



    

class Business_signup(models.Model):
    user        = models.OneToOneField(settings.AUTH_USER_MODEL,
                                    related_name='business_signup',
                                    on_delete=models.CASCADE)
    name        = models.CharField(max_length=300, null=True)
    key         = models.CharField(max_length=7,
                                   null=True,
                                   blank=True,
                                   unique=True,
                                   db_index=False)
    min_age    = models.IntegerField(default=0)
    account_number = models.CharField(max_length=50,
                                   null=True,
                                   blank=True,
                                   )
    bank = models.CharField(max_length=1000,
                                   null=True,
                                   blank=True,
                                   )
    bank_account_name= models.CharField(max_length=1000,
                                   null=True,
                                   blank=True,
                                   )
    recipient_info = models.CharField(max_length=100000,
                                   null=True,
                                   blank=True,
                                   )
    bank_email_confirmation = models.BooleanField(default=False)
    total_earned   = models.IntegerField(default=0)
    total_received = models.IntegerField(default=0)
    order_active = models.BooleanField(default=False)
    slug        = models.SlugField(blank=True,db_index=False)
    created     = models.DateTimeField(auto_now_add=True)
    address     = models.CharField(max_length=300, null=True)
    state       = models.CharField(max_length=300, null=True)
    country     = models.CharField(max_length=300, null=True)
    iso_code    = models.CharField(max_length=2, null=True)
    dp          = models.ImageField(upload_to='profile',null=True)
    timezone    = models.CharField(max_length=100,
                                   blank=True,
                                   null=True)
    has_orders  = models.BooleanField(default=False)


    days_open     = models.CharField(max_length=42,
                                     blank=True,null=True)
    
    mo_o     = models.TimeField(blank=True,null=True)
    mo_c    = models.TimeField(blank=True,null=True)

    
    tu_o     = models.TimeField(blank=True,null=True)
    tu_c    = models.TimeField(blank=True,null=True)

    
    we_o     = models.TimeField(blank=True,null=True)
    we_c    = models.TimeField(blank=True,null=True)

    
    th_o     = models.TimeField(blank=True,null=True)
    th_c    = models.TimeField(blank=True,null=True)

    
    fr_o     = models.TimeField(blank=True,null=True)
    fr_c    = models.TimeField(blank=True,null=True)

    
    sa_o      = models.TimeField(blank=True,null=True)
    sa_c     = models.TimeField(blank=True,null=True)

    
    su_o    = models.TimeField(blank=True,null=True)
    su_c    = models.TimeField(blank=True,null=True)


    
    class Meta:
        indexes = [
            models.Index(fields=['name','address','state'])
            ]

    def filename(self):
        return os.path.basename(self.dp.name)    
    
    
    
    
    def __str__(self):
        return self.user.first_name

    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Business_signup, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:user_detailview',
                        args=[
                              str(self.key),
                              self.slug
                            ])
    
    

class Items(models.Model):
    name                    = models.CharField(max_length=251,
                                               null=True,
                                               blank=True)
    business                = models.ForeignKey(Business_signup,
                                        related_name='all_items',
                                        on_delete = models.CASCADE)
    price                   = models.IntegerField()
    units_available         = models.IntegerField()
    
    
    

class Orders(models.Model):
    reference         = models.CharField(max_length=1000)
    items             = models.CharField(max_length=10485760)
    total             = models.CharField(max_length=250)
    status            = models.CharField(max_length=250)
    user              = models.ForeignKey(User_signup,
                                     on_delete=models.CASCADE,
                                     related_name='all_orders',
                                    )
    business          = models.ForeignKey(Business_signup,
                                     on_delete=models.CASCADE,
                                     related_name='not_important',
                                    )
    pin               = models.IntegerField()
    is_active         = models.BooleanField(default=False)
    order_status      = models.CharField(max_length=250,null=True)
    created           = models.DateTimeField()
    ready_time        = models.DateTimeField()
    has_seen_notification = models.BooleanField(default=False)
    fees          = models.FloatField(default=0)
    
    
    
    
    
    
    
    
    
    
    
    
