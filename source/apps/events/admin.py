from django.contrib import admin

from apps.events.models import Event, EventFile, EventType


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EventType._meta.fields]


@admin.register(EventFile)
class EventFileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EventFile._meta.fields]


class EventFileInline(admin.StackedInline):
    model = EventFile
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventFileInline]

    def save_model(self, request, obj, form, change):
        obj.save()

        for afile in request.FILES.getlist('files_multiple'):
            eventfile = EventFile(attachment_file=afile, event=obj)
            eventfile.save()


# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Event._meta.fields]