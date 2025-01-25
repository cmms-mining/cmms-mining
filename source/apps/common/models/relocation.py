from django.contrib.auth.models import User
from django.db import models

from apps.common.services import get_user


class Relocation(models.Model):
    """Перемещения"""
    from_site = models.ForeignKey(
        to='sites.Site',
        related_name='%(class)ss_from_site',
        on_delete=models.CASCADE,
        verbose_name='Откуда',
        blank=True,
        null=True,
    )
    to_site = models.ForeignKey(
        to='sites.Site',
        related_name='%(class)ss_to_site',
        on_delete=models.CASCADE,
        verbose_name='Куда',
    )
    date = models.DateField(
        verbose_name='Дата перемещения',
        null=True,
        )
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.author = get_user()
        super(Relocation, self).save(*args, **kwargs)
