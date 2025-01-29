from datetime import date
from typing import TYPE_CHECKING, Union

from django.contrib.auth.models import User
from django.db import models

from apps.common.models import CurrentData
from apps.common.services import get_user, set_file_size, validate_scan_file
from apps.importer.models import Nomenclature, Warehouse
from apps.sites.models import Site

from .installations import ComponentDeinstallation, ComponentInstallation, ComponentInstallationLocation
from .relocation import ComponentRelocation
from .techstate import ComponentTechState


if TYPE_CHECKING:
    from apps.equipments.models import Equipment


class Component(models.Model):
    """Справочник Компоненты"""
    number = models.CharField(verbose_name='Порядковый номер', max_length=50, unique=True)
    serial_number = models.CharField(verbose_name='Серийный номер', max_length=20, blank=True, null=True, unique=True)
    component_type = models.ForeignKey(
        to='components.ComponentType',
        related_name='components',
        on_delete=models.CASCADE,
        verbose_name='Тип',
        )
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)
    requires_reconciliation = models.BooleanField(verbose_name='Требует сверки', blank=True, null=True)
    is_serial_number_marked = models.BooleanField(verbose_name='Нанесен серийный номер', default=False)
    # TODO nomenclature_code - поле должно быть уникальным
    nomenclature_code = models.CharField(verbose_name='Код номенклатуры', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural = '(Справочник) Компоненты'
        ordering = ['component_type']

    def get_relocation(self) -> ComponentRelocation | None:
        last_relocation = ComponentRelocation.objects.filter(component=self).first()
        if last_relocation:
            return last_relocation

    def get_last_relocation_date(self) -> date | None:
        relocation = self.get_relocation()
        if relocation:
            return relocation.date

    def get_location(self) -> Site | None:
        #  если компонент установлен на оборудовании, его локацию не слудет отображать
        if self.get_relocation() and not self.get_equipment():
            return self.get_relocation().to_site

    def get_equipment(self) -> Union['Equipment', None]:
        latest_installation = ComponentInstallation.objects.filter(component=self).first()
        latest_deinstallation = ComponentDeinstallation.objects.filter(component=self).first()
        if not latest_installation:
            return None
        if not latest_deinstallation:
            return latest_installation.to_equipment
        if latest_installation.date >= latest_deinstallation.date:
            return latest_installation.to_equipment
        else:
            return None

    def get_location_on_equipment(self) -> ComponentInstallationLocation | None:
        if self.get_equipment():
            equipment_installation: ComponentInstallation = self.get_installation()
            location: ComponentInstallationLocation = equipment_installation.location
            return location

    def get_installation(self) -> ComponentInstallation | ComponentDeinstallation | None:
        latest_installation = ComponentInstallation.objects.filter(component=self).first()
        latest_deinstallation = ComponentDeinstallation.objects.filter(component=self).first()
        if not latest_installation:  # вообще не было установок
            return None
        if not latest_deinstallation:  # вообще не было демонтажей, значит была только одна установка
            return latest_installation
        if latest_installation.date >= latest_deinstallation.date:
            return latest_installation
        else:
            return latest_deinstallation

    def get_compatible_equipment_models(self):
        from apps.equipments.models import EquipmentModel

        return EquipmentModel.objects.filter(componenttypeequipmentmodel__component_type=self.component_type)

    def get_compatible_installation_locations(self):
        component_type = self.component_type
        # Получаем совместимые места установки для данного типа компонента
        compatible_locations = ComponentInstallationLocation.objects.filter(
            componenttypeequipmentmodel__component_type=component_type,
        ).distinct()
        return compatible_locations

    def get_techstate(self) -> ComponentTechState | None:
        latest_techstate = ComponentTechState.objects.filter(component=self).first()
        if latest_techstate:
            return latest_techstate

    def get_is_operable(self) -> bool:
        latest_techstate = ComponentTechState.objects.filter(component=self).first()
        if latest_techstate:
            return latest_techstate.is_operable

    def get_nomenclature_from_import_data(self) -> Nomenclature | None:
        if Nomenclature.objects.filter(code=self.nomenclature_code).exists():
            return Nomenclature.objects.get(code=self.nomenclature_code)

    def get_warehouse_from_import_data(self) -> Warehouse | None:
        if self.get_nomenclature_from_import_data():
            return self.get_nomenclature_from_import_data().warehouse

    def __str__(self):
        return self.component_type.name + ' ' + self.number


class ComponentKind(models.Model):
    """Справочник видов компонентов (цилиндр, ДВС, гидромотор)"""
    name = models.CharField(verbose_name='Наименование', max_length=40, unique=True)

    class Meta:
        verbose_name = 'Вид компонента'
        verbose_name_plural = '(Справочник) Виды компонентов'
        ordering = ['name']

    def __str__(self):
        return self.name


class ComponentType(models.Model):
    """Справочник типов компонентов (цилиндр люнета ROC, гидронасос главный DM, гидронасос строенный DM)"""
    name = models.CharField(verbose_name='Наименование', max_length=60, unique=True)
    kind = models.ForeignKey(
        to='components.ComponentKind',
        related_name='components_types',
        on_delete=models.CASCADE,
        verbose_name='Вид',
        )
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)

    class Meta:
        verbose_name = 'Тип компонента'
        verbose_name_plural = '(Справочник) Типы компонентов'
        ordering = ['name']

    def __str__(self):
        return self.name


