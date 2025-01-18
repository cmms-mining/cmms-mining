from django.contrib import admin

from apps.firefighting.models import FirefightingCheck, FirefightingSystem


@admin.register(FirefightingSystem)
class FirefightingSystemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FirefightingSystem._meta.fields]


@admin.register(FirefightingCheck)
class FirefightingCheckAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FirefightingCheck._meta.fields]
