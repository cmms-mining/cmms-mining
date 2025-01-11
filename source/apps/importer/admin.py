from django.contrib import admin

from apps.importer.models import Nomenclature, Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Warehouse._meta.fields]


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Nomenclature._meta.fields]
