from typing import Any

from django.contrib import messages
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView, TemplateView

from apps.components.forms import ComponentDeinstallationForm, ComponentInstallationForm
from apps.components.models import Component, ComponentDeinstallation, ComponentInstallation, ComponentRelocation
from apps.components.services import get_combined_installs_and_deinstalls


class ComponentInstallationsTabView(TemplateView):
    template_name = 'components/installations/component_installations_tab.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        context['component'] = component

        comb_installations = get_combined_installs_and_deinstalls(component=component)
        context['comb_installations'] = comb_installations

        context['installations_tab'] = True
        return context


class FormValidationMixin:
    def validate_form(self, form):
        de_installation = self.de_installation
        component: Component = self.de_installation.component

        if isinstance(self, ComponentDeinstallationCreateView):
            if not component.get_equipment():
                messages.warning(self.request, 'Компонент не установлен на оборудовании!')
                return False

            last_installation_date = component.get_installation().date
            if de_installation.date <= last_installation_date:
                messages.warning(
                    self.request,
                    'Ошибка - дата демонтажа компонента не может быть меньше или равна дате предыдущего монтажа!',
                    )
                return False

        if isinstance(self, ComponentInstallationCreateView):

            if component.get_equipment():
                messages.warning(self.request, 'Компонент уже установлен на оборудовании!')
                return False

            if component.get_installation() and de_installation.date <= component.get_installation().date:
                messages.warning(
                    self.request,
                    'Дата установки компонента не может быть меньше или равна дате предыдущего демонтажа!',
                    )
                return False

        #     if component.get_is_being_repaired():
        #         messages.warning(
        #             self.request,
        #             'Установка находящегося в ремонте компонента невозможна!',
        #             )
        #         return False

        if de_installation.date > timezone.localtime().date():
            messages.warning(
                self.request,
                'Ошибка - дата установки не может быть больше текущей даты!',
                )
            return False

        return True


class ComponentDeinstallationCreateView(FormValidationMixin, CreateView):
    model = ComponentDeinstallation
    form_class = ComponentDeinstallationForm
    template_name = 'components/installations/component_deinstallation_create.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        context['component'] = component
        context['installations_tab'] = True
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        deinstallation: ComponentDeinstallation = form.save(commit=False)
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        deinstallation.component = component
        self.de_installation = deinstallation

        if not self.validate_form(form):
            return redirect('component_installations_tab', component_number=component.number)

        deinstallation.from_equipment = component.get_equipment()
        deinstallation.author = self.request.user
        deinstallation.save()

        if deinstallation.from_equipment.get_location():
            ComponentRelocation.objects.create(
                component=component,
                to_site=deinstallation.from_equipment.get_location(),
                date=deinstallation.date,
            )
        messages.success(self.request, 'Компонент демонтирован. Обновите техсостояние при необходимости!')
        return redirect('component_installations_tab', component_number=component.number)


class ComponentInstallationCreateView(FormValidationMixin, CreateView):
    model = ComponentInstallation
    form_class = ComponentInstallationForm
    template_name = 'components/installations/component_installation_create.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        context['component'] = component
        context['installations_tab'] = True
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        installation: ComponentInstallation = form.save(commit=False)
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        installation.component = component

        self.de_installation = installation

        if not self.validate_form(form):
            return redirect('component_installations_tab', component_number=component.number)

        installation.author = self.request.user
        installation.save()
        messages.success(self.request, 'Компонент установлен!')
        return redirect('component_installations_tab', component_number=component.number)

    # Передаем объект component в kwargs формы
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        kwargs['component'] = component
        return kwargs
