from django.db import models
from django.db.models import UniqueConstraint

from apps.common.models import CurrentData
from apps.components.models import Component, ComponentTypeEquipmentModel
from apps.sites.models import Site

from .relocation import EquipmentRelocation


class EquipmentType(models.Model):
    """Тип оборудования (экскаваторы, бульдозеры и т.д.)"""
    name = models.CharField(verbose_name='Название', max_length=50)
    icon = models.ImageField(verbose_name='Иконка', upload_to='icons', blank=True)
    slug = models.SlugField(verbose_name='Слаг', unique=True)

    class Meta:
        verbose_name = 'Тип оборудования'
        verbose_name_plural = 'Типы оборудования'
        ordering = ['name']

    def __str__(self):
        return self.name


class EquipmentModel(models.Model):
    """Модель оборудования (SD32, EC750 и т.д.)"""
    name = models.CharField(verbose_name='Название', max_length=50, unique=True)
    equipment_type = models.ForeignKey(
        to='equipments.EquipmentType',
        on_delete=models.CASCADE,
        related_name='equipment_models',
        verbose_name='Тип оборудования',
        )
    manufacturer = models.CharField(verbose_name='Производитель', max_length=60, blank=True)

    class Meta:
        verbose_name = 'Модель оборудования'
        verbose_name_plural = 'Модели оборудования'
        ordering = ['name']

    def get_component_install_locations_number(self, component: 'Component') -> int:
        """Получить сколько мест установки имеет компонент component на оборудовании модели self"""
        component_type = component.component_type
        number = ComponentTypeEquipmentModel.objects.filter(
            component_type=component_type,
            equipment_model=self,
            ).count()
        return number

    def __str__(self):
        return self.name


class EquipmetRunningTime(models.Model):
    """Наработка оборудования (моточасы)"""

    equipment = models.ForeignKey(
        to='equipments.Equipment',
        related_name='running_times',
        on_delete=models.CASCADE,
        verbose_name='Оборудование',
        )
    date = models.DateField(verbose_name='Дата')
    running_time = models.PositiveIntegerField(verbose_name='Общая наработка')

    class Meta:
        verbose_name = 'Наработка оборудования'
        verbose_name_plural = 'Наработки оборудования'
        ordering = ['-date']
        constraints = [
            UniqueConstraint(fields=['equipment', 'date'], name='unique_equipment_date'),
        ]

    def __str__(self):
        return f'Наработка {self.equipment.number} на {self.date.strftime("%d-%m-%Y")}'


class Equipment(models.Model):
    """Оборудование (единицы техники)"""
    name = models.CharField(verbose_name='Наименование', max_length=200, blank=True, null=True)
    number = models.CharField(verbose_name='Бортовой номер', max_length=20, unique=True)
    equipment_model = models.ForeignKey(
        to='equipments.EquipmentModel',
        related_name='equipments',
        on_delete=models.CASCADE,
        verbose_name='Модель оборудования',
    )
    equipment_maintenance_group = models.ForeignKey(
        to='maintenance.EquipmentMaintenanceGroup',
        on_delete=models.CASCADE,
        related_name='equipments',
        blank=True,
        null=True,
        default=None,
        verbose_name='Группа обслуживания',
        )
    serial_number = models.CharField(verbose_name='Серийный номер', max_length=50, blank=True, null=True, unique=True)
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)
    inventory_number = models.CharField(
        verbose_name='Инвентарный номер',
        max_length=30,
        blank=True,
        null=True,
        unique=True,
        )
    decommissioned = models.BooleanField(verbose_name="Списан", default=False)

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'
        ordering = ['number']

    def is_bucket_installed(self) -> bool:
        if self.bucketinstallations.all():
            if self.bucketdeinstallations.all():
                last_install_date = self.bucketinstallations.first().date
                last_deinstall_date = self.bucketdeinstallations.first().date
                if last_install_date >= last_deinstall_date:
                    return True
            else:
                return True
        return False

    def get_bucket(self):
        if self.is_bucket_installed():
            return self.bucketinstallations.first().bucket
        return

    def get_relocation(self) -> EquipmentRelocation | None:
        last_relocation = EquipmentRelocation.objects.filter(equipment=self, date__isnull=False).first()
        if last_relocation:
            return last_relocation

    def get_location(self) -> Site | None:
        if self.get_relocation():
            return self.get_relocation().to_site

    def get_running_time(self) -> EquipmetRunningTime | None:
        last_running_time = EquipmetRunningTime.objects.filter(equipment=self).first()
        return last_running_time

    def get_components_installations(self):
        return self.componentinstallations.all()

    def __str__(self):
        if self.inventory_number:
            return f'{self.number} ({self.inventory_number})'
        return self.number


class EquipmentCurrentData(CurrentData):
    """Хранение последних данных по оборудованию (местоположение, статус ремонта)"""

    equipment = models.OneToOneField(
        to='equipments.Equipment',
        related_name='current_data',
        on_delete=models.CASCADE,
        verbose_name='Оборудование',
        unique=True,
        )

    class Meta:
        verbose_name = 'Текущие данные по оборудованию'
        verbose_name_plural = 'Текущие данные по оборудованию'
        ordering = ['equipment']

    def __str__(self):
        return self.equipment.number
