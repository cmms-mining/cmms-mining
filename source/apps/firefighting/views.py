from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from apps.equipments.models import Equipment

from .forms import FirefightingCheckForm
from .models import FirefightingCheck, FirefightingSystem


class FirefightingsListView(ListView):
    context_object_name = 'firefighting_systems'
    template_name = 'firefighting/firefightings_list.html'
    model = FirefightingSystem


class FirefightingCheckCreateView(CreateView):
    model = FirefightingCheck
    form_class = FirefightingCheckForm
    template_name = 'firefighting/firefighting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipment = get_object_or_404(Equipment, number=self.kwargs.get('equipment_number'))
        context['equipment'] = equipment
        return context

    def form_valid(self, form):
        equipment = get_object_or_404(Equipment, number=self.kwargs.get('equipment_number'))
        firefighting_system = equipment.firefighting_system
        check: FirefightingCheck = form.save(commit=False)
        check.firefighting_system = firefighting_system
        check.save()
        return redirect('firefightings')


class FirefightingCheckUpdateView(UpdateView):
    model = FirefightingCheck
    form_class = FirefightingCheckForm
    template_name = 'firefighting/firefighting.html'
    success_url = reverse_lazy('firefightings')

    def get_object(self, queryset=None):
        check: FirefightingCheck = get_object_or_404(FirefightingCheck, pk=self.kwargs.get('firefighting_check_pk'))
        return check
