from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView

from apps.equipments.models import Equipment


class EquipmentsListView(TemplateView):
    template_name = 'equipments/equipments/equipments_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipments = Equipment.objects.filter(decommissioned=False)
        context['equipments'] = equipments
        return context


class EquipmentAllEventsView(DetailView):
    context_object_name = 'equipment'
    template_name = 'equipments/equipments/equipment_all_events_tab.html'

    def get_object(self):
        return get_object_or_404(Equipment, number=self.kwargs.get('equipment_number'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_events_tab'] = True
        return context
