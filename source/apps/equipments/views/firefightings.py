from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.equipments.models import Equipment


class FirefightingTabView(TemplateView):
    template_name = 'equipments/firefightings/firefighting_tab.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        equipment = get_object_or_404(Equipment, number=self.kwargs.get('equipment_number'))
        context['equipment'] = equipment

        context['firefighting_tab'] = True

        return context
