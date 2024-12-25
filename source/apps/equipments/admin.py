from django.contrib import admin

from apps.equipments.models import (Characteristic, CharacteristicGroup, CharacteristicValue, Equipment,
                                    EquipmentCurrentData, EquipmentModel, EquipmentRelocation, EquipmentType,
                                    Nameplate, RelocationAttachment, RelocationOrder)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Equipment._meta.fields]
    list_filter = ['equipment_model']
    search_fields = ['number']


@admin.register(EquipmentCurrentData)
class EquipmentCurrentDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EquipmentCurrentData._meta.fields]


@admin.register(EquipmentRelocation)
class EquipmentRelocationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EquipmentRelocation._meta.fields]


@admin.register(RelocationOrder)
class RelocationOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RelocationOrder._meta.fields]


@admin.register(RelocationAttachment)
class RelocationAttachmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RelocationAttachment._meta.fields]


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EquipmentType._meta.fields]


@admin.register(EquipmentModel)
class EquipmentModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EquipmentModel._meta.fields]


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Characteristic._meta.fields]


@admin.register(CharacteristicGroup)
class CharacteristicGroupAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CharacteristicGroup._meta.fields]


@admin.register(CharacteristicValue)
class CharacteristicValueAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CharacteristicValue._meta.fields]


@admin.register(Nameplate)
class NameplateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Nameplate._meta.fields]
    list_filter = ['equipment']
