from django.db import models
from django.utils.text import slugify
from core.common.fields import (DefaultCharField)
from core.common.models import BaseModel
from core.manager import CustomManager
from account.models import UserProfile






class UserQueue(BaseModel):
    owner     = models.ForeignKey("account.UserProfile",
                                    on_delete=models.DO_NOTHING,
                                    related_name='owned_user_queue'
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
        verbose_name = '[ User Queue ]'
        ordering = ["-created_at"]
        
        

    def __str__(self):
        return f"[ User Queue ] - >  {self.name}"

    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True
        self.slug = slugify(self.name)
        super(UserQueue, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.people_present.set([])
        self.is_active = False
        super(UserQueue, self).save(*args, **kwargs)

 
        
    



