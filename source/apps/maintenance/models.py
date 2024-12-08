from django.db import models


class MaintenanceCategory(models.Model):
    """Виды технического обслуживания - ТО-10, ТО-50"""
    name = models.CharField(verbose_name='Название', max_length=50, unique=True)
    running_time = models.PositiveSmallIntegerField(verbose_name='Наработка для проведения', blank=True, null=True)

    class Meta:
        verbose_name = 'Вид обслуживания'
        verbose_name_plural = 'Виды обслуживаний'
        ordering = ['running_time']

    def __str__(self):
        return self.name


class ScheduledMaintenanceWorkSystem(models.Model):
    """Системы оборудования для регламентных работ"""
    name = models.CharField(verbose_name='Название', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Система оборудования'
        verbose_name_plural = 'Системы оборудования'
        ordering = ['name']

    def __str__(self):
        return self.name


class ScheduledMaintenanceWork(models.Model):
    """Регламентные работы на обслуживание"""
    name = models.CharField(verbose_name='Название', max_length=100, unique=True)
    equipment_system = models.ForeignKey(
        to='maintenance.ScheduledMaintenanceWorkSystem',
        on_delete=models.CASCADE,
        verbose_name='Система оборудования',
        related_name='maintenance_works',
        )

    class Meta:
        verbose_name = 'Регламентная работа'
        verbose_name_plural = 'Регламентные работы'
        ordering = ['name']

    def __str__(self):
        return self.name


class EquipmentMaintenanceGroup(models.Model):
    """Группы оборудования с идентичным техническим обслуживанием"""
    name = models.CharField(verbose_name='Название', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Группа оборудования ТО'
        verbose_name_plural = 'Группы оборудования ТО'

    def __str__(self):
        return self.name


class MaintenanceCardItem(models.Model):
    """Пункты карт технического обслуживания"""
    equipment_maintenance_group = models.ForeignKey(
        to='maintenance.EquipmentMaintenanceGroup',
        on_delete=models.CASCADE,
        verbose_name='Группа оборудования ТО',
        related_name='maintenance_card_items',
        )
    maintenance_category = models.ForeignKey(
        to='maintenance.MaintenanceCategory',
        on_delete=models.CASCADE,
        verbose_name='Вид ТО',
        related_name='maintenance_card_items',
        )
    scheduled_maintenance_work = models.ForeignKey(
        to='maintenance.ScheduledMaintenanceWork',
        on_delete=models.CASCADE,
        verbose_name='Регламентная работа ТО',
        related_name='maintenance_card_items',
        )
    material_quantity = models.IntegerField(verbose_name='Количество материала', blank=True, null=True)

    class Meta:
        verbose_name = 'Пункт карт ТО'
        verbose_name_plural = 'Пункты карт ТО'
        ordering = ['maintenance_category']
        unique_together = ('equipment_maintenance_group', 'maintenance_category', 'scheduled_maintenance_work')

    def __str__(self) -> str:
        return f'{self.maintenance_category.name} - {self.scheduled_maintenance_work.name}'
