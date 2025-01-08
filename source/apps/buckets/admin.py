from django.contrib import admin

from apps.buckets.models import (
    Bucket, BucketCapacity, BucketCurrentData, BucketDecommission, BucketDeinstallation, BucketInstallation,
    BucketManufacturer, BucketReconciliation, BucketRelocation, BucketRelocationAttachment, BucketRepair,
    BucketTechState, ToothAdapter,
    )


# -------------Ковши------------------
@admin.register(Bucket)
class BucketAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bucket._meta.fields]


@admin.register(BucketCurrentData)
class BucketCurrentDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BucketCurrentData._meta.fields]
# -------------Ковши------------------


# --------Перемещения ковшей---------
@admin.register(BucketRelocation)
class BucketRelocationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BucketRelocation._meta.fields]
# --------Перемещения ковшей---------


# --------Установки ковшей---------
@admin.register(BucketInstallation)
class BucketInstallationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BucketInstallation._meta.fields]


@admin.register(BucketDeinstallation)
class BucketDeinstallationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BucketDeinstallation._meta.fields]
# --------Установки ковшей---------


# -------Техсостояние ковшей---------
@admin.register(BucketTechState)
class BucketTechStateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BucketTechState._meta.fields]
# -------Техсостояние ковшей---------


# -------Ремонты ковшей---------
@admin.register(BucketRepair)
class BucketRepairAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BucketRepair._meta.fields]
# -------Ремонты ковшей---------


# -----------Сверки ковшей-----------
@admin.register(BucketReconciliation)
class BucketReconciliationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BucketReconciliation._meta.fields]
# -----------Сверки ковшей-----------


@admin.register(BucketDecommission)
class BucketDecommissionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BucketDecommission._meta.fields]


@admin.register(BucketRelocationAttachment)
class BucketRelocationAttachmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BucketRelocationAttachment._meta.fields]


@admin.register(BucketCapacity)
class BucketCapacityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BucketCapacity._meta.fields]


@admin.register(BucketManufacturer)
class BucketManufacturerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BucketManufacturer._meta.fields]


@admin.register(ToothAdapter)
class ToothAdapterAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ToothAdapter._meta.fields]
