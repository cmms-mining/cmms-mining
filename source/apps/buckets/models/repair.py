from django.contrib.auth.models import User
from django.db import models

from apps.common.services import get_user


class BucketRepair(models.Model):
    """Ремонты ковшей"""
    bucket = models.ForeignKey(
        to='buckets.Bucket',
        related_name='repairs',
        on_delete=models.CASCADE,
        verbose_name='Ковш',
    )
    start_date = models.DateField(verbose_name='Дата начала', blank=True, null=True)
    end_date = models.DateField(verbose_name='Дата окончания', blank=True, null=True)
    plan_start_date = models.DateField(verbose_name='Плановая дата начала', blank=True, null=True)
    plan_end_date = models.DateField(verbose_name='Плановая дата окончания', blank=True, null=True)
    worklist = models.TextField(verbose_name='Требуемые работы')
    note = models.TextField(verbose_name='Примечания', blank=True, null=True)
    # created_at для возможности добавления в список всех событий (сортировка идет по полю date)
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey(
        to=User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='authored_buckets_repairs',
        blank=True,
        null=True,
        )

    class Meta:
        verbose_name = 'Ремонт ковша'
        verbose_name_plural = 'Ремонты ковшей'
        ordering = ['-pk']

    def is_edit_allowed(self) -> bool:
        """Доступность к редактированию (только последний ремонт ковша)"""
        bucket = self.bucket
        if int(self.pk) == int(BucketRepair.objects.filter(bucket=bucket).first().pk):
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.pk:
            self.author = get_user()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.bucket.number + ' ' + self.date.strftime("%d-%m-%Y")
