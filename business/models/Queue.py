from django.db import models
from core.common.fields import (DefaultCharField)
from core.common.models import BaseModel
from core.manager import CustomManager
from django.utils.text import slugify
from django.urls import reverse
from account.models import BusinessProfile

class BusinessQueue(BaseModel):
    owner     = models.ForeignKey("account.BusinessProfile",
                                    on_delete=models.DO_NOTHING,
                                    related_name='queue'
                                    )
    name         = models.CharField(max_length=255)
    instruction  = models.CharField(max_length=10000)
    information  = models.CharField(max_length=10000)
    
    key  = models.CharField(
                            max_length=8,
                            unique=True,
                            )
    
    objects = CustomManager()
    
    class Meta:
        verbose_name = '[ Business Queue ]'
        ordering = ["-created_at"]
        
        

    def __str__(self):
        return f"[ Business Queue ] - >  {self.name}"

    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True
        super(BusinessQueue, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.people_on_queue.set([])
        self.is_active = False
        super(BusinessQueue, self).save(*args, **kwargs)

 
       
                        
        
    







