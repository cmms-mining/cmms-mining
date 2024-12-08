from django.contrib import admin

from apps.maintenance.models import (EquipmentMaintenanceGroup,
                                     MaintenanceCardItem, MaintenanceCategory,
                                     ScheduledMaintenanceWork,
                                     ScheduledMaintenanceWorkSystem)


@admin.register(EquipmentMaintenanceGroup)
class EquipmentMaintenanceGroupAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EquipmentMaintenanceGroup._meta.fields]


@admin.register(MaintenanceCategory)
class MaintenanceCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MaintenanceCategory._meta.fields]


@admin.register(ScheduledMaintenanceWork)
class ScheduledMaintenanceWorkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ScheduledMaintenanceWork._meta.fields]
    search_fields = ['name']


@admin.register(MaintenanceCardItem)
class MaintenanceCardItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MaintenanceCardItem._meta.fields]


@admin.register(ScheduledMaintenanceWorkSystem)
class ScheduledMaintenanceWorkSystemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ScheduledMaintenanceWorkSystem._meta.fields]