class ComponentCurrentData(CurrentData):
    """Хранение последних данных по компоненту (местоположение, оборудование, статус)"""

    component = models.OneToOneField(
        to='components.Component',
        related_name='current_data',
        on_delete=models.CASCADE,
        verbose_name='Компонент',
        unique=True,
        )
    equipment = models.ForeignKey(
        to='equipments.Equipment',
        related_name='components',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Оборудование',
        )
    installation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата установки',
    )
    component_location = models.ForeignKey(
        to='components.ComponentInstallationLocation',
        related_name='components',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Место установки',
        )
    state = models.ForeignKey(
        to='components.ComponentState',
        related_name='components',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Состояние',
        )

    class Meta:
        verbose_name = 'Текущие данные по компоненту'
        verbose_name_plural = 'Текущие данные по компонентам'
        ordering = ['component']

    def __str__(self):
        return self.component.number


class ComponentState(models.Model):
    """Статусы компонентов (в ожидании отправки, хранение)"""
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Статус компонента'
        verbose_name_plural = 'Статусы компонентов'
        ordering = ['name']

    def __str__(self):
        return self.name


def component_attachment_upload_path(instance, filename):
    return f'component/{instance.component.number}' \
           f'/{instance.attachment_type}/{filename}'


class ComponentAttachment(models.Model):
    """Файлы вложений для компонентов (шильдики, фото и др.)"""
    attachment_file = models.FileField(
        verbose_name='Файл',
        upload_to=component_attachment_upload_path,
        validators=[validate_scan_file],
    )
    component = models.ForeignKey(
        to='components.Component',
        related_name='attachments',
        verbose_name='Компонент',
        on_delete=models.CASCADE,
    )
    TYPE_CHOICES = (
        ('Шильдик', 'Шильдик'),
        ('Фото компонента', 'Фото компонента'),
    )
    attachment_type = models.CharField(
        verbose_name='Тип вложения',
        max_length=30,
        choices=TYPE_CHOICES,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='authored_component_attachments',
        )
    file_size = models.CharField(verbose_name='Размер файла', max_length=30, blank=True, null=True)
    description = models.CharField(verbose_name='Описание', max_length=70, blank=True, null=True)

    class Meta:
        verbose_name = 'Вложение компонента'
        verbose_name_plural = 'Вложения компонентов'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.author = get_user()
        set_file_size(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Вложение компонента {self.component.number}'
