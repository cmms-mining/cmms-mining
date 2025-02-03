from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.components.models import ComponentInstallation
from apps.equipments.models import Equipment


class EquipmentComponentsListView(TemplateView):
    template_name = 'equipments/components/equipment_components_tab.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipment = get_object_or_404(Equipment, number=self.kwargs.get('equipment_number'))
        context['equipment'] = equipment

        components_installations = ComponentInstallation.objects.filter(to_equipment=equipment).select_related(
            'component', 'location',
        ).values('component__component_type__name', 'component__number', 'date', 'location__name')
        context['components_installations'] = components_installations

        context['components_tab'] = True
        return context
