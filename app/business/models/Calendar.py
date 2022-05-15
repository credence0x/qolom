from django.db import models
from core.common.fields import (
                                DefaultTimeField
                                )
from core.common.models import BaseModel
from core.manager import CustomManager




class Calendar(BaseModel):
    owner     = models.ForeignKey("account.BusinessProfile",
                                    on_delete=models.DO_NOTHING,
                                    related_name='calendar'
                                    )  
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
        verbose_name = '[Business] Calendar'
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"Calendar for {self.owner}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True
        super(Calendar, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        super(Calendar, self).save(*args, **kwargs)
