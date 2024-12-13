from typing import Any

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, UpdateView

from ..forms import ComponentRepairForm
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


class ComponentRepairUpdateView(UpdateView):
    form_class = ComponentRepairForm
    context_object_name = 'repair'
    template_name = 'components/repairs/component_repair_update.html'

    def get_object(self):
        obj = get_object_or_404(ComponentRepair, pk=self.kwargs.get('repair_pk'))
        return obj

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['component'] = self.object.component
        context['repairs_tab'] = True
        return context

    def form_valid(self, form):
        repair: ComponentRepair = form.save()
        return redirect('component_repairs_tab', component_number=repair.component.number)
