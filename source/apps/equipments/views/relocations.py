from datetime import datetime
from typing import Any

from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from apps.equipments.forms import EquipmentRelocationForm, RelocationAttachmentForm
from apps.equipments.models import Equipment, EquipmentRelocation, RelocationAttachment


class EquipmentRelocationsTabView(DetailView):
    context_object_name = 'equipment'
    template_name = 'equipments/relocations/equipment_relocations_tab.html'

    def get_object(self):
        return get_object_or_404(Equipment, number=self.kwargs.get('equipment_number'))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['equipment_relocations_tab'] = True
        context['user_can_create_relocation'] = self.request.user.groups.filter(name='Перемещение оборудования').exists()
        return context


class EquipmentRelocationCreateView(CreateView):
    model = EquipmentRelocation
    form_class = EquipmentRelocationForm
    template_name = 'equipments/relocations/equipment_relocation_create.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        equipment = get_object_or_404(Equipment, number=self.kwargs.get('equipment_number'))
        context['equipment'] = equipment
        context['equipment_relocations_tab'] = True
        return context

    def form_valid(self, form):
        relocation: EquipmentRelocation = form.save(commit=False)
        equipment = get_object_or_404(Equipment, number=self.kwargs.get('equipment_number'))
        relocation.equipment = equipment
        self.relocation = relocation
        try:
            relocation.save()
            messages.success(self.request, 'Перемещение успешно добавлено!')
        except IntegrityError:
            form.add_error(None, 'Перемещение по этому приказу уже существует')
            return self.form_invalid(form)

        return redirect('equipment_relocation_update', equipment_relocation_pk=relocation.pk)


class EquipmentRelocationUpdateView(UpdateView):
    model = EquipmentRelocation
    form_class = EquipmentRelocationForm
    template_name = 'equipments/relocations/equipment_relocation_update.html'
    context_object_name = 'relocation'

    def get_object(self) -> EquipmentRelocation:
        obj = get_object_or_404(EquipmentRelocation, pk=self.kwargs.get('equipment_relocation_pk'))
        return obj

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        equipment = self.get_object().equipment
        context['equipment'] = equipment
        context['equipment_relocations_tab'] = True
        context['relocation_attachment_form'] = RelocationAttachmentForm()
        context['user_can_create_relocation'] = self.request.user.groups.filter(name='Перемещение оборудования').exists()
        return context

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, 'Перемещение по этому приказу уже существует')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('equipment_relocation_update', kwargs={'equipment_relocation_pk': self.object.pk})


class EquipmentsRelocationsListView(ListView):
    model = EquipmentRelocation
    context_object_name = 'relocations'
    template_name = 'equipments/relocations/equipments_relocations_list.html'


class EquipmentRelocationAddAttachmentView(CreateView):
    model = RelocationAttachment
    form_class = RelocationAttachmentForm

    def form_valid(self, form):
        relocation_attachment: RelocationAttachment = form.save(commit=False)
        equipment_relocation = get_object_or_404(EquipmentRelocation, pk=self.kwargs.get('equipment_relocation_pk'))
        relocation_attachment.equipment_relocation = equipment_relocation
        relocation_attachment.save()
        return redirect(self.request.META.get('HTTP_REFERER', '/'))


class EquipmentRelocationDateAddView(View):

    def post(self, request, equipment_relocation_pk, *args, **kwargs):
        relocation = get_object_or_404(EquipmentRelocation, pk=equipment_relocation_pk)
        date: str = request.POST.get('date')
        date: datetime.date = datetime.strptime(date, '%Y-%m-%d').date()
        relocation.date = date
        relocation.save()
        return redirect(self.request.META.get('HTTP_REFERER', '/'))
