from django.contrib import admin

from apps.common.models import DeinstallationReason, TechStateOption


@admin.register(DeinstallationReason)
class DeinstallationReasonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DeinstallationReason._meta.fields]


@admin.register(TechStateOption)
class TechStateOptionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TechStateOption._meta.fields]
