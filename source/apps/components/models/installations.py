from django.db import models
from django.db.models import Q, UniqueConstraint

from apps.common.models import Deinstallation, Installation


class ComponentInstallation(Installation):
    """Монтажи компонентов"""
    component = models.ForeignKey(
        to='components.Component',
        related_name='component_installations',
        on_delete=models.CASCADE,
        verbose_name='Компонент',
    )

    class Meta:
        verbose_name = 'Монтаж компонента'
        verbose_name_plural = 'Монтажи компонентов'
        ordering = ['-date']

    def __str__(self):
        return self.component.number + ' на ' + self.to_equipment.number


class ComponentDeinstallation(Deinstallation):
    """Демонтажи компонентов"""
    component = models.ForeignKey(
        to='components.Component',
        related_name='component_deinstallations',
        on_delete=models.CASCADE,
        verbose_name='Компонент',
    )

    class Meta:
        verbose_name = 'Демонтаж компонента'
        verbose_name_plural = 'Демонтажи компонентов'
        ordering = ['-date']

    def __str__(self):
        return self.component.number + ' с ' + self.from_equipment.number


class ComponentInstallationLocation(models.Model):
    """Справочник мест установки компонентов на оборудовании (сторона кабины, задняя сторона)"""
    name = models.CharField(max_length=100, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Место установки компонента'
        verbose_name_plural = '(Справочник) Места установки компонентов'
        ordering = ['name']

    def __str__(self):
        return self.name


class ComponentTypeEquipmentModel(models.Model):
    """Места установки компонентов (instance) на модели оборудования"""
    component_type = models.ForeignKey(
        to='components.ComponentType',
        on_delete=models.CASCADE,
        verbose_name='Тип компонента',
        related_name='equipment_models',
        )
    equipment_model = models.ForeignKey(
        to='equipments.EquipmentModel',
        on_delete=models.CASCADE,
        verbose_name='Модель оборудования',
        )
    location = models.ForeignKey(
        to='components.ComponentInstallationLocation',
        on_delete=models.CASCADE,
        verbose_name='Место установки',
        blank=True,
        null=True,
        )

    class Meta:
        verbose_name = 'Место установки компонента на модели оборудования'
        verbose_name_plural = 'Места установки компонентов на моделях оборудования'
        ordering = ['component_type']
        constraints = [
            UniqueConstraint(fields=['component_type', 'equipment_model', 'location'], name='unique_equipment_location'),
            # Уникальность для сочетания component_type и equipment_model, если location is NULL
            UniqueConstraint(
                fields=['component_type', 'equipment_model'],
                condition=Q(location__isnull=True),
                name='unique_component_and_equipment_when_location_is_null',
            ),
        ]

    def __str__(self) -> str:
        if self.location:
            return self.component_type.name + ' ' + self.equipment_model.name + ' ' + self.location.name
        return self.component_type.name + ' ' + self.equipment_model.name
