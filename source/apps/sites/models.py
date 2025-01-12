from django.db import models


class WorkCenter(models.Model):
    """Производственные участки"""
    name = models.CharField(verbose_name='Наименование', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Производтвенный участок'
        verbose_name_plural = 'Производственные участки'
        ordering = ['name']

    def __str__(self):
        return self.name


class Site(models.Model):
    """Проекты, местонахождения"""
    name = models.CharField(verbose_name='Проект', max_length=50, unique=True)
    workcenter = models.ForeignKey(
        to='sites.WorkCenter',
        related_name='sites',
        on_delete=models.CASCADE,
        verbose_name='Производственный участок',
        )
    is_contractor = models.BooleanField(verbose_name='Является подрядчиком', default=False)
    warehouse_group = models.ForeignKey(
        to='importer.WarehouseGroup',
        related_name='sites',
        on_delete=models.SET_NULL,
        verbose_name='Группа складов',
        blank=True,
        null=True,
        )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['name']

    def __str__(self):
        return self.name
