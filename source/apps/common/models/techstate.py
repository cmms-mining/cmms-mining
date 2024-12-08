from django.contrib.auth.models import User
from django.db import models

from apps.common.services import get_user


class TechState(models.Model):
    """Техсостояние"""
    date = models.DateField(verbose_name='Дата техсостояния')
    techstate = models.ForeignKey(
        to='common.TechStateOption',
        related_name='%(class)ss',
        on_delete=models.CASCADE,
        verbose_name='Техсостояние',
    )
    is_operable = models.BooleanField(verbose_name='Подлежит эксплуатации')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.author = get_user()
        super(TechState, self).save(*args, **kwargs)


class TechStateOption(models.Model):
    """Варианты техсостояний"""
    name = models.CharField(verbose_name='Название', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Вариант техсостояния'
        verbose_name_plural = '(Справочник) Варианты техсостояний'
        ordering = ['name']

    def __str__(self):
        return self.name
