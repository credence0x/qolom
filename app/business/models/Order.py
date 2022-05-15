from django.db import models
from core.common.fields import (DefaultTextField, 
                                DefaultDateTimeField,
                                DefaultIntegerField,
                                DefaultCharField)
from core.common.models import BaseModel
from core.manager import CustomManager
from django.db import transaction




class Order(BaseModel):
    class StatusChoices(models.IntegerChoices):
        AWAITING_PAYMENT = 1
        SENT = 2
        READY = 3
        COLLECTED = 4

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

    total             = DefaultIntegerField() # total minus fees
    status            = models.IntegerField(choices=StatusChoices.choices)

    
    
    was_ready_by        = DefaultDateTimeField()
    # True when buyer has been notified that order is ready 
    buyer_notified = models.BooleanField(default=False)
    # True when seller has been notified that order has been sent
    seller_notified = models.BooleanField(default=False)
    fees          = models.FloatField(default=0)
    objects = CustomManager()

    class Meta:
        verbose_name = '[Order]'
        ordering = ["-created_at"]
        
        

    def __str__(self):
        return f"[ Order ] - >  {self.id} from {self.seller} to {self.buyer}"

    def payment_successful(self,reference=None):
        """
        Function is called when payment has been made successfully
        
        Reference is an optional field that would only be added 
        when a charge is made directly on the user (i.e when they pay
        with a saved card). This means that no reference had previously
        been generated and thus the new one is added 
        """
        with transaction.atomic():
            order = (
                    Order.objects
                    .select_for_update()
                        .get(
                                id=self.id
                            )
            )
            if order.status == 1: #AWAITING PAYMENT
                for purchased_item in order.purchased_item.all():
                    item = purchased_item.item
                    item.units -= purchased_item.units
                    item.save()

                
                # update item 
                for purchased_item in order.purchased_item.all():
                    item = purchased_item.item
                    item.units -= purchased_item.units
                    item.save()

                if reference:
                    order.reference = reference
                
                order.status = 2 # SENT
                order.save()
    




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


