from django.db import models
from core.common.fields import (DefaultTextField, 
                                DefaultCharField)
from core.common.models import BaseModel
from core.manager import CustomManager
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from account.models import BusinessProfile



class Bank(BaseModel):
    business                = models.ForeignKey("account.BusinessProfile",
                                        related_name='bank',
                                        on_delete = models.DO_NOTHING)    
    account_number = DefaultCharField()
    bank = DefaultTextField()
    account_name= DefaultTextField()
    recipient_info = DefaultTextField()
    email_confirmation = models.BooleanField(default=False)
    objects = CustomManager()
    
    class Meta:
        verbose_name = '[Business Profile] Bank'
        ordering = ["-created_at"]

    def __str__(self):
        return f"Bank for {self.business}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True
        super(Bank, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        super(Bank, self).save(*args, **kwargs)