from django.contrib.auth.models import User
from django.db import models

from apps.common.services import get_user


class Reconciliation(models.Model):
    date = models.DateField(verbose_name='Дата сверки', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.author = get_user()
        super(Reconciliation, self).save(*args, **kwargs)
