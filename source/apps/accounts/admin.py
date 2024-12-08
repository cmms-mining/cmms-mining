from django.contrib import admin

from apps.accounts.models import CustomGroup, JobTitle, UserJobTitle


@admin.register(CustomGroup)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomGroup._meta.fields]


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in JobTitle._meta.fields]


@admin.register(UserJobTitle)
class UserJobTitleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserJobTitle._meta.fields]
