from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView, TemplateView

from apps.components.forms import ComponentTechStateForm
from apps.components.models import Component, ComponentTechState


class FormValidationMixin:
    def validate_form(self, form):
        new_techstate_date = self.techstate.date
        component: Component = self.techstate.component

        if component.get_techstate():
            # проверка даты, должна быть не меньше и не равна дате предыдущего техсостояния
            last_techstate_date = component.get_techstate().date
            if new_techstate_date <= last_techstate_date:
                messages.warning(
                    self.request,
                    'Дата техсостояния не может быть меньше или равна дате предыдущего техсостояния!',
                    )
                return False

        if new_techstate_date > timezone.localtime().date():
            messages.warning(self.request, 'Ошибка - дата техсостояния не может быть больше текущей даты!')
            return False

        # if component.get_is_being_repaired() and self.techstate.techstate.name == 'Ремонта не требует':
        #     messages.warning(
        #         self.request,
        #         'Ошибка - статус "Ремонта не требует" нельзя установить находящемуся в ремонте ковшу!',
        #         )
        #     return False

        if not self.techstate.is_operable and self.techstate.techstate.name == 'Ремонта не требует':
            messages.warning(
                self.request,
                'Ошибка - компонент, не требующий ремонта должен подлежать эксплуатации!',
                )
            return False

        return True


class ComponentTechStatesListView(TemplateView):
    """Список техсостояний"""
    template_name = 'components/techstates/component_techstates_tab.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['component'] = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        context['techstates_tab'] = True
        return context


class ComponentTechStatesCreateView(FormValidationMixin, CreateView):
    model = ComponentTechState
    form_class = ComponentTechStateForm
    template_name = 'components/techstates/component_techstate_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        context['component'] = component
        context['techstates_tab'] = True
        return context

    def form_valid(self, form):
        techstate: ComponentTechState = form.save(commit=False)
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        techstate.component = component
        self.techstate = techstate

        if not self.validate_form(form):
            return redirect('component_techstates_tab', component_number=component.number)

        techstate.save()
        messages.success(self.request, 'Техсостояние успешно изменено!')
        return redirect('component_techstates_tab', component_number=techstate.component.number)
