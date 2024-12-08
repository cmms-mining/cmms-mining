from django.contrib import admin

from apps.sites.models import Site, WorkCenter


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Site._meta.fields]


@admin.register(WorkCenter)
class WorkCenterAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WorkCenter._meta.fields]
