from datetime import timedelta

from django.db import models
from django.utils import timezone

from apps.buckets.settings import DAYS_TO_BUCKETS_RECONCILIATION
from apps.common.models import CurrentData
from apps.equipments.models import Equipment
from apps.sites.models import Site

from .installations import BucketDeinstallation, BucketInstallation
from .reconciliation import BucketReconciliation
from .relocation import BucketRelocation
from .repair import BucketRepair
from .techstate import BucketTechState


class BucketCapacity(models.Model):
    """Типоразмеры ковшей"""
    capacity = models.CharField(verbose_name='Объем', max_length=10, unique=True)

    class Meta:
        verbose_name = 'Объем ковша'
        verbose_name_plural = '(Справочник) Объемы ковшей'
        ordering = ['capacity']

    def __str__(self):
        return self.capacity


class ToothAdapter(models.Model):
    """Тип адаптера зуба"""
    name = models.CharField(verbose_name='Тип адаптера', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Адаптер коронки'
        verbose_name_plural = '(Справочник) Адаптеры коронок'
        ordering = ['name']

    def __str__(self):
        return self.name


class BucketManufacturer(models.Model):
    """Производители ковшей"""
    name = models.CharField(verbose_name='Производитель', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Производитель ковша'
        verbose_name_plural = '(Справочник) Производители ковшей'
        ordering = ['name']

    def __str__(self):
        return self.name


class Bucket(models.Model):
    """Ковши"""
    # TODO сделать проверку на запретные символы, используется как slug
    number = models.CharField(verbose_name='Номер', max_length=5, unique=True)
    capacity = models.ForeignKey(
        to='buckets.BucketCapacity',
        related_name='buckets',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Объем',
        )
    tooth_adapter = models.ForeignKey(
        to='buckets.ToothAdapter',
        related_name='buckets',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Адаптер',
        )
    manufacturer = models.ForeignKey(
        to='buckets.BucketManufacturer',
        related_name='buckets',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Производитель',
        )
    production_year = models.IntegerField(verbose_name='Год выпуска', blank=True, null=True)
    nomencl_code = models.CharField(verbose_name='Код номенклатуры', max_length=15, blank=True, null=True)
    equipment_model = models.ForeignKey(
        to='equipments.EquipmentModel',
        related_name='buckets',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Модель экскаватора',
        )
    note = models.TextField(verbose_name='Примечание', blank=True, null=True)
    requires_reconciliation = models.BooleanField(verbose_name='Требует сверки', default=True)

    class Meta:
        verbose_name = 'Ковш'
        verbose_name_plural = '(Справочник) Ковши'
        ordering = ['number']

    def get_relocation(self) -> BucketRelocation | None:
        last_relocation = BucketRelocation.objects.filter(bucket=self).first()
        if last_relocation:
            return last_relocation

    def get_location(self) -> Site | None:
        if self.get_relocation():
            return self.get_relocation().to_site

    def get_techstate(self) -> BucketTechState | None:
        latest_techstate = BucketTechState.objects.filter(bucket=self).first()
        if latest_techstate:
            return latest_techstate

    def get_repair(self) -> BucketRepair | None:
        last_repair = BucketRepair.objects.filter(bucket=self).first()
        if last_repair:
            return last_repair

    def get_reconciliation(self) -> BucketReconciliation | None:
        latest_reconciliation = BucketReconciliation.objects.filter(bucket=self).first()
        if latest_reconciliation:
            return latest_reconciliation

    def get_equipment(self) -> Equipment | None:
        latest_installation = BucketInstallation.objects.filter(bucket=self).first()
        latest_deinstallation = BucketDeinstallation.objects.filter(bucket=self).first()
        if not latest_installation:
            return None
        if not latest_deinstallation:
            return latest_installation.to_equipment
        if latest_installation.date >= latest_deinstallation.date:
            return latest_installation.to_equipment
        else:
            return None

    def get_equipment_days(self) -> int | None:
        equipment = self.get_equipment()
        if equipment:
            latest_document = BucketInstallation.objects.filter(bucket=self).first()
        else:
            latest_document = BucketDeinstallation.objects.filter(bucket=self).first()
        if not latest_document:
            return None
        days = (timezone.localtime().date() - latest_document.date).days
        if days == -1:
            days = 0
        return days

    def get_installation(self) -> BucketInstallation | BucketDeinstallation | None:
        latest_installation = BucketInstallation.objects.filter(bucket=self).first()
        latest_deinstallation = BucketDeinstallation.objects.filter(bucket=self).first()
        if not latest_installation:  # вообще не было установок
            return None
        if not latest_deinstallation:  # вообще не было демонтажей, значит была только одна установка
            return latest_installation
        if latest_installation.date >= latest_deinstallation.date:
            return latest_installation
        else:
            return latest_deinstallation

    def get_is_operable(self) -> bool:
        latest_techstate = BucketTechState.objects.filter(bucket=self).first()
        if latest_techstate:
            return latest_techstate.is_operable

    def is_to_reconciliate(self) -> bool:
        date_threshold = timezone.localtime().date() - timedelta(days=DAYS_TO_BUCKETS_RECONCILIATION)
        if not self.reconciliations.filter(date__gte=date_threshold).exists():
            return True

    def get_overdue_days_to_reconciliation(self) -> int:
        """Не используется"""
        reconciliation = self.get_reconciliation()
        if not reconciliation:
            return 999

        last_reconciliation_date = self.get_reconciliation().date

        days_from_reconciliation = (timezone.localtime().date() - last_reconciliation_date).days
        overdue_days_to_reconciliation = days_from_reconciliation - DAYS_TO_BUCKETS_RECONCILIATION

        return overdue_days_to_reconciliation

    def get_is_not_operable_days(self) -> int:
        """считает, сколько времени длится последний статус not is_operable"""
        techstates = BucketTechState.objects.filter(bucket=self)
        if not techstates:
            return

        latest_techstate = techstates.first()
        if latest_techstate.is_operable:
            return

        operable_techstates = BucketTechState.objects.filter(bucket=self, is_operable=True)
        if not operable_techstates:
            wish_techstate = BucketTechState.objects.filter(bucket=self).last()

        else:
            latest_date_operable = operable_techstates.first().date
            not_operable_techstates = BucketTechState.objects.filter(date__gte=latest_date_operable, is_operable=False)
            if not_operable_techstates:
                wish_techstate = not_operable_techstates.last()
            else:
                return

        return (timezone.localtime().date() - wish_techstate.date).days

    def get_is_obsoleted(self) -> bool:
        return self.decommission.obsoleted

    def get_is_decommissioned(self) -> bool:
        return self.decommission.decommissioned

    def get_is_being_repaired(self) -> bool:
        """Определяет статус 'В ремонте' - только если указана дата начала ремонта"""
        latest_repair = BucketRepair.objects.filter(bucket=self).first()
        if not latest_repair:
            return False
        if latest_repair.end_date:
            return False
        if not latest_repair.start_date:
            return False
        return True

    def get_is_being_repaired_days(self) -> int | None:
        if not self.get_is_being_repaired:
            return None
        last_repair_start_date = self.get_repair().start_date
        if not last_repair_start_date:
            return None
        days = (timezone.localtime().date() - last_repair_start_date).days
        return days

    def is_awaiting_repair(self):
        latest_repair = BucketRepair.objects.filter(bucket=self).first()
        if not latest_repair:
            return False
        if not latest_repair.start_date and not latest_repair.end_date:
            return True
        return False

    def get_is_needs_any_repair(self) -> bool:
        if not self.get_techstate():
            return False
        if self.get_techstate().techstate.name == 'Ремонта не требует':
            return False
        if self.get_techstate().techstate.name == 'Ремонт нецелесообразен':
            return False
        return True

    def __str__(self):
        return self.number


class BucketDecommission(models.Model):
    """Списание ковшей"""
    bucket = models.OneToOneField(
        to='buckets.Bucket',
        related_name='decommission',
        on_delete=models.CASCADE,
        verbose_name='Ковш',
        )
    obsoleted = models.BooleanField(verbose_name="Выведен из эксплуатации", default=False)
    obsoleted_date = models.DateField(verbose_name='Дата вывода из эксплуатации', blank=True, null=True)
    decommissioned = models.BooleanField(verbose_name="Списан", default=False)
    decommissioned_date = models.DateField(verbose_name='Дата списания', blank=True, null=True)

    class Meta:
        verbose_name = 'Списание ковша'
        verbose_name_plural = 'Списания ковшей'
        ordering = ['bucket']

    def __str__(self):
        return self.bucket.number


class BucketCurrentData(CurrentData):
    """Хранение последних данных по ковшу (местоположение, оборудование, статус ремонта)"""

    bucket = models.OneToOneField(
        to='buckets.Bucket',
        related_name='current_data',
        on_delete=models.CASCADE,
        verbose_name='Ковш',
        unique=True,
        )
    equipment = models.OneToOneField(
        to='equipments.Equipment',
        related_name='bucket',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Оборудование',
        )

    class Meta:
        verbose_name = 'Текущие данные по ковшу'
        verbose_name_plural = 'Текущие данные по ковшам'
        ordering = ['bucket']

    def __str__(self):
        return self.bucket.number
