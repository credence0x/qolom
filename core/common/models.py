from django.db import models
from django.utils.timezone import now


class ActiveQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class ActiveModelManager(models.Manager):
    def get_queryset(self):
        return ActiveQuerySet(model=self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()


class ActivatorModel(models.Model):
    is_active = models.BooleanField(default=False)
    activated_at = models.DateTimeField(blank=True, null=True)
    deactivated_at = models.DateTimeField(blank=True, null=True)
    objects = ActiveModelManager()

    class Meta:
        ordering = (
            "is_active",
            "-activated_at",
        )
        abstract = True

    def save(self, *args, **kwargs):
        if not self.activated_at:
            self.activated_at = now()
        if not self.deactivated_at and not self.is_active:
            self.deactivated_date = now()
        elif self.deactivated_at and self.is_active:
            self.deactivate_date = None
        super(ActivatorModel, self).save(*args, **kwargs)


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at", "-updated_at")


class BaseModel(ActivatorModel, TimestampedModel):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True
        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.is_active = False
        return super().save(*args, **kwargs)