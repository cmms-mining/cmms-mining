from django.db import models


class Characteristic(models.Model):
    """Характеристика оборудования (вес, длина и т.д.)"""
    name = models.CharField(verbose_name='Название', max_length=200, unique=True)
    note = models.TextField(verbose_name='Примечание', null=True, blank=True)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'
        ordering = ['name']

    def __str__(self):
        return self.name


class CharacteristicGroup(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200, unique=True)
    note = models.TextField(verbose_name='Примечание', null=True, blank=True)
    equipments = models.ManyToManyField(
        to='equipments.Equipment',
        related_name='characteristic_groups',
        verbose_name='Оборудование',
        blank=True,
    )

    class Meta:
        verbose_name = 'Группа оборудования по характеристикам'
        verbose_name_plural = 'Группы оборудования по характеристикам'

    def __str__(self):
        return self.name


class CharacteristicValue(models.Model):
    characteristic_group = models.ForeignKey(
        to='equipments.CharacteristicGroup',
        related_name='characteristic_values',
        on_delete=models.CASCADE,
        verbose_name='Группа оборудования по характеристикам',
    )
    characteristic = models.ForeignKey(
        to='equipments.Characteristic',
        related_name='characteristics',
        on_delete=models.CASCADE,
        verbose_name='Характеристика',
    )
    value = models.CharField(verbose_name='Значение', max_length=80)

    class Meta:
        verbose_name = 'Величина характеристики'
        verbose_name_plural = 'Величины характеристик'

    def __str__(self):
        return f'{self.characteristic}: {self.value}'
