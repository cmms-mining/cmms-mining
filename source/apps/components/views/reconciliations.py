from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.components.models import Component


class ComponentReconciliationsTabView(TemplateView):
    template_name = 'components/reconciliations/component_reconciliations_tab.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        context['component'] = component
        context['reconciliations_tab'] = True
        return context
