from django.contrib import admin

from apps.accounts.models import CustomGroup


@admin.register(CustomGroup)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomGroup._meta.fields]
