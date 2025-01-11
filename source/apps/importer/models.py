from django.db import models


class Warehouse(models.Model):
    """Справочник складов"""
    name = models.CharField(verbose_name='Название', max_length=50)

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = '(Справочник) Склады'
        ordering = ['name']

    def __str__(self):
        return self.name


class Nomenclature(models.Model):
    """Справочник номеклатуры"""
    name = models.CharField(verbose_name='Название', max_length=120)
    code = models.CharField(verbose_name='Код', max_length=30, unique=True)
    number = models.CharField(verbose_name='Порядковый номер', max_length=20, blank=True, null=True)
    warehouse = models.ForeignKey(
        to='importer.Warehouse',
        verbose_name='Склад',
        on_delete=models.CASCADE,
        related_name='nomenclatures',
    )

    class Meta:
        verbose_name = 'Номенклатура'
        verbose_name_plural = '(Справочник) Номенклатуры'
        ordering = ['name']

    def __str__(self):
        return self.name
