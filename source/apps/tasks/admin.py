from django.contrib import admin

from apps.tasks.models import Task, TaskComment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Task._meta.fields]
    list_filter = ('executor', 'verified')
    search_fields = ['pk']


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TaskComment._meta.fields]
