from django.db import models
from core.common.fields import  DefaultTimeField
from core.common.fields import (DefaultTextField, 
                                DefaultDateTimeField,
                                DefaultIntegerField,
                                DefaultCharField)
from core.common.models import BaseModel
from core.manager import CustomManager
from account.models import UserProfile
from account.models import BusinessProfile




class Order(BaseModel):
    user_profile            = models.ForeignKey("account.UserProfile",
                                     on_delete=models.DO_NOTHING,
                                     related_name='orders',
                                    )
    business          = models.ForeignKey("account.BusinessProfile",
                                     on_delete=models.DO_NOTHING,
                                     related_name='orders',
                                    )
    reference         = DefaultTextField()
    items             = models.CharField(max_length=10485760)
    total             = DefaultCharField()
    status            = DefaultCharField()
    
    
    pin               = DefaultIntegerField()
    has_been_actived   = models.BooleanField(default=False)
    order_status      = DefaultCharField()
    ready_time        = DefaultDateTimeField()
    user_has_seen_notification = models.BooleanField(default=False)
    fees          = models.FloatField(default=0)
    objects = CustomManager()

    class Meta:
        verbose_name = '[Order]'
        ordering = ["-created_at"]
        
        

    def __str__(self):
        return f"[ Order ] - >  {self.reference}"

    
    




class Item(BaseModel):
    business                = models.ForeignKey("account.BusinessProfile",
                                        related_name='items',
                                        on_delete = models.DO_NOTHING)

    name                    = DefaultCharField()
    
    price                   = DefaultIntegerField()
    units_available         = DefaultIntegerField()
    objects = CustomManager()
    
    
    class Meta:
        verbose_name = '[Business] Item '
        ordering = ["-created_at"]
        
        

    def __str__(self):
        return f"[ Item ] - >  {self.name}"

