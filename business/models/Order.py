from django.db import models
from core.common.fields import (DefaultTextField, 
                                DefaultDateTimeField,
                                DefaultIntegerField,
                                DefaultCharField)
from core.common.models import BaseModel
from core.manager import CustomManager




class Order(BaseModel):
    class StatusChoices(models.IntegerChoices):
        SENT = 1
        READY = 2
        COLLECTED = 3

    seller          = models.ForeignKey("account.BusinessProfile",
                                     on_delete=models.DO_NOTHING,
                                     related_name='orders',
                                    )
    buyer            = models.ForeignKey("account.UserProfile",
                                     on_delete=models.DO_NOTHING,
                                     related_name='orders',
                                    )
    
    
    reference         = DefaultTextField()
    pin               = DefaultIntegerField()

    total             = DefaultCharField()
    status            = models.IntegerField(choices=StatusChoices.choices)

    
    
    paid                 = models.BooleanField(default=False)
    was_ready_by        = DefaultDateTimeField()
    # True when buyer has been notified that order is ready 
    buyer_notified = models.BooleanField(default=False)
    fees          = models.FloatField(default=0)
    objects = CustomManager()

    class Meta:
        verbose_name = '[Order]'
        ordering = ["-created_at"]
        
        

    def __str__(self):
        return f"[ Order ] - >  {self.reference}"

    
    




class Item(BaseModel):
    owner                = models.ForeignKey("account.BusinessProfile",
                                        related_name='items',
                                        on_delete = models.DO_NOTHING)
    
    name                    = DefaultCharField()
    units                    = DefaultIntegerField() 
    
    price                   = DefaultIntegerField()
    objects = CustomManager()
    
    
    class Meta:
        verbose_name = '[Business] Item '
        ordering = ["-created_at"]
        
        

    def __str__(self):
        return f"[ Item ] - >  {self.name}"


class PurchasedItem(BaseModel):
    item                = models.ForeignKey(Item,
                                        related_name='purchased_item',
                                        on_delete = models.DO_NOTHING)
    
    units                    = DefaultIntegerField() 
    order                = models.ForeignKey(Order,
                                        related_name='purchased_item',
                                        on_delete = models.DO_NOTHING
                                        )
    objects = CustomManager()
    
    
    class Meta:
        verbose_name = '[Business] Purchased Item '
        ordering = ["-created_at"]
        
        

    def __str__(self):
        return f"[ Purchased Item ] - >  {self.item}"


