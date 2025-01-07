from django.contrib import admin

from apps.components.models import (Component, ComponentAttachment, ComponentCurrentData, ComponentDeinstallation,
                                    ComponentInstallation, ComponentInstallationLocation, ComponentKind,
                                    ComponentReconciliation, ComponentRelocation, ComponentRepair,
                                    ComponentRepairAttachment, ComponentState, ComponentTask, ComponentTechState,
                                    ComponentType, ComponentTypeEquipmentModel)


# -------------Компоненты------------------
@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Component._meta.fields]
    search_fields = ['number']


@admin.register(ComponentKind)
class ComponentKindAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ComponentKind._meta.fields]


@admin.register(ComponentType)
class ComponentTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ComponentType._meta.fields]


@admin.register(ComponentTypeEquipmentModel)
class ComponentTypeEquipmentModelAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ComponentTypeEquipmentModel._meta.fields]


@admin.register(ComponentCurrentData)
class ComponentCurrentDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ComponentCurrentData._meta.fields]


@admin.register(ComponentState)
class ComponentStateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ComponentState._meta.fields]


@admin.register(ComponentAttachment)
class ComponentAttachmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ComponentAttachment._meta.fields]
# -------------Компоненты------------------


# -------------Перемещения-----------------
@admin.register(ComponentRelocation)
class ComponentRelocationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ComponentRelocation._meta.fields]
# -------------Перемещения-----------------


# -------------Техсостояния-----------------
@admin.register(ComponentTechState)
class ComponentTechStateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ComponentTechState._meta.fields]
# -------------Техсостояния-----------------


# -------------Демонтажи/монтажи-----------------
@admin.register(ComponentDeinstallation)
class ComponentDeinstallationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ComponentDeinstallation._meta.fields]


@admin.register(ComponentInstallation)
class ComponentInstallationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ComponentInstallation._meta.fields]


@admin.register(ComponentInstallationLocation)
class ComponentInstallationLocationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ComponentInstallationLocation._meta.fields]
# -------------Демонтажи/монтажи-----------------


# -------------Задачи-----------------
@admin.register(ComponentTask)
class ComponentTaskAdmin(admin.ModelAdmin):
    list_display = ['component_link'] + [field.name for field in ComponentTask._meta.fields]
    list_filter = ('executor', 'completed', 'verified')

    def component_link(self, obj):
        """Ссылка на компонент"""
        from django.utils.html import format_html
        from django.urls import reverse

        url = reverse('component_state_tab', args=[obj.component.number])
        return format_html('<a href="{}">{}</a>', url, obj.component)

    component_link.short_description = 'Компонент'  # Название колонки
# -------------Задачи-----------------


# -------------Сверки-----------------
@admin.register(ComponentReconciliation)
class ComponentReconciliationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ComponentReconciliation._meta.fields]
# -------------Сверки-----------------


# -------------Ремонты-----------------
@admin.register(ComponentRepair)
class ComponentRepairAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ComponentRepair._meta.fields]


@admin.register(ComponentRepairAttachment)
class ComponentRepairAttachmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ComponentRepairAttachment._meta.fields]
# -------------Ремонты-----------------
