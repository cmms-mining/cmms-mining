from django.contrib.auth.models import User
from django.db.models import CharField, Value
from django.shortcuts import get_object_or_404

from apps.common.models import DeinstallationReason
from apps.components.models import (Component, ComponentCurrentData, ComponentDeinstallation, ComponentInstallation,
                                    ComponentInstallationLocation)
from apps.equipments.models import Equipment


def get_combined_installs_and_deinstalls(component: Component) -> list[dict[str, str]]:
    """Получаем все установки и демонтажи компонента"""

    installations = ComponentInstallation.objects.filter(component=component).values(
        'pk',
        'to_equipment',
        'date',
        'note',
        'author',
        'location',
    ).annotate(
            from_equipment=Value(None, output_field=CharField()),
        )

    deinstallations = ComponentDeinstallation.objects.filter(component=component).values(
        'pk',
        'from_equipment',
        'date',
        'reason',
        'note',
        'author',
    ).annotate(
            to_equipment=Value(None, output_field=CharField()),
        )

    combined_queryset = list(installations) + list(deinstallations)

    combined_queryset = sorted(combined_queryset, key=lambda x: x['date'], reverse=True)

    for item in combined_queryset:
        item['author'] = get_object_or_404(User, pk=item['author'])
        if item.get('reason'):
            item['reason'] = get_object_or_404(DeinstallationReason, pk=item['reason'])
        if item.get('to_equipment'):
            item['to_equipment'] = Equipment.objects.get(pk=item['to_equipment']).number
        if item.get('from_equipment'):
            item['from_equipment'] = Equipment.objects.get(pk=item['from_equipment']).number
        if item.get('location'):
            item['location'] = ComponentInstallationLocation.objects.get(pk=item['location'])
    return combined_queryset


def update_component_current_data(component: Component):
    current_data, created = ComponentCurrentData.objects.get_or_create(component=component)
    current_data.location = component.get_location()
    current_data.relocation_date = component.get_last_relocation_date()
    current_data.equipment = component.get_equipment()
    if component.get_installation():
        current_data.installation_date = component.get_installation().date
    current_data.component_location = component.get_location_on_equipment()
    if component.get_techstate():
        current_data.techstate = component.get_techstate().techstate
        current_data.is_operable = component.get_is_operable()
    else:
        current_data.is_operable = None
    current_data.save()
