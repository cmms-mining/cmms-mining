from typing import Any

from django.shortcuts import get_object_or_404

from django.views.generic import ListView, TemplateView

from ..models import Component, ComponentRepair


class ComponentsRepairsListView(ListView):
    model = ComponentRepair
    template_name = 'components/repairs/repairs_list.html'
    context_object_name = 'repairs'


class ComponentRepairsListView(TemplateView):
    """Список ремонтов компонента"""
    template_name = 'components/repairs/component_repairs_tab.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['component'] = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        context['repairs_tab'] = True
        return context
