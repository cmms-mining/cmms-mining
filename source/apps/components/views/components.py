from typing import Any

from django.db.models import Exists, OuterRef, QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, ListView

from apps.components.models import Component, ComponentState, ComponentTask

from ..forms import ComponentStateForm
from ..services import update_component_current_data


class ComponentsListView(ListView):
    model = Component
    context_object_name = 'components'
    template_name = 'components/components_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        unverified_task_exists = ComponentTask.objects.filter(
            component=OuterRef('pk'),
            verified=False,
        )
        queryset = Component.objects.all(
        ).annotate(
            has_unverified_task=Exists(unverified_task_exists),
        ).values(
            'number',
            'serial_number',
            'nomenclature_code',
            'is_compliant_with_accounting',
            'component_type__name',
            'component_type__kind__name',
            'current_data__equipment__number',
            'current_data__component_location__name',
            'current_data__installation_date',
            'current_data__location__name',
            'current_data__relocation_date',
            'current_data__state__name',
            'current_data__is_operable',
            'has_unverified_task',
        )
        return queryset


class ComponentStateView(FormView):
    """Вкладка 'Текущий статус'"""
    form_class = ComponentStateForm
    context_object_name = 'component'
    template_name = 'components/component_state_tab.html'

    def get_object(self) -> Component:
        if not hasattr(self, '_object'):
            self._object = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        return self._object

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['component'] = self.get_object()
        context['state_tab'] = True
        return context

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        component = self.get_object()
        if hasattr(component, 'current_data'):
            initial['state'] = component.current_data.state
        initial['is_serial_number_marked'] = component.is_serial_number_marked
        initial['nomenclature_code'] = component.nomenclature_code
        initial['serial_number'] = component.serial_number
        initial['is_compliant_with_accounting'] = component.is_compliant_with_accounting
        return initial

    def form_valid(self, form):
        state_name: str = form.cleaned_data['state']
        state = get_object_or_404(ComponentState, name=state_name)
        component = self.get_object()
        update_component_current_data(component=component)
        component.current_data.state = state
        component.current_data.save()

        if form.cleaned_data['is_serial_number_marked']:
            is_serial_number_marked: bool = form.cleaned_data['is_serial_number_marked']
            component.is_serial_number_marked = is_serial_number_marked
        if form.cleaned_data['is_compliant_with_accounting']:
            is_compliant_with_accounting: bool = form.cleaned_data['is_compliant_with_accounting']
            component.is_compliant_with_accounting = is_compliant_with_accounting
        if form.cleaned_data['nomenclature_code']:
            nomenclature_code: str = form.cleaned_data['nomenclature_code']
            component.nomenclature_code = nomenclature_code
        if form.cleaned_data['serial_number']:
            serial_number: str = form.cleaned_data['serial_number']
            component.serial_number = serial_number

        component.save()

        return redirect('component_state_tab', component_number=component.number)
