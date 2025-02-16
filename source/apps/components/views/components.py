from typing import Any

from django.db.models import Count, Exists, OuterRef, Prefetch, Q, Subquery
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, TemplateView

from apps.components.models import Component, ComponentRepair, ComponentState, ComponentTask, ComponentType
from apps.importer.models import Nomenclature, Warehouse
from apps.sites.models import Site

from ..forms import ComponentStateForm
from ..services import update_component_current_data


class ComponentsListView(TemplateView):
    template_name = 'components/components_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        unverified_task_exists = ComponentTask.objects.filter(
            component=OuterRef('pk'),
            verified=False,
        )
        repairs_list = ComponentRepair.objects.filter(component=OuterRef('pk'), completed_at=None)

        warehouse_subquery = Nomenclature.objects.filter(
            code=OuterRef('nomenclature_code'),
        ).values('warehouse__name')[:1]

        nomenclature_subquery = Nomenclature.objects.filter(
            code=OuterRef('nomenclature_code'),
        ).values('name')[:1]

        components = Component.objects.prefetch_related(
            Prefetch('repairs'),
        ).annotate(
            has_unverified_task=Exists(unverified_task_exists),
            repair=Subquery(repairs_list.values('id')[:1]),
            warehouse=Subquery(warehouse_subquery),
            nomenclature=Subquery(nomenclature_subquery),
        ).values(
            'number',
            'serial_number',
            'nomenclature_code',
            'repair',
            'is_serial_number_marked',
            'requires_action',

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
            'warehouse',
            'nomenclature',
        )

        for component in components:
            location_warehouse_group = None
            warehouse_group = None
            if component.get('current_data__location__name') and component.get('warehouse'):
                location_warehouse_group = Site.objects.get(
                    name=component.get('current_data__location__name')).warehouse_group
                warehouse_group = Warehouse.objects.get(name=component.get('warehouse')).group
                if location_warehouse_group and location_warehouse_group == warehouse_group:
                    component['is_compliant_with_import_data'] = True

        context['components'] = components

        return context


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
        initial['requires_action'] = component.requires_action
        initial['note'] = component.note
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
        if form.cleaned_data['serial_number']:
            serial_number: str = form.cleaned_data['serial_number']
            component.serial_number = serial_number
        component.nomenclature_code = form.cleaned_data['nomenclature_code'] or None
        component.requires_action = form.cleaned_data['requires_action']
        component.note = form.cleaned_data['note'] or None
        component.save()

        return redirect('component_state_tab', component_number=component.number)


class ComponentsSummaryView(TemplateView):
    """Сводный отчет по компонентам"""
    template_name = 'components/components_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        components_types = ComponentType.objects.annotate(
            total_components=Count('components'),
            installed_components=Count('components', filter=Q(components__current_data__equipment__isnull=False)),
            rotable_components=Count('components', filter=Q(components__current_data__equipment__isnull=True)),
            healthy_components=Count(
                'components',
                filter=Q(components__current_data__equipment__isnull=True) &
                Q(components__current_data__state__name='Хранение'),
                ),
        )
        context['components_types'] = components_types

        return context
