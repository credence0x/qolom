from django.db import models
from core.common.fields import (DefaultCharField)
from core.common.models import BaseModel
from core.manager import CustomManager
from django.utils.text import slugify
from django.urls import reverse
from account.models import BusinessProfile

class BusinessQueue(BaseModel):
    business     = models.ForeignKey("account.BusinessProfile",
                                    on_delete=models.DO_NOTHING,
                                    related_name='queue'
                                    )
    name         = DefaultCharField()
    instruction  = DefaultCharField()
    information  = DefaultCharField()
    
    key  = models.CharField(max_length=8,
                            blank=True,
                            unique=True,
                            null=True)
    slug         = models.SlugField(max_length=80,
                                    db_index=False)
    objects = CustomManager()
    
    class Meta:
        verbose_name = '[ Business Queue ]'
        ordering = ["-created_at"]
        
        

    def __str__(self):
        return f"[ Business Queue ] - >  {self.name}"

    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True
        self.slug = slugify(self.name)
        super(BusinessQueue, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.people_present.set([])
        self.is_active = False
        super(BusinessQueue, self).save(*args, **kwargs)

 
    
    def get_absolute_url(self):
        return reverse('business:business_detailview',
                        args=[
                              str(self.slug)
                            ])
       
                        
        
    







