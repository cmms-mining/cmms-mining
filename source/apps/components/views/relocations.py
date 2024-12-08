from typing import Any

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView

from apps.components.forms import ComponentRelocationForm
from apps.components.models import Component, ComponentRelocation


class ComponentRelocationsTabView(DetailView):
    context_object_name = 'component'
    template_name = 'components/relocations/component_relocations_tab.html'

    def get_object(self):
        return get_object_or_404(Component, number=self.kwargs.get('component_number'))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['relocations_tab'] = True
        return context


class ComponentRelocationCreateView(CreateView):
    model = ComponentRelocation
    form_class = ComponentRelocationForm
    template_name = 'components/relocations/component_relocation_create.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        context['component'] = component
        context['relocations_tab'] = True
        return context

    # Передаем объект Site в kwargs формы
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        if component.get_relocation():
            last_site_instance = component.get_relocation().to_site
            kwargs['site_instance'] = last_site_instance
        return kwargs

    def form_valid(self, form):
        relocation: ComponentRelocation = form.save(commit=False)
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        relocation.component = component
        self.relocation = relocation
        # if not self.validate_form(form):
        #     return redirect('component_relocations_tab', component_number=component.number)

        relocation.save()
        messages.success(self.request, 'Перемещение успешно добавлено!')
        return redirect('component_relocations_tab', component_number=component.number)
