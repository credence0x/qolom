import os
from datetime import datetime
from django.db import models


class DeactivateQuerySet(models.QuerySet):
    def delete(self):
        return super(DeactivateQuerySet, self).update(is_active=False)


class CustomManager(models.Manager):
    def get_queryset(self):
        return DeactivateQuerySet(self.model, using=self.db).filter(is_active=True)